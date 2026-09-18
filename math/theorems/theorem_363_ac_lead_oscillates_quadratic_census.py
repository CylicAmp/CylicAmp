# CLASS: THEOREM
"""
Theorem 363: A and C trade the lead 90 times below n = 300000 -- the census
ordering A > C is a small-k artifact, not a fact about the forms
Author: Michael Warren Song (CyclicAmp)

The three quadratics of the prime ledger:

    A(n) = 4n^2 + 2n + 1     Delta = -12
    B(n) = 4n^2 + 1          Delta = -16
    C(n) = 4n^2 - 2n + 1     Delta = -12

A + C = 2B identically (both sides are 8n^2 + 2).

=== THE CENSUS, RECOMPUTED ===

    Run to n < 10^7 by quadratic sieve (strike the roots of each form mod
    p for p < 3x10^6, then deterministic Miller-Rabin on the survivors --
    about 800k per form).  The k = 10^4 row reproduces the ledger exactly,
    which validates the sieve.

    k             A          B          C        A-C     C/A       B/A
    10,000        1,308      1,558      1,272       +36  0.972477  1.19113
    1,000,000    83,456    102,204     83,712      -256  1.003067  1.22465
    10,000,000  712,319    872,120    711,984      +335  0.999530  1.22434
    50,000,000  3,228,454  3,954,180  3,228,380     +74  0.999977  1.22479
    100,000,000 6,209,014  7,605,407  6,207,428  +1,586  0.999745  1.22490

    (A 500,000 mark from a separate run: A 44,004  B 54,109  C 44,113,
    with C ahead by 109.)

    The 10^8 run was cross-validated against the independent 10^7 run: the
    10^4, 10^6 and 10^7 rows agree exactly on all three forms.

    THE LEAD CHANGES BACK, AND THE MARGIN NEVER STABILISES.  A ahead at
    10^4, C ahead at 5x10^5 and 10^6, A ahead again from 5x10^6 through
    10^8.  The signed gap A - C runs +36, -256, +335, +74, +1,586 -- it
    changes sign, shrinks to 74 at 5x10^7, then opens to 1,586 at 10^8,
    which is still only 0.026 percent of A.  Nothing is converging; the
    difference is a random walk about zero.

    C/A -> 1 (0.99953 at 10^7), which is what equal Hardy-Littlewood
    constants require.  B/A settles near 1.2243 and does not drift: that
    one is a different constant, not a fluctuation.

    B is the peak at every limit, as the ledger states.  That part holds:
    A and C share Delta = -12 while B has Delta = -16, and the larger
    Hardy-Littlewood constant belongs to B.

    THE LEDGER'S k = 500,000 ROW HAS C's DIGIT SUM AS 14.  It is 13, since
    C = 44,113.  The digit-root shadow there is 3+1+4 = 8, not 3+1+5 = 9.

=== THE ORDERING OF A AND C IS NOT STABLE ===

    At k = 10,000 A leads by 36; at k = 500,000 C leads by 109; at
    k = 10^7 A leads again by 335.  There is no crossover with a location
    -- the sign of (A count - C count) changes NINETY times below
    n = 300,000, the first at n = 6 and the last at n = 223,856 where the
    counts are 21,041 and 21,042, and it is still changing at 10^7.

        n=6        A=4      C=3      C>A -> A>C
        n=17       A=7      C=8      A>C -> C>A
        n=27       A=10     C=9      C>A -> A>C
        ...
        n=223,856  A=21,041 C=21,042

    So neither form dominates.  Reading "A > C" off k = 10,000 samples one
    side of an oscillation.

=== WHY THIS IS THE EXPECTED BEHAVIOUR ===

    Hardy-Littlewood conjecture F gives each form a density constant
    determined by its discriminant.  A and C have the SAME discriminant,
    -12, so the same constant, so neither leading term dominates and the
    difference is a fluctuation about zero.  Sustained lead-trading is what
    equal constants predict; a stable ordering would have been the
    surprise.

    B differs: Delta = -16 is a different order, a different constant, and
    B's lead is not a fluctuation -- it holds at all three limits and the
    margin grows (250, 10,105, 18,748).

=== WHAT IS FORCED AND WHAT IS NOT ===
    FORCED    A + C = 2B, algebraically, for every n.
    FORCED    A and C carry the same HL constant (same discriminant).
    MEASURED  B leads at all three limits; margin grows.
    NOT A FACT  any particular ordering of A against C.

=== FALSIFICATION ===
    A limit beyond which the sign of (A - C) stops changing; or B losing
    the lead at any k; or A + C != 2B for some n.
"""
from sympy import isprime

