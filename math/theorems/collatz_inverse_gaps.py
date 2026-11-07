"""
collatz_inverse_gaps.py

THE GAP LAW FOR THE INVERSE ACCELERATED COLLATZ MAP.

Setting. On the odd integers, the accelerated Collatz map is

    T(n) = (3n + 1) / 2^(v_2(3n+1)).

Read backwards it is a branching generator: the odd pre-images of an odd m
are the numbers n_k = (2^k m - 1)/3 for those k where that is an integer.
This module proves exactly which gaps n_{k2} - n_{k1} that generator can
produce, because a plausible-looking claim about it is false and the false
version is easy to re-derive.

--------------------------------------------------------------------
LEMMA 1   EXISTENCE AND THE PARITY FILTER
--------------------------------------------------------------------
n_k = (2^k m - 1)/3 is an integer exactly when 2^k m = 1 (mod 3). Since
2 = -1 (mod 3) this is (-1)^k m = 1 (mod 3), so:

    3 | m            NO pre-images at all   (2^k m = 0, never 1)
    m = 1 (mod 3)    k must be EVEN
    m = 2 (mod 3)    k must be ODD

When the condition holds, n_k really is an odd pre-image: 3 n_k + 1 = 2^k m
with m odd, so v_2(3 n_k + 1) = k exactly and T(n_k) = m; and 2^k m - 1 is
odd for k >= 1, so n_k is odd.

The first branch of this -- that a multiple of 3 has no pre-images -- is
why the gap law below comes out as cleanly as it does.

--------------------------------------------------------------------
LEMMA 2   THE EXACT GAP
--------------------------------------------------------------------
Let k_1 < k_2 both be valid for the same m. They share a parity, so
d := k_2 - k_1 is EVEN, and 3 | 2^d - 1. Writing j := (2^d - 1)/3,

    n_{k2} - n_{k1} = m (2^{k2} - 2^{k1}) / 3 = m * 2^{k_1} * j.

Both m and j are odd (2^d - 1 is odd, so dividing by 3 keeps it odd), so

    v_2(gap) = k_1   EXACTLY.

CONSECUTIVE BRANCHES. Consecutive valid exponents differ by 2, where
j = (2^2 - 1)/3 = 1, so the gap between consecutive pre-images is exactly

    n_{k+2} - n_k = m * 2^k,

which is why consecutive gaps scale by 2^2 = 4.

--------------------------------------------------------------------
THEOREM   WHEN IS THE GAP A MULTIPLE OF 6?
--------------------------------------------------------------------
    6 | (n_{k2} - n_{k1})     if and only if     6 | (k_2 - k_1).

Proof. The gap is m * 2^{k_1} * j with k_1 >= 1, so 2 always divides it and
the question is 3. Since 3 does not divide m (Lemma 1) and 3 is prime,
3 | gap iff 3 | j, i.e. iff 9 | 2^d - 1. The multiplicative order of 2
modulo 9 is 6, so that holds iff 6 | d. []

TWO CONSEQUENCES WORTH SEPARATING OUT:

  * NO consecutive gap is ever a multiple of 6. Consecutive branches have
    d = 2, and 6 does not divide 2. The gap is m * 2^k with 3 not dividing
    m, so it is never divisible by 3 at all. The first multiple-of-6 gap
    appears only at d = 6, three branch-steps apart.

  * The gaps are always EVEN, with 2-adic valuation exactly k_1.

--------------------------------------------------------------------
THE FALSE VERSION, AND WHY IT IS TEMPTING
--------------------------------------------------------------------
The claim "the inverse Collatz tree automatically generates gaps divisible
by 6" is FALSE, and it is worth recording because the derivation that
produces it is one step from correct. That derivation observes, rightly,
that

    2^{k2} - 2^{k1} = 2^{k_1} (2^d - 1)   is divisible by 6

(2 from the power, 3 from 2^d - 1 with d even) and then concludes 6 | gap.
But the gap DIVIDES BY 3:

    gap = m (2^{k2} - 2^{k1}) / 3.

The factor of 3 is consumed by that division, and only the factor 2
survives. The seed m = 7 is a clean refutation:

    k = 2, 4, 6, 8   ->   n = 9, 37, 149, 597
    gaps             ->   28, 112, 448
    each one = 4 (mod 6), never 0

Those are exactly the gaps m * 2^k = 7*4, 7*16, 7*64. The first gap from
m = 7 that IS divisible by 6 is k = 2 to k = 8, giving 597 - 9 = 588 = 6*98,
and d = 6 there, as the theorem requires.

--------------------------------------------------------------------
SCOPE -- what this does NOT say
--------------------------------------------------------------------
This is a statement about the inverse Collatz tree and nothing else. In
particular it says nothing about prime gaps. The resemblance to "twin-prime
gaps are divisible by 6" is a coincidence of the number 6: there it comes
from p > 3 forcing p = +-1 (mod 6), here from the order of 2 modulo 9.
Nothing transfers between them, and the frequent prime gaps are the
primorials 2, 6, 30, 210 -- 42 = 2*3*7 is not among them and has no
special status as a gap.
"""

