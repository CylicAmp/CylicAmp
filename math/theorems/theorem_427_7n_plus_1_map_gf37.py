# CLASS: THEOREM
"""
Theorem 427: the 7n+1 map on GF(37), and the general order formula
|<A_m, mu>| = 37 * lcm(ord_37(m), 3) that subsumes T338, T346 and T426

PRIOR ART: 7n+1 and 7x+1 are absent from the corpus.  The analogues are
cited throughout: T271/T346 (3n+1), T337/T338 (2x+1), T425 (parity-branched
3n+1), T426 (5n+1), lob_26_collatz_f37.py.

    A_7(x) = 7x + 1 (mod 37)                     affine, a permutation
    W(x)   = 19x (mod 37) if the representative x in {0..36} is even
             7x + 1 (mod 37) if it is odd        parity-branched, not one

================================================================================
1. ord_37(7) = 9 -- A THIRD VALUE, AND A THIRD CYCLE TYPE
================================================================================

    ord_37(2)  = 36   primitive   sigma(x)=2x+1  1 + 36-cycle
    ord_37(3)  = 18   index 2     C(x)=3x+1      1 + two 18-cycles
    ord_37(5)  = 36   primitive   A_5(x)=5x+1    1 + 36-cycle
    ord_37(7)  =  9   index 4     A_7(x)=7x+1    1 + FOUR 9-cycles
    ord_37(26) =  3               mu(x)=26x      1 + twelve 3-cycles

  A_7 has fixed point 6 and seam preimage 21:
      A_7(x) = x  ->  6x = -1  ->  x = -6^-1 = -31 = 6   (6^-1 = 31)
      A_7(x) = 0  ->  x = -7^-1 = -16 = 21               (7^-1 = 16)
  6 is in TESLA, 21 is in SA_ST_B.  C has (18, 12) and A_5 has (9, 22), so
  no two of the three share a distinguished point.

================================================================================
2. THE GROUP ORDER IS A FORMULA, NOT A CASE ANALYSIS
================================================================================

  T338 found <sigma, mu> = all of AGL(1,37).  T346 found <C, mu> = 666,
  exactly half, and gave the reason as "3 is not a primitive root".  T426
  confirmed the complementary case for m = 5.  Adding m = 7 makes the shape
  visible, and it is a single formula:

      |<A_m, mu>|  =  37 * lcm( ord_37(m), 3 )        A_m(x) = mx+1

  verified by exhaustive construction for EVERY m in 2..36.

      m = 2   ord 36   ->  1332   all of AGL(1,37)
      m = 3   ord 18   ->   666   half                    (T346)
      m = 5   ord 36   ->  1332   all                     (T426)
      m = 7   ord  9   ->   333   a QUARTER
      m = 26  ord  3   ->   111   a twelfth

  WHY.  The linear parts of A_m and mu generate <m, 26> inside F_37*, a
  cyclic group, so that subgroup has order lcm(ord(m), ord(26)) =
  lcm(ord(m), 3).  The translation part is all of Z/37Z as soon as the
  linear part is non-trivial, because the commutator of a translation with
  a non-identity homothety is again a translation and 37 is prime.  Hence
  the product 37 * lcm(ord(m), 3).

  WHAT THIS DOES AND DOES NOT DO TO T346.  It subsumes T346's ORDER -- 666
  is the formula at ord(3) = 18, not a fact about the Collatz map as such.
  It does NOT subsume T346's second half: that file also identifies WHAT the
  missing coset is, the quadratic character of differences, and that
  description exists because index 2 subgroups are kernels of characters.
  At m = 7 the index is 4 and the missing three quarters are not a single
  character, so T346's characterisation is genuinely narrower than its order
  statement and remains its own.

================================================================================
3. THE PARITY-BRANCHED W, FULL DYNAMICS
================================================================================

  (1) cycle type      [1, 4, 5]   {0}  {1,8,4,2}  {5,36,18,9,27}
  (2) transients      27 of 37; maximum tail length 7
  (3) sources         9: {20, 21, 25, 26, 29, 30, 31, 34, 35}
  (4) in-degrees      0 -> 9, 1 -> 19, 2 -> 9; image size 28
  (5) eventual image  10 states at depth 8, exactly the union of the cycles
  (6) permutation     NO (28 < 37)

  The three parity-branched maps side by side:

      m   cycle type    transients  max tail  eventual image  depth
      3   [1,3,9]           24          9          13          10
      5   [1,1,3,7]         25         12          12          13
      7   [1,4,5]           27          7          10           8

  The shared in-degree profile {0:9, 1:19, 2:9} is part forced and was
  decomposed in T426: both branches are injective on 19 even and 18 odd
  representatives, so the profile is always {0:k, 1:37-2k, 2:k}, and k = 9
  for m in {3,5,7,9} but 10 for {11,13,15}, 12 for 17 and 1 for 19.  It is a
  block of multipliers sharing a k, not a property of these maps.

================================================================================
4. DESCENT FAILS; ONE CYCLE GENUINE, ONE INVENTED
================================================================================

  Parity is not a function of a residue class mod 37, so the integer map
  does not descend.  Witness: 1 = 38 (mod 37), 7*1+1 = 8, 38/2 = 19, and
  8 != 19 (mod 37).  W is the integer map on the canonical REPRESENTATIVE,
  then reduced.

  A step loses nothing when x is even, or x is odd with 7x+1 < 37, i.e.
  x <= 5.  The bar rises as m rises: x <= 11 for m=3, x <= 7 for m=5,
  x <= 5 for m=7.  Fewer and fewer steps survive the lift.

      {0}                   no reduced step         GENUINE
      {1, 8, 4, 2}          no reduced step         GENUINE
      {5, 36, 18, 9, 27}    9 -> 64, 27 -> 190      ARTIFACT

  And {1,8,4,2} is exactly the integer 7n+1 cycle 1 -> 8 -> 4 -> 2 -> 1,
  element for element and in order.  A search over starts 1..59 in the
  integers finds no other cycle, so unlike 5n+1 -- where two real cycles
  were invisible because they exceed 37 -- here W's genuine cycle may well
  be the whole periodic story.  "May well be" is the honest strength: the
  search is bounded and proves nothing.

  The same structural point as T425 and T426 stands, and harder: 7n+1 is
  more supercritical than 5n+1, yet W is a self-map of 37 states so every
  W-trajectory cycles.  That is forced by finiteness.  W cannot exhibit
  divergence, so its boundedness is not evidence about the integers.  T428
  makes the growth statement exact rather than heuristic.

  FALSIFICATION.  Any of: ord_37(7) != 9; |<A_7, mu>| != 333; the order
  formula failing for any m in 2..36; a fourth W-cycle; a tail longer than
  7; an eventual image other than the 10 cycle elements; or a reduced step
  inside {1,8,4,2}.  All are asserted below.
"""

