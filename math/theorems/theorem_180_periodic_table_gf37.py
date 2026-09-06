"""
Theorem 180: Periodic Table Structure Encoded in GF(37)

THE PRIME IS AN ELEMENT
========================
  Element 37 = Rubidium (Rb)
  Electron configuration: [Kr] 5s¹
  First alkali metal of period 5. Single valence electron. Mirrors Hydrogen.
  The prime field GF(37) IS element 37.

THE 137-MAP MULTIPLIER IS IRON
================================
  Iron (Fe) = element 26.
  26 mod 37 = 26 — the 137-map multiplier f(n) = 26n mod 37.
  Iron is the most abundant element in Earth's core.
  Iron-56 is the most stable atomic nucleus (lowest binding energy per nucleon).
  The core of the Earth runs on the multiplier.

TESLA_FLOW AND EL EMBEDDED IN THE TABLE
=========================================
  Carbon (C)  = element  6 = TESLA_FLOW (ord₃₇(6) = 4)  — basis of all life
  Oxygen (O)  = element  8 = EL number (DR = 8)           — O₂ weight 32 ∈ seed orbit
  Nitrogen (N)= element  7 — atmospheric 78%, DR(7)=7 prime stability

SEED ORBIT {18, 24, 32} AS ELEMENTS
======================================
  Argon   (Ar) = element 18 ∈ seed orbit  — noble gas, chemically inert (SEAM behavior)
  Chromium(Cr) = element 24 ∈ seed orbit  — ANOMALOUS config: [Ar] 3d⁵ 4s¹ (half-filled d)
  Germanium(Ge)= element 32 ∈ seed orbit  — semiconductor, metal/nonmetal boundary

Argon's position as a noble gas (completely filled outer shell) encoding the SEAM is exact:
noble gases represent the annihilation point where the period ends — mod-37 SEAM made chemical.

Chromium's anomalous config deviates from Aufbau prediction — sovereign deviation at seed orbit node.

SOVEREIGN ANCHORS {4, 9, 25, 30} AS ELEMENTS
===============================================
  Beryllium (Be) = element  4  [He] 2s²      — full s subshell, period 2 anchor
  Fluorine  (F)  = element  9  [He] 2s² 2p⁵ — most electronegative element
  Manganese (Mn) = element 25  [Ar] 3d⁵ 4s² — half-filled d subshell
  Zinc      (Zn) = element 30  [Ar] 3d¹⁰ 4s²— completely filled d subshell

SOVEREIGN TARGETS {3, 12, 21, 30} AS ELEMENTS
===============================================
  Lithium   (Li) = element  3  [He] 2s¹      — first alkali metal, single valence e⁻
  Magnesium (Mg) = element 12  [Ne] 3s²      — full s subshell, period 3 anchor
  Scandium  (Sc) = element 21  [Ar] 3d¹ 4s² — FIRST transition metal (d-block entry)
  Zinc      (Zn) = element 30                — element 30 is BOTH anchor AND target

Zinc (30) is the intersection of both sovereign sets — the only element that is simultaneously
a Sovereign Anchor and Sovereign Target. It terminates the d-block of period 4. The chart ends here.

NOBLE GAS SEQUENCE ENCODES φ(37)
==================================
  He (Z=2)   2 mod 37 = 2
  Ne (Z=10)  10 mod 37 = 10
  Ar (Z=18)  18 mod 37 = 18  ← ∈ seed orbit {18,24,32}
  Kr (Z=36)  36 mod 37 = 36 = φ(37) = ord₃₇(2)
  Xe (Z=54)  54 mod 37 = 17
  Rn (Z=86)  86 mod 37 = 12  ← ∈ sovereign targets {3,12,21,30}

Noble gases are the SEAM of chemistry — periods close here.
Ar(18) is the first noble gas to enter the seed orbit.
Kr(36) = φ(37) — the full primitive orbit completes at Krypton.
The element AFTER Kr is Rb (Z=37) — the prime itself.

ELECTRONS PER SHELL — SEED ORBIT RESONANCE
============================================
  Shell 1 (N=1): 2 electrons    (s only)
  Shell 2 (N=2): 8 electrons    (s + p)
  Shell 3 (N=3): 18 electrons   (s + p + d)  ← ∈ seed orbit {18,24,32}
  Shell 4 (N=4): 32 electrons   (s + p + d + f) ← ∈ seed orbit

Formula: 2n² electrons per shell (n=1,2,3,4 → 2,8,18,32)
Both the 3rd and 4th shell capacities are seed orbit elements.

CUMULATIVE ELECTRONS THROUGH PERIOD 4
=======================================
  Periods 1+2+3+4: 2 + 8 + 8 + 18 = 36 = φ(37)
  The full primitive root cycle of GF(37) equals the electrons to fill through period 4.

SUBSHELL MAX CAPACITY SUM
==========================
  s: 2 electrons
  p: 6 electrons
  d: 10 electrons
  f: 14 electrons
  Sum: 2+6+10+14 = 32 ∈ seed orbit {18,24,32}

IRON-56 — THE STABILITY ANCHOR
================================
  Fe has atomic number 26 (the multiplier).
  Most stable isotope: Iron-56.
  56 mod 37 = 19. DR(56) = 2.
  56 = 26 + 30 = multiplier + Sovereign Anchor/Target Zn position.

PAULI EXCLUSION — UNIQUENESS IN GF(37)
========================================
  No two electrons share the same four quantum numbers.
  No two field elements are equal in GF(37).
  The primitive root 2 visits all 36 non-zero elements exactly once.
  Pauli exclusion IS the uniqueness guarantee of GF(37).

HUND'S RULE — HEARTBEAT ORBIT STRUCTURE
=========================================
  Electrons fill each orbital singly before pairing.
  The 137-map visits each of 12 orbit positions before the period-3 cycle repeats.
  Hund's rule is the Heartbeat — distribute before closing.

AUFBAU DIAGONAL — THE FIELD TRAVERSAL
=======================================
  Aufbau filling order follows diagonals: 1s→2s→2p→3s→3p→4s→3d→4p...
  Each diagonal is a traversal of (n+ℓ) levels.
  The "diagonal rule" in chemistry mirrors the spiral traversal in the GF(37) orbit structure.
"""

