"""
Connects MetaEngine and Field simulation into the core pipeline.

MetaEngine.rule_multiplier feeds InsightEngine.multiplier.
Field.mean_threshold feeds TrajectoryGenerator angle modulation.
Two-number patterns feed the modular filter via DR=8 (AHL) anchor.
"""

from cylicamp.trajectory import TrajectoryGenerator
from cylicamp.insights import InsightEngine
from cylicamp.duality import DualityVerifier
from math.primes.meta_engine import MetaEngine
from math.primes.field_simulation import Field, Packet


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

    print(f"Seed:              {seed}")
    print(f"Meta multiplier:   {multiplier}")
    print(f"Field threshold:   {angle_mod:.4f}")
    print(f"Insight Score:     {insight_score:.4f}")
    print(f"Spectrum Status:   {result['Status']}")
    print(f"Stability Ratio:   {result['Stability_Ratio']:.4f}")

    return {
        "seed": seed,
        "multiplier": multiplier,
        "field_threshold": angle_mod,
        "insight_score": insight_score,
        "stability": result,
        "meta_history": history,
    }


if __name__ == "__main__":
    run_integrated_engine(seed=246, iterations=3)
