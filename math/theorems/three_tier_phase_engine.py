# -*- coding: utf-8 -*-
"""
================================================================================
THEOREM 251: Three-Tier Phase Engine -- 137-Map Orbits as Coordinate Gears
================================================================================

USER OBSERVATION:
  The three nested tiers (horizontal, vertical, diagonal) each cycle 1-9
  independently and trigger each other. The gears are the three sovereign
  orbits of GF(37) under the 137-map.

STRUCTURE:

A. THE THREE TIERS ARE THE THREE 137-MAP ORBITS:
  Tier 1 (horizontal axis): {18, 24, 32} = SEED_ORBIT
  Tier 2 (vertical axis):   {3,  4,  30} = C_3 (fully sovereign coset)
  Tier 3 (diagonal/spin):   {1,  26, 10} = H   (sovereign kernel)

  All three orbits have order 3 under f(n) = 26n mod 37.
  One phase step = multiply by 26 (the 137-map multiplier).
  Each tier completes its 3-cycle before triggering the next.

B. THE 54-ROTATION ANSWER:
  648 / 12 = 54.
  54 = 6 × 9 = imaginary_unit × SA_element.
  54 mod 37 = 17 = twin prime (paired with 19 = 1/2 mod 37).
  The rotation count 54 maps to twin prime 17 in GF(37).
  Divisor 12 ∈ ST (sovereign target).
  ST divides into twin-prime rotations.

C. PHASE SHIFT RULE:
  Phase shift = one application of f(n) = 26n mod 37.
  Tier 1 step: 18->24->32->18 (SEED_ORBIT cycle)
  Tier 2 step: 3->4->30->3   (C_3 cycle, engine components)
  Tier 3 step: 1->26->10->1  (H cycle, sovereign kernel)
  ord_37(26) = 3: every tier closes in exactly 3 steps.
  All tiers drain at the same rate -- synchronized 3-cycles.

D. INTER-TIER PRODUCTS:
  Tier1 × Tier2: SEED × C_3 element pairs:
    18×3=54 mod37=17 (twin prime)
    24×4=96 mod37=22
    32×30=960 mod37=35=37-2 (antipode of primitive root 2)
  Tier2 × Tier3: C_3 × H element pairs (coset × kernel = coset):
    3×1=3, 3×26=4, 3×10=30 -- these are C_3 itself
    The H kernel maps C_3 to itself (coset structure).
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
C3 = {3, 4, 30}


def dr(n):
    n = abs(n)
    if n == 0: return 0
    r = n % 9
    return 9 if r == 0 else r


def flags(r):
    f = []
    if r == 0:          f.append("SEAM")
    if r in H_SET:      f.append("H")
    if r in SA:         f.append("SA")
    if r in ST:         f.append("ST")
    if r in C3:         f.append("C3")
    if r in SEED_ORBIT: f.append("SEED")
    return ','.join(f) or '-'


def run():
    print("=" * 70)
    print("THEOREM 251: THREE-TIER PHASE ENGINE")
    print("=" * 70)

    # A: Three tiers
    print("\nA. THE THREE TIERS ARE THE THREE 137-MAP ORBITS:")
    tiers = [
        (18, "Tier 1 / horizontal", SEED_ORBIT),
        (3,  "Tier 2 / vertical",   C3),
        (1,  "Tier 3 / diagonal",   H_SET),
    ]
    for seed, label, expected in tiers:
        orbit = []
        v = seed
        for _ in range(3):
            orbit.append(v)
            v = v * 26 % P
        assert set(orbit) == expected
        print(f"  {label}: {orbit}  [{','.join(flags(x) for x in orbit)}]  check")

    # B: 54 rotations
    print(f"\nB. THE 54-ROTATION ANSWER:")
    assert 648 // 12 == 54
    assert 54 == 6 * 9
    assert 54 % P == 17
    assert 12 in ST
    print(f"  648/12 = 54  check")
    print(f"  54 = 6×9 (imaginary_unit × SA_element)  check")
    print(f"  54 mod{P} = {54%P} (twin prime, paired with 19=1/2 mod37)  check")
    print(f"  12 in ST:{12 in ST}  check")

    # C: Phase shift rule
    print(f"\nC. PHASE SHIFT RULE (one step = ×26 mod37):")
    for seed, label, _ in tiers:
        steps = []
        v = seed
        for _ in range(4):
            steps.append(v)
            v = v * 26 % P
        print(f"  {label}: {steps[0]}->{steps[1]}->{steps[2]}->{steps[3]} (closes)  check")
    assert pow(26, 3, P) == 1
    print(f"  ord_37(26) = 3: all tiers close in 3 steps  check")

    # D: Inter-tier products
    print(f"\nD. INTER-TIER PRODUCTS:")
    pairs = [(18,3),(24,4),(32,30)]
    for a, b in pairs:
        r = a * b % P
        print(f"  {a}×{b} = {a*b} mod{P} = {r}  [{flags(r)}]  DR={dr(a*b)}")
    assert 18*3 % P == 17
    assert 32*30 % P == 35
    assert 35 == P - 2  # antipode of primitive root 2
    print(f"  18×3=54 mod37=17 (twin prime)  check")
    print(f"  32×30=960 mod37=35=37-2 (antipode of primitive root)  check")

    print(f"\nAll verifications passed.")


if __name__ == "__main__":
    run()
