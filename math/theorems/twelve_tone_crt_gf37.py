# -*- coding: utf-8 -*-
"""
================================================================================
12-TONE / CRT MUSIC ALGEBRA TOWER — ℤ₁₂ × ℤ₃₇ ≅ ℤ₄₄₄
================================================================================

Author: Michael Warren Song (CyclicAmp)

CRT ISOMORPHISM [P]:
  gcd(12, 37) = 1  →  ℤ₁₂ × ℤ₃₇ ≅ ℤ₄₄₄  (Chinese Remainder Theorem)
  444 = 12 × 37

  CRT basis elements:
    e₁ = 37: satisfies e₁ ≡ 1 (mod 12), e₁ ≡ 0 (mod 37)
    e₂ = 408: satisfies e₂ ≡ 0 (mod 12), e₂ ≡ 1 (mod 37)
             (12⁻¹ mod 37 = 34; e₂ = 12 × 34 = 408)

  Map: (a, b) ∈ ℤ₁₂ × ℤ₃₇  ↦  (37a + 408b) mod 444

12-TONE PITCH CLASSES [P]:
  C=0, C#=1, D=2, D#=3, E=4, F=5, F#=6, G=7, G#=8, A=9, A#=10, B=11

GF(37) ORBITS → PITCH CLASSES [V]:
  IC = {1,10,26}    → {C#, D, A#}   (pitch classes {1,2,10})
  SEED = {18,24,32} → {C, F#, G#}   (pitch classes {0,6,8})
  SA = {4,9,25,30}  → {C#,E,F#,A}   (pitch classes {1,4,6,9})
  CASCADE={8,13,24} → {C, C#, G#}   (pitch classes {0,1,8})
  NEG_H={11,27,36}  → {C, D#, B}    (pitch classes {0,3,11})

KEY CONSTANTS [V]:
  4403 = 119 × 37:  mod 12 = 11 (note B), mod 37 = 0 (SEAM)
  1666:             mod 12 = 10 (note A#), mod 37 = 1 (IC)

  4403 and 1666 are adjacent semitones (B and A#/B♭).
  4403 is on the SEAM (multiple of 37); 1666 is in IC (mod 37 = 1).
  Their difference: 4403 - 1666 = 2737 = 74 × 37 - 1. 2737 mod 37 = 36 ∈ NEG_H.

SEED PITCH STRUCTURE:
  SEED = {18,24,32} → pitch classes {0,6,8} = {C, F#, G#}
  Intervals in ℤ₁₂: C→F# = 6 (tritone), F#→G# = 2 (major 2nd), G#→C = 4 (major 3rd)
  The tritone (6 semitones) is the unique self-inverse interval in ℤ₁₂.

IC PITCH STRUCTURE:
  IC = {1,10,26} → pitch classes {1,2,10} = {C#, D, A#}
  Intervals: C#→D = 1 (semitone), D→A# = 8 (minor 6th), A#→C# = 3 (minor 3rd)
================================================================================
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from math import gcd

P = 37
N = 12
M = P * N  # 444

IC      = {1, 10, 26}
SEED    = {18, 24, 32}
SA      = {4, 9, 25, 30}
CASCADE = {8, 13, 24}
NEG_H   = {11, 27, 36}

NOTES = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']


def run():
    print("=" * 70)
    print("12-TONE / CRT MUSIC ALGEBRA TOWER — Z12 x Z37 ≅ Z444")
    print("=" * 70)

    # CRT isomorphism
    assert gcd(N, P) == 1
    print(f"\ngcd(12, 37) = {gcd(N,P)} — CRT applies  check")
    print(f"Z_12 x Z_37 ≅ Z_{M}")

    e1 = P  # 37
    assert e1 % N == 1 and e1 % P == 0
    print(f"e1 = {e1}: ≡1 mod 12, ≡0 mod 37  check")

    inv12 = pow(N, -1, P)  # 12^{-1} mod 37
    e2 = (N * inv12) % M   # 408
    assert e2 % N == 0 and e2 % P == 1
    print(f"e2 = {e2}: ≡0 mod 12, ≡1 mod 37  check")

    # Verify CRT map
    for a in range(N):
        for b in range(P):
            x = (a * e1 + b * e2) % M
            assert x % N == a and x % P == b
    print(f"CRT map verified for all (a,b) in Z_12 x Z_37  check")

    # GF(37) orbits → pitch classes
    print(f"\nGF(37) orbits → 12-tone pitch classes:")
    for label, orbit in [('IC', IC), ('SEED', SEED), ('SA', SA),
                          ('CASCADE', CASCADE), ('NEG_H', NEG_H)]:
        pcs = sorted({x % N for x in orbit})
        names = [NOTES[pc] for pc in pcs]
        print(f"  {label:10s} = {sorted(orbit)} → {pcs} = {names}")

    # Key constants
    print(f"\nKey constants:")
    for n, label in [(4403, '4403'), (1666, '1666')]:
        a = n % N
        b = n % P
        cat = 'SEAM' if b == 0 else ('IC' if b in IC else ('SEED' if b in SEED else ('SA' if b in SA else str(b))))
        print(f"  {label}: mod 12 = {a} ({NOTES[a]}), mod 37 = {b} ({cat})")
    diff = 4403 - 1666
    print(f"  4403 - 1666 = {diff}, mod 37 = {diff % P} ∈ NEG_H: {diff % P in NEG_H}")
    assert 4403 % P == 0
    assert 1666 % P == 1 and 1666 % P in IC
    print(f"  4403 = {4403//P} × 37 (SEAM)  check")
    print(f"  1666 ≡ 1 mod 37 (IC)  check")

    # SEED pitch structure
    print(f"\nSEED pitch intervals (C=0, F#=6, G#=8):")
    seed_pcs = sorted({x % N for x in SEED})
    for i in range(len(seed_pcs)):
        a = seed_pcs[i]
        b = seed_pcs[(i+1) % len(seed_pcs)]
        interval = (b - a) % N
        print(f"  {NOTES[a]} → {NOTES[b]}: {interval} semitones")

    print(f"\nAll verifications passed.")


if __name__ == "__main__":
    run()
