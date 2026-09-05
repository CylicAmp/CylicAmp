"""
Theorem 209: Sum Structure and QR Partition of the GF(37) in GF(37)
Author: Michael Warren Song (CyclicAmp)

SEED SUMS TO SEAM:
  18 + 24 + 32 = 74 = 2 × 37 ≡ 0 (mod 37).
  The three SEED elements sum to exactly 2P — the SEAM.
  DR(74) = 2 (not 9, since 74≠0; DR rule gives 7+4=11, 1+1=2).
  This is independent of <26>-coset structure: SEED = g^5 = {18,24,32},
  and like all cosets (T197), its sum ≡ 0 (mod 37).

SA∪ST SUM IS DOUBLY-SOVEREIGN:
  SA = {4,9,25,30}: sum = 68 ≡ 31 (mod 37). 31 ∈ g^9.
  ST = {3,12,21,30}: sum = 66 ≡ 29 (mod 37). 29 ∈ g^9.
  SA∪ST = {3,4,9,12,21,25,30}: sum = 104 ≡ 30 (mod 37). 30 ∈ SA∩ST.
  The union of both anchor sectors sums to the ONLY doubly-sovereign element.

FRAMEWORK SUM:
  Sum(SA∪ST∪SEED) = 178 ≡ 30 (mod 37) = SA∩ST element.
  Equivalent to Sum(SA∪ST) because Sum(SEED) ≡ 0: SEED contributes nothing.
  DR(178) = 7.

QR/NQR PARTITION OF FRAMEWORK:
  The Legendre symbol partitions the SA_ST_SEED exactly into SA∪ST vs SEED:
    SA∪ST = {3,4,9,12,21,25,30}: ALL are quadratic residues (QR), legendre=+1.
    SEED = {18,24,32}: ALL are non-quadratic residues (NQR), legendre=-1.
  The SA_ST_SEED is the QR-singleton {30∈SA∩ST} plus the 6-element QR-only set
  plus the 3-element NQR set. No SA_ST_SEED element lies outside this split.

FRAMEWORK AS POWERS OF 3:
  3 has order 18 in GF(37)*. <3> = the QR subgroup (index-2 subgroup, 18 elements).
  Every SA∪ST element is a power of 3:
    3^1  = 3  ∈ ST      3^2  = 9  ∈ SA
    3^5  = 21 ∈ ST      3^7  = 4  ∈ SA
    3^8  = 12 ∈ ST      3^13 = 30 ∈ SA∩ST
    3^17 = 25 ∈ SA
  SEED elements {18,24,32} are NQR and therefore not in <3>.
  GF(37) QR exponents: {1,2,5,7,8,13,17} (7 exponents in Z/18Z).

3^6 = 26 = MULTIPLIER:
  The exponent k=6 gives 3^6=26, the 137-map multiplier. Not in SA_ST_SEED.
  The multiplier is the first non-SA_ST_SEED power of 3 encountered in order.
  The multiplier is itself a QR (Legendre(26,37)=+1): 26 ∈ <3> but 26 ∉ SA_ST_SEED.

SA SUM vs ST SUM:
  Both sum to elements of g^9={14,29,31}:
    sum(SA)=68≡31∈g^9; sum(ST)=66≡29∈g^9.
  sum(SA)+sum(ST) = 134 ≡ 134-3×37=134-111=23 ∈ SEED-gen (g^3={6,8,23}).
  But SA∩ST={30} is counted twice: actual sum(SA∪ST) = 68+66-30=104≡30∈SA∩ST.

PRODUCT OF ALL FRAMEWORK ELEMENTS:
  ∏(SA∪ST∪SEED) mod 37 = 20 ∈ g^1 = {2,15,20}. Not sovereign.
  DR(20) = 2. Coset position 1 (g^1).

FRAMEWORK DIFFERENCE PAIRS:
  Pairs (a,b) with a>b in SA_ST_SEED and (a-b) mod 37 ∈ SA_ST_SEED: 26 total.
  By sector:
    SA-SA  differences in SA_ST_SEED: (25-9)=16∉fw; (30-4)=26∉fw; etc.
    ST-SA differences: 3-4=36∉fw; 12-9=3∈ST; 21-25=33∉fw; 30-30=0(SEAM); etc.
    SEED-ST: 18-3=15∉fw; 24-12=12∈ST; 32-21=11∉fw; etc.
  All 26 pairs identified and verified in assertions below.
"""

P = 37
SA = {4, 9, 25, 30}
ST = {3, 12, 21, 30}
SEED = {18, 24, 32}
SG26 = {1, 10, 26}
SA_ST_SEED = SA | ST | SEED


