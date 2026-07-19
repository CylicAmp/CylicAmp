#!/usr/bin/env python3
"""
Twin Prime 3-adic Saturation Witness — MSW Framework Layer
===========================================================
WITNESS_VERSION: v4_saturation_30M

Tracks how twin prime pairs fill residue cosets as the hierarchy
level k increases through the 3-adic tower.

3-adic hierarchy (two 3-digits per level):
  level k  |  modulus M_k = 9^(k+1)  |  cosets/type = 9^k
  ─────────┼─────────────────────────┼───────────────────
  k=0      |  9                      |  1   (type itself)
  k=1      |  81                     |  9
  k=2      |  729                    |  81
  k=3      |  6 561                  |  729
  k=4      |  59 049  (= 3^10)       |  6 561

Types (by DR(p) of the twin prime p-side):
  A: DR(p) = 2  →  p ≡ 2 (mod 9)
  B: DR(p) = 5  →  p ≡ 5 (mod 9)
  C: DR(p) = 8  →  p ≡ 8 (mod 9)

CERTIFIED RESULTS at k=4, N=30_000_000 (v4_saturation_30M):
  Type A: 6561/6561  ρ_4 = 1.000   COMPLETE
  Type B: 6559/6561  ρ_4 ≈ 0.9997  CERTIFIED_INCOMPLETE  gaps=2
  Type C: 6559/6561  ρ_4 ≈ 0.9997  CERTIFIED_INCOMPLETE  gaps=2
  FAIL_CLOSED_ABOVE: N=30M for ρ_4=1 on all types
  HEURISTIC_N*_all_types_6561: ~3.5×10^7  (UNVERIFIED)

Identified gap cosets (r = p mod 59049, unfilled at N=30M):
  B: [31640, 43439]   (31640 ≡ 5 mod 9, 43439 ≡ 5 mod 9  ✓)
  C: [21716, 41345]   (21716 ≡ 8 mod 9, 41345 ≡ 8 mod 9  ✓)

Refinement ratio (parent→child, k=3→k=4, at N=5M):
  A: 7.528   B: 7.451   C: 7.455   mean ≈ 7.48
  Naive 9× assumption fails at this depth/window.

© 2026 Michael Warren Song. All Rights Reserved.
"""

import numpy as np

# ── Certified 30M constants ────────────────────────────────────

CERTIFIED = {
    'version':  'v4_saturation_30M',
    'k':        4,
    'modulus':  59049,         # 3^10 = 9^5
    'N':        30_000_000,
    'A': {'filled': 6561, 'total': 6561, 'rho': 1.0,       'complete': True,  'gaps': []},
    'B': {'filled': 6559, 'total': 6561, 'rho': 6559/6561, 'complete': False, 'gaps': [31640, 43439]},
    'C': {'filled': 6559, 'total': 6561, 'rho': 6559/6561, 'complete': False, 'gaps': [21716, 41345]},
    'heuristic_N_star': 35_000_000,   # UNVERIFIED
    'refinement_5M':    7.478,        # mean k=3→k=4 ratio at 5M
    'refinement_naive': 9.0,
}

# Gap cosets satisfy their type's base residue mod 9
assert all(r % 9 == 5 for r in CERTIFIED['B']['gaps'])
assert all(r % 9 == 8 for r in CERTIFIED['C']['gaps'])


# ── Core arithmetic ────────────────────────────────────────────

def sieve_twins(N: int) -> np.ndarray:
    """Return array of p where (p, p+2) are both prime, p ≤ N."""
    sv = np.ones(N + 3, dtype=bool)
    sv[0] = sv[1] = False
    for i in range(2, int(N**0.5) + 1):
        if sv[i]:
            sv[i * i::i] = False
    return np.where(sv[:-2] & sv[2:])[0]


def classify(twins: np.ndarray) -> dict:
    """Return boolean mask for each type {A,B,C}."""
    dr = 1 + (twins - 1) % 9
    return {'A': dr == 2, 'B': dr == 5, 'C': dr == 8}


# ── Saturation sweep ───────────────────────────────────────────

def saturation_sweep(twins: np.ndarray, max_level: int = 4) -> dict:
    """
    Compute ρ_k (filled fraction) for levels k=1..max_level and types A/B/C.

    Returns:
        {k: {'A': {'filled':int,'total':int,'rho':float,'gaps':int}, ...}}
    """
    masks = classify(twins)
    results = {}
    for k in range(1, max_level + 1):
        mod   = 9 ** (k + 1)
        total = 9 ** k
        results[k] = {}
        for t, m in masks.items():
            filled = int(np.unique(twins[m] % mod).size)
            results[k][t] = {
                'filled': filled,
                'total':  total,
                'rho':    filled / total,
                'gaps':   total - filled,
            }
    return results


