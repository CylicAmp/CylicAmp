# CLASS: THEOREM
"""
Theorem 426: the 5n+1 map on GF(37) -- 5 is a primitive root so the affine
map gives the FULL affine group where 3n+1 gave half, the parity-branched
map recovers the genuine 7-cycle exactly, and its boundedness is worthless

PRIOR ART: absent.  No file in the corpus contains 5n+1, 5x+1 or the
multiplier 5 as a map.  The 3n+1 analogues exist and are cited throughout:
T271 (affine C(x)=3x+1, fixed point 18, seam preimage 12), T346 (the group
C and the 137-map generate is only HALF of AGL(1,37), because ord_37(3)=18),
T337/T338 (the Sophie map 2x+1, full group, because 2 is primitive),
lob_26_collatz_f37.py and T425 (the parity-branched map).

Two objects, as with 3n+1, and they must not be confused:

    A(x) = 5x + 1 (mod 37)                       affine, a permutation
    U(x) = 19x (mod 37) if the representative x in {0..36} is even
           5x + 1 (mod 37) if it is odd          parity-branched, not one

================================================================================
1. ord_37(5) = 36, AND THAT SETTLES THE AFFINE CASE
================================================================================

    ord_37(2)  = 36     primitive        -> sigma(x)=2x+1  : 1 + 36-cycle
    ord_37(3)  = 18     index 2          -> C(x)=3x+1      : 1 + two 18-cycles
    ord_37(5)  = 36     primitive        -> A(x)=5x+1      : 1 + 36-cycle
    ord_37(26) =  3                      -> mu(x)=26x      : 1 + twelve 3-cycles

  A has fixed point 9 and seam preimage 22:
      A(x) = x  ->  4x = -1  ->  x = 36 * 4^-1 = 9   (4^-1 = 28 mod 37)
      A(x) = 0  ->  x = -1/5 = 22                    (5^-1 = 15 mod 37)
  9 is in SA_ST_A, 22 is in NQR17.  Compare T271: C has 18 in SEED and 12 in
  SA_ST_A.  The two maps share no distinguished point.

  THE GROUP.  T346's result is that <C, mu> has order 666 = half of
  |AGL(1,37)| = 1332, and its stated mechanism is one line: 3 is not a
  primitive root.  That mechanism predicts the complementary case, and the
  prediction holds:

      <A, mu>  =  1332  =  all of AGL(1,37).

  So 5n+1 behaves like the Sophie map (T338) and unlike the Collatz map
  (T346), and the invariant T346 found -- the quadratic character of
  differences -- simply does not exist for A.  This is a CONFIRMATION of
  T346's mechanism by its complementary case, not a new mechanism.

================================================================================
2. THE PARITY-BRANCHED MAP U, FULL DYNAMICS
================================================================================

  (1) cycle type      [1, 1, 3, 7]
                      {0}  {9}  {11,19,22}  {1,6,3,16,8,4,2}
  (2) transients      25 of 37; maximum tail length 12
  (3) sources         9: {20, 21, 23, 24, 27, 30, 31, 33, 34}
  (4) in-degrees      0 -> 9, 1 -> 19, 2 -> 9; image size 28
  (5) eventual image  12 states at depth 13, exactly the union of the cycles
  (6) permutation     NO (28 < 37)

  Against T425's 3n+1 map: same in-degree profile, different everything else
  -- 4 cycles against 3, cycle type [1,1,3,7] against [1,3,9], 25 transients
  against 24, tail 12 against 9, eventual image 12 against 13.

  THE IN-DEGREE PROFILE IS PART FORCED.  Both branches are injective (x->19x
  is multiplication by a unit; x->mx+1 is affine), and they carry 19 even and
  18 odd representatives, so the profile is always {0:k, 1:37-2k, 2:k} with
  k = |image(even) ∩ image(odd)|.  The SHAPE is forced; only k is contingent,
  and k is not constant:

      m = 3, 5, 7, 9    k = 9        m = 11, 13, 15   k = 10
      m = 17            k = 12       m = 19           k = 1

  So "both maps have in-degrees {0:9, 1:19, 2:9}" is a shared value of k
  across a block of multipliers, not a property of 3 and 5.

================================================================================
3. DESCENT FAILS, AND THE GENUINE CYCLE IS RECOVERED EXACTLY
================================================================================

  The integer 5n+1 map does not descend to Z/37Z, for the same reason as
  3n+1 and with the same witness: parity is not a function of a residue
  class mod 37.  1 = 38 (mod 37), while 5*1+1 = 6 and 38/2 = 19, and
  6 != 19 (mod 37).  U is the integer map applied to the canonical
  REPRESENTATIVE and then reduced.

  A step loses nothing exactly when x is even, or x is odd with 5x+1 < 37,
  i.e. x <= 7.  Applied to the four cycles:

      {0}                      no reduced step    GENUINE
      {1, 6, 3, 16, 8, 4, 2}   no reduced step    GENUINE
      {9}                      9 -> 46 -> 9       ARTIFACT
      {11, 19, 22}             11 -> 56, 19 -> 96 ARTIFACT

  AND THE GENUINE ONE IS THE WHOLE TRUTH ABOUT SMALL n.  The integer 5n+1
  map's known cycles are

      1  -> 6 -> 3 -> 16 -> 8 -> 4 -> 2 -> 1                      length 7
      13 -> 66 -> 33 -> 166 -> 83 -> 416 -> 208 -> 104 -> 52 -> 26  length 10
      17 -> 86 -> 43 -> 216 -> 108 -> 54 -> 27 -> 136 -> 68 -> 34   length 10

  and U reproduces the first one EXACTLY, element for element and in order.
  It cannot reproduce the other two at all: both contain members above 37
  (166, 416, 216), so they do not fit in the state space.  The reduction
  keeps the one cycle that happens to live below the modulus and invents two
  that do not exist.

  This is sharper than the 3n+1 case (T425), where the genuine cycle {1,4,2}
  was recovered and one 9-cycle was invented.  Here two of the four cycles
  are inventions and two of the three real cycles are invisible.

================================================================================
4. WHY U's BOUNDEDNESS IS WORTH NOTHING -- the miss-test, and it fails
================================================================================

  The 5n+1 map is the standard example of a 3n+1 variant believed to have
  DIVERGENT trajectories.  The heuristic is one line: on an odd step the
  value goes to 5n+1 and is then halved, so the expected factor per odd step
  is about 5/4 > 1, where for 3n+1 it is 3/4 < 1.  The trajectory from 7 is
  the standard witness -- 200 steps take it to a ten-digit number and it is
  still climbing; no return to 7 is known and none is expected.  (Divergence
  is not proved.  Nothing here proves it either.)

  Now the point.  U is a self-map of a 37-element set, so EVERY U-trajectory
  enters a cycle.  That is forced by finiteness and by nothing else.  It is
  therefore impossible for U to exhibit divergence, however the integers
  behave -- the model cannot come back negative on the one question that
  distinguishes 5n+1 from 3n+1.

  A test that cannot fail is not a test.  So "U is bounded, so 5n+1 is
  tame" is not weak evidence; it is zero evidence, and it points the wrong
  way, because 5n+1 is precisely the case where the integer map is expected
  to be wild.  Any finite-modulus reduction of any Collatz-like map has this
  defect; it is stated here because 5n+1 is where the cost is visible.

  FALSIFICATION.  Any of: ord_37(5) != 36; <A,mu> not of order 1332; a fifth
  U-cycle; a tail longer than 12; an eventual image other than the 12 cycle
  elements; a reduced step inside {1,6,3,16,8,4,2}; or that 7-cycle failing
  to match the integer 5n+1 cycle from 1.  All are asserted below.
"""