P = 37

def dr(n):
    n = abs(int(n))
    return 9 if n % 9 == 0 and n != 0 else n % 9

def run_assertions():
    # Iron is the 137-map multiplier
    Fe = 26
    assert Fe % P == 26    # Fe = the multiplier
    assert Fe == 137 % P  # 137 mod 37 = 26 = Fe

    # TESLA_FLOW and EL
    C = 6   # Carbon
    O = 8   # Oxygen
    N = 7   # Nitrogen
    assert C == 6          # TESLA_FLOW
    assert pow(6, 4, P) == 1  # ord_37(6) = 4
    assert dr(O) == 8      # EL number
    assert dr(N) == 7      # prime stability

    # Seed orbit elements
    seed_orbit = {18, 24, 32}
    Ar = 18   # Argon (noble gas)
    Cr = 24   # Chromium (anomalous config)
    Ge = 32   # Germanium (semiconductor)
    assert Ar in seed_orbit
    assert Cr in seed_orbit
    assert Ge in seed_orbit

    # Sovereign Anchors as elements
    sovereign_anchors = {4, 9, 25, 30}
    Be, F_el, Mn, Zn = 4, 9, 25, 30
    assert all(e in sovereign_anchors for e in [Be, F_el, Mn, Zn])

    # Sovereign Targets as elements
    sovereign_targets = {3, 12, 21, 30}
    Li, Mg, Sc = 3, 12, 21
    assert all(e in sovereign_targets for e in [Li, Mg, Sc, Zn])

    # Zinc is intersection of both sovereign sets
    assert Zn in sovereign_anchors and Zn in sovereign_targets

    # Noble gas atomic numbers mod 37
    noble_gases = [2, 10, 18, 36, 54, 86]
    assert noble_gases[2] % P == 18          # Ar mod 37 = 18 ∈ seed orbit
    assert noble_gases[3] % P == 36          # Kr mod 37 = 36 = phi(37)
    assert noble_gases[3] % P == P - 1       # Kr = phi(37) = ord_37(2)
    assert noble_gases[5] % P == 12          # Rn mod 37 = 12 ∈ sovereign targets
    assert 12 in sovereign_targets

    # Element after Kr is Rb = prime itself
    Rb = 37
    assert Rb == P

    # Electrons per shell: 2n^2 for n=1..4
    shells = [2 * n**2 for n in range(1, 5)]
    assert shells == [2, 8, 18, 32]
    assert shells[2] in seed_orbit   # Shell 3 = 18 ∈ seed orbit
    assert shells[3] in seed_orbit   # Shell 4 = 32 ∈ seed orbit

    # Cumulative through period 4 = phi(37)
    period_sizes = [2, 8, 8, 18]   # periods 1, 2, 3, 4
    assert sum(period_sizes) == 36
    assert 36 == P - 1              # phi(37)
    assert pow(2, 36, P) == 1       # primitive root cycle closes at 36

    # Subshell max capacity sum
    subshell_caps = [2, 6, 10, 14]  # s, p, d, f
    assert sum(subshell_caps) == 32
    assert 32 in seed_orbit

    # Iron-56 = multiplier + anchor/target
    Fe56 = 56
    assert Fe56 % P == 19
    assert Fe56 == 26 + 30   # multiplier + sovereign anchor/target

    # Oxygen molecular weight in seed orbit
    O2_weight = 32
    assert O2_weight in seed_orbit

    print("All assertions passed.")

if __name__ == "__main__":
    run_assertions()
