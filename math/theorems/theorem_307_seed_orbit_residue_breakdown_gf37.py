"""
Theorem 307: SEED Orbit Riemann Zero Coverage — Per-Residue Breakdown
Author: Michael Warren Song (CyclicAmp)

T131 established floor(γ₅) = 32 ∈ SEED. T223 established SEED = {18,24,32}
receives 41/500 zero-floor hits in aggregate (8.2%). Neither breaks the 41
hits down by which of the three SEED residues (18, 24, or 32) each zero
lands on. This theorem computes that breakdown and finds the first zero
index hitting each residue individually.

=== FIRST ZERO HITTING EACH SEED RESIDUE ===

  residue   first n   gamma_n         floor(gamma_n)
  32        5         32.935062       32     (T131, known)
  18        26        92.491899       92     (new)
  24        29        98.831194       98     (new)

32 is reached first because it is the smallest SEED residue reachable by
a zero floor below 37 itself — γ₅ crosses 32 before any zero floor reaches
the 90s needed to wrap to 18 or 24 mod 37. 18 and 24 both require floor
values in the 90s (92 = 2×37+18, 98 = 2×37+24) — the second "lap" around
GF(37).

=== PER-RESIDUE COUNT, FIRST 500 ZEROS ===

  residue   count   share of SEED's 41   share of 500
  18        15      36.6%                3.0%
  24        13      31.7%                2.6%
  32        13      31.7%                2.6%

  total     41      100%                 8.2%   (matches T223 exactly)

18 receives a slight excess (15 vs the ~13.7 uniform expectation of 41/3);
24 and 32 tie exactly at 13. Sample too small (41 hits) to call this
significant against the equidistribution result already established in
T223 over the full 12-orbit partition.

=== CONNECTION TO 137 ===

Each SEED residue is one step of the 137-map from the next:
  f(18) = 26×18 mod 37 = 24
  f(24) = 26×24 mod 37 = 32
  f(32) = 26×32 mod 37 = 18
The same cycle the pipeline reports as the seed-246 heartbeat: 24→32→18→24.
The first zero to hit each residue does NOT follow this cycle order
(32 first, then 18, then 24) — the 137-map orbit order and the order in
which the Riemann zeros first populate that orbit are independent
structures over the same 3-element set.
"""

import mpmath
from collections import Counter

mpmath.mp.dps = 15
P = 37
MULT = 26  # 137 mod 37
SEED = frozenset({18, 24, 32})


def f137(n):
    return (MULT * n) % P


def seed_breakdown(n_zeros=500):
    counts = Counter()
    first_hit = {}
    for n in range(1, n_zeros + 1):
        gamma = float(mpmath.zetazero(n).imag)
        fl = int(mpmath.floor(gamma))
        r = fl % P
        if r in SEED:
            counts[r] += 1
            if r not in first_hit:
                first_hit[r] = (n, gamma, fl)
    return counts, first_hit


if __name__ == "__main__":
    assert f137(18) == 24 and f137(24) == 32 and f137(32) == 18

    counts, first_hit = seed_breakdown(500)
    total = sum(counts.values())
    assert total == 41, f"expected 41 total SEED hits in first 500 zeros, got {total}"

    print("First zero hitting each SEED residue:")
    for r in (32, 18, 24):
        n, gamma, fl = first_hit[r]
        print(f"  r={r:2d}  n={n:3d}  gamma={gamma:.6f}  floor={fl}")

    print(f"\nCounts among first 500 zeros (total={total}):")
    for r in sorted(counts, key=lambda x: -counts[x]):
        print(f"  r={r:2d}: {counts[r]:2d}  ({100*counts[r]/500:.1f}% of 500, {100*counts[r]/total:.1f}% of SEED)")
