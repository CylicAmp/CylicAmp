"""
Principle 1: The Substrate Principle

CORRECTION ON NEWTON
======================
Newton did not write the rules. Newton described what was already happening.
Biology implemented the substrate rules in hardware hundreds of millions of years
before Newton put them into words. Newton's laws are a translation.
Biology's vestibular system is a direct physical instantiation.

Neither Newton nor biology is the authority. Both are readers of the same source.

Priority order (correct):
  1. The substrate (GF(37) / physical law)
  2. Biology — reads and implements in hardware, directly, without intermediary
  3. Newton — reads and translates into symbolic equations, with human intermediary
  4. Formal mathematics — reads Newton's translation and formalizes further

The standard textbook presentation reverses this: "Newton discovered laws → biology follows them."
This is wrong. Biology ran the experiment first. Newton named it. The substrate is prior to both.

Implication for intuition:
  When pattern recognition fires before formal proof — when you sense a connection
  before you can state it — that is biological substrate reading running ahead of
  the symbolic translation. It is not guessing. It is the direct hardware reader
  operating at its native speed, prior to the language layer.

STATEMENT
==========
Biology does not invent. Biology reverse-engineers.
Evolution surveys the physical substrate and builds hardware to match its rules.
If the substrate is GF(37), then every biological system optimized by evolution
will reflect GF(37) structure — not because we imposed the lens,
but because the lens is the substrate itself.

THE CONVERGENT ENGINEERING PROOF
==================================
Silicon accelerometers and biological vestibular systems arrived at the same design:
  - Three orthogonal axes (X, Y, Z)
  - Inertial mass on a compliant suspension
  - Linear transduction of acceleration to signal

They are not the same because engineering copied biology or vice versa.
They are the same because neither had a choice. The substrate (3D space + gravity)
wrote the specification. Both implementations read from the same rulebook.

This is the falsifiability argument:
  IF the design were arbitrary → different implementations would diverge.
  IF the design were substrate-mandated → all implementations would converge.
  Observation: convergence.
  Conclusion: substrate-mandated.

The same argument applies to GF(37): if the framework were imposed,
we would expect misses. We find hits across biology, physics, chemistry, and cosmology.
The hits are convergence evidence — the substrate is GF(37).

BIOLOGICAL SUBSTRATE READINGS
================================

BODY TEMPERATURE: 37°C = THE PRIME = SEAM
  Human core temperature: 37°C.
  37 mod 37 = 0 = SEAM.
  Life maintains its core at the prime temperature — the field annihilation point.
  The thermal optimum for human enzyme activity is the prime itself.
  Not 36°C. Not 38°C. 37°C.

CIRCADIAN RHYTHM: 24h ∈ SEED ORBIT
  The biological clock period: 24 hours.
  24 ∈ Seed Orbit {18, 24, 32}.
  The clock that governs all biological timing is tuned to a seed orbit period.
  Evolution read the Earth's rotation (24h) and embedded it in the seed orbit.

ATP MOLECULAR WEIGHT ≡ 26 (mod 37) = MULTIPLIER
  ATP (adenosine triphosphate): molecular weight ≈ 507 g/mol.
  507 mod 37 = 26 = the 137-map multiplier.
  ATP is the universal energy currency of all life.
  Every cellular process — muscle contraction, nerve firing, protein synthesis —
  runs through ATP. The energy currency of life operates at multiplier frequency.

RESTING HEART RATE 72 bpm: DR = 9 = SEAM
  Standard resting heart rate: ~72 bpm.
  DR(72) = 9 = SEAM.
  The baseline cardiac rhythm has digital root SEAM.

SOLAR PEAK WAVELENGTH ≡ 32 (mod 37) = SEED ORBIT
  Solar emission peak: ~550 nm (green-yellow).
  550 mod 37 = 32 ∈ Seed Orbit {18, 24, 32}.
  Human eyes are tuned to the solar peak wavelength.
  The photoreceptors did not choose their peak — the sun dictated it.
  The sun's peak is a seed orbit wavelength.

LUNAR CYCLE ≡ 30 (mod 37) = SOVEREIGN ANCHOR AND TARGET
  Lunar synodic period: ~29.5 days. Rounded: 30 days.
  30 mod 37 = 30 ∈ Sovereign Anchors {4, 9, 25, 30}.
  30 ∈ Sovereign Targets {3, 12, 21, 30}.
  The lunar cycle is the only element in both sovereign sets.
  Human reproductive cycle (~28-30 days) is entrained to the lunar cycle.

ACTION POTENTIAL PEAK ≡ 3 (mod 37) = SOVEREIGN TARGET
  Neural action potential peak: ~+40 mV.
  40 mod 37 = 3 ∈ Sovereign Targets {3, 12, 21, 30}.
  The voltage that fires every thought, sensation, and movement
  is a sovereign target.

DNA BASE PAIRING: 3-CYCLE AND PRIMITIVE ROOT
  GC bond: 3 hydrogen bonds = the heartbeat cycle length (ord₃₇(26) = 3).
  AT bond: 2 hydrogen bonds = the primitive root of GF(37) (ord₃₇(2) = 36).
  DNA uses the heartbeat number for its stronger bond
  and the primitive root number for its weaker bond.
  The double helix encodes the two fundamental structures of GF(37).

VESTIBULAR SYSTEM: 3D SPACE → 3-CYCLE (Theorem 181, 182)
  3 otolith axes + 3 semicircular canals = 6 DOF = TESLA_FLOW.
  CaCO₃ molecular weight mod 37 = 26 = multiplier.
  Ca atomic mass mod 37 = 3 = sovereign target.
  Ca noble-gas core = Ar (Z=18) ∈ seed orbit.
  The substrate (3D space + gravity) dictated the design.
  The design reflects GF(37) because GF(37) is the substrate.

THE PRINCIPLE IN ONE STATEMENT
================================
  Biology is constrained by physics.
  Physics is structured by GF(37).
  Therefore biology reflects GF(37).

  Not as metaphor. Not as approximation.
  As direct consequence of the substrate being what it is.

  Every biological constant that lands in the framework
  is a convergence data point. The accumulation of convergences
  is the evidence that the substrate — not the analyst —
  is the source of the structure.
"""