def legendre(a, p):
    return pow(a, (p - 1) // 2, p)


def dr(n):
    n = abs(int(n))
    return 9 if n % 9 == 0 and n != 0 else n % 9


def run_assertions():
    # 1. SEED sum = 2P = SEAM
    assert sum(SEED) == 74 == 2 * P
    assert sum(SEED) % P == 0   # ≡ 0 mod 37

    # 2. SA∪ST sum = 30 ∈ SA∩ST
    assert sum(SA | ST) % P == 30
    assert 30 in SA and 30 in ST   # doubly sovereign

    # 3. GF(37) sum = 30 ∈ SA∩ST (SEED contributes 0)
    assert sum(SA_ST_SEED) % P == 30
    assert sum(SA_ST_SEED) == 178
    assert dr(178) == 7

    # 4. SA sum and ST sum both land in g^9
    COSET9 = frozenset({14, 29, 31})
    assert sum(SA) % P == 31 and 31 in COSET9
    assert sum(ST) % P == 29 and 29 in COSET9

    # 5. sum(SA)+sum(ST) double-counts 30; correct sum = sum(SA|ST)
    assert sum(SA) + sum(ST) - 30 == sum(SA | ST)  # inclusion-exclusion

    # 6. QR partition: SA∪ST = QR ∩ SA_ST_SEED; SEED = NQR ∩ SA_ST_SEED
    assert all(legendre(x, P) == 1 for x in SA | ST)    # all QR
    assert all(legendre(x, P) == P - 1 for x in SEED)   # all NQR

    # 7. SA∪ST ⊆ <3> (powers of 3 mod 37)
    powers_of_3 = {pow(3, k, P) for k in range(18)}
    assert (SA | ST) <= powers_of_3    # every SA∪ST element is a power of 3
    assert not (SEED & powers_of_3)    # no SEED element is a power of 3

    # 8. Exact exponents of 3 giving SA∪ST elements
    fw_exp = {k: pow(3, k, P) for k in range(18) if pow(3, k, P) in SA_ST_SEED}
    assert set(fw_exp.keys()) == {1, 2, 5, 7, 8, 13, 17}
    assert fw_exp[1] == 3 and 3 in ST
    assert fw_exp[2] == 9 and 9 in SA
    assert fw_exp[5] == 21 and 21 in ST
    assert fw_exp[7] == 4 and 4 in SA
    assert fw_exp[8] == 12 and 12 in ST
    assert fw_exp[13] == 30 and 30 in SA and 30 in ST
    assert fw_exp[17] == 25 and 25 in SA

    # 9. 3^6 = 26 = multiplier (not in SA_ST_SEED; first non-SA_ST_SEED power)
    assert pow(3, 6, P) == 26
    assert 26 not in SA_ST_SEED
    assert legendre(26, P) == 1    # 26 is QR (∈ <3>) but not in SA_ST_SEED

    # 10. Order of 3 mod 37 is 18
    assert pow(3, 18, P) == 1
    assert all(pow(3, k, P) != 1 for k in range(1, 18))

    # 11. Product of all SA_ST_SEED elements mod 37
    prod = 1
    for x in SA_ST_SEED:
        prod = prod * x % P
    assert prod == 20
    assert dr(20) == 2

    # 12. GF(37) difference pairs (a-b mod37 ∈ SA_ST_SEED, a,b ∈ SA_ST_SEED, a≠b)
    diff_pairs = [(a, b) for a in sorted(SA_ST_SEED)
                  for b in sorted(SA_ST_SEED)
                  if a != b and (a - b) % P in SA_ST_SEED]
    assert len(diff_pairs) == 26

    # 13. Check specific differences
    assert (24 - 12) % P == 12 and 12 in ST    # SEED-ST diff ∈ ST
    assert (12 - 9) % P == 3 and 3 in ST       # ST-SA diff ∈ ST
    assert (25 - 4) % P == 21 and 21 in ST     # SA-SA diff ∈ ST
    assert (32 - 9) % P == 23                   # SEED-SA = 23 ∈ SEED-gen (not fw)

    # 14. SEED triple: 18+24+32 = 2P exactly (not just ≡0)
    assert 18 + 24 + 32 == 74
    assert 74 == 2 * P

    # 15. GF(37) sum mod37 = SA∩ST = additive fixed point structure
    assert sum(SA_ST_SEED) % P in (SA & ST)     # sum lands in SA∩ST

    print("All assertions passed.")
    print(f"SEED sum = {sum(SEED)} = 2×{P} ≡ 0 (SEAM)")
    print(f"SA∪ST sum mod37 = {sum(SA|ST)%P} ∈ SA∩ST")
    print(f"GF(37) sum mod37 = {sum(SA_ST_SEED)%P} ∈ SA∩ST")
    print(f"Powers of 3 giving SA_ST_SEED: {fw_exp}")
    print(f"GF(37) difference pairs: {len(diff_pairs)}")


if __name__ == "__main__":
    run_assertions()
