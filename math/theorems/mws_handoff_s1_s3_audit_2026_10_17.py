# CLASS: AUDIT
"""
Audit of the MWS Unified Framework handoff, sections 1-3 (owner_work #272, 2026-10-14; the owner's
pasted document, stored verbatim in owner_work/messages/2026-10-14.txt). Section 4 is built as
tools/zeta_parity_engine.py, section 5 as dashboards/mws_unified/. Formulas lost in the paste (the Mod 37
residue vector, the entropy formula, the matrices M and dr(M)) are not guessed.

HOLDS
  S1  every digital-root example (45.0% -> 9, 45.1% -> 1, 0.09% -> 9, 12% -> 3, 19% -> 1; 0.084 -> 3,
      0.232 -> 7, 0.253 -> 1, 0.257 -> 5); the 12 arrangements of 0046 (all digital root 1); 0.064 -> 1
      (the minus sign of -0.064 is dropped by the rule, since only digits are summed).
  S2  the primes 1009 1013 1019 1021 1031 1033 1039, gaps [4,6,2,10,2,6], the 14 odd composites listed
      (complete), 1029 = 3 x 7^3 = 3 x 343. Mod 37 residues (the vector was lost in the paste):
      10 14 20 22 32 34 3 -> IC C9 DARK_A NQR17 SEED D7 C3.
      phi(a,b,c) + phi(c,b,a) = pi holds for b > 0 (tested on a, b, c in 1..29, a != c).
      The lag-1 correlation of consecutive prime gaps is -0.0639 for primes below 130,000 and -0.0641
      below 200,000: the handoff's -0.064 matches a range near 1.3e5 to 2e5.
  S3  Game of Life on the owner's 9 x 11 matrix (16 cells, dead border): runs and dies out.

CORRECTIONS
  S2  "-0.064" is not one constant: -0.0700 below 1e5, -0.0431 below 1e6, -0.0381 below 1e7. The figure
      depends on how far the primes go and falls toward 0 as the range grows; these runs do not settle the limit.
  S2  phi(a,b,c) + phi(c,b,a) = pi needs b > 0: for b < 0 the sum is -pi, and for b = 0 with a = c it is 0.
  S2  "mean (c-a) = 0.0019 -> 0": for consecutive gaps the mean of g[n+2] - g[n] telescopes to
      (g[N+1] + g[N+2] - g[1] - g[2]) / N exactly, so it goes to 0 for any gap sequence -- forced, not a
      finding. Below 1e5 it is 0.00177.
  S2  "45.0% vs 45.1%, excess 0.09%": 45.1 - 45.0 = 0.1, so 0.09 holds only for unrounded values. s_prev and
      s_next are not defined. For consecutive gap pairs the shares of g_prev > g_next and g_prev < g_next
      are 48.06% and 48.13% below 1e6 -- not 45.0 / 45.1. Not reproduced.
  S3  the matrix is shown as "Generation 6", but the seed is not given. The 16-cell ring itself, run
      forward, has 22 cells at its generation 6: it is not generation 6 of itself.

NOT DEFINED IN THE HANDOFF (so not checked): the DCPG dataset, the entropy formula, Module 1's
  hourglass operation, the construction of [111, 30, 3, 3, 0] from the seed 286692321 (= 3 x 131 x 729497,
  digital root 3, 4 mod 37, C3), the matrices M and dr(M), DR_peak, Refraction_null, Entropy_mean 0.6730 nats
  (ln 2 = 0.6931).

FALSIFICATION: any assertion failing.
"""
import math
from sympy import factorint, isprime, primerange


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


def digits_dr(s):
    return dr(sum(int(c) for c in s if c.isdigit()))


