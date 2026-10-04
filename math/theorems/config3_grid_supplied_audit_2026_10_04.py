# CLASS: AUDIT
"""
Audit of a supplied reconstruction (2026-10-04) of "Config 3" from
prime_root_grids_and_96_templates_supplied_audit_2026_10_04.py: the nine roots
{2, 3, 5, 7, 2, 4, 8, 1, 5} of the first nine primes, centre 1, row sums 10, 12, 15.
Mathematics only.

CORRECT
  R1 Grid 2 3 5 / 4 1 7 / 5 8 2 uses exactly the nine roots; rows 10, 12, 15; columns 11, 12, 14;
     main diagonal 5, anti-diagonal 11; determinant 108 (root 9).
  R2 The deduction is forced once the corners are fixed: top edge 10 - 7 = 3, bottom edge
     15 - 7 = 8, and the side edges are the remaining {4, 7} summing to 11.
  R3 Swapping the side edges keeps the rows and diagonals and turns the columns into 14, 12, 11 --
     but the "preserving the corner balances" note leaves out that the determinant changes:
     2 3 5 / 7 1 4 / 5 8 2 has determinant 213, not 108.
COMPLETING THE COUNT (exhaustive over all arrangements of the multiset)
  R4 Exactly 4 arrangements have centre 1, rows 10 / 12 / 15 and diagonal sums {5, 11}: the 2s on the
     main diagonal or the 5s on it, times the 2 orders of {4, 7}. Their determinants are 108, 213,
     -213, -108. With the text's own condition (main diagonal 2 + 1 + 2) there are 2: determinants
     108 (the stated grid) and 213 (its side-swap).
     (A first draft of this file assumed the swap kept the determinant; the assertion caught it.)
FALSIFICATION: any assertion failing.
"""
import itertools

from sympy import Matrix

ROOTS = [2, 3, 5, 7, 2, 4, 8, 1, 5]
G = [[2, 3, 5], [4, 1, 7], [5, 8, 2]]
assert sorted(sum(G, [])) == sorted(ROOTS)                                               # R1
assert [sum(r) for r in G] == [10, 12, 15] and [sum(c) for c in zip(*G)] == [11, 12, 14]
assert G[0][0] + G[1][1] + G[2][2] == 5 and G[0][2] + G[1][1] + G[2][0] == 11
assert Matrix(G).det() == 108 and 108 % 9 == 0
assert (10 - 2 - 5, 15 - 5 - 2, 12 - 1) == (3, 8, 11) and 4 + 7 == 11                    # R2
G2 = [[2, 3, 5], [7, 1, 4], [5, 8, 2]]
assert [sum(r) for r in G2] == [10, 12, 15] and [sum(c) for c in zip(*G2)] == [14, 12, 11]  # R3
assert Matrix(G2).det() == 213
sols = set()
for p in set(itertools.permutations(ROOTS)):                                             # R4
    g = [list(p[0:3]), list(p[3:6]), list(p[6:9])]
    if g[1][1] == 1 and [sum(r) for r in g] == [10, 12, 15] and \
            {g[0][0] + g[1][1] + g[2][2], g[0][2] + g[1][1] + g[2][0]} == {5, 11}:
        sols.add(tuple(map(tuple, g)))
assert len(sols) == 4
assert sorted(int(Matrix([list(r) for r in g]).det()) for g in sols) == [-213, -108, 108, 213]
assert len([g for g in sols if g[0][0] + g[1][1] + g[2][2] == 5]) == 2
