# CLASS: AUDIT
"""
The pasted JSON bundle ("derived_from": "verified_data_bundle", generated 2026-03-22) and its "Key findings" table:
mod 37 structure, twin-prime counts, the G5 solver's SSR, powers of 2, the D7 frequencies, digital roots of the
first 100 primes -- and the owner's question with it, "see if this failure is telling us something important as
well" (owner_work #425, 2026-10-23). Audit on arrival. The walk to 100,000,000,000 asked in the same message is in
owner_engine_walk_100b_2026_10_23.py.

THE PASTE: a data bundle and a summary from another tool, relayed by the owner. Nothing below puts a claim of it in
the owner's mouth.

RIGHT (re-run):
  2 is a primitive root, phi = 36, its divisors; the whole discrete-log table (36 entries); all 9 subgroups with
  their generators and elements; the roots of x x + x + 1 are 10 = 2^24 and 26 = 2^12
  3,424,506 twin pairs below 10^9 (the walk to 500,000,000); C2 = 0.6601618...; density 0.003424506
  the G5 sweep counts (2 4 6 8 10 20 40 kept points; 8 kept at 144 steps) and SSR 0; 1.3824^144 = 1.783431e20
  powers of 2 by 9 (1 2 4 8 7 5), by 37 (all 36), by 72 (1 2 4 8 16 32 64 56 40, then 8 16 32 64 56 40 again)
  the D7 arithmetic: 429.914 - 339.932 = 89.982; / phi = 210.09, 265.70, 55.61; 406.6 cents; 26.47%
  the first 100 primes (2 to 541); 16 of them have root 7

WRONG -- each changes a number:
  1. The order-6 Cayley table: 20 of its 36 cells are wrong (10 x 11 = 110 = 2 x 37 + 36 -> 36, not 1;
     10 x 26 = 260 -> 1, not 11; row 26 has 1 twice, which no group table can). The right table is asserted below.
  2. "expected_pairs_approx 1,537,213" and "observed/expected 2.2277": the estimate dropped a factor 2. The
     twin-prime estimate is 2 x C2 x N / (ln N)^2 = 3,074,426 (ratio 1.114), and its sharper form
     2 x C2 x (the sum of 1 / (ln t)^2 from 2 to N) = 3,425,308 -- the actual 3,424,506 is 0.99977 of it, 0.02% off.
     So observed and expected agree; there is no 2.23.
  3. "brun_partial_to_1e9_approx 1.8228": the sum of 1/p + 1/(p + 2) over the twin pairs below 10^9 is 1.77474.
  4. "average_gap_between_pairs 291.98": 10^9 / 3,424,506 = 292.01.
  5. "filtered_distances_sample" at steps 37 and 38: 1.3824^37 = 159,752.6 and 1.3824^38 = 220,841.9 (the paste
     has 184,467.4 and 255,008.8).
  6. The digital roots of the first 100 primes: the paste's 14 16 2 16 15 1 16 14 6 (roots 1..9) are wrong except the
     16 at root 7. The right counts: root 1: 16, 2: 18, 3: 1 (the prime 3), 4: 15, 5: 18, 6: 0, 7: 16, 8: 16, 9: 0.
     No prime has root 6 or 9 -- the paste's own "observation" line says so and its table has 7 of them.
  7. "dr_7_percentage 16.0 vs expected_uniform 11.11": the wrong baseline. Primes above 3 only have roots
     1 2 4 5 7 8, so the even share is 1 in 6 = 16.7%, and 16 of the 98 primes above 3 is 16.3% -- on the even
     share, not above it. (CLAUDE.md: a wrong baseline turns the sign of an effect.)

THE OWNER'S QUESTION: is the SSR failure telling us something? Yes -- three things, each computed below.
  A. The test cannot pass. A check value is a prime with root 7 about once in 6 x ln(value) tries (the primes
     thin out as 1 / ln, and the roots 1 2 4 5 7 8 share them evenly). For the 8 kept values at 144 steps that is
     under 3% each, so the chance of reaching the pass mark 0.5 (4 of 8) is about 1 in 4.5 million (2.2e-7), and
     the chance of SSR = 0 is 93%. SSR = 0 is what chance gives; the 0.5 mark is out of reach by construction.
  B. Above 9,007,199,254,740,992 (2^53) a computer's decimal number can only hold even whole numbers, so every check
     value past that is even and can never be prime. With PSI = 1.3824 the steps 111 and 112 are past it.
  C. The trajectory never sees the seed: cylicamp/engine_integration.py starts it at (1, 0) with the field's angle
     0.95, the same for every seed. So the SSR and its FAIL are the same for every seed -- the repo's T316 already
     found "stability_ratio = 0.0, spectrum_status = FAIL" constant over 1110 seeds. It is light from above
     (pasted_shadows_critical_experiment_audit_2026_10_23.py): every candidate gives the same shadow.
  The bundle's "potential fixes" (move PSI, the multiplier, the filter until something passes) would make it pass
  by tuning, not make it tell anything. A test that can tell: count the DR-7 primes against the chance count
  (the sum of 1 / (6 ln value)), use whole-number arithmetic past 2^53, and let the seed reach the trajectory.

FALSIFICATION: any assertion failing.
"""
import math
import pathlib
import sys

