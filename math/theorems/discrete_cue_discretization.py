"""
DISCRETE CUE ON Z/m — m ∈ {9, 37, 333}
=============================================

The CUE_N eigenvalue joint density on the unit circle is proportional to

    P({θ_k}) ∝ ∏_{j<k} |e^{iθ_j} − e^{iθ_k}|²

DISCRETIZATION: Replace the continuous circle S¹ with Z/m = {0,…,m−1},
embedding k as z_k = exp(2πik/m). For a configuration S ⊆ Z/m the
discrete Vandermonde weight is

    W(S) = ∏_{j<k, j,k∈S} |exp(2πij/m) − exp(2πik/m)|²

Maximum-weight configurations are equally-spaced subsets (when n | m).

ORBITS UNDER ×2:
  m = 9:   ord_9(2) = 6   →  orbit of 1 is {1,2,4,5,7,8} (size 6)
             complementary orbit: {3,6} (size 2)
  m = 37:  ord_37(2) = 36  →  orbit of 1 = {1,…,36}  (primitive root)
  m = 333: 333 = 9×37; by CRT  Z/333 ≅ Z/9 × Z/37
             ord_333(2) = lcm(ord_9(2), ord_37(2)) = lcm(6, 36) = 36
             orbit of 1 has size 36; contains 167 = 2^35 mod 333

SPACING VARIANCE (normalized gaps, enforced mean = 1):
  CUE Wigner surmise (β=2, N→∞): var = 3π/8 − 1 ≈ 0.17810
  Z/9  orbit {1,2,4,5,7,8},  n=6:  var = 1/9       ≈ 0.11111  (alternating 2/3, 4/3)
  Z/37 full ×2 orbit,        n=36: var = 35/37²    ≈ 0.02557  (near-lattice)
  Z/333 ×2 orbit,            n=36: var = 755/37²   ≈ 0.55158  (clustered by powers of 2)

LOG-VANDERMONDE WEIGHTS (exact):
  log W({1,2,4,5,7,8}, 9)  = 9 log 3           ≈ 9.888  (W = 3^9 = 19683)
  log W({1,…,36},      37) = 35 log 37          ≈ 130.2  (W = 37^35, from m^{m-2} formula)

KLEIN CONNECTION:
  167 = 2^35 mod 333 links the ×2 iteration to the digit-rotation valid set
  {127,137,147,157,167,187,197} and the D4 Klein four-group analysis in
  digit_rotation_patterns.py.  The same 167 appears in 92837 + 73829 = 166666
  (six-sixes vortex) via the factorisation 166666 = 2 × 167 × 499.
"""

from typing import List

import numpy as np


# ---------------------------------------------------------------------------
# ORBITS UNDER ×2
# ---------------------------------------------------------------------------

def x2_orbit(m: int, start: int = 1) -> List[int]:
    """Return the ×2 orbit of `start` in Z/m (terminates when cycle closes)."""
    orbit: List[int] = []
    x = start % m
    seen: set = set()
    while x not in seen:
        seen.add(x)
        orbit.append(x)
        x = (2 * x) % m
    return orbit


def all_x2_orbits(m: int) -> List[List[int]]:
    """Partition Z/m \\ {0} into orbits under ×2 (0 is a fixed point)."""
    remaining = set(range(1, m))
    orbits: List[List[int]] = []
    while remaining:
        start = min(remaining)
        orb = x2_orbit(m, start)
        orbits.append(orb)
        remaining -= set(orb)
    return orbits


# ---------------------------------------------------------------------------
# LOG-VANDERMONDE WEIGHT
# ---------------------------------------------------------------------------

def log_vandermonde_weight(S: List[int], m: int) -> float:
    """
    Compute log W(S) = Σ_{j<k} 2·log|exp(2πij/m) − exp(2πik/m)| for S ⊆ Z/m.

    Uses logarithm to avoid overflow for large orbits (e.g. n=36 gives W ≈ 10^56).
    """
    zs = np.exp(2j * np.pi * np.array(S, dtype=float) / m)
    log_w = 0.0
    n = len(zs)
    for i in range(n):
        for j in range(i + 1, n):
            d = abs(zs[i] - zs[j])
            log_w += 2.0 * np.log(d)
    return float(log_w)


# ---------------------------------------------------------------------------
# SPACING STATISTICS
# ---------------------------------------------------------------------------

