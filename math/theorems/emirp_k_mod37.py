"""
emirp_k_mod37.py

K-statistic distribution of emirps modulo 37.

DEFINITIONS:
  emirp: prime p with rev(p) prime, rev(p) ≠ p  (strict — excludes palindrome primes)
  K(p) = ((rev(p) - p) % 333) // 9 * pow(11, -1, 37) % 37

POPULATION (4-digit ≤ n < 10^5):
  9424 primes
  1610 strict emirps

HISTOGRAM:
  HIST[k] = count of emirps with K(p) = k, for k in 0..36
  Symmetric: HIST[k] = HIST[37 - k % 37]  (proven forced, not empirical)
  Zero bins:  K = 5,  K = 32

SYMMETRY REASON:
  N - R = 99(a - c)  for 3-digit N=100a+10b+c.
  For 4-digit: structured by decimal expansion. The reflection p ↔ rev(p)
  swaps sign of (rev(p) - p), forcing HIST[k] = HIST[(37-k) % 37].
"""

from sympy import isprime

# ──────────────────────────────────────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────────────────────────────────────

def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


def rev(n):
    return int(str(n)[::-1])


INV11 = pow(11, -1, 37)    # 11^{-1} mod 37 = 27
assert INV11 == 27


def K(p):
    return ((rev(p) - p) % 333) // 9 * INV11 % 37


# ──────────────────────────────────────────────────────────────────────────────
# ENUMERATE
# ──────────────────────────────────────────────────────────────────────────────

primes_4plus = [n for n in range(1000, 100000) if isprime(n)]
assert len(primes_4plus) == 9424

emirps = [p for p in primes_4plus if rev(p) != p and isprime(rev(p))]
assert len(emirps) == 1610

# ──────────────────────────────────────────────────────────────────────────────
# HISTOGRAM
# ──────────────────────────────────────────────────────────────────────────────

HIST = [0] * 37
for p in emirps:
    HIST[K(p)] += 1

EXPECTED = [
    66, 22, 4, 58, 55, 0, 38, 79, 13, 23, 102, 51, 3, 78, 70,
    17, 44, 94, 21, 21, 94, 44, 17, 70, 78, 3, 51, 102, 23, 13,
    79, 38, 0, 55, 58, 4, 22
]
assert HIST == EXPECTED

# ──────────────────────────────────────────────────────────────────────────────
# PROPERTIES
# ──────────────────────────────────────────────────────────────────────────────

# Zero bins
assert HIST[5]  == 0
assert HIST[32] == 0

# Symmetry: HIST[k] == HIST[37 - k] for k in 1..36; HIST[0] self-maps
for k in range(1, 37):
    assert HIST[k] == HIST[37 - k], f"symmetry broken at k={k}"

# Total
assert sum(HIST) == 1610

# DR of K values for emirps stays in prime DR set {1,2,4,5,7,8} mostly
# (K=0 means no shift; K=5 and K=32 are empty by the zero-bin rule)


# ──────────────────────────────────────────────────────────────────────────────
# OUTPUT
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Emirp K mod 37 distribution")
    print("=" * 62)
    print(f"  Primes in [1000, 100000):  {len(primes_4plus)}")
    print(f"  Strict emirps:             {len(emirps)}")
    print(f"  11^{{-1}} mod 37 = {INV11}")
    print()
    print("  K   count")
    for k, cnt in enumerate(HIST):
        zero_flag = "  ← zero bin" if cnt == 0 else ""
        print(f"  {k:2d}  {cnt:4d}{zero_flag}")
    print()
    print(f"  Symmetry HIST[k] = HIST[37-k]: verified")
    print(f"  Zero bins at K=5 and K=32:     verified")
    print(f"  Total: {sum(HIST)}")
    print()
    print("All assertions passed.")
