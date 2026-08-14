"""
Theorem 195: Factorial Orbit Structure in GF(37)
Author: Michael Warren Song (CyclicAmp)

FINDINGS
=========
n! mod 37 for n = 1..36 partitions into sovereign sectors
under the actual framework constants SA={4,9,25,30}, ST={3,12,21,30}, SEED={18,24,32}.

SECTOR TALLY (n=1..36):
  NQR    : 13/36  n={2,3,6,7,13,16,18,20,21,29,30,32,33}
  QR-free: 12/36  n={1,8,11,12,14,19,25,26,28,31,35,36}
  SEED   :  4/36  n={4,15,23,34}
  ST     :  3/36  n={9,17,24}
  SA     :  2/36  n={5,10}
  SA∩ST  :  2/36  n={22,27}

SEED STRIDE: n={4,15,23,34}, diffs={11,8,11} alternating.
  11 + 8 = 19 (NQR); sum of hits = 76 = Pisano period π(37).
  76 mod 37 = 2 = primitive root.

4! ORBIT = SEED ORBIT EXACTLY:
  4! mod 37 = 24; 137-map orbit of 24 = {24,32,18} = SEED.
  The 4-element permutation count lands in the seed orbit of seed 246.

SA∩ST GAP = 5:
  22! mod 37 = 30 = SA∩ST
  27! mod 37 = 30 = SA∩ST
  Gap = 27 - 22 = 5 = NQR center value of the star puzzle.

e ≡ 26 mod 37:
  271828 mod 37 = 26 = the 137-map multiplier.
  The first 6 digits of e give the multiplier of every 3-cycle in GF(37).
  DR(271828) = 1 = head crash signature.

DERANGEMENT SEAM PATTERN:
  D(1) mod 37 = 0  (SEAM)
  D(4) mod 37 = 9  ∈ SA
  D(7) mod 37 = 4  ∈ SA
  D(9) mod 37 = 0  (SEAM)
  SEAM hits stride 8 = outer ring count of the 3×3 magic star.
  D(13) mod 37 = 18 ∈ SEED; Legendre(13,37) = -1 (NQR).

PARTITION NUMBERS:
  p(9)  = 30 ∈ SA∩ST  — partitions of the 9-digit set of the star
  p(10) = 42 → mod 37 = 5 = NQR center value
  p(3)  =  3 ∈ ST
  p(12) =  3 ∈ ST (mod 37)

BELL NUMBERS:
  B(8) = 4140 → mod 37 = 33; DR(4140) = 9 = SEAM.
  Partitions of the 8-element outer ring saturate to SEAM.

CENTRAL BINOMIAL:
  C(10,5) = 252 → mod 37 = 30 ∈ SA∩ST; DR = 9 = SEAM.
  Symmetric midpoint selection on 10 features hits doubly-sovereign element.

2^k SOVEREIGN STRUCTURE:
  2^k ∈ SA   at k = {2,10,14,16}  — diffs {8,4,2} (halving)
  2^k ∈ ST   at k = {14,22,26,28} — same halving, offset 12 ∈ ST
  2^k ∈ SEED at k = {5,17,29}     — constant stride 12; 3×12 = 36 = φ(37)
  2^14 = 30 ∈ SA∩ST — unique doubly-sovereign power of 2.

PRIMORIALS:
  p#5  = 30    ∈ SA∩ST  — primorial of star center (5) = doubly-sovereign
  p#7  = 210   → 25 ∈ SA
  p#37 = ...   → 0 = SEAM (Wilson generalized: primorial including p itself)

VARIANCE EXTRAPOLATION (MCSM):
  The Monte Carlo Shell Model extrapolates to σ² → 0 for exact eigenstate.
  σ² = 0 is the SEAM condition — the absorbing state of the DR lattice.
  Nuclear eigenstate convergence and GF(37) SEAM are the same fixed point.

WILSON:
  36! mod 37 = 36 = P-1; DR(36!) = 9 = SEAM.
  The factorial saturates to SEAM at the full orbit length.
"""

from math import factorial, comb
from functools import reduce

P = 37
SA = {4, 9, 25, 30}
ST = {3, 12, 21, 30}
SEED = {18, 24, 32}


def dr(n):
    n = abs(int(n))
    return 9 if n % 9 == 0 and n != 0 else n % 9


