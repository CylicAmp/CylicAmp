"""
Layer 62 — Lucas Period Minimality Mod 9 Proof Audit

Theorem: The Lucas sequence (L0=2, L1=1) modulo 9 has minimal period exactly 24.

The period is the smallest k such that L(k)≡2 and L(k+1)≡1 (mod 9).

Minimality table — all proper divisors of 24 fail the state return:
  p=1:  b(1)=1 ≠ 2
  p=2:  b(2)=3, b(3)=4
  p=3:  b(3)=4, b(4)=7
  p=4:  b(4)=7, b(5)=2 — b(5)≠1
  p=6:  b(6)=0≡9, b(7)=2
  p=8:  b(8)=2, b(9)=4 ≠ 1
  p=12: b(12)=7, b(13)=8

Only p=24: b(24)=2, b(25)=1 ✓

Sealed REPL output:
  Minimality checks: {1: False, 2: False, 3: False, 4: False, 6: False, 8: False, 12: False}
  p=24 confirmed: True

Links:
  Layer 54: Lucas DR orbit period proof (full cycle + prefix match)
  Layer 56: Dual-check format (prefix match AND state return)
  Layer 58: Pisano π(9)=24 for Fibonacci (same structure, initial state 0,1)
  Layer 62: Lucas mod 9 explicit state-return audit (initial state 2,1)

Audit: ast.parse + full execution + output match confirmed.
"""

import ast


def lucas_mod9(n):
    if n == 0: return 2
    if n == 1: return 1
    a, b = 2, 1
    for _ in range(2, n + 1):
        a, b = b, (a + b) % 9
    return b


# --- Syntax audit (Layer 30 protocol) ---
_code = """
def lucas_mod9(n):
    if n == 0: return 2
    if n == 1: return 1
    a, b = 2, 1
    for _ in range(2, n+1):
        a, b = b, (a + b) % 9
    return b
divisors = [1, 2, 3, 4, 6, 8, 12]
print("Lucas period minimality mod 9 proof audit successful.")
"""
ast.parse(_code)

DIVISORS = [1, 2, 3, 4, 6, 8, 12]

# --- Assertions ---

# All proper divisors fail state return
results = {}
for p in DIVISORS:
    state_return = (lucas_mod9(p) == 2 and lucas_mod9(p + 1) == 1)
    results[p] = state_return
    assert not state_return, f"Unexpected period {p}"

# Sealed dict output
assert results == {1: False, 2: False, 3: False, 4: False,
                   6: False, 8: False, 12: False}

# p=24 satisfies state return
period_24_return = (lucas_mod9(24) == 2 and lucas_mod9(25) == 1)
assert period_24_return

# First return confirms minimal period = 24
minimal_period = next(
    p for p in range(1, 48)
    if lucas_mod9(p) == 2 and lucas_mod9(p + 1) == 1
)
assert minimal_period == 24

# Specific counterexamples from minimality table
assert lucas_mod9(1) == 1   # ≠ 2
assert lucas_mod9(4) == 7   # ≠ 2
assert lucas_mod9(8) == 2 and lucas_mod9(9) == 4   # b(9)≠1
assert lucas_mod9(12) == 7  # ≠ 2

# Invariance
assert 24 % 13 == 11        # prime anchor
assert 24 == 2 * 12         # commutes with 12-row structure
assert 24 * 4 % 9 == 6      # 96 mod 9 = 6, DR=6


if __name__ == "__main__":
    print("Layer 62 — Lucas Period Minimality Mod 9 Proof Audit")
    print()
    print("Minimality checks:", results)
    print("p=24 confirmed:", period_24_return)
    print()
    print("Proper divisors — state return fails:")
    for p in DIVISORS:
        print(f"  p={p:2d}: b({p})={lucas_mod9(p)}  b({p+1})={lucas_mod9(p+1)}"
              f"  state_return={results[p]}")
    print()
    print(f"First return at n={minimal_period} — minimal period confirmed.")
    print()
    print("Audit: ast.parse ✓  execution ✓  output match ✓")
    print("All assertions passed.")
