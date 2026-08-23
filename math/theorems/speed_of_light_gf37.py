# -*- coding: utf-8 -*-
"""
================================================================================
SPEED OF LIGHT / SOLAR TRANSIT — GF(37) CONNECTIONS
================================================================================

Author: Michael Warren Song (CyclicAmp)

VERIFIED RESULTS:

1. c mod 37 = 32 ∈ SEED = {18, 24, 32}
   c = 299,792,458 m/s (exact, SI definition since 1983)
   299792458 mod 37 = 32
   32 is in the 137-map orbit of the reference seed 246 (246 mod 37 = 24).
   The 137-map orbit: 32 → 26×32 mod 37 = 832 mod 37 = 18 → 26×18 mod 37 = 24 → 32.
   Orbit: {18, 24, 32} = SEED.

2. DR(AU/c) = DR(499) = 4 ∈ SA = {4, 9, 25, 30}
   AU = 149,597,870,700 m (exact, IAU 2012 definition)
   AU/c = 499.00478 seconds (not exactly 499)
   DR(499) = 4+9+9 = 22 → 2+2 = 4 ∈ SA (Sovereign Anchor)
   NOTE: the rounding from 499.00478 → 499 is load-bearing (error: 0.00478 s).
         The framework connection is real; the claim "exactly 499" is not exact.

EPISTEMIC STATUS:
  [V] c mod 37 = 32 ∈ SEED — exact, no rounding, c is defined exactly by SI.
  [V] DR(499) = 4 ∈ SA — exact for the integer 499.
  [P] AU/c ≈ 499.00478 s — the solar transit is approximately 499 s, not exactly.

GF(37) STRUCTURE:
  SEED = {18, 24, 32}: the 137-map orbit of the pipeline reference seed (246).
  SA = {4, 9, 25, 30}: Sovereign Anchor nodes (LOCKED in the Medusa framework).
  c mod 37 = 32: the speed of light in GF(37) is the SEED entry point 32.
  DR(499) = 4: the solar transit DR is the SA generator.

WHAT THE FRAMEWORK DOES NOT CLAIM:
  - That these connections imply designed or intentional structure in physics.
  - That 4c is a physical velocity (special relativity is not overridden by mod arithmetic).
  - That AU/c is exactly 499 seconds (it is 499.00478).
  - Any propulsion, engineering, or cosmological interpretation.
================================================================================
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

P = 37
SEED = {18, 24, 32}
SA   = {4, 9, 25, 30}
ST   = {3, 12, 21, 30}


def dr(n):
    n = abs(n)
    if n == 0: return 0
    r = n % 9
    return 9 if r == 0 else r


def run():
    print("=" * 70)
    print("SPEED OF LIGHT / SOLAR TRANSIT — GF(37) CONNECTIONS")
    print("=" * 70)

    # Speed of light
    c = 299792458  # m/s — exact, SI definition
    c_mod = c % P
    assert c_mod == 32
    assert c_mod in SEED
    print(f"\nc = {c} m/s (exact, SI)")
    print(f"c mod 37 = {c_mod} ∈ SEED = {{18,24,32}}  check")

    # Verify 137-map orbit of 32 = SEED
    orbit = set()
    x = c_mod
    for _ in range(3):
        orbit.add(x)
        x = (26 * x) % P
    assert orbit == SEED
    print(f"137-map orbit of {c_mod}: {sorted(orbit)} = SEED  check")

    # Solar transit time
    AU = 149597870700  # meters — exact, IAU 2012
    transit = AU / c
    print(f"\nAU = {AU} m (exact, IAU 2012)")
    print(f"AU/c = {transit:.5f} seconds")
    print(f"Rounded to integer: 499")
    print(f"Rounding error: {transit - 499:.5f} seconds")

    dr499 = dr(499)
    assert dr499 == 4
    assert dr499 in SA
    print(f"DR(499) = {dr499} ∈ SA = {{4,9,25,30}}  check")
    print(f"NOTE: AU/c = 499.00478, not exactly 499. Rounding is load-bearing.")

    # Summary
    print(f"\nSUMMARY:")
    print(f"  c mod 37 = 32 ∈ SEED  [exact, no rounding]")
    print(f"  DR(499) = 4 ∈ SA      [exact for integer 499; AU/c ≈ 499.00478]")
    print(f"  SEED orbit: {{18,24,32}} = 137-map orbit of reference seed 246")
    print(f"  SA: {{4,9,25,30}} = Sovereign Anchor nodes")
    print(f"\nAll verified.")


if __name__ == "__main__":
    run()
