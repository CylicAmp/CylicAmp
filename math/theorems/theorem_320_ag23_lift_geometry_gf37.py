# CLASS: THEOREM
"""
Theorem 320: the lift machine is AG(2,3); columns are always one parallel
class, and rows are lines for exactly 3 of the 9 grids — all or none
Author: Michael Warren Song (CyclicAmp)

Places T319's lift machine inside the unique affine plane of order 3.

=== THE LABELLING ===

    Points are F_3^2. Stamp the digit  d = 1 + x + 3y:

            x=0  x=1  x=2
     y=0     1    2    3
     y=1     4    5    6
     y=2     7    8    9

    x is the orbit index, y the phase. Adding 3 to a digit is y -> y+1 with x
    fixed: translation by (0,1). So T319's +3 lift IS an affine translation.

=== THE FOUR PARALLEL CLASSES (12 lines, verified) ===

    direction  rule       lines              line sums
    (1,0)      y = c      123  456  789      6, 15, 24
    (0,1)      x = c      147  258  369      12, 15, 18
    (1,1)      y = x+c    159  267  348      15, 15, 15
    (1,2)      y = 2x+c   168  249  357      15, 15, 15

    NOTE ON DIRECTION LABELS. (1,0) increments x with y fixed, so it is the
    rule y = c and the lines 123/456/789. (0,1) is x = c and 147/258/369. A
    source table for this had those two vectors swapped against their rules;
    the rules and lines were correctly paired with each other, only the
    vectors were transposed. Recorded because the swap is easy to inherit.

    Incidence verified directly: two distinct points on exactly one line;
    two lines meet in 0 or 1 point; each point on exactly 4 lines, one per
    class; 3 points per line, 3 lines per class, 4 classes, 12 lines.

=== WHY THE COLUMN SUMS ARE 12, 15, 18 ===

    T319 found empirically that every lift grid has column sums 12, 15, 18.
    Here is the reason: the columns ARE the x = c class, whose three lines
    sum to 12, 15 and 18. Nothing about the seed can change it.

    And a line of either DIAGONAL class meets each x once and each y once, so
    its digit sum is 3 + (0+1+2) + 3(0+1+2) = 15, forced. That is exactly why
    grids 7 and 8 — and only those two — have all three row sums equal to 15.

=== ROWS ARE LINES FOR EXACTLY 3 OF THE 9 GRIDS, AND IT IS ALL OR NONE ===

    grid 1  123 456 789   rows = class (1,0)
    grid 7  159 483 726   rows = class (1,1)
    grid 8  168 492 735   rows = class (1,2)
    grids 2,3,4,5,6,9     ALL THREE rows are non-lines

    Never one, never two. Reason: the lift is translation by (0,1), and a
    translation carries a line to a PARALLEL line. So if the seed is a line,
    the two lifted rows are its parallel translates and the three rows are a
    complete parallel class; if the seed is not a line, none of the three is.

    Rows can never belong to the x = c class, because every row of a lift grid
    is a transversal of the columns — one point from each.

    So the three ruled grids are exactly the three ways to take x = c as
    columns and one of the OTHER three classes as rows.

=== MIX-VS-789 IS NOT A RULING ===

    156 234 789  and  126 345 789: only the frozen 789 row is a line. The
    other two rows are never lines of any class. A mix grid is a point
    partition that keeps one line of the y = c class and discards the plane's
    other structure. No translation carries a mix grid to a lift grid.

=== SCOPE ===

    The quartet {S, S+9a, S+9b, S+9c} is NOT an affine invariant. It is
    decimal notation 10a+b plus the leftover point, and it lives on the
    labelling d = 1+x+3y, not on the plane. AG(2,3) licenses the +3 structure
    and the column class; it says nothing about quartets or closes.

    D3 on three slots is not the collineation group. |AGL(2,3)| = 9 * 48 = 432
    with |GL(2,3)| = (9-1)(9-3) = 48. Permuting three symbols in a row is a
    collineation only if the positions are separately identified with
    x = 0,1,2 and the map checked to be affine.

=== FALSIFICATION ===
    Any assert below failing.
"""

from itertools import combinations, permutations, product

D = lambda x, y: 1 + x + 3 * y
PTS = [(x, y) for y in range(3) for x in range(3)]
DIRS = [(1, 0), (0, 1), (1, 1), (1, 2)]


def klass(v):
    return {frozenset(D((p[0] + t * v[0]) % 3, (p[1] + t * v[1]) % 3)
                      for t in range(3)) for p in PTS}


def adv(v, k):
    return ((v - 1 + k) % 9) + 1


def lift(seed):
    return [tuple(adv(v, 3 * t) for v in seed) for t in range(3)]


def covers(g):
    return sorted(d for r in g for d in r) == list(range(1, 10))


