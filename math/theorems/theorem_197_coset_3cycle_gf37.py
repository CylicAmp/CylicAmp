"""
Theorem 197: Coset 3-Cycle Structure in GF(37) — The 137-Map Partition
Author: Michael Warren Song (CyclicAmp)

MASTER IDENTITY:
  1 + 26 + 10 = 37 = P
  Every element g of GF(37)* generates a 3-cycle {g, 26g, 10g} under the 137-map.
  These three elements sum to g(1+26+10) = 37g ≡ 0 (mod 37) = SEAM.
  ALL 12 three-cycles of the 137-map sum to SEAM.

COSET PARTITION — 12 three-cycles of <26> in GF(37)*:
  GF(37)* has order 36. <26> = {1,10,26} has order 3. Quotient has 12 cosets.

  SOVEREIGN CYCLES (contain SA or ST elements):
    {3, 4, 30}    sum=37  DR=1  sectors: ST→SA→SA∩ST→ST
    {9, 12, 16}   sum=37  DR=1  sectors: SA→ST→free→SA
    {21, 25, 28}  sum=74  DR=2  sectors: ST→free→SA→ST

  SEED CYCLE (pure):
    {18, 24, 32}  sum=74  DR=2  sectors: SEED→SEED→SEED (all 3 elements ∈ SEED)

  FREE/NQR CYCLES (no GF(37) elements):
    {1, 10, 26}   {7, 33, 34}   {11, 27, 36}  — free
    {2, 15, 20}   {5, 13, 19}   {6, 8, 23}    — NQR
    {14, 29, 31}  {17, 22, 35}                 — NQR

  DR SPLIT: 6 cycles sum to 37 (DR=1, head-crash); 6 sum to 74 (DR=2, primitive root).

KEY CYCLE {3, 4, 30}:
  The unique 3-cycle spanning all three sovereign classes: ST, SA, and SA∩ST.
  137-map action: 3→4→30→3  (ST → SA → SA∩ST → ST).
    26×3 mod37 = 4 (SA)
    26×4 mod37 = 30 (SA∩ST)
    26×30 mod37 = 3 (ST)
  Sum = 3+4+30 = 37 = P → SEAM.  DR(37) = 1 (head-crash signature).

SA∪ST PARTITION:
  SA∪ST = {3,4,9,12,21,25,30} (7 elements, SA∩ST={30} counted once).
  Partitions exactly into 3 sovereign cosets:
    {3,4,30}:   3∈ST, 4∈SA, 30∈SA∩ST
    {9,12,16}:  9∈SA, 12∈ST, 16∈free
    {21,25,28}: 21∈ST, 25∈SA, 28∈free
  Each coset sums to SEAM. The 6 unnamed fillers are {16,28}.

SEED COSET:
  {18,24,32} = SEED. Unique coset where all elements belong to a single sovereign sector.
  Sum = 74 = 2×37 ≡ 0 mod 37.  DR(74) = 2 (primitive root of GF(37)).
  Pre-images under ×3: SEED/3 = {6,8,23} — all NQR.
  The 137-map orbit of SEED is SEED itself (3-cycle under ×26).

ORD₃₇(3) = 18 = φ(37)/2:
  3 is a quadratic residue mod 37 (Legendre(3,37)=+1). Order 18, not 36.
  Powers of 3 with sovereign hits:
    3^1  = 3  ∈ ST
    3^2  = 9  ∈ SA
    3^5  = 21 ∈ ST
    3^6  = 26 = 137-map multiplier
    3^7  = 4  ∈ SA
    3^8  = 12 ∈ ST
    3^13 = 30 ∈ SA∩ST  (exponent 13 is NQR)
    3^17 = 25 ∈ SA
    3^9  = 36 = -1 (half-orbit: 3^18 = 1)
  Sovereign k-values: {1,2,5,7,8,13,17} — 7 out of 18.
  Mirror symmetry: 3^k × 3^(18-k) ≡ 1 — inverse pairs.
    3^1=3(ST) × 3^17=25(SA) = 1
    3^5=21(ST) × 3^13=30(SA∩ST) = 1

3×k MULTIPLES — SOVEREIGN STRUCTURE:
  3×{1,4,7,10} mod37 = {3,12,21,30} = ST  (k≡1 mod 3 for k≤10)
  3×{3,10,26,33} mod37 = {9,30,4,25} = SA  (SA generators)
  3×{6,8,23} mod37 = {18,24,32} = SEED
  k=10: 3×10=30 ∈ SA∩ST — the unique k in both SA and ST generator sets.
  SEED generator sum: 6+8+23=37=P → SEAM (SEED generators also sum to SEAM).
"""

