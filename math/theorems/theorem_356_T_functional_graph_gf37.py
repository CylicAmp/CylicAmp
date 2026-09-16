# CLASS: THEOREM
"""
Theorem 356: T descends to a well-defined map on the quotient, whose graph
is one 6-cycle fed by two transient chains of length three
Author: Michael Warren Song (CyclicAmp)

T355 concluded that of the four maps in the family, exactly one carries
information: T itself.  This is that map, worked out completely.

=== T DESCENDS TO THE QUOTIENT ===

    T(x) = x^3 + 33 is constant on every 137-orbit, because the fibres of
    cubing ARE the orbits (T349).  So T induces a well-defined map phi on
    the twelve orbits:

        IC      -> D7          SA_ST_A -> NQR17
        D7      -> TESLA       NQR17   -> SA_ST_B
        TESLA   -> NEG_H       SA_ST_B -> D7
        NEG_H   -> SEED        C9      -> DARK_A
        SEED    -> CAS_EXT     DARK_A  -> C3
        CAS_EXT -> IC          C3      -> TESLA

        SEAM    -> D7

=== THE STRUCTURE OF phi ===

    ONE cycle, of length 6:

        IC -> D7 -> TESLA -> NEG_H -> SEED -> CAS_EXT -> IC

    and TWO transient chains of length three feeding into it:

        C9      -> DARK_A -> C3      -> TESLA     (enters at TESLA)
        SA_ST_A -> NQR17  -> SA_ST_B -> D7        (enters at D7)

    plus the seam, which drops straight onto D7.

    Six orbits on the cycle, six transient -- an exact split, and the two
    transient chains have EQUAL LENGTH, entering at two distinct cycle
    points.

    CORRECTION TO AN EARLIER WORDING.  This was first described as a
    "symmetric" structure.  That is wrong, not merely undefined.  Equal
    chain length is not a symmetry: a symmetry would be a graph
    automorphism exchanging the two chains, and none exists.  Any
    automorphism must rotate the 6-cycle, the two entry points sit at
    ADJACENT cycle positions 1 (D7) and 2 (TESLA), and no rotation of a
    6-cycle transposes two adjacent points -- checked for all six
    rotations, none swaps them and only the identity preserves the pair as
    a set.  So the graph has no symmetry relating the chains; they are
    merely the same length.

    What is established, separately and in order:

      (a) phi is WELL DEFINED on the quotient     -- theorem, from T349
      (b) phi has exactly one cycle, length 6     -- computed
      (c) two transient chains, both length 3     -- computed
      (d) entering at distinct, adjacent points   -- computed
      (e) no automorphism exchanges them          -- computed

    (a) is the structural fact; (b)-(e) are the measured shape.  The two
    should not be stated as one claim, and "complete" and "symmetric" are
    not defined terms in this framework, so neither belongs in the
    statement.

=== THE STATE-LEVEL PICTURE AGREES ===

        level 0   6 states    the six cycle points, one per cycle orbit
        level 1  12 states    the other two members of each cycle orbit
        level 2   7 states    C3, SA_ST_B, and the seam
        level 3   6 states    DARK_A, NQR17
        level 4   6 states    C9, SA_ST_A

    Levels 0 and 1 together are exactly the six cycle orbits, complete.
    Each cycle orbit contributes its one cycle point and its two other
    members as level-1 leaves.  In-degrees are 3 on the twelve image points
    and 1 at 33 (the image of the seam); the remaining twenty-four states
    have no preimage at all.

    So every cycle point c is fed by exactly one orbit -- namely T^-1(c) --
    and that orbit is itself one of the six on the cycle.  The six orbits
    feeding the cycle and the six orbits ON the cycle are the SAME six.

=== INDICES, REPORTED WITHOUT CLAIM ===

        on-cycle    {0, 3, 5, 6, 8, 11}
        transient   {1, 2, 4, 7, 9, 10}

    Three of the six on-cycle orbits lie in T331's 37-sum half, three in
    the 74-sum half; three have even index and three odd.  Both splits are
    even, and no finer pattern in the index was found.  Recorded as
    measured, with no structure asserted.

    Note phi is NOT the cubing map on indices.  Cubing alone would send
    index j to 3j (mod 12), which is not injective since gcd(3,12) = 3 --
    it collapses.  The additive 33 is what makes phi a map worth drawing.

=== FALSIFICATION ===
    An orbit on which T is not constant; a second cycle of phi; or a
    transient chain of length other than three.
"""

