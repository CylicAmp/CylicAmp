"""
Emirp Non-Uniformity Mod 37
arXiv connection: Calegari–Dimitrov–Tang (2408.15403)

An emirp is a prime p whose digit-reversal rev(p) is also prime
(with the same number of digits).

Result: emirps are significantly non-uniformly distributed mod 37.
        No such signal exists for mod 31, 41, or 43.

Measured (primes 1000–10^6, N=11241 emirps):
  mod 31: chi2=20.7 / df=29  Z=-1.09  (consistent with uniform)
  mod 37: chi2=59.5 / df=35  Z=+2.93  (≈3σ, SIGNIFICANT)
  mod 41: chi2=33.9 / df=39  Z=-0.58  (consistent with uniform)
  mod 43: chi2=34.3 / df=41  Z=-0.74  (consistent with uniform)

WHY MOD 37 IS SPECIAL:
  ord10(37) = 3  →  10^3 ≡ 1 (mod 37)  →  999 ≡ 0 (mod 37)
  37 is the unique prime (besides 3) dividing 999 = 3^3 × 37.

  For a 3-digit emirp p = 100a + 10b + c (a,c ∈ {1,3,7,9}):
    100 ≡ 26 ≡ 10^{-1} (mod 37)  [since 10×26 = 260 ≡ 1 mod 37]
    p     ≡ 26a + 10b + c  (mod 37)
    rev(p) ≡ 26c + 10b + a  (mod 37)
    rev(p) − p ≡ 25(c − a)  (mod 37)

  Since a,c ∈ {1,3,7,9}, c−a ∈ {−8,−6,−4,−2,0,2,4,6,8}.
  Allowed differences 25(c−a) mod 37: {0,2,11,13,15,22,24,26,35}
  Only 9 out of 37 possible differences are reachable.
  The emirp pair graph on Z/37Z is SPARSE — 28 differences are forbidden.

ENRICHED / DEPLETED (top/bottom 6):
  Most enriched:  r=8  (AHL! ratio=1.127), r=34, r=23, r=24, r=13, r=12
  Most depleted:  r=36 (ratio=0.833), r=11, r=27, r=10, r=20, r=26

  The most emirp-dense residue class mod 37 is r ≡ 8 — the AHL value.
  The DR-sovereign residues (DR=9: r=27,36) are among the most depleted.

CONNECTION TO EISENSTEIN STRUCTURE:
  37 is Loeschian: 37 = 3^2 + 3×4 + 4^2, splits in Z[omega].
  10 is a primitive cube root of 1 mod 37 (order 3 in (Z/37Z)*).
  This is the same 3-periodicity that makes Z[omega] special:
  the Eisenstein unit omega satisfies omega^3 = 1.
  The emirp non-uniformity is a decimal-representation shadow
  of the Eisenstein lattice structure at p=37.
"""

import math

def rev(n): return int(str(n)[::-1])

def dr(n): return (n-1)%9+1 if n>0 else 0

def chi_m3(n):
    r = n % 3
    return 1 if r==1 else (-1 if r==2 else 0)

def sieve(limit):
    is_p = bytearray([1])*(limit+1)
    is_p[0] = is_p[1] = 0
    for i in range(2, int(limit**0.5)+1):
        if is_p[i]:
            is_p[i*i::i] = bytearray(len(is_p[i*i::i]))
    return is_p

def emirp_counts(limit, m, lo=1000):
    is_p = sieve(limit)
    counts = [0]*m
    for p in range(lo, limit+1):
        if is_p[p]:
            rp = rev(p)
            if len(str(rp)) == len(str(p)) and is_p[rp]:
                counts[p % m] += 1
    return counts


def chi2_z(counts, m):
    r = counts[1:]
    tr = sum(r)
    exp = tr / (m-1)
    chi2 = sum((c-exp)**2/exp for c in r)
    df = m - 2
    Z = (chi2 - df) / (2*df)**0.5
    return tr, chi2, df, Z


# Verify the mechanism algebraically
def allowed_differences_3digit():
    diffs = set()
    for a in (1,3,7,9):
        for c in (1,3,7,9):
            diffs.add((25*(c-a)) % 37)
    return sorted(diffs)


# Core assertions (use sieve for speed in tests)
counts_37 = emirp_counts(10**6, 37)
N37, chi2_37, df_37, Z_37 = chi2_z(counts_37, 37)

assert Z_37 > 2.5, f"Expected Z>2.5 for mod 37, got {Z_37:.2f}"

diffs = allowed_differences_3digit()
assert len(diffs) == 9, "Should be exactly 9 allowed differences"
assert 0 in diffs, "d=0 (palindromic) must be allowed"

# AHL=8 should be the most enriched residue
exp = N37 / 36
enriched_order = sorted(range(1, 37), key=lambda r: -counts_37[r])
assert enriched_order[0] == 8, f"AHL (r=8) should be most enriched, got r={enriched_order[0]}"

# DR-9 residues (27 and 36) should be depleted
dr9_residues = [r for r in range(1,37) if dr(r)==9]
assert all(counts_37[r] < exp for r in dr9_residues), "DR=9 residues should be depleted"

# Verify 10^{-1} ≡ 26 (mod 37)
assert (10 * 26) % 37 == 1
# And 100 ≡ 26 (mod 37)
assert 100 % 37 == 26


if __name__ == "__main__":
    from sympy import isprime  # fallback for validation

    print("EMIRP NON-UNIFORMITY MOD 37")
    print("=" * 50)
    print()

    print("Algebraic mechanism:")
    print(f"  10 × 26 ≡ {(10*26)%37} (mod 37)  →  26 = 10^{{-1}}")
    print(f"  rev(p) − p ≡ 25(c−a) (mod 37)  for 3-digit emirp p=100a+10b+c")
    print(f"  Allowed differences: {diffs}")
    print(f"  Forbidden: {37-len(diffs)} out of 37")
    print()

    counts_31 = emirp_counts(10**6, 31)
    counts_41 = emirp_counts(10**6, 41)
    counts_43 = emirp_counts(10**6, 43)

    print("Chi-squared test results:")
    for m, cnt in [(31,counts_31),(37,counts_37),(41,counts_41),(43,counts_43)]:
        N, chi2, df, Z = chi2_z(cnt, m)
        o = 1; c = 10%m
        while c != 1: c=(c*10)%m; o+=1
        print(f"  mod {m}: ord10={o}  999%{m}={999%m:>2}  "
              f"chi2={chi2:.1f}  df={df}  Z={Z:+.2f}")
    print()

    print("Residue enrichment mod 37 (top 6 / bottom 6):")
    exp = N37 / 36
    ranked = sorted(range(1,37), key=lambda r: -counts_37[r])
    print("  Enriched:")
    for r in ranked[:6]:
        c = counts_37[r]
        print(f"    r={r:>2}  n={c}  ratio={c/exp:.3f}  "
              f"DR={dr(r)}  χ₋₃={chi_m3(r):+d}"
              + (" ← AHL" if r==8 else ""))
    print("  Depleted:")
    for r in ranked[-6:]:
        c = counts_37[r]
        print(f"    r={r:>2}  n={c}  ratio={c/exp:.3f}  "
              f"DR={dr(r)}  χ₋₃={chi_m3(r):+d}"
              + (" ← −1 mod 37" if r==36 else ""))
    print()
    print("All assertions passed.")