def spacing_stats(S: List[int], m: int) -> dict:
    """
    Compute normalized gap statistics for S ⊆ Z/m on the unit circle.

    Gaps are measured as arc lengths in [0, 2π], then divided by mean gap
    2π/|S| so that mean = 1 exactly.  Returns dict: spacings, mean, var,
    min, max, n.
    """
    n = len(S)
    angles = np.array(sorted(2.0 * np.pi * k / m for k in S))
    raw = np.diff(angles).tolist()
    raw.append(float(2.0 * np.pi - angles[-1] + angles[0]))  # wrap-around gap
    raw = np.array(raw)
    mean_gap = 2.0 * np.pi / n
    s = raw / mean_gap
    return {
        "spacings": s,
        "mean": float(s.mean()),
        "var": float(s.var()),
        "min": float(s.min()),
        "max": float(s.max()),
        "n": n,
    }


# ---------------------------------------------------------------------------
# EXACT ANALYTIC VARIANCES
# ---------------------------------------------------------------------------

# CUE β=2 Wigner surmise: P(s) = (32/π²)s² exp(−4s²/π), var = 3π/8 − 1
WIGNER_SURMISE_VAR: float = float(3 * np.pi / 8 - 1)  # ≈ 0.17810


def var_z9_exact() -> float:
    """
    Z/9 orbit {1,2,4,5,7,8}: gaps alternate 1 and 2 (in Z/9 units).
    Normalised spacings alternate 2/3 and 4/3; variance = 1/9.
    """
    # 3 gaps at 2/3, 3 gaps at 4/3
    s = np.array([2.0 / 3] * 3 + [4.0 / 3] * 3)
    return float(s.var())  # = 1/9 exactly


def var_z37_exact() -> float:
    """
    Z/37 full ×2 orbit (n=36): 35 gaps at 36/37, one gap at 72/37.
    Variance = 35/37² (maximum rigidity; 0 excluded → single double gap).
    """
    s = np.array([36.0 / 37] * 35 + [72.0 / 37])
    return float(s.var())  # = 35/37² exactly


def var_z333_exact() -> float:
    """
    Z/333 ×2 orbit (n=36): 36 gaps whose sum = 333 = 9×37.
    Mean gap = 333/36 = 37/4.
    Exact variance = 755/37² (derived from Σgap² = 4779 and gap mean = 37/4).
    """
    return float(755.0 / 37 ** 2)


# ---------------------------------------------------------------------------
# VERIFICATION
# ---------------------------------------------------------------------------