def find_gaps(twins: np.ndarray, k: int = 4) -> dict:
    """
    Identify the specific unfilled cosets at level k for each type.

    Returns:
        {'A': [list of unfilled r], 'B': [...], 'C': [...]}
    """
    mod   = 9 ** (k + 1)
    masks = classify(twins)
    BASE  = {'A': 2, 'B': 5, 'C': 8}
    result = {}
    for t, m in masks.items():
        filled_set = set(twins[m] % mod)
        all_cosets = set(range(BASE[t], mod, 9))
        result[t]  = sorted(all_cosets - filled_set)
    return result


def refinement_ratio(twins: np.ndarray, N_obs: int, k_from: int = 3, k_to: int = 4) -> dict:
    """
    Compute the empirical parent→child fill ratio at level k_from→k_to,
    evaluated at twins ≤ N_obs.

    Naive expectation: 9 (each parent coset splits into 9 children,
    all filled simultaneously). Empirical value < 9 at finite N.
    """
    sub   = twins[twins <= N_obs]
    masks = classify(sub)
    ratios = {}
    for t, m in masks.items():
        p_t = sub[m]
        f_from = int(np.unique(p_t % 9 ** (k_from + 1)).size)
        f_to   = int(np.unique(p_t % 9 ** (k_to   + 1)).size)
        ratios[t] = f_to / f_from if f_from else 0.0
    ratios['mean'] = sum(v for k, v in ratios.items() if k != 'mean') / 3
    return ratios


# ── Full report ────────────────────────────────────────────────

def run(N: int = 5_000_000, show_certified: bool = True):
    print("=" * 65)
    print("  TWIN PRIME 3-ADIC SATURATION WITNESS — MSW Framework")
    print(f"  WITNESS_VERSION: {CERTIFIED['version']}")
    print("  © 2026 Michael Warren Song")
    print("=" * 65)
    print()

    twins = sieve_twins(N)
    masks = classify(twins)
    print(f"  Computing up to N = {N:,}")
    print(f"  Twin prime pairs: {len(twins):,}")
    for t, m in masks.items():
        print(f"    Type {t} (DR(p)={2 if t=='A' else 5 if t=='B' else 8}):  {m.sum():,}")
    print()

    # Saturation sweep
    sweep = saturation_sweep(twins)
    print(f"  {'k':>2}  {'mod':>7}  {'cosets':>7}  "
          f"{'A filled':>9}  {'B filled':>9}  {'C filled':>9}  "
          f"{'gaps A':>7}  {'gaps B':>7}  {'gaps C':>7}")
    print("  " + "─" * 77)
    for k, res in sweep.items():
        mod   = 9 ** (k + 1)
        total = 9 ** k
        print(f"  {k:>2}  {mod:>7,}  {total:>7,}  "
              f"{res['A']['filled']:>9,}  {res['B']['filled']:>9,}  {res['C']['filled']:>9,}  "
              f"{res['A']['gaps']:>7}  {res['B']['gaps']:>7}  {res['C']['gaps']:>7}")
    print()

    # Refinement ratio
    ratios = refinement_ratio(twins, N_obs=min(5_000_000, N))
    print(f"  REFINEMENT RATIO k=3→k=4 (at N={min(5_000_000,N):,}):")
    for t in 'ABC':
        print(f"    Type {t}: {ratios[t]:.3f}")
    print(f"    Mean:   {ratios['mean']:.3f}  (naive 9× expected)")
    print()

    # Gap identification at k=4 if N is large enough
    gaps = find_gaps(twins, k=4)
    print("  UNFILLED COSETS AT k=4 (r = p mod 59049):")
    for t in 'ABC':
        g = gaps[t]
        print(f"    Type {t}: {len(g)} gap(s)  {g if len(g) <= 10 else str(g[:10])+'...'}")
    print()

    # Certified results comparison
    if show_certified:
        print("  CERTIFIED RESULTS (N=30M, v4_saturation_30M):")
        for t in 'ABC':
            c = CERTIFIED[t]
            print(f"    Type {t}: {c['filled']}/{c['total']}  ρ_4={c['rho']:.6f}  "
                  f"{'COMPLETE' if c['complete'] else f'gaps={c[\"gaps\"]}'}")
        print()
        print("  FAIL_CLOSED_ABOVE: N=30M for ρ_4=1 on all types")
        print(f"  HEURISTIC_N*: ~{CERTIFIED['heuristic_N_star']:,}  (UNVERIFIED)")
        print(f"  Certified gap cosets (N=30M):")
        print(f"    B: {CERTIFIED['B']['gaps']}")
        print(f"    C: {CERTIFIED['C']['gaps']}")
    print()
    print("=" * 65)

    return {
        'twins':  twins,
        'sweep':  sweep,
        'gaps':   gaps,
        'ratios': ratios,
    }


if __name__ == "__main__":
    run()
