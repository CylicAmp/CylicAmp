# CLASS: THEOREM
"""
The unit-offset quadruplet {n+-1, n+-5}: a transversal of (Z/12Z)*

Written from the configuration  7 - (11 13) - 17.

PRIOR ART, checked first.
  twin_midpoint_dr_axis.py (THEOREM 71) already owns the statement that a
  twin pair's midpoint is divisible by 6, with the chi_{-3} and DR-in-{3,6,9}
  consequences.  Part (a) of the LEMMA below IS that result and is cited, not
  claimed.
  constellation_mirror_audit.py is the methodological precedent: it audits the
  SIX-prime mirror constellation {c+-1, c+-11, c+-13} and proves a covering
  theorem for it -- that the three pair-starts, being spaced 12 apart with
  DR(12) = 3, necessarily cover the three DR tracks {2,5,8}.  The pattern
  here is different (four primes, offsets 1 and 5, not six primes with
  offsets 1, 11, 13) and the covering is mod 12 rather than mod 9, but the
  shape of the argument is theirs.
  mod12_collision_audit.py owns the collision law  f(n-d) = f(n+d) <=> 6 | d
  for f(x) = x mod 12.  THEOREM 1 below is built on it.
  prime_lanes_6k_audit_2026_10_03.py owns the 6k+-1 lane framing.
  prime_quartet_chains_palindromes.py owns the FIRST four primes {2,3,5,7};
  this file is about a different quartet.

WHAT IS NEW: the offsets-are-the-units observation and THEOREM 1, part (b)
of the lemma (consecutiveness is automatic), the identification of 12 as the
first centre with the n = 6 degeneracy, and THEOREM 2.

====================================================================
THE CONFIGURATION
====================================================================

        7  -  (11  13)  -  17

    gaps 4, 2, 4 -- symmetric.  Four consecutive primes.  Centre 12:

        7 = 12 - 5     11 = 12 - 1     13 = 12 + 1     17 = 12 + 5

The offsets are {-5, -1, +1, +5}.  Reduced mod 12 those are {7, 11, 1, 5},
which is exactly

        (Z/12Z)*  =  {1, 5, 7, 11}.

So the offset set IS the unit group mod 12, written with signed
representatives of least absolute value.  That is the whole reason the
pattern behaves, and it is what the two theorems below make precise.

====================================================================
LEMMA (the centre).
====================================================================
Let n > 8 and suppose n-5, n-1, n+1, n+5 are all prime.  Then

    (a)  n = 0  (mod 6), and
    (b)  n-5, n-1, n+1, n+5 are CONSECUTIVE primes.

PROOF.
  (a) is THEOREM 71: n-1 and n+1 are twin primes both exceeding 3, so their
      midpoint n is divisible by 6.
  (b) Given (a), every integer strictly between n-5 and n+5 other than
      n+-1 is composite:
          n-4, n-2, n+2, n+4   are even and exceed 2   (n is even),
          n-3, n+3             are divisible by 3 and exceed 3 (3 | n),
          n                    is divisible by 6.
      So the only primes in the open interval (n-6, n+6) are the four
      listed, and they are therefore consecutive.  QED

Part (b) is what makes the configuration rigid: one cannot have a symmetric
+-1, +-5 prime quadruplet with anything hiding between its members.

====================================================================
THEOREM 1 (the transversal).
====================================================================
For every n = 0 (mod 6),

    { n-5, n-1, n+1, n+5 }  reduced mod 12  =  (Z/12Z)*  =  {1, 5, 7, 11},

each unit hit exactly once.  No primality is needed; primality of n+-1 only
supplies the hypothesis n = 0 (mod 6) via the LEMMA.

PROOF.  n = 0 (mod 6) means n = 0 or 6 (mod 12).
    n = 0  (mod 12):  {n-5, n-1, n+1, n+5} = { 7, 11,  1,  5}  (mod 12)
    n = 6  (mod 12):  {n-5, n-1, n+1, n+5} = { 1,  5,  7, 11}  (mod 12)
  the same four residues either way.  Injectivity is the collision law of
  mod12_collision_audit.py: n-d and n+d agree mod 12 exactly when 6 | d,
  and here d = 1, 5, neither divisible by 6, so the two members of each
  pair differ; and the pairs differ from each other because 1 != +-5
  (mod 12).  Four distinct units in a group of order 4 is all of it.  QED

COROLLARY.  When the four are prime this is forced twice over, since every
prime exceeding 3 is coprime to 12 and so already lies in {1,5,7,11}.  The
quadruplet is then a complete set of prime representatives of (Z/12Z)*.

====================================================================
12 IS THE FIRST CENTRE, AND 6 IS THE DEGENERATE ONE
====================================================================
Centres below 1200:

    12, 18, 42, 102, 108, 228, 312, 462, 858, 882, 1092
     |
     +-- {7, 11, 13, 17}

all = 0 (mod 6), all giving four consecutive primes, all hitting
{1,5,7,11} mod 12.

At n = 6 the pattern degenerates in the prettiest way available:

    {6-5, 6-1, 6+1, 6+5}  =  {1, 5, 7, 11}  =  (Z/12Z)*  as integers.

Three of those are prime; 1 is not.  So n = 6 is where the quadruplet IS
the unit group, and n = 12 is the first place where the unit group is lifted
by four primes.  The LEMMA needs n > 8 precisely to exclude n = 6.

====================================================================
THEOREM 2 (the DR classes), after constellation_mirror_audit.py
====================================================================
For n = 0 (mod 6), the multiset of digital roots of {n+-1, n+-5} depends
only on n mod 9, which lies in {0, 3, 6}, giving exactly three patterns:

    n = 3 (mod 9):  DRs {7, 2, 4, 8}      e.g. n = 12, 102, 228
    n = 0 (mod 9):  DRs {4, 8, 1, 5}      e.g. n = 18, 108
    n = 6 (mod 9):  DRs {1, 5, 7, 2}      e.g. n = 42

Each pattern omits two of the six residues coprime to 3, and the three
patterns together cover all six, {1,2,4,5,7,8}.  Stepping n by 6 permutes
the three patterns cyclically, the same 3-cycle mechanism
constellation_mirror_audit.py uses for its mod-9 tracks.

No DR is ever a multiple of 3, since 3 | n forces 3 to miss n+-1 and n+-5.

====================================================================
THE ARITHMETIC OF THE PAIRS
====================================================================
Both pairs sum to 2n, and the products follow the difference of squares:

    (n-1) + (n+1) = (n-5) + (n+5) = 2n
    (n-1)(n+1) = n^2 - 1          (n-5)(n+5) = n^2 - 25
    difference  = 24,  independent of n

At n = 12: 11 + 13 = 7 + 17 = 24, and 143 - 119 = 24.  The 24 appears twice
for two different reasons -- once as 2n and once as 25 - 1 -- and only at
n = 12 do they coincide.

GOLDBACH.  2n = 24 has exactly three prime partitions, 5+19, 7+17, 11+13,
and the quadruplet displays two of them nested.  The third, 5 + 19, is the
+-7 pair; 7 is not a unit mod 12 (gcd(7,12)=1, so it is -- but 7 > 6, so
+-7 is not a least-absolute-value unit representative), which is why it
sits outside the quadruplet.

THE PRODUCT.  7 * 11 * 13 = 1001 = 10^3 + 1, so three of the four primes are
the factorisation of the m = 3 annihilator of abcba_place_value_grid.py, and

    7 * 11 * 13 * 17 = 17017 = 17 * 1001.

Recorded as an identity about this quadruplet only; 17 divides 10^8 + 1, a
different layer, and no claim is made that the two are related.
"""