# S1
assert [digits_dr(s) for s in ("45.0%", "45.1%", "0.09%", "12%", "19%")] == [9, 1, 9, 3, 1]
assert [digits_dr(s) for s in ("0", "0.084", "0.232", "0.253", "0.257")] == [0, 3, 7, 1, 5]
from itertools import permutations
perms = sorted({"".join(p) for p in permutations("0046")})
assert len(perms) == 12 and set(perms) == {"0046", "0406", "0460", "4006", "4060", "4600", "0064", "0604", "0640", "6004", "6040", "6400"}
assert {digits_dr(p) for p in perms} == {1} and digits_dr("0.064") == 1 and digits_dr("-0.064") == 1
# S2
ps = list(primerange(1002, 1045))
assert ps == [1009, 1013, 1019, 1021, 1031, 1033, 1039] and [b - a for a, b in zip(ps, ps[1:])] == [4, 6, 2, 10, 2, 6]
assert [p % 37 for p in ps] == [10, 14, 20, 22, 32, 34, 3]
LISTED = [1003, 1005, 1007, 1011, 1015, 1017, 1023, 1025, 1027, 1029, 1035, 1037, 1041, 1043]
assert [n for n in range(1003, 1044, 2) if not isprime(n)] == LISTED and factorint(1029) == {3: 1, 7: 3} and 3 * 343 == 1029
assert all(abs(math.atan2(b, c - a) + math.atan2(b, a - c) - math.pi) < 1e-12 for a in range(1, 30) for b in range(1, 30) for c in range(1, 30) if a != c)
assert abs(math.atan2(-2, 3) + math.atan2(-2, -3) + math.pi) < 1e-12 and math.atan2(0, 0) + math.atan2(0, 0) == 0


def lag1(N):
    p = list(primerange(2, N)); g = [b - a for a, b in zip(p, p[1:])]; x, y = g[:-1], g[1:]
    mx, my = sum(x) / len(x), sum(y) / len(y)
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y)); sxx = sum((a - mx) ** 2 for a in x); syy = sum((b - my) ** 2 for b in y)
    return sxy / math.sqrt(sxx * syy), g


for N, lo, hi in ((10 ** 5, -0.0705, -0.0695), (130000, -0.0645, -0.0635), (200000, -0.0646, -0.0636), (10 ** 6, -0.0436, -0.0426)):
    r, g = lag1(N); assert lo < r < hi, (N, r)
g = lag1(10 ** 5)[1]; n = len(g) - 2
assert abs(sum(g[i + 2] - g[i] for i in range(n)) / n - (g[-1] + g[-2] - g[0] - g[1]) / n) < 1e-12 and 0.0017 < (g[-1] + g[-2] - g[0] - g[1]) / n < 0.0018
assert 45.1 - 45.0 != 0.09
r6, g6 = lag1(10 ** 6); pairs = list(zip(g6[:-1], g6[1:]))
gt, lt = sum(a > b for a, b in pairs) / len(pairs), sum(a < b for a, b in pairs) / len(pairs)
assert 0.480 < gt < 0.481 and 0.481 < lt < 0.482
# S3
assert factorint(286692321) == {3: 1, 131: 1, 729497: 1} and dr(286692321) == 3 and 286692321 % 37 == 4
assert abs(math.log(2) - 0.6931) < 1e-4 and 0.6730 != round(math.log(2), 4)
M = ["00000000000", "00001110000", "00010001000", "00100000100", "01000000010", "00100000100", "00010001000", "00001110000", "00000000000"]
assert len(M) == 9 and all(len(r) == 11 for r in M)


def step(live, bounded):
    cnt = {}
    for (r, c) in live:
        for a in (-1, 0, 1):
            for b in (-1, 0, 1):
                if (a, b) != (0, 0): cnt[(r + a, c + b)] = cnt.get((r + a, c + b), 0) + 1
    new = {x for x, k in cnt.items() if k == 3 or (k == 2 and x in live)}
    return {(r, c) for (r, c) in new if 0 <= r < 9 and 0 <= c < 11} if bounded else new


start = {(r, c) for r, row in enumerate(M) for c, ch in enumerate(row) if ch == "1"}
assert len(start) == 16
live, sizes = set(start), []
for _ in range(14): sizes.append(len(live)); live = step(live, True)
assert sizes == [16, 26, 34, 30, 28, 44, 20, 20, 14, 14, 8, 6, 4, 0]                       # bounded 9x11, dead border: cells per generation 0..13
live, t = set(start), 0
while live and t < 30: live = step(live, True); t += 1
assert t == 13 and not live                                                                # dies out at generation 13
live, sizes = set(start), []
for _ in range(7): sizes.append(len(live)); live = step(live, False)
assert sizes[0] == 16 and sizes[6] == 22                                                    # unbounded plane: 22 cells at generation 6

if __name__ == "__main__":
    print("handoff S1-S3: examples and prime audit hold; -0.064 is range-dependent (-0.070, -0.043, -0.038); mean(c-a) is forced; Life ring dies out at gen 13")