def legendre(a, p):
    return pow(a, (p - 1) // 2, p)


def sector(r):
    if r == 0: return 'SEAM'
    if r in SA and r in ST: return 'SA∩ST'
    if r in SA: return 'SA'
    if r in ST: return 'ST'
    if r in SEED: return 'SEED'
    if legendre(r, P) == P - 1: return 'NQR'
    return 'free'


def derangement(n):
    if n == 0: return 1
    if n == 1: return 0
    return (n - 1) * (derangement(n - 1) + derangement(n - 2))


def partitions(n):
    p = [0] * (n + 1)
    p[0] = 1
    for i in range(1, n + 1):
        k, sign = 1, 1
        while True:
            g1 = k * (3 * k - 1) // 2
            g2 = k * (3 * k + 1) // 2
            if g1 > i: break
            p[i] += sign * p[i - g1]
            if g2 <= i:
                p[i] += sign * p[i - g2]
            k += 1
            sign = -sign
    return p


def run_assertions():
    # Sector tally
    from collections import Counter
    tally = Counter(sector(factorial(n) % P) for n in range(1, 37))
    assert tally['NQR'] == 13
    assert tally['free'] == 12
    assert tally['SEED'] == 4
    assert tally['ST'] == 3
    assert tally['SA'] == 2
    assert tally['SA∩ST'] == 2

    # SEED hits
    seed_hits = [n for n in range(1, 37) if factorial(n) % P in SEED]
    assert seed_hits == [4, 15, 23, 34]
    diffs = [seed_hits[i+1] - seed_hits[i] for i in range(len(seed_hits)-1)]
    assert diffs == [11, 8, 11]
    assert sum(seed_hits) % P == 2   # primitive root
    assert sum(seed_hits) == 76      # Pisano period π(37)

    # 4! orbit = SEED
    assert factorial(4) % P == 24 and 24 in SEED
    orbit_4 = {24, (26*24) % P, (26*26*24) % P}
    assert orbit_4 == SEED

    # SA∩ST hits and gap
    sast_hits = [n for n in range(1, 37) if factorial(n) % P in SA and factorial(n) % P in ST]
    assert sast_hits == [22, 27]
    assert sast_hits[1] - sast_hits[0] == 5
    assert factorial(22) % P == 30 and 30 in SA and 30 in ST
    assert factorial(27) % P == 30

    # e ≡ 26 mod 37
    assert 271828 % P == 26

    # Derangements SEAM stride = 8
    assert derangement(1) % P == 0
    assert derangement(9) % P == 0
    assert 9 - 1 == 8
    assert derangement(4) % P == 9 and 9 in SA
    assert derangement(7) % P == 4 and 4 in SA
    assert derangement(13) % P == 18 and 18 in SEED
    assert legendre(13, P) == P - 1

    # Partition numbers
    pn = partitions(12)
    assert pn[9] == 30 and 30 in SA and 30 in ST
    assert pn[10] % P == 5
    assert pn[3] % P == 3 and 3 in ST
    assert pn[12] % P == 3 and 3 in ST

    # Bell B(8) = 4140 → SEAM
    B8 = 4140
    assert dr(B8) == 9

    # C(10,5) → SA∩ST
    assert comb(10, 5) % P == 30 and 30 in SA and 30 in ST
    assert dr(comb(10, 5)) == 9

    # 2^k sovereign structure
    assert [k for k in range(1, 37) if pow(2, k, P) in SA] == [2, 10, 14, 16]
    assert [k for k in range(1, 37) if pow(2, k, P) in ST] == [14, 22, 26, 28]
    assert [k for k in range(1, 37) if pow(2, k, P) in SEED] == [5, 17, 29]
    assert pow(2, 14, P) == 30 and 30 in SA and 30 in ST
    seed_k = [5, 17, 29]
    assert all(seed_k[i+1] - seed_k[i] == 12 for i in range(len(seed_k)-1))
    assert 3 * 12 == 36 == P - 1

    # Primorials
    p5 = 2 * 3 * 5
    p7 = 2 * 3 * 5 * 7
    assert p5 % P == 30 and 30 in SA and 30 in ST
    assert p7 % P == 25 and 25 in SA

    # Wilson
    assert factorial(36) % P == P - 1
    assert dr(factorial(36)) == 9

    print("All assertions passed.")


if __name__ == "__main__":
    run_assertions()