from math import gcd

OFFSETS = (-5, -1, 1, 5)
UNITS_MOD_12 = (1, 5, 7, 11)
FIRST_CENTRE = 12
FIRST_QUADRUPLET = (7, 11, 13, 17)
DEGENERATE_CENTRE = 6
CENTRES_BELOW_1200 = [12, 18, 42, 102, 108, 228, 312, 462, 858, 882, 1092]
DR_PATTERNS = {3: [7, 2, 4, 8], 0: [4, 8, 1, 5], 6: [1, 5, 7, 2]}


def is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


def digital_root(n):
    return 9 if n == 0 else (n - 1) % 9 + 1


def quadruplet(n):
    """The four integers n-5, n-1, n+1, n+5."""
    return tuple(n + o for o in OFFSETS)


def is_centre(n):
    """True if all four members of the quadruplet at n are prime."""
    return all(is_prime(x) for x in quadruplet(n))


def centres(limit):
    return [n for n in range(1, limit) if is_centre(n)]


def residues_mod_12(n):
    return sorted(x % 12 for x in quadruplet(n))


def units_mod(m):
    return tuple(u for u in range(m) if gcd(u, m) == 1)


# =====================================================================
#                             SELF-TESTS
# =====================================================================
def test_the_configuration():
    assert quadruplet(FIRST_CENTRE) == FIRST_QUADRUPLET
    assert all(is_prime(p) for p in FIRST_QUADRUPLET)
    # four CONSECUTIVE primes
    assert [q for q in range(7, 18) if is_prime(q)] == list(FIRST_QUADRUPLET)
    # gaps 4, 2, 4
    g = [FIRST_QUADRUPLET[i + 1] - FIRST_QUADRUPLET[i] for i in range(3)]
    assert g == [4, 2, 4]
    # the offsets, reduced mod 12, ARE the unit group
    assert sorted(o % 12 for o in OFFSETS) == list(UNITS_MOD_12)
    assert units_mod(12) == UNITS_MOD_12
    print("  config  7-(11 13)-17: consecutive, gaps 4,2,4, offsets mod 12 "
          "= (Z/12Z)*")


