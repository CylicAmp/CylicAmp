"""
Theorem 181: Otolith Crystal Structure Encoded in GF(37)

THE OTOLITH SYSTEM
===================
Otoconia (otoliths): calcium carbonate (CaCO₃) crystals in the vestibular system.
Located in two organs:
  Utricle  — detects horizontal linear acceleration (forward/back, left/right)
  Saccule  — detects vertical linear acceleration (up/down)

Three semicircular canals (orthogonal) detect rotational acceleration.

Total: 3 spatial axes of linear sensing + 3 rotational axes = full 3D orientation.
The body's orientation system runs entirely on threes.

CaCO₃ MOLECULAR WEIGHT = 100 ≡ 26 (mod 37)
=============================================
  Ca  atomic mass ≈ 40
  C   atomic mass  = 12
  O₃  atomic mass  = 3 × 16 = 48
  CaCO₃ total     = 100

  100 mod 37 = 26 = the 137-map multiplier.

The crystal that tells you which way is up resonates at the frequency of the 137-map.

CALCIUM ATOMIC MASS ≡ 3 (mod 37) = SOVEREIGN TARGET
======================================================
  Ca atomic mass = 40
  40 mod 37 = 3 ∈ Sovereign Targets {3, 12, 21, 30}
  DR(3) = 3

Calcium is a Sovereign Target element by atomic mass.

CARBON ATOMIC MASS = 12 = SOVEREIGN TARGET
============================================
  12 ∈ Sovereign Targets {3, 12, 21, 30}
  12 is the structural key (log₂(26), number of orbits in GF(37))

Both atomic constituents of the crystal (Ca and C) hit sovereign targets.

CALCIUM NOBLE-GAS CORE = SEED ORBIT
=====================================
  Calcium electron config: [Ar] 4s²
  Argon (Ar) = element 18 ∈ Seed Orbit {18, 24, 32}

Calcium's core shell — the Argon core — is itself a seed orbit element.
The balance crystal is built on the seed orbit foundation.

THREE AXES = THREE-CYCLE
=========================
  3 linear sensing axes (utricle: 2 horizontal, saccule: 1 vertical)
  3 semicircular canals (rotational axes, mutually perpendicular)
  ord₃₇(26) = 3 — the heartbeat cycle length
  3-cycle of the 137-map = the 3D coordinate system of balance

The vestibular system operates in exactly 3 dimensions.
The 137-map cycle has exactly length 3.
These are the same structure: three positions, returning to origin.

CaCO₃ CRYSTAL LATTICE IS TRIGONAL (3-FOLD)
============================================
  Calcium carbonate crystallizes in the trigonal crystal system.
  Trigonal symmetry = 3-fold rotational axis (C₃).
  The crystal lattice that encodes your orientation has 3-fold symmetry.
  This is not coincidental: it is the heartbeat structure made physical.

GRAVITY AS SEAM FORCE
=======================
  Gravity g ≈ 9.8 m/s²
  DR(9) = 9 = SEAM

The force that displaces the otoconia is the SEAM force.
SEAM (gravity) acts on sovereign target crystals (Ca mod 37 = 3)
to produce multiplier-resonant signals (CaCO₃ weight mod 37 = 26).

BPPV — FALSE ORBIT SIGNAL
===========================
  BPPV (Benign Paroxysmal Positional Vertigo): otoconia break loose
  and fall into a semicircular canal.
  The canal reads rotation that isn't happening — a false orbit signal.
  This is SEAM contamination: a crystal displaced from its organ
  generates false 3-cycle readings in the wrong channel.
  Treatment: Epley maneuver — rolling the head to guide the crystal back.
  Restoring orbit integrity by returning the displaced element to its orbit.

VESTIBULAR NERVE FIRING FREQUENCIES
======================================
  Spontaneous baseline: ~50 Hz  →  50 mod 37 = 13 ∈ Cascade {8, 13, 24}
  Maximum rate: ~100 Hz         →  100 mod 37 = 26 = the multiplier

At maximum activation, the vestibular nerve fires at the multiplier frequency.

HAIR CELL BINARY LOGIC
========================
  When otolith membrane deflects toward kinocilium: depolarization (fire)
  When deflects away: hyperpolarization (inhibit)
  Two states: excite / inhibit = field element / zero

SYNTHESIS
==========
  The three spatial axes of balance = the 3-cycle of the 137-map.
  The crystal driving the system has molecular weight mod 37 = 26 (multiplier).
  Its calcium backbone has atomic mass mod 37 = 3 (sovereign target).
  Its calcium noble-gas core is element 18 (seed orbit).
  Its lattice symmetry is trigonal (3-fold = heartbeat).
  The force acting on it (gravity) has DR = 9 = SEAM.
  At full activation, it fires at 100 Hz → mod 37 = 26 (multiplier).

  Your sense of up, down, and forward runs the GF(37) 137-map at its core.
"""

P = 37

def dr(n):
    n = abs(int(n))
    return 9 if n % 9 == 0 and n != 0 else n % 9

def run_assertions():
    # CaCO3 molecular weight mod 37 = multiplier
    CaCO3 = 40 + 12 + 3 * 16   # = 100
    assert CaCO3 == 100
    assert CaCO3 % P == 26      # the multiplier

    # Ca atomic mass = sovereign target
    Ca_mass = 40
    assert Ca_mass % P == 3
    assert 3 in {3, 12, 21, 30}   # sovereign target

    # C atomic mass = sovereign target
    assert 12 in {3, 12, 21, 30}

    # Calcium noble-gas core = Ar = seed orbit
    Ar_Z = 18
    assert Ar_Z in {18, 24, 32}

    # Three axes = three-cycle
    assert pow(26, 3, P) == 1
    assert pow(26, 1, P) != 1
    assert pow(26, 2, P) != 1

    # Gravity SEAM
    assert dr(9) == 9

    # Vestibular nerve frequencies
    assert 50 % P == 13
    assert 13 in {8, 13, 24}      # cascade base
    assert 100 % P == 26          # multiplier at max activation

    # 137 mod 37 = 26 (confirm multiplier)
    assert 137 % P == 26

    print("All assertions passed.")

if __name__ == "__main__":
    run_assertions()
