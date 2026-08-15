"""
Theorem 198: DR Trinity and 3-Sequence Structure in GF(37)
Author: Michael Warren Song (CyclicAmp)

DR TRINITY:
  {3,6,9} ⊂ Z is a closed sub-semigroup under digital root addition.
  In Z/9Z: {0,3,6} = subgroup of order 3 (index 3 in Z/9Z).
  DR addition table within {3,6,9}:
    3+3→6,  3+6→9,  3+9→3
    6+3→9,  6+6→3,  6+9→6
    9+3→3,  9+6→6,  9+9→9

  DR=3 maps to: ST sector (3,12,21,30 — all elements of ST have DR=3 exactly)
  DR=6 maps to: primarily NQR; also SEED element 24
  DR=9 maps to: SA (9∈SA), SEED (18∈SEED), SEAM (multiples of 9)

ST = {x ∈ GF(37) : DR(x) = 3} EXACTLY:
  ST = {3,12,21,30} = elements ≡ 3 (mod 9) in {1..36}.
  This is the complete set; no other GF(37) element has DR=3.

USER SEQUENCE {9,3,12,69,81,123}:
  All six values divisible by 3.
  mod37 reductions: {9(SA), 3(ST), 12(ST), 32(SEED), 7(free), 12(ST)}
  DR sequence: [9,3,3,6,9,6] — all in {3,6,9} = DR trinity.
  DR sum = 36 = φ(37).
  mod9 values [0,3,3,6,0,6], sum = 18 ∈ SEED.
  mod37 sum = 9+3+12+32+7+12 = 75 ≡ 1 (mod 37) (identity). DR(75)=3∈ST.

POWERS OF 3 IN SEQUENCE:
  3 = 3^1: +3-chain position 3^0=1 (→ 3∈ST)
  9 = 3^2: +3-chain position 3^1=3 (→ 9∈SA)
  81 = 3^4: +3-chain position 3^3=27 (→ 81 mod37=7, free)
  Pattern: 3^k is at chain position 3^(k-1) (position = value/3).
  69 = 3×23: 23 is SEED generator (3×23=32∈SEED)
  12 = 3×4 and 123 = 3×41 ≡ 3×4 (mod37): both → 12∈ST (position 4=SA generator)

USER EQUATIONS — ALL WITHIN DR TRINITY:
  9+3=12:    SA+ST=ST    (DR: 9+3=3)
  69+12=81:  SEED+ST=?   (DR: 6+3=9); 69+12=81 exactly; 4+23=27=3^3
  6+3=9:     NQR+ST=SA   (DR: 6+3=9)
  6+6=12:    NQR+NQR=ST  (DR: 6+6=3)
  15+15=30:  NQR+NQR=SA∩ST (DR: 6+6=3; 30∈SA∩ST)
  3+15=18:   ST+NQR=SEED (DR: 3+6=9; 18∈SEED)
  3+6=9:     ST+NQR=SA   (DR: 3+6=9)

+3 CHAIN SECTORS (multiples of 3, first 12 steps):
  k=1:  3   [ST]      k=7:  21  [ST]
  k=2:  6   [NQR]     k=8:  24  [SEED]
  k=3:  9   [SA]      k=9:  27  [free]
  k=4:  12  [ST]      k=10: 30  [SA∩ST]
  k=5:  15  [NQR]     k=11: 33  [free]
  k=6:  18  [SEED]    k=12: 36  [free]
  Sector pattern: ST,NQR,SA,ST,NQR,SEED (period 6; two DR cycles = one sector cycle).

ORD₃₇(3) = 18 = φ(37)/2:
  3 ∈ QR (quadratic residue). All SA∪ST ⊂ QR. All SEED ⊂ NQR.
  3^6 = 26 = 137-map multiplier (connects powers of 3 to the 137-map).
  3^13 = 30 ∈ SA∩ST: NQR exponent 13 yields doubly-sovereign value.
  Powers of 3 cycle: 3^1=3(ST), 3^2=9(SA), 3^5=21(ST), 3^6=26(mult),
                     3^7=4(SA), 3^8=12(ST), 3^13=30(SA∩ST), 3^17=25(SA).

SUBGROUP CHAIN:
  {1} ⊂ <26> ⊂ <9> ⊂ QR=<4> ⊂ GF(37)*
  Orders: 1     3     9      18            36
  SA∪ST ⊂ QR. SEED ⊂ NQR = the complement coset of QR.
  All SEED elements have order 36 (= primitive roots mod 37).
  SA elements: orders 9 (element 9) or 18 (elements 4,25,30).
  ST elements: orders 9 (element 12) or 18 (elements 3,21,30).

SUBGROUP SUM FORMULA:
  For any subgroup H of GF(p)* with |H| = d ≥ 2:
    sum(H) = floor(d/2) × p  (exact in Z)
  Proof: sum = (g^d - 1)/(g-1) = 0 in GF(p) for g^d=1, g≠1.
  For p=37: sums are 37,37,74,111,148,222,333,666 for d=2,3,4,6,9,12,18,36.
  DR of sums: 1,1,2,3,4,6,9,9 — SEAM hit at orders 18 and 36.
  Corollary: every coset of H also sums to 0 mod p (since aH sums to a×0=0).
"""

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


