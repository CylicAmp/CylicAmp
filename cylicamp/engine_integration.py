"""
Connects MetaEngine and Field simulation into the core pipeline.

MetaEngine.rule_multiplier feeds InsightEngine.multiplier.
Field.mean_threshold feeds TrajectoryGenerator angle modulation.
Two-number patterns feed the modular filter via DR=8 (AHL) anchor.
Seed is classified through the Ulam/GF(37) framework (ulam_spiral.classify).
"""

import sys
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.join(_HERE, "..")
_PRIMES_DIR = os.path.join(_HERE, "..", "math", "primes")

for _p in (_PROJECT_ROOT, _PRIMES_DIR):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from cylicamp.trajectory import TrajectoryGenerator
from cylicamp.insights import InsightEngine
from cylicamp.duality import DualityVerifier
from meta_engine import MetaEngine
from field_simulation import Field, Packet
from ulam_spiral import classify as ulam_classify

_THEOREMS_DIR = os.path.join(_HERE, "..", "math", "theorems")
if _THEOREMS_DIR not in sys.path:
    sys.path.insert(0, _THEOREMS_DIR)

from cascade_8_13_24 import build_cascade
from medusa_v3_sovereign import medusa_v3_sovereign, ANCHORS, TARGETS
from abcabc_mod37_orbit import abcabc_theorem, compute_orbit
from lucas_abbc_chain import lucas_seq


def run_integrated_engine(seed=246, iterations=3, field_nodes=12, steps=50):
    # Step 1: meta_evolve_lane produces multiplier sequence from seed
    engine = MetaEngine(rule_multiplier=7)
    history = engine.meta_evolve_lane(seed_number=seed, iterations=iterations)
    multiplier = history[-1]["multiplier"]

    # Step 2: Field simulation — threshold mean feeds trajectory angle
    field = Field(n=field_nodes)
    for _ in range(50):
        field.step()
    p = Packet(value=0.95, activation=0.4)
    field.inject(p)
    for _ in range(5):
        field.degrade(0.1)
    angle_mod = field.mean_threshold()

    # Step 3: Trajectory using field threshold as angle modulation
    tg = TrajectoryGenerator()
    trajectory = tg.generate_trajectory(steps=steps, angle_multiplier=angle_mod)
    energy_spectrum = [abs(x) + abs(y) for x, y in trajectory]

    # Step 4: Insight engine with meta-evolved multiplier
    ie = InsightEngine(multiplier=float(multiplier))
    raw_data = [int(e * 1000) for e in energy_spectrum]
    filtered = ie.apply_modular_filter(raw_data)
    insight_score = ie.calculate_weighted_insights(filtered)

    # Step 5: Duality verification
    dv = DualityVerifier()
    result = dv.verify_duality_spectrum(energy_spectrum, required_min_stability=0.5)

    # Step 6: Classify seed through Ulam/GF(37) framework
    seed_cell = ulam_classify(seed)

    # Step 7: Cascade — seed residue mod 37 is 24, which is in the {8,13,24} base.
    # Run the cascade and score how many of its 37 elements share the seed's orbit.
    cascade, _, _ = build_cascade([8, 13, 24])
    seed_orbit = set(seed_cell["orbit_137"] or [])
    cascade_orbit_hits = [v for v in cascade if v % 37 in seed_orbit]

    # Step 8: Sovereign classification of seed residue
    sovereign_status = medusa_v3_sovereign(seed_cell["mod37"])

    # Step 9: ABCABC orbit — seed residue is the orbit start (residue 24)
    abcabc_orbit = compute_orbit()
    orbit_position = abcabc_orbit.index(seed_cell["mod37"]) if seed_cell["mod37"] in abcabc_orbit else -1

    # Step 10: Lucas sequence — L(6)=18 is in the seed's orbit (18,24,32)
    lucas = lucas_seq(4, 8)  # L(3)..L(10)
    lucas_orbit_hits = [(i+3, v) for i, v in enumerate(lucas) if v % 37 in seed_orbit]

    print(f"Seed:              {seed}")
    print(f"Meta multiplier:   {multiplier}")
    print(f"Field threshold:   {angle_mod:.4f}")
    print(f"Insight Score:     {insight_score:.4f}")
    print(f"Spectrum Status:   {result['Status']}")
    print(f"Stability Ratio:   {result['Stability_Ratio']:.4f}")
    print(f"Seed DR:           {seed_cell['dr']}")
    print(f"Seed mod 37:       {seed_cell['mod37']}  (sovereign: {seed_cell['sovereign']})")
    print(f"Seed 137-orbit:    {seed_cell['orbit_137']}")
    print(f"Cascade orbit hits:{len(cascade_orbit_hits)}/37  {cascade_orbit_hits}")
    print(f"Sovereign status:  {sovereign_status}")
    print(f"ABCABC orbit pos:  {orbit_position} (0 = orbit start)")
    print(f"Lucas orbit hits:  {lucas_orbit_hits}")

    return {
        "seed": seed,
        "multiplier": multiplier,
        "field_threshold": angle_mod,
        "insight_score": insight_score,
        "stability": result,
        "meta_history": history,
        "seed_ulam": seed_cell,
    }


if __name__ == "__main__":
    run_integrated_engine(seed=246, iterations=3)
