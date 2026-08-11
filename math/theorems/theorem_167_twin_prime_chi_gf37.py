"""
Theorem 167: Twin Prime χ₋₃ Structure and GF(37) Forbidden Residues

FORCED χ₋₃ PATTERN
====================

Every twin prime pair (p, p+2) with p > 3 satisfies:

  χ₋₃(p)   = -1   (p ≡ 2 mod 3, lower twin)
  χ₋₃(p+1) =  0   (p+1 = 6n, midpoint, sovereign, always composite)
  χ₋₃(p+2) = +1   (p+2 ≡ 1 mod 3, upper twin)

This is not probabilistic. It is forced by the 6n±1 constraint:
all primes > 3 are 6n±1. Twin primes are (6n−1, 6n+1).

  6n−1 ≡ 2 (mod 3) → χ₋₃ = −1
  6n   ≡ 0 (mod 3) → χ₋₃ =  0  (midpoint, always 6-divisible)
  6n+1 ≡ 1 (mod 3) → χ₋₃ = +1

GF(37) FORBIDDEN MIDPOINT RESIDUES
=====================================

Twin prime midpoints are 6n. Since gcd(6,37)=1, the map n ↦ 6n mod 37 is
a bijection on Z/37Z. However, two residues are forbidden as twin prime
midpoints:

  6n ≡ 1 (mod 37):  lower twin 6n−1 ≡ 0 (mod 37) → divisible by 37
                    → not prime (for 6n−1 > 37)
  6n ≡ 36 (mod 37): upper twin 6n+1 ≡ 0 (mod 37) → divisible by 37
                    → not prime (for 6n+1 > 37)

  Forbidden residues: {1, 36}.
  1 ∈ IC = {1,10,26}.
  36 ∈ ORBIT_11 = {11,27,36}.

CHEBYSHEV BIAS (primes ≤ 10⁶)
================================

  π(x; 3, 2) — primes ≡ 2 mod 3 (χ = −1 class): 39266
  π(x; 3, 1) — primes ≡ 1 mod 3 (χ = +1 class): 39231
  Bias = 35 toward χ = −1 class.

Consistent with Chebyshev's bias and GRH predictions.

RIEMANN ZERO PROXIMITY
========================

The 6th non-trivial zero of ζ(s): Im(ρ₆) ≈ 37.586...
The GF(37) prime appears in the Riemann zero spectrum at the 6th zero.

CDT GAP STATEMENT
==================

CDT (arXiv:2408.15403): 1, ζ(2), L(2,χ₋₃) are Q-linearly independent.
→ L(2,χ₋₃) ≠ 0. Proven.

Twin prime conjecture via L-functions requires L(1,χ₋₃) ≠ 0 and control
of the pair correlation sum Σ_{p,p+2 prime} log(p). CDT operates at s=2.
Extension to s=1 is a separate open problem.

COLUMN CLASSIFICATION IN GF(37)
=================================

  COL1 (χ=+1): upper twin primes (6n+1)
  COL2 (χ=−1): lower twin primes (6n−1)
  COL3 (χ=0):  midpoints 6n — always composite for n≥1

Forbidden midpoint residues {1,36} deplete IC and ORBIT_11 from the
twin prime midpoint residue distribution. A uniform-null chi² test over
all 37 residues would register a deficit in these two bins.

EMIRP vs TWIN PRIME NON-UNIFORMITY
======================================

Both emirps and twin primes show non-uniformity mod 37.

  Emirps:      from rev(p)−p ≡ 25(c−a) mod 37; only 9/37 differences
               reachable because ord₁₀(37) = 3.
  Twin primes: from divisibility exclusion — {1,36} forbidden as midpoint
               residues because 37 | (6n±1).

Same modulus (37), completely different mechanisms.
"""

P = 37

