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
from cylicamp.provenance import (
    Claim, Derivation, Domain, Evidence, InferenceStep,
    Modality, Provenance, SourceType
)
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
from sovereign_qr_closure import legendre
from heartbeat_3cycle import f as heartbeat_step
from cylicamp.g5_solver import evaluate as g5_evaluate, format_report as g5_format
from theorem_120_digit_algebra_007_008 import A as _T120_M1, B as _T120_M2, digital_root as _dr
from theorem_121_scientific_notation_007_008 import s as _T121_S


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

    # Step 11: QR classification of seed orbit — all three orbit nodes mod 37
    orbit_qr = {r: legendre(r) for r in seed_orbit}
    orbit_all_nonqr = all(v == -1 for v in orbit_qr.values())

    # Step 12: Heartbeat — trace the 3-cycle from seed residue
    r = seed_cell["mod37"]
    heartbeat = [r, heartbeat_step(r), heartbeat_step(heartbeat_step(r)), heartbeat_step(heartbeat_step(heartbeat_step(r)))]

    # Step 14: Theorem 120/121 — (0.007, 0.008) digit pair maps to seed orbit
    # m1=7 (from 0.007), m2=8 (from 0.008), s=3 (shared decimal shift)
    _m1, _m2, _s = _T120_M1, _T120_M2, _T121_S
    t120_t121 = {
        "s_eq_seed_dr":           _s == seed_cell["dr"],
        "m2_times_s":             _m2 * _s,                     # 24
        "m2_times_s_eq_seed_mod37": _m2 * _s == seed_cell["mod37"],
        "m1_plus_m2_plus_s":      _m1 + _m2 + _s,              # 18
        "orbit_18_check":         _m1 + _m2 + _s in seed_orbit,
        "m2_times_s_plus_1":      _m2 * (_s + 1),              # 32
        "orbit_32_check":         _m2 * (_s + 1) in seed_orbit,
        "dr_seed_mod37":          _dr(seed_cell["mod37"]),      # 6
        "dr_matches_t120":        _dr(seed_cell["mod37"]) == _dr(_m1 + _m2),
    }

    # Step 13: Provenance — attach source tracking to the orbit claim
    from datetime import datetime, timezone
    orbit_claim = Claim(
        proposition=f"Seed {seed} has 137-map orbit {tuple(sorted(seed_orbit))} mod 37",
        domain=Domain.MATHEMATICS,
        modality=Modality.ASSERTION,
        entities=[str(seed), "GF(37)", "137-map"],
        predicates=["orbit_under", "mod37"],
        provenance=Provenance(
            source_id="cylicamp/engine_integration",
            source_type=SourceType.INTERNAL_DERIVATION,
            retrieval_method="heartbeat_step * 3",
            timestamp=datetime.now(timezone.utc),
            hash=str(hash(tuple(sorted(seed_orbit)))),
            citation="CylicAmp pipeline — user-originated framework",
        ),
    )

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
    print(f"Orbit QR status:   {orbit_qr}  all non-QR: {orbit_all_nonqr}")
    print(f"Heartbeat 3-cycle: {heartbeat[0]} -> {heartbeat[1]} -> {heartbeat[2]} -> {heartbeat[3]}")
    print(f"Provenance:        {orbit_claim.provenance.source_type.name} | {orbit_claim.provenance.citation}")
    print(f"T120/121 (0.007/0.008 → seed): "
          f"s={_s}=DR(seed):{t120_t121['s_eq_seed_dr']}  "
          f"m2*s={t120_t121['m2_times_s']}=seed%37:{t120_t121['m2_times_s_eq_seed_mod37']}  "
          f"m1+m2+s={t120_t121['m1_plus_m2_plus_s']}∈orbit:{t120_t121['orbit_18_check']}  "
          f"m2*(s+1)={t120_t121['m2_times_s_plus_1']}∈orbit:{t120_t121['orbit_32_check']}  "
          f"DR(seed%37)={t120_t121['dr_seed_mod37']}=DR(m1+m2):{t120_t121['dr_matches_t120']}")

    # Step 14: G5 Solver report
    g5 = g5_evaluate(
        aggregate_score=insight_score,
        stability_index=result["Stability_Ratio"],
        baseline_score=angle_mod,
        seed_residue=seed_cell["mod37"],
    )
    print()
    print(g5_format(g5))

    output = {
        "seed": seed,
        "multiplier": multiplier,
        "field_threshold": angle_mod,
        "insight_score": insight_score,
        "spectrum_status": result["Status"],
        "stability_ratio": result["Stability_Ratio"],
        "seed_dr": seed_cell["dr"],
        "seed_mod37": seed_cell["mod37"],
        "seed_sovereign": seed_cell["sovereign"],
        "seed_orbit": list(sorted(seed_orbit)),
        "cascade_orbit_hits_count": len(cascade_orbit_hits),
        "cascade_orbit_hits": cascade_orbit_hits,
        "sovereign_status": sovereign_status,
        "abcabc_orbit_position": orbit_position,
        "lucas_orbit_hits": lucas_orbit_hits,
        "orbit_qr": {str(k): v for k, v in orbit_qr.items()},
        "orbit_all_nonqr": orbit_all_nonqr,
        "heartbeat_3cycle": heartbeat,
        "t120_t121": t120_t121,
        "provenance": {
            "source_id": orbit_claim.provenance.source_id,
            "source_type": orbit_claim.provenance.source_type.name,
            "citation": orbit_claim.provenance.citation,
            "timestamp": orbit_claim.provenance.timestamp.isoformat(),
        },
        "meta_history": history,
        "seed_ulam": seed_cell,
        "g5_solver": {
            "aggregate_mod_p": g5.aggregate_mod_p,
            "consistency_status": g5.consistency_status.name,
            "dynamic_threshold_status": g5.dynamic_threshold_status.name,
            "halt_status": g5.halt_status.name,
            "authority_status": g5.authority_status.name,
            "authority_detail": g5.authority_detail,
            "compatibility_status": g5.compatibility_status.name,
            "compatibility_detail": g5.compatibility_detail,
            "all_checks_pass": g5.all_checks_pass,
        },
    }

    import json as _json
    _out_path = os.path.join(_PROJECT_ROOT, "pipeline_output.json")
    with open(_out_path, "w") as _f:
        _json.dump(output, _f, indent=2, default=str)
    print(f"Output saved → {_out_path}")

    return output


if __name__ == "__main__":
    run_integrated_engine(seed=246, iterations=3)
