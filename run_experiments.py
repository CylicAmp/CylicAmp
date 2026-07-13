"""
CylicAmp Experiment Runner

Runs all verified experiments using the existing module stack,
then applies the full pipeline to discover structural anchor points.
"""
import time
import math

from cylicamp.euler_totient import totient_product_formula, rsa_demo
from cylicamp.chebyshev_bias import demonstrate as chebyshev_demo, _sieve, chi3
from cylicamp.pipeline import print_pipeline, find_anchors, scan_range
from cylicamp.tribonacci_dr import CYCLE as TRIB_CYCLE, show_cycle_grid, show_triples
from cylicamp.prime_visual import find_dr7_primes, grid_display
from cylicamp.law_of_12 import demonstrate as law12_demo
from cylicamp.time_dr import run_analysis as time_dr_analysis
from cylicamp.cycle_triples import analyze_triples, CYCLE as MASTER_CYCLE
from cylicamp.diff_geometry import run_tests, run_tensor_tests


def verify_totient(n_max: int = 40) -> bool:
    """Cross-check product formula against GCD count for n=1..n_max."""
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    for n in range(1, n_max + 1):
        phi_formula  = totient_product_formula(n)
        phi_iterative = sum(1 for i in range(1, n + 1) if gcd(i, n) == 1)
        if phi_formula != phi_iterative:
            print(f"  MISMATCH at n={n}: formula={phi_formula}, iterative={phi_iterative}")
            return False
    return True


def analyze_twin_primes(limit: int = 1_000_000) -> None:
    """Twin prime modular bias analysis (uses existing sieve)."""
    print(f"  Running sieve up to {limit:,}...")
    S = _sieve(limit)

    twin_count = 0
    mod3 = {0: 0, 1: 0, 2: 0}
    mod4 = {1: 0, 3: 0}

    for p in range(3, limit - 1, 2):
        if S[p] and S[p + 2]:
            twin_count += 1
            mod3[p % 3] += 1
            if p % 4 in mod4:
                mod4[p % 4] += 1

    print(f"  Found {twin_count:,} twin prime pairs")
    print(f"  Mod-3 distribution: {mod3}")
    print(f"  Twin primes p ≡ 1 (mod 4): {mod4[1]:,}")
    print(f"  Twin primes p ≡ 3 (mod 4): {mod4[3]:,}")
    violations = mod3[0] + mod3[1]
    print(f"  Violations of p≡2(mod3): {violations}  "
          f"{'STRUCTURAL NECESSITY CONFIRMED' if violations == 0 else 'FAILED'}")


def show_37_field() -> None:
    """Scan the full 37-field (n=1..37) and map every dimension."""
    from cylicamp.core import digital_root
    from cylicamp.prime_visual import is_prime, is_dr7_prime
    from cylicamp.chebyshev_bias import chi3
    from cylicamp.euler_totient import totient_product_formula
    from cylicamp.law_of_12 import is_tesla

    print(f"\n{'n':>3}  DR  Trinity  Prime  DR7P  χ₋₃  φ(n)  φ-DR  Tesla  Trib")
    print("-" * 58)
    for n in range(1, 38):
        dr    = digital_root(n)
        tri   = "Y" if dr in {3,6,9} else "."
        prime = "P" if is_prime(n) else "."
        dr7   = "[7]" if is_dr7_prime(n) else "   "
        chi   = f"{chi3(n):+d}" if chi3(n) != 0 else " 0"
        phi   = totient_product_formula(n)
        phi_dr = digital_root(phi)
        tesla  = "T" if is_tesla(n) else "."
        trib_v = TRIB_CYCLE[(n-1) % 39]
        trib_t = "T" if trib_v in {3,6,9} else "."
        print(f"{n:>3}  {dr:>2}  {tri:^7}  {prime:^5}  {dr7}  "
              f"{chi}  {phi:>4}  {phi_dr:>4}  {tesla:^5}  {trib_v}({trib_t})")


