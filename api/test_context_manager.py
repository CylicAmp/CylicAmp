"""
test_context_manager.py

Unit tests for ProductionContextManager (api/context_manager.py).

Coverage:
  - Token budget arithmetic (_usable_budget)
  - set_system_instructions
  - add_message: normal, RAISE, DROP, TRUNCATE
  - get_optimized_context: eviction by priority, FIFO tiebreak, system messages preserved
  - Post-eviction invariants (total <= allowed, survivors sorted by id)
  - Knapsack suboptimality counterexample (greedy A > optimal B+C scenario)
  - OversizedPolicy.DROP leaves history empty
  - Empty history returns only system messages
"""

import sys
import os
import pytest

# Allow import without package install
sys.path.insert(0, os.path.dirname(__file__))

from context_manager import ProductionContextManager, OversizedPolicy, TOKEN_SAFETY_MARGIN


# ---------------------------------------------------------------------------
# Helper: manager with no tiktoken (pure fallback arithmetic)
# ---------------------------------------------------------------------------

def make_cm(max_tokens=200, policy=OversizedPolicy.RAISE, safety_margin=0,
            system="S"):
    """Return a manager with a fixed system prompt and deterministic token counts."""
    cm = ProductionContextManager(
        model_name="gpt-4-0613",
        max_tokens=max_tokens,
        oversized_policy=policy,
        safety_margin=safety_margin,
    )
    cm.encoder = None  # force fallback: len(text)//4
    if system:
        cm.set_system_instructions(system)
    return cm


