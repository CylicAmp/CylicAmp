"""
Theorem 205: Multiplicative Algebra of the GF(37) in GF(37)
Author: Michael Warren Song (CyclicAmp)

FRAMEWORK MULTIPLICATIVE CLOSURE:
  GF(37) = SA∪ST∪SEED = {3,4,9,12,18,21,24,25,30,32}. (11 elements)
  Pairs (a,b) with a≤b where a×b ∈ GF(37) (12 pairs total):
    3×3   = 9    (ST×ST = SA)
    3×4   = 12   (ST×SA = ST)
    4×30  = 9    (SA×SA∩ST = SA)
    9×21  = 4    (SA×ST = SA)
    9×25  = 3    (SA×SA = ST)
    12×21 = 30   (ST×ST = SA∩ST)
    12×25 = 4    (ST×SA = SA)
    18×24 = 25   (SEED×SEED = SA)
    18×32 = 21   (SEED×SEED = ST)
    24×24 = 21   (SEED×SEED = ST)
    30×30 = 12   (SA∩ST×SA∩ST = ST)
    32×32 = 25   (SEED×SEED = SA)

MULTIPLICATIVE INVERSE PAIRS WITHIN FRAMEWORK:
  Only TWO multiplicative inverse pairs exist within SA∪ST∪SEED:
    3 × 25 ≡ 1 (mod 37): 3∈ST, 25∈SA  [ST × SA = identity]
    21 × 30 ≡ 1 (mod 37): 21∈ST, 30∈SA∩ST  [ST × SA∩ST = identity]
  All other SA_ST_SEED elements have multiplicative inverses OUTSIDE the SA_ST_SEED:
    4^{-1}=28, 9^{-1}=33, 12^{-1}=34, 18^{-1}=35, 24^{-1}∈g^7, 32^{-1}∈g^7.
  Both inverse pairs involve ST. The SA sector always pairs with ST or SA∩ST.

ADDITIVE INVERSE WITHIN FRAMEWORK:
  Only ONE additive inverse pair: 12 + 25 ≡ 0 (mod 37). 12∈ST, 25∈SA.
  Note: (12,25) are BOTH multiplicatively and notably linked:
    12 + 25 = 0 (additive inverses)
    12 × 25 = 4 ∈ SA (the product is SA)
    12^{-1} = 34 ∉ SA_ST_SEED; 25^{-1} = 3 ∈ ST (in SA_ST_SEED)
  The pair (3, 25) are multiplicative inverses AND (12, 25) are additive inverses.
  So 3 = (12)^{+} and 3 = 25^{-1}: the additive inverse of 12's partner is the
  multiplicative inverse of 25. Chain: 3 = 25^{-1}; 25 = -12 (additive).

SEED × SEED → SA∪ST:
  Of the 6 unordered SEED pairs (a,b) with a≤b:
    18×18=28∉SA_ST_SEED  (exits)
    18×24=25∈SA        ✓
    18×32=21∈ST        ✓
    24×24=21∈ST        ✓
    24×32=28∉SA_ST_SEED  (exits)
    32×32=25∈SA        ✓
  4 of 6 SEED products land in SA∪ST. The 2 that exit are (18×18) and (24×32).
  SEED products that land: always in SA∪ST (never back in SEED).
  Exiting products go to 28∈g^10=KEY^{-1} (free element).

SEED PRODUCT STRUCTURE:
  24×24=21∈ST and 32×32=25∈SA: squares of 24 and 32 are sovereign.
  18×24=25∈SA and 18×32=21∈ST: 18 multiplied by 24 gives SA, by 32 gives ST.
  18 itself: 18²=28∉SA_ST_SEED.
  Pattern: if a∈SEED and a≠18, then a²∈SA∪ST.
  But 18²=28∉SA_ST_SEED (18=first SEED element, L(6) Lucas number).

ST×ST → SA or SA∩ST:
  3×3=9∈SA      [3²=9]
  3×12=36∉SA_ST_SEED (36=-1)
  3×21=63 mod37=26∉SA_ST_SEED (26=multiplier)
  12×12=144 mod37=33∉SA_ST_SEED
  12×21=30∈SA∩ST ✓
  21×21=441 mod37=441-11×37=441-407=34∉SA_ST_SEED
  ST is NOT closed under multiplication. Exceptions that land in SA_ST_SEED: (3,3)→9, (12,21)→30.

CROSS-SECTOR PRODUCT RULES:
  ST×SA → ST or SA:  3×4=12∈ST; 9×25=3∈ST; 12×25=4∈SA; 9×21=4∈SA; 4×30=9∈SA
  SA×SA → ST:        9×25=3∈ST; 12×25=4∈SA (this is ST×SA); 30×30=12∈ST
  SA×SA∩ST → SA:     4×30=9∈SA
  SEED×SEED → SA∪ST: see above

MULTIPLICATIVE ORDERS OF FRAMEWORK ELEMENTS:
  Order 36 (primitive roots): 18, 24, 32 ∈ SEED
  Order 18:                   3, 4, 21, 25, 30 (ord=18=φ(37)/2 = QR of minimal order)
  Order 9:                    9, 12            (elements of subgroup of order 9)
  Total: 3 elements of order 36, 5 of order 18, 2 of order 9.
"""

