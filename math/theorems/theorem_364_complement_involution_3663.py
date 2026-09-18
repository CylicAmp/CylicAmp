# CLASS: THEOREM
"""
Theorem 364: the 9s-complement on Z_3663 is a GLOBAL affine involution;
F_37 is its invariant fibre; {3663, 6336} is one of eighteen two-cycles
Author: Michael Warren Song (CyclicAmp)

=== STATEMENT ===

    R = Z_3663 = Z_9 x Z_11 x Z_37, CRT coordinates (a, b, c).
    C(X) = 9999 - X, the four-digit 9s-complement.

    (1) GLOBAL FORM.  9999 = 2(3663) + 2673, so on R

            C(x) = 2673 - x   (mod 3663),

        and 2673 -> (0,0,9), giving for EVERY (a,b,c)

            C(a, b, c) = (-a, -b, 9 - c),        C^2 = id_R.

    (2) INVARIANT FIBRE.  F_37 = {(0,0,c) : c in Z_37} satisfies
        C(F_37) = F_37, since C(0,0,c) = (0,0,9-c).
        Off the fibre a -> -a and b -> -b, so nonzero 9- and 11-
        coordinates are INVERTED, not preserved.

    (3) ORBIT DECOMPOSITION ON THE FIBRE.  The induced map is the
        one-dimensional affine involution c -> 9 - c (mod 37).  Its fixed
        points solve 2c = 9; with 2^-1 = 19 (mod 37) the unique one is
        c = 23.  An involution on 37 points with one fixed point splits the
        other 36 into 18 disjoint two-cycles:

            F_37 = {(0,0,23)} u O_1 u ... u O_18,   |O_k| = 2.

    (4) THE SUPPLIED PAIR.  3663 <-> 6336 is the orbit (0,0,0) <-> (0,0,9),
        since 6336 = 2673 (mod 3663) and 2673 -> (0,0,9).  It is ONE of the
        eighteen two-cycles, not the mechanism that creates the fibre.

=== WHAT THIS CORRECTS IN THE FIRST VERSION SUPPLIED ===

    That version stated the CRT identity as a property of the restricted
    domain D = {3663, 6336}, with a scope caveat against generalising it.
    The caveat guards the wrong statement.  The identity generalises -- it
    is the whole map in coordinates, verified on all 3663 residues.  What
    does NOT generalise is the fixing of the 9- and 11-coordinates, which
    holds on D only because D lies on the (0,0) fibre where 0 is already
    the unique fixed point of negation.

    Confinement to the 37-axis is a property of the fibre, not of the map.

Supplied as a restricted-domain invariance theorem.  Every step verifies.
The scope caveat attached to it is correct to be cautious but guards the
wrong statement: the formula generalises, and what does not is the fixing
of the 9- and 11-coordinates.

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
