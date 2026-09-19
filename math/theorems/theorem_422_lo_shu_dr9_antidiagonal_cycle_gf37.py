# CLASS: THEOREM
"""
Theorem 422: the 3x3 DR-9 family has 72 members, the diagonal calibration has
24 = 4! (forced), and the 30-vertex anti-diagonal graph IS Hamiltonian

Audit of a supplied optimization/calibration run on 3x3 grids of 1..9.
Three of its numbers are right, three of its conclusions are not.

PRIOR ART.
  T104 (theorem_104_lo_shu_gf37.py) puts the Lo Shu itself on GF(37):
  magic constant 15, total 45 = 8 (mod 37), the cell-by-cell classification.
  T324 (theorem_324_general_lift_magic_gf37.py) shows the magic constant
  n(n^2+1)/2 was never special.
  Neither touches the DR-9 family, the calibration count, or the
  anti-diagonal graph. Those three are this file's own.

=== CONFIRMED FROM THE SUPPLIED RUN ===

  (1) Exactly 8 magic squares on 1..9 with no repeats. Brute force over all
      9! = 362880 arrangements agrees. This is the single Lo Shu class under
      the 8 symmetries of the square (T104's "unique up to symmetry").

  (2) The eight listed row-triples are those 8, 492/357/816 among them.

  (3) The exhibited DR-9 grid does have all eight lines = 0 (mod 9):

          9 8 1     rows 18 18  9
          7 6 5     cols 18 18  9
          2 4 3     main 18   anti 9

=== CORRECTION 1: "Best DR-9 score: 9/8" ===

  There are 8 lines (3 rows, 3 columns, 2 diagonals). A score of 9 out of a
  denominator of 8 is not a score. The 9th term is the grand total 45, and

      every arrangement of 1..9 totals 45, and DR(45) = 9

  so that term is FORCED. It is true of all 362880 grids and separates
  nothing. The honest score is 8/8, and the denominator was the error.

=== CORRECTION 2: "Best grid" is one of 72, not one ===

  Grids with all eight lines = 0 (mod 9):   72   of 362880  = 0.0198%

  The run reports a single "best grid" for an optimum that 72 grids attain.
  0.0198% is genuinely selective -- the miss-test passes, the property could
  have come back empty -- but "best" implies a unique argmax and there is
  none.

  The DR-9 family and the magic family are DISJOINT, and forced to be:
  a magic line sums to 15, and DR(15) = 6, never 9. So this is not a
  near-miss variant of the Lo Shu; it is a different family entirely.
  15 = 15 (mod 37) in DARK_A; the DR-9 line sums are 18 in SEED and 9 in
  SA_ST_A.

=== CORRECTION 3: the diagonal calibration count 24 is forced ===

  Target main = [1,2,3], anti = [4,2,5]. The run reports "Best score: 0" and
  one grid. The number of grids with score 0 is 24, and it is forced:

      the two diagonals share the center, so the target pins 5 of the 9
      cells (1,2,3 on the main; 4,5 at the anti corners);
      the remaining 4 cells are free;   4! = 24.

  So the search performs no work beyond placing the five constrained cells.
  A "best score 0" here is the definition being satisfiable, not an
  optimization result. 24 = 24 (mod 37) in SEED -- the seed orbit -- but
  that is 4! reduced, a forced count, and is recorded as such, not as a hit.

=== CORRECTION 4 (the substantive one): the cycle EXISTS ===

  The run reports, for main diagonal fixed to [1,2,3]:

      Cycle length: 30      Returns to start: False
      Digit changes per step: {1,2}     All single changes: False

  A Hamiltonian cycle returns to its start by definition; "Returns to start:
  False" means the search found a path and stopped, not that no cycle exists.

  THE GRAPH.  With the main diagonal [1,2,3], the anti-diagonal is [a,2,b]
  with a,b distinct in S = {4,5,6,7,8,9}: 6*5 = 30 ordered pairs, which is
  where the run's 30 comes from. Join two when they differ in exactly one
  coordinate. The graph is 8-regular (4 changes per coordinate, the value
  equal to the other coordinate excluded) and vertex-transitive.

  RESULT.  A Hamiltonian CYCLE exists, it closes, and every one of its 30
  steps changes exactly ONE digit:

      (4,5) (4,6) (4,7) (4,8) (4,9) (5,9) (5,6) (5,7) ... (9,5) -> (4,5)

  So all three of the run's negative findings invert:

      returns to start        False -> True
      digit changes per step  {1,2} -> {1}
      all single changes      False -> True

  This is a search failure in the supplied script, not an obstruction. The
  cycle is exhibited and verified below, which is why it is stated as a
  theorem and not as a conjecture.

=== GF(37) ===

  30 = 30 (mod 37) in C3      the vertex count, = 6*5
  72 = 35 (mod 37) in NQR17   the DR-9 family size, = 8*9
   8 =  8 (mod 37) in TESLA   the magic-square count
  45 =  8 (mod 37) in TESLA   the grand total (T104 Lemma 104.2, as CB)
  24 = 24 (mod 37) in SEED    the calibration count, forced as 4!

  8 and 45 land on the same residue because 45 = 37 + 8. That is the seam,
  not a coincidence between the two counts, and it is T104's Lemma 104.2
  restated -- cited, not rediscovered.

  FORCED, carrying no information: DR(45) = 9 for every arrangement;
  24 = 4!; the magic constant 15 (T324: it is n(n^2+1)/2 for every n).

=== FALSIFICATION ===

  Any of: a 9th magic square; a 73rd or 71st DR-9 grid; a 25th or 23rd
  score-0 calibration grid; or a single step of the exhibited cycle that
  changes two digits or fails to close. All four are checked by assertion.
"""

