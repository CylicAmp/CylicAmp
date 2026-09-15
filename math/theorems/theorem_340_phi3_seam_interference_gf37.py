# CLASS: THEOREM
"""
Theorem 340: T331's seam is Phi_3, and so is three-path cancellation --
one identity, two settings, graded as an analogy
Author: Michael Warren Song (CyclicAmp)

Prompted by a quantum-interference post (Bhattacharyya, SRM-AP, "Can
Possibilities Interfere With Each Other?", Quantum Age #011).  Two things
came out of checking it: an error in the post, and a correction to T331.

=== THE POST'S ALGEBRA, CHECKED ===

    The graphic states, correctly,

        P = |A1 + A2|^2 = |A1|^2 + |A2|^2 + 2 Re(A1* A2)

    The post's TEXT drops the conjugate and writes 2 Re(A1 A2).  That is
    not a surviving typo -- with A1 = 0.6+0.2i, A2 = 0.3-0.5i the true
    value is 0.900 and the conjugate-free version gives 1.300.

    Second: the graphic labels the two outcomes "higher probability" and
    "lower probability".  For an ideal balanced Mach-Zehnder the outputs at
    relative phase 0 are exactly 1 and 0 -- total, not partial.  The
    interferometer is deterministic at the extremes, which is the striking
    part and is understated by "higher / lower".

    Correct as written, and worth saying so: "a quantum computer does not
    simply try every answer and pick the right one -- it manipulates
    amplitudes".  That is the standard correction to the parallel-universe
    misreading, stated properly.

=== THE CORRECTION TO T331 ===

    T331 said: the rotation seam is "not really about the integer 111",
    that 1 + 10 + 26 = 37 is the coordinate-free fact and 111 = 3 x 37 is
    "the numeral corollary".

    That framing is wrong.  They are the SAME expression:

        1 + 10 + 26  ==  1 + 10 + 10^2  ==  Phi_3(10)  ==  111

    since 26 = 100 mod 37.  One is reduced term by term, the other is not.
    Neither is more fundamental; both evaluate the third cyclotomic
    polynomial at 10.

    The genuinely coordinate-free statement is the one T333 already named:

        Phi_3(x) = x^2 + x + 1,  and Phi_3(w) = 0 for w a primitive cube
        root of unity.

    10 is such a root mod 37 (10^3 = 1000 = 27x37 + 1), so Phi_3(10) == 0,
    so the orbit multipliers sum to zero.  T331's result and T333's
    admissible-base criterion are one fact, not two -- both are Phi_3.

=== THE SHARED IDENTITY, GRADED AS AN ANALOGY ===

    In C, three paths of equal amplitude at relative phases 0, 2pi/3,
    4pi/3 cancel completely:

        1 + w + w^2 = 0,   w = exp(2 pi i / 3)

    In GF(37) the 137-orbit multipliers cancel completely:

        1 + 10 + 26 = 0   (mod 37)

    Same polynomial, same reason.  This is a LEVEL-1 CORRESPONDENCE in the
    T305 sense -- a shared algebraic identity, nothing more.  It does NOT
    say GF(37) models interference, that orbits are physical paths, or that
    the fine-structure constant enters anywhere.  A single photon in a
    Mach-Zehnder does not involve the coupling constant at all, so 1/137
    has no role here beyond the name this project gives the multiplier 26.

    Recorded because the identity is real and the grading keeps it from
    being quoted as more.

=== FALSIFICATION ===
    Phi_3(10) != 0 mod 37; or 1 + 10 + 26 != 111.
"""

P = 37


