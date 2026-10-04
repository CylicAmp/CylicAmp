# CLASS: AUDIT
"""
Audit of a long supplied block (2026-10-04): digital roots of the first nine primes on 3x3 grids,
coupled grids, a "geyser" with eight rays, the matrices Z / P0 / J / ring B, and 96 diagonal
templates (1-2-3 diagonal, 1-6-7 arm, 4 open cells filled by permutations of {4,5,8,9}) with
their determinants. (The block restating the Gaussian-prime audit is accurate.) Mathematics only.

CORRECT
  A1 First nine primes 2..23 -> roots 2 3 5 7 2 4 8 1 5; sum 37 (root 1); 6 and 9 absent; 2 and
     5 twice. Reading-order grid: column 2 = 6, main diagonal 9, anti-diagonal 15; det = -42.
  A2 Geyser ray sums through a centre 1: 8, 10, 14, 8 with the eight remaining roots. Spiral case:
     opposite rays 8, 10, 12, 14 (step 2). Orthogonal {2,3,4,5} = 14, diagonal {6,7,8,9} = 30,
     total 44 = 2 + ... + 9. Opposite pairs summing to 11 (2+9, 3+8, 4+7, 5+6) make every line
     through the centre 12 -- forced: 2..9 pair off to 11.
  A3 Z, P0, J: ranks 0, 1, 1; J has eigenvalue 3 on (1,1,1); J M J = (sum of M) J, so 45 J for any
     arrangement of 1..9. 9! = 362,880; with three cells fixed, 6! = 720.
  A4 ALL 96 DETERMINANTS ARE CORRECT -- every table entry recomputed from the template the
     text's own determinant formula defines. Main-diagonal templates give +204..+385, anti-
     diagonal templates -385..-204, and each anti-diagonal table is the negative of a main one.
     +385 at (main, P14) and (reverse main, P11); -385 at (anti, P12) and (reverse anti, P4).
     385 = 1^2 + ... + 10^2 is a true identity (its appearance here is not derived).

WRONG
  W1 "Not a single configuration yields det = 0 mod 9": +234 and -234 do (234 = 26 x 9, root 9) --
     the main template at P21, the reverse main at P13, and their negatives. The conclusion drawn
     from it ("a topological barrier against singular collapse") falls with it.
  W2 Ring B = J - P0 (ones with a 0 centre): eigenvalues are 1 + sqrt 3, 1 - sqrt 3 and 0
     (= 2.732, -0.732, 0), not 3, 1, -2. Only the trace 2 is right.
  W3 A 2x2 block of 3x3 grids overlapping in a 5x5: 36 slots on 25 cells -- 11 is the overcount,
     but only 9 cells are shared (the middle row and middle column; the centre is shared four
     ways). And a 5x5 has nine 3x3 sub-grids, not four; four only when they step by 2.
FALSIFICATION: any assertion failing.
"""
import itertools

import numpy as np
from sympy import Matrix

roots = [1 + (p - 1) % 9 for p in (2, 3, 5, 7, 11, 13, 17, 19, 23)]
assert roots == [2, 3, 5, 7, 2, 4, 8, 1, 5] and sum(roots) == 37                       # A1
G = [roots[0:3], roots[3:6], roots[6:9]]
assert sum(G[r][1] for r in range(3)) == 6 and G[0][0] + G[1][1] + G[2][2] == 9
assert G[0][2] + G[1][1] + G[2][0] == 15 and Matrix(G).det() == -42
assert sorted([2, 5, 7, 2, 5, 8, 3, 4]) == sorted(roots[:7] + roots[8:])                  # A2
assert [2 + 1 + 5, 7 + 1 + 2, 5 + 1 + 8, 3 + 1 + 4] == [8, 10, 14, 8]
assert [2 + 6, 3 + 7, 4 + 8, 5 + 9] == [8, 10, 12, 14] and sum(range(2, 10)) == 44
J = np.ones((3, 3)); P0 = np.zeros((3, 3)); P0[1, 1] = 1                                  # A3
assert np.linalg.matrix_rank(J) == 1 and np.allclose(J @ np.ones(3), 3 * np.ones(3))
M = np.arange(1, 10).reshape(3, 3)
assert np.allclose(J @ M @ J, 45 * J)

T = {"main": lambda a, b, g, d: [[1, a, b], [6, 2, g], [7, d, 3]],
     "rev_main": lambda a, b, g, d: [[3, a, 7], [b, 2, 6], [g, d, 1]],
     "anti": lambda a, b, g, d: [[7, a, 3], [6, 2, b], [1, g, d]],
     "rev_anti": lambda a, b, g, d: [[a, b, 1], [g, 2, 6], [3, d, 7]]}
GIVEN = {"main": [286, 284, 349, 269, 340, 262, 284, 295, 340, 275, 330, 254, 257, 385, 250, 380, 210, 212, 255, 372, 234, 366, 204, 219],
         "rev_main": [219, 212, 366, 254, 380, 275, 204, 210, 372, 262, 385, 269, 234, 330, 255, 340, 295, 284, 250, 340, 257, 349, 284, 286],
         "anti": [-212, -219, -254, -366, -275, -380, -210, -204, -262, -372, -269, -385, -330, -234, -340, -255, -284, -295, -340, -250, -349, -257, -286, -284],
         "rev_anti": [-284, -295, -257, -385, -255, -372, -286, -284, -250, -380, -234, -366, -349, -269, -340, -275, -204, -219, -340, -262, -330, -254, -210, -212]}
perms = list(itertools.permutations((4, 5, 8, 9)))
dets = {k: [int(Matrix(f(*p)).det()) for p in perms] for k, f in T.items()}
assert dets == GIVEN                                                                      # A4
assert sorted(dets["anti"]) == sorted(-x for x in dets["main"])
assert min(dets["main"] + dets["rev_main"]) == 204 and max(dets["anti"] + dets["rev_anti"]) == -204
assert sum(k * k for k in range(1, 11)) == 385
assert T["main"](4, 5, 8, 9) == [[1, 4, 5], [6, 2, 8], [7, 9, 3]]                         # P1 row/col spot check
assert [sum(r) for r in T["main"](4, 5, 8, 9)] == [10, 16, 19]
assert [sum(c) for c in zip(*T["main"](4, 5, 8, 9))] == [14, 15, 16]
zero9 = sorted({d for v in dets.values() for d in v if d % 9 == 0})                      # W1
assert zero9 == [-234, 234] and dets["main"][20] == 234 and dets["rev_main"][12] == 234
B = np.ones((3, 3)); B[1, 1] = 0                                                          # W2
ev = sorted(np.linalg.eigvalsh(B))
assert np.allclose(ev, [1 - 3 ** 0.5, 0, 1 + 3 ** 0.5]) and np.isclose(sum(ev), 2)
cnt = np.zeros((5, 5), int)                                                               # W3
for r0, c0 in ((0, 0), (0, 2), (2, 0), (2, 2)):
    cnt[r0:r0 + 3, c0:c0 + 3] += 1
assert cnt.sum() == 36 and (cnt > 0).sum() == 25 and (cnt > 1).sum() == 9 and cnt.sum() - 25 == 11
assert len([(r, c) for r in range(3) for c in range(3)]) == 9
