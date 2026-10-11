# CLASS: AUDIT
"""
Audit of a supplied "constructive test of the Discrete Resonant Lattice"
(pasted 2026-10-11; another tool's output, not the owner's own text).

The supplied construction: the circulant graph C_12(1,2,3,6) -- vertices
v0..v11 in the cyclic order A0..A5, B5..B0 with A_i = (2i, 3) and
B_i = (2i, -3), edges {v_i, v_(i+d)} for d in {1, 2, 3, 6} -- drawn with
straight segments, every pair of edges intersected in exact rationals.

=== 1. WHAT REPRODUCES -- all of it ===

    vertices 12, edges 42, every degree 7            (C_12(1,2,3,6): +-1, +-2,
                                                       +-3 and the self-inverse 6)
    proper crossing pairs 43, distinct points 25
    15 edge pairs at (5,0); 3 pairs each at (2,0) and (8,0)

The supplied code was run verbatim and every printed number matched. 43
was also reached by a second route (C1 below). The table that was meant to
list the 25 points arrived with every coordinate cell empty, so the points
are listed and asserted here (POINTS).

=== 2. WHAT IS FORCED ===

  F-a  The 15-pair concurrency at (5,0). The offset-6 edges are the perfect
       matching i <-> i+6, and the coordinates put v_(i+6) at the point
       reflection of v_i through (5,0): A_i = (2i,3) -> (10-2i,-3) = B_(5-i).
       A segment from a point to its reflection through c has midpoint c, so
       all six pass through (5,0) and give C(6,2) = 15 pairs. The paste calls
       this "a theorem of the chosen coordinates", which is right; the
       mechanism is that one line. It recurs in every centrally symmetric
       placement compatible with the matching (the regular 12-gon also has
       15 pairs at its centre) and vanishes without that symmetry (C3).
  F-b  12 / 42 / 7-regular are the definition of C_12(1,2,3,6).
  F-c  The order-4 symmetry (W2). The 12 points fill a 6 x 2 grid in the
       non-square rectangle [0,10] x [-3,3], whose isometry group has order
       4 (all 4 found by exact search, no more). In index terms the maps are
       i -> 5-i, i -> 11-i, i -> i+6 -- dihedral maps of Z/12, which preserve
       every circulant graph. Checked for all 63 connection sets
       S in {1..6}: the symmetry does not depend on {1,2,3,6}.

=== 3. WHAT DOES NOT HOLD AS STATED ===

  W1  "The set is symmetric about [blank] ... The three points on [blank]
      are their own reflections." The axis symbol was lost in transit, and
      two readings remain:
        - over the whole 25-point set (which is what "the set" in that
          sentence refers to): five points lie on y = 0, (1,0), (2,0),
          (5,0), (8,0), (9,0); one lies on x = 5. Three fits neither; the
          sentence omits (1,0) and (9,0).
        - over the points where more than one pair crosses: exactly three,
          (2,0), (5,0), (8,0), all on y = 0 -- matching section 5's "six-line
          central concurrency; two additional triple-crossing centers on the
          horizontal axis". On this reading "three" is right.
      The text does not settle which was meant.
  W2  "bilateral reflection symmetry" undercounts. The drawing -- edges and
      coordinates together -- is invariant under a group of order 4:
      x -> 10-x (index map i -> 5-i), y -> -y (i -> 11-i), and their
      product, the point reflection through (5,0) (i -> i+6). The 25 points
      are invariant under all four. Forced: see F-c.
  W3  Not checked in the paste: the drawing is DEGENERATE. 24 of the 42
      edges lie on the two row lines y = +-3. There are 20 (edge, vertex)
      pairs with a vertex strictly inside an edge it does not end at
      (A0-A3 passes through A1 and A2), and 66 edge pairs that are
      collinear and overlap along a segment. The supplied code skips all of
      it without a word, by three different branches: of the 66
      overlapping pairs, 40 share an endpoint (shared-vertex check) and 26
      reach `den == 0`; the 48 (row edge, cross-row edge) pairs that meet
      at a vertex inside the row edge fail the strict range test, 24 at
      u = 0 and 24 at t = 1. So only the 18 edges joining the two rows can
      cross (16 do; A0-B0 and A5-B5 cross nothing), and 43 counts crossings
      of a figure that is not a valid straight-line drawing of the graph --
      in it, A0-A3 cannot be told apart from the path A0-A1-A2-A3.

=== 4. WHAT STANDS, AND ITS GRADE ===

  C1  43 = the number of strict inversions among the 18 cross-row edges
      written as (x on top, x on bottom): two such segments cross exactly
      when their order flips. Independent of the supplied code path.
  C2  The point set: 25 exact rational points, listed in POINTS. Besides
      (5,0) the only multi-pair points are (2,0) and (8,0), three edges
      each, all offset-3 chords: A0-B2, A1-B1, A2-B0 and their mirror images
      A5-B3, A4-B4, A3-B5 under x -> 10-x.
  C3  The counts belong to the coordinates, not the graph. Same graph, same
      cyclic order, other placements:
          any STRICTLY convex position  111 crossing pairs (chords cross
                                         iff their endpoints interleave)
          regular 12-gon (Q(sqrt 3))    111 pairs, 73 points, 15 at the centre
                                         (60 points of 1 pair, 12 of 3, 1 of 15)
          integer parabola (k, k^2)     111 pairs, 111 points, no concurrency
          supplied two-row grid          43 pairs,  25 points, 15 at (5,0)
      The supplied grid is itself in weakly convex position -- the points
      run in cyclic order round the rectangle's boundary -- and its 111
      interleaving pairs split 43 proper + 48 touching at a vertex + 20
      collinear. 12, 42 and 7-regularity are facts of the graph; 111 is a
      fact of the graph with its cyclic order; 43, 25 and 73 are facts of
      particular coordinates.

=== CORRECTIONS (status history) ===

  First version, commit 9aef035 (2026-10-11). Eight independent agents, each
  writing its own exact-arithmetic code, were set to refute the findings.
  Five stood unchanged (reproduction, inversion route, symmetry, forced
  concurrency, triple points); three were refuted at the level of wording,
  each re-checked here before correcting:
    W1  said "three fits neither axis". The multi-pair reading makes three
        correct; both readings are now stated.
    W3  said the code drops the degenerate cases via `den == 0` or a
        parameter equal to 0. It uses three branches (shared vertex,
        den == 0, t or u at 0 or 1); counts above.
    C3  said "any convex position". It must be strictly convex: the
        supplied grid is weakly convex and gives 43, not 111.

  Grade: the supplied arithmetic is correct and reproducible; the
  concurrency is forced by the chosen central symmetry; the counts 43 and
  25 are properties of one degenerate placement.

=== 5. NOT ASSESSABLE FROM WHAT WAS SUPPLIED ===

  * "Axiom 8 is satisfied" / "the intended core of Axiom 9". Neither axiom's
    text is in this repository (the MWS framework's axioms in T190 stop at
    7 and concern digits). The paste paraphrases Axiom 8 as "12 vertices,
    42 edges, degree 7", which holds; the axioms themselves are needed to
    say more.
  * Nested diamonds / octahedral projections: undefined in the paste, which
    says so itself. UNVERIFIED.

=== RECORD (PROTOCOL.md) ===

  RLAT-1 COMPUTATIONAL RESULT | A4 (all 861 edge pairs checked, missed 0)
         | DIRECT-CALCULATION, INDEPENDENT-CROSS-CHECK, EXHAUSTIVE-FINITE
         | COMPUTATIONALLY VERIFIED | 12/42/7, 43 pairs, 25 points, 15 at (5,0)
  RLAT-2 PROPOSITION | A2 | SYMBOLIC | PROVED | 15-pair concurrency forced by
         central symmetry of the placement
  RLAT-3 COMPUTATIONAL RESULT | A4 | EXHAUSTIVE-FINITE | COMPUTATIONALLY
         VERIFIED | 24 row edges, 20 edge-through-vertex, 66 overlaps (W3)
  RLAT-4 COMPUTATIONAL RESULT | A4 | EXHAUSTIVE-FINITE, INDEPENDENT-CROSS-CHECK
         | COMPUTATIONALLY VERIFIED | other placements 111 / 73 / 111 (C3)
  RLAT-6 PROPOSITION | A4 | EXHAUSTIVE-FINITE, STRUCTURAL | PROVED | the
         order-4 symmetry is forced for every circulant on this grid (F-c)
  RLAT-5 PROPOSITION | A0 | NONE | UNVERIFIED | Axioms 8, 9; nested diamonds

=== STANDING FRAMEWORK RUN (CLAUDE.md; recorded, no connection claimed) ===

  12 -> SA_ST_A, j=4, DR 3     7 -> D7, j=8, prime, twin/cousin/sexy, safe
  42 -> 5 CAS_EXT, j=11, DR 6  43 -> 6 TESLA, j=3, prime, twin/cousin/sexy
  25 -> SA_ST_B, j=10, DR 7    15 -> DARK_A, j=1, DR 6
  Nothing in the lattice depends on these; they are the standing run only.

FALSIFICATION: any assertion below failing.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations
from math import comb

A = [(2 * i, 3) for i in range(6)]
B = [(2 * i, -3) for i in range(6)]
V = A + B[::-1]
E = sorted({tuple(sorted((i, (i + d) % 12))) for i in range(12) for d in (1, 2, 3, 6)})


def sub(p, q):
    return (p[0] - q[0], p[1] - q[1])


def cr(p, q):
    return p[0] * q[1] - p[1] * q[0]


def crossings(P, sign=lambda z: (z > 0) - (z < 0)):
    pts = {}
    for e, f in combinations(E, 2):
        if set(e) & set(f):
            continue
        p, q, r, s = P[e[0]], P[e[1]], P[f[0]], P[f[1]]
        a, b = sub(q, p), sub(s, r)
        den = cr(a, b)
        if sign(den) == 0:
            continue
        d = sub(r, p)
        t, u = cr(d, b) / den, cr(d, a) / den
        if sign(t) > 0 and sign(1 - t) > 0 and sign(u) > 0 and sign(1 - u) > 0:
            pts.setdefault((p[0] + t * a[0], p[1] + t * a[1]), []).append((e, f))
    return pts


# --- 1. reproduction ---
assert len(V) == 12 and len(E) == 42 and comb(12, 2) - 42 == 24
assert all(sum(i in e for e in E) == 7 for i in range(12))
Vf = [(F(x), F(y)) for x, y in V]
X = crossings(Vf)
assert sum(map(len, X.values())) == 43 and len(X) == 25
mult = {p: len(v) for p, v in X.items() if len(v) > 1}
assert mult == {(5, 0): 15, (2, 0): 3, (8, 0): 3}

POINTS = sorted([
    (F(1), F(0)), (F(9), F(0)), (F(2), F(0)), (F(8), F(0)), (F(5), F(0)),
    (F(4, 3), F(1)), (F(4, 3), F(-1)), (F(26, 3), F(1)), (F(26, 3), F(-1)),
    (F(5, 3), F(2)), (F(5, 3), F(-2)), (F(25, 3), F(2)), (F(25, 3), F(-2)),
    (F(2), F(9, 5)), (F(2), F(-9, 5)), (F(8), F(9, 5)), (F(8), F(-9, 5)),
    (F(16, 5), F(9, 5)), (F(16, 5), F(-9, 5)), (F(34, 5), F(9, 5)), (F(34, 5), F(-9, 5)),
    (F(20, 7), F(9, 7)), (F(20, 7), F(-9, 7)), (F(50, 7), F(9, 7)), (F(50, 7), F(-9, 7)),
])
assert sorted(X) == POINTS

# --- 2. forced: offset-6 edges join each vertex to its reflection through (5,0) ---
for i in range(12):
    j = (i + 6) % 12
    assert (V[i][0] + V[j][0], V[i][1] + V[j][1]) == (10, 0)
assert comb(6, 2) == 15
through_c = [e for e in E if cr(sub(V[e[1]], V[e[0]]), sub((5, 0), V[e[0]])) == 0
             and min(V[e[0]][0], V[e[1]][0]) < 5 < max(V[e[0]][0], V[e[1]][0])]
assert sorted(through_c) == sorted(tuple(sorted((i, i + 6))) for i in range(6))

# --- 3. W1: points fixed by each reflection, under both readings ---
assert sorted(p for p in X if p[1] == 0) == [(1, 0), (2, 0), (5, 0), (8, 0), (9, 0)]
assert [p for p in X if p[0] == 5] == [(5, 0)]
assert sorted(mult) == [(2, 0), (5, 0), (8, 0)]                # the multi-pair reading: 3

# --- C2: the triple points are offset-3 chords, mirror images of each other ---
NM = [f"A{i}" for i in range(6)] + [f"B{i}" for i in range(5, -1, -1)]
through = {pt: sorted({NM[a] + "-" + NM[b] for pair in X[pt] for a, b in pair})
           for pt in [(2, 0), (8, 0)]}
assert through[(2, 0)] == ["A0-B2", "A1-B1", "A2-B0"]
assert through[(8, 0)] == ["A3-B5", "A4-B4", "A5-B3"]
assert all(min((b - a) % 12, (a - b) % 12) == 3
           for pt in [(2, 0), (8, 0)] for pair in X[pt] for a, b in pair)

# --- 3. W2: the symmetry group has order 4 ---
maps = {
    "x->10-x": lambda p: (10 - p[0], p[1]),
    "y->-y": lambda p: (p[0], -p[1]),
    "point reflection": lambda p: (10 - p[0], -p[1]),
}
index = {"x->10-x": lambda i: (5 - i) % 12, "y->-y": lambda i: (11 - i) % 12,
         "point reflection": lambda i: (i + 6) % 12}
for k, g in maps.items():
    perm = [V.index(g(V[i])) for i in range(12)]
    assert perm == [index[k](i) for i in range(12)], k
    assert sorted(tuple(sorted((perm[a], perm[b]))) for a, b in E) == E, k
    assert sorted(g(p) for p in X) == POINTS, k

# F-c: exactly 4 isometries of the vertex set (exact search about the centroid) ...
C0 = [(F(x) - 5, F(y)) for x, y in V]
iso = 0
for q0 in C0:
    for q1 in C0:
        p0, p1 = C0[0], C0[1]
        det = p0[0] * p1[1] - p0[1] * p1[0]
        m = ((q0[0] * p1[1] - q1[0] * p0[1]) / det, (q1[0] * p0[0] - q0[0] * p1[0]) / det,
             (q0[1] * p1[1] - q1[1] * p0[1]) / det, (q1[1] * p0[0] - q0[1] * p1[0]) / det)
        orth = (m[0] ** 2 + m[2] ** 2 == 1 and m[1] ** 2 + m[3] ** 2 == 1
                and m[0] * m[1] + m[2] * m[3] == 0)
        if orth and {(m[0] * x + m[1] * y, m[2] * x + m[3] * y) for x, y in C0} == set(C0):
            iso += 1
assert iso == 4
# ... and every circulant C_12(S), S in {1..6}, is preserved by the three index maps
for mask in range(1, 64):
    ES = sorted({tuple(sorted((i, (i + d) % 12))) for i in range(12)
                 for d in range(1, 7) if mask >> (d - 1) & 1})
    for g in index.values():
        assert sorted({tuple(sorted((g(a), g(b)))) for a, b in ES}) == ES, mask

# --- 3. W3: the drawing is degenerate ---
row = [e for e in E if V[e[0]][1] == V[e[1]][1]]
assert len(row) == 24


def strictly_inside(k, e):
    p, q = V[e[0]], V[e[1]]
    return (k not in e and cr(sub(q, p), sub(V[k], p)) == 0
            and min(p[0], q[0]) < V[k][0] < max(p[0], q[0]))


inc = [(e, k) for e in E for k in range(12) if strictly_inside(k, e)]
assert len(inc) == 20
assert ((0, 3), 1) in inc and ((0, 3), 2) in inc            # A0-A3 through A1, A2


def overlap(e, f):
    (p, q), (r, s) = (V[e[0]], V[e[1]]), (V[f[0]], V[f[1]])
    if not (p[1] == q[1] == r[1] == s[1]):
        return False
    lo1, hi1 = sorted((p[0], q[0]))
    lo2, hi2 = sorted((r[0], s[0]))
    return min(hi1, hi2) > max(lo1, lo2)


OV = [(e, f) for e, f in combinations(E, 2) if overlap(e, f)]
assert len(OV) == 66
assert all(e not in row and f not in row for v in X.values() for e, f in v)


def supplied_route(e, f):
    """The branch of the supplied proper_intersection() that decides (e, f)."""
    if set(e) & set(f):
        return "shared"
    p, q, r, s = V[e[0]], V[e[1]], V[f[0]], V[f[1]]
    a, b = sub(q, p), sub(s, r)
    den = cr(a, b)
    if den == 0:
        return "den0"
    d = sub(r, p)
    t, u = F(cr(d, b), den), F(cr(d, a), den)
    if 0 < t < 1 and 0 < u < 1:
        return "proper"
    return "t0" if t == 0 else "t1" if t == 1 else "u0" if u == 0 else "u1" if u == 1 else "out"


assert Counter(supplied_route(e, f) for e, f in OV) == {"shared": 40, "den0": 26}
TOUCH = [tuple(sorted((r_, x))) for r_ in row for x in E if x not in row
         if any(strictly_inside(k, r_) for k in x)]
assert len(TOUCH) == 48
assert Counter(supplied_route(e, f) for e, f in TOUCH) == {"u0": 24, "t1": 24}
crossing_edges = {e for v in X.values() for pair in v for e in pair}
assert sorted(e for e in E if e not in row and e not in crossing_edges) == [(0, 11), (5, 6)]  # A0-B0, A5-B5

# --- 4. C1: 43 as inversions of the 18 cross-row edges ---
cross_row = [e for e in E if e not in row]
assert len(cross_row) == 18
tb = [tuple(V[k][0] for k in sorted(e, key=lambda k: -V[k][1])) for e in cross_row]
assert sum((a1 - a2) * (b1 - b2) < 0 for (a1, b1), (a2, b2) in combinations(tb, 2)) == 43

# --- 4. C3: other placements of the same graph ---
interleave = sum(1 for e, f in combinations(E, 2) if not set(e) & set(f)
                 and ((e[0] < f[0] < e[1]) != (e[0] < f[1] < e[1])))
assert interleave == 111
# the supplied grid is weakly convex (cyclic order round the rectangle) and gives 43, not 111
turns = [cr(sub(V[(i + 1) % 12], V[i]), sub(V[(i + 2) % 12], V[(i + 1) % 12])) for i in range(12)]
assert all(t <= 0 for t in turns) and turns.count(0) == 8
INTER = [(e, f) for e, f in combinations(E, 2) if not set(e) & set(f)
         and ((e[0] < f[0] < e[1]) != (e[0] < f[1] < e[1]))]
assert Counter(supplied_route(e, f) for e, f in INTER) == {"proper": 43, "u0": 24, "t1": 24, "den0": 20}

par = [(F(k), F(k * k)) for k in range(12)]
Xp = crossings(par)
assert sum(map(len, Xp.values())) == 111 and len(Xp) == 111


class Q3:
    """Exact a + b*sqrt(3)."""
    __slots__ = ("a", "b")

    def __init__(s, a, b=0):
        s.a, s.b = F(a), F(b)

    def _c(o):
        return o if isinstance(o, Q3) else Q3(o)

    def __add__(s, o):
        o = Q3._c(o)
        return Q3(s.a + o.a, s.b + o.b)

    __radd__ = __add__

    def __neg__(s):
        return Q3(-s.a, -s.b)

    def __sub__(s, o):
        return s + -Q3._c(o)

    def __rsub__(s, o):
        return Q3._c(o) - s

    def __mul__(s, o):
        o = Q3._c(o)
        return Q3(s.a * o.a + 3 * s.b * o.b, s.a * o.b + s.b * o.a)

    __rmul__ = __mul__

    def __truediv__(s, o):
        o = Q3._c(o)
        n = o.a * o.a - 3 * o.b * o.b
        return s * Q3(o.a / n, -o.b / n)

    def sign(s):
        if s.a == 0 and s.b == 0:
            return 0
        if s.a >= 0 and s.b >= 0:
            return 1
        if s.a <= 0 and s.b <= 0:
            return -1
        big_a = s.a * s.a > 3 * s.b * s.b
        return (1 if s.a > 0 else -1) if big_a else (1 if s.b > 0 else -1)

    def __eq__(s, o):
        o = Q3._c(o)
        return s.a == o.a and s.b == o.b

    def __hash__(s):
        return hash((s.a, s.b))


h = F(1, 2)
cos30 = [Q3(1), Q3(0, h), Q3(h), Q3(0), Q3(-h), Q3(0, -h),
         Q3(-1), Q3(0, -h), Q3(-h), Q3(0), Q3(h), Q3(0, h)]
reg = [(cos30[k], cos30[(k - 3) % 12]) for k in range(12)]
Xr = crossings(reg, sign=lambda z: z.sign())
assert sum(map(len, Xr.values())) == 111 and len(Xr) == 73
assert max(map(len, Xr.values())) == 15 and len(Xr[(Q3(0), Q3(0))]) == 15
assert Counter(map(len, Xr.values())) == {1: 60, 3: 12, 15: 1}

# --- standing framework run (recorded only) ---
ORB = {"SA_ST_A": {9, 12, 16}, "D7": {7, 33, 34}, "CAS_EXT": {5, 13, 19},
       "TESLA": {6, 8, 23}, "SA_ST_B": {21, 25, 28}, "DARK_A": {2, 15, 20}}
for n, o in [(12, "SA_ST_A"), (7, "D7"), (42, "CAS_EXT"), (43, "TESLA"),
             (25, "SA_ST_B"), (15, "DARK_A")]:
    assert n % 37 in ORB[o] and {n % 37 * 26 ** k % 37 for k in range(3)} == ORB[o]

if __name__ == "__main__":
    print("Supplied lattice: 12 vertices, 42 edges, 7-regular; 43 crossing pairs, "
          "25 points, 15 at (5,0) -- all reproduce.")
    print("Forced: (5,0) concurrency = central symmetry of the placement.")
    print("W1 five points on y=0 (three if only multi-pair points count); "
          "W2 symmetry group order 4, forced; W3 24 row edges, 20 edge-through-vertex, "
          "66 overlaps, dropped by three branches.")
    print("Same graph elsewhere: strictly convex 111 pairs; regular 12-gon 73 points; "
          "parabola 111 points; the weakly convex supplied grid 43.")
    print("All assertions passed.")