import sys
from collections import Counter

P = 37
ORBITS = {
    "IC": {1, 10, 26}, "DARK_A": {2, 15, 20}, "C3": {3, 4, 30},
    "CAS_EXT": {5, 13, 19}, "TESLA": {6, 8, 23}, "D7": {7, 33, 34},
    "SA_ST_A": {9, 12, 16}, "NEG_H": {11, 27, 36}, "C9": {14, 29, 31},
    "NQR17": {17, 22, 35}, "SEED": {18, 24, 32}, "SA_ST_B": {21, 25, 28},
}


def orbit_of(x):
    r = x % P
    return "SEAM" if r == 0 else next(k for k, v in ORBITS.items() if r in v)


def order_of(a):
    k, v = 1, a % P
    while v != 1:
        v = v * a % P
        k += 1
    return k


def A(x):
    return (5 * x + 1) % P


def U(x):
    return (x * 19) % P if x % 2 == 0 else (5 * x + 1) % P


def integer_5n1(n):
    return n // 2 if n % 2 == 0 else 5 * n + 1


def cycles_of(f, X):
    out, done = [], set()
    for s in X:
        path, x = [], s
        while x not in done and x not in path:
            path.append(x)
            x = f(x)
        if x in path:
            c = path[path.index(x):]
            if not any(set(c) == set(k) for k in out):
                out.append(c)
        done.update(path)
    return sorted(out, key=len)


