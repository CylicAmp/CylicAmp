"""
shared_numerator_difference.py

WHEN DOES A DIFFERENCE OF TWO FRACTIONS WITH THE SAME NUMERATOR SQUARE
THAT NUMERATOR?

The starting observation is

    1.5 - 0.6 = 0.9,    i.e.    3/2 - 3/5 = (15-6)/10 = 9/10 = 3^2/(2*5):

the prime 3 is the shared numerator, the denominators 2 and 5 combine into
10, and the result carries 3 SQUARED. This module settles exactly when that
happens, and the answer turns out to be about twin primes.

--------------------------------------------------------------------
LEMMA 1   THE MECHANISM
--------------------------------------------------------------------
For any a and any b < c,

    a/b - a/c = a(c - b)/(bc),

so the numerator is a^2 if and only if

    c - b = a.

In 3/2 - 3/5 the gap 5 - 2 is 3, which is the shared numerator itself. So
the squaring is not a separate fact about 3 sitting next to 2 and 5 -- it
is the gap between the denominators coinciding with the numerator. Nothing
about primality is needed for this part.

--------------------------------------------------------------------
LEMMA 2   THE PARITY SPLIT, WHEN a, b, c ARE ALL PRIME
--------------------------------------------------------------------
Require a, b, c prime with c - b = a.

  * If a is ODD, then b and c = b + a have opposite parity, so one of them
    is even, and the only even prime is 2. Since b < c this forces

        b = 2,    c = a + 2,

    a SINGLE candidate, which exists exactly when a + 2 is also prime --
    that is, exactly when (a, a+2) is a twin prime pair.

  * If a = 2, the parity obstruction disappears: c - b = 2 with b, c prime
    says precisely that (b, c) is a twin prime pair, and there are
    infinitely many of those conjecturally.

--------------------------------------------------------------------
THEOREM   EVERY INSTANCE IS A TWIN PRIME PAIR
--------------------------------------------------------------------
For primes a, b, c with b < c,

    a/b - a/c = a^2/(bc)

holds if and only if one of the following, and in both cases a twin prime
pair is what makes it work:

    a = 2       and (b, c) is a twin prime pair     -- the twins are the
                                                       DENOMINATORS
    a odd       and b = 2, c = a + 2, with (a, a+2)
                a twin prime pair                  -- the twins are the
                                                       NUMERATOR and the
                                                       larger denominator

The two closed forms:

    a odd:   a/2 - a/(a+2) = a^2 / (2(a+2))
    a = 2:   2/p - 2/(p+2) = 2^2 / (p(p+2))

Both are automatically in lowest terms: gcd(a^2, 2(a+2)) = 1 because a is
an odd prime dividing neither 2 nor a+2, and gcd(4, p(p+2)) = 1 because p
and p+2 are odd.

--------------------------------------------------------------------
WHAT THIS SAYS ABOUT 3/2 - 3/5 SPECIFICALLY
--------------------------------------------------------------------
For EACH odd prime a there is AT MOST ONE such identity, and it exists iff
a is the smaller member of a twin pair. So

    3/2 - 3/5 = 3^2/(2*5)

is the unique identity of this shape with shared numerator 3 -- not one
example among many for that numerator, but the only one. The next few:

    5/2  - 5/7   = 5^2/(2*7)   = 25/14
    11/2 - 11/13 = 11^2/(2*13) = 121/26
    17/2 - 17/19 = 17^2/(2*19) = 289/38

and a = 7, 13, 19, 23 admit none at all, because 9, 15, 21 and 25 are
composite. The odd a that work are exactly 3, 5, 11, 17, 29, 41, 59, 71,
101, 107, ... -- the smaller members of twin pairs, i.e. OEIS A001359.

3 is where this list begins, and its identity has the smallest possible
denominators, 2 and 5.

--------------------------------------------------------------------
SCOPE
--------------------------------------------------------------------
The classification is complete and elementary; no part of it is
conjectural. What IS open is only how many instances exist: the a = 2 row
is infinite iff the twin prime conjecture holds, and the odd rows are
indexed by A001359, so the count of odd a that work is infinite under the
same conjecture. Nothing here bears on that conjecture in either
direction -- it reformulates the twin condition, it does not approach it.
"""

from fractions import Fraction
from math import gcd, isqrt
from typing import List, Tuple


def is_prime(n: int) -> bool:
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


def squares_numerator(a: int, b: int, c: int) -> bool:
    """Does a/b - a/c equal a^2/(bc)?"""
    return Fraction(a, b) - Fraction(a, c) == Fraction(a * a, b * c)


def is_twin_pair(p: int, q: int) -> bool:
    return q - p == 2 and is_prime(p) and is_prime(q)


def instances(a_max: int, c_max: int) -> List[Tuple[int, int, int]]:
    """All prime triples a, b < c below the bounds with a/b - a/c = a^2/(bc)."""
    pr = [p for p in range(2, max(a_max, c_max) + 1) if is_prime(p)]
    out = []
    for a in (p for p in pr if p <= a_max):
        for b in (p for p in pr if p <= c_max):
            for c in (p for p in pr if b < p <= c_max):
                if squares_numerator(a, b, c):
                    out.append((a, b, c))
    return out


def odd_form(a: int) -> Tuple[Fraction, Fraction]:
    """a/2 - a/(a+2) and its closed form a^2/(2(a+2))."""
    return Fraction(a, 2) - Fraction(a, a + 2), Fraction(a * a, 2 * (a + 2))


def even_form(p: int) -> Tuple[Fraction, Fraction]:
    """2/p - 2/(p+2) and its closed form 4/(p(p+2))."""
    return Fraction(2, p) - Fraction(2, p + 2), Fraction(4, p * (p + 2))