def test_lemma_a_is_theorem_71():
    """Part (a): twin primes above 3 have a midpoint divisible by 6."""
    n = 5
    found = 0
    while found < 400:
        n += 2
        if is_prime(n) and is_prime(n + 2):
            assert (n + 1) % 6 == 0, n
            found += 1
    # and the midpoint DR is in {3,6,9}, THEOREM 71's companion claim
    n = 5
    found = 0
    while found < 200:
        n += 2
        if is_prime(n) and is_prime(n + 2):
            assert digital_root(n + 1) in {3, 6, 9}, n
            found += 1
    print("  lemma a (= THEOREM 71) twin midpoint divisible by 6, DR in {3,6,9}")


def test_lemma_b_consecutiveness_is_automatic():
    """Part (b): with 6 | n, nothing between n-5 and n+5 is prime but n+-1."""
    for n in range(12, 20000, 6):
        inner = [x for x in range(n - 4, n + 5) if x not in (n - 1, n + 1)]
        # every one of those is even or divisible by 3, hence composite
        for x in inner:
            assert x % 2 == 0 or x % 3 == 0, (n, x)
            assert not is_prime(x), (n, x)
    # so for any centre, the four really are consecutive primes
    for n in CENTRES_BELOW_1200:
        assert [q for q in range(n - 5, n + 6) if is_prime(q)] == \
               list(quadruplet(n)), n
    print("  lemma b  consecutiveness automatic once 6 | n, no exceptions")


def test_theorem_1_transversal():
    """Unconditional for 6 | n -- primality is not used."""
    for n in range(6, 60000, 6):
        assert residues_mod_12(n) == list(UNITS_MOD_12), n
    # the two cases of the proof
    assert sorted((0 + o) % 12 for o in OFFSETS) == list(UNITS_MOD_12)
    assert sorted((6 + o) % 12 for o in OFFSETS) == list(UNITS_MOD_12)
    # injectivity via the collision law: n-d = n+d (mod 12) iff 6 | d
    for d in range(1, 40):
        collide = (12 - d) % 12 == (12 + d) % 12
        assert collide == (d % 6 == 0), d
    for d in (1, 5):
        assert d % 6 != 0
    # it FAILS when 6 does not divide n -- the hypothesis is doing work
    offenders = [n for n in range(1, 400) if n % 6 and
                 residues_mod_12(n) == list(UNITS_MOD_12)]
    assert offenders == [], offenders
    print("  thm 1   {n+-1, n+-5} mod 12 = (Z/12Z)* for every 6 | n, "
          "and for no other n")


def test_twelve_is_first_and_six_is_degenerate():
    c = centres(1200)
    assert c == CENTRES_BELOW_1200, c
    assert c[0] == FIRST_CENTRE == 12
    assert all(n % 6 == 0 for n in c)
    # n = 6: the quadruplet IS the unit group, as integers
    assert quadruplet(DEGENERATE_CENTRE) == UNITS_MOD_12
    assert not is_centre(DEGENERATE_CENTRE)      # because 1 is not prime
    assert not is_prime(1)
    assert all(is_prime(x) for x in quadruplet(6) if x != 1)
    # nothing between 6 and 12 qualifies
    assert [n for n in range(7, 12) if is_centre(n)] == []
    print(f"  first   12 is the least centre; at n=6 the quadruplet is "
          f"{UNITS_MOD_12} itself, and 1 is not prime")


