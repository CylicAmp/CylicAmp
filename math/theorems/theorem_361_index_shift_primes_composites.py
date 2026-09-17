# CLASS: THEOREM
"""
Theorem 361: a_n -> a_n + n on primes and on composites -- the overlap is
three terms deep and was forced to break
Author: Michael Warren Song (CyclicAmp)

Supplied as two lists, "original" and "missing", presented as separate
observations. They are one construction applied to the two complementary
sequences:

    original   p_n + n    2+1, 3+2, 5+3, 7+4   ->   3,  5,  8, 11
    missing    c_n + n    4+1, 6+2, 8+3, 9+4   ->   5,  8, 11, 13

The second terms 1,2,3,4 are the index in both. Same map, two inputs.

=== THE OVERLAP, AND WHAT IS FORCED IN IT ===

    The sum-sets share {5, 8, 11}, the missing list shifted one place. The
    condition for that is

        c_n + n = p_{n+1} + (n+1)   <=>   c_n = p_{n+1} + 1.

    THE EQUIVALENCE IS FORCED -- it is one line of algebra, nothing more.
    THE INPUT FACT IS CONTINGENT. c_n = p_{n+1} + 1 holds for n = 1,2,3:

        c_1 = 4 = 3+1    c_2 = 6 = 5+1    c_3 = 8 = 7+1

    because 3, 5, 7 are consecutive odd primes at gap 2, so 4, 6, 8 are
    exactly the evens that follow them. Nothing enforces that; it is the
    density of primes at the very bottom of the range. Keeping the two
    apart matters: a forced equivalence sitting on a contingent premise is
    not a forced result.

=== THEOREM ===

    Let p_n be the n-th prime, c_n the n-th composite, and

        d_n = c_n - (p_{n+1} + 1).

    Then the zero set of d is exactly

        { n : d_n = 0 }  =  {1, 2, 3}.

    In particular the three-term alignment 4 = 3+1, 6 = 5+1, 8 = 7+1 is a
    FINITE coincidence, not the start of a recurring correspondence.

=== PROOF ===

    Directly, d_1 = d_2 = d_3 = 0, and d_4 = 9 - (11 + 1) = -3.
    It remains to show d_n never returns to zero.

    For every n >= 1,

        d_{n+1} - d_n = (c_{n+1} - c_n) - (p_{n+2} - p_{n+1}).

    COMPOSITE GAPS ARE AT MOST 2.  A gap of 3 or more would put two
    consecutive integers c_n+1, c_n+2 both outside the composites, hence
    both prime.  Of two consecutive integers one is even, and the only even
    prime is 2, while c_n + 1 >= 5.  So no such gap exists and consecutive
    composites sit at distance 1 or 2.  (Checked to 200000: no composite
    c >= 4 has c+1 and c+2 both prime.  The check is a check; the argument
    is the proof.)

    PRIME GAPS ARE AT LEAST 2.  For n >= 1 we have p_{n+1} >= p_2 = 3, so
    p_{n+1} is odd and p_{n+2} - p_{n+1} >= 2.  The single prime gap of 1,
    namely p_2 - p_1 = 3 - 2, occurs at n = 0 and is outside the range.

    Hence d_{n+1} - d_n <= 2 - 2 = 0: d is non-increasing on n >= 1.  With
    d_4 = -3 this gives d_n <= -3 for every n >= 4, so no n >= 4 has
    d_n = 0, and the zero set is exactly {1, 2, 3}.   []

    PROOF DECOMPOSITION -- the two statements have distinct roles, and
    both are required.

      (1) MONOTONICITY

          d_(n+1) - d_n
            = (c_(n+1) - c_n) - (p_(n+2) - p_(n+1))
            <= 2 - 2
            = 0.

          Therefore

              d_(n+1) <= d_n

          for every n >= 1.

          This statement alone does not exclude zeros after n = 3:
          a non-increasing sequence may remain at zero indefinitely.

      (2) STRICT NEGATIVITY AT THE FIRST FAILURE

          d_4 = c_4 - (p_5 + 1)
              = 9 - (11 + 1)
              = -3 < 0.

          This statement alone does not control later terms.

      (3) COMBINATION

          From (1), for every n >= 4,

              d_n <= d_4 = -3 < 0.

          Therefore

              d_n != 0  for every n >= 4.

          Together with d_1 = d_2 = d_3 = 0,

              {n : d_n = 0} = {1, 2, 3}.

    This is the complete finite proof.  The zero set is established
    directly: the first three values are exactly zero, and monotonicity
    together with d_4 < 0 places every subsequent value strictly below
    zero.

    The value n = 4 is where the exact sequences first differ:

              c_4 = 9,
              p_5 + 1 = 12.

    The proof does not require any interpretation of this value beyond the
    strict inequality d_4 < 0.  Its role is precisely to establish that,
    once monotonicity is known, every subsequent d_n remains negative.

    THIS IS THE LOAD-BEARING RESULT.  It is what licenses the word
    "coincidence".  Calling a pattern a coincidence is as much a claim as
    calling it a structure, and without a complete zero set the label would
    be an interpretation imposed after the fact rather than a theorem.

=== ASYMPTOTIC SEPARATION (INDEPENDENT, AND WEAKER WHERE IT MATTERS) ===

    The finite argument already excludes every later equality.  Separately,
    composites have natural density 1 and primes density 1/log n, so

        c_n ~ n,    p_{n+1} ~ n log n,    d_n ~ n - n log n -> -infinity.

    The sequences do not merely fail to meet again; the separation grows
    without bound, on the order of n log n.

    NOTE WHAT THIS DOES NOT DO.  A sequence tending to -infinity may still
    return to zero finitely often first.  So the asymptotics alone would
    NOT give the zero set, and "just a three-term coincidence" argued from
    density alone would be numerology with the sign reversed.  The gap
    inequality is what forbids recovery at every finite n.

=== THE FIRST FAILURE IS LOCAL; THE DIVERGENCE IS GLOBAL ===

    c_4 = 9 != p_5 + 1 = 12 fails twice over -- 9 is the first ODD
    composite, and the gap 7 -> 11 is 4.  Both are true and both are local.
    They say where the alignment first becomes visibly broken.  They are
    not the mechanism: that is the gap inequality for recovery, and the
    density mismatch for scale.

=== IT WAS GOING TO BREAK, AND THE LOCAL REASONS ARE SYMPTOMS ===

    At n = 4 it fails twice over -- c_4 = 9 is the first ODD composite, and
    the prime gap 7 -> 11 is 4, putting p_5 + 1 = 12 out of reach. Both are
    true, and both are local. The governing reason is density:

        composites have density 1     =>  c_n ~ n
        primes have density 1/log n   =>  p_n ~ n log n
        so  d_n := c_n - (p_{n+1}+1) ~ n - n log n  ->  -infinity.

        n         4      5     10     100     1000    10000    50000
        d_n      -3     -4    -14   -415    -6731   -93370  -556311

    FOUR CLAIMS, SEPARATED -- the asymptotic argument above does NOT by
    itself give the finite ones, and conflating them was the first draft's
    error:

      (1) EXACT.     d_1 = d_2 = d_3 = 0.
      (2) PROVED.    d_n is non-increasing for every n >= 1, and d_n <= -3
                     for every n >= 4.  Two lines:

                         d_{n+1} - d_n = (c_{n+1}-c_n) - (p_{n+2}-p_{n+1})

                     Composite gaps are 1 or 2 -- a gap of 3 or more would
                     need two consecutive integers both prime, which happens
                     only at (2,3).  Prime gaps are >= 2 above p = 3.  So
                     the difference is <= 2 - 2 = 0 always.  Monotonicity
                     plus d_4 = -3 then forces d_n <= -3 for all n >= 4.
                     Checked against the proof to n = 2000.
      (3) ASYMPTOTIC. d_n -> -infinity, by the density mismatch above.
      (4) INTERPRETATION. 9 is the first visible symptom, not the cause.

    (2) was recorded as "measured" in the first version of this file.  It is
    not measured; it is a consequence of the two gap bounds, and it is the
    claim that actually rules out recovery at any finite n.  (3) alone would
    permit d_n to wander back to 0 finitely often before diverging; (2) is
    what forbids that.

    So the three matches are the closing of a small-number window, not the
    opening of a structure. Had 9 been even and 11 been 9, the divergence
    would have taken over within a few more terms regardless.

=== THE PARITY NOTE THAT CAME WITH IT IS WRONG AS A RULE ===

    The supplied note offers "5 + 3 consists of two prime terms yielding a
    composite sum" as if it were a finding. But 3 + 2 is also two primes
    and gives 5, which is prime.

    The actual rule is parity, and it is forced: for odd primes p, q the
    sum p + q is even and > 2, hence composite, always. 3 + 2 escapes only
    because 2 is the even prime. So 8 in the original list is the single
    outcome available, not an observation about primes interacting.

=== GF(37): NOT A GOVERNING RULE, AND THE TWIN COUNT IS NOISE ===

    original   3:C3        5:CAS_EXT   8:TESLA   11:NEG_H
    missing    5:CAS_EXT   8:TESLA    11:NEG_H   13:CAS_EXT

    CAS_EXT = {5,13,19} holds both endpoints of the missing list. It is two
    of three, not a closed orbit: the next missing term is c_5 + 5 = 15,
    not 19. Recorded at that strength and no higher.

    The union {3,5,8,11,13} has four primes, 3,5,11,13, which are exactly
    the twin pairs (3,5) and (11,13), with 8 the lone composite and that
    one parity-forced. Tier-tested rather than reported: in [3,13] the twin
    members are {3,5,7,11,13}, five of eleven, so a random 5-subset carries
    four or more twin members with probability 0.067. Post hoc, n = 1. No
    signal. At this height nearly everything is prime or adjacent to one.

=== WHAT SURVIVES ===
    One sentence: the same index-shift on primes and on composites agrees
    for three terms because c_n = p_{n+1} + 1 there, and cannot agree again
    because composites outrun primes. Everything else here is forced,
    contingent, or noise, and is labelled as such above.

=== FALSIFICATION ===
    An n > 3 with c_n = p_{n+1} + 1; or d_n returning to 0; or the 0.067
    baseline being computed wrong.
"""
from sympy import isprime, prime

