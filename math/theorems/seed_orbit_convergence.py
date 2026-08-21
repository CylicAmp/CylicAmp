# -*- coding: utf-8 -*-
"""
================================================================================
THEOREM 250: Seed Orbit Convergence -- {18,24,32} Collects Across Domains
================================================================================

USER OBSERVATION:
  The SEED_ORBIT = {18, 24, 32} (137-map orbit of seed 246) is not local
  to the pipeline. It pulls in values from physics, astronomy, biology,
  and chronology -- all collapsing to the same three positions mod 37.

STRUCTURE:

A. THE SEED_ORBIT DEFINED:
  SEED_ORBIT = {18, 24, 32} = {26×32 mod37, 26×18 mod37, 26×24 mod37}.
  Orbit of seed 246 under f(n)=26n mod37:
    246 mod37=24 -> 26×24=624 mod37=32 -> 26×32=832 mod37=18 -> 26×18=468 mod37=24.
  The reference seed 246 is in its own orbit.

B. CONVERGENTS INTO SEED_ORBIT (mod 37):
  18 slot:
    18 itself         DR=9 in SA
    499 (solar transit, seconds)  DR=4 in SA, prime
    1979 (calendar anchor)        DR=8
    55 (cumul. orbitals n=1..5, T241)  DR=1 in H
  24 slot:
    24 itself         DR=6 (imaginary unit)
    246 (pipeline seed)           DR=3 in ST
    95040 (M12 group order, T243) DR=9 in SA
  32 slot:
    32 itself         DR=5 (prime seed)
    c mod37=32 (speed of light, T248)  DR=1 in H

C. LINKS BETWEEN 499 AND 1979:
  Both land at SEED_ORBIT position 18.
  1979 - 499 = 1480.  1480 mod37 = 0 (SEAM).
  1979 / 499 mod37 = 1 in H (identity).
  The difference is a SEAM; the ratio is the identity.
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


def flags(r):
    f = []
    if r == 0:          f.append("SEAM")
    if r in H_SET:      f.append("H")
    if r in SA:         f.append("SA")
    if r in ST:         f.append("ST")
    if r in SEED_ORBIT: f.append("SEED")
    return ','.join(f) or '-'


def run():
    print("=" * 70)
    print("THEOREM 250: SEED ORBIT CONVERGENCE")
    print("=" * 70)

    # A: Orbit definition
    print("\nA. SEED_ORBIT UNDER 137-MAP:")
    v = 246 % P
    orbit = []
    for _ in range(3):
        orbit.append(v)
        v = v * 26 % P
    assert set(orbit) == SEED_ORBIT
    print(f"  246 mod{P}={246%P}  orbit: {orbit} = SEED_ORBIT  check")

    # B: Convergents
    print(f"\nB. CONVERGENTS INTO SEED_ORBIT:")
    convergents = [
        (18,    "18 itself"),
        (499,   "solar transit (seconds)"),
        (1979,  "calendar anchor"),
        (55,    "cumul. orbitals n=1..5 (T241)"),
        (24,    "24 itself"),
        (246,   "pipeline seed"),
        (95040, "M12 group order (T243)"),
        (32,    "32 itself"),
        (299792458, "speed of light c"),
    ]
    for n, label in convergents:
        r = n % P
        assert r in SEED_ORBIT, f"{n} mod37={r} not in SEED_ORBIT"
        print(f"  {n} ({label}): mod{P}={r}  [{flags(r)}]  DR={dr(n)}")

    # C: 499 and 1979 link
    print(f"\nC. LINKS BETWEEN 499 AND 1979:")
    assert 499 % P == 1979 % P == 18
    diff = (1979 - 499) % P
    ratio = 1979 * pow(499, -1, P) % P
    assert diff == 0 and ratio == 1
    print(f"  499 mod{P} = {499%P}  1979 mod{P} = {1979%P}  same slot: True  check")
    print(f"  1979-499 = 1480  mod{P} = {diff}  [{flags(diff)}]  check")
    print(f"  1979/499 mod{P} = {ratio}  [{flags(ratio)}]  (identity)  check")

    print(f"\nAll verifications passed.")


if __name__ == "__main__":
    run()
