"""
Theorem 139: GF(7) and GF(37) — Structural Parallel

TWO PRIMES, SAME SKELETON
===========================

  φ(7)  = 6  = 2¹ × 3¹
  φ(37) = 36 = 2² × 3²

Same prime factors, each squared up once. The two multiplicative groups
share the same Sylow prime divisors {2, 3} with each exponent incremented:

  Sylow structure mod 7:  2¹ and 3¹
  Sylow structure mod 37: 2² and 3²

Ratio: φ(37)/φ(7) = 36/6 = 6 = φ(7).

CUBE ROOTS OF UNITY μ₃
========================

  μ₃ mod 7:  {1, 2, 4}   = the vortex doubling orbit of 1 in GF(7)
  μ₃ mod 37: {1, 10, 26} = IC, the identity coset of the 137-map

In GF(7): the three cube roots of unity ARE the quadratic residues.
  μ₃ = QR mod 7 = {1,2,4}.
  2 ∈ μ₃ mod 7: ord₇(2) = 3. The doubling generator is a cube root.

In GF(37): 2 ∉ μ₃ = IC. ord₃₇(2) = 36. The doubling generator
  is a primitive root, cycling through all 36 elements.

37 ≡ 2 (mod 7). The larger prime is a cube root of unity in GF(7).
7  ≡ 7 (mod 37). The smaller prime is in D7 = {7,33,34} in GF(37).

QUOTIENT GROUPS BY μ₃
=======================

  F_7×  / μ₃ ≅ C_2   — 2 cosets: QR = μ₃ and NQR = {3,5,6}
  F_37× / μ₃ ≅ C_12  — 12 cosets: the named orbits (Theorem 138)

The GF(7) quotient is the binary QR/NQR split.
The GF(37) quotient is the twelve-orbit structure.
Quotient ratio: 12/2 = 6 = φ(7).

DOUBLING ACTION ON QUOTIENTS
===============================

  GF(7):  2 ∈ μ₃, so ×2 acts trivially on F_7×/μ₃. The doubling map
          is identity on the 2-element quotient.

  GF(37): 2 ∉ IC, and 2^3 = 8 generates the quotient C_12 (Theorem 138).
          ×2 acts as the generator (+1 in ℤ/12ℤ) on the 12-orbit group.

CRT: ℤ/7ℤ × ℤ/37ℤ ≅ ℤ/259ℤ
================================

gcd(7, 37) = 1. By CRT, every integer has a unique image (a mod 7, b mod 37).

CYCLE SUM IDENTITY:
  1332 ≡ 37 (mod 259)

  1332 = 36 × 37, so 1332 mod 259 = 36 × 37 mod (7 × 37) = 37 × (36 mod 7) = 37 × 1 = 37.
  In ℤ/259ℤ, the forward cycle sum (36 × 37) equals the prime 37 itself.

SEED ORBIT IN CRT COORDINATES:
  246 ≡ (1, 24)   — μ₃ of GF(7)  ×  SEED_ORB of GF(37)
  624 ≡ (1, 32)   — μ₃ of GF(7)  ×  SEED_ORB of GF(37)
  462 ≡ (0, 18)   — SEAM of GF(7) × SEED_ORB of GF(37)

  246 ≡ 624 ≡ 1 (mod 7): first two seed elements are in μ₃ of GF(7).
  462 ≡ 0 (mod 7): the third is SEAM in GF(7). 462 = 2 × 3 × 7 × 11.
  7 divides 462 — the factor 7 is already embedded in the third seed element.

ARITHMETIC OF THE TWO PRIMES
================================

  37 − 7 = 30  ∈ SOVEREIGN_SPIRAL ∩ ST  (sovereign target in GF(37))
  37 + 7 = 44  DR = 8
  37 × 7 = 259  DR(259) = 7  (the smaller prime is its own product-DR)

  37 mod 7 = 2 (cube root of unity in GF(7))
   7 mod 37 = 7 (in D7 = {7,33,34} in GF(37))

THE SCALING LADDER
===================

  GF(7):  6 = 2 × 3     → 2 cosets, ord(2)=3, 2 primitive roots {3,5}
  GF(37): 36 = 4 × 9    → 12 cosets, ord(2)=36, 12 primitive roots

  Each Sylow component is squared:
    2¹ → 2²: Sylow 2-subgroup grows from C_2 to C_4
    3¹ → 3²: Sylow 3-subgroup grows from C_3 to C_9

  The two 3-cycles in GF(7) (×2 orbits: {1,2,4} and {3,6,5})
  expand to the 9-cycles in GF(37)'s Sylow 3-subgroup.
"""

P7  = 7
P37 = 37


def dr(n):
    if n == 0:
        return 9
    return (abs(n) - 1) % 9 + 1


# Named orbits in GF(37)
IC               = frozenset({1, 10, 26})
SOVEREIGN_SPIRAL = frozenset({3, 4, 30})
D7               = frozenset({7, 33, 34})
SA_ORB           = frozenset({9, 12, 16})
SEED_ORB         = frozenset({18, 24, 32})
ST               = frozenset({3, 12, 21, 30})