ORBITS = {
    'IC': (1, 10, 26), 'DARK_A': (2, 15, 20), 'C3': (3, 4, 30),
    'CAS_EXT': (5, 13, 19), 'TESLA': (6, 8, 23), 'D7': (7, 33, 34),
    'SA_ST_A': (9, 12, 16), 'NEG_H': (11, 27, 36), 'C9': (14, 29, 31),
    'NQR17': (17, 22, 35), 'SEED': (18, 24, 32), 'SA_ST_B': (21, 25, 28),
}


def orbit_of(n):
    r = n % 37
    return 'SEAM' if r == 0 else next(k for k, v in ORBITS.items() if r in v)


def composites(limit):
    s = bytearray([1]) * (limit + 1)
    s[0] = s[1] = 0
    for i in range(2, int(limit ** 0.5) + 1):
        if s[i]:
            s[i * i::i] = bytearray(len(s[i * i::i]))
    return [i for i in range(2, limit + 1) if not s[i]]


def run():
    C = composites(300000)
    P = [prime(n) for n in range(1, 6)]

    # --- the two lists are one construction ---
    orig = [P[n] + (n + 1) for n in range(4)]
    miss = [C[n] + (n + 1) for n in range(4)]
    assert orig == [3, 5, 8, 11] and miss == [5, 8, 11, 13]
    assert sorted(set(orig) & set(miss)) == [5, 8, 11]

    # --- equivalence forced; input fact contingent, true for exactly n<=3 ---
    for n in range(1, 8):
        shift = (C[n - 1] + n == prime(n + 1) + (n + 1))
        assert shift == (C[n - 1] == prime(n + 1) + 1)      # the algebra
        assert shift == (n <= 3), (n, shift)                 # the premise
    assert (C[0], C[1], C[2]) == (4, 6, 8) == (P[1] + 1, P[2] + 1, P[3] + 1)
    assert C[3] == 9 and prime(5) + 1 == 12                  # the break

    # --- d_n: strictly negative from n=4, monotone, never returns ---
    d = [C[n - 1] - (prime(n + 1) + 1) for n in range(1, 2000)]
    assert d[:3] == [0, 0, 0]                                # (1) exact
    # (2) proved: the two gap bounds the monotonicity argument rests on
    gaps_c = {C[i + 1] - C[i] for i in range(20000)}
    assert gaps_c == {1, 2}                                  # composite gaps
    # the ARGUMENT behind that bound, not just the observation:
    assert not any(not isprime(c) and isprime(c + 1) and isprime(c + 2)
                   for c in range(4, 200000))
    # THE THEOREM: the zero set is exactly {1,2,3}
    assert [n for n in range(1, 2000) if d[n - 1] == 0] == [1, 2, 3]
    assert d[3] == 9 - (11 + 1) == -3 < 0                     # (2)
    assert all(x <= d[3] for x in d[3:])                      # (3) from (1),(2)
    assert all(prime(n + 2) - prime(n + 1) >= 2 for n in range(1, 2000))
    assert all(d[i + 1] - d[i] <= 0 for i in range(len(d) - 1))
    assert d[3] == -3 and all(x <= -3 for x in d[3:])         # forced by (2)
    big = {n: C[n - 1] - (prime(n + 1) + 1) for n in (4, 5, 10, 100, 1000)}
    assert big == {4: -3, 5: -4, 10: -14, 100: -415, 1000: -6731}

    # --- parity: the note's rule fails, the real one is forced ---
    assert isprime(3 + 2)                       # two primes -> prime
    assert not isprime(5 + 3)                   # two primes -> composite
    for p in [q for q in range(3, 200) if isprime(q)]:
        for q in [r for r in range(3, 200) if isprime(r)]:
            assert not isprime(p + q)           # both odd => forced composite

    # --- GF(37), graded down ---
    assert [orbit_of(x) for x in orig] == ['C3', 'CAS_EXT', 'TESLA', 'NEG_H']
    assert [orbit_of(x) for x in miss] == ['CAS_EXT', 'TESLA', 'NEG_H', 'CAS_EXT']
    assert {5, 13} < set(ORBITS['CAS_EXT'])     # two of three, proper subset
    assert C[4] + 5 == 15 and orbit_of(15) != 'CAS_EXT'   # next term misses

    print("T361  a_n -> a_n + n, on primes and on composites\n")
    print("  original  p_n + n :", orig)
    print("  missing   c_n + n :", miss)
    print("  shared            :", sorted(set(orig) & set(miss)), "-- one-place shift\n")
    print("  FORCED      c_n + n = p_(n+1) + (n+1)  <=>  c_n = p_(n+1) + 1")
    print("  CONTINGENT  that premise holds for n = 1,2,3 only, because 3,5,7")
    print("              are consecutive odd primes at gap 2\n")
    print("  d_n = c_n - (p_(n+1)+1):  n=1..3 zero, then")
    print("   ", {k: v for k, v in big.items()})
    print("  THEOREM  d_n = c_n - (p_(n+1)+1)")
    print("   (a) d_1 = d_2 = d_3 = 0, d_4 = -3")
    print("   (b) d_(n+1) <= d_n for every n >= 1   [composite gaps <= 2,")
    print("       prime gaps >= 2, so the difference is <= 0]")
    print("   (c) hence d_n <= -3 for n >= 4: {1,2,3} is the COMPLETE zero set")
    print("   (d) separately, d_n ~ -n log n -> -infinity")
    print("   the table above VERIFIES the implementation; (b),(c) are proved.\n")
    print("  (1) exact       d_1 = d_2 = d_3 = 0")
    print("  (2) proved      non-increasing for all n >= 1, and <= -3 for n >= 4:")
    print("                  composite gaps are 1 or 2 (two consecutive integers")
    print("                  both prime only at 2,3); prime gaps are >= 2; so")
    print("                  d_(n+1) - d_n <= 2 - 2 = 0.  Not a measurement.")
    print("  (3) asymptotic  c_n ~ n vs p_n ~ n log n, so d_n -> -infinity")
    print("  (4) reading     9 is the first symptom, not the cause")
    print("  (3) alone would allow d_n back to 0 finitely often; (2) forbids it.\n")
    print("  parity: two ODD primes always sum to an even number > 2.")
    print("  3+2 = 5 is prime only because 2 is the even prime, so the")
    print("  supplied 'two primes give a composite' note is not a rule.\n")
    print("  GF(37):", [orbit_of(x) for x in miss], "-- CAS_EXT at both ends,")
    print("  but {5,13} is 2 of 3 and the next term is 15, not 19. Not an orbit.")
    print("  twin count in the union: 4 of 5, baseline p = 0.067, post hoc. Noise.")
    print("\n  ALL ASSERTIONS PASS")


if __name__ == '__main__':
    run()