import sys
from itertools import permutations

P = 37
ORBITS = {
    "IC": {1, 10, 26}, "DARK_A": {2, 15, 20}, "C3": {3, 4, 30},
    "CAS_EXT": {5, 13, 19}, "TESLA": {6, 8, 23}, "D7": {7, 33, 34},
    "SA_ST_A": {9, 12, 16}, "NEG_H": {11, 27, 36}, "C9": {14, 29, 31},
    "NQR17": {17, 22, 35}, "SEED": {18, 24, 32}, "SA_ST_B": {21, 25, 28},
}


def orbit_of(x):
    r = x % P
    if r == 0:
        return "SEAM"
    return next(k for k, v in ORBITS.items() if r in v)


def lines(g):
    """The 8 lines of a 3x3 grid held as a flat 9-tuple."""
    return [g[0:3], g[3:6], g[6:9], g[0::3], g[1::3], g[2::3],
            [g[0], g[4], g[8]], [g[2], g[4], g[6]]]


def census():
    magic, dr9, calib = [], [], []
    for p in permutations(range(1, 10)):
        L = lines(p)
        if all(sum(l) == 15 for l in L):
            magic.append(p)
        if all(sum(l) % 9 == 0 for l in L):
            dr9.append(p)
        if [p[0], p[4], p[8]] == [1, 2, 3] and [p[2], p[4], p[6]] == [4, 2, 5]:
            calib.append(p)
    return magic, dr9, calib


def antidiagonal_graph(S=(4, 5, 6, 7, 8, 9)):
    V = [(a, b) for a in S for b in S if a != b]
    adj = {v: [] for v in V}
    for a, b in V:
        for c, d in V:
            if (a, b) != (c, d) and ((a == c) ^ (b == d)):
                adj[(a, b)].append((c, d))
    return V, adj


def hamiltonian_cycle(V, adj):
    """Backtracking with a least-remaining-neighbours order. Returns a cycle
    as a list of vertices, or None."""
    start = V[0]
    used = {v: False for v in V}
    used[start] = True
    path = [start]

    def step():
        if len(path) == len(V):
            return start in adj[path[-1]]
        nxt = sorted(adj[path[-1]],
                     key=lambda x: sum(1 for y in adj[x] if not used[y]))
        for v in nxt:
            if not used[v]:
                used[v] = True
                path.append(v)
                if step():
                    return True
                used[v] = False
                path.pop()
        return False

    return path if step() else None


