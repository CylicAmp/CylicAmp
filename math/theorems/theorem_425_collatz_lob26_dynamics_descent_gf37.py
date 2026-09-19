# CLASS: THEOREM
"""
Theorem 425: the parity-branched Collatz map T on {0..36} is not induced by
the integer Collatz map, its 9-cycle is an artifact of reduction, and its
eventual image forbids any semiconjugacy onto T271's affine C

PRIOR ART, read before writing.
  lob_26_collatz_f37.py has T and its three cycles [1, 3, 9], the count
  "13 cycle elements, 24 basin nodes", and the Legendre symbol (3|37) = +1.
  It stops there. Everything below -- transients, sources, in-degrees,
  eventual image, the descent question, and which cycles are genuine -- is
  not in that file.
  T271 has C(x) = 3x+1 mod 37 as an affine bijection, fixed point 18, seam
  preimage 12. T346 has the group C and the 137-map generate. Neither treats
  the parity-branched map, which is a different object: C is a permutation
  and T is not.

    T(x) = 19x mod 37   if the representative x in {0..36} is even
    T(x) = 3x + 1 mod 37 if it is odd

  (19 = 2^-1 mod 37, and for an even representative 19x mod 37 really is the
  integer x/2, since x/2 < 37.)

================================================================================
1. THE DESCENT QUESTION, WHICH DECIDES WHAT T IS
================================================================================

  The integer Collatz map does NOT descend to Z/37Z.  Parity is not a
  function of a residue class mod 37, because 37 is odd and every class
  contains both parities.  One witness settles it:

      1 and 38 are congruent mod 37,
      Collatz(1)  = 4,   Collatz(38) = 19,   and 4 != 19 (mod 37).

  So T is not "the Collatz map in F_37".  T is the integer Collatz map
  applied to the CANONICAL REPRESENTATIVE and then reduced -- which is a
  choice of lift, not a field-theoretic construction.  It is a perfectly
  good self-map of a 37-element set; it is simply not a map on Z/37Z induced
  by Collatz, and its orbits are not Collatz orbits.

  WHICH STEPS SURVIVE THE LIFT.  A step loses nothing exactly when no
  reduction happens: x even (always, since x/2 < 37), or x odd with
  3x + 1 < 37, i.e. x <= 11.  Applied to the three cycles:

      {0}                                  no reduced step   GENUINE
      {1, 4, 2}                            no reduced step   GENUINE
      {7,22,11,34,17,15,9,28,14}           TWO reduced steps ARTIFACT
                                           17 -> 52 -> 15 and 15 -> 46 -> 9

  The 3-cycle is the real Collatz cycle 1 -> 4 -> 2 -> 1.  The 9-cycle is
  not a Collatz phenomenon: seven of its nine steps are genuine, and the two
  that are not are exactly the two that close it.  Follow 17 in the integers
  and it goes 17, 52, 26, 13, 40, 20, 10, 5, 16, 8, 4, 2, 1 -- into the
  3-cycle, not around a 9-cycle.

  This is the miss-test applied to the obvious reading: "T has a 9-cycle"
  could have meant something about Collatz, and it does not.

================================================================================
2. FULL FINITE DYNAMICS OF T  (the finite-dynamics skill's six items)
================================================================================

  (1) cycle type          [1, 3, 9] -- {0}, {1,4,2}, {7,22,11,34,17,15,9,28,14}
  (2) transients          24 of 37; maximum tail length 9
  (3) sources             9, with empty preimage:
                          {19, 23, 24, 25, 29, 30, 31, 35, 36}
  (4) in-degrees          0 -> 9 states, 1 -> 19 states, 2 -> 9 states
                          image size 28  (19 + 9 = 28, and 19 + 2*9 = 37)
  (5) eventual image      13 states, reached at depth 10, and it is EXACTLY
                          the union of the three cycles
  (6) permutation         NO -- 28 < 37

  T is therefore an attractor-plus-trees system, not a shuffle.  "Trajectory
  terminates" is the wrong word for any of it: only {0} is a fixed point;
  every other trajectory enters a 3- or 9-cycle and continues forever.

================================================================================
3. THE SEMICONJUGACY BOUND -- T AND T271's C CANNOT BE RELATED
================================================================================

  The corpus now holds two objects both called Collatz-on-37: T271's affine
  C(x) = 3x+1, a permutation with cycle type 1 + 18 + 18, and this T.  They
  are not two views of one system, and the eventual image closes it rather
  than merely suggesting it.

  If f is not a permutation with eventual image E, there is no surjective
  pi : X -> Y intertwining f with a permutation g on |Y| > |E| points:
  g^n(pi X) = pi(f^n X) is inside pi(E), so the left side has at most |E|
  elements, while pi onto and g bijective force it to be all of Y.

  Here |E| = 13.  Both C(x) = 3x+1 and the 137-map mu(x) = 26x are
  permutations of all 37 residues, and 37 > 13.  So

      no surjection intertwines T with C, and none intertwines T with mu.

  That is stronger than listing invariants that differ: differing invariants
  leave open that some map relates the two systems, and this rules out all
  of them at once.

================================================================================
4. GF(37), AND WHICH PARTS ARE FORCED
================================================================================

  The nine sources meet eight of the twelve orbits, C9 twice.  The cycle set
  has 13 elements and 13 is in CAS_EXT; 24 transients, 24 in SEED; 9 sources,
  9 in SA_ST_A.  Recorded, not leaned on.

  FORCED and carrying no information: 19 = 2^-1 (mod 37) is a definition;
  (3|37) = +1 is a Legendre symbol computation with no bearing on the cycle
  structure, and lob_26 says so itself; and in-degrees summing to 37 is the
  pigeonhole, not a finding.

  NOT FORCED and therefore reportable: the cycle type [1,3,9], the tail
  bound 9, the in-degree profile, and the fact that the eventual image is
  exactly the cycle set -- that last one says T has no "wandering" periodic
  structure above its cycles, which a general non-injective map need not
  satisfy at any finite depth.

  FALSIFICATION.  Any of: a fourth cycle; a tail longer than 9; a tenth or
  eighth source; an eventual image other than the 13 cycle elements; a pair
  a = b (mod 37) with Collatz(a) = Collatz(b) (mod 37) for ALL such pairs,
  which would make T descend after all; or a reduced step inside the
  3-cycle. All are asserted below.
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


def T(x):
    return (x * 19) % P if x % 2 == 0 else (3 * x + 1) % P


def collatz(n):
    return n // 2 if n % 2 == 0 else 3 * n + 1


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


def main():
    X = list(range(P))
    print("=" * 78)
    print("THEOREM 425: THE PARITY-BRANCHED COLLATZ MAP T ON {0..36}")
    print("=" * 78)

    print("\nPart 1: the integer Collatz map does NOT descend to Z/37Z")
    assert collatz(1) % P != collatz(38) % P
    print("  1 = 38 (mod 37), but Collatz(1)=%d and Collatz(38)=%d, and %d != %d"
          % (collatz(1), collatz(38), collatz(1) % P, collatz(38) % P))
    wit = [(a, b) for a in range(1, 200) for b in range(a + 1, 200)
           if a % P == b % P and collatz(a) % P != collatz(b) % P]
    print("  witnesses below 200: %d, first three %s" % (len(wit), wit[:3]))
    assert wit, "Collatz would descend, which it does not"
    print("  so T is Collatz on the canonical REPRESENTATIVE, then reduced.")

    print("\nPart 2: which cycles survive the lift")
    cyc = cycles_of(T, X)
    for c in cyc:
        red = [(x, 3 * x + 1) for x in c if x % 2 == 1 and 3 * x + 1 >= P]
        tag = "GENUINE" if not red else "ARTIFACT, reduced at %s" % red
        print("  len %-2d %-34s %s" % (len(c), c, tag))
    three = [c for c in cyc if len(c) == 3][0]
    nine = [c for c in cyc if len(c) == 9][0]
    assert not [x for x in three if x % 2 == 1 and 3 * x + 1 >= P]
    assert len([x for x in nine if x % 2 == 1 and 3 * x + 1 >= P]) == 2
    n = 17
    walk = [n]
    while n != 1:
        n = collatz(n)
        walk.append(n)
    print("  integer Collatz from 17: %s" % walk)
    assert walk[-3:] == [4, 2, 1], walk

    print("\nPart 3: full finite dynamics")
    cycset = set().union(*[set(c) for c in cyc])
    print("  (1) cycle type      %s" % sorted(len(c) for c in cyc))
    assert sorted(len(c) for c in cyc) == [1, 3, 9]

    def tail(x):
        k = 0
        while x not in cycset:
            x = T(x)
            k += 1
        return k
    tl = {x: tail(x) for x in X}
    print("  (2) transients      %d of %d, max tail %d"
          % (P - len(cycset), P, max(tl.values())))
    assert P - len(cycset) == 24 and max(tl.values()) == 9

    deg = Counter(T(x) for x in X)
    src = sorted(x for x in X if deg[x] == 0)
    print("  (3) sources         %d: %s" % (len(src), src))
    assert len(src) == 9
    dist = dict(sorted(Counter(deg[x] for x in X).items()))
    print("  (4) in-degrees      %s, image size %d"
          % (dist, len([x for x in X if deg[x] > 0])))
    assert dist == {0: 9, 1: 19, 2: 9}
    assert 19 + 2 * 9 == P and 19 + 9 == 28

    S, depth = set(X), 0
    while True:
        S2 = {T(x) for x in S}
        depth += 1
        if S2 == S:
            break
        S = S2
    print("  (5) eventual image  %d states at depth %d; == cycle set: %s"
          % (len(S), depth, S == cycset))
    assert len(S) == 13 and S == cycset and depth == 10
    assert len({T(x) for x in X}) != P
    print("  (6) permutation     No (image 28 < 37)")

    print("\nPart 4: the semiconjugacy bound")
    print("  |eventual image| = 13; C(x)=3x+1 and mu(x)=26x are permutations")
    print("  of all 37 residues, and 37 > 13, so NO surjection intertwines T")
    print("  with either. T271's C and this T are not two views of one system.")
    assert len({(3 * x + 1) % P for x in X}) == P       # C is a permutation
    assert len({(26 * x) % P for x in X}) == P          # mu is a permutation
    assert P > len(S)

    print("\nPart 5: GF(37), recorded not leaned on")
    print("  sources meet orbits: %s"
          % sorted({orbit_of(x) for x in src}))
    for v, what in ((13, "cycle elements"), (24, "transients"),
                    (9, "sources")):
        print("  %-3d %-16s mod 37 -> %s" % (v, what, orbit_of(v)))
    print("  forced, no information: 19 = 2^-1 (definition); (3|37)=+1 has no")
    print("  bearing on cycle structure (lob_26 says so); in-degrees sum to 37.")

    print("\n" + "=" * 78)
    print("ALL ASSERTIONS PASS")
    print("=" * 78)


if __name__ == "__main__":
    sys.exit(main())