def run_verification() -> bool:
    print("=" * 70)
    print("DISCRETE CUE ON Z/m — VERIFICATION")
    print("=" * 70)

    # -----------------------------------------------------------------------
    # m = 9 : DR orbit
    # -----------------------------------------------------------------------
    print("\n--- m = 9 ---")
    orbits_9 = all_x2_orbits(9)
    print("  Orbits under ×2 in Z/9 \\ {0}:")
    for orb in orbits_9:
        print(f"    {sorted(orb)}  (size {len(orb)})")

    dr_orbit = sorted(x2_orbit(9, 1))
    assert set(dr_orbit) == {1, 2, 4, 5, 7, 8}, f"unexpected orbit: {dr_orbit}"
    assert len(dr_orbit) == 6

    stats_9 = spacing_stats(dr_orbit, 9)
    assert abs(stats_9["mean"] - 1.0) < 1e-12, f"mean ≠ 1: {stats_9['mean']}"
    assert abs(stats_9["var"] - 1.0 / 9) < 1e-12, f"var ≠ 1/9: {stats_9['var']}"
    print(f"  Spacings: {np.round(stats_9['spacings'], 4).tolist()}")
    print(f"  Variance: {stats_9['var']:.6f}  (exact: 1/9 = {1/9:.6f})")
    print(f"  CUE reference: {WIGNER_SURMISE_VAR:.6f}")

    log_w9 = log_vandermonde_weight(dr_orbit, 9)
    expected_log_w9 = 9.0 * np.log(3.0)  # W = 3^9 = 19683
    assert abs(log_w9 - expected_log_w9) < 1e-8, (
        f"log W ≠ 9 log 3: got {log_w9:.8f}, expected {expected_log_w9:.8f}"
    )
    print(f"  log W = {log_w9:.6f}  (exact: 9 log 3 = {expected_log_w9:.6f}  → W = 3^9 = 19683)")

    # -----------------------------------------------------------------------
    # m = 37 : primitive root orbit
    # -----------------------------------------------------------------------
    print("\n--- m = 37 ---")
    orbit_37 = sorted(x2_orbit(37, 1))
    assert len(orbit_37) == 36, f"period ≠ 36: {len(orbit_37)}"
    assert set(orbit_37) == set(range(1, 37)), "2 is not a primitive root mod 37"
    print(f"  ×2 orbit size: {len(orbit_37)} = φ(37)  (primitive root confirmed)")

    stats_37 = spacing_stats(orbit_37, 37)
    assert abs(stats_37["mean"] - 1.0) < 1e-12
    assert abs(stats_37["var"] - 35.0 / 37 ** 2) < 1e-12, (
        f"var ≠ 35/37²: {stats_37['var']:.8f}"
    )
    print(f"  Variance: {stats_37['var']:.6f}  (exact: 35/37² = {35/37**2:.6f})")
    print(f"  Gap pattern: 35 × {36/37:.4f}  +  1 × {72/37:.4f}  (0 excluded → double gap)")

    log_w37 = log_vandermonde_weight(orbit_37, 37)
    expected_log_w37 = 35.0 * np.log(37.0)  # W = 37^35 from m^{m-2} formula
    assert abs(log_w37 - expected_log_w37) < 1e-5, (
        f"log W ≠ 35 log 37: got {log_w37:.6f}, expected {expected_log_w37:.6f}"
    )
    print(f"  log W = {log_w37:.4f}  (exact: 35 log 37 = {expected_log_w37:.4f}  → W = 37^35)")

    # -----------------------------------------------------------------------
    # m = 333 : CRT composite orbit
    # -----------------------------------------------------------------------
    print("\n--- m = 333 = 9 × 37 ---")
    orbit_333_seq = x2_orbit(333, 1)
    assert len(orbit_333_seq) == 36, f"expected period 36, got {len(orbit_333_seq)}"
    assert pow(2, 35, 333) == 167, "2^35 mod 333 must equal 167"
    assert 167 in orbit_333_seq
    assert orbit_333_seq.index(167) == 35, "167 must be at orbit position k=35"
    print(f"  ×2 orbit size: 36 = lcm(ord_9(2), ord_37(2)) = lcm(6, 36)")
    print(f"  2^35 mod 333 = {pow(2, 35, 333)} = 167  (connects to digit-rotation valid set)")

    orbit_333 = sorted(orbit_333_seq)
    stats_333 = spacing_stats(orbit_333, 333)
    expected_var_333 = var_z333_exact()  # 755/37²
    assert abs(stats_333["mean"] - 1.0) < 1e-12
    assert abs(stats_333["var"] - expected_var_333) < 1e-8, (
        f"Z/333 var mismatch: {stats_333['var']:.8f} vs {expected_var_333:.8f}"
    )
    print(f"  Variance: {stats_333['var']:.6f}  (exact: 755/37² = {expected_var_333:.6f})")
    print(f"  Gap range: [{stats_333['min']:.4f}, {stats_333['max']:.4f}]")

    log_w333 = log_vandermonde_weight(orbit_333, 333)
    print(f"  log W = {log_w333:.4f}")

    # -----------------------------------------------------------------------
    # Sorted orbit (shows 167 in context)
    # -----------------------------------------------------------------------
    print(f"\n  Sorted Z/333 orbit (36 elements):")
    print(f"  {orbit_333}")

    # -----------------------------------------------------------------------
    # Summary table
    # -----------------------------------------------------------------------
    print("\n--- SPACING VARIANCE COMPARISON TABLE ---")
    print(f"  {'Configuration':<42} {'n':>4}  {'Var':>8}  {'Δ vs CUE':>10}")
    print(f"  {'-'*42} {'-'*4}  {'-'*8}  {'-'*10}")
    entries = [
        ("CUE / Wigner surmise (β=2, N→∞)", "∞",  WIGNER_SURMISE_VAR),
        ("Z/9  ×2 orbit  {1,2,4,5,7,8}",    6,    1.0 / 9),
        ("Z/37 full ×2 orbit (primitive root)", 36, 35.0 / 37 ** 2),
        ("Z/333 ×2 orbit  (CRT composite)",  36,   755.0 / 37 ** 2),
    ]
    for name, n_v, var in entries:
        delta = var - WIGNER_SURMISE_VAR
        n_str = str(n_v)
        print(f"  {name:<42} {n_str:>4}  {var:>8.5f}  {delta:>+10.5f}")

    print()
    print("  Interpretation:")
    print("    Z/37 (primitive root): near-lattice rigidity   — var << CUE")
    print("    Z/9  (DR orbit):       intermediate rigidity   — var < CUE")
    print("    CUE:                   universal repulsion     — benchmark")
    print("    Z/333 (CRT composite): clustered (powers of 2) — var >> CUE")
    print()
    print("  167 ∈ Z/333 orbit (at k=35) links ×2-iteration to:")
    print("    • Digit-rotation valid set {127,…,197}")
    print("    • D4 Klein four-group K4 < D4 (digit_rotation_patterns.py)")
    print("    • Six-sixes vortex: 166666 = 2 × 167 × 499")
    print()
    print("All assertions passed.")
    return True


if __name__ == "__main__":
    run_verification()
