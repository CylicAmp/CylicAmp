# CLASS: AUDIT
"""
Audit of supplied text (2026-10-04): minimal 14-cell polyominoes, their "cut 10" placements in an
8 x 8 grid, and invariants of det G(m) = (2m^3 + m^2 - 1)(m - 1). Mathematics only.

CORRECT
  P1 Perimeter = 4n - 2e; Harary-Harborth max internal edges 2n - ceil(2 sqrt n) = 28 - 8 = 20 for
     n = 14, so perimeter >= 16. Both shapes (3x5 minus a corner; 4x4 minus two cells) have 20
     internal edges and perimeter 16.
  P2 2m^3 + m^2 - 1 has no rational root (values 2, -2, -1/2, -1 at m = 1, -1, 1/2, -1/2), so it is
     irreducible over Q; discriminant 4 - 108 = -104 < 0, one real root; positive for m >= 1.
  P3 det G(m) is even iff m is odd; 2m^3 + m^2 - 1 is never 0 mod 3, so 3 | det iff m = 1 mod 3.

WRONG
  P4 "Anchored at the corner, k = 3 + 3 = 6, so cut = 10": shape A at the corner (0, 0) touches the
     grid's edge along 3 cells on one side and 5 on the other -- k = 3 + 5 = 8 (a corner cell has
     an edge on each side; nothing is double-counted). Its cut is 16 - 8 = 8, not 10. Shape B at
     the corner: also k = 8, cut 8. Both computed cell by cell below.
  P5 So "cut 10 is the minimum for 14 cells in the 8 x 8 grid" is false: cut 8 is achieved (h <= 8/14
     = 4/7, not 5/7). Among all corner staircase shapes (Young diagrams) of 14 cells the minimum cut
     is 8 (e.g. rows 3 3 3 3 2). This also bears on AUD-WAV-CHEEGER-42
     (dirichlet_cheeger_42_supplied_audit_2026_10_04.py), whose 10/14 came from the same count.
NOT ESTABLISHED
  P6 "Exactly 20 valid embeddings" and "5 non-isomorphic embeddings per corner": no enumeration
     given, and they count placements with cut 10, which P4 shows is not what corner placement
     gives. The source and meaning of G(m) are not stated; the mod-5 table is cut off.
FALSIFICATION: any assertion failing.
"""
from math import ceil, sqrt

from sympy import Rational, symbols

D = ((1, 0), (-1, 0), (0, 1), (0, -1))


def perimeter(S):
    S = set(S)
    return sum((x + dx, y + dy) not in S for x, y in S for dx, dy in D)


def grid_cut(S, N=8):
    S = set(S)
    return sum(0 <= x + dx < N and 0 <= y + dy < N and (x + dx, y + dy) not in S for x, y in S for dx, dy in D)


A = [(x, y) for x in range(5) for y in range(3) if (x, y) != (4, 2)]
B = [(x, y) for x in range(4) for y in range(4) if (x, y) not in ((3, 2), (3, 3))]
assert 2 * 14 - ceil(2 * sqrt(14)) == 20 and 4 * 14 - 2 * 20 == 16                          # P1
assert perimeter(A) == perimeter(B) == 16 and len(A) == len(B) == 14
m = symbols("m")
lp = 2 * m ** 3 + m ** 2 - 1
assert [lp.subs(m, v) for v in (1, -1, Rational(1, 2), Rational(-1, 2))] == [2, -2, Rational(-1, 2), -1]   # P2
assert 18 * 2 * 1 * 0 * (-1) - 4 * 1 ** 3 * (-1) + 1 ** 2 * 0 ** 2 - 4 * 2 * 0 ** 3 - 27 * 2 ** 2 * (-1) ** 2 == -104
det = lambda v: (2 * v ** 3 + v ** 2 - 1) * (v - 1)
assert all((det(v) % 2 == 0) == (v % 2 == 1) for v in range(-50, 50))                      # P3
assert all((2 * v ** 3 + v ** 2 - 1) % 3 != 0 for v in range(-50, 50))
assert all((det(v) % 3 == 0) == (v % 3 == 1) for v in range(-50, 50))
kA = sum(1 for x, y in A if x == 0) + sum(1 for x, y in A if y == 0)
assert kA == 8 and grid_cut(A) == 8 == perimeter(A) - kA and grid_cut(B) == 8              # P4


def partitions(n, mx):
    if n == 0:
        yield []
        return
    for k in range(min(n, mx), 0, -1):
        for rest in partitions(n - k, k):
            yield [k] + rest


best = min(grid_cut([(x, y) for y, r in enumerate(p) for x in range(r)])
           for p in partitions(14, 8) if len(p) <= 8)
assert best == 8                                                                           # P5