def fallback_tokens(text: str) -> int:
    return max(1, len(text) // 4)


def msg_tokens(text: str) -> int:
    return fallback_tokens(text) + 4


# ---------------------------------------------------------------------------
# 1. Usable budget arithmetic
# ---------------------------------------------------------------------------

class TestUsableBudget:
    def test_no_system(self):
        cm = make_cm(max_tokens=100, system=None, safety_margin=0)
        # No system messages: usable = 100 - 0 - 3 - 0 = 97
        assert cm._usable_budget() == 97

    def test_with_system(self):
        system_text = "Bot."
        cm = make_cm(max_tokens=100, system=system_text, safety_margin=0)
        sys_tok = msg_tokens(system_text)   # fallback_tokens("Bot.")+4 = 1+4 = 5
        expected = 100 - sys_tok - 3 - 0
        assert cm._usable_budget() == expected

    def test_safety_margin_applied(self):
        cm = make_cm(max_tokens=100, system=None, safety_margin=TOKEN_SAFETY_MARGIN)
        # 100 - 0 - 3 - 32 = 65
        assert cm._usable_budget() == 65

    def test_budget_negative_when_system_huge(self):
        cm = make_cm(max_tokens=10, system="A" * 200, safety_margin=0)
        assert cm._usable_budget() < 0

    def test_get_optimized_context_raises_on_negative_budget(self):
        cm = make_cm(max_tokens=10, system="A" * 200, safety_margin=0)
        with pytest.raises(ValueError, match="System instructions"):
            cm.get_optimized_context()


# ---------------------------------------------------------------------------
# 2. set_system_instructions
# ---------------------------------------------------------------------------

class TestSetSystemInstructions:
    def test_replaces_previous(self):
        cm = make_cm(max_tokens=200, system=None)
        cm.set_system_instructions("First.")
        cm.set_system_instructions("Second.")
        ctx = cm.get_optimized_context()
        assert len(cm.system_messages) == 1
        assert cm.system_messages[0]["content"] == "Second."

    def test_system_message_always_first(self):
        cm = make_cm(max_tokens=200, system="Sys.")
        cm.add_message("user", "Hello", priority=1)
        ctx = cm.get_optimized_context()
        assert ctx[0]["role"] == "system"
        assert ctx[0]["content"] == "Sys."


# ---------------------------------------------------------------------------
# 3. add_message — oversized policy
# ---------------------------------------------------------------------------

class TestAddMessageOversized:
    def test_normal_message_accepted(self):
        cm = make_cm(max_tokens=100, system="S", safety_margin=0)
        cm.add_message("user", "Hi", priority=1)
        assert len(cm.history) == 1

    def test_raise_on_oversized(self):
        # Budget ~ 100 - msg_tokens("S") - 3 = 100 - 5 - 3 = 92
        # "A"*400 → fallback=100, +4=104 > 92
        cm = make_cm(max_tokens=100, system="S", safety_margin=0,
                     policy=OversizedPolicy.RAISE)
        with pytest.raises(ValueError, match="exceeds usable budget"):
            cm.add_message("user", "A" * 400, priority=1)

    def test_drop_on_oversized(self):
        cm = make_cm(max_tokens=100, system="S", safety_margin=0,
                     policy=OversizedPolicy.DROP)
        cm.add_message("user", "A" * 400, priority=1)
        assert len(cm.history) == 0

    def test_truncate_on_oversized(self):
        # Budget ~ 92 tokens (see above). Truncated content must fit.
        cm = make_cm(max_tokens=100, system="S", safety_margin=0,
                     policy=OversizedPolicy.TRUNCATE)
        cm.add_message("user", "A" * 400, priority=1)
        assert len(cm.history) == 1
        content = cm.history[0]["message"]["content"]
        actual_tokens = msg_tokens(content)
        assert actual_tokens <= cm._usable_budget()

    def test_truncate_produces_longest_fitting_prefix(self):
        cm = make_cm(max_tokens=100, system="S", safety_margin=0,
                     policy=OversizedPolicy.TRUNCATE)
        cm.add_message("user", "B" * 400, priority=1)
        content = cm.history[0]["message"]["content"]
        budget = cm._usable_budget()
        # Extending by 4 chars should exceed budget (binary-search is tight)
        extended_tok = msg_tokens(content + "BBBB")
        assert extended_tok > budget or len(content) == 400, (
            "Truncation did not find the longest fitting prefix"
        )


# ---------------------------------------------------------------------------
# 4. get_optimized_context — eviction behavior
# ---------------------------------------------------------------------------

class TestEviction:
    def test_no_eviction_when_fits(self):
        cm = make_cm(max_tokens=200, system="S", safety_margin=0)
        cm.add_message("user", "Hi", priority=1)
        cm.add_message("assistant", "Hello", priority=1)
        ctx = cm.get_optimized_context()
        # system + 2 history messages
        assert len(ctx) == 3

    def test_low_priority_evicted_first(self):
        # max_tokens=25, safety_margin=0
        # system "Bot." → sys_tok=5, budget=25-5-3=17
        # Add 3 messages, only the high-priority one should survive after eviction.
        cm = make_cm(max_tokens=25, system="Bot.", safety_margin=0)
        # "Log data trace alpha..." → len=22, fallback=5, +4=9 tokens, priority=1
        cm.add_message("user", "Log data trace alpha...", priority=1)
        # "Alpha received." → len=16, fallback=4, +4=8 tokens, priority=1
        cm.add_message("assistant", "Alpha received.", priority=1)
        # "CRITICAL: Bypass step 5." → len=25, fallback=6, +4=10 tokens, priority=5
        cm.add_message("user", "CRITICAL: Bypass step 5.", priority=5)
        # Total = 9+8+10=27 > 17. Must evict p=1 messages to reach ≤17.
        ctx = cm.get_optimized_context()
        contents = [m["content"] for m in ctx]
        assert "CRITICAL: Bypass step 5." in contents, "High-priority message must survive"

    def test_system_messages_never_evicted(self):
        cm = make_cm(max_tokens=25, system="Bot.", safety_margin=0)
        cm.add_message("user", "A" * 30, priority=1)
        cm.add_message("user", "B" * 30, priority=2)
        ctx = cm.get_optimized_context()
        assert ctx[0]["role"] == "system"
        assert ctx[0]["content"] == "Bot."

    def test_fifo_tiebreak_oldest_evicted_first(self):
        # Equal priority: first inserted is evicted before later inserted.
        cm = make_cm(max_tokens=30, system="S", safety_margin=0)
        # budget = 30 - msg_tokens("S") - 3 = 30 - 5 - 3 = 22
        # "First" → len=5, fallback=1, +4=5 tokens
        # "Second" → len=6, fallback=1, +4=5 tokens
        # "Third!" → len=6, fallback=1, +4=5 tokens
        # Total = 15 ≤ 22 — so let's use bigger tokens with longer strings
        # "AAAA..." × N approach: fill up so eviction is forced.
        # Use budget=22; insert two 10-token messages (each ~"XXXXXXXXXX"×24=60 chars → 15 fallback+4=19 tok)
        # Actually: fallback = max(1, len//4), so 80 chars → 20 tokens, +4=24 > 22.
        # Let's use 64 chars → 16 tok, +4=20. Two such = 40 > 22. One fits (20 ≤ 22).
        text_a = "A" * 64    # 20 tokens
        text_b = "B" * 64    # 20 tokens
        cm.add_message("user", text_a, priority=3)
        cm.add_message("user", text_b, priority=3)
        ctx = cm.get_optimized_context()
        contents = [m["content"] for m in ctx if m["role"] != "system"]
        assert text_b in contents, "Newer message (B) should survive"
        assert text_a not in contents, "Older message (A) should be evicted"

    def test_post_eviction_token_budget_satisfied(self):
        cm = make_cm(max_tokens=25, system="Bot.", safety_margin=0)
        cm.add_message("user", "Log data trace alpha...", priority=1)
        cm.add_message("assistant", "Alpha received.", priority=1)
        cm.add_message("user", "CRITICAL: Bypass step 5.", priority=5)
        cm.add_message("user", "Log data trace beta...", priority=1)
        ctx = cm.get_optimized_context()
        # Recount surviving tokens
        total = sum(
            cm._get_message_tokens(m) for m in ctx if m["role"] != "system"
        )
        assert total <= cm._usable_budget()

    def test_survivors_ordered_by_insertion(self):
        cm = make_cm(max_tokens=200, system="S", safety_margin=0)
        cm.add_message("user", "First", priority=1)
        cm.add_message("assistant", "Second", priority=2)
        cm.add_message("user", "Third", priority=1)
        ctx = cm.get_optimized_context()
        non_sys = [m["content"] for m in ctx if m["role"] != "system"]
        assert non_sys == ["First", "Second", "Third"]

    def test_empty_history_returns_system_only(self):
        cm = make_cm(max_tokens=100, system="Bot.", safety_margin=0)
        ctx = cm.get_optimized_context()
        assert len(ctx) == 1
        assert ctx[0]["role"] == "system"
        assert ctx[0]["content"] == "Bot."

    def test_all_evicted_when_necessary(self):
        # max_tokens=9, system="S" → sys_tok=5, budget=9-5-3=1.
        # Any user message has token count ≥ 5 (1 content + 4 overhead) > 1.
        # DROP policy silently discards oversized messages at add time.
        # get_optimized_context sees empty history → returns system only.
        cm = make_cm(max_tokens=9, system="S", safety_margin=0,
                     policy=OversizedPolicy.DROP)
        cm.add_message("user", "Hello", priority=1)
        assert len(cm.history) == 0, "DROP should have discarded the oversized message"
        ctx = cm.get_optimized_context()
        assert len(ctx) == 1  # only system


# ---------------------------------------------------------------------------
# 5. Greedy knapsack suboptimality counterexample
# ---------------------------------------------------------------------------

class TestKnapsackSuboptimality:
    """
    Documented counterexample:
      A  (100 tok, p=3)
      B  ( 51 tok, p=2)
      C  ( 51 tok, p=2)
      budget = 102

    Heap eviction: evicts B then C (lower priority) → keeps A (utility=3).
    Optimal: keep B+C (102 tok, utility=4).
    Greedy utility 3 < optimal utility 4.
    """

    def _build_cm_with_direct_entries(self, budget):
        """Inject history entries directly to bypass token approximation."""
        cm = ProductionContextManager(max_tokens=1000, safety_margin=0)
        cm.encoder = None
        cm.system_messages = []
        # Patch _usable_budget to return exactly `budget`
        cm._usable_budget = lambda: budget
        return cm

    def test_greedy_chooses_A_not_BC(self):
        cm = self._build_cm_with_direct_entries(budget=102)
        # Inject entries directly with known token counts
        cm.history = [
            {"id": 0, "message": {"role": "user", "content": "A"}, "priority": 3, "tokens": 100},
            {"id": 1, "message": {"role": "user", "content": "B"}, "priority": 2, "tokens": 51},
            {"id": 2, "message": {"role": "user", "content": "C"}, "priority": 2, "tokens": 51},
        ]
        cm._counter = 3
        ctx = cm.get_optimized_context()
        contents = [m["content"] for m in ctx]
        # Greedy keeps A (evicts B and C because p=2 < p=3)
        assert "A" in contents
        assert "B" not in contents
        assert "C" not in contents

    def test_optimal_would_choose_BC(self):
        # Verify that B+C together satisfy the budget where A+B or A+C do not
        assert 51 + 51 <= 102   # B+C fit
        assert 100 + 51 > 102   # A+B do not fit
        assert 100 + 51 > 102   # A+C do not fit
        # Greedy utility (keep A) = 3 < optimal utility (keep B+C) = 2+2 = 4
        assert 3 < 4

    def test_greedy_total_tokens_valid(self):
        cm = self._build_cm_with_direct_entries(budget=102)
        cm.history = [
            {"id": 0, "message": {"role": "user", "content": "A"}, "priority": 3, "tokens": 100},
            {"id": 1, "message": {"role": "user", "content": "B"}, "priority": 2, "tokens": 51},
            {"id": 2, "message": {"role": "user", "content": "C"}, "priority": 2, "tokens": 51},
        ]
        cm._counter = 3
        ctx = cm.get_optimized_context()
        # A alone = 100 ≤ 102: invariant holds
        total = sum(
            entry["tokens"] for entry in cm.history
            if entry["message"]["content"] in [m["content"] for m in ctx]
        )
        assert total <= 102


# ---------------------------------------------------------------------------
# 6. Counter monotonicity
# ---------------------------------------------------------------------------

class TestCounter:
    def test_counter_increments(self):
        cm = make_cm(max_tokens=200, system="S", safety_margin=0)
        assert cm._counter == 0
        cm.add_message("user", "A", priority=1)
        assert cm._counter == 1
        cm.add_message("user", "B", priority=1)
        assert cm._counter == 2

    def test_drop_does_not_increment_counter(self):
        cm = make_cm(max_tokens=10, system="S", safety_margin=0,
                     policy=OversizedPolicy.DROP)
        cm.add_message("user", "A" * 400, priority=1)
        assert cm._counter == 0


if __name__ == "__main__":
    import unittest
    # Run all tests via pytest when invoked directly
    import subprocess
    result = subprocess.run(
        ["python", "-m", "pytest", __file__, "-v"],
        capture_output=False,
    )
    raise SystemExit(result.returncode)