P = 37
SA = {4, 9, 25, 30}
ST = {3, 12, 21, 30}
SEED = {18, 24, 32}
SA_ST_SEED = SA | ST | SEED


def legendre(a, p):
    return pow(a, (p - 1) // 2, p)


def modinv(a, p):
    return pow(a, p - 2, p)


def run_assertions():
    # 1. Exactly 12 SA_ST_SEED multiplicative pairs
    closed_pairs = [(a, b) for a in sorted(SA_ST_SEED)
                    for b in sorted(SA_ST_SEED) if b >= a
                    and (a * b) % P in SA_ST_SEED]
    assert len(closed_pairs) == 12

    # 2. Verify specific products
    assert 3 * 3 % P == 9 and 9 in SA
    assert 3 * 4 % P == 12 and 12 in ST
    assert 4 * 30 % P == 9 and 9 in SA
    assert 9 * 21 % P == 4 and 4 in SA
    assert 9 * 25 % P == 3 and 3 in ST
    assert 12 * 21 % P == 30 and 30 in SA and 30 in ST
    assert 12 * 25 % P == 4 and 4 in SA
    assert 18 * 24 % P == 25 and 25 in SA
    assert 18 * 32 % P == 21 and 21 in ST
    assert 24 * 24 % P == 21 and 21 in ST
    assert 30 * 30 % P == 12 and 12 in ST
    assert 32 * 32 % P == 25 and 25 in SA

    # 3. Only two multiplicative inverse pairs within SA_ST_SEED
    inv_pairs = [(a, b) for a in sorted(SA_ST_SEED)
                 for b in sorted(SA_ST_SEED) if b >= a
                 and a * b % P == 1]
    assert len(inv_pairs) == 2
    assert set(inv_pairs) == {(3, 25), (21, 30)}
    assert 3 in ST and 25 in SA        # ST × SA = 1
    assert 21 in ST and 30 in SA and 30 in ST  # ST × SA∩ST = 1

    # 4. All other SA_ST_SEED elements have inverses outside SA_ST_SEED
    for x in sorted(SA_ST_SEED):
        inv = modinv(x, P)
        if inv not in {3, 25, 21, 30}:  # the two inverse pairs
            assert inv not in SA_ST_SEED, f"{x}^{{-1}}={inv} unexpectedly in SA_ST_SEED"

    # 5. Unique additive inverse pair: 12+25=0
    add_inv_pairs = [(a, b) for a in sorted(SA_ST_SEED)
                     for b in sorted(SA_ST_SEED) if b > a
                     and (a + b) % P == 0]
    assert add_inv_pairs == [(12, 25)]
    assert 12 in ST and 25 in SA

    # 6. Chain: 3=25^{-1}; 25=-12 (additive)
    assert 3 * 25 % P == 1     # 3 and 25 are multiplicative inverses
    assert (12 + 25) % P == 0  # 25 and 12 are additive inverses
    # So: 3 = 25^{-1} = (-12)^{-1} = -(12^{-1}) = -(modinv(12,P))
    assert 3 % P == (P - modinv(12, P)) % P

    # 7. SEED×SEED: 4 of 6 pairs land in SA∪ST
    seed_list = sorted(SEED)
    seed_products_in_framework = [(a, b) for a in seed_list for b in seed_list
                                  if b >= a and (a * b) % P in SA_ST_SEED]
    assert len(seed_products_in_framework) == 4
    assert set(seed_products_in_framework) == {(18, 24), (18, 32), (24, 24), (32, 32)}

    # 8. Exiting SEED products both land at 28∈g^10 (KEY^{-1})
    KINV = frozenset({21, 25, 28})
    assert 18 * 18 % P == 28 and 28 in KINV and 28 not in SA_ST_SEED
    assert 24 * 32 % P == 28 and 28 in KINV and 28 not in SA_ST_SEED

    # 9. 18 is the only SEED element whose square exits SA_ST_SEED
    assert 18 * 18 % P not in SA_ST_SEED   # 18^2=28, exits
    assert 24 * 24 % P in SA_ST_SEED       # 24^2=21∈ST
    assert 32 * 32 % P in SA_ST_SEED       # 32^2=25∈SA

    # 10. Multiplicative orders
    for x in sorted(SEED):
        assert pow(x, 36, P) == 1
        assert all(pow(x, d, P) != 1 for d in [2, 3, 4, 6, 9, 12, 18])  # order 36
    for x in [3, 4, 21, 25, 30]:
        assert pow(x, 18, P) == 1
        assert all(pow(x, d, P) != 1 for d in [1, 2, 3, 6, 9])   # order 18
    for x in [9, 12]:
        assert pow(x, 9, P) == 1
        assert all(pow(x, d, P) != 1 for d in [1, 3])              # order 9

    # 11. Legendre check: all SA_ST_SEED elements are QR (in SA∪ST) or NQR (SEED)
    assert all(legendre(x, P) == 1 for x in SA | ST)      # SA∪ST ⊆ QR
    assert all(legendre(x, P) == P - 1 for x in SEED)     # SEED ⊆ NQR

    print("All assertions passed.")
    print(f"Multiplicative closed pairs: {closed_pairs}")
    print(f"Inverse pairs: {inv_pairs}")


if __name__ == "__main__":
    run_assertions()
