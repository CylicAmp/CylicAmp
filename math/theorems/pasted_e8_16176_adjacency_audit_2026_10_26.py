# CLASS: AUDIT
"""
The pasted note on "16,176 as an E8 graph adjacency sum" (owner_work #444, 2026-10-26). Audit on arrival. Text from
another tool, about a "compilation report" of an earlier conversation; 16,176 is not in owner_work/ or in this repo
(the only match is inside the unrelated number 8592161760 of an OEIS data file).

RIGHT (built from first principles below):
  E8 has 240 roots of squared length 2: 112 with whole coordinates (two entries +-1, the rest 0: 28 places x 4 signs)
  and 128 with all entries +-1/2 and an even number of minus signs
  from any root, the other roots fall at inner product 2, 1, 0, -1, -2 in the numbers 1, 56, 126, 56, 1 (= 240)
  a regular graph on the 240 roots has adjacency sum 240 x (degree): 16176 / 240 = 67.4 is not whole, so no regular
  graph on the roots gives 16,176 -- right; counting edges instead (half the sum, 120 x degree): 16176 / 120 = 134.8,
  not whole either
  the two graphs the note names: inner product 1 -> degree 56, sum 13,440 (6,720 edges);
                                 inner product 0 -> degree 126, sum 30,240 (15,120 edges)

NEW LINES: 16,176 = 2^4 x 3 x 337 is none of the standard E8 counts computed here --
  the theta series 240, 2160, 6720, 17520, 30240, 60480 (vectors of length 2, 4, ..., 12)
  pairs at each inner product (13,440 / 30,240 / 13,440 ordered), triangles of the 56-graph (60,480)
  the sum of all |<a, b>| (27,840) and of all <a, b>^2 (28,800)
  the Cartan matrix sum (2) and its inverse's sum (620 = the coefficients of rho added up)
  So the note's conclusion stands: without its own definition, 16,176 is not an E8 adjacency number.

FALSIFICATION: any assertion failing.
"""
from fractions import Fraction as F
from itertools import combinations, product

import numpy as np

roots = []
for i, j in combinations(range(8), 2):
    for si, sj in product((1, -1), repeat=2):
        v = [0] * 8
        v[i], v[j] = si, sj
        roots.append(tuple(F(x) for x in v))
for signs in product((1, -1), repeat=8):
    if signs.count(-1) % 2 == 0:
        roots.append(tuple(F(s, 2) for s in signs))
R = np.array([[float(x) for x in r] for r in roots])
assert len(roots) == 240 and len(set(roots)) == 240 and np.allclose((R * R).sum(1), 2)
G = np.rint(R @ R.T).astype(int)
assert np.allclose(R @ R.T, G)
for row in G:
    assert sorted(np.unique(row, return_counts=True)[1].tolist()) == [1, 1, 56, 56, 126]
    assert dict(zip(*np.unique(row, return_counts=True))) == {2: 1, 1: 56, 0: 126, -1: 56, -2: 1}
A56, A126 = (G == 1).astype(int), (G == 0).astype(int)
assert A56.sum() == 240 * 56 == 13_440 and A126.sum() == 240 * 126 == 30_240
assert A56.sum() // 2 == 6_720 and A126.sum() // 2 == 15_120
assert 16176 % 240 and 16176 / 240 == 67.4 and 16176 % 120 and 16176 / 120 == 134.8
assert 16176 == 2 ** 4 * 3 * 337

# standard counts, none of them 16176
def sigma3(n):
    return sum(d ** 3 for d in range(1, n + 1) if n % d == 0)


theta = [240 * sigma3(n) for n in range(1, 7)]
assert theta == [240, 2160, 6720, 17520, 30240, 60480]
triangles = int(np.trace(A56 @ A56 @ A56)) // 6
assert triangles == 60_480
abs_sum = int(np.abs(G).sum())
sq_sum = int((G ** 2).sum())
assert abs_sum == 240 * (2 + 56 + 56 + 2) == 27_840 and sq_sum == 240 * (4 + 56 + 56 + 4) == 28_800
# Cartan matrix of E8 (Bourbaki order: 1-3-4-5-6-7-8 with 2 on 4)
C = 2 * np.eye(8, dtype=int)
for a, b in [(0, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (1, 3)]:
    C[a, b] = C[b, a] = -1
Cinv = np.rint(np.linalg.inv(C)).astype(int)
assert np.allclose(np.linalg.inv(C), Cinv) and C.sum() == 2 and Cinv.sum() == 620
standard = theta + [13_440, 30_240, 6_720, 15_120, triangles, abs_sum, sq_sum, int(C.sum()), int(Cinv.sum())]
assert 16176 not in standard

if __name__ == "__main__":
    print("E8 from first principles: 240 roots, 1/56/126/56/1 by inner product; 16176/240 = 67.4, so no regular "
          "root graph gives it; 16176 = 2^4 x 3 x 337 matches no standard E8 count")