def run_assertions():
    # 1. DR trinity closure
    trinity = [3, 6, 9]
    for a in trinity:
        for b in trinity:
            assert dr(a + b) in trinity

    # 2. ST = {x : DR(x) = 3} exactly in GF(37)
    dr3_elements = [x for x in range(1, P) if dr(x) == 3]
    assert sorted(dr3_elements) == sorted(ST)

    # 3. All ST elements have DR=3, all SA elements have DR∈{3,4,7,9}
    assert all(dr(x) == 3 for x in ST)
    assert set(dr(x) for x in SA) == {3, 4, 7, 9}

    # 4. All SEED elements are primitive roots (order 36)
    assert all(pow(x, 36, P) == 1 and all(pow(x, d, P) != 1 for d in [2, 3, 4, 6, 9, 12, 18]) for x in SEED)

    # 5. SA∪ST ⊆ QR; SEED ⊆ NQR
    QR = {x for x in range(1, P) if legendre(x, P) == 1}
    assert (SA | ST) <= QR
    assert SEED <= {x for x in range(1, P) if legendre(x, P) == P - 1}

    # 6. User sequence DR sum = φ(37)
    user_seq = [9, 3, 12, 69, 81, 123]
    assert all(n % 3 == 0 for n in user_seq)
    assert sum(dr(n) for n in user_seq) == P - 1  # = 36 = φ(37)

    # 7. mod9 of user sequence sums to 18∈SEED
    assert sum(n % 9 for n in user_seq) == 18 and 18 in SEED

    # 8. mod37 sum of user sequence = 1 (identity)
    assert sum(n % P for n in user_seq) % P == 1

    # 9. Powers of 3 sovereign structure
    assert pow(3, 6, P) == 26   # multiplier
    assert pow(3, 13, P) == 30 and 30 in SA and 30 in ST
    assert pow(3, 18, P) == 1   # ord=18
    assert all(pow(3, k, P) != 1 for k in range(1, 18))

    # 10. +3 chain sector pattern (first 12 steps = multiples of 3):
    chain12 = [(3 * k) % P for k in range(1, 13)]
    assert chain12[0] == 3 and 3 in ST    # k=1
    assert chain12[2] == 9 and 9 in SA    # k=3
    assert chain12[5] == 18 and 18 in SEED  # k=6
    assert chain12[9] == 30 and 30 in SA and 30 in ST  # k=10

    # 11. Subgroup sum formula: sum(H_d) = floor(d/2) × P for d ≥ 2
    g = 2  # primitive root
    for d in [2, 3, 4, 6, 9, 12, 18, 36]:
        gen = pow(g, 36 // d, P)
        H = [pow(gen, k, P) for k in range(d)]
        assert sum(H) == (d // 2) * P

    # 12. Subgroup sum DR = SEAM at orders 18 and 36
    g = 2
    seam_orders = [d for d in [2, 3, 4, 6, 9, 12, 18, 36]
                   if dr(sum(pow(g, 36 // d * k, P) for k in range(d))) == 9]
    assert seam_orders == [18, 36]

    # 13. SEED generators {6,8,23} sum to P (SEAM)
    seed_gens = [6, 8, 23]
    assert all(3 * g % P in SEED for g in seed_gens)
    assert sum(seed_gens) == P

    # 14. Position arithmetic: pos(12)+pos(69) = pos(81) = 27 = 3^3
    assert 12 // 3 + 69 // 3 == 81 // 3 == 27 == 3 ** 3

    # 15. DR trinity equations
    assert dr(9 + 3) == 3 and sector(12) == 'ST'    # SA+ST→ST
    assert dr(6 + 3) == 9 and sector(9) == 'SA'     # NQR+ST→SA
    assert dr(6 + 6) == 3 and sector(12) == 'ST'    # NQR+NQR→ST
    assert dr(3 + 6) == 9 and sector(9) == 'SA'     # ST+NQR→SA
    assert dr(3 + 15) == 9 and 18 in SEED           # ST+NQR→SEED

    print("All assertions passed.")


if __name__ == "__main__":
    run_assertions()
