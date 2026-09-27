"""
ds_congruence_mod9.py

Digit sum congruence: DS(n) ≡ n (mod 9).

─────────────────────────────────────────────────────────────────
DEFINITION:
  DS: Z⁺ → Z⁺,   DS(n) = sum of decimal digits of n

THEOREM 1 [PROVEN]:
  DS(n) ≡ n (mod 9)  for all n ≥ 0.

PROOF:
  10 ≡ 1 (mod 9)  →  10^k ≡ 1 (mod 9) for all k ≥ 0.
  For n = Σ dₖ 10^k:  n ≡ Σ dₖ · 1 = DS(n) (mod 9).         □

THEOREM 2 [PROVEN]:
  1 ≤ DS(n) ≤ 9(⌊log₁₀ n⌋ + 1)  for all n ≥ 1.
  The upper bound is achieved at n = 10^m − 1 (all-9s numbers).

COROLLARY [PROVEN]:
  DS(9k) ≡ 0 (mod 9)  and  DS(9k) ∈ {9, 18, 27, ...}
  In particular DS(18k) ∈ {9, 18, 27, 36} for k = 1..1369.

TIER APPLICATION [PROVEN]:
  DS(18k−4) ≡ 18k−4 ≡ −4 ≡ 5 (mod 9)
  Combined with DS(18k) ≡ 0 (mod 9):
  T(k) = DS(18k) + DS(18k−4) ≡ 5 (mod 9)  for all k ≥ 1.
─────────────────────────────────────────────────────────────────
"""

import math


def ds(n):
    return sum(int(d) for d in str(n))


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


# ──────────────────────────────────────────────────────────────────────────────
# THEOREM 1: DS(n) ≡ n (mod 9)
# ──────────────────────────────────────────────────────────────────────────────

# 10 ≡ 1 (mod 9)
assert 10 % 9 == 1
for k in range(0, 20):
    assert (10**k) % 9 == 1

# DS(n) ≡ n (mod 9) for all n in wide range
for n in range(0, 2000):
    assert ds(n) % 9 == n % 9 if n % 9 != 0 else ds(n) % 9 == 0


# ──────────────────────────────────────────────────────────────────────────────
# THEOREM 2: UPPER BOUND
# ──────────────────────────────────────────────────────────────────────────────

for n in [1, 9, 10, 99, 100, 999, 9999, 19998, 99999]:
    digits = math.floor(math.log10(n))
    bound = 9 * (digits + 1)
    assert ds(n) <= bound, f"DS({n})={ds(n)} > bound {bound}"

# Bound is tight at all-9s numbers
for m in range(1, 7):
    n_max = 10**m - 1   # 9, 99, 999, ...
    digits = math.floor(math.log10(n_max))
    bound = 9 * (digits + 1)
    assert ds(n_max) == bound    # DS(99...9) = 9m = bound


# ──────────────────────────────────────────────────────────────────────────────
# COROLLARY: DS(9k) is a multiple of 9
# ──────────────────────────────────────────────────────────────────────────────

for k in range(1, 300):
    assert ds(9 * k) % 9 == 0, f"DS(9×{k}) not divisible by 9"

# DS(18k) ∈ {9, 18, 27, 36} for k=1..1369
ds_18k_vals = {ds(18*k) for k in range(1, 1370)}
assert ds_18k_vals == {9, 18, 27, 36}

# DS(18k-4) ≡ 5 (mod 9)
for k in range(1, 1370):
    assert ds(18*k - 4) % 9 == 5, f"DS(18×{k}−4) not ≡ 5 (mod 9)"
ds_nm4_vals = {ds(18*k - 4) for k in range(1, 1370)}
assert ds_nm4_vals == {5, 14, 23, 32}


# ──────────────────────────────────────────────────────────────────────────────
# TIER APPLICATION
# ──────────────────────────────────────────────────────────────────────────────

def T(k):
    return ds(18 * k) + ds(18 * k - 4)

# T(k) ≡ 5 (mod 9) — derived from DS congruences, not observed
for k in range(1, 1370):
    assert T(k) % 9 == 5, f"T({k}) not ≡ 5 (mod 9)"

# The AP constraint: since T(k) ≡ 5 (mod 9), tier values ∈ {14, 23, 32, 41, 50, 59, 68, ...}
TIER_VALS = {14, 23, 32, 41, 50, 59, 68}
from collections import Counter
observed = set(Counter(T(k) for k in range(1, 1370)).keys())
assert observed == TIER_VALS    # exactly these 7 values appear


# ──────────────────────────────────────────────────────────────────────────────
# NON-CONTINUITY (p-adic, for p | 10)
# ──────────────────────────────────────────────────────────────────────────────

# DS is not continuous in the 2-adic metric:
# |n|_2 can be small while DS(n) changes drastically
# Example: 999 and 1000 are close in 10-adic sense
assert ds(999) == 27 and ds(1000) == 1    # huge jump at decade boundary
assert ds(9999) == 36 and ds(10000) == 1   # same pattern

# DS IS congruence-compatible with mod 9 (3-adic structure only)
for n in range(1, 200):
    assert ds(n) % 3 == n % 3    # follows from 10 ≡ 1 (mod 3) and mod 9


# ──────────────────────────────────────────────────────────────────────────────
# OUTPUT
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Digit Sum Congruence DS(n) ≡ n (mod 9)")
    print("=" * 62)

    print("\n── THEOREM 1 ──")
    print("  10 ≡ 1 (mod 9)  →  DS(n) ≡ n (mod 9)  for all n ≥ 0.")
    print("  Verified for n = 0..1999.")

    print("\n── THEOREM 2: UPPER BOUND ──")
    print(f"  DS(n) ≤ 9(⌊log₁₀n⌋+1).  Tight at n = 10^m−1.")
    for m in range(1, 6):
        n_max = 10**m - 1
        print(f"    DS({n_max}) = {ds(n_max)} = 9×{m}  [tight]")

    print("\n── COROLLARY ──")
    print(f"  DS(18k) values for k=1..1369:   {sorted(ds_18k_vals)}")
    print(f"  DS(18k-4) values for k=1..1369: {sorted(ds_nm4_vals)}")
    print(f"  All DS(18k) ≡ 0 (mod 9),  all DS(18k-4) ≡ 5 (mod 9).")

    print("\n── TIER APPLICATION ──")
    print(f"  T(k) = DS(18k)+DS(18k-4) ≡ 0+5 ≡ 5 (mod 9).  Verified k=1..1369.")
    print(f"  Observed tier values: {sorted(observed)}")

    print("\n── NON-CONTINUITY (p | 10) ──")
    print(f"  DS(999)={ds(999)}, DS(1000)={ds(1000)}: large jump at decade boundary.")
    print(f"  DS is congruence-compatible with mod 3 and mod 9 only.")

    print()
    print("All assertions passed.")
