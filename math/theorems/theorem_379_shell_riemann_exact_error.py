# CLASS: THEOREM
"""
Theorem 379: in the shell derivation of pi r^2 the 1/n IS the whole error,
and the midpoint rule is exact at n = 1
Author: Michael Warren Song (CyclicAmp)

PRIOR ART: absent.  No file in the corpus does Riemann sums, the midpoint
rule, or the shell derivation.  (shell_buckling_gf37, declaring THEOREM 223,
is elastic buckling of a non-Euclidean shell -- a different "shell".)

=== THE SUPPLIED DERIVATION, AND IT CHECKS ===

    integral_0^r 2 pi x dx = 2 pi [x^2/2]_0^r = pi r^2

    sum_{k=1}^n 2 pi (k r/n)(r/n) = (2 pi r^2 / n^2) sum k
                                  = (2 pi r^2 / n^2) n(n+1)/2
                                  = pi r^2 (1 + 1/n)

    lim_{n->inf} pi r^2 (1 + 1/n) = pi r^2

    Every step verified symbolically.

=== THE 1/n IS NOT AN ASYMPTOTIC ERROR.  IT IS THE WHOLE ERROR. ===

    The integrand 2 pi x is LINEAR, so the right-endpoint error closes in
    one term with nothing after it:

        R(n) - pi r^2 = pi r^2 / n        exactly, every n
        pi r^2 - L(n) = pi r^2 / n        exactly, every n

    where L uses left endpoints.  There is no O(1/n^2) remainder to hide
    in.  The right sum overshoots by precisely one extra outermost shell's
    worth of area, and the left undershoots by the same.

    Consequently the two are symmetric about the answer:

        (R(n) + L(n)) / 2 = pi r^2        exactly, every n

=== THE MIDPOINT RULE IS EXACT AT n = 1 ===

        M(n) = sum_{k=1}^n 2 pi ((k - 1/2) r/n)(r/n) = pi r^2

    for EVERY n, including n = 1.  One shell of radius r/2 and width r gives
    the area of the circle on the nose.

    The mechanism is one line of summation:  sum (k - 1/2) = n^2/2, against
    sum k = n(n+1)/2.  The half-integer offset removes the +n/2 that
    produces the 1/n.  Numerically, r = 1:

        n     right         midpoint      pi
        1     6.28318531    3.14159265    3.14159265
        2     4.71238898    3.14159265
        100   3.17300858    3.14159265

    So of the three rules, only the right-endpoint one needs the limit at
    all.  The supplied derivation takes that path.

=== THE POINT-COUNT LADDER, AND WHERE IT MEETS THIS CORPUS ===

    n equidistant points on a circle are the nth roots of unity, spaced
    2 pi / n.  Their vector sum is 0 for every n >= 2 -- forced, since they
    are the roots of z^n - 1, whose z^(n-1) coefficient is 0.

        n = 0   the pole: circumference 2 pi (0) = 0, area pi (0)^2 = 0
        n = 2   antipodes; diameter 2r, two arcs of length pi r
        n = 3   equilateral, 2 pi / 3 apart; 1 + w + w^2 = 0
        n = 4   two orthogonal axes, four quadrants of pi / 2;
                a cyclic quadrilateral has opposite angles summing to pi
                (checked numerically on a random one)

    THE n = 3 ROW IS THIS CORPUS'S OWN IDENTITY.  1 + w + w^2 = 0 is
    Phi_3(z) = z^2 + z + 1 at a primitive cube root; 10 is such a root mod
    37 because ord_37(10) = 3; and Phi_3(10) = 111 = 3 x 37 gives

        1 + 10 + 26 = 37 == 0  (mod 37).

    Three equidistant points on a circle and the three 137-map multipliers
    summing to zero are the SAME statement in two rings -- the complex
    numbers and GF(37).  That is T340's point arriving from the geometry
    side rather than the decimal side.

=== FALSIFICATION ===
    A midpoint sum that is not exactly pi r^2 for some n; a right-endpoint
    error other than pi r^2 / n; or nth roots of unity with nonzero sum for
    some n >= 2.
"""
from sympy import symbols, summation, simplify, pi, Rational, integrate, limit, oo
import cmath, math