def twin_smaller(limit: int) -> List[int]:
    return [p for p in range(2, limit) if is_prime(p) and is_prime(p + 2)]


# =====================================================================
# SELF-TESTS
# =====================================================================

def test_the_starting_observation() -> None:
    assert 1.5 - 0.6 == 0.9
    assert Fraction(3, 2) - Fraction(3, 5) == Fraction(9, 10)
    assert Fraction(9, 10) == Fraction(3 * 3, 2 * 5)
    assert (15 - 6, 10) == (9, 10)
    print("[ok] 1.5 - 0.6 = 0.9, and 3/2 - 3/5 = 9/10 = 3^2/(2*5)")


def test_lemma1_mechanism() -> None:
    """a/b - a/c = a^2/(bc) iff c - b = a, for ALL a and b < c."""
    for a in range(1, 40):
        for b in range(1, 40):
            for c in range(b + 1, 60):
                assert squares_numerator(a, b, c) == (c - b == a), (a, b, c)
                assert (Fraction(a, b) - Fraction(a, c)
                        == Fraction(a * (c - b), b * c)), (a, b, c)
    print("[ok] lemma 1: the numerator squares exactly when c - b = a")


def test_lemma2_parity_split() -> None:
    """Odd a forces b = 2 and c = a + 2; a = 2 gives twin denominators."""
    for a in (p for p in range(3, 200, 2) if is_prime(p)):
        sols = [(b, b + a) for b in range(2, 400)
                if is_prime(b) and is_prime(b + a)]
        assert all(b == 2 for b, _ in sols), (a, sols)
        assert len(sols) <= 1, (a, sols)
        assert bool(sols) == is_prime(a + 2), (a, sols)
    twos = [(b, b + 2) for b in range(2, 200)
            if is_prime(b) and is_prime(b + 2)]
    assert len(twos) > 10 and all(is_twin_pair(*t) for t in twos)
    print(f"[ok] lemma 2: odd a admits at most one pair (always b=2); "
          f"a=2 gives {len(twos)} twin pairs below 200")


def test_theorem_every_instance_is_twin() -> None:
    sols = instances(120, 400)
    assert sols, "there should be instances"
    for a, b, c in sols:
        assert c - b == a, (a, b, c)
        if a == 2:
            assert is_twin_pair(b, c), (a, b, c)
        else:
            assert b == 2 and c == a + 2, (a, b, c)
            assert is_twin_pair(a, c), (a, b, c)
    print(f"[ok] theorem: all {len(sols)} instances carry a twin pair "
          f"(denominators when a=2, {{a, c}} when a is odd)")


def test_odd_a_are_exactly_the_twin_smaller_primes() -> None:
    sols = instances(120, 400)
    odd_a = sorted({a for a, _, _ in sols if a % 2 == 1})
    expect = [p for p in twin_smaller(120) if p % 2 == 1]
    assert odd_a == expect, (odd_a, expect)
    assert odd_a[:6] == [3, 5, 11, 17, 29, 41], odd_a
    for a in (7, 13, 19, 23):
        assert is_prime(a) and not is_prime(a + 2)
        assert a not in odd_a, a
    print(f"[ok] the odd a that work are exactly the twin-smaller primes: "
          f"{odd_a[:8]} ...")


def test_closed_forms_and_lowest_terms() -> None:
    for a in twin_smaller(400):
        if a == 2:
            continue
        lhs, rhs = odd_form(a)
        assert lhs == rhs, a
        assert gcd(a * a, 2 * (a + 2)) == 1, a
    for p in twin_smaller(400):
        lhs, rhs = even_form(p)
        assert lhs == rhs, p
        assert gcd(4, p * (p + 2)) == 1, p
    assert odd_form(3)[0] == Fraction(9, 10)
    assert odd_form(5)[0] == Fraction(25, 14)
    assert even_form(3)[0] == Fraction(4, 15)
    print("[ok] both closed forms hold and are automatically in lowest terms")


def test_uniqueness_for_numerator_three() -> None:
    """3/2 - 3/5 is the ONLY instance with shared numerator 3."""
    three = [s for s in instances(3, 2000) if s[0] == 3]
    assert three == [(3, 2, 5)], three
    print("[ok] 3/2 - 3/5 = 3^2/(2*5) is the unique instance for numerator 3")


def test_scope_no_claim_about_twins() -> None:
    """The classification is unconditional; only the COUNT is conjectural."""
    assert len(twin_smaller(1000)) == 35, len(twin_smaller(1000))
    assert is_twin_pair(3, 5) and not is_twin_pair(7, 9)
    print("[ok] scope: classification is unconditional; only how MANY "
          "instances exist depends on the twin prime conjecture")


def self_test() -> None:
    test_the_starting_observation()
    test_lemma1_mechanism()
    test_lemma2_parity_split()
    test_theorem_every_instance_is_twin()
    test_odd_a_are_exactly_the_twin_smaller_primes()
    test_closed_forms_and_lowest_terms()
    test_uniqueness_for_numerator_three()
    test_scope_no_claim_about_twins()
    print("\nAll self-tests passed.")
    print("THEOREM. For primes a, b < c,  a/b - a/c = a^2/(bc)  holds iff")
    print("  a = 2 and (b,c) is a twin pair      -- twins as DENOMINATORS")
    print("  a odd, b = 2, c = a+2, (a,a+2) twin -- twins as NUMERATOR and")
    print("                                         larger DENOMINATOR")
    print("Both branches are governed by twin primes. For each odd a there is")
    print("at most ONE instance, so 3/2 - 3/5 = 3^2/(2*5) is the unique")
    print("identity of this shape with shared numerator 3.")


if __name__ == "__main__":
    self_test()
