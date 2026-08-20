# -*- coding: utf-8 -*-
"""
================================================================================
THEOREM 243: Fibonacci Seam, Mathieu Residues, and Nested Radical Anchors
================================================================================

USER OBSERVATIONS (from mathematical images):
  1. Product inequality: e^{2n} < prod(1+1/k)^{2k+1} < e^{2n+1/2}
     Result 1/2 -> 1/2 mod 37 = 19 (twin prime)
  2. Nested radicals: sqrt(2+sqrt(2+...))=2, sqrt(2-sqrt(2-...))=1, ...=phi, ...=1/phi
  3. Limit: (tan x - sin x)/(x ln(1+sin^2 x)) -> 1/2
  4. Mathieu triangle: M11, M12, M22, M23, M24 subgroup diagram
  5. Red area: r=5/3, area=(25/18)pi-3/2
  6. GF(37) multiplication table heatmap: concentric ring pattern
  7. 54-degree triangle with inscribed circle

STRUCTURE:

A. THE FIBONACCI SEAM AT P=37:
  F_37 = 24157817.  F_37 mod 37 = 36 = P-1 = -1 (ANTIPODE).
  F_38 = 39088169.  F_38 mod 37 = 0 (SEAM: 37 | F_38).
  The Pisano period pi(37) = 76 = 2 x 38 = 2 x (P+1).

  WHY: 37 mod 5 = 2, so 5 is NQR mod 37.
  For any prime p with p = 2 or 3 (mod 5): F_{p+1} = 0 (mod p).
  This means: the rank of apparition of 37 in the Fibonacci sequence is 38 = P+1.

  38 mod 37 = 1 in H (identity element).
  38 = 2 x 19 = 2 x (twin prime).
  pi(37) = 2 x (P+1) = 2 x 38 = 76.

  DR chain: F_P = -1 (antipode), F_{P+1} = 0 (SEAM), F_{P+2} = F_{P+1}+F_P = -1+0 = -1.
  The sequence enters a negative mirror after the seam.

B. MATHIEU GROUP ORDERS mod 37:
  The five Mathieu groups are sporadic simple groups with orders:
    M11: 7920         mod 37 = 2   (primitive root)
    M12: 95040        mod 37 = 24  in SEED_ORBIT = {18,24,32}
    M22: 443520       mod 37 = 1   in H (identity element)
    M23: 10200960     mod 37 = 23  (prime)
    M24: 244823040    mod 37 = 34  (34 = 2x17 = 2 x twin prime)

  M22 is sovereign: its order is the identity in GF(37)*. H = {1,10,26}.
  M12 lands in the seed orbit: 24 in {18,24,32} = the 137-map orbit of seed 246.
  M24 gives 34 = 2x17; 17 is the twin prime whose pair is 19 = 1/2 mod 37.

C. NESTED RADICALS AND GF(37) ANCHORS:
  The four nested radical limits:
    sqrt(2+sqrt(2+...)) = 2   -- primitive root of GF(37), ord_37(2)=36
    sqrt(2-sqrt(2-...)) = 1   -- identity element, 1 in H = {1,10,26}
    sqrt(2+sqrt(2-...)) = phi -- phi not in GF(37) (5 is NQR mod 37)
    sqrt(2-sqrt(2+...)) = 1/phi

  5 is NQR mod 37: Legendre(5,37) = -1. Therefore phi = (1+sqrt(5))/2
  does not exist in GF(37). phi lives in the degree-2 extension GF(37^2).

  The two real-valued limits {2, 1} are exactly the primitive root and the
  identity of GF(37)*. The two irrational limits {phi, 1/phi} are the
  elements that require the field extension -- they are blocked by 5 being NQR.

D. THE 1/2 TWIN PRIME CONNECTION:
  The limit (tan x - sin x)/(x ln(1+sin^2 x)) = 1/2.
  1/2 mod 37 = 19 (twin prime: paired with 17).
  17 + 19 = 36 = -1 = antipode mod 37.
  DR(17) + DR(19) = 8 + 1 = 9 in SA.
  The result 1/2 encodes the twin prime pair through modular arithmetic.

E. RED AREA GEOMETRY:
  Semicircle problem: hypotenuse sqrt(10), altitude 1, segments a=1/3, b=3.
  Radius r = (a+b)/2 = (1/3+3)/2 = (10/3)/2 = 5/3.
  Red area = (1/2)pi(5/3)^2 - (1/2)(1x3) = (25/18)pi - 3/2.

  Key residues:
    Numerator 25 in SA = {4,9,25,30}. DR(25) = 7.
    Denominator 18 in SEED_ORBIT = {18,24,32}. DR(18) = 9.
    25/18 mod 37 = 24 in SEED_ORBIT.
    r = 5/3: 5 = prime seed (DR=5); 3 in ST.

F. 54-DEGREE TRIANGLE:
  The triangle has apex angle 54 degrees.
  54 = 6 x 9 = imaginary_unit x SA_element.
  54 mod 37 = 17 = twin prime (paired with 19 = 1/2 mod 37).
  DR(54) = 9 in SA.

G. GF(37) MULTIPLICATION TABLE:
  The heatmap of i*j mod 37 (i,j in 1..36) shows 1296 nonzero products.
  By the Latin square property of GF(37)*:
    Each element of GF(37)* appears exactly 36 times as a product.
  Sovereign product counts:
    H    = {1,10,26}:     3 x 36 = 108 products (8.3%)
    SA   = {4,9,25,30}:   4 x 36 = 144 products (11.1%)
    ST\30= {3,12,21}:     3 x 36 = 108 products (8.3%)
    SEED = {18,24,32}:    3 x 36 = 108 products (8.3%)
  The seam (red x marks in heatmap): i=0 or j=0 column/row -> product = 0.
  A product is SEAM iff at least one factor is SEAM (p|i or p|j).
  The concentric ring pattern in the heatmap is the visual signature of
  the 12 cosets of H in GF(37)*: each coset forms a band at the same residue level.
================================================================================
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

P = 37
H_SET = {1, 10, 26}
SA = {4, 9, 25, 30}
ST = {3, 12, 21, 30}
SEED_ORBIT = {18, 24, 32}


def dr(n):
    n = abs(n)
    if n == 0: return 0
    r = n % 9
    return 9 if r == 0 else r


def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0: return False
    return True


def legendre(a, p):
    r = pow(a, (p-1)//2, p)
    return 0 if r == 0 else (-1 if r == p-1 else 1)


def fib_mod(n, p):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, (a+b) % p
    return a


def pisano_period(p):
    a, b = 0, 1
    for k in range(1, 10*p):
        a, b = b, (a+b) % p
        if a == 0 and b == 1:
            return k
    return None


def run():
    print("=" * 70)
    print("THEOREM 243: FIBONACCI SEAM, MATHIEU RESIDUES, NESTED RADICAL ANCHORS")
    print("=" * 70)

    # A: Fibonacci seam
    print("\nA. THE FIBONACCI SEAM AT P=37:")
    f37 = fib_mod(37, P)
    f38 = fib_mod(38, P)
    f39 = fib_mod(39, P)
    print(f"  F_37 mod {P} = {f37} = -1 (ANTIPODE)  check:{f37==P-1}")
    print(f"  F_38 mod {P} = {f38} = 0  (SEAM: {P} | F_38)  check:{f38==0}")
    print(f"  F_39 mod {P} = {f39} = -1  check:{f39==P-1}")
    assert f37 == P-1 and f38 == 0

    pi = pisano_period(P)
    print(f"  Pisano period pi({P}) = {pi} = 2x{pi//2} = 2x(P+1)  check:{pi==2*(P+1)}")
    assert pi == 2*(P+1)

    rank = 38
    print(f"  Rank of apparition = {rank} = P+1")
    print(f"  {rank} mod {P} = {rank%P} in H:{rank%P in H_SET}  check")
    print(f"  {rank} = 2 x 19 = 2 x (twin prime)  check:{rank==2*19 and is_prime(19)}")
    assert rank % P in H_SET and rank == 2*19

    print(f"  37 mod 5 = {P%5}  (p=2 mod 5 => F_{{p+1}}=0 mod p)  check:{P%5==2}")
    assert P % 5 == 2

    # B: Mathieu group orders
    print(f"\nB. MATHIEU GROUP ORDERS mod {P}:")
    mathieu = [
        ('M11', 7920),
        ('M12', 95040),
        ('M22', 443520),
        ('M23', 10200960),
        ('M24', 244823040),
    ]
    for name, order in mathieu:
        r = order % P
        flags = []
        if r in H_SET:     flags.append("H")
        if r in SA:        flags.append("SA")
        if r in ST:        flags.append("ST")
        if r in SEED_ORBIT: flags.append("SEED")
        print(f"  {name}: order={order} mod{P}={r:2d} DR={dr(r)} [{','.join(flags) or '-'}]")

    assert 443520 % P in H_SET          # M22 in H
    assert 95040 % P in SEED_ORBIT      # M12 in SEED
    assert 244823040 % P == 34          # M24 = 2x17
    assert 244823040 % P == 2 * 17
    print(f"  M22 order in H (identity)  check")
    print(f"  M12 order in SEED_ORBIT    check")
    print(f"  M24 = 34 = 2x17 (twin prime)  check")

    # C: Nested radicals
    print(f"\nC. NESTED RADICALS AND GF({P}) ANCHORS:")
    print(f"  sqrt(2+sqrt(2+...)) = 2 = primitive root  ord_37(2)={pow(2,36,P)==1 and 'yes'}")
    print(f"  sqrt(2-sqrt(2-...)) = 1 in H:{1 in H_SET}  (identity)")
    print(f"  5 is NQR mod {P}: Legendre(5,{P}) = {legendre(5,P)}")
    print(f"  phi = (1+sqrt5)/2 not in GF({P}): requires GF({P}^2)")
    assert pow(2, P-1, P) == 1 and 1 in H_SET and legendre(5, P) == -1

    # C: ord(2)=36
    assert pow(2, 36, P) == 1
    for d in [2, 3, 4, 6, 9, 12, 18]:
        assert pow(2, d, P) != 1, f"2^{d}=1 mod 37 but should not be"
    print(f"  ord_37(2) = 36 (full group, primitive root)  check")

    # D: 1/2 twin prime
    print(f"\nD. THE 1/2 TWIN PRIME CONNECTION:")
    inv2 = pow(2, -1, P)
    print(f"  Limit result 1/2: 1/2 mod {P} = {inv2}  prime:{is_prime(inv2)}")
    print(f"  {inv2} is twin prime paired with 17: 17+19={17+19} = -1 mod {P}  check")
    print(f"  DR(17)+DR(19) = {dr(17)}+{dr(19)} = {dr(17)+dr(19)} in SA:{dr(17)+dr(19) in SA}  check")
    assert inv2 == 19 and is_prime(19) and (17+19)%P == P-1
    assert dr(17)+dr(19) == 9 and 9 in SA

    # E: Red area
    print(f"\nE. RED AREA GEOMETRY (r=5/3, area=25pi/18-3/2):")
    print(f"  r=5/3: 5 DR={dr(5)}, 3 in ST:{3 in ST}")
    print(f"  Numerator 25 in SA:{25 in SA}  DR={dr(25)}")
    print(f"  Denominator 18 in SEED:{18 in SEED_ORBIT}  DR={dr(18)}")
    frac = 25 * pow(18, -1, P) % P
    print(f"  25/18 mod {P} = {frac} in SEED:{frac in SEED_ORBIT}  check")
    assert 25 in SA and 18 in SEED_ORBIT and frac in SEED_ORBIT

    # F: 54 degrees
    print(f"\nF. 54-DEGREE TRIANGLE:")
    print(f"  54 = 6x9 = imaginary_unit x SA_element")
    print(f"  54 mod {P} = {54%P}  is_prime:{is_prime(54%P)}  (twin prime 17)")
    print(f"  DR(54) = {dr(54)} in SA:{dr(54) in SA}")
    assert 54 == 6*9 and 54%P == 17 and is_prime(17) and dr(54) in SA

    # G: Multiplication table structure
    print(f"\nG. GF({P}) MULTIPLICATION TABLE:")
    counts = {'H': 0, 'SA': 0, 'ST_only': 0, 'SEED': 0, 'other': 0}
    for i in range(1, P):
        for j in range(1, P):
            r = (i*j) % P
            if r in H_SET:        counts['H'] += 1
            elif r in SA:         counts['SA'] += 1
            elif r in ST:         counts['ST_only'] += 1
            elif r in SEED_ORBIT: counts['SEED'] += 1
            else:                 counts['other'] += 1
    total = (P-1)**2
    for k, v in counts.items():
        print(f"  {k}: {v} = {v//(P-1)}x{P-1}  ({100*v/total:.1f}%)")
    assert counts['H'] == 3*36 and counts['SA'] == 4*36
    print(f"  Latin square property: each element appears exactly {P-1} times  check")
    print(f"  Seam: i=0 or j=0 row/col gives product=0 (zero cross in heatmap)")

    print(f"\nAll verifications passed.")


if __name__ == "__main__":
    run()