from collections import Counter
from math import gcd

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


ALL_COSETS = [
    [1, 10, 26], [2, 15, 20], [3, 4, 30], [5, 13, 19],
    [6, 8, 23],  [7, 33, 34], [9, 12, 16], [11, 27, 36],
    [14, 29, 31],[17, 22, 35],[18, 24, 32],[21, 25, 28],
]


def run_assertions():
    # 1. Master identity
    assert 1 + 26 + 10 == P

    # 2. All 12 cosets sum ≡ 0 mod 37
    assert all(sum(c) % P == 0 for c in ALL_COSETS)

    # 3. SEED is the unique purely-homogeneous sovereign coset
    assert all(x in SEED for x in [18, 24, 32])
    assert not any(all(x in SEED for x in c) for c in ALL_COSETS if sorted(c) != [18, 24, 32])

    # 4. {3,4,30} spans all three sovereign classes
    assert 3 in ST and 4 in SA and 30 in SA and 30 in ST
    assert sum([3, 4, 30]) == P
    assert dr(sum([3, 4, 30])) == 1

    # 5. 137-map 3-cycle: 3→4→30→3
    assert 26 * 3 % P == 4 and sector(4) == 'SA'
    assert 26 * 4 % P == 30 and sector(30) == 'SA∩ST'
    assert 26 * 30 % P == 3 and sector(3) == 'ST'

    # 6. DR split: 6 cycles with DR=1, 6 with DR=2
    dr_vals = Counter(dr(sum(c)) for c in ALL_COSETS)
    assert dr_vals == {1: 6, 2: 6}

    # 7. SEED/3 ⊆ NQR
    for s in SEED:
        pre = s * pow(3, P - 2, P) % P
        assert legendre(pre, P) == P - 1

    # 8. SA∪ST partitions into 3 sovereign cosets summing to SEAM
    sov_cosets = [[3, 4, 30], [9, 12, 16], [21, 25, 28]]
    assert all(sum(c) % P == 0 for c in sov_cosets)
    covered = sorted(x for c in sov_cosets for x in c if x in SA or x in ST)
    assert covered == sorted(SA | ST)

    # 9. ord₃₇(3) = 18 = φ(37)/2
    assert pow(3, 18, P) == 1
    assert all(pow(3, k, P) != 1 for k in range(1, 18))

    # 10. 3^13 = 30 ∈ SA∩ST; exponent 13 is NQR
    assert pow(3, 13, P) == 30 and 30 in SA and 30 in ST
    assert legendre(13, P) == P - 1

    # 11. Mirror inverse pairs
    assert pow(3, 1, P) * pow(3, 17, P) % P == 1
    assert pow(3, 5, P) * pow(3, 13, P) % P == 1
    assert sector(pow(3, 1, P)) == 'ST' and sector(pow(3, 17, P)) == 'SA'
    assert sector(pow(3, 5, P)) == 'ST' and sector(pow(3, 13, P)) == 'SA∩ST'

    # 12. 3×k = ST requires k∈{1,4,7,10}; 3×k = SEED requires k∈{6,8,23}
    st_k = [k for k in range(1, P + 1) if (3 * k) % P in ST]
    assert st_k == [1, 4, 7, 10]
    seed_k = [k for k in range(1, P + 1) if (3 * k) % P in SEED]
    assert seed_k == [6, 8, 23]
    assert sum(seed_k) % P == 0  # SEED generators sum to SEAM

    # 13. 3^6 = 26 (multiplier) — powers of 3 generate the 137-map multiplier
    assert pow(3, 6, P) == 26

    print("All assertions passed.")


if __name__ == "__main__":
    run_assertions()