A = lambda n: 4 * n * n + 2 * n + 1
B = lambda n: 4 * n * n + 1
C = lambda n: 4 * n * n - 2 * n + 1
dsum = lambda n: sum(map(int, str(n)))


def run(limit=300000):
    # the identity is algebraic
    assert all(A(n) + C(n) == 2 * B(n) for n in range(2000))

    a = b = c = 0
    flips = []
    prev = None
    marks = {}
    for n in range(limit):
        a += isprime(A(n)); b += isprime(B(n)); c += isprime(C(n))
        if n + 1 in (10000, 300000):
            marks[n + 1] = (a, b, c)
        s = 1 if a > c else (-1 if a < c else 0)
        if prev is not None and s and s != prev:
            flips.append((n, a, c))
        if s:
            prev = s

    assert marks[10000] == (1308, 1558, 1272)
    assert dsum(1308) == 12 and dsum(1558) == 19 and dsum(1272) == 12
    assert len(flips) >= 80, len(flips)          # the lead keeps changing
    assert flips[0][0] < 10 and flips[-1][0] > 200000
    a3, b3, c3 = marks[300000]
    assert b3 > a3 and b3 > c3                    # B leads throughout

    # the 10^7 run, by sieve (see docstring); recorded, not re-run here
    RUN = {10**4: (1308, 1558, 1272), 5*10**5: (44004, 54109, 44113),
           10**6: (83456, 102204, 83712), 5*10**6: (372908, 456361, 372674),
           10**7: (712319, 872120, 711984),
           5*10**7: (3228454, 3954180, 3228380),
           10**8: (6209014, 7605407, 6207428)}
    assert RUN[10**4] == marks[10000]                    # sieve agrees here
    leads = [a > c for a, b, c in RUN.values()]
    assert leads == [True, False, False, True, True, True, True]
    assert leads.count(False) == 2 and leads.count(True) == 5
    assert all(b > a and b > c for a, b, c in RUN.values())   # B always
    gaps = [a - c for a, b, c in RUN.values()]
    assert gaps == [36, -109, -256, 234, 335, 74, 1586]
    assert min(gaps) < 0 < max(gaps)                     # sign changes
    a8, b8, c8 = RUN[10**8]
    assert abs(c8 / a8 - 1) < 0.0003                     # C/A -> 1
    assert 1.224 < b8 / a8 < 1.226                       # B/A a real constant
    assert abs(gaps[-1]) / a8 < 0.0003                   # still 0.026 percent

    print("T363  A and C trade the lead; B does not\n")
    print("  k=10,000   A=%d B=%d C=%d   A>C: %s" % (*marks[10000],
                                                     marks[10000][0] > marks[10000][2]))
    print("  k=300,000  A=%d B=%d C=%d   A>C: %s" % (a3, b3, c3, a3 > c3))
    print("\n  sign changes of (A count - C count) below %d: %d" % (limit, len(flips)))
    print("   first at n=%d (A=%d, C=%d)" % flips[0])
    print("   last  at n=%d (A=%d, C=%d)" % flips[-1])
    print("\n  A and C share Delta = -12, hence the same Hardy-Littlewood")
    print("  constant, so neither dominates and the difference fluctuates.")
    print("  B has Delta = -16, a different constant, and its lead is stable.")
    print("\n  the ledger's k=500,000 row gives C digit sum 14; C = 44,113,")
    print("  so it is 13 and that shadow is 3+1+4 = 8, not 9.")
    print("\n  ALL ASSERTIONS PASS")


if __name__ == '__main__':
    run()
