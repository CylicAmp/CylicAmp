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
from cylicamp.chebyshev_bias import chi3
from cylicamp.euler_totient import totient_product_formula
from cylicamp.tribonacci_dr import CYCLE as TRIB_CYCLE
from cylicamp.prime_visual import is_prime, is_dr7_prime
from cylicamp.law_of_12 import is_tesla, TESLA_COMPLETION_FACTOR


def _trib_position(n: int) -> tuple:
    """Return (position in 39-cycle, value at that position)."""
    pos = (n - 1) % 39
    return pos, TRIB_CYCLE[pos]


def _is_twin_prime(n: int) -> bool:
    """True if n forms a twin prime pair (n prime and n+2 prime, or n-2 prime)."""
    if not is_prime(n):
        return False
    return is_prime(n + 2) or (n >= 5 and is_prime(n - 2))


def run_pipeline(n: int = 50) -> dict:
    """
    Run n through the full CylicAmp logic stack.

    Stages:
      1.  Digital root classification
      2.  Trinity dynamics (24-step doubling)
      3.  Fibonacci DR cycle
      4.  Pisano period
      5.  Lattice seed
      6.  G5 solver integrity check
      7.  Chebyshev chi_-3 character
      8.  Euler totient φ(n)
      9.  Tribonacci DR position (period-39 cycle)
      10. Prime / DR-7 prime / twin prime classification
      11. Law of 12 completion check
      12. Final verdict (all axes)
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
    fib_all_trinity = all(v in TRINITY for v in cycle)
    results["fib_cycle_all_trinity"] = fib_all_trinity

    # --- 4. Pisano period ---
    pi_n = pisano_period(n) if n > 0 else 0
    results["pisano_period"] = pi_n
    results["pisano_law12"] = (pi_n % 12 == 0) if pi_n > 0 else False

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

    # --- 7. Chebyshev chi_-3 character ---
    chi = chi3(n)
    results["chi3"] = chi
    results["chi3_label"] = ("+1 (≡1 mod 3)" if chi == 1
                             else ("-1 (≡2 mod 3)" if chi == -1 else "0 (≡0 mod 3)"))
    results["twin_prime"] = _is_twin_prime(n)

    # --- 8. Euler totient ---
    phi = totient_product_formula(n) if n > 0 else 0
    results["totient"] = phi
    results["totient_dr"] = digital_root(phi) if phi > 0 else 0
    results["totient_in_trinity"] = digital_root(phi) in TRINITY if phi > 0 else False
    results["totient_ratio"] = round(phi / n, 4) if n > 0 else 0

    # --- 9. Tribonacci DR position ---
    trib_pos, trib_val = _trib_position(n)
    results["trib_pos"] = trib_pos
    results["trib_val"] = trib_val
    results["trib_in_trinity"] = trib_val in TRINITY

    # --- 10. Prime classification ---
    prime = is_prime(n)
    dr7_prime = is_dr7_prime(n)
    results["is_prime"] = prime
    results["is_dr7_prime"] = dr7_prime

    # --- 11. Law of 12 ---
    results["law12_completion"] = (n % 12 == 0) and n > 0
    results["law12_tesla"] = is_tesla(n)

    # --- 12. Verdict (all axes) ---
    sovereign = in_trinity and res["trinity_visits"] == 24
    stable    = report["halt_check"] == "PASS"
    authorized = report["dac_check_status"] == "AUTHORIZED"
    lattice_aligned = lattice_dr in TRINITY

    # Count how many axes align
    axes_aligned = sum([
        in_trinity,
        sovereign,
        stable,
        authorized,
        lattice_aligned,
        fib_all_trinity,
        results["pisano_law12"],
        results["totient_in_trinity"],
        results["trib_in_trinity"],
        results["law12_tesla"],
    ])
    results["axes_aligned"] = axes_aligned

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


def scan_range(lo: int, hi: int) -> list:
    """
    Run every integer in [lo, hi] through the pipeline.
    Returns list of result dicts, sorted by axes_aligned descending.
    """
    results = []
    for n in range(lo, hi + 1):
        try:
            r = run_pipeline(n)
            results.append(r)
        except Exception:
            pass
    return sorted(results, key=lambda r: r["axes_aligned"], reverse=True)


def find_anchors(lo: int, hi: int, min_axes: int = 6) -> list:
    """
    Find all numbers in [lo, hi] where axes_aligned >= min_axes.
    These are structural anchor points — numbers special across many dimensions.
    """
    anchors = []
    for n in range(lo, hi + 1):
        try:
            r = run_pipeline(n)
            if r["axes_aligned"] >= min_axes:
                anchors.append(r)
        except Exception:
            pass
    return sorted(anchors, key=lambda r: r["axes_aligned"], reverse=True)


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
    print(f"  Fib all trinity:  {'YES' if r['fib_cycle_all_trinity'] else 'NO'}")
    print(f"  Pisano π({r['input']}):    {r['pisano_period']}  "
          f"{'(÷12 ✓)' if r['pisano_law12'] else ''}")
    print(f"\n  Lattice center:   {r['lattice_center']}  DR={r['lattice_dr']}"
          f"  {'(trinity)' if r['lattice_in_trinity'] else ''}")
    print(f"\n  G5 Structural:    {r['g5_structural']}")
    print(f"  G5 Temporal:      {r['g5_temporal']}")
    print(f"  G5 Halt:          {r['g5_halt']}")
    print(f"  G5 DAC:           {r['g5_dac']}")
    print(f"  G5 Insight:       {r['g5_insight']:,.2f}")
    print(f"\n  χ_-3 character:   {r['chi3_label']}")
    print(f"  Twin prime:       {'YES' if r['twin_prime'] else 'NO'}")
    print(f"\n  Totient φ({r['input']}):   {r['totient']}  (DR={r['totient_dr']}"
          f"{'  trinity' if r['totient_in_trinity'] else ''})")
    print(f"  φ/n ratio:        {r['totient_ratio']}")
    print(f"\n  Tribonacci DR:    pos={r['trib_pos']}  val={r['trib_val']}"
          f"  {'(trinity)' if r['trib_in_trinity'] else ''}")
    print(f"\n  Prime:            {'YES' if r['is_prime'] else 'NO'}"
          f"{'  [DR=7]' if r['is_dr7_prime'] else ''}")
    print(f"  Law of 12:        {'COMPLETE' if r['law12_completion'] else 'cycle'}  "
          f"Tesla={r['law12_tesla']}")
    print(f"\n  Axes aligned:     {r['axes_aligned']}/10")
    print(f"  VERDICT: {r['verdict']}")
    print("=" * 60)


if __name__ == "__main__":
    import sys
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 50
    print_pipeline(n)
