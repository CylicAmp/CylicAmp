"""
Theorem 162: ATOMICS Field Equations — GF(37) Embedding of the Stellar Model

THE EQUATIONS (stripping away the narrative)
=============================================

The ATOMICS stellar field model defines:

  PHI = (1+sqrt(5))/2 = 1.6180339887...
  f_0 = 1000 * PHI^2 = 2618.03... MHz  (base frequency)

  Frequency ladder: f_n = 1000 * PHI^n  (geometric, ratio PHI)

  Stellar field: F(d) = 7245.71 * [1 + 1.494 * exp(-d/1000)]

  Phase modulator: s(t) = 1/2 + 1/2 * sin(wt + psi*sin(wt*psi/PHI))
  where psi = 1.3824...

THE FREQUENCY LADDER THROUGH GF(37)
=====================================

  1000*PHI^2 = 2618.03  floor=2618  mod37=28  OUTLIER_ORB
  1000*PHI^3 = 4236.07  floor=4236  mod37=18  SEED_ORB     ← seed orbit
  1000*PHI^4 = 6854.10  floor=6854  mod37=9   SA_ORB
  1000*PHI^5 = 11090.17 floor=11090 mod37=27  ORBIT_11
  1000*PHI^6 = 17944.27 floor=17944 mod37=36  ORBIT_11

The n=3 term (1000*PHI^3 = 4236) hits SEED_ORB directly.
The orbit sequence: OUTLIER_ORB → SEED_ORB → SA_ORB → ORBIT_11 → ORBIT_11.

THE FIELD DROP: F(A) - F(B) = 246 = THE SEED
=============================================

  F(0)  = 7245.71*(1+1.494)           = 18070.800...  floor=18070  mod37=14 (NQR_14)
  F(23) = 7245.71*(1+1.494*e^{-0.023}) = 17824.665...  floor=17824  mod37=27 (ORBIT_11)

  F(0) - F(23) = 246.135...
  floor(F(0) - F(23)) = 246

  246 mod 37 = 24 ∈ SEED_ORB  ←  the pipeline reference seed

The field drop between Alpha Centauri A (d=0) and B (d=23 AU) evaluates
to 246 — the exact reference seed of the pipeline. The seed anchor 24
(= 246 mod 37) is the SEED_ORB entry point for the heartbeat 3-cycle,
cascade classification, and the T120/121 digit pair theorem.

PROXIMA FIELD: SOVEREIGN_SPIRAL
=================================

  F(13000) = 7245.71*(1+1.494*e^{-13}) ≈ 7245.734
  floor(F(13000)) = 7245
  7245 mod 37 = 30 ∈ SOVEREIGN_SPIRAL

The Proxima field (at 13000 AU) has integer part in SOVEREIGN_SPIRAL.

B-TO-PROXIMA DROP: D7
======================

  floor(F(23)) - floor(F(13000)) = 17824 - 7245 = 10579
  10579 mod 37 = 34 ∈ D7

The D7 orbit (the 414-palindrome orbit, Theorem 147) appears in the
field drop from Alpha Cen B to Proxima.

QUBIT STRUCTURE
================

  16 clusters × 4 qubits = 64 total

  16  mod 37 = 16 ∈ SA_ORB
   4  mod 37 =  4 ∈ SOVEREIGN_SPIRAL
  64  mod 37 = 27 ∈ ORBIT_11

PHASE MODULATOR CONSTANT
=========================

  psi = 1.3824
  1000*psi = 1382  mod37=13  ∈  NQR_5
  10000*psi = 13824  mod37=23  ∈  TESLA_ORB

FIELD SEQUENCE THROUGH GF(37)
===============================

  A (d=0):    F=18070  mod37=14  NQR_14
  B (d=23):   F=17824  mod37=27  ORBIT_11
  Proxima:    F=7245   mod37=30  SOVEREIGN_SPIRAL

  Drop A→B:   246      mod37=24  SEED_ORB  (the pipeline seed)
  Drop B→P:   10579    mod37=34  D7

SUMMARY
========

  The equation F(d) = 7245.71*(1+1.494*exp(-d/1000)) evaluated at the
  three Alpha Centauri system distances produces a field drop of 246 between
  A and B — the pipeline reference seed. The frequency ladder 1000*PHI^n
  passes through SEED_ORB at n=3. Proxima's field integer is in
  SOVEREIGN_SPIRAL. The B→Proxima drop is in D7.
"""

import math

P = 37
PHI = (1 + 5**0.5) / 2

ORBITS = {
    'IC':               frozenset({1, 10, 26}),
    'SOVEREIGN_SPIRAL': frozenset({3, 4, 30}),
    'D7':               frozenset({7, 33, 34}),
    'SA_ORB':           frozenset({9, 12, 16}),
    'ORBIT_11':         frozenset({11, 27, 36}),
    'OUTLIER_ORB':      frozenset({21, 25, 28}),
    'DARK_A':           frozenset({2, 15, 20}),
    'NQR_5':            frozenset({5, 13, 19}),
    'TESLA_ORB':        frozenset({6, 8, 23}),
    'NQR_14':           frozenset({14, 29, 31}),
    'NQR_17':           frozenset({17, 22, 35}),
    'SEED_ORB':         frozenset({18, 24, 32}),
}