from math import gcd
from typing import List, Optional


def accelerated_T(n: int) -> int:
    """T(n) = (3n+1)/2^v2(3n+1) for odd n."""
    if n % 2 == 0:
        raise ValueError("accelerated_T is defined on odd integers")
    x = 3 * n + 1
    # x // (x & -x) strips every factor of 2 at once: x & -x isolates the
    # lowest set bit, which is 2^v_2(x).
    return x // (x & -x)


def valid_exponents(m: int, limit: int) -> List[int]:
    """The k in [1, limit] for which (2^k m - 1)/3 is an integer."""
    if m % 3 == 0:
        return []
    return [k for k in range(1, limit + 1) if (pow(2, k) * m - 1) % 3 == 0]


def preimage(m: int, k: int) -> Optional[int]:
    """n_k = (2^k m - 1)/3, or None when k is not valid for m."""
    t = pow(2, k) * m - 1
    if t % 3:
        return None
    return t // 3


def gap(m: int, k1: int, k2: int) -> int:
    """n_{k2} - n_{k1}, by the closed form m * 2^k1 * (2^d - 1)/3."""
    d = k2 - k1
    return m * pow(2, k1) * ((pow(2, d) - 1) // 3)


def gap_divisible_by_6(m: int, k1: int, k2: int) -> bool:
    """The theorem, as a predicate: it depends ONLY on k2 - k1."""
    return (k2 - k1) % 6 == 0


def order_of_2_mod_9() -> int:
    return next(e for e in range(1, 10) if pow(2, e, 9) == 1)


# =====================================================================
# SELF-TESTS
# =====================================================================

def test_lemma1_parity_filter() -> None:
    for m in range(1, 400, 2):
        ks = valid_exponents(m, 12)
        if m % 3 == 0:
            assert ks == [], (m, ks)
            continue
        assert ks, m
        want_even = (m % 3 == 1)
        assert all((k % 2 == 0) == want_even for k in ks), (m, ks)
    print("[ok] lemma 1: 3 | m has no pre-images; otherwise k's parity is "
          "forced by m mod 3")


def test_lemma1_preimages_are_genuine() -> None:
    for m in range(1, 200, 2):
        if m % 3 == 0:
            continue
        for k in valid_exponents(m, 10):
            n = preimage(m, k)
            assert n is not None and n % 2 == 1, (m, k, n)
            assert 3 * n + 1 == pow(2, k) * m, (m, k)
            assert accelerated_T(n) == m, (m, k, n)
    print("[ok] lemma 1: every n_k is odd, with v_2(3n_k+1) = k and T(n_k) = m")


def test_lemma2_closed_form_and_valuation() -> None:
    for m in range(1, 150, 2):
        if m % 3 == 0:
            continue
        ks = valid_exponents(m, 14)
        for i in range(len(ks)):
            for j in range(i + 1, len(ks)):
                k1, k2 = ks[i], ks[j]
                g = preimage(m, k2) - preimage(m, k1)
                assert g == gap(m, k1, k2), (m, k1, k2)
                v = (g & -g).bit_length() - 1      # v_2(g)
                assert v == k1, (m, k1, k2, v)
    print("[ok] lemma 2: closed form holds and v_2(gap) = k_1 exactly")


def test_lemma2_consecutive_gap() -> None:
    for m in range(1, 300, 2):
        if m % 3 == 0:
            continue
        ks = valid_exponents(m, 14)
        for i in range(len(ks) - 1):
            k1, k2 = ks[i], ks[i + 1]
            assert k2 - k1 == 2, (m, k1, k2)
            g = preimage(m, k2) - preimage(m, k1)
            assert g == m * pow(2, k1), (m, k1, g)
        for i in range(len(ks) - 2):
            g1 = preimage(m, ks[i + 1]) - preimage(m, ks[i])
            g2 = preimage(m, ks[i + 2]) - preimage(m, ks[i + 1])
            assert g2 == 4 * g1, (m, i)
    print("[ok] lemma 2: consecutive gap is exactly m * 2^k, so gaps scale by 4")


def test_theorem_6_divides_gap() -> None:
    assert order_of_2_mod_9() == 6, order_of_2_mod_9()
    checked = 0
    for m in range(1, 900, 2):
        if m % 3 == 0:
            continue
        ks = valid_exponents(m, 34)
        for i in range(len(ks)):
            for j in range(i + 1, len(ks)):
                k1, k2 = ks[i], ks[j]
                g = preimage(m, k2) - preimage(m, k1)
                assert (g % 6 == 0) == gap_divisible_by_6(m, k1, k2), (m, k1, k2, g)
                assert g % 2 == 0, (m, k1, k2)
                checked += 1
    assert checked > 20000, checked
    print(f"[ok] theorem: 6 | gap iff 6 | (k2-k1), on {checked:,} branch pairs")


def test_no_consecutive_gap_is_divisible_by_6() -> None:
    for m in range(1, 500, 2):
        if m % 3 == 0:
            continue
        ks = valid_exponents(m, 16)
        for i in range(len(ks) - 1):
            g = preimage(m, ks[i + 1]) - preimage(m, ks[i])
            assert g % 3 != 0, (m, ks[i], g)
            assert g % 6 != 0, (m, ks[i], g)
    print("[ok] corollary: no consecutive gap is ever divisible by 6 (or by 3)")


def test_the_false_claim_is_false() -> None:
    """The m = 7 refutation, kept as a regression test."""
    ks = valid_exponents(7, 8)
    assert ks == [2, 4, 6, 8], ks
    ns = [preimage(7, k) for k in ks]
    assert ns == [9, 37, 149, 597], ns
    gaps = [ns[i + 1] - ns[i] for i in range(3)]
    assert gaps == [28, 112, 448], gaps
    assert all(g % 6 == 4 for g in gaps), gaps
    assert all(g == 7 * pow(2, k) for g, k in zip(gaps, [2, 4, 6]))
    # and the first gap from m=7 that IS divisible by 6
    g = preimage(7, 8) - preimage(7, 2)
    assert g == 588 and g % 6 == 0 and g == 6 * 98, g
    assert (8 - 2) % 6 == 0, "d = 6, as the theorem requires"
    print("[ok] the false claim: m=7 gives gaps 28, 112, 448, all 4 (mod 6); "
          "the first 6-divisible gap is 588 at d=6")


def test_scope_no_prime_gap_transfer() -> None:
    """6 arises here from ord_9(2); in prime gaps it arises from p = +-1 mod 6.
    The two are unrelated, and 42 is not a frequent prime gap."""
    from math import isqrt
    LIM = 200000
    s = bytearray([1]) * (LIM + 1)
    s[0:2] = b"\x00\x00"
    for i in range(2, isqrt(LIM) + 1):
        if s[i]:
            s[i * i::i] = bytearray(len(s[i * i::i]))
    pr = [i for i in range(LIM + 1) if s[i]]
    from collections import Counter
    g = Counter(pr[i + 1] - pr[i] for i in range(len(pr) - 1))
    top = [x for x, _ in g.most_common(8)]
    assert 6 in top, top
    assert 42 not in top, top
    assert g[30] > g[42], (g[30], g[42])
    for p in pr:
        if p > 3:
            assert p % 6 in (1, 5), p
    print(f"[ok] scope: 6 is a top prime gap and 42 is not (counts "
          f"{g[30]} vs {g[42]}); the two roles of 6 are unrelated")


def self_test() -> None:
    test_lemma1_parity_filter()
    test_lemma1_preimages_are_genuine()
    test_lemma2_closed_form_and_valuation()
    test_lemma2_consecutive_gap()
    test_theorem_6_divides_gap()
    test_no_consecutive_gap_is_divisible_by_6()
    test_the_false_claim_is_false()
    test_scope_no_prime_gap_transfer()
    print("\nAll self-tests passed.")
    print("THEOREM. For odd m and valid branch exponents k_1 < k_2,")
    print("    6 | (n_k2 - n_k1)   <=>   6 | (k_2 - k_1),")
    print("  because the gap is m * 2^k_1 * (2^d - 1)/3 with 3 not dividing m,")
    print("  and ord_9(2) = 6. The gap is always even, with v_2 = k_1 exactly.")
    print("  No CONSECUTIVE gap is ever divisible by 6: there d = 2 and the")
    print("  gap is exactly m * 2^k, which is never divisible by 3.")


if __name__ == "__main__":
    self_test()
