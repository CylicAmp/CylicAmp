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

=== 3. WHAT DOES NOT HOLD AS STATED ===

  W1  "The three points on [the axis] are their own reflections." The
      reflection named in section 1 is about the horizontal axis y = 0.
      Five crossing points lie on it: (1,0), (2,0), (5,0), (8,0), (9,0).
      On the vertical line x = 5 there is one, (5,0). Three fits neither.
      (The axis symbol was lost in transit; both readings are checked.)
  W2  "bilateral reflection symmetry" undercounts. The drawing -- edges and
      coordinates together -- is invariant under a group of order 4:
      x -> 10-x (index map i -> 5-i), y -> -y (i -> 11-i), and their
      product, the point reflection through (5,0) (i -> i+6). All three are
      automorphisms of C_12(1,2,3,6) realised geometrically. The 25 points
      are invariant under all four.
  W3  Not checked in the paste: the drawing is DEGENERATE. 24 of the 42
      edges lie on the two row lines y = +-3. Of those, 20 (edge, vertex)
      pairs have a vertex strictly inside an edge it does not end at
      (A0-A3 passes through A1 and A2), and 66 edge pairs are collinear and
      overlap along a segment. The supplied code skips them without a word:
      `den == 0` drops collinear pairs, and the strict 0 < t, u test drops
      an edge meeting a vertex. So only the 18 edges joining the two rows
      can cross, and 43 counts crossings of a figure that is not a valid
      straight-line drawing of the graph -- in it, A0-A3 cannot be told apart
      from the path A0-A1-A2-A3.

=== 4. WHAT STANDS, AND ITS GRADE ===

  C1  43 = the number of strict inversions among the 18 cross-row edges
      written as (x on top, x on bottom): two such segments cross exactly
      when their order flips. Independent of the supplied code path.
  C2  The point set: 25 exact rational points, listed in POINTS.
  C3  The counts belong to the coordinates, not the graph. Same graph, other
      placements in cyclic order:
          any convex position          111 crossing pairs (chords interleave)
          regular 12-gon (Q(sqrt 3))   111 pairs, 73 points, 15 at the centre
          integer parabola (k, k^2)    111 pairs, 111 points, no concurrency
          supplied two-row grid         43 pairs,  25 points, 15 at (5,0)
      Only 12, 42 and 7-regularity are facts about C_12(1,2,3,6).

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
  RLAT-4 COMPUTATIONAL RESULT | A4 | EXHAUSTIVE-FINITE | COMPUTATIONALLY
         VERIFIED | other placements 111 / 73 / 111 (C3)
  RLAT-5 PROPOSITION | A0 | NONE | UNVERIFIED | Axioms 8, 9; nested diamonds

=== STANDING FRAMEWORK RUN (CLAUDE.md; recorded, no connection claimed) ===

  12 -> SA_ST_A, j=4, DR 3     7 -> D7, j=8, prime, twin/cousin/sexy, safe
  42 -> 5 CAS_EXT, j=11, DR 6  43 -> 6 TESLA, j=3, prime, twin/cousin/sexy
  25 -> SA_ST_B, j=10, DR 7    15 -> DARK_A, j=1, DR 6
  Nothing in the lattice depends on these; they are the standing run only.

FALSIFICATION: any assertion below failing.
"""
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

# --- 3. W1: points fixed by each reflection ---
assert sorted(p for p in X if p[1] == 0) == [(1, 0), (2, 0), (5, 0), (8, 0), (9, 0)]
assert [p for p in X if p[0] == 5] == [(5, 0)]

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


assert sum(overlap(e, f) for e, f in combinations(E, 2)) == 66
assert all(e not in row and f not in row for v in X.values() for e, f in v)

# --- 4. C1: 43 as inversions of the 18 cross-row edges ---
cross_row = [e for e in E if e not in row]
assert len(cross_row) == 18
tb = [tuple(V[k][0] for k in sorted(e, key=lambda k: -V[k][1])) for e in cross_row]
assert sum((a1 - a2) * (b1 - b2) < 0 for (a1, b1), (a2, b2) in combinations(tb, 2)) == 43

# --- 4. C3: other placements of the same graph ---
interleave = sum(1 for e, f in combinations(E, 2) if not set(e) & set(f)
                 and ((e[0] < f[0] < e[1]) != (e[0] < f[1] < e[1])))
assert interleave == 111

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
    print("W1 five points on y=0, not three; W2 symmetry group order 4; "
          "W3 24 row edges, 20 edge-through-vertex, 66 overlaps.")
    print("Same graph elsewhere: convex 111 pairs; regular 12-gon 73 points; "
          "parabola 111 points.")
    print("All assertions passed.")