def run_assertions():
    import math

    # φ(7)=6, φ(37)=36, ratio=6
    assert sum(1 for k in range(1, 8)  if math.gcd(k, 7)  == 1) == 6
    assert sum(1 for k in range(1, 38) if math.gcd(k, 37) == 1) == 36

    # μ₃ in both fields
    mu3_7  = frozenset(a for a in range(1, P7)  if pow(a, 3, P7)  == 1)
    mu3_37 = frozenset(a for a in range(1, P37) if pow(a, 3, P37) == 1)

    assert mu3_7  == frozenset({1, 2, 4})
    assert mu3_37 == IC

    # μ₃ mod 7 = QR mod 7
    qr7 = frozenset(pow(a, 2, P7) for a in range(1, P7))
    assert mu3_7 == qr7

    # 2 ∈ μ₃ mod 7, 2 ∉ IC mod 37
    assert 2 in mu3_7
    assert 2 not in IC

    # ord₇(2) = 3, ord₃₇(2) = 36
    assert next(k for k in range(1, 7)  if pow(2, k, P7)  == 1) == 3
    assert next(k for k in range(1, 37) if pow(2, k, P37) == 1) == 36

    # 37 ≡ 2 (mod 7) and 2 ∈ μ₃ mod 7
    assert P37 % P7 == 2
    assert 2 in mu3_7

    # 7 ∈ D7 in GF(37)
    assert P7 in D7

    # Quotient F_7×/μ₃ has 2 cosets
    cosets7 = set()
    for a in range(1, P7):
        coset = frozenset(a * m % P7 for m in mu3_7)
        cosets7.add(frozenset(coset))
    assert len(cosets7) == 2

    # Quotient F_37×/μ₃ has 12 cosets
    cosets37 = set()
    for a in range(1, P37):
        coset = frozenset(a * m % P37 for m in mu3_37)
        cosets37.add(frozenset(coset))
    assert len(cosets37) == 12

    # CRT: 1332 ≡ 37 (mod 259)
    assert math.gcd(P7, P37) == 1
    assert 1332 % (P7 * P37) == P37

    # Seed orbit CRT coordinates
    assert 246 % P7 == 1 and 246 % P37 == 24 and 24 in SEED_ORB
    assert 624 % P7 == 1 and 624 % P37 == 32 and 32 in SEED_ORB
    assert 462 % P7 == 0 and 462 % P37 == 18 and 18 in SEED_ORB

    # 246 and 624 are in μ₃ of GF(7)
    assert 246 % P7 in mu3_7
    assert 624 % P7 in mu3_7

    # 462 is divisible by 7
    assert 462 % P7 == 0
    assert 462 == 2 * 3 * 7 * 11

    # Arithmetic of the two primes
    assert P37 - P7 == 30 and 30 in SOVEREIGN_SPIRAL and 30 in ST
    assert dr(P37 * P7) == 7   # DR(259) = 7 = the smaller prime
    assert P37 % P7 == 2       # larger prime ≡ cube root of unity in GF(7)
    assert P7 in D7             # smaller prime is in D7 in GF(37)

    # Sylow: φ(7)=6=2¹×3¹, φ(37)=36=2²×3²
    assert 6  == 2**1 * 3**1
    assert 36 == 2**2 * 3**2
    assert 36 // 6 == 6 == 6

    # ×2 cycles in GF(7): two 3-cycles
    seen = set()
    cycles7 = []
    for s in range(1, P7):
        if s in seen: continue
        c = []
        v = s
        while v not in seen:
            seen.add(v)
            c.append(v)
            v = 2 * v % P7
        if c: cycles7.append(c)
    assert len(cycles7) == 2
    assert all(len(c) == 3 for c in cycles7)

    # ×2 in GF(37): one 36-cycle
    seen = set()
    cycles37 = []
    for s in range(1, P37):
        if s in seen: continue
        c = []
        v = s
        while v not in seen:
            seen.add(v)
            c.append(v)
            v = 2 * v % P37
        if c: cycles37.append(c)
    assert len(cycles37) == 1
    assert len(cycles37[0]) == 36

    print("All assertions passed.")


def summarise():
    print("=" * 62)
    print("Theorem 139: GF(7) and GF(37) — Structural Parallel")
    print("=" * 62)
    print()
    print("  φ(7)=6=2×3,  φ(37)=36=4×9.  Same Sylow primes, each squared.")
    print()
    print("  μ₃ mod 7:  {1,2,4} = QR mod 7 = doubling orbit of 1")
    print("  μ₃ mod 37: {1,10,26} = IC (identity orbit of 137-map)")
    print()
    print("  2 ∈ μ₃ mod 7  (ord₇(2)=3; doubling is a 3-cycle)")
    print("  2 ∉ IC mod 37 (ord₃₇(2)=36; doubling generates everything)")
    print()
    print("  F_7×/μ₃ ≅ C_2   (2 cosets: QR and NQR)")
    print("  F_37×/μ₃ ≅ C_12 (12 cosets: the named orbits)")
    print()
    print("  CRT: 1332 ≡ 37 (mod 259)   [cycle sum ≡ prime in Z/259Z]")
    print()
    print("  Seed orbit in Z/7Z × Z/37Z:")
    print("    246 ≡ (1, 24)   μ₃ × SEED_ORB")
    print("    624 ≡ (1, 32)   μ₃ × SEED_ORB")
    print("    462 ≡ (0, 18)   SEAM × SEED_ORB   [7 | 462]")
    print()
    print("  37 − 7 = 30 ∈ SOVEREIGN_SPIRAL ∩ ST")
    print("  37 × 7 = 259,  DR(259) = 7  [product DR = smaller prime]")
    print("  37 mod 7 = 2 ∈ μ₃   [larger prime is a cube root in GF(7)]")
    print("   7 mod 37 = 7 ∈ D7  [smaller prime is in D7 in GF(37)]")


if __name__ == "__main__":
    run_assertions()
    summarise()