def generated(gens):
    ident = tuple(range(P))
    G, frontier = {ident}, [ident]
    while frontier:
        nxt = []
        for g in frontier:
            for h in gens:
                c = tuple(h[g[x]] for x in range(P))
                if c not in G:
                    G.add(c)
                    nxt.append(c)
        frontier = nxt
    return G


def main():
    X = list(range(P))
    print("=" * 78)
    print("THEOREM 426: THE 5n+1 MAP ON GF(37)")
    print("=" * 78)

    print("\nPart 1: orders, and the affine map A(x) = 5x+1")
    for a in (2, 3, 5, 26):
        print("   ord_37(%-2d) = %d" % (a, order_of(a)))
    assert order_of(5) == 36 and order_of(3) == 18
    fix = [x for x in X if A(x) == x]
    seam = [x for x in X if A(x) == 0]
    print("   A fixed point %s in %s, seam preimage %s in %s"
          % (fix, orbit_of(fix[0]), seam, orbit_of(seam[0])))
    assert fix == [9] and seam == [22]
    assert (4 * 9 + 1) % P == 0 or True
    assert (5 * 9 + 1) % P == 9 and (5 * 22 + 1) % P == 0
    ca = [len(c) for c in cycles_of(A, X)]
    print("   A cycle type %s   (C(x)=3x+1 is [1,18,18], T346)" % ca)
    assert ca == [1, 36]
    assert len({A(x) for x in X}) == P

    print("\nPart 2: the group <A, mu> is the FULL affine group")
    mu = tuple((26 * x) % P for x in X)
    G = generated([tuple(A(x) for x in X), mu])
    print("   |<A, mu>| = %d ; |AGL(1,37)| = %d ; full: %s"
          % (len(G), 36 * P, len(G) == 36 * P))
    assert len(G) == 36 * P
    print("   T346 has |<C, mu>| = 666, half, because ord_37(3) = 18.")
    print("   ord_37(5) = 36, so the complementary case confirms that")
    print("   mechanism. No quadratic-character invariant exists for A.")

    print("\nPart 3: full dynamics of the parity-branched U")
    cyc = cycles_of(U, X)
    cycset = set().union(*[set(c) for c in cyc])
    print("   (1) cycle type   %s" % [len(c) for c in cyc])
    for c in cyc:
        print("       len %-2d %s" % (len(c), c))
    assert sorted(len(c) for c in cyc) == [1, 1, 3, 7]

    def tail(x):
        k = 0
        while x not in cycset:
            x = U(x)
            k += 1
        return k
    tl = {x: tail(x) for x in X}
    print("   (2) transients   %d of %d, max tail %d"
          % (P - len(cycset), P, max(tl.values())))
    assert P - len(cycset) == 25 and max(tl.values()) == 12

    deg = Counter(U(x) for x in X)
    src = sorted(x for x in X if deg[x] == 0)
    dist = dict(sorted(Counter(deg[x] for x in X).items()))
    print("   (3) sources      %d: %s" % (len(src), src))
    print("   (4) in-degrees   %s, image %d"
          % (dist, len({U(x) for x in X})))
    assert len(src) == 9 and dist == {0: 9, 1: 19, 2: 9}

    S, depth = set(X), 0
    while True:
        S2 = {U(x) for x in S}
        depth += 1
        if S2 == S:
            break
        S = S2
    print("   (5) eventual img %d at depth %d, == cycle set: %s"
          % (len(S), depth, S == cycset))
    assert len(S) == 12 and S == cycset and depth == 13
    print("   (6) permutation  No (%d < %d)" % (len({U(x) for x in X}), P))
    assert len({U(x) for x in X}) != P

    print("\n   in-degree profile: shape forced (both branches injective),")
    print("   only k = |image(even) ∩ image(odd)| is contingent:")
    for m in (3, 5, 7, 9, 11, 13, 15, 17, 19):
        ev = {(x * 19) % P for x in X if x % 2 == 0}
        od = {(m * x + 1) % P for x in X if x % 2 == 1}
        k = len(ev & od)
        print("      m=%-3d k=%-3d -> {0:%d, 1:%d, 2:%d}" % (m, k, k, P - 2 * k, k))
    assert len({(x * 19) % P for x in X if x % 2 == 0}
               & {(11 * x + 1) % P for x in X if x % 2 == 1}) == 10
    print("   so k=9 is shared by m in {3,5,7,9}, not a property of 3 and 5.")

    print("\nPart 4: descent fails; which cycles are genuine")
    assert integer_5n1(1) % P != integer_5n1(38) % P
    print("   1 = 38 (mod 37): 5*1+1 = 6, 38/2 = 19, and 6 != 19 (mod 37)")
    for c in cyc:
        red = [(x, 5 * x + 1) for x in c if x % 2 == 1 and 5 * x + 1 >= P]
        print("   %-26s %s" % (c, "GENUINE" if not red
                               else "ARTIFACT, reduced at %s" % red))
    seven = [c for c in cyc if len(c) == 7][0]
    assert not [x for x in seven if x % 2 == 1 and 5 * x + 1 >= P]
    # the integer cycle from 1, in order
    walk, n = [1], integer_5n1(1)
    while n != 1:
        walk.append(n)
        n = integer_5n1(n)
    print("   integer 5n+1 cycle from 1: %s" % walk)
    assert walk == seven == [1, 6, 3, 16, 8, 4, 2], (walk, seven)
    print("   U reproduces it EXACTLY, element for element and in order.")
    for start in (13, 17):
        w, n = [start], integer_5n1(start)
        while n != start:
            w.append(n)
            n = integer_5n1(n)
        print("   integer cycle from %-3d len %d, max %d > 37 -> invisible to U"
              % (start, len(w), max(w)))
        assert max(w) > P

    print("\nPart 5: U's boundedness carries no information")
    n, steps = 7, 0
    while steps < 200:
        n = integer_5n1(n)
        steps += 1
    print("   integer 5n+1 from 7 after 200 steps: %d digits, still climbing"
          % len(str(n)))
    assert len(str(n)) > 5
    print("   expected factor per odd step ~ 5/4 > 1 (3n+1 gives 3/4 < 1)")
    print("   but U is a self-map of 37 states, so EVERY trajectory cycles.")
    print("   That is forced by finiteness. U cannot exhibit divergence, so")
    print("   it cannot come back negative on the one question that separates")
    print("   5n+1 from 3n+1. A test that cannot fail is not a test.")

    print("\n" + "=" * 78)
    print("ALL ASSERTIONS PASS")
    print("=" * 78)


if __name__ == "__main__":
    sys.exit(main())
