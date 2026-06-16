"""
context_manager.py

Production context window manager: O(N log N) priority-queue eviction.

Fixes applied from two-round audit:
  - Correct import formatting (no concatenation)
  - Dead `import time` removed
  - Heap tuple de-duplicated: (priority, id) is sufficient; id is unique
  - Reply primer is 3 tokens (ChatML <|im_start|>assistant\n)
  - Test window forces actual eviction (not borderline zero-eviction)
  - No false "chunk-and-merge" claims

Hardening applied from third-round review:
  - TOKEN_SAFETY_MARGIN guards against serialization overhead drift
  - add_message enforces oversized-message policy (reject/truncate/raise)
  - Post-eviction assertions catch silent accounting bugs
  - Lazy-deletion guard added for future priority-mutation support
  - Heap priorities are immutable post-insertion (assumption documented)

Complexity: O(N + K log N + M log M) = O(N log N) worst case.
Eviction is a greedy approximation to 0/1 knapsack (not globally optimal).
Counterexample: A(100tok,p=3), B+C(51tok each,p=2), budget=102
  → heap keeps A (utility=3); optimal keeps B+C (utility=4).
"""

import heapq
from enum import Enum
from typing import List, Dict, Any, Optional

try:
    import tiktoken
    _TIKTOKEN_AVAILABLE = True
except ImportError:
    _TIKTOKEN_AVAILABLE = False

# Extra tokens reserved beyond the ChatML primer to absorb serialization
# overhead drift across model families and serialization layers.
TOKEN_SAFETY_MARGIN = 32


class OversizedPolicy(Enum):
    RAISE = "raise"       # raise ValueError immediately
    DROP = "drop"         # silently discard the message
    TRUNCATE = "truncate" # keep as many chars as fit (lossy)


class ProductionContextManager:
    """
    Priority-queue context manager with O(N log N) eviction.

    Messages are evicted lowest-priority-first. Within equal priority,
    oldest messages are evicted first (FIFO via monotonic counter).
    System messages are never evicted.

    Heap entries are immutable after insertion. If priority mutation is
    added later, use lazy deletion:
        _, target_id = heapq.heappop(heap)
        if target_id not in active:
            continue  # stale entry — skip
    """

    def __init__(
        self,
        model_name: str = "gpt-4-0613",
        max_tokens: int = 4096,
        oversized_policy: OversizedPolicy = OversizedPolicy.RAISE,
        safety_margin: int = TOKEN_SAFETY_MARGIN,
    ):
        if _TIKTOKEN_AVAILABLE:
            self.encoder = tiktoken.encoding_for_model(model_name)
        else:
            self.encoder = None
        self.max_tokens = max_tokens
        self.oversized_policy = oversized_policy
        self.safety_margin = safety_margin
        self.system_messages: List[Dict[str, str]] = []
        self.history: List[Dict[str, Any]] = []
        self._counter = 0

    def _count_tokens(self, text: str) -> int:
        if self.encoder is not None:
            return len(self.encoder.encode(text))
        return max(1, len(text) // 4)  # fallback approximation

    def _get_message_tokens(self, message: Dict[str, str]) -> int:
        # +4: ChatML overhead per message (3 framing + 1 trailer)
        return self._count_tokens(message["content"]) + 4

    def _usable_budget(self) -> int:
        system_tokens = sum(self._get_message_tokens(m) for m in self.system_messages)
        # 3: ChatML reply primer <|im_start|>assistant\n
        return self.max_tokens - system_tokens - 3 - self.safety_margin

    def set_system_instructions(self, content: str) -> None:
        self.system_messages = [{"role": "system", "content": content}]

    def add_message(
        self,
        role: str,
        content: str,
        priority: int = 1,
    ) -> None:
        """
        Add a message. Oversized messages are handled per oversized_policy:
          RAISE    — ValueError; caller must handle
          DROP     — message silently discarded
          TRUNCATE — content truncated to fit (lossy; log this in production)
        """
        budget = self._usable_budget()
        message = {"role": role, "content": content}
        tok = self._get_message_tokens(message)

        if tok > budget:
            if self.oversized_policy is OversizedPolicy.RAISE:
                raise ValueError(
                    f"Message alone ({tok} tokens) exceeds usable budget ({budget}). "
                    f"Define an oversized policy: DROP or TRUNCATE."
                )
            elif self.oversized_policy is OversizedPolicy.DROP:
                return
            elif self.oversized_policy is OversizedPolicy.TRUNCATE:
                # Binary-search for the longest prefix that fits within budget
                lo, hi = 0, len(content)
                while lo < hi:
                    mid = (lo + hi + 1) // 2
                    if self._get_message_tokens({"role": role, "content": content[:mid]}) <= budget:
                        lo = mid
                    else:
                        hi = mid - 1
                content = content[:lo]
                message = {"role": role, "content": content}
                tok = self._get_message_tokens(message)

        self.history.append({
            "id": self._counter,
            "message": message,
            "priority": priority,
            "tokens": tok,
        })
        self._counter += 1

    def get_optimized_context(self) -> List[Dict[str, str]]:
        allowed = self._usable_budget()

        if allowed <= 0:
            raise ValueError("System instructions + margin exceed token window.")

        active = {p["id"]: p for p in self.history}
        total = sum(p["tokens"] for p in self.history)

        # (priority, insertion_id): lower priority → evicted first.
        # Ties broken by id: oldest (lowest id) evicted first.
        heap = [(p["priority"], p["id"]) for p in self.history]
        heapq.heapify(heap)

        while total > allowed and heap:
            _, target_id = heapq.heappop(heap)
            # Lazy-deletion guard: skip if already removed (safe no-op now;
            # required if priority mutation is ever added).
            if target_id not in active:
                continue
            evicted = active.pop(target_id)
            total -= evicted["tokens"]

        surviving = sorted(active.values(), key=lambda p: p["id"])

        # Post-eviction invariant checks
        assert len(surviving) == len(active), "active_packets count mismatch"
        assert total <= allowed, (
            f"Token budget violated after eviction: {total} > {allowed}"
        )

        return list(self.system_messages) + [p["message"] for p in surviving]


if __name__ == "__main__":
    print("--- Normal eviction (CRITICAL survives) ---")
    m = ProductionContextManager(max_tokens=25, safety_margin=0)
    m.set_system_instructions("Bot.")
    m.add_message("user", "Log data trace alpha...", priority=1)
    m.add_message("assistant", "Alpha received.", priority=1)
    m.add_message("user", "CRITICAL: Bypass step 5.", priority=5)
    m.add_message("user", "Log data trace beta...", priority=1)
    result = m.get_optimized_context()
    print(f"Messages: {len(result)}")
    for msg in result:
        print(f"  [{msg['role'].upper()}]: {msg['content']}")

    print("\n--- Oversized message: RAISE ---")
    m2 = ProductionContextManager(max_tokens=20, safety_margin=0,
                                   oversized_policy=OversizedPolicy.RAISE)
    m2.set_system_instructions("Bot.")
    try:
        m2.add_message("user", "A" * 200, priority=1)
        print("  ERROR: should have raised")
    except ValueError as e:
        print(f"  Correctly raised: {e}")

    print("\n--- Oversized message: TRUNCATE ---")
    m3 = ProductionContextManager(max_tokens=20, safety_margin=0,
                                   oversized_policy=OversizedPolicy.TRUNCATE)
    m3.set_system_instructions("Bot.")
    m3.add_message("user", "A" * 200, priority=1)
    result3 = m3.get_optimized_context()
    print(f"  Messages: {len(result3)}")
    print(f"  Content length after truncation: {len(result3[-1]['content'])}")