def run():
    import cmath

    # --- the post's algebra ---
    A1, A2 = complex(0.6, 0.2), complex(0.3, -0.5)
    true = abs(A1 + A2) ** 2
    with_conj = abs(A1) ** 2 + abs(A2) ** 2 + 2 * (A1.conjugate() * A2).real
    no_conj = abs(A1) ** 2 + abs(A2) ** 2 + 2 * (A1 * A2).real
    assert abs(true - with_conj) < 1e-12          # the graphic is right
    assert abs(true - no_conj) > 0.3              # the text is wrong
    assert abs(true - 0.9) < 1e-12 and abs(no_conj - 1.3) < 1e-12

    # ideal balanced MZ: total, not partial
    def ports(phi):
        return (abs((1 + cmath.exp(1j * phi)) / 2) ** 2,
                abs((1 - cmath.exp(1j * phi)) / 2) ** 2)
    a, b = ports(0.0)
    assert abs(a - 1) < 1e-12 and abs(b) < 1e-12
    a, b = ports(cmath.pi)
    assert abs(a) < 1e-12 and abs(b - 1) < 1e-12
    a, b = ports(cmath.pi / 2)
    assert abs(a - 0.5) < 1e-12 and abs(b - 0.5) < 1e-12

    # --- the correction to T331 ---
    assert 100 % P == 26
    assert 1 + 10 + 26 == 37 == P
    assert 1 + 10 + 100 == 111 == 3 * P
    assert (1 + 10 + 26) % P == (1 + 10 + 100) % P == 0
    phi3 = lambda x: x * x + x + 1
    assert phi3(10) == 111                        # they are ONE expression
    assert phi3(10) % P == 0
    assert pow(10, 3, P) == 1 and 1000 == 27 * P + 1
    # T333's admissible bases are exactly the roots of Phi_3 mod 37
    assert [b for b in range(P) if phi3(b) % P == 0] == [10, 26]
    assert phi3(26) % P == 0 and phi3(26) == 703 == 19 * P

    # --- the shared identity ---
    w = cmath.exp(2j * cmath.pi / 3)
    assert abs(1 + w + w * w) < 1e-12             # in C
    assert (1 + 10 + 26) % P == 0                 # in GF(37)
    # both are Phi_3 at a primitive cube root of unity
    assert abs(phi3(w)) < 1e-12
    assert phi3(10) % P == 0

    print("All assertions passed.\n")
    print("THEOREM 340.  The seam is Phi_3.\n")
    print("  THE POST'S ALGEBRA")
    print(f"   |A1+A2|^2                 = {true:.3f}")
    print(f"   ...+ 2Re(A1* A2)          = {with_conj:.3f}   graphic: RIGHT")
    print(f"   ...+ 2Re(A1  A2)          = {no_conj:.3f}   post text: WRONG")
    print( "   the missing conjugate is not a surviving typo.\n")
    print( "   ideal balanced Mach-Zehnder, phase 0:  P = 1 and 0 exactly,")
    print( "   not 'higher' and 'lower'.  Deterministic at the extremes.")
    print( "   Correct in the post, and worth saying: a quantum computer does")
    print( "   NOT try every answer -- it manipulates amplitudes.\n")
    print("  CORRECTION TO T331")
    print( "   T331 called 1+10+26 = 37 coordinate-free and 111 = 3x37 'the")
    print( "   numeral corollary'.  They are the SAME expression:")
    print( "     1 + 10 + 26  ==  1 + 10 + 10^2  ==  Phi_3(10)  ==  111")
    print( "   since 26 = 100 mod 37.  Neither is more fundamental.")
    print( "   The coordinate-free statement is T333's: Phi_3(x) = x^2+x+1,")
    print(f"   whose roots mod 37 are {[b for b in range(P) if phi3(b)%P==0]}.")
    print( "   T331 and T333 are ONE fact.\n")
    print("  THE SHARED IDENTITY")
    print(f"   in C:       1 + w + w^2 = 0,  w = exp(2 pi i/3)   (3-path)")
    print(f"   in GF(37):  1 + 10 + 26 = 0                        (the seam)")
    print( "   same polynomial, same reason.\n")
    print( "   GRADE: level-1 correspondence -- a shared algebraic identity.")
    print( "   It does NOT say GF(37) models interference, that orbits are")
    print( "   physical paths, or that 1/137 enters.  A single photon in a")
    print( "   Mach-Zehnder never involves the coupling constant.")


if __name__ == "__main__":
    run()