import math
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


def group_order(m):
    Am = tuple((m * x + 1) % P for x in range(P))
    mu = tuple((26 * x) % P for x in range(P))
    ident = tuple(range(P))
    G, fr = {ident}, [ident]
    while fr:
        nxt = []
        for g in fr:
            for h in (Am, mu):
                c = tuple(h[g[x]] for x in range(P))
                if c not in G:
                    G.add(c)
                    nxt.append(c)
        fr = nxt
    return len(G)


def W(x):
    return (x * 19) % P if x % 2 == 0 else (7 * x + 1) % P


def integer_7n1(n):
    return n // 2 if n % 2 == 0 else 7 * n + 1


def main():
    X = list(range(P))
    print("=" * 78)
    print("THEOREM 427: THE 7n+1 MAP ON GF(37)")
    print("=" * 78)

    print("\nPart 1: ord_37(7) = 9, a third value")
    for a in (2, 3, 5, 7, 26):
        print("   ord_37(%-2d) = %d" % (a, order_of(a)))
    assert order_of(7) == 9
    A7 = lambda x: (7 * x + 1) % P
    fix = [x for x in X if A7(x) == x]
    seam = [x for x in X if A7(x) == 0]
    print("   A_7 fixed %s in %s, seam preimage %s in %s"
          % (fix, orbit_of(fix[0]), seam, orbit_of(seam[0])))
    assert fix == [6] and seam == [21]
    ct = [len(c) for c in cycles_of(A7, X)]
    print("   A_7 cycle type %s" % ct)
    assert ct == [1, 9, 9, 9, 9]

    print("\nPart 2: |<A_m, mu>| = 37 * lcm(ord_37(m), 3), for EVERY m")
    for m in range(2, P):
        o = order_of(m)
        pred = P * (o * 3 // math.gcd(o, 3))
        assert group_order(m) == pred, (m, o, group_order(m), pred)
    print("   verified by exhaustive construction for all m in 2..36 ✓")
    names = {1332: "all", 666: "half", 333: "a quarter", 111: "a twelfth"}
    for m in (2, 3, 5, 7, 26):
        g = group_order(m)
        print("   m=%-3d ord %-3d -> |G| = %-5d %s" % (m, order_of(m), g,
                                                       names.get(g, "")))
    assert group_order(3) == 666 and group_order(7) == 333
    assert group_order(2) == group_order(5) == 1332

    print("\nPart 3: full dynamics of W")
    cyc = cycles_of(W, X)
    cycset = set().union(*[set(c) for c in cyc])
    print("   (1) cycle type   %s" % [len(c) for c in cyc])
    for c in cyc:
        print("       len %-2d %s" % (len(c), c))
    assert sorted(len(c) for c in cyc) == [1, 4, 5]

    def tail(x):
        k = 0
        while x not in cycset:
            x = W(x)
            k += 1
        return k
    tl = {x: tail(x) for x in X}
    deg = Counter(W(x) for x in X)
    src = sorted(x for x in X if deg[x] == 0)
    dist = dict(sorted(Counter(deg[x] for x in X).items()))
    print("   (2) transients   %d of %d, max tail %d"
          % (P - len(cycset), P, max(tl.values())))
    print("   (3) sources      %d: %s" % (len(src), src))
    print("   (4) in-degrees   %s, image %d" % (dist, len({W(x) for x in X})))
    assert P - len(cycset) == 27 and max(tl.values()) == 7
    assert len(src) == 9 and dist == {0: 9, 1: 19, 2: 9}

    S, depth = set(X), 0
    while True:
        S2 = {W(x) for x in S}
        depth += 1
        if S2 == S:
            break
        S = S2
    print("   (5) eventual img %d at depth %d, == cycle set: %s"
          % (len(S), depth, S == cycset))
    print("   (6) permutation  No (%d < %d)" % (len({W(x) for x in X}), P))
    assert len(S) == 10 and S == cycset and depth == 8
    assert len({W(x) for x in X}) != P

    print("\nPart 4: descent fails; genuine vs invented")
    assert integer_7n1(1) % P != integer_7n1(38) % P
    print("   1 = 38 (mod 37): 7*1+1 = 8, 38/2 = 19, and 8 != 19 (mod 37)")
    for c in cyc:
        red = [(x, 7 * x + 1) for x in c if x % 2 == 1 and 7 * x + 1 >= P]
        print("   %-24s %s" % (c, "GENUINE" if not red
                               else "ARTIFACT, reduced at %s" % red))
    four = [c for c in cyc if len(c) == 4][0]
    assert not [x for x in four if x % 2 == 1 and 7 * x + 1 >= P]
    walk, n = [1], integer_7n1(1)
    while n != 1:
        walk.append(n)
        n = integer_7n1(n)
    print("   integer 7n+1 cycle from 1: %s" % walk)
    assert walk == four == [1, 8, 4, 2]
    print("   genuine-step bar by multiplier: x<=11 (m=3), x<=7 (m=5), x<=5 (m=7)")
    for m, b in ((3, 11), (5, 7), (7, 5)):
        assert m * b + 1 < P <= m * (b + 2) + 1
    print("   fewer steps survive the lift as m grows ✓")

    print("\n   side by side:")
    print("   m   cycle type    transients  max tail  eventual  depth")
    print("   3   [1,3,9]           24          9        13       10")
    print("   5   [1,1,3,7]         25         12        12       13")
    print("   7   [1,4,5]           27          7        10        8")

    print("\n" + "=" * 78)
    print("ALL ASSERTIONS PASS")
    print("=" * 78)


if __name__ == "__main__":
    sys.exit(main())