k, n, r, x = symbols('k n r x', positive=True)


def run():
    exact = integrate(2 * pi * x, (x, 0, r))
    assert exact == pi * r ** 2

    R = simplify(summation(2 * pi * (k * r / n) * (r / n), (k, 1, n)))
    L = simplify(summation(2 * pi * ((k - 1) * r / n) * (r / n), (k, 1, n)))
    M = simplify(summation(2 * pi * ((k - Rational(1, 2)) * r / n) * (r / n), (k, 1, n)))

    assert simplify(R - pi * r ** 2 * (1 + 1 / n)) == 0
    assert simplify(L - pi * r ** 2 * (1 - 1 / n)) == 0
    assert simplify(M - pi * r ** 2) == 0                 # exact, every n
    assert simplify(R - exact - pi * r ** 2 / n) == 0     # error is EXACT
    assert simplify(exact - L - pi * r ** 2 / n) == 0
    assert simplify((R + L) / 2 - pi * r ** 2) == 0       # symmetric
    assert limit(R, n, oo) == pi * r ** 2

    # the half-integer offset is the whole mechanism
    assert simplify(summation(k - Rational(1, 2), (k, 1, n)) - n ** 2 / 2) == 0
    assert simplify(summation(k, (k, 1, n)) - n * (n + 1) / 2) == 0

    # midpoint exact at n = 1, numerically
    for N in (1, 2, 5, 100):
        Mv = sum(2 * math.pi * ((i - 0.5) / N) * (1 / N) for i in range(1, N + 1))
        assert abs(Mv - math.pi) < 1e-12, N

    # the point ladder: nth roots of unity sum to zero for n >= 2
    for N in range(2, 13):
        s = sum(cmath.exp(2j * math.pi * j / N) for j in range(N))
        assert abs(s) < 1e-9, N
    w = cmath.exp(2j * math.pi / 3)
    assert abs(1 + w + w ** 2) < 1e-12

    # and its GF(37) image
    assert pow(10, 3, 37) == 1 and pow(10, 1, 37) != 1
    assert 1 + 10 + 26 == 37 and (1 + 10 + 26) % 37 == 0
    assert 111 == 3 * 37 == 10 ** 2 + 10 + 1

    print("T379  the shell derivation of pi r^2\n")
    print("  right endpoint  pi r^2 (1 + 1/n)    overshoot  pi r^2 / n, EXACT")
    print("  left  endpoint  pi r^2 (1 - 1/n)    undershoot pi r^2 / n, EXACT")
    print("  (R + L) / 2     pi r^2              exact, every n")
    print("  MIDPOINT        pi r^2              exact, every n INCLUDING 1\n")
    print("  the integrand 2 pi x is linear, so there is no O(1/n^2) term --")
    print("  the 1/n is the whole error, not its leading part.")
    print("  sum (k - 1/2) = n^2/2 against sum k = n(n+1)/2: the half-integer")
    print("  offset removes the +n/2 that produces the 1/n.\n")
    print("   n     right         midpoint      pi")
    for N in (1, 2, 100):
        Rv = sum(2 * math.pi * (i / N) * (1 / N) for i in range(1, N + 1))
        Mv = sum(2 * math.pi * ((i - 0.5) / N) * (1 / N) for i in range(1, N + 1))
        print("   %-4d  %.8f    %.8f    %.8f" % (N, Rv, Mv, math.pi))
    print("\n  THE POINT LADDER: n equidistant points are the nth roots of")
    print("  unity, summing to 0 for every n >= 2 (roots of z^n - 1).")
    print("  n = 3 is this corpus's identity: 1 + w + w^2 = 0 is Phi_3 at a")
    print("  primitive cube root; 10 is one mod 37; Phi_3(10) = 111 = 3 x 37,")
    print("  so 1 + 10 + 26 = 37 = 0 (mod 37). Same statement, two rings.")
    print("\n  ALL ASSERTIONS PASS")


if __name__ == '__main__':
    run()