import numpy as np
from scipy import integrate
from sympy import isprime, primerange

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "tools"), str(ROOT)]
import owner_walk_big as B  # noqa: E402

P = 37


def root(m):
    while m > 9:
        m = sum(map(int, str(m)))
    return m


def order(a):
    return next(k for k in range(1, P) if pow(a, k, P) == 1)


# --- RIGHT: mod 37 ---
assert order(2) == 36 and [d for d in range(1, 37) if 36 % d == 0] == [1, 2, 3, 4, 6, 9, 12, 18, 36]
dlog = {pow(2, k, P): k for k in range(36)}
assert dlog[10] == 24 and dlog[26] == 12 and dlog[27] == 6 and dlog[19] == 35 and len(dlog) == 36
subs = {1: (1, [1]), 2: (36, [1, 36]), 3: (26, [1, 10, 26]), 4: (31, [1, 6, 31, 36]), 6: (27, [1, 10, 11, 26, 27, 36]),
        9: (16, [1, 7, 9, 10, 12, 16, 26, 33, 34]), 12: (8, [1, 6, 8, 10, 11, 14, 23, 26, 27, 29, 31, 36]),
        18: (4, [1, 3, 4, 7, 9, 10, 11, 12, 16, 21, 25, 26, 27, 28, 30, 33, 34, 36])}
assert all(order(g) == o and sorted({pow(g, k, P) for k in range(o)}) == el for o, (g, el) in subs.items())
assert [r for r in range(1, P) if (r * r + r + 1) % P == 0] == [10, 26]

# --- WRONG 1: the Cayley table ---
E = [1, 10, 11, 26, 27, 36]
pasted = {1: [1, 10, 11, 26, 27, 36], 10: [10, 26, 1, 11, 36, 27], 11: [11, 1, 10, 36, 26, 27],
          26: [26, 11, 36, 10, 1, 1], 27: [27, 36, 26, 1, 10, 11], 36: [36, 27, 27, 1, 11, 10]}
right = {a: [a * b % P for b in E] for a in E}
assert right == {1: [1, 10, 11, 26, 27, 36], 10: [10, 26, 36, 1, 11, 27], 11: [11, 36, 10, 27, 1, 26],
                 26: [26, 1, 27, 10, 36, 11], 27: [27, 11, 1, 36, 26, 10], 36: [36, 27, 26, 11, 10, 1]}
assert sum(pasted[a][i] != right[a][i] for a in E for i in range(6)) == 20
assert len(set(pasted[26])) < 6 and all(sorted(right[a]) == E for a in E)

# --- the twin counts, Brun's sum, the gap ---
w = B.walk_big(500_000_000, block=10_000_000)
n = w["pairs"].astype(np.float64)
assert len(n) == 3_424_506
C2 = 0.6601618158468696
N, L = 1e9, math.log(1e9)
assert round(C2 * N / L ** 2) == 1_537_213                       # the paste's number: C2 without the 2
simple = 2 * C2 * N / L ** 2
li2, _ = integrate.quad(lambda t: 1 / math.log(t) ** 2, 2, N, limit=200)
sharp = 2 * C2 * li2
assert round(simple) == 3_074_426 and round(3_424_506 / simple, 3) == 1.114
assert round(sharp) == 3_425_308 and abs(3_424_506 / sharp - 1) < 0.0003
brun = float(np.sum(1 / (2 * n - 1) + 1 / (2 * n + 1)))
assert round(brun, 5) == 1.77474
assert round(1e9 / 3_424_506, 2) == 292.01

# --- G5 distances ---
psi = 1.3824
assert abs(psi - 0.8 * 1.2 ** 3) < 1e-15
assert round(psi ** 37, 1) == 159752.6 and round(psi ** 38, 1) == 220841.9 and f"{psi ** 144:.6e}" == "1.783431e+20"
assert [k for k in range(145) if k % 37 in (0, 1)] == [0, 1, 37, 38, 74, 75, 111, 112]

