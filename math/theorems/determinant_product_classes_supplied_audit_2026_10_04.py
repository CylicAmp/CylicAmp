# CLASS: AUDIT
"""
Audit of supplied text (2026-10-04): the main diagonal template's determinant as a polynomial,
and its 24 values sorted by the products ag, gd, bd. Template [[1,a,b],[6,2,g],[7,d,3]],
(a,b,g,d) a permutation of (4,5,8,9) (prime_root_grids_and_96_templates_supplied_audit_2026_10_04.py).
Mathematics only.

CORRECT
  D1 det = 6 - 18a - 14b + 7ag + 6bd - gd for every permutation.
  D2 Only two values repeat: 284 at (4,5,9,8) and (5,4,8,9); 340 at (4,9,5,8) and (5,8,4,9).
     D(a,b,g,d) = D(b,a,d,g) holds only for those two swaps.
  D3 The ag table (20: 330 340 340 349 / 1359; 32: 210 250 262 286 / 1008; 36: 204 234 269 284
     / 991; 40: 212 254 257 284 / 1007; 45: 219 255 275 295 / 1044; 72: 366 372 380 385 / 1503)
     and the gd table are exact. Each class has 4 members: fixing {a, g} leaves {b, d} in 2
     orders, and {a, g} itself in 2 orders.
  D4 ag and bd sort the 24 cases identically with the products reversed -- forced: {b, d} is the
     other pair of {4,5,8,9}, so bd is the complementary product: 20 <-> 72, 32 <-> 45,
     36 <-> 40.

WRONG
  D5 The listed pairing "ag 20 <-> gd 72, 32 <-> 45, 36 <-> 32, 40 <-> 40, 45 <-> 36, 72 <-> 20"
     has no stated rule and matches neither table: the ag = 20 and gd = 72 classes share no
     value (330 340 340 349 vs 284 284 286 295), and 36 <-> 32, 40 <-> 40, 45 <-> 36 are not
     complements. The real pairing is the complementary one in D4 (ag with bd).
FALSIFICATION: any assertion failing.
"""
import itertools
from collections import Counter, defaultdict

from sympy import Matrix

P = list(itertools.permutations((4, 5, 8, 9)))
D = lambda a, b, g, d: 6 - 18 * a - 14 * b + 7 * a * g + 6 * b * d - g * d
assert all(D(a, b, g, d) == Matrix([[1, a, b], [6, 2, g], [7, d, 3]]).det() for a, b, g, d in P)   # D1
c = Counter(D(*p) for p in P)
assert {k: v for k, v in c.items() if v > 1} == {284: 2, 340: 2}                                    # D2
assert sorted(p for p in P if c[D(*p)] > 1) == [(4, 5, 9, 8), (4, 9, 5, 8), (5, 4, 8, 9), (5, 8, 4, 9)]
assert sum(D(b, a, d, g) == D(a, b, g, d) for a, b, g, d in P) == 2


def classes(f):
    out = defaultdict(list)
    for a, b, g, d in P:
        out[f(a, b, g, d)].append(D(a, b, g, d))
    return {k: sorted(v) for k, v in out.items()}


ag, gd, bd = classes(lambda a, b, g, d: a * g), classes(lambda a, b, g, d: g * d), classes(lambda a, b, g, d: b * d)
assert ag == {20: [330, 340, 340, 349], 32: [210, 250, 262, 286], 36: [204, 234, 269, 284],       # D3
              40: [212, 254, 257, 284], 45: [219, 255, 275, 295], 72: [366, 372, 380, 385]}
assert [sum(ag[k]) for k in (20, 32, 36, 40, 45, 72)] == [1359, 1008, 991, 1007, 1044, 1503]
assert gd == {20: [204, 210, 212, 219], 32: [234, 254, 330, 366], 36: [250, 275, 340, 380],
              40: [255, 262, 340, 372], 45: [257, 269, 349, 385], 72: [284, 284, 286, 295]}
comp = {20: 72, 72: 20, 32: 45, 45: 32, 36: 40, 40: 36}                                          # D4
assert all(bd[comp[k]] == v for k, v in ag.items())
assert not set(ag[20]) & set(gd[72]) and comp[36] == 40 != 32                                     # D5