def test_theorem_2_dr_classes():
    for n in range(6, 20000, 6):
        pat = [digital_root(x) for x in quadruplet(n)]
        assert pat == DR_PATTERNS[n % 9], (n, pat)
        assert all(d % 3 for d in pat), (n, pat)      # never a multiple of 3
    # each pattern omits two of the six, and the three cover all six
    union = set()
    for pat in DR_PATTERNS.values():
        assert len(set(pat)) == 4
        union |= set(pat)
    assert union == {1, 2, 4, 5, 7, 8}
    assert set(DR_PATTERNS) == {0, 3, 6}
    # stepping n by 6 cycles the three patterns
    seen = [n % 9 for n in range(6, 6 + 6 * 7, 6)]
    assert seen == [6, 3, 0, 6, 3, 0, 6]
    print("  thm 2   DR pattern depends only on n mod 9, three classes "
          "covering {1,2,4,5,7,8}")


def test_pair_arithmetic():
    for n in range(6, 5000, 6):
        a, b, c, d = quadruplet(n)        # n-5, n-1, n+1, n+5
        assert b + c == a + d == 2 * n
        assert b * c == n * n - 1
        assert a * d == n * n - 25
        assert b * c - a * d == 24        # independent of n
    # at n = 12 the two 24s coincide, and only there
    assert 2 * 12 == 24 == 25 - 1
    assert [n for n in range(6, 2000, 6) if 2 * n == 24] == [12]
    # Goldbach partitions of 24
    parts = [(p, 24 - p) for p in range(2, 13)
             if is_prime(p) and is_prime(24 - p)]
    assert parts == [(5, 19), (7, 17), (11, 13)]
    assert (7, 17) in parts and (11, 13) in parts     # the nested two
    assert (5, 19) == (12 - 7, 12 + 7)                # the +-7 pair
    print("  pairs   both pairs sum to 2n; products differ by 24 always; "
          "24 has exactly 3 Goldbach partitions")


def test_product_is_1001_times_17():
    assert 7 * 11 * 13 == 1001 == 10 ** 3 + 1
    assert 7 * 11 * 13 * 17 == 17017 == 17 * 1001
    # cross-reference only: 17 belongs to a different layer
    assert (10 ** 8 + 1) % 17 == 0
    assert (10 ** 3 + 1) % 17 != 0
    print("  product 7*11*13 = 1001 = 10^3+1; whole product 17017 = 17*1001")


def test_does_not_prove_too_much():
    # the pattern is not generic: most multiples of 6 are not centres
    hits = len(centres(1200))
    assert 0 < hits < 40, hits
    # a quadruplet with a composite member is correctly rejected
    assert not is_centre(30)                  # 25 = 5^2
    assert not is_prime(25)
    assert not is_centre(72)                  # 77 = 7*11
    assert not is_prime(77)
    # THEOREM 1 is about residues, not primality: 30 still transversal
    assert residues_mod_12(30) == list(UNITS_MOD_12)
    assert not is_centre(30)
    # the LEMMA's n > 8 is needed, and 6 is the only thing it excludes
    assert quadruplet(6)[0] == 1 and not is_prime(1)
    print("  check   30 is transversal but not a centre (25 = 5^2); "
          "primality and residue claims stay separate")


def self_test():
    print("unit_offset_quadruplet_mod12.py self-tests\n")
    test_the_configuration()
    test_lemma_a_is_theorem_71()
    test_lemma_b_consecutiveness_is_automatic()
    test_theorem_1_transversal()
    test_twelve_is_first_and_six_is_degenerate()
    test_theorem_2_dr_classes()
    test_pair_arithmetic()
    test_product_is_1001_times_17()
    test_does_not_prove_too_much()
    print("\nAll assertions passed.")
    print("THE UNIT-OFFSET QUADRUPLET {n+-1, n+-5}")
    print("  the offsets, mod 12, ARE (Z/12Z)* = {1,5,7,11}")
    print("  LEMMA   6 | n (THEOREM 71), and then the four are consecutive")
    print("          primes -- nothing can hide between them")
    print("  THM 1   the four residues mod 12 are exactly the units, each")
    print("          once, for every 6 | n and for no other n")
    print("  THM 2   DR pattern is a function of n mod 9; three classes,")
    print("          together covering {1,2,4,5,7,8}, never a multiple of 3")
    print("  12 is the first centre: 7 - (11 13) - 17")
    print("  6 is degenerate: the quadruplet is {1,5,7,11} itself, 1 not prime")
    print("  both pairs sum to 2n; the products always differ by 24")


if __name__ == "__main__":
    self_test()