# --- powers of 2 ---
assert [pow(2, k, 9) for k in range(6)] == [1, 2, 4, 8, 7, 5]
assert [pow(2, k, 72) for k in range(12)] == [1, 2, 4, 8, 16, 32, 64, 56, 40, 8, 16, 32]
assert sorted({pow(2, k, 72) for k in range(40)}) == [1, 2, 4, 8, 16, 32, 40, 56, 64]

# --- D7 arithmetic ---
lo, hi = 339.932, 429.914
phi = (1 + 5 ** 0.5) / 2
assert round(hi - lo, 3) == 89.982 and round(lo / phi, 2) == 210.09 and round(hi / phi, 2) == 265.70
assert round(1200 * math.log2(hi / lo), 1) == 406.6 and round(100 * (hi - lo) / lo, 2) == 26.47

# --- WRONG 6 and 7: roots of the first 100 primes ---
ps = list(primerange(2, 542))[:100]
assert ps[-1] == 541
counts = [sum(1 for p in ps if root(p) == r) for r in range(1, 10)]
assert counts == [16, 18, 1, 15, 18, 0, 16, 16, 0] and counts[6] == 16
assert counts != [14, 16, 2, 16, 15, 1, 16, 14, 6]
above3 = [p for p in ps if p > 3]
assert len(above3) == 98                                   # 2 and 3 removed from 100
assert sum(1 for p in above3 if root(p) == 7) == 16 and round(16 / 98, 3) == 0.163
assert all(root(p) in (1, 2, 4, 5, 7, 8) for p in above3)

# --- THE QUESTION ---
# A. chance of a DR-7 prime among numbers of the same sizes as the kept check values
PHI_ = phi


def kept_values(psi, steps=144, angle=0.95):
    x, y = 1.0, 0.0
    vals = []
    for k in range(steps + 1):
        if k % 37 in (0, 1):
            vals.append(int((abs(x) + abs(y)) * 1000))
        a = math.atan2(y, x) + PHI_ * angle
        d = math.hypot(x, y) * psi
        x, y = d * math.cos(a), d * math.sin(a)
    return vals


vals = kept_values(1.3824)
assert len(vals) == 8
chance = [0.0 if v > 2 ** 53 or v < 10 else 1 / (6 * math.log(v)) for v in vals]
assert all(c < 0.03 for c in chance)
# exact probability of k hits among 8 independent tries (Poisson-binomial)
dist = [1.0]
for c in chance:
    dist = [(dist[i] if i < len(dist) else 0) * (1 - c) + (dist[i - 1] * c if i >= 1 else 0) for i in range(len(dist) + 1)]
p_zero, p_pass = dist[0], sum(dist[4:])
assert round(p_zero, 2) == 0.93 and 2e-7 < p_pass < 2.5e-7
# the same rate measured: primes with root 7 among the 200,000 numbers above 10^6 and above 10^9
for base in (10 ** 6, 10 ** 9):
    hits = sum(1 for m in range(base, base + 200_000) if root(m) == 7 and isprime(m))
    assert abs(hits / 200_000 - 1 / (6 * math.log(base))) < 0.15 / (6 * math.log(base))

# B. past 2^53 a float holds only even whole numbers
assert 2 ** 53 == 9_007_199_254_740_992
assert all(int(float(m)) % 2 == 0 for m in (2 ** 53 + 1, 2 ** 53 + 3, 5_661_717_843_717_091_329, 7 * 10 ** 18 + 1))
assert [v > 2 ** 53 for v in vals] == [False] * 6 + [True] * 2 and all(v % 2 == 0 for v in vals[6:])

# C. the trajectory never sees the seed
src = (ROOT / "cylicamp" / "engine_integration.py").read_text()
assert "tg = TrajectoryGenerator()" in src and "generate_trajectory(steps=steps, angle_multiplier=angle_mod)" in src
assert "TrajectoryGenerator(seed" not in src and "angle_multiplier=seed" not in src
t316 = (ROOT / "math" / "theorems" / "theorem_316_t120_seed_class_mod_333_gf37.py").read_text()
assert "stability_ratio = 0.0" in t316 and "spectrum_status = FAIL" in t316 and "CONSTANT for every seed" in t316

if __name__ == "__main__":
    print("bundle: mod 37 tables right; Cayley table 20/36 cells wrong; expected twins dropped a 2 (3,425,308 sharp, "
          "actual 0.99977 of it); Brun to 1e9 = 1.77474; prime-root counts wrong, baseline 1/6 not 1/9; "
          "SSR = 0 is what chance gives (P(pass) %.1e, P(0) %.2f), past 2^53 values are even, the seed never reaches it"
          % (p_pass, p_zero))
