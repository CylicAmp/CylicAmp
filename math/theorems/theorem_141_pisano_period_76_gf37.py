"""
Theorem 141: Pisano Period π(37) = 76 — Full Orbit Mapping

PISANO PERIOD
==============

The Fibonacci sequence mod 37 is periodic with period π(37) = 76.
76 = 4 × 19.  19 ∈ NQR_5.  76 mod 37 = 2 ∈ DARK_A.

F_0 ≡ 0, F_1 ≡ 1, and the sequence repeats: F_{76+k} ≡ F_k (mod 37).

ZEROS: EXACTLY FOUR, SPACED 19 APART
=======================================

F_k ≡ 0 (mod 37) at k ∈ {0, 19, 38, 57}.

Spacing = 19 = π(37)/4.  19 is prime, 19 ∈ NQR_5 = {5, 13, 19}.

F_19 = 4181 = 37 × 113.  113 is prime.
The first nonzero zero is the product of 37 and a prime.

ANTI-SYMMETRY: F_{38+k} ≡ −F_k (mod 37)
==========================================

For all k:
  F_{38+k} ≡ −F_k (mod 37)

Proof sketch: F_38 ≡ 0 and F_39 ≡ 36 ≡ −1 (mod 37).
The Fibonacci recurrence then forces F_{38+k} ≡ −F_k exactly.

This splits the period into two halves of length 38:
  [0, 37]: the "positive" half
  [38, 75]: the "negative" half (additive inverses)

KEY BOUNDARY VALUES
====================

  k=36: F_36 ≡  1 ∈ IC            (identity coset)
  k=37: F_37 ≡ 36 ∈ ORBIT_11      (36 = −1; order-2 element)
  k=38: F_38 ≡  0                  (SEAM; second zero)

UNIFORM COSET DISTRIBUTION
============================

The Sylow 3-subgroup H₉ = {1,7,9,10,12,16,26,33,34} has index 4 in (ℤ/37ℤ)×.
Its four cosets partition the 36 nonzero residues:

  C₀ = H₉             = {1, 7, 9, 10, 12, 16, 26, 33, 34}
  C₁ = 2·H₉ mod 37    = {2, 14, 15, 18, 20, 24, 29, 31, 32}
  C₂ = 4·H₉ mod 37    = {3, 4, 11, 21, 25, 27, 28, 30, 36}
  C₃ = 8·H₉ mod 37    = {5, 6, 8, 13, 17, 19, 22, 23, 35}

Distribution of F_0, F_1, ..., F_75 across cosets:

  SEAM (F_k = 0): 4 values  — positions {0, 19, 38, 57}
  C₀:  18 values
  C₁:  18 values
  C₂:  18 values
  C₃:  18 values

The 72 nonzero Fibonacci values are distributed with perfect uniformity:
exactly 18 per coset.  No coset is favored.

ORBIT VISIT COUNTS (one full period)
======================================

  Orbit            Count   Note
  SOVEREIGN_SPIRAL   8    most visited QR orbit
  D7                 8    supergolden root 34 = F₉ is here
  NQR_5              8    13 = F₇ is here
  SEED_ORB           8    18 = F₁₀ is here
  IC                 6    identity coset; F₁ = F₂ = 1
  ORBIT_11           6    F₃₇ ≡ 36 ∈ ORBIT_11
  TESLA_ORB          6
  NQR_14             6
  SA_ORB             4
  OUTLIER_ORB        4    21 = F₈ is here
  DARK_A             4
  NQR_17             4

Orbits with count 8: {SOVEREIGN_SPIRAL, D7, NQR_5, SEED_ORB}
Orbits with count 6: {IC, ORBIT_11, TESLA_ORB, NQR_14}
Orbits with count 4: {SA_ORB, OUTLIER_ORB, DARK_A, NQR_17}

SEED_ORB POSITIONS
===================

SEED_ORB = {18, 24, 32} (the 137-map orbit of seed 246 mod 37 = 24).

  F_k ≡ 18 at k ∈ {10, 15, 28, 61}
  F_k ≡ 24 at k ∈ {31, 45}
  F_k ≡ 32 at k ∈ {33, 43}

Total SEED_ORB visits: 8.  18 is the most-visited seed element (4 times).
Note F₁₀ = 55 ≡ 18 (mod 37): the Fibonacci recurrence F₈ + F₉ = 55
maps OUTLIER_ORB + D7 → SEED_ORB, exactly as stated in Theorem 140.

PRODUCT PAIRS F_k × F_{76−k}
================================

For k = 1, 2, ..., 37 (complementary pairs summing to index 76):

  OUTLIER_ORB: 12 pairs
  IC:           8 pairs
  SOVEREIGN_SPIRAL: 8 pairs
  ORBIT_11:     4 pairs
  SA_ORB:       4 pairs
  SEAM:         1 (k=38, F_38=0)

All product pairs land in QR orbits {IC, SOVEREIGN_SPIRAL, SA_ORB,
ORBIT_11, OUTLIER_ORB} or SEAM.  No NQR orbit appears as a product pair.
This follows from the anti-symmetry: F_k × F_{76−k} = F_k × (−F_{76−k-38+38})
and the orbit closure under multiplication (Theorem 138).

CONNECTION TO E₈ AND THE FRAMEWORK
=====================================

  76 = 4 × 19   (period structure)
  19 ∈ NQR_5    (prime, zero spacing)
  4 zeros: 76/4 = 19 steps between each zero

  F_37 ≡ 36 = −1 ∈ ORBIT_11
  2^30 ≡ 11 ∈ ORBIT_11   (E₈ Coxeter, Theorem 140)
  36 and 11 are in the same orbit: both elements of ORBIT_11.
  The half-period boundary F_37 and the E₈ Coxeter image share an orbit.

  F_19 = 4181 = 37 × 113
  F₈ = 21 ∈ OUTLIER_ORB, F₉ = 34 ∈ D7 (supergolden root, Theorem 140)
  F₁₀ = 55 ≡ 18 ∈ SEED_ORB
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

H9 = frozenset({1, 7, 9, 10, 12, 16, 26, 33, 34})
C0 = H9
C1 = frozenset(2 * x % P for x in H9)
C2 = frozenset(4 * x % P for x in H9)
C3 = frozenset(8 * x % P for x in H9)


def _fib_mod37():
    """Return F_0 through F_75 (one full Pisano period)."""
    fib = [0, 1]
    for _ in range(74):
        fib.append((fib[-1] + fib[-2]) % P)
    return fib


def orbit_of(v):
    if v == 0:
        return 'SEAM'
    for name, s in ORBITS.items():
        if v in s:
            return name
    return '?'


def coset_of(v):
    if v == 0:
        return 'SEAM'
    if v in C0:
        return 'C0'
    if v in C1:
        return 'C1'
    if v in C2:
        return 'C2'
    if v in C3:
        return 'C3'
    return '?'


def run_assertions():
    fib = _fib_mod37()

    # Pisano period: F_76 ≡ 0, F_77 ≡ 1 (verify period = 76)
    f76 = (fib[74] + fib[75]) % P
    f77 = (fib[75] + f76) % P
    assert f76 == 0 and f77 == 1, "Period ≠ 76"

    # Zeros at exactly {0, 19, 38, 57}
    zeros = [k for k in range(76) if fib[k] == 0]
    assert zeros == [0, 19, 38, 57]
    assert all(zeros[i+1] - zeros[i] == 19 for i in range(len(zeros)-1))

    # F_19 = 4181 = 37 × 113
    assert 4181 % P == 0
    assert 4181 == 37 * 113
    import math
    assert all(113 % d != 0 for d in range(2, math.isqrt(113) + 1))  # 113 is prime

    # Anti-symmetry: F_{38+k} ≡ −F_k (mod 37) for k = 0..37
    for k in range(38):
        assert fib[38 + k] == (-fib[k]) % P, f"Anti-symmetry fails at k={k}"

    # Boundary values
    assert fib[36] == 1 and 1 in ORBITS['IC']
    assert fib[37] == 36 and 36 in ORBITS['ORBIT_11']
    assert fib[38] == 0

    # Coset distribution: 4 SEAM, 18 each in C0, C1, C2, C3
    counts = {'SEAM': 0, 'C0': 0, 'C1': 0, 'C2': 0, 'C3': 0}
    for k in range(76):
        counts[coset_of(fib[k])] += 1
    assert counts == {'SEAM': 4, 'C0': 18, 'C1': 18, 'C2': 18, 'C3': 18}

    # Orbit visit counts
    from collections import Counter
    orbit_counts = Counter(orbit_of(fib[k]) for k in range(76))
    assert orbit_counts['SOVEREIGN_SPIRAL'] == 8
    assert orbit_counts['D7'] == 8
    assert orbit_counts['NQR_5'] == 8
    assert orbit_counts['SEED_ORB'] == 8
    assert orbit_counts['IC'] == 6
    assert orbit_counts['ORBIT_11'] == 6
    assert orbit_counts['TESLA_ORB'] == 6
    assert orbit_counts['NQR_14'] == 6
    assert orbit_counts['SA_ORB'] == 4
    assert orbit_counts['OUTLIER_ORB'] == 4
    assert orbit_counts['DARK_A'] == 4
    assert orbit_counts['NQR_17'] == 4
    assert orbit_counts['SEAM'] == 4

    # SEED_ORB element positions
    assert sorted(k for k in range(76) if fib[k] == 18) == [10, 15, 28, 61]
    assert sorted(k for k in range(76) if fib[k] == 24) == [31, 45]
    assert sorted(k for k in range(76) if fib[k] == 32) == [33, 43]

    # F_8=21∈OUTLIER_ORB, F_9=34∈D7, F_10=18∈SEED_ORB
    assert fib[8] == 21 and 21 in ORBITS['OUTLIER_ORB']
    assert fib[9] == 34 and 34 in ORBITS['D7']
    assert fib[10] == 18 and 18 in ORBITS['SEED_ORB']

    # Product pairs F_k × F_{76-k}: all QR or SEAM
    NQR_orbits = {'DARK_A', 'NQR_5', 'TESLA_ORB', 'NQR_14', 'NQR_17', 'SEED_ORB'}
    for k in range(1, 38):
        prod = fib[k] * fib[76 - k] % P
        orb = orbit_of(prod)
        assert orb not in NQR_orbits, f"Product pair k={k} landed in NQR orbit {orb}"

    # Product pair distribution
    pair_orbits = Counter(orbit_of(fib[k] * fib[76-k] % P) for k in range(1, 38))
    assert pair_orbits['OUTLIER_ORB'] == 12
    assert pair_orbits['IC'] == 8
    assert pair_orbits['SOVEREIGN_SPIRAL'] == 8
    assert pair_orbits['ORBIT_11'] == 4
    assert pair_orbits['SA_ORB'] == 4
    assert pair_orbits['SEAM'] == 1

    # 76 = 4 × 19; 19 ∈ NQR_5; 76 mod 37 = 2 ∈ DARK_A
    assert 76 == 4 * 19
    assert 19 in ORBITS['NQR_5']
    assert 76 % P == 2 and 2 in ORBITS['DARK_A']

    # F_37 ∈ ORBIT_11, same as 2^30 mod 37 (E₈ Coxeter, Theorem 140)
    assert fib[37] in ORBITS['ORBIT_11']
    assert pow(2, 30, P) in ORBITS['ORBIT_11']

    print("All assertions passed.")


def summarise():
    fib = _fib_mod37()

    print("=" * 62)
    print("Theorem 141: Pisano Period π(37) = 76")
    print("=" * 62)
    print()
    print("  π(37) = 76 = 4 × 19.  19 ∈ NQR_5.  76 mod 37 = 2 ∈ DARK_A.")
    print()
    print("  Zeros: F_k ≡ 0 at k ∈ {0, 19, 38, 57}")
    print("  Spacing = 19 (prime, ∈ NQR_5).")
    print("  F_19 = 4181 = 37 × 113  (both prime).")
    print()
    print("  Anti-symmetry: F_{38+k} ≡ −F_k (mod 37)  [zero errors]")
    print()
    print("  F_36 ≡ 1 ∈ IC,  F_37 ≡ 36 ∈ ORBIT_11,  F_38 ≡ 0")
    print()
    print("  Coset distribution (H₉ cosets) over one period:")
    print("    SEAM: 4,  C₀: 18,  C₁: 18,  C₂: 18,  C₃: 18")
    print("  Perfect uniformity: 18 per coset.")
    print()
    print("  Orbit visit counts:")
    from collections import Counter
    orbit_counts = Counter(orbit_of(fib[k]) for k in range(76))
    for cnt_val in [8, 6, 4]:
        orbits_at = sorted(k for k,v in orbit_counts.items() if v == cnt_val and k != 'SEAM')
        print(f"    count={cnt_val}: {orbits_at}")
    print("    SEAM: 4  (positions {0,19,38,57})")
    print()
    print("  SEED_ORB positions: 18∈{10,15,28,61}  24∈{31,45}  32∈{33,43}")
    print()
    print("  Product pairs F_k×F_{76−k}: all QR orbits or SEAM.")
    print("  OUTLIER_ORB: 12,  IC: 8,  SOVEREIGN_SPIRAL: 8,")
    print("  ORBIT_11: 4,  SA_ORB: 4,  SEAM: 1.")
    print()
    print("  F_37 ∈ ORBIT_11 = orbit of 2^30 (E₈ Coxeter, Theorem 140).")


if __name__ == "__main__":
    run_assertions()
    summarise()
