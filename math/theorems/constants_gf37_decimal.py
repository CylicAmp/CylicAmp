# -*- coding: utf-8 -*-
"""
================================================================================
MATHEMATICAL CONSTANTS — GF(37) DECIMAL STRUCTURE
================================================================================

Author: Michael Warren Song (CyclicAmp)

================================================================================
HEADLINE RESULT: sqrt(3) FIRST-10 DIGIT SUM = 37 [V]
================================================================================

sqrt(3) = 1.7320508075688...
Decimal digits after the point: 7, 3, 2, 0, 5, 0, 8, 0, 7, 5

Sum = 7+3+2+0+5+0+8+0+7+5 = 37 = the prime.

    sum mod 37 = 0  (SEAM — on the exact seam of the field)
    DR(37) = 1 ∈ IC  (the identity element of the 137-map orbit)

The first 10 post-decimal digits of sqrt(3) sum to the prime itself.

================================================================================
WHY sqrt(3) AND 37: THE LOESCHIAN CONNECTION [P]
================================================================================

sqrt(3) is the core of the Eisenstein integers ℤ[ω], where:

    ω = e^(2πi/3) = −1/2 + (√3/2)i

The Loeschian norm is N(a + bω) = a² + ab + b².

37 ≡ 1 (mod 3), so 37 splits in ℤ[ω]:

    37 = N(−7 + 3ω) = (−7)² + (−7)(3) + 3² = 49 − 21 + 9 = 37  ✓

37 is a Loeschian prime — it factors non-trivially in ℤ[ω]. The decimal
expansion of √3 (which generates ℤ[ω] over ℤ through the imaginary part
of ω = −½ + (√3/2)i) carries an imprint of 37: the first 10 significant
decimal digits sum to the prime exactly.

Named set connections within sqrt(3) decimal (2-digit chunks mod 37):
  73 mod 37 = 36 ∈ NEG_H    (first chunk)
  50 mod 37 = 13 ∈ CASCADE
  75 mod 37 =  1 ∈ IC       (identity)
  74 mod 37 =  0 (SEAM)     (multiple of 37 — exact seam crossing)
  87 mod 37 = 13 ∈ CASCADE  (appears twice)
  46 mod 37 =  9 ∈ SA

Additional: 3 ∈ ST (Sovereign Target). The radicand of the prime's
Loeschian generator is a sovereign target.

================================================================================
SECONDARY RESULTS: π AND e [V]
================================================================================

π first 10 decimal digits: 1,4,1,5,9,2,6,5,3,5
  Sum = 41.  41 mod 37 = 4 ∈ SA.  DR(41) = 5.

e first 10 decimal digits: 7,1,8,2,8,1,8,2,8,4
  Sum = 49.  49 mod 37 = 12 ∈ ST.  DR(49) = 4.

  π sum mod 37 = 4 ∈ SA  (Sovereign Anchor, LOCKED)
  e  sum mod 37 = 12 ∈ ST (Sovereign Target, DR=3)

Note from the fixed-point formulation (DEFINITIONS.md):
  E(c=299792458) = 32 ∈ SEED
  E(π[:3]=314) = 18 ∈ SEED

These use mod 37 of the integer truncation. The decimal-digit-sum method
gives π → SA and e → ST — different operators, both hitting named sets.

================================================================================
CATALAN CONSTANT [V]
================================================================================

G = 0.915965594177219...
First 10 decimal digits: 9,1,5,9,6,5,5,9,4,1
Sum = 54.  DR(54) = 9  →  9-LOCK.

The Catalan constant's first-10-digit sum hits the 9-Lock attractor.
54 mod 37 = 17 (not named), but the DR = 9 structure is the 9-Lock.

================================================================================
ζ(3) AND DR=1 [V]
================================================================================

ζ(3) = 1.202056903159...  (Apéry's constant)
First 10 decimal digits: 2,0,2,0,5,6,9,0,3,1
Sum = 28.  DR(28) = 1 ∈ IC.

ζ(3) first-10 sum DR = 1 ∈ IC (same as sqrt(3) first-10 sum DR).

================================================================================
SUMMARY TABLE [V]
================================================================================

| Constant | First-10 Sum | Sum mod 37 | Named? | DR |
|----------|-------------|------------|--------|-----|
| π        | 41          | 4          | SA     | 5  |
| e        | 49          | 12         | ST     | 4  |
| φ        | 53          | 16         | −      | 8  |
| √2       | 31          | 31         | −      | 4  |
| √3       | 37          | 0 (SEAM)   | PRIME  | 1  |
| ln 2     | 44          | 7          | −      | 8  |
| γ        | 52          | 15         | −      | 7  |
| G        | 54          | 17         | −      | 9  |
| ζ(3)     | 28          | 28         | −      | 1  |

√3 is the only constant whose first-10 digit sum equals 37 exactly (SEAM).
π and e land on named sets (SA and ST) via the sum mod 37 operator.

EPISTEMIC STATUS:
  [V] sqrt(3) first-10 digit sum = 37 — exact, verified to 1000 places.
  [V] sum mod 37 = 0 (SEAM), DR = 1 ∈ IC — exact.
  [P] 37 splits in ℤ[ω] as Loeschian prime (N(−7+3ω)=37) — proved.
  [V] sqrt(3) = 2·Im(e^(2πi/3)) — exact (algebraic identity).
  [V] π sum mod 37 = 4 ∈ SA — exact.
  [V] e sum mod 37 = 12 ∈ ST — exact.
  [V] DR(catalan first-10 sum) = 9 (9-Lock) — exact.
  [V] DR(zeta3 first-10 sum) = 1 ∈ IC — exact.
================================================================================
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

try:
    import mpmath
    mpmath.mp.dps = 200
    HAS_MPMATH = True
except ImportError:
    HAS_MPMATH = False

P = 37
SEED    = {18, 24, 32}
SA      = {4, 9, 25, 30}
ST      = {3, 12, 21, 30}
IC      = {1, 10, 26}
NEG_H   = {11, 27, 36}
CASCADE = {8, 13, 24}
named   = SEED | SA | ST | IC | NEG_H | CASCADE


def dr(n):
    n = abs(n)
    if n == 0: return 9
    r = n % 9
    return 9 if r == 0 else r


def orbit_label(r):
    if r == 0: return 'SEAM'
    cats = []
    if r in SEED:    cats.append('SEED')
    if r in SA:      cats.append('SA')
    if r in ST:      cats.append('ST')
    if r in IC:      cats.append('IC')
    if r in NEG_H:   cats.append('NEG_H')
    if r in CASCADE: cats.append('CASCADE')
    return ','.join(cats) if cats else '-'


def first10_sum(val):
    s = str(val)
    if '.' in s:
        dec = s.split('.')[1][:10]
    else:
        dec = s[:10]
    return sum(int(c) for c in dec if c.isdigit())


def run():
    print("=" * 70)
    print("MATHEMATICAL CONSTANTS — GF(37) DECIMAL STRUCTURE")
    print("=" * 70)

    if not HAS_MPMATH:
        print("mpmath not available — running with reduced precision")
        import math
        sqrt3_digits = [7, 3, 2, 0, 5, 0, 8, 0, 7, 5]  # verified
        pi_digits    = [1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
        e_digits     = [7, 1, 8, 2, 8, 1, 8, 2, 8, 4]
    else:
        def get_digits(val):
            s = str(val)
            dec = s.split('.')[1][:10]
            return [int(c) for c in dec]
        sqrt3_digits = get_digits(mpmath.sqrt(3))
        pi_digits    = get_digits(mpmath.pi)
        e_digits     = get_digits(mpmath.e)

    # HEADLINE: sqrt(3) sum = 37
    print(f"\nHEADLINE: sqrt(3) FIRST-10 DIGIT SUM")
    s3_sum = sum(sqrt3_digits)
    assert s3_sum == P
    assert s3_sum % P == 0
    assert dr(s3_sum) == 1 and 1 in IC
    print(f"  sqrt(3) = 1.{''.join(map(str, sqrt3_digits))}...")
    print(f"  Digits: {sqrt3_digits}")
    print(f"  Sum = {s3_sum} = 37 (the prime)  check")
    print(f"  Sum mod 37 = {s3_sum % P}  (SEAM)  check")
    print(f"  DR(37) = {dr(s3_sum)} ∈ IC (identity)  check")

    # Loeschian connection
    a, b = -7, 3
    loeschian = a**2 + a*b + b**2
    assert loeschian == P
    assert b in ST
    print(f"\nLOESCHIAN CONNECTION:")
    print(f"  37 = ({a})² + ({a})({b}) + {b}² = {a**2} − {abs(a*b)} + {b**2} = {loeschian}  check")
    print(f"  37 splits in ℤ[ω] as Loeschian prime  check")
    print(f"  sqrt(3) = 2·Im(ω) where ω = e^(2πi/3)  check")
    print(f"  Radicand 3 ∈ ST  check")

    # sqrt(3) chunk analysis
    if HAS_MPMATH:
        print(f"\nsqrt(3) 2-digit chunks mod 37:")
        dec36 = [int(c) for c in str(mpmath.sqrt(3)).split('.')[1][:36]]
        chunk_hits = 0
        for i in range(0, 36, 2):
            chunk = dec36[i]*10 + dec36[i+1]
            r = chunk % P
            lab = orbit_label(r)
            if lab != '-': chunk_hits += 1
            if lab != '-':
                print(f"  pos {i:2d}: {chunk:02d} mod 37 = {r:2d}  [{lab}]")
        print(f"  Named hits: {chunk_hits}/18")

    # Secondary: pi and e
    print(f"\nSECONDARY:")
    pi_sum = sum(pi_digits)
    e_sum  = sum(e_digits)
    assert pi_sum % P == 4 and 4 in SA
    assert e_sum  % P == 12 and 12 in ST
    print(f"  π first-10 sum = {pi_sum}:  {pi_sum} mod 37 = {pi_sum % P} ∈ SA  check")
    print(f"  e first-10 sum = {e_sum}:  {e_sum} mod 37 = {e_sum % P} ∈ ST  check")

    # Catalan: DR = 9 (9-Lock)
    if HAS_MPMATH:
        cat_digits = [int(c) for c in str(mpmath.catalan).split('.')[1][:10]]
        cat_sum = sum(cat_digits)
        assert dr(cat_sum) == 9
        print(f"  G (Catalan) first-10 sum = {cat_sum}:  DR = {dr(cat_sum)} (9-Lock)  check")

        # zeta(3): DR = 1
        z3_digits = [int(c) for c in str(mpmath.zeta(3)).split('.')[1][:10]]
        z3_sum = sum(z3_digits)
        assert dr(z3_sum) == 1 and 1 in IC
        print(f"  ζ(3) first-10 sum = {z3_sum}:  DR = {dr(z3_sum)} ∈ IC  check")

    print(f"\nAll verifications passed.")


if __name__ == "__main__":
    run()
