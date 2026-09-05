"""
mod9_midpoint.py

5 as the arithmetic midpoint of {1,...,9} and its role in the
mod-9 constraint of the tier function T(k).

─────────────────────────────────────────────────────────────────
THEOREM [PROVEN]:
  5 = mean({1, 2, 3, 4, 5, 6, 7, 8, 9}) = 45/9

PROOF:
  sum({1,...,9}) = 9×10/2 = 45.  45/9 = 5.                    □

COMPLEMENT PAIRS [PROVEN]:
  Each pair (k, 10−k) for k = 1..4 sums to 10.
  Each pair (k, 9+1−k) for k = 1..4 has midpoint 5.
  5 is the unique self-complementary element: 10−5 = 5.

CORRECTED PROOF SKETCH (replacing the document's version):
  The original sketch "x+(9−x)=9 for all pairs" is a tautology
  that holds for all x and does not characterize 5.
  The correct characterization: 5 is the unique integer b ∈ {1,...,9}
  satisfying mean({1,...,9}) = b, equivalently 9b = sum({1,...,9}) = 45.

TIER CONNECTION [PROVEN]:
  T(k) ≡ 5 (mod 9) for all k ≥ 1  (from tier_ds_18k_distribution.py).
  So every tier value t satisfies t = 9m + 5 for some m ≥ 1.
  The midpoint 5 is the mod-9 residue locked by the tier formula.
─────────────────────────────────────────────────────────────────
"""


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


# ──────────────────────────────────────────────────────────────────────────────
# MIDPOINT OF {1,...,9}
# ──────────────────────────────────────────────────────────────────────────────

S = list(range(1, 10))
assert sum(S) == 45
assert len(S) == 9
assert sum(S) // len(S) == 5    # integer mean
# Exact mean
from fractions import Fraction
assert Fraction(sum(S), len(S)) == Fraction(5, 1)


# ──────────────────────────────────────────────────────────────────────────────
# COMPLEMENT PAIRS (summing to 10)
# ──────────────────────────────────────────────────────────────────────────────

PAIRS = [(k, 10 - k) for k in range(1, 5)]
assert PAIRS == [(1, 9), (2, 8), (3, 7), (4, 6)]
for a, b in PAIRS:
    assert a + b == 10
    assert (a + b) // 2 == 5    # midpoint = 5

# 5 is self-complementary under x ↦ 10 − x
assert 10 - 5 == 5


# ──────────────────────────────────────────────────────────────────────────────
# UNIQUENESS OF 5 AS MIDPOINT
# ──────────────────────────────────────────────────────────────────────────────

# No other element of {1,...,9} is the arithmetic mean of the set
for x in range(1, 10):
    is_mean = (9 * x == 45)
    assert is_mean == (x == 5)


# ──────────────────────────────────────────────────────────────────────────────
# CORRECTED PROOF SKETCH
# ──────────────────────────────────────────────────────────────────────────────

# The document stated: "5 is the unique solution to x+(9-x)=9 for all pairs."
# This is incorrect: x+(9-x)=9 holds for ALL x, not just x=5.
for x in range(0, 20):
    assert x + (9 - x) == 9    # true for every x — does not characterize 5


# ──────────────────────────────────────────────────────────────────────────────
# TIER CONNECTION
# ──────────────────────────────────────────────────────────────────────────────

# T(k) = DS(18k) + DS(18k-4)
def ds(n):
    return sum(int(d) for d in str(n))

def T(k):
    return ds(18 * k) + ds(18 * k - 4)

# Every T(k) ≡ 5 (mod 9) — the midpoint residue
for k in range(1, 500):
    assert T(k) % 9 == 5, f"T({k}) = {T(k)} not ≡ 5 (mod 9)"

# Tier values are 5 + 9m: they are 9-spaced elements anchored at the midpoint
TIER_VALS = [14, 23, 32, 41, 50, 59, 68]
for tv in TIER_VALS:
    assert tv % 9 == 5


# ──────────────────────────────────────────────────────────────────────────────
# OUTPUT
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Mod-9 Midpoint: 5 as mean of {1,...,9}")
    print("=" * 62)

    print(f"\n  {{1,...,9}}: sum={sum(S)}, count={len(S)}, mean={sum(S)//len(S)}")
    print(f"  5 is the unique arithmetic mean of {{1,...,9}}.")

    print(f"\n  Complement pairs (summing to 10):")
    for a, b in PAIRS:
        print(f"    ({a}, {b})  midpoint = {(a+b)//2}")
    print(f"  Self-complementary: 10−5 = 5")

    print(f"\n  Corrected proof sketch:")
    print(f"    Original: 'x+(9-x)=9 for all pairs' — tautology, all x.")
    print(f"    Correct:  5 = 45/9 = mean({{1,...,9}}).")

    print(f"\n  Tier connection:")
    print(f"    T(k) ≡ 5 (mod 9) for all k ≥ 1.")
    print(f"    Tier values = {{14, 23, 32, 41, 50, 59, 68}} = 5 + 9×{{1,...,7}}.")
    print(f"    5 is the residue locked by DS(18k)+DS(18k-4) mod 9.")

    print()
    print("All assertions passed.")