def run():
    CL = {v: klass(v) for v in DIRS}
    LINES = {L for c in CL.values() for L in c}

    # --- the labelling, and +3 as a translation ---
    assert [D(x, 0) for x in range(3)] == [1, 2, 3]
    assert [D(x, 2) for x in range(3)] == [7, 8, 9]
    for x, y in PTS:
        assert adv(D(x, y), 3) == D(x, (y + 1) % 3)

    # --- direction labels, stated correctly ---
    assert sorted(sorted(L) for L in CL[(1, 0)]) == [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    assert sorted(sorted(L) for L in CL[(0, 1)]) == [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
    assert sorted(sorted(L) for L in CL[(1, 1)]) == [[1, 5, 9], [2, 6, 7], [3, 4, 8]]
    assert sorted(sorted(L) for L in CL[(1, 2)]) == [[1, 6, 8], [2, 4, 9], [3, 5, 7]]

    # --- incidence: this is a projective/affine plane of order 3 ---
    assert len(LINES) == 12
    assert all(len(L) == 3 for L in LINES)
    assert all(len(CL[v]) == 3 for v in DIRS)
    for p in combinations(range(1, 10), 2):
        assert sum(1 for L in LINES if set(p) <= L) == 1, p
    for A, B in combinations(LINES, 2):
        assert len(A & B) in (0, 1)
    for p in range(1, 10):
        assert sum(1 for L in LINES if p in L) == 4

    # --- line sums ---
    assert sorted(sum(L) for L in CL[(1, 0)]) == [6, 15, 24]
    assert sorted(sum(L) for L in CL[(0, 1)]) == [12, 15, 18]
    assert sorted(sum(L) for L in CL[(1, 1)]) == [15, 15, 15]
    assert sorted(sum(L) for L in CL[(1, 2)]) == [15, 15, 15]

    # --- the 9 lift grids ---
    good = [p for p in permutations(range(1, 10), 3) if covers(lift(p))]
    seen, grids = set(), []
    for p in sorted({tuple(sorted(x)) for x in {frozenset(q) for q in good}}):
        k = frozenset(frozenset(r) for r in lift(p))
        if k in seen:
            continue
        seen.add(k)
        grids.append(lift(p))
    assert len(grids) == 9

    # columns are ALWAYS the x = c class
    for g in grids:
        cols = {frozenset(g[t][j] for t in range(3)) for j in range(3)}
        assert cols == CL[(0, 1)], g
        assert sorted(sum(c) for c in cols) == [12, 15, 18]

    # rows are lines for exactly 3 grids, all-or-none
    ruled = []
    for i, g in enumerate(grids, 1):
        flags = [frozenset(r) in LINES for r in g]
        assert len(set(flags)) == 1, (i, flags)          # ALL or NONE
        if flags[0]:
            rows = {frozenset(r) for r in g}
            assert any(rows == CL[v] for v in DIRS)      # a whole class
            assert rows != CL[(0, 1)]                    # never the column class
            ruled.append(i)
    assert ruled == [1, 7, 8]
    assert {frozenset(r) for r in grids[0]} == CL[(1, 0)]
    assert {frozenset(r) for r in grids[6]} == CL[(1, 1)]
    assert {frozenset(r) for r in grids[7]} == CL[(1, 2)]
    # and those two diagonal ones are exactly the all-15 grids
    for i, g in enumerate(grids, 1):
        allsame = len({sum(r) for r in g}) == 1
        assert allsame == (i in (7, 8)), i
        if allsame:
            assert {sum(r) for r in g} == {15}

    # --- mix grids are not rulings ---
    for m in ([(1, 5, 6), (2, 3, 4), (7, 8, 9)], [(1, 2, 6), (3, 4, 5), (7, 8, 9)]):
        flags = [frozenset(r) in LINES for r in m]
        assert flags == [False, False, True], m

    # --- group orders ---
    GL = [t for t in product(range(3), repeat=4) if (t[0] * t[3] - t[1] * t[2]) % 3]
    assert len(GL) == 48 == (9 - 1) * (9 - 3)
    assert 9 * len(GL) == 432

    print("All assertions passed.\n")
    print("AG(2,3) with d = 1 + x + 3y     +3 is translation by (0,1)\n")
    print(f"  {'direction':<10} {'rule':<10} {'lines':<22} line sums")
    for v, rule in ((1, 0), "y = c"), (((0, 1)), "x = c"), \
                   (((1, 1)), "y = x+c"), (((1, 2)), "y = 2x+c"):
        ls = sorted(sorted(L) for L in CL[v])
        print(f"  {str(v):<10} {rule:<10} "
              f"{'  '.join(''.join(map(str,L)) for L in ls):<22} "
              f"{sorted(sum(L) for L in CL[v])}")
    print("\n  columns of EVERY lift grid = the x = c class -> sums 12, 15, 18")
    print("  diagonal lines meet each x and each y once -> sum 15, forced\n")
    print("ROWS ARE LINES: all or none")
    for i, g in enumerate(grids, 1):
        rows = {frozenset(r) for r in g}
        w = next((v for v in DIRS if rows == CL[v]), None)
        print(f"  grid {i}: {'  '.join(''.join(map(str,r)) for r in g)}   "
              + (f"rows = class {w}" if w else "no row is a line"))
    print("\n  3 of 9 ruled; the lift is translation by (0,1) and translation")
    print("  carries a line to a parallel line, so it cannot be 1 or 2.")


if __name__ == "__main__":
    run()