P = 37

def dr(n):
    n = abs(int(n))
    return 9 if n % 9 == 0 and n != 0 else n % 9

def run_assertions():
    # Body temperature = prime = SEAM
    body_temp_C = 37
    assert body_temp_C == P
    assert body_temp_C % P == 0    # SEAM

    # Circadian rhythm: 24h in seed orbit
    circadian_h = 24
    assert circadian_h in {18, 24, 32}

    # ATP molecular weight mod 37 = multiplier
    ATP_weight = 507
    assert ATP_weight % P == 26    # multiplier
    assert 137 % P == 26           # confirm multiplier

    # Heart rate 72 DR = SEAM
    assert dr(72) == 9

    # Solar peak mod 37 = seed orbit
    solar_peak_nm = 550
    assert solar_peak_nm % P == 32
    assert 32 in {18, 24, 32}

    # Lunar cycle mod 37 = sovereign anchor and target
    lunar_days = 30
    assert lunar_days % P == 30
    assert 30 in {4, 9, 25, 30}    # sovereign anchor
    assert 30 in {3, 12, 21, 30}   # sovereign target

    # Action potential peak mod 37 = sovereign target
    action_potential_mV = 40
    assert action_potential_mV % P == 3
    assert 3 in {3, 12, 21, 30}    # sovereign target

    # DNA: GC=3, AT=2
    GC_bonds = 3
    AT_bonds = 2
    assert pow(26, GC_bonds, P) == 1   # 3 = cycle length of 137-map
    assert pow(AT_bonds, 36, P) == 1   # 2 = primitive root

    # Vestibular DOF = 6 = TESLA_FLOW
    vestibular_dof = 6
    assert pow(vestibular_dof, 4, P) == 1   # ord_37(6) = 4

    print("All assertions passed.")

if __name__ == "__main__":
    run_assertions()