def main():
    print("=" * 78)
    print("THEOREM 422: DR-9 FAMILY, FORCED CALIBRATION COUNT, AND THE")
    print("             HAMILTONIAN ANTI-DIAGONAL CYCLE")
    print("=" * 78)

    magic, dr9, calib = census()

    print("\nPart 1: the three censuses over all 9! = 362880 arrangements")
    print("  magic squares (every line = 15):      %6d" % len(magic))
    print("  DR-9 grids  (every line = 0 mod 9):   %6d   (%.4f%%)"
          % (len(dr9), 100.0 * len(dr9) / 362880))
    print("  calibration grids (main/anti target): %6d   = 4! , forced"
          % len(calib))
    assert len(magic) == 8, "magic square count moved off 8"
    assert len(dr9) == 72, "DR-9 family size moved off 72"
    assert len(calib) == 24, "calibration count moved off 24 = 4!"

    print("\nPart 2: the supplied 'best' grids are not unique")
    claimed = (9, 8, 1, 7, 6, 5, 2, 4, 3)
    assert claimed in dr9, "the exhibited DR-9 grid is not in the family"
    print("  exhibited DR-9 grid is in the family:  True")
    print("  but the family has %d members, so 'best' has no unique argmax"
          % len(dr9))
    claimed_cal = (1, 6, 4, 7, 2, 8, 5, 9, 3)
    assert claimed_cal in calib
    print("  exhibited calibration grid is one of %d" % len(calib))

    print("\nPart 3: the 9th term of '9/8' is forced")
    totals = {sum(p) for p in permutations(range(1, 10))}
    print("  total over every arrangement: %s -> DR %d, always"
          % (totals, 1 + (45 - 1) % 9))
    assert totals == {45}, "the grand total is not constant"
    print("  so the score denominator is 8, not 9; 8/8 is the real result")

    print("\nPart 4: DR-9 and magic are disjoint, and forced to be")
    print("  magic line sum 15 -> DR %d ; DR-9 needs 9" % (1 + (15 - 1) % 9))
    assert not (set(magic) & set(dr9)), "a grid is both magic and DR-9"
    print("  intersection: empty  (15 = 6 mod 9, never 0)")

    print("\nPart 5: the anti-diagonal graph IS Hamiltonian")
    V, adj = antidiagonal_graph()
    deg = {len(a) for a in adj.values()}
    print("  vertices %d   degree %s   regular %s"
          % (len(V), deg, len(deg) == 1))
    assert len(V) == 30, "vertex count is not 30"
    cyc = hamiltonian_cycle(V, adj)
    assert cyc is not None, "no Hamiltonian cycle found"
    assert len(cyc) == 30 and len(set(cyc)) == 30, "not a Hamiltonian path"
    steps = set()
    for k in range(len(cyc)):
        a, b = cyc[k]
        c, d = cyc[(k + 1) % len(cyc)]
        steps.add((a != c) + (b != d))
    closes = cyc[0] in adj[cyc[-1]]
    print("  cycle found:            %s" % (cyc is not None))
    print("  returns to start:       %s   (run said False)" % closes)
    print("  digit changes per step: %s   (run said {1, 2})" % steps)
    print("  all single changes:     %s   (run said False)" % (steps == {1}))
    print("  first eight: %s ..." % (cyc[:8],))
    assert closes, "the cycle does not close"
    assert steps == {1}, "some step changes more than one digit"

    print("\nPart 6: GF(37)")
    for n, what in [(8, "magic squares"), (72, "DR-9 family"),
                    (24, "calibration = 4!"), (30, "graph vertices"),
                    (45, "grand total")]:
        print("  %-6d mod 37 = %-3d %-9s  %s" % (n, n % P, orbit_of(n), what))
    assert 45 % P == 8 % P, "45 and 8 no longer share a residue"
    print("  8 and 45 share residue 8 because 45 = 37 + 8 -- the seam.")
    print("  That is T104 Lemma 104.2, cited, not rediscovered.")

    print("\n" + "=" * 78)
    print("ALL ASSERTIONS PASS")
    print("=" * 78)


if __name__ == "__main__":
    sys.exit(main())
