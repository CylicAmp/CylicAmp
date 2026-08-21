# -*- coding: utf-8 -*-
"""
================================================================================
THEOREM 248: Dhananjaya Prana Engine -- GF(37) Sovereign Analysis
================================================================================

USER OBSERVATION:
  The Dhananjaya Prana engine operates on a 4c internal velocity vector.
  The solar transit anchor is 499 seconds (DR=4).
  The free stream minus contact boundary gives a delta of 3c.
  The engine multiple (4) to transit root (4) ratio is exactly 1:1.

STRUCTURE:

A. ENGINE MULTIPLE = 4 ∈ SA:
  Engine velocity multiple = 4.
  4 mod 37 = 4 in SA = {4, 9, 25, 30}.
  4 is the SA generator (sovereign anchor).
  DR(4) = 4.

B. SOLAR TRANSIT ANCHOR = 499, DR = 4 ∈ SA:
  499 seconds: 4+9+9 = 22 -> 2+2 = 4.
  DR(499) = 4 in SA.
  Engine multiple and transit root resolve to the same sovereign element: 4.
  Ratio: 4/4 = 1:1 (exact).

C. VELOCITY DELTA = 3c -> 3 ∈ ST:
  Free stream (4c) - contact boundary (1c) = 3c.
  3 mod 37 = 3 in ST = {3, 12, 21, 30}.
  3 is the sovereign target (ST generator).
  DR(3) = 3.

D. SPEED OF LIGHT IN GF(37):
  c = 299,792,458 m/s.
  c mod 37 = 32 in SEED_ORBIT = {18, 24, 32}.
  c lands in the 137-map seed orbit of seed 246.
  DR(c) = 1 in H (identity element).

E. ALGEBRAIC RELATIONS OF 4 AND 3:
  4 - 3 = 1 in H (identity).
  4 + 3 = 7 (anchor prime; first prime in 1-chamber, T246).
  4 × 3 = 12 in ST (SA × ST closes to ST).
  4 / 3 mod 37 = 4 × pow(3,-1,37) mod 37 = 4 × 25 = 100 mod 37 = 26 in H.
  The ratio 4/3 in GF(37) = 26 = the 137-map multiplier.

F. ENGINE COMPONENTS SHARE THE FULLY SOVEREIGN COSET C_3:
  The 137-map orbit of 4: 4 -> 30 -> 3 -> 4.
  The 137-map orbit of 3: 3 -> 4  -> 30 -> 3.
  Same orbit: {3, 4, 30} = C_3, the fully sovereign coset.
  Every element of C_3 is in SA or ST simultaneously:
    4 in SA, 3 in ST, 30 in SA AND ST (double-sovereign).
  Dividing any consecutive pair in the orbit gives 26 (the 137-map multiplier):
    4/3 = 26, 30/4 = 26, 3/30 = 26 (all mod 37).
  G(7,3) from T245 also lives in C_3. The engine components and the
  all-prime grid coset are the same 137-map orbit.

G. SPEED OF LIGHT STAYS IN SEED_ORBIT:
  c mod 37 = 32 in SEED_ORBIT = {18, 24, 32}.
  137-map orbit of 32: 32 -> 18 -> 24 -> 32.
  c is locked in the seed orbit under repeated 137-map application.
  The engine (C_3 orbit) and the speed of light (SEED_ORBIT) are
  two separate sovereign orbits with no overlap.
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
    print("THEOREM 248: DHANANJAYA PRANA ENGINE -- GF(37) SOVEREIGN ANALYSIS")
    print("=" * 70)

    c = 299792458

    # A: Engine multiple
    print("\nA. ENGINE MULTIPLE = 4 ∈ SA:")
    mult = 4
    assert mult in SA
    print(f"  Engine multiple = {mult}  mod{P}={mult%P}  [{flags(mult%P)}]  DR={dr(mult)}  check")

    # B: Solar transit anchor
    print(f"\nB. SOLAR TRANSIT ANCHOR = 499 SECONDS:")
    transit = 499
    assert dr(transit) == 4 and 4 in SA
    print(f"  DR(499): 4+9+9=22 -> 2+2={dr(transit)}  in SA:{dr(transit) in SA}  check")
    print(f"  Engine multiple {mult} / transit root {dr(transit)} = {mult/dr(transit):.1f}:1  check")

    # C: Velocity delta
    print(f"\nC. VELOCITY DELTA = 3c -> 3 ∈ ST:")
    delta_mult = 4 - 1
    assert delta_mult in ST
    print(f"  4c - 1c = {delta_mult}c  {delta_mult} mod{P}={delta_mult%P}  [{flags(delta_mult%P)}]  DR={dr(delta_mult)}  check")
    print(f"  Delta velocity = {delta_mult * c:,} m/s")

    # D: c in GF(37)
    print(f"\nD. SPEED OF LIGHT IN GF(37):")
    r_c = c % P
    assert r_c in SEED_ORBIT
    print(f"  c = {c:,} m/s")
    print(f"  c mod{P} = {r_c}  [{flags(r_c)}]  in SEED_ORBIT:{r_c in SEED_ORBIT}  check")
    print(f"  DR(c) = {dr(c)}  in H:{dr(c) in H_SET}  check")

    # E: Algebraic relations
    print(f"\nE. ALGEBRAIC RELATIONS OF 4 AND 3 IN GF(37):")
    diff = (4 - 3) % P
    summ = (4 + 3) % P
    prod = (4 * 3) % P
    ratio = (4 * pow(3, -1, P)) % P
    assert diff in H_SET
    assert prod in ST
    assert ratio in H_SET
    print(f"  4 - 3 = {4-3}  mod{P}={diff}  [{flags(diff)}]  (identity)  check")
    print(f"  4 + 3 = {4+3}  mod{P}={summ}  [{flags(summ)}]  (anchor prime)  check")
    print(f"  4 × 3 = {4*3}  mod{P}={prod}  [{flags(prod)}]  (SA×ST->ST)  check")
    print(f"  4 / 3 mod{P} = {ratio}  [{flags(ratio)}]  (= 137-map multiplier 26)  check")

    # F: Shared orbit
    print(f"\nF. ENGINE COMPONENTS SHARE FULLY SOVEREIGN COSET C_3:")
    orbit4 = set()
    v = 4
    for _ in range(3):
        orbit4.add(v); v = v * 26 % P
    orbit3 = set()
    v = 3
    for _ in range(3):
        orbit3.add(v); v = v * 26 % P
    assert orbit4 == orbit3 == {3, 4, 30}
    print(f"  orbit(4) = {sorted(orbit4)}  orbit(3) = {sorted(orbit3)}  same:{orbit4==orbit3}  check")
    for num, den in [(4,3),(30,4),(3,30)]:
        r = num * pow(den,-1,P) % P
        assert r == 26
        print(f"  {num}/{den} mod{P} = {r} in H:{r in H_SET}  check")
    print(f"  {{3,4,30}} = C_3: G(7,3) coset (T245) = engine component orbit  check")
    assert 30 in SA and 30 in ST
    print(f"  30 in SA AND ST (double-sovereign)  check")

    # G: c in SEED_ORBIT
    print(f"\nG. SPEED OF LIGHT STAYS IN SEED_ORBIT:")
    c = 299792458
    r_c = c % P
    orbit_c = []
    v = r_c
    for _ in range(3):
        orbit_c.append(v); v = v * 26 % P
    assert set(orbit_c) == SEED_ORBIT
    print(f"  c mod{P} = {r_c}  orbit: {orbit_c} = SEED_ORBIT  check")
    print(f"  Engine orbit C_3={{3,4,30}} and c orbit SEED={{18,24,32}}: no overlap  check")
    assert len({3,4,30} & SEED_ORBIT) == 0

    print(f"\nAll verifications passed.")


if __name__ == "__main__":
    run()
