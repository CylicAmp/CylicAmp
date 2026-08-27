#!/usr/bin/env python3
"""
GF(37) Riemann Zero Coverage Algorithm
Author: Michael Warren Song (CyclicAmp)

Tests: floor(gamma_n) mod 37 against the complete 12-orbit partition of GF(37)*.

THEOREM: For every nontrivial Riemann zero 1/2 + i*gamma_n,
  floor(gamma_n) mod 37 lands in one of the 12 named orbits or SEAM.
  Coverage is 100% for ALL zeros. No misses are possible.

REQUIRES: mpmath  (pip install mpmath)

USAGE:
  python3 riemann_gf37_coverage.py              # test first 100 zeros
  python3 riemann_gf37_coverage.py 500          # test first 500 zeros
  python3 riemann_gf37_coverage.py 1000         # test first 1000 zeros
  python3 riemann_gf37_coverage.py 100 400      # test zeros 100 through 400
  python3 riemann_gf37_coverage.py --precision 30 1000  # higher precision
"""

import sys
import mpmath

# ── GF(37) framework constants ───────────────────────────────────────────────

P    = 37
MULT = 26   # 137 mod 37 — the 137-map multiplier

# 12 disjoint 3-cycles that partition GF(37)* = {1..36}
# Every nonzero residue mod 37 belongs to exactly one of these.
ORBITS = {
    'IC':      frozenset({1, 10, 26}),   # Identity Cycle; 26=multiplier, 10=alpha
    'DARK_A':  frozenset({2, 15, 20}),   # Primitive root 2; ord_37(2)=36
    'C3':      frozenset({3, 4, 30}),    # 3∈ST, 4∈SA, 30∈SA∩ST (double-sovereign)
    'CAS_EXT': frozenset({5, 13, 19}),   # 13∈CASCADE; 19=2^{-1}=critical line
    'TESLA':   frozenset({6, 8, 23}),    # 6=first perfect divisor; 8∈CASCADE
    'D7':      frozenset({7, 33, 34}),   # 33=prime index of 137; 7 prime
    'SA_ST_A': frozenset({9, 12, 16}),   # 9∈SA, 12∈ST; 16=2^4
    'NEG_H':   frozenset({11, 27, 36}),  # 36=-1 mod 37; negation orbit
    'C9':      frozenset({14, 29, 31}),  # floor(gamma_1)=14 lives here
    'NQR17':   frozenset({17, 22, 35}),  # all non-quadratic-residues
    'SEED':    frozenset({18, 24, 32}),  # orbit of seed 246; c mod 37=32
    'SA_ST_B': frozenset({21, 25, 28}),  # 21∈ST, 25∈SA
}

# SEAM: residue 0 (floor = exact multiple of 37). Expected ~2.7% of zeros.

# Sanity: verify partition
_union = set()
for _orb in ORBITS.values():
    assert len(_orb) == 3
    _union |= _orb
assert _union == set(range(1, P)), "ORBITS must partition {1..36}"


def orbit_label(r):
    """Return the orbit name for residue r mod 37."""
    r = r % P
    if r == 0:
        return 'SEAM'
    for name, orb in ORBITS.items():
        if r in orb:
            return name
    return 'UNKNOWN'   # impossible by partition theorem


def compute_zeros(start, end, dps=15):
    """
    Compute floor(gamma_n) mod 37 for zeros n in [start, end].
    Returns list of (n, gamma, floor, residue, orbit_label).
    """
    mpmath.mp.dps = dps
    results = []
    for n in range(start, end + 1):
        z = mpmath.zetazero(n)
        gamma = float(mpmath.im(z))
        f = int(gamma)           # floor
        r = f % P
        label = orbit_label(r)
        results.append((n, gamma, f, r, label))
    return results


def run(start=1, end=100, dps=15, verbose=False):
    """
    Run the coverage test and print results.
    """
    N = end - start + 1
    print(f"{'='*60}")
    print(f"GF(37) Riemann Zero Coverage")
    print(f"Zeros {start} to {end}  (N={N})  precision={dps} dps")
    print(f"{'='*60}")

    results = compute_zeros(start, end, dps)

    counts = {}
    misses = []
    seam_list = []

    for n, gamma, f, r, label in results:
        counts[label] = counts.get(label, 0) + 1
        if label == 'UNKNOWN':
            misses.append((n, gamma, f, r))
        if label == 'SEAM':
            seam_list.append((n, gamma, f))

    # Print each zero in verbose mode
    if verbose:
        print()
        print(f"  {'n':>5}  {'gamma':>12}  {'floor':>6}  {'r':>3}  orbit")
        print(f"  {'-'*5}  {'-'*12}  {'-'*6}  {'-'*3}  -----")
        for n, gamma, f, r, label in results:
            seam_tag = ' ← SEAM (floor divisible by 37)' if label == 'SEAM' else ''
            print(f"  {n:>5}  {gamma:>12.6f}  {f:>6}  {r:>3}  {label}{seam_tag}")

    # Summary
    print()
    print(f"Result: {N - len(misses)}/{N} covered  ({len(misses)} misses)")
    print(f"SEAM hits: {len(seam_list)}  ({len(seam_list)/N*100:.1f}%)")
    print()
    print("Orbit distribution:")
    print(f"  {'orbit':<10}  {'count':>5}  {'%':>6}  elements")
    print(f"  {'-'*10}  {'-'*5}  {'-'*6}  --------")
    for name, count in sorted(counts.items(), key=lambda x: -x[1]):
        elements = sorted(ORBITS[name]) if name != 'SEAM' else [0]
        pct = count / N * 100
        print(f"  {name:<10}  {count:>5}  {pct:>5.1f}%  {elements}")

    if misses:
        print()
        print(f"MISSES ({len(misses)}):")
        for n, gamma, f, r in misses:
            print(f"  gamma_{n} = {gamma:.6f}  floor={f}  r={r}")
    else:
        print()
        print("No misses. Every zero maps to a named orbit.")

    # Notable zeros
    print()
    print("Notable orbit assignments (first few named zeros):")
    seen = set()
    for n, gamma, f, r, label in results:
        if label not in seen and label != 'SEAM':
            seen.add(label)
            print(f"  gamma_{n} = {gamma:.4f}  floor={f}  mod37={r}  → {label}")
        if len(seen) >= 6:
            break

    return {
        'start': start,
        'end': end,
        'N': N,
        'misses': len(misses),
        'coverage': (N - len(misses)) / N,
        'seam_count': len(seam_list),
        'counts': counts,
    }


if __name__ == "__main__":
    # Parse arguments
    args = sys.argv[1:]
    dps = 15
    verbose = False

    if '--verbose' in args:
        verbose = True
        args = [a for a in args if a != '--verbose']
    if '--precision' in args:
        idx = args.index('--precision')
        dps = int(args[idx + 1])
        args = [a for a in args if a != '--precision' and a != args[idx + 1]]

    numeric = [int(a) for a in args if a.lstrip('-').isdigit()]

    if len(numeric) == 0:
        start, end = 1, 100
    elif len(numeric) == 1:
        start, end = 1, numeric[0]
    else:
        start, end = numeric[0], numeric[1]

    run(start=start, end=end, dps=dps, verbose=verbose)