def solve_anchor_search(lo: int, hi: int, min_axes: int = 6) -> None:
    """
    THE PROBLEM SOLVER.

    Find all numbers in [lo, hi] that satisfy >= min_axes simultaneous
    structural constraints. These are anchor points where the system's
    logic converges.
    """
    print(f"\n  Scanning {lo}..{hi} for structural anchors (≥{min_axes}/10 axes)...")
    t0 = time.perf_counter()
    anchors = find_anchors(lo, hi, min_axes)
    t1 = time.perf_counter()

    if not anchors:
        print(f"  No anchors found at threshold {min_axes}.")
        return

    print(f"  Found {len(anchors)} anchors in {t1-t0:.3f}s\n")
    print(f"  {'n':>4}  {'DR':>2}  {'Tri':>3}  {'φ(n)':>5}  "
          f"{'π(n)':>6}  {'Trib':>4}  {'Axes':>4}  Verdict")
    print("  " + "-" * 68)

    for r in anchors:
        n    = r["input"]
        dr   = r["digital_root"]
        tri  = "YES" if r["trinity"] else " no"
        phi  = r["totient"]
        pi   = r["pisano_period"]
        trib = r["trib_val"]
        axes = r["axes_aligned"]
        verd = r["verdict"].split("—")[0].strip()
        print(f"  {n:>4}  {dr:>2}  {tri:>3}  {phi:>5}  "
              f"{pi:>6}  {trib:>4}  {axes:>4}  {verd}")

    # Summary by verdict category
    print()
    categories = {}
    for r in anchors:
        cat = r["verdict"].split("—")[0].strip()
        categories.setdefault(cat, []).append(r["input"])
    for cat, nums in sorted(categories.items()):
        print(f"  {cat}: {nums}")


def show_tribonacci() -> None:
    """Tribonacci DR cycle analysis."""
    print(f"  Period-39 cycle: {TRIB_CYCLE}")
    print(f"  Length: {len(TRIB_CYCLE)}")
    trinity_pos = [i+1 for i, v in enumerate(TRIB_CYCLE) if v in {3,6,9}]
    print(f"  Trinity positions (1-indexed): {trinity_pos}")
    print(f"  Trinity density: {len(trinity_pos)}/{len(TRIB_CYCLE)} = "
          f"{len(trinity_pos)/len(TRIB_CYCLE)*100:.1f}%")
    show_cycle_grid(TRIB_CYCLE, 13)
    print()
    show_triples(TRIB_CYCLE, 6)


def show_cycle_triples() -> None:
    """Master cycle triple window analysis."""
    print(f"  Master cycle (len={len(MASTER_CYCLE)}): {MASTER_CYCLE}")
    print()
    for a, b, c, s, d in analyze_triples(MASTER_CYCLE, 10):
        tri = " (trinity)" if d in {3,6,9} else ""
        print(f"  {a}+{b}+{c} = {s} → DR {d}{tri}")


def show_dr7_primes() -> None:
    """DR=7 prime distribution up to 300."""
    dr7 = find_dr7_primes(300)
    print(f"  DR=7 primes up to 300: {len(dr7)} found")
    print(f"  List: {dr7}")
    gaps = [dr7[i] - dr7[i-1] for i in range(1, len(dr7))]
    avg_gap = sum(gaps) / len(gaps)
    print(f"  Average gap: {avg_gap:.2f}")
    print(f"  Max gap: {max(gaps)}  Min gap: {min(gaps)}")
    grid_display(limit=100, width=10)


