#!/usr/bin/env python3
"""
Permanent and determinant congruences in 3 x 3 digit grids -- reproduction (plain Python 3, no libraries).
The owner's Egor calculations (2026-11-28): the grid 1 2 3 / 4 5 6 / 7 8 9, the swaps 2<->5 and 7<->8, a mod-9 criterion.

    python3 reproduce.py        prints PASS / FAIL for every claim
"""
from itertools import permutations, product


def sign(p):
    s = 1
    for i in range(len(p)):
        for j in range(i + 1, len(p)):
            if p[i] > p[j]:
                s = -s
    return s


def per_det_odd(M):
    per = det = odd = 0
    for p in permutations(range(3)):
        t = M[0][p[0]] * M[1][p[1]] * M[2][p[2]]
        per += t
        det += sign(p) * t
        odd += t if sign(p) < 0 else 0
    return per, det, odd


def swap(M, a, b):
    return [[b if x == a else a if x == b else x for x in row] for row in M]


S = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
GRIDS = {"none": S, "2<->5": swap(S, 2, 5), "7<->8": swap(S, 7, 8), "both": swap(swap(S, 2, 5), 7, 8)}
WANT = {"none": (450, 0, 225), "2<->5": (594, 54, 270), "7<->8": (459, -9, 234), "both": (612, 72, 270)}

results = []


def claim(name, ok):
    results.append(bool(ok))
    print(("PASS  " if ok else "FAIL  ") + name)


for k, M in GRIDS.items():
    claim(f"swap {k}: per, det, odd sum = {WANT[k]}", per_det_odd(M) == WANT[k])
    p, d, o = per_det_odd(M)
    claim(f"swap {k}: per - det = 2 x odd sum, and per = det by 9", p - d == 2 * o and (p - d) % 9 == 0)
claim("interaction 72 - 54 - (-9) + 0 = 27", WANT["both"][1] - WANT["2<->5"][1] - WANT["7<->8"][1] + WANT["none"][1] == 27)
claim("the two single swaps give determinants of opposite sign (54 and -9)", WANT["2<->5"][1] > 0 > WANT["7<->8"][1])

n = fails = 0
for u in product(range(9), repeat=3):
    if sorted(x % 3 for x in u) != [0, 1, 2]:
        continue
    for v in product(range(9), repeat=3):
        A = [[u[i] + 3 * v[j] for j in range(3)] for i in range(3)]
        p, d, _ = per_det_odd(A)
        n += 1
        fails += ((p - d) % 9 == 0) != (sum(v) % 3 == 0)
claim(f"criterion: A_ij = u_i + 3 v_j, u = the three classes by 3 -> per = det by 9 iff v1+v2+v3 = 0 by 3 ({n} cases)", fails == 0)
claim("the standard grid is in the family: transpose of u = (1,2,3), v = (0,1,2), and 0+1+2 = 3",
      [[1 + 3 * j for j in range(3)], [2 + 3 * j for j in range(3)], [3 + 3 * j for j in range(3)]] == [list(c) for c in zip(*S)])

flips = {}
for fl in product([0, 1], repeat=3):
    M = [row[::-1] if f else row for row, f in zip(S, fl)]
    p, d, _ = per_det_odd(M)
    flips[fl] = (p, d, (p - d) % 9)
claim("row flips of 1 2 3 / 4 5 6 / 7 8 9: det stays 0 (every row is evenly spaced)", all(v[1] == 0 for v in flips.values()))
claim("row flips: per = 450 478 490 502; per - det by 9 = 0 for no flip and all three flips, 1 4 7 otherwise",
      sorted({v[0] for v in flips.values()}) == [450, 478, 490, 502]
      and flips[(0, 0, 0)][2] == flips[(1, 1, 1)][2] == 0
      and sorted({v[2] for k, v in flips.items() if 0 < sum(k) < 3}) == [1, 4, 7])

print("ALL PASS" if all(results) else "SOME FAILED")
raise SystemExit(0 if all(results) else 1)
