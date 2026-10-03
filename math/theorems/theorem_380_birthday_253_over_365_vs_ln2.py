# CLASS: THEOREM
"""
Theorem 380: 253/365 agrees with ln 2 to 3.5e-6, so the Poisson estimate
lands on 1/2 -- but that is the ESTIMATE, not the answer
Author: Michael Warren Song (CyclicAmp)

PRIOR ART: the collision problem is absent.  The files matching "birthday"
are T176 and T270, both about March 3 as a calendar date, a different
subject.  Nothing in the corpus computes a collision probability.

=== THE SUPPLIED DERIVATION, VERIFIED EXACTLY ===

    K_23 on 365 slots has C(23,2) = 253 chords.  With d = 365 equiprobable
    outcomes,

        P(no collision) = prod_{k=0}^{22} (365-k)/365 = 0.4927027657
        P(collision)    = 0.5072972343   >  1/2

    computed in exact rationals, not floating point.  And 23 is the
    smallest n that clears 1/2, checked exactly over every n.  The
    threshold formula agrees:

        n ~ sqrt(2 d ln 2) = 1.177410 sqrt(365) = 22.4944  ->  23

=== THE NEAR-COINCIDENCE, AND WHAT IT DOES NOT BUY ===

        253/365 = 0.693150685
        ln 2    = 0.693147181
        differ by 3.50e-06 -- five decimal places

    So exp(-253/365) = 0.499998248, and the Poisson estimate for the
    collision probability comes out at 0.500002: essentially exactly 1/2.
    That is a real and pretty fact, and it is a fact about d = 365 alone.

    IT IS THE ESTIMATE LANDING ON 1/2, NOT THE TRUTH.

        Poisson  1 - exp(-C(23,2)/365) = 0.500002
        exact                            0.507297
        error                            0.007295

    The approximation is low by 0.73 percent.  It uses 1 - x ~ e^-x on each
    factor and so drops the higher terms of the product; that error is
    present whatever 253/365 happens to equal.  Two unrelated things meet
    here: the shortcut is off by 0.0073, and 253/365 sits 3.5e-6 from ln 2.
    Neither causes the other, and the second does not repair the first.

    Both still exceed 1/2, so the conclusion "23 suffices" is right by
    either route -- but only the exact product establishes it.

=== THE CRYPTOGRAPHIC BRIDGE IS THE SAME COUNT ===

    C(n,2) ~ n^2/2 is why collision search costs O(sqrt(N)): n draws give
    ~n^2/2 pairs, so n ~ sqrt(N) pairs suffice to expect a repeat.  That is
    the same 253-chords-on-365-slots count, and it sets generic discrete-log
    resistance for a group of order r at O(sqrt(r)).  For r ~ 2^255,
    sqrt(r) = 2^127.5 ~ 2^128.  Pollard rho and baby-step giant-step both
    realise it.

=== GF(37): NOTHING ===

    23 in TESLA, 253 in C9, 365 in SEED, 128 in NQR17, 255 in D7 -- five
    values, five different orbits, which is what unrelated numbers do.
    253 = 11 x 23 and 365 = 5 x 73.  The 73 is in the Tier B set
    {7, 37, 73}, but that set comes from ord_p(137) = 3 and has nothing to
    do with a calendar length; 73 | 365 is arithmetic.  Recorded and graded
    down rather than left for someone to pick up.

=== FALSIFICATION ===
    An n < 23 with exact P(collision) > 1/2; 253/365 differing from ln 2 by
    more than 1e-5; or the Poisson estimate agreeing with the exact value
    to better than 1e-3.
"""
from math import comb, log, exp, sqrt
from fractions import Fraction as F

D = 365


def p_no_collision(n, d=D):
    p = F(1)
    for k in range(n):
        p *= F(d - k, d)
    return p


def run():
    assert comb(23, 2) == 253

    exact_no = p_no_collision(23)
    exact_yes = 1 - float(exact_no)
    assert abs(float(exact_no) - 0.4927027657) < 1e-10
    assert exact_yes > 0.5

    # 23 is the smallest n clearing 1/2, checked exactly
    first = next(n for n in range(1, D) if 1 - float(p_no_collision(n)) > 0.5)
    assert first == 23
    assert 1 - float(p_no_collision(22)) < 0.5

    # the threshold formula
    thr = sqrt(2 * D * log(2))
    assert abs(thr - 22.4944) < 1e-4 and -(-thr // 1) == 23

    # the near-coincidence
    gap = abs(253 / D - log(2))
    assert gap < 4e-6, gap
    poisson = 1 - exp(-253 / D)
    assert abs(poisson - 0.5) < 1e-5                    # estimate lands on 1/2

    # ... but the estimate is NOT the answer
    err = exact_yes - poisson
    assert 0.007 < err < 0.008                          # low by 0.73 percent
    assert poisson > 0.5 and exact_yes > 0.5            # same verdict, different margin

    # the crypto bound
    assert abs(sqrt(2.0 ** 255) - 2.0 ** 127.5) < 1e-30 * 2 ** 127
    assert round(255 / 2) == 128

    # GF(37): five values, five orbits
    ORB = {'IC': (1, 10, 26), 'DARK_A': (2, 15, 20), 'C3': (3, 4, 30),
           'CAS_EXT': (5, 13, 19), 'TESLA': (6, 8, 23), 'D7': (7, 33, 34),
           'SA_ST_A': (9, 12, 16), 'NEG_H': (11, 27, 36), 'C9': (14, 29, 31),
           'NQR17': (17, 22, 35), 'SEED': (18, 24, 32), 'SA_ST_B': (21, 25, 28)}
    orb = lambda v: next(k for k, s in ORB.items() if v % 37 in s)
    hits = [orb(v) for v in (23, 253, 365, 128, 255)]
    assert len(set(hits)) == 5                          # scattered, no signal
    assert 253 == 11 * 23 and 365 == 5 * 73

    print("T380  the birthday collision at n = 23\n")
    print("  C(23,2) = 253 chords on 365 slots")
    print("  P(no collision) = %.10f   (exact rationals)" % float(exact_no))
    print("  P(collision)    = %.10f   > 1/2" % exact_yes)
    print("  smallest n clearing 1/2, computed exactly: %d" % first)
    print("  threshold sqrt(2 d ln 2) = %.4f -> 23\n" % thr)
    print("  NEAR-COINCIDENCE: 253/365 = %.9f" % (253 / D))
    print("                    ln 2    = %.9f   differ by %.2e" % (log(2), gap))
    print("  so exp(-253/365) = %.9f and the Poisson estimate is %.6f"
          % (exp(-253 / D), poisson))
    print("\n  BUT THAT IS THE ESTIMATE, NOT THE ANSWER:")
    print("   Poisson %.6f   exact %.6f   low by %.6f" % (poisson, exact_yes, err))
    print("   the shortcut drops the higher terms of the product; that error")
    print("   is there whatever 253/365 equals. Neither fact causes the other.")
    print("\n  same count gives the crypto bound: C(n,2) ~ n^2/2, so collision")
    print("  search is O(sqrt(N)); r ~ 2^255 -> 2^127.5 ~ 2^128.")
    print("\n  GF(37): %s -- five values, five orbits. Nothing." % hits)
    print("\n  ALL ASSERTIONS PASS")


if __name__ == '__main__':
    run()
