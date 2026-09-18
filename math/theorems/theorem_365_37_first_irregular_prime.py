# CLASS: THEOREM
"""
Theorem 365: 37 is the FIRST IRREGULAR PRIME, and this is a second reason
37 is distinguished -- independent of ord_37(10) = 3
Author: Michael Warren Song (CyclicAmp)

=== THE FACT ===

    A prime p is IRREGULAR (Kummer, 1850) if it divides the numerator of
    the Bernoulli number B_k for some even k with 2 <= k <= p - 3.
    Equivalently, p divides the class number h of the cyclotomic field
    Q(zeta_p).

    37 IS THE FIRST SUCH PRIME.  No p < 37 is irregular -- verified here
    for every prime from 3 to 31 over every admissible k.  The irregular
    pair is (37, 32):

        B_32 = -7709321041217 / 510,     7709321041217 = 0 (mod 37)

    The next two are 59 with k = 44, and 67 with k = 58.

=== WHY IT MATTERS ===

    Kummer proved Fermat's Last Theorem for all REGULAR prime exponents.
    37 is therefore the first exponent his method does not reach -- the
    smallest p for which that entire 19th-century programme fails.  The
    irregularity is exactly the obstruction: p | h(Q(zeta_p)) breaks the
    unique-factorisation argument.

    Via zeta(1 - k) = -B_k / k, the statement is also
    37 | numerator(zeta(-31)), which is the p-adic zeta / Kubota-Leopoldt
    reading of the same congruence.

=== THE POINT FOR THIS CORPUS: TWO INDEPENDENT DISTINCTIONS ===

    This repository's one Tier C fact is

        ord_37(10) = 3,  because 10^3 - 1 = 999 = 3^3 x 37,

    which is a statement about 37 in BASE 10.  Irregularity is a statement
    about Bernoulli numerators and cyclotomic class numbers.  Nothing
    connects them: one is about the multiplicative order of a particular
    base, the other about the arithmetic of Q(zeta_37).

    So 37 carries (at least) two unrelated reasons to be singled out, and
    they must not be cited as though they were one.  Neither implies the
    other, and neither strengthens the other.  Recorded here precisely so
    the corpus does not fuse them later.

=== THE ONE GF(37) OBSERVATION, AND IT IS NOISE ===

    The irregular index k = 32 lands in SEED = {18, 24, 32}, the orbit of
    the reference seed 246.  That is 1 orbit of 12, post hoc, n = 1.

    Tier-tested rather than reported: the irregular indices of the first
    eight irregular primes, read mod 37, are

        p=37  k=32  -> SEED        p=103 k=24   -> SEED
        p=59  k=44  -> D7          p=131 k=22   -> NQR17
        p=67  k=58  -> SA_ST_B     p=149 k=130  -> CAS_EXT
        p=101 k=68  -> C9          p=157 k=62,110 -> SA_ST_B, NEG_H

    Scattered across seven different orbits.  SEED occurs twice in nine
    indices, which is what 1/12 looks like at this sample size.  No signal.

=== FALSIFICATION ===
    An irregular prime below 37; or 37 not dividing the numerator of B_32;
    or an even k other than 32 in [2, 34] with 37 | numerator(B_k).
"""
from sympy import bernoulli, primerange

ORBITS = {
    'IC': (1, 10, 26), 'DARK_A': (2, 15, 20), 'C3': (3, 4, 30),
    'CAS_EXT': (5, 13, 19), 'TESLA': (6, 8, 23), 'D7': (7, 33, 34),
    'SA_ST_A': (9, 12, 16), 'NEG_H': (11, 27, 36), 'C9': (14, 29, 31),
    'NQR17': (17, 22, 35), 'SEED': (18, 24, 32), 'SA_ST_B': (21, 25, 28),
}


def orbit_of(n):
    r = n % 37
    return 'SEAM' if r == 0 else next(k for k, v in ORBITS.items() if r in v)


def irregular_indices(p):
    """even k in [2, p-3] with p dividing the numerator of B_k"""
    return [k for k in range(2, p - 1, 2) if bernoulli(k).p % p == 0]


def run():
    # no prime below 37 is irregular
    for p in primerange(3, 37):
        assert irregular_indices(p) == [], (p, irregular_indices(p))

    # 37 is, with the single index 32
    assert irregular_indices(37) == [32]
    b32 = bernoulli(32)
    assert b32.p == -7709321041217 and b32.q == 510
    assert b32.p % 37 == 0
    assert 32 % 2 == 0 and 2 <= 32 <= 37 - 3

    # the next two
    assert irregular_indices(59) == [44]
    assert irregular_indices(67) == [58]

    # the GF(37) reading, graded down
    pairs = [(37, [32]), (59, [44]), (67, [58]), (101, [68]),
             (103, [24]), (131, [22]), (149, [130]), (157, [62, 110])]
    orbs = [orbit_of(k) for _, ks in pairs for k in ks]
    assert orbit_of(32) == 'SEED'
    assert orbs.count('SEED') == 2 and len(orbs) == 9      # 2 of 9, vs 1/12
    assert len(set(orbs)) == 7                              # seven orbits hit

    # the corpus's own Tier C fact, and its independence from this one
    assert pow(10, 3, 37) == 1 and pow(10, 1, 37) != 1
    assert 10 ** 3 - 1 == 999 == 27 * 37

    print("T365  37 is the first irregular prime\n")
    print("  no prime below 37 is irregular (checked 3..31, all admissible k)")
    print("  37 is, with the single index k = 32:")
    print("   B_32 = %d / %d,  numerator mod 37 = %d" % (b32.p, b32.q, b32.p % 37))
    print("  next: 59 (k=44), 67 (k=58)\n")
    print("  Kummer proved FLT for regular exponents, so 37 is the first")
    print("  exponent that programme does not reach. Equivalently 37 divides")
    print("  the class number of Q(zeta_37).\n")
    print("  TWO INDEPENDENT DISTINCTIONS, not to be fused:")
    print("   ord_37(10) = 3   -- about base 10, gives 999 = 27 x 37")
    print("   irregularity     -- about Bernoulli numerators / Q(zeta_37)")
    print("   neither implies the other.\n")
    print("  the GF(37) reading is noise: k = 32 is in SEED, but the first")
    print("  nine irregular indices scatter over %d orbits, SEED twice."
          % len(set(orbs)))
    print("  1 of 12, post hoc, n = 1.")
    print("\n  ALL ASSERTIONS PASS")


if __name__ == '__main__':
    run()
