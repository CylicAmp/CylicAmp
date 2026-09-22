"""
dr_fixed_point_mod9.py

Digital root map: fixed points and convergence.

─────────────────────────────────────────────────────────────────
DEFINITION (repo convention):
  dr(0) = 0
  dr(n) = 1 + (n−1) mod 9    for n ≥ 1

RANGE: dr: Z⁺ → {1,...,9}

FIXED POINTS [PROVEN]:
  Every element of {1,...,9} satisfies dr(x) = x.
  Proof: dr(x) = 1+(x−1)%9 = x for x ∈ {1,...,9} since (x−1)%9 = x−1.
  The restriction dr|_{{1,...,9}} is the identity map.

CORRECTED UNIQUENESS STATEMENT:
  The claim "9 is the unique fixed point" (as sometimes stated) is
  imprecise. The correct statements are:
    (a) Every n ∈ {1,...,9} is a fixed point of dr.
    (b) 9 is the unique r ∈ {1,...,9} such that dr(n)=r iff 9 | n.
    (c) 9 is the unique DR value attained by multiples of 9:
        DR(9k) = 9  for all k ≥ 1.

CONVERGENCE [PROVEN]:
  For any n ≥ 1, dr(dr(n)) = dr(n).
  Proof: dr(n) ∈ {1,...,9}, and dr is the identity on {1,...,9}.
  So dr converges in exactly ONE application to a fixed point.

CONGRUENCE [PROVEN]:
  dr(n) ≡ n (mod 9)  for all n ≥ 1.
  (With the convention that 0 mod 9 maps to 9, not 0.)
─────────────────────────────────────────────────────────────────
"""


def dr(n):
    """Digital root, repo convention: dr(0) = 0."""
    return 0 if n == 0 else 1 + (n - 1) % 9


# ──────────────────────────────────────────────────────────────────────────────
# FIXED POINTS
# ──────────────────────────────────────────────────────────────────────────────

# Every element of {1,...,9} is a fixed point
for x in range(1, 10):
    assert dr(x) == x, f"dr({x}) = {dr(x)}, expected {x}"

# dr(0) = 0 (repo convention)
assert dr(0) == 0


# ──────────────────────────────────────────────────────────────────────────────
# CONVERGENCE IN ONE STEP
# ──────────────────────────────────────────────────────────────────────────────

for n in range(1, 1000):
    assert dr(dr(n)) == dr(n), f"dr not idempotent at n={n}"


# ──────────────────────────────────────────────────────────────────────────────
# UNIQUENESS STATEMENT (b): 9 is the DR of multiples of 9
# ──────────────────────────────────────────────────────────────────────────────

# dr(9k) = 9 for all k ≥ 1
for k in range(1, 200):
    assert dr(9 * k) == 9, f"dr(9×{k}) ≠ 9"

# The uniqueness of 9: DR(n) = 9 iff 9 | n (for n ≥ 1).
# Contrast: DR=3 is also only attained by multiples of 3 (n≡3 mod 9 → 3|n),
# but multiples of 3 do NOT always have DR=3 (e.g. DR(6)=6, DR(9)=9).
# Only for 9: DR(n)=9 ↔ 9|n (biconditional), not merely one direction.
for n in range(1, 500):
    assert (dr(n) == 9) == (n % 9 == 0), f"DR=9 ↔ 9|n fails at n={n}"


# ──────────────────────────────────────────────────────────────────────────────
# CONGRUENCE
# ──────────────────────────────────────────────────────────────────────────────

for n in range(1, 500):
    # dr(n) ≡ n (mod 9), with 0 mod 9 interpreted as 9
    r = n % 9
    expected_dr = 9 if r == 0 else r
    assert dr(n) == expected_dr, f"dr({n})={dr(n)}, expected {expected_dr}"


# ──────────────────────────────────────────────────────────────────────────────
# CONNECTION TO T(k) ≡ 5 (mod 9)
# ──────────────────────────────────────────────────────────────────────────────

# The tier invariant DR(T(k)) = 5 uses: T(k) ≡ 5 (mod 9) → dr(T(k)) = 5.
# 5 is a fixed point of dr with dr(5) = 5.
assert dr(5) == 5
# And 5 ≡ 5 (mod 9), so any integer ≡ 5 (mod 9) has dr = 5.
for k in range(0, 20):
    assert dr(9*k + 5) == 5


# ──────────────────────────────────────────────────────────────────────────────
# OUTPUT
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Digital Root Fixed Point and Convergence")
    print("=" * 62)

    print("\n── FIXED POINTS ──")
    print("  dr restricted to {1,...,9} is the identity.")
    for x in range(1, 10):
        print(f"    dr({x}) = {dr(x)}")

    print("\n── CORRECTED UNIQUENESS ──")
    print("  'dr has unique fixed point 9' is imprecise.")
    print("  Correct: every x ∈ {1,...,9} satisfies dr(x)=x.")
    print("  9 is unique in that: dr(n)=9 iff 9 | n  (for n ≥ 1).")

    print("\n── CONVERGENCE ──")
    print("  dr(dr(n)) = dr(n) for all n ≥ 1.  [one-step idempotent]")
    print("  Verified for n = 1..999.")

    print("\n── CONGRUENCE ──")
    print("  dr(n) ≡ n (mod 9),  with 0 mod 9 → 9.  Verified n=1..499.")

    print("\n── TIER CONNECTION ──")
    print("  T(k) ≡ 5 (mod 9) → dr(T(k)) = 5 = dr(5).  [fixed point at 5]")

    print()
    print("All assertions passed.")