def orbit_of(v):
    v = v % P
    if v == 0:
        return 'SEAM'
    return next((name for name, s in ORBITS.items() if v in s), '?')


def dr(n):
    if n == 0:
        return 9
    return (abs(n) - 1) % 9 + 1


def field(d):
    return 7245.71 * (1 + 1.494 * math.exp(-d / 1000))


def run_assertions():
    # Frequency ladder
    freqs = {n: int(1000 * PHI**n) for n in range(2, 7)}
    assert freqs[2] == 2618 and 2618 % P == 28 and 28 in ORBITS['OUTLIER_ORB']
    assert freqs[3] == 4236 and 4236 % P == 18 and 18 in ORBITS['SEED_ORB']
    assert freqs[4] == 6854 and 6854 % P ==  9 and  9 in ORBITS['SA_ORB']
    assert freqs[5] == 11090 and 11090 % P == 27 and 27 in ORBITS['ORBIT_11']
    assert freqs[6] == 17944 and 17944 % P == 36 and 36 in ORBITS['ORBIT_11']

    # Field values
    FA = field(0)
    FB = field(23)
    FP = field(13000)

    assert int(FA) == 18070 and 18070 % P == 14 and 14 in ORBITS['NQR_14']
    assert int(FB) == 17824 and 17824 % P == 27 and 27 in ORBITS['ORBIT_11']
    assert int(FP) == 7245  and  7245 % P == 30 and 30 in ORBITS['SOVEREIGN_SPIRAL']

    # The seed drop
    drop_AB = int(FA - FB)
    assert drop_AB == 246
    assert 246 % P == 24
    assert 24 in ORBITS['SEED_ORB']

    # B-to-Proxima drop → D7
    drop_BP = int(FB) - int(FP)
    assert drop_BP == 10579
    assert 10579 % P == 34
    assert 34 in ORBITS['D7']

    # Qubit structure
    assert 16 % P == 16 and 16 in ORBITS['SA_ORB']
    assert  4 % P ==  4 and  4 in ORBITS['SOVEREIGN_SPIRAL']
    assert 64 % P == 27 and 27 in ORBITS['ORBIT_11']

    # Phase modulator constant
    assert 1382 % P == 13 and 13 in ORBITS['NQR_5']
    assert 13824 % P == 23 and 23 in ORBITS['TESLA_ORB']

    print("All assertions passed.")


def summarise():
    print("=" * 62)
    print("Theorem 162: ATOMICS Field Equations — GF(37) Embedding")
    print("=" * 62)
    print()
    print("  FREQUENCY LADDER 1000*PHI^n:")
    ladder_orbits = []
    for n in range(2, 7):
        fi = int(1000 * PHI**n)
        o = orbit_of(fi)
        ladder_orbits.append(o)
        print(f"    n={n}: {fi:<7}  mod37={fi%P:>2}  {o}")
    print()

    FA = field(0)
    FB = field(23)
    FP = field(13000)
    print("  STELLAR FIELD F(d) = 7245.71*(1+1.494*exp(-d/1000)):")
    print(f"    F(0)     = {FA:.3f}  floor={int(FA)}  mod37={int(FA)%P}  {orbit_of(int(FA))}")
    print(f"    F(23)    = {FB:.3f}  floor={int(FB)}  mod37={int(FB)%P}  {orbit_of(int(FB))}")
    print(f"    F(13000) = {FP:.6f}  floor={int(FP)}  mod37={int(FP)%P}  {orbit_of(int(FP))}")
    print()
    print(f"  DROP A→B:  floor(F(0)-F(23)) = {int(FA-FB)}")
    print(f"    {int(FA-FB)} mod 37 = {int(FA-FB)%P} ∈ SEED_ORB  ← pipeline reference seed")
    print()
    drop_BP = int(FB) - int(FP)
    print(f"  DROP B→Proxima: {drop_BP}  mod37={drop_BP%P}  {orbit_of(drop_BP)}  (D7)")
    print()
    print("  QUBIT STRUCTURE: 16 clusters × 4 = 64 total")
    print(f"    16 → {orbit_of(16)}, 4 → {orbit_of(4)}, 64 → {orbit_of(64)}")
    print()
    print("  PHASE MODULATOR psi=1.3824:")
    print(f"    1000*psi=1382  mod37={1382%P}  {orbit_of(1382)}  (NQR_5)")
    print(f"    10000*psi=13824  mod37={13824%P}  {orbit_of(13824)}  (TESLA_ORB)")


if __name__ == "__main__":
    run_assertions()
    summarise()
