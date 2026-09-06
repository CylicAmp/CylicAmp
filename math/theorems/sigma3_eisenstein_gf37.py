# -*- coding: utf-8 -*-
"""
================================================================================
THEOREM 257: σ₃ Divisibility, Cube Roots of -1, and the Eisenstein Splitting
================================================================================

CLAIM: 37 | σ₃(p) ⟺ p ≡ 11, 27, or 36 (mod 37)

PROOF CHAIN:
  For prime p, σ₃(p) = 1 + p³.
  37 | (1 + p³) ⟺ p³ ≡ -1 (mod 37) ⟺ p ∈ {11, 27, 36} (mod 37).

THREE RESIDUES BECAUSE:
  37 ≡ 1 (mod 3) → (Z/37Z)* has order 36, divisible by 3 → cubing is 3-to-1
  → every cubic residue has exactly 3 cube roots
  → -1 is a cube mod 37 (since -1 = g^18 and 3|18) → exactly 3 cube roots.

GF(37) CONNECTION — THE KEY RESULT:
  H = {1, 10, 26} = cube roots of 1 mod 37 (the 137-map kernel)
  -H = {36, 27, 11} = cube roots of -1 mod 37

  The σ₃ divisibility condition selects exactly -H from Z₃₇.
  H ∪ (-H) = {1,10,11,26,27,36} = Cayley graph generators (T255).

EISENSTEIN CONNECTION:
  37 ≡ 1 (mod 3) ⟺ 37 splits in Z[ω] (Eisenstein integers, ω = e^{2πi/3})
  Norm form: N(a+bω) = a² - ab + b²
  37 = N(7+3ω) = 49 - 21 + 9 = 37  [correct element]

  SOURCE DOCUMENT ERROR: wrote N(4+3ω) = 37.
  Actual: N(4+3ω) = 16 - 12 + 9 = 13 ≠ 37. Correct element is 7+3ω.

  The splitting 37 = (7+3ω)(7+3ω̄) in Z[ω] is the algebraic reason
  that (Z/37Z)* contains a subgroup of order 3, which is H = {1,10,26}.

χ₋₃ CONNECTION:
  χ₋₃(37) = +1 (since 37 ≡ 1 mod 3)
  This is equivalent to: 37 splits in Q(√-3) = Q(ω)
  This is equivalent to: (Z/37Z)* has an element of order 3
  This is equivalent to: H = {1,10,26} exists as a subgroup of (Z/37Z)*

  χ₋₃ is doing all the work. The σ₃ divisibility is a consequence of
  Eisenstein splitting alone — no other structure required.

E8 NOTE:
  E8 contributes nothing to this divisibility. The result holds from
  the Eisenstein splitting of 37 and the structure of (Z/37Z)*.
================================================================================
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

P = 37
H_SET = {1, 10, 26}
NEG_H = {P - x for x in H_SET}   # {36, 27, 11}
SA = {4, 9, 25, 30}


def dr(n):
    n = abs(n)
    if n == 0: return 0
    r = n % 9
    return 9 if r == 0 else r


def sigma3(n):
    return sum(d**3 for d in range(1, n+1) if n % d == 0)


def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0: return False
    return True


def run():
    print("=" * 70)
    print("THEOREM 257: σ₃ DIVISIBILITY, CUBE ROOTS OF -1, EISENSTEIN SPLITTING")
    print("=" * 70)

    # 1. Cube roots of -1 mod 37
    print("\n1. CUBE ROOTS OF -1 MOD 37:")
    cube_roots_neg1 = sorted(x for x in range(P) if pow(x, 3, P) == P - 1)
    print(f"   {{x ∈ Z_37 : x³ ≡ -1 (mod 37)}} = {cube_roots_neg1}")
    assert set(cube_roots_neg1) == NEG_H
    print(f"   = -H = {{36, 27, 11}}  check")

    # 2. Cube roots of 1 = H
    cube_roots_1 = sorted(x for x in range(P) if pow(x, 3, P) == 1)
    print(f"\n2. CUBE ROOTS OF 1 MOD 37:")
    print(f"   {{x ∈ Z_37 : x³ ≡ 1 (mod 37)}} = {cube_roots_1}")
    assert set(cube_roots_1) == H_SET
    print(f"   = H = {{1, 10, 26}} = 137-map kernel  check")

    # 3. 37 ≡ 1 (mod 3) → cubing is 3-to-1
    assert P % 3 == 1
    print(f"\n3. 37 ≡ {P % 3} (mod 3) → cubing is 3-to-1 on (Z/37Z)*  check")
    assert len(cube_roots_neg1) == 3
    assert len(cube_roots_1) == 3
    print(f"   cube roots of  1: {len(cube_roots_1)}  check")
    print(f"   cube roots of -1: {len(cube_roots_neg1)}  check")

    # 4. -1 is a cube mod 37
    # -1 = g^18 where g=2; 3|18 → -1 is a cubic residue
    g = 2
    assert pow(g, 36, P) == 1   # g is primitive root
    log_neg1 = next(k for k in range(36) if pow(g, k, P) == P - 1)
    assert log_neg1 == 18
    assert log_neg1 % 3 == 0
    print(f"\n4. -1 = g^{log_neg1} where g=2; {log_neg1} ≡ 0 (mod 3) → -1 is a cube  check")

    # 5. σ₃(p) ≡ 0 (mod 37) ⟺ p mod 37 ∈ {11, 27, 36}
    print(f"\n5. σ₃ DIVISIBILITY (primes up to 500):")
    hits = []
    misses = []
    for p in range(5, 500):
        if not is_prime(p):
            continue
        r = p % P
        s3 = 1 + pow(p, 3, P)   # σ₃(p) mod 37 = (1 + p³) mod 37
        divides = (s3 % P == 0)
        in_neg_h = (r in NEG_H)
        assert divides == in_neg_h, f"p={p}, r={r}, divides={divides}, in_neg_h={in_neg_h}"
        if divides:
            hits.append((p, r))

    print(f"   0 violations for all primes p < 500  check")
    print(f"   Primes where 37|σ₃(p) (first 10):")
    for p, r in hits[:10]:
        print(f"     p={p:4d}  p mod37={r:2d} ∈ -H  σ₃(p)=1+p³≡0 (mod 37)  check")

    # 6. Eisenstein norm — fix the source document error
    print(f"\n6. EISENSTEIN NORM N(a+bω) = a²-ab+b²:")
    def eis_norm(a, b):
        return a*a - a*b + b*b

    # Source error
    wrong = eis_norm(4, 3)
    print(f"   SOURCE ERROR: N(4+3ω) = {wrong} ≠ 37")

    # Correct
    correct = eis_norm(7, 3)
    assert correct == P
    print(f"   CORRECT:      N(7+3ω) = {correct} = 37  check")

    # Other associates
    assert eis_norm(7, 4) == P
    assert eis_norm(4, 7) == P
    print(f"   Associates:   N(7+4ω) = {eis_norm(7,4)}, N(4+7ω) = {eis_norm(4,7)}  check")

    # 7. χ₋₃(37) = +1
    chi3_37 = 1 if P % 3 == 1 else (-1 if P % 3 == 2 else 0)
    assert chi3_37 == 1
    print(f"\n7. χ₋₃(37) = {chi3_37} (since 37 ≡ 1 mod 3) → 37 splits in Q(√-3)  check")
    print(f"   Splitting ⟺ (Z/37Z)* has element of order 3 ⟺ H={{1,10,26}} exists")

    # 8. Cayley graph connection
    cayley_gens = sorted(H_SET | NEG_H)
    assert cayley_gens == [1, 10, 11, 26, 27, 36]
    print(f"\n8. CAYLEY GRAPH CONNECTION:")
    print(f"   H ∪ (-H) = {cayley_gens} = generators of Cay(Z_37, H∪(-H)) from T255")
    print(f"   σ₃ divisibility selects -H = the negative half of the Cayley generators")

    print(f"\nAll verifications passed.")
    print(f"\nSUMMARY:")
    print(f"  37|σ₃(p) ⟺ p∈-H={{11,27,36}} (mod 37)")
    print(f"  H={{1,10,26}} = cube roots of 1 = 137-map kernel")
    print(f"  -H = cube roots of -1")
    print(f"  Both follow from 37≡1(mod 3) = Eisenstein splitting N(7+3ω)=37")
    print(f"  χ₋₃ is the driving character. E8 contributes nothing here.")


if __name__ == "__main__":
    run()