P = 37
ORBITS = {
    'IC': (1, 10, 26),      'DARK_A': (2, 15, 20),  'C3': (3, 4, 30),
    'CAS_EXT': (5, 13, 19), 'TESLA': (6, 8, 23),    'D7': (7, 33, 34),
    'SA_ST_A': (9, 12, 16), 'NEG_H': (11, 27, 36),  'C9': (14, 29, 31),
    'NQR17': (17, 22, 35),  'SEED': (18, 24, 32),   'SA_ST_B': (21, 25, 28),
}
BY = {r: n for n, o in ORBITS.items() for r in o}
IDX = {BY[pow(2, j, P)]: j for j in range(12)}
T = lambda x: (pow(x, 3, P) + 33) % P


def run():
    from collections import Counter

    # --- T is constant on orbits ---
    phi, img = {}, {}
    for o, mem in ORBITS.items():
        vals = {T(x) for x in mem}
        assert len(vals) == 1, o
        v = vals.pop()
        img[o] = v
        phi[o] = BY[v] if v else 'SEAM'
    assert T(0) == 33 and BY[33] == 'D7'

    # --- one 6-cycle ---
    seen, cycles = set(), []
    for s in ORBITS:
        if s in seen:
            continue
        path, y = [], s
        while y not in path and y not in seen:
            path.append(y)
            y = phi[y]
        if y in path:
            cycles.append(path[path.index(y):])
        seen |= set(path)
    assert len(cycles) == 1 and len(cycles[0]) == 6
    cyc = cycles[0]
    assert set(cyc) == {'IC', 'D7', 'TESLA', 'NEG_H', 'SEED', 'CAS_EXT'}
    # walk it in order from IC
    w = ['IC']
    while phi[w[-1]] != 'IC':
        w.append(phi[w[-1]])
    assert w == ['IC', 'D7', 'TESLA', 'NEG_H', 'SEED', 'CAS_EXT']

    # --- two transient chains of length 3 ---
    trans = sorted(set(ORBITS) - set(cyc))
    assert trans == ['C3', 'C9', 'DARK_A', 'NQR17', 'SA_ST_A', 'SA_ST_B']
    def chain(o):
        c = [o]
        while c[-1] not in cyc:
            c.append(phi[c[-1]])
        return c
    a, b = chain('C9'), chain('SA_ST_A')
    assert a == ['C9', 'DARK_A', 'C3', 'TESLA']
    assert b == ['SA_ST_A', 'NQR17', 'SA_ST_B', 'D7']
    assert len(a) - 1 == len(b) - 1 == 3
    assert a[-1] != b[-1]                       # enter at different points
    # and no rotation of the 6-cycle exchanges the two entry points
    pos = {o: i for i, o in enumerate(w)}
    assert pos['D7'] == 1 and pos['TESLA'] == 2          # adjacent
    swaps = [k for k in range(6)
             if (pos['TESLA'] + k) % 6 == pos['D7']
             and (pos['D7'] + k) % 6 == pos['TESLA']]
    assert swaps == []                                   # no symmetry
    keeps = [k for k in range(6)
             if {(pos['TESLA'] + k) % 6, (pos['D7'] + k) % 6}
             == {pos['TESLA'], pos['D7']}]
    assert keeps == [0]                                  # identity only
    assert phi['SEAM'] if False else BY[T(0)] == 'D7'

    # --- state levels ---
    onc = {x for o in cyc for x in ORBITS[o] if T(x) in
           {y for oo in cyc for y in ORBITS[oo]} and True}
    # recompute properly: the 6 actual cycle points
    pts = [6]
    while T(pts[-1]) != pts[0]:
        pts.append(T(pts[-1]))
    assert len(pts) == 6 and set(pts) == {6, 27, 32, 19, 10, 34}
    lev = {}
    for x in range(P):
        y, t = x, 0
        while y not in set(pts):
            y = T(y)
            t += 1
        lev[x] = t
    cnt = Counter(lev.values())
    assert dict(cnt) == {0: 6, 1: 12, 2: 7, 3: 6, 4: 6}
    for k, want in ((2, {'C3', 'SA_ST_B'}), (3, {'DARK_A', 'NQR17'}),
                    (4, {'C9', 'SA_ST_A'})):
        got = {BY[x] for x in range(P) if lev[x] == k and x}
        assert got == want, (k, got)
    lo = {BY[x] for x in range(P) if lev[x] in (0, 1)}
    assert lo == set(cyc)                        # levels 0+1 = the cycle orbits

    # --- in-degrees, and the feeders ---
    ind = Counter(T(x) for x in range(P))
    assert dict(Counter(ind.values())) == {3: 12, 1: 1}
    assert len(ind) == 13 == (P - 1) // 3 + 1
    feed = {BY[x] for c in pts for x in range(1, P) if T(x) == c}
    assert feed == set(cyc)                      # feeders ARE the cycle orbits

    # --- indices ---
    assert sorted(IDX[o] for o in cyc) == [0, 3, 5, 6, 8, 11]
    assert sorted(IDX[o] for o in trans) == [1, 2, 4, 7, 9, 10]
    h37 = {'IC', 'DARK_A', 'C3', 'CAS_EXT', 'TESLA', 'SA_ST_A'}
    assert sum(o in h37 for o in cyc) == 3
    assert sum(IDX[o] % 2 == 0 for o in cyc) == 3
    # cubing alone would collapse the index
    assert len({(3 * j) % 12 for j in range(12)}) == 4

    print("All assertions passed.\n")
    print("THEOREM 356.  T's functional graph, complete.\n")
    print("  T IS CONSTANT ON ORBITS, so it descends to phi on the twelve:")
    for o in ORBITS:
        print(f"    {o:9s} -> {img[o]:2d} -> {phi[o]}")
    print(f"    SEAM      -> {T(0)} -> {BY[T(0)]}\n")
    print("  ONE CYCLE, LENGTH 6")
    print(f"    {' -> '.join(w)} -> {w[0]}\n")
    print("  TWO TRANSIENT CHAINS OF LENGTH THREE")
    print(f"    {' -> '.join(a)}")
    print(f"    {' -> '.join(b)}")
    print("    entering at two DISTINCT, ADJACENT cycle points (D7 at")
    print("    position 1, TESLA at 2), plus the seam dropping onto D7.")
    print("    Equal length is NOT a symmetry: no rotation of a 6-cycle")
    print("    transposes two adjacent points, so no automorphism exchanges")
    print("    the chains. Checked for all six rotations.\n")
    print("  STATE LEVELS")
    for k in sorted(cnt):
        os = sorted({('SEAM' if x == 0 else BY[x])
                     for x in range(P) if lev[x] == k})
        print(f"    level {k}: {cnt[k]:2d} states   {os}")
    print("    levels 0 and 1 together are exactly the six cycle orbits:")
    print("    each contributes one cycle point and two level-1 leaves.")
    print(f"    in-degrees {dict(Counter(ind.values()))}, image size {len(ind)},")
    print(f"    {P-len(ind)} states with no preimage.\n")
    print("  INDICES, measured and not claimed")
    print(f"    on-cycle  {sorted(IDX[o] for o in cyc)}")
    print(f"    transient {sorted(IDX[o] for o in trans)}")
    print("    3 of 6 in the 37-half, 3 of 6 even. Both splits even, no")
    print("    finer pattern found.")
    print("    phi is NOT cubing on indices: j -> 3j collapses 12 to 4.")
    print("    The additive 33 is what makes phi worth drawing.")


if __name__ == "__main__":
    run()