ORBITS = {
    'IC':               frozenset({1, 10, 26}),
    'SOVEREIGN_SPIRAL': frozenset({3, 4, 30}),
    'D7':               frozenset({7, 33, 34}),
    'SA_ORB':           frozenset({9, 12, 16}),
    'ORBIT_11':         frozenset({11, 27, 36}),
    'OUTLIER_ORB':      frozenset({21, 25, 28}),
    'DARK_A':           frozenset({2, 15, 20}),
    'NQR_5':            frozenset({5, 13, 19}),
    'TESLA_ORB':        frozenset({6, 8, 23}),
    'NQR_14':           frozenset({14, 29, 31}),
    'NQR_17':           frozenset({17, 22, 35}),
    'SEED_ORB':         frozenset({18, 24, 32}),
}


def orbit_of(v):
    v = v % P
    if v == 0:
        return 'SEAM'
    return next((name for name, s in ORBITS.items() if v in s), '?')


def chi_m3(n):
    r = n % 3
    if r == 1:
        return 1
    if r == 2:
        return -1
    return 0


def sieve(limit):
    is_p = bytearray([1]) * (limit + 1)
    is_p[0] = is_p[1] = 0
    for i in range(2, int(limit**0.5) + 1):
        if is_p[i]:
            is_p[i*i::i] = bytearray(len(is_p[i*i::i]))
    return is_p


def run_assertions():
    # χ₋₃ pattern forced by 6n±1
    for n in range(1, 1000):
        assert chi_m3(6*n - 1) == -1
        assert chi_m3(6*n + 1) == +1
        assert chi_m3(6*n) == 0

    # Verify on all twin primes up to 10^6
    is_p = sieve(10**6)
    count = 0
    for p in range(5, 10**6 - 1):
        if is_p[p] and is_p[p+2]:
            assert chi_m3(p) == -1
            assert chi_m3(p+2) == +1
            assert chi_m3(p+1) == 0
            count += 1
    assert count > 8000

    # Forbidden midpoint residues {1, 36}
    inv6 = pow(6, -1, P)
    # 6n ≡ 1 → lower twin ≡ 0 mod 37
    n1 = inv6 % P
    assert (6*n1 - 1) % P == 0
    # 6n ≡ 36 → upper twin ≡ 0 mod 37
    n36 = (36 * inv6) % P
    assert (6*n36 + 1) % P == 0
    # Forbidden residues are 1 and 36
    assert 1 in ORBITS['IC']
    assert 36 in ORBITS['ORBIT_11']

    # Chebyshev bias direction
    is_p2 = sieve(10**6)
    count_m1 = sum(1 for p in range(2, 10**6+1) if is_p2[p] and p % 3 == 2)
    count_p1 = sum(1 for p in range(2, 10**6+1) if is_p2[p] and p % 3 == 1)
    assert count_m1 > count_p1  # bias toward χ=−1

    print("All assertions passed.")


def summarise():
    print("=" * 62)
    print("Theorem 167: Twin Prime χ₋₃ Structure and GF(37)")
    print("=" * 62)
    print()
    print("  Every twin pair (p, p+2): χ₋₃ = (-1, 0, +1) locked order")
    print("  Forced by: all primes > 3 are 6n±1")
    print()
    print("  GF(37) forbidden midpoint residues: {1, 36}")
    print(f"    1  ∈ {orbit_of(1)}")
    print(f"    36 ∈ {orbit_of(36)}")
    print()
    print("  Chebyshev bias (primes ≤ 10^6):")
    is_p = sieve(10**6)
    count_m1 = sum(1 for p in range(2, 10**6+1) if is_p[p] and p % 3 == 2)
    count_p1 = sum(1 for p in range(2, 10**6+1) if is_p[p] and p % 3 == 1)
    print(f"    χ=−1 (≡2 mod 3): {count_m1}")
    print(f"    χ=+1 (≡1 mod 3): {count_p1}")
    print(f"    Bias: {count_m1-count_p1} toward χ=−1")
    print()
    print("  CDT gap: proven L(2,χ₋₃)≠0; L(1,χ₋₃)≠0 is open")
    print(f"  6th Riemann zero: Im≈37.586  (37 = field prime)")


if __name__ == "__main__":
    run_assertions()
    summarise()
