# CLASS: THEOREM
"""
Theorem 364: the 9s-complement on Z_3663 is x -> 2673 - x, and its CRT form
(0,0,9) - (a,b,c) is GLOBAL, not restricted to {3663, 6336}
Author: Michael Warren Song (CyclicAmp)

Supplied as a restricted-domain invariance theorem.  Every step verifies.
The scope caveat attached to it is correct to be cautious but guards the
wrong statement: the formula generalises, and what does not is the fixing
of the 9- and 11-coordinates.

=== WHAT WAS SUPPLIED, AND CHECKS ===

    N = 3663 = 9 x 11 x 37,  C(X) = 9999 - X,  D = {3663, 6336}.

    C(3663) = 6336 and C(6336) = 3663, so C restricted to D is an
    involution and D is a closed 2-orbit.

    Mod 3663: 3663 == 0 and 6336 == 2673.  CRT coordinates (mod 9, 11, 37):

        3663 -> (0, 0, 0)
        6336 -> (0, 0, 9)          2673 = 72 x 37 + 9

    so the orbit is (0,0,0) <-> (0,0,9), with the 9- and 11-coordinates
    zero throughout and all motion in the 37-coordinate.  All verified.

=== THE SHARPENING: THE CRT FORMULA IS GLOBAL ===

    9999 mod 3663 = 2673, so for EVERY X,

        C(X) = 9999 - X == 2673 - X    (mod 3663),

    and since 2673 -> (0,0,9),

        C_CRT(a, b, c) = (0, 0, 9) - (a, b, c)

    holds on all 3663 residues, not only on D.  Verified exhaustively.

    So the supplied identity is not a property of the restricted domain.
    It is the whole map, written in coordinates.

=== WHAT IS ACTUALLY RESTRICTED ===

    The 9- and 11-coordinates are NOT invariant in general.  The formula
    sends a -> -a and b -> -b.  On D they look fixed only because D's
    points have a = b = 0, and 0 is the unique fixed point of negation in
    Z_9 and in Z_11.  Checked: no residue with a nonzero 9-coordinate is
    fixed by C.

    That is the real content -- D sits on the (0,0) fibre, where two of the
    three coordinates are already at their negation fixed point, so the map
    can only move the third.  Confinement to the 37-axis is a property of
    the fibre, not of the map.

    The 37-coordinate is not free either: c -> 9 - c has the fixed point
    2c == 9, i.e. c == 23.  So on the (0,0) fibre C has exactly one fixed
    point and 18 two-cycles, of which D's is one.

=== SCOPE, RESTATED ===
    C|_D : (0,0,0) <-> (0,0,9) is correct.
    C_CRT(a,b,c) = (0,0,9) - (a,b,c) is correct and GLOBAL.
    "the 9- and 11-coordinates remain invariant" is true only on a = b = 0.

=== FALSIFICATION ===
    An X in Z_3663 with C_CRT(X) != (0,0,9) - CRT(X); or a residue with
    nonzero 9- or 11-coordinate fixed by C; or a second fixed point on the
    (0,0) fibre.
"""
N = 3663
crt = lambda x: (x % 9, x % 11, x % 37)
C = lambda X: 9999 - X


def run():
    assert N == 9 * 11 * 37
    D = [3663, 6336]

    # the supplied claims
    assert C(3663) == 6336 and C(6336) == 3663
    assert [C(C(x)) for x in D] == D                    # involution on D
    assert 3663 % N == 0 and 6336 % N == 2673
    assert crt(0) == (0, 0, 0) and crt(2673) == (0, 0, 9)

    # the sharpening: the formula is global
    assert 9999 % N == 2673
    for x in range(N):
        lhs = crt((2673 - x) % N)
        rhs = tuple((u - v) % m for u, v, m in zip(crt(2673), crt(x), (9, 11, 37)))
        assert lhs == rhs, x

    # the 9- and 11-coordinates are not invariant off the (0,0) fibre
    fixed9 = [x for x in range(N) if x % 9 and crt((2673 - x) % N)[0] == x % 9]
    fixed11 = [x for x in range(N) if x % 11 and crt((2673 - x) % N)[1] == x % 11]
    assert fixed9 == [] and fixed11 == []

    # on the (0,0) fibre: one fixed point, 18 two-cycles
    fibre = [x for x in range(N) if x % 9 == 0 and x % 11 == 0]
    assert len(fibre) == 37
    fp = [x for x in fibre if (2673 - x) % N == x]
    assert len(fp) == 1 and fp[0] % 37 == 23
    assert (2 * 23) % 37 == 9
    assert (len(fibre) - 1) // 2 == 18

    print("T364  the 9s-complement on Z_3663\n")
    print("  3663 = 9 x 11 x 37;  C(X) = 9999 - X")
    print("  C(3663) = 6336, C(6336) = 3663 -- involution on D, verified")
    print("  CRT:  3663 -> (0,0,0)    6336 = 2673 -> (0,0,9)\n")
    print("  SHARPENING: 9999 mod 3663 = 2673, so C(X) = 2673 - X for EVERY X,")
    print("  hence C_CRT(a,b,c) = (0,0,9) - (a,b,c) on all %d residues," % N)
    print("  not only on D. Checked exhaustively.\n")
    print("  so the 9- and 11-coordinates are NOT invariant: a -> -a, b -> -b.")
    print("  no residue with a nonzero 9- or 11-coordinate is fixed.")
    print("  they appear fixed on D only because D lies on the (0,0) fibre,")
    print("  where 0 is already the unique fixed point of negation.\n")
    print("  on that fibre (37 points) C has exactly 1 fixed point, c = 23")
    print("  (since 2c = 9 mod 37), and 18 two-cycles. D's orbit is one of them.")
    print("\n  ALL ASSERTIONS PASS")


if __name__ == '__main__':
    run()
