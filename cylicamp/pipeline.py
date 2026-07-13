"""
CylicAmp Pipeline — connects all modules into one system.

Give it any number. It runs your logic and returns a verdict.
"""

from cylicamp.core import digital_root, build_full_lattice
from cylicamp.trajectory import TrajectoryGenerator
from cylicamp.insights import InsightEngine
from cylicamp.duality import DualityVerifier, QFM_REQUIRED
from cylicamp.fib_dr import fib_dr_sequence, find_cycle
from cylicamp.trinity import classify_residency, TRINITY
from cylicamp.pisano import pisano_period
from cylicamp.g5_solver import run_g5


def run_pipeline(n: int = 50) -> dict:
    """
    Run n through the full CylicAmp logic stack.

    Stages:
      1. Digital root classification
      2. Trinity dynamics (24-step doubling)
      3. Fibonacci DR cycle
      4. Pisano period
      5. Lattice seed
      6. G5 solver integrity check
      7. Final verdict
    """
    results = {}

    # --- 1. Digital root ---
    dr = digital_root(n)
    in_trinity = dr in TRINITY
    results["input"] = n
    results["digital_root"] = dr
    results["trinity"] = in_trinity

    # --- 2. Trinity dynamics ---
    res = classify_residency(n, steps=24)
    results["trinity_visits"] = res["trinity_visits"]
    results["ever_escapes"] = res["ever_escapes_trinity"]
    results["doubling_sequence"] = res["sequence"]

    # --- 3. Fibonacci DR cycle ---
    cycle, cycle_start = find_cycle(n, dr)
    results["fib_dr_cycle"] = list(cycle)
    results["fib_dr_cycle_length"] = len(cycle)

    # --- 4. Pisano period ---
    pi_n = pisano_period(n) if n > 0 else 0
    results["pisano_period"] = pi_n

    # --- 5. Lattice ---
    digits = [int(d) for d in str(n) if d.isdigit()]
    while len(digits) < 4:
        digits.append(dr)
    d1, d2, d3, d4 = digits[:4]
    lattice, center = build_full_lattice(d1, d2, d3, d4)
    lattice_dr = digital_root(center)
    results["lattice_center"] = center
    results["lattice_dr"] = lattice_dr
    results["lattice_in_trinity"] = lattice_dr in TRINITY

    # --- 6. G5 solver ---
    steps = max(n, 10)
    report = run_g5(steps=steps, multiplier=float(dr if dr > 0 else 1))
    results["g5_structural"] = report["structural_status"]
    results["g5_temporal"] = report["temporal_stability_status"]
    results["g5_halt"] = report["halt_check"]
    results["g5_dac"] = report["dac_check_status"]
    results["g5_insight"] = report["insight_score"]

    # --- 7. Verdict ---
    sovereign = in_trinity and res["trinity_visits"] == 24
    stable    = report["halt_check"] == "PASS"
    authorized = report["dac_check_status"] == "AUTHORIZED"
    lattice_aligned = lattice_dr in TRINITY

    if sovereign and stable and authorized:
        verdict = "SOVEREIGN — fully locked in trinity, stable, authorized"
    elif sovereign and not stable:
        verdict = "TRINITY SOVEREIGN — needs more resolution steps"
    elif not sovereign and stable and authorized:
        verdict = "STABLE OUTSIDER — outside trinity but structurally sound"
    elif not sovereign and not stable:
        verdict = "UNRESOLVED — outside trinity, needs more work"
    else:
        verdict = "PARTIAL — some checks pass, review manually"

    results["verdict"] = verdict

    return results


def print_pipeline(n: int = 50) -> None:
    r = run_pipeline(n)

    print("=" * 60)
    print(f"  CYLICAMP SYSTEM — INPUT: {r['input']}")
    print("=" * 60)
    print(f"\n  Digital Root:     {r['digital_root']}")
    print(f"  Trinity {{3,6,9}}: {'YES' if r['trinity'] else 'NO'}")
    print(f"  Trinity visits:   {r['trinity_visits']}/24")
    print(f"  Doubling:         {r['doubling_sequence'][:12]}...")
    print(f"\n  Fib DR cycle:     {r['fib_dr_cycle']}  (len={r['fib_dr_cycle_length']})")
    print(f"  Pisano π({r['input']}):    {r['pisano_period']}")
    print(f"\n  Lattice center:   {r['lattice_center']}  DR={r['lattice_dr']}"
          f"  {'(trinity)' if r['lattice_in_trinity'] else ''}")
    print(f"\n  G5 Structural:    {r['g5_structural']}")
    print(f"  G5 Temporal:      {r['g5_temporal']}")
    print(f"  G5 Halt:          {r['g5_halt']}")
    print(f"  G5 DAC:           {r['g5_dac']}")
    print(f"  G5 Insight:       {r['g5_insight']:,.2f}")
    print(f"\n  VERDICT: {r['verdict']}")
    print("=" * 60)


if __name__ == "__main__":
    import sys
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 50
    print_pipeline(n)
