"""
context_manager.py

Production context window manager: O(N log N) priority-queue eviction.

Fixes applied from two-round audit:
  - Correct import formatting (no concatenation)
  - Dead `import time` removed
  - Heap tuple de-duplicated: (priority, id) is sufficient; id is unique
  - Reply primer is 3 tokens (ChatML <|im_start|>assistant\\n)
  - Test window forces actual eviction (not borderline zero-eviction)
  - No false "chunk-and-merge" claims
"""

import heapq
from typing import List, Dict, Any

try:
    import tiktoken
    _TIKTOKEN_AVAILABLE = True
except ImportError:
    _TIKTOKEN_AVAILABLE = False


class ProductionContextManager:
    """
    Priority-queue context manager with O(N log N) eviction.

    Messages are evicted lowest-priority-first. Within equal priority,
    oldest messages are evicted first (FIFO via monotonic counter).
    System messages are never evicted.
    """

    def __init__(self, model_name: str = "gpt-4-0613", max_tokens: int = 4096):
        if _TIKTOKEN_AVAILABLE:
            self.encoder = tiktoken.encoding_for_model(model_name)
        else:
            self.encoder = None
        self.max_tokens = max_tokens
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

    def set_system_instructions(self, content: str) -> None:
        self.system_messages = [{"role": "system", "content": content}]

    def add_message(self, role: str, content: str, priority: int = 1) -> None:
        message = {"role": role, "content": content}
        self.history.append({
            "id": self._counter,
            "message": message,
            "priority": priority,
            "tokens": self._get_message_tokens(message),
        })
        self._counter += 1

    def get_optimized_context(self) -> List[Dict[str, str]]:
        system_tokens = sum(self._get_message_tokens(m) for m in self.system_messages)
        # 3 tokens: ChatML reply primer <|im_start|>assistant\n
        allowed = self.max_tokens - system_tokens - 3

        if allowed <= 0:
            raise ValueError("System instructions exceed token window.")

        active = {p["id"]: p for p in self.history}
        total = sum(p["tokens"] for p in self.history)

        # Heap entries: (priority, insertion_id)
        # Lower priority → evicted first. Ties broken by id (oldest = lowest id → evicted first).
        heap = [(p["priority"], p["id"]) for p in self.history]
        heapq.heapify(heap)

        while total > allowed and heap:
            _, target_id = heapq.heappop(heap)
            evicted = active.pop(target_id)
            total -= evicted["tokens"]

        surviving = sorted(active.values(), key=lambda p: p["id"])
        return list(self.system_messages) + [p["message"] for p in surviving]


if __name__ == "__main__":
    # max_tokens=25: system(5)+primer(3)=8 overhead, budget=17 history tokens
    # history needs ~35 tokens → forces 3 evictions, CRITICAL(priority=5) survives alone
    m = ProductionContextManager(max_tokens=25)
    m.set_system_instructions("Bot.")
    m.add_message("user", "Log data trace alpha...", priority=1)   # evicted 1st (oldest P1)
    m.add_message("assistant", "Alpha received.", priority=1)       # evicted 2nd (next P1)
    m.add_message("user", "CRITICAL: Bypass step 5.", priority=5)  # survives (high priority)
    m.add_message("user", "Log data trace beta...", priority=1)     # evicted 3rd (newest P1)

    result = m.get_optimized_context()
    print(f"Messages after eviction: {len(result)}")
    for msg in result:
        print(f"  [{msg['role'].upper()}]: {msg['content']}")