def main():
    print("=" * 60)
    print("  CYLICAMP EXPERIMENT RUNNER")
    print("=" * 60)

    # --- [1] Totient verification ---
    print("\n[1] TOTIENT & RSA VERIFICATION")
    print("-" * 40)
    t0 = time.perf_counter()
    ok = verify_totient(40)
    t1 = time.perf_counter()
    if ok:
        print(f"  Product formula matches GCD count for n=1..40  ✓")
    print(f"  Time: {(t1-t0)*1000:.2f}ms")
    rsa_demo(p=61, q=53)

    # --- [2] Twin prime bias ---
    print("\n[2] TWIN PRIME BIAS ANALYSIS")
    print("-" * 40)
    t0 = time.perf_counter()
    analyze_twin_primes(limit=1_000_000)
    t1 = time.perf_counter()
    print(f"  Time: {t1-t0:.4f}s")

    # --- [3] Chebyshev bias (full) ---
    print("\n[3] CHEBYSHEV BIAS (full report)")
    print("-" * 40)
    t0 = time.perf_counter()
    chebyshev_demo(limit=1_000_000)
    t1 = time.perf_counter()
    print(f"\n  Time: {t1-t0:.4f}s")

    # --- [4] Pipeline on key numbers ---
    print("\n[4] PIPELINE: KEY NUMBERS")
    print("-" * 40)
    for n in [3, 9, 37, 432, 419]:
        print_pipeline(n)

    # --- [5] 37-Field map ---
    print("\n[5] 37-FIELD STRUCTURAL MAP (n=1..37)")
    print("-" * 40)
    show_37_field()

    # --- [6] DR=7 prime simulation ---
    print("\n[6] DR=7 PRIME SIMULATION")
    print("-" * 40)
    show_dr7_primes()

    # --- [7] Tribonacci DR cycle ---
    print("\n[7] TRIBONACCI DR CYCLE (period 39)")
    print("-" * 40)
    show_tribonacci()

    # --- [8] Cycle triples ---
    print("\n[8] MASTER CYCLE TRIPLE ANALYSIS")
    print("-" * 40)
    show_cycle_triples()

    # --- [9] Law of 12 ---
    print("\n[9] LAW OF 12: UNIVERSAL CYCLE COMPLETION")
    print("-" * 40)
    law12_demo()

    # --- [10] Time DR ---
    print("\n[10] TIME DIGITAL ROOT — 21:42 ANALYSIS")
    print("-" * 40)
    time_dr_analysis()

    # --- [11] Differential geometry ---
    print("\n[11] DIFFERENTIAL GEOMETRY VERIFICATION")
    print("-" * 40)
    run_tests()
    run_tensor_tests()

    # --- [12] THE PROBLEM SOLVER ---
    print("\n[12] PROBLEM SOLVER: STRUCTURAL ANCHOR SEARCH")
    print("=" * 60)
    print("  QUESTION: Which numbers are simultaneously special")
    print("  across the most dimensions of the logic system?")
    print("=" * 60)

    # Scan 1-100 at threshold 6
    print("\n  --- Anchors in 1..100 (axes ≥ 6) ---")
    solve_anchor_search(1, 100, min_axes=6)

    # Scan the key numbers explicitly
    print("\n  --- Key numbers: 3, 9, 12, 37, 108, 419, 432 ---")
    key_nums = [3, 9, 12, 37, 108, 419, 432]
    for n in key_nums:
        from cylicamp.pipeline import run_pipeline
        r = run_pipeline(n)
        flags = []
        if r["trinity"]:     flags.append("trinity")
        if r["is_prime"]:    flags.append("prime")
        if r["is_dr7_prime"]: flags.append("DR7P")
        if r["twin_prime"]:  flags.append("twin")
        if r["law12_completion"]: flags.append("12-complete")
        if r["pisano_law12"]: flags.append("π÷12")
        if r["trib_in_trinity"]: flags.append("trib-T")
        if r["totient_in_trinity"]: flags.append("φ-T")
        flag_str = "  ".join(flags) if flags else "—"
        print(f"\n  n={n}  DR={r['digital_root']}  axes={r['axes_aligned']}/10")
        print(f"  Flags: {flag_str}")
        print(f"  Verdict: {r['verdict']}")

    print("\n" + "=" * 60)
    print("  ALL EXPERIMENTS COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
