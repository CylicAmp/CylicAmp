"""
k6_closed.py

THEOREM (k = 6). No positive integer n satisfies

    n = d_1^2 + d_2^2 + d_3^2 + d_4^2 + d_5^2 + d_6^2

where d_1 < ... < d_6 are the SIX SMALLEST divisors of n.

Proved at Level 1 -- parameter-free, every prime, no bounded range and no
search. The proof is short, and shorter than k=5: it never reaches a
discriminant. It runs on the same two engines as the rest of the ledger,

  (P)  PREFIX RULE. If e | n and e < max(prefix), then e is among the six
       smallest divisors, so e is IN the prefix. True for composite e.

  (L)  LCM RULE. The prefix elements all divide n, so lcm(prefix) | n, and
       since n > 0 this forces n >= lcm(prefix).

plus one modular step at 8, which is as far as odd^2 = 1 (mod 8) reaches.

--------------------------------------------------------------------
STEP 1   n IS EVEN
--------------------------------------------------------------------
If n were odd then no d_i is even (an even divisor would give 2 | n), so
all six are odd, and a sum of six odd squares is even -- contradiction.
So n is even and d_2 = 2.

This is the parity lemma: a sum of k odd squares has the parity of k, so
EVEN k admits no odd n. k=6 is the first even case where the rest of the
ledger does not already finish the job.

--------------------------------------------------------------------
STEP 2   THE MOD 8 COUNT
--------------------------------------------------------------------
Squares mod 8, by residue class of d:

    d odd         d^2 = 1  (mod 8)
    d = 2 (mod 4) d^2 = 4  (mod 8)
    d = 0 (mod 4) d^2 = 0  (mod 8)

Writing A, B, C for the number of prefix elements in each class,

    A + B + C = 6   and   sum d_i^2 = A + 4B   (mod 8),

so for a SOLUTION (where n = sum d_i^2) also n = A + 4B (mod 8).

A >= 1 always, since d_1 = 1 is odd.

--------------------------------------------------------------------
STEP 3   v_2(n) = 1 IS IMPOSSIBLE
--------------------------------------------------------------------
If v_2(n) = 1 then no divisor is divisible by 4, so C = 0 and A + B = 6.
Then n = A + 4(6-A) = 24 - 3A = 5A (mod 8), while n = 2 (mod 4) forces
n in {2, 6} (mod 8). Solving 5A = 2 or 6 (mod 8) over 1 <= A <= 6 leaves
A = 2 or A = 6. A = 6 means no even divisor at all, contradicting n even.
So A = 2 and B = 4.

But B = 4 is impossible. Each element counted by B is 2d with d odd, and
then d | n with d < 2d <= max(prefix), so (P) puts d in the prefix. The
odd prefix elements number A = 2, so there are at most 2 such d, giving
B <= 2. Contradiction.

--------------------------------------------------------------------
STEP 4   SO 4 | n, AND THE PROFILE IS FORCED
--------------------------------------------------------------------
v_2(n) >= 2, so 4 | n. If 4 were not in the prefix then 4 > max(prefix),
so all six prefix elements would be divisors below 4, i.e. drawn from
{1, 2, 3} -- only three values for six distinct elements. So 4 IS in the
prefix, giving C >= 1, and B >= 1 because 2 is in the prefix.

Now 4 | n gives n = 0 (mod 4), and n = A + 4B (mod 8) gives A = 0 (mod 4).
With 1 <= A <= 6 this forces

    A = 4,    hence B + C = 2,    hence B = C = 1.

So the prefix is exactly

    {1, 2, 4, p, q, w},     p < q < w,  all odd and > 1,

with 2 the ONLY element that is 2 (mod 4) and 4 the ONLY element that is
0 (mod 4).

--------------------------------------------------------------------
STEP 5   w < 2p, AND p, q, w ARE PRIME
--------------------------------------------------------------------
2p divides n and 2p = 2 (mod 4). Since B = 1 and 2 is already that one
element, 2p is not in the prefix, so by (P)

    2p > max(prefix) = w.

Next, p is the least odd prime factor of n: an odd prime f | n with f < p
would be an odd divisor below w, so (P) would put f in the prefix, but the
odd elements are exactly 1, p, q, w and f < p. Hence every odd divisor of
n has all prime factors >= p, so a COMPOSITE odd divisor is at least
p^2 > 2p > w and cannot be in the prefix. So p, q, w are all prime.

--------------------------------------------------------------------
STEP 6   THE LCM RULE FINISHES IT
--------------------------------------------------------------------
p, q, w are distinct odd primes, so lcm{1,2,4,p,q,w} = 4pqw, and (L) gives
n >= 4pqw. But

    n = 1 + 4 + 16 + p^2 + q^2 + w^2 = 21 + p^2 + q^2 + w^2
      < 21 + 3w^2  < 21 + 12p^2        (since w < 2p)
    4pqw > 4p * p * p = 4p^3           (since w > q > p)

and 4p^3 > 21 + 12p^2 for p >= 5 (at p = 5: 500 > 321). So n < 4pqw <= n,
a contradiction, for every p >= 5.

--------------------------------------------------------------------
STEP 7   p = 3 IS VACUOUS
--------------------------------------------------------------------
Step 6 needs p >= 5, and p = 3 is not covered (108 < 129). It needs no
bound: p = 3 requires two odd primes q < w with 3 < q < w < 6, and there
is only one odd number in that range. No configuration exists.

(p = 5 is likewise vacuous -- the only prime strictly between 5 and 10 is
7, and two are needed -- so steps 6 and 7 overlap rather than just meet.)

Every case is contradicted. k = 6 is closed.

--------------------------------------------------------------------
CONSISTENCY
--------------------------------------------------------------------
The argument must not prove too much. It is specific to k = 6: step 2's
count and step 4's A = 0 (mod 4) both use the number six. Known solutions
survive, as they must:

    k = 1   n = 1
    k = 4   n = 130    1+4+25+100,     prefix 1,2,5,10
    k = 11  n = 1860   prefix 1,2,3,4,5,6,10,12,15,20,30

Note n = 130 is the sharp test of step 4's style of reasoning: it is even,
v_2 = 1, and it survives because at k = 4 the mod 8 count reads
n = A + 4B with A + B + C = 4, which admits A = 2, B = 2 -- and B = 2 is
exactly what the prefix rule allows, since the odd elements are 1 and 5
and the even ones are 2 = 2*1 and 10 = 2*5. At k = 6 the same bookkeeping
demands B = 4 from only 2 available odd divisors, which is what breaks.
"""

from math import isqrt, gcd
from typing import List, Tuple

MOD8_BY_CLASS = {"odd": 1, "2 mod 4": 4, "0 mod 4": 0}


def primes_upto(n: int) -> List[int]:
    sieve = bytearray([1]) * (n + 1)
    sieve[0:2] = b"\x00\x00"
    for i in range(2, isqrt(n) + 1):
        if sieve[i]:
            sieve[i * i::i] = bytearray(len(sieve[i * i::i]))
    return [i for i in range(n + 1) if sieve[i]]


def lcm_of(vals) -> int:
    out = 1
    for v in vals:
        out = out * v // gcd(out, v)
    return out


def smallest_divisors(n: int, k: int) -> List[int]:
    out = []
    for i in range(1, isqrt(n) + 1):
        if n % i == 0:
            out.append(i)
            out.append(n // i)
    return sorted(set(out))[:k]


def class_of(d: int) -> str:
    if d % 2:
        return "odd"
    return "2 mod 4" if d % 4 == 2 else "0 mod 4"


def profile(prefix) -> Tuple[int, int, int]:
    """(A, B, C) = counts of odd, 2 mod 4, 0 mod 4."""
    A = sum(1 for d in prefix if class_of(d) == "odd")
    B = sum(1 for d in prefix if class_of(d) == "2 mod 4")
    C = sum(1 for d in prefix if class_of(d) == "0 mod 4")
    return A, B, C


def step6_bound_holds(p: int) -> bool:
    return 4 * p ** 3 > 21 + 12 * p * p


def step7_configurations(p: int) -> List[Tuple[int, int]]:
    """odd primes q < w with p < q < w < 2p."""
    ps = [x for x in primes_upto(2 * p) if p < x < 2 * p]
    return [(ps[i], ps[j]) for i in range(len(ps)) for j in range(i + 1, len(ps))]


# =====================================================================
# SELF-TESTS
# =====================================================================

def test_step1_parity() -> None:
    """A sum of six odd squares is even, so no odd n has k=6."""
    for ds in [(1, 3, 5, 7, 9, 11), (1, 5, 7, 11, 13, 17), (1, 3, 9, 27, 81, 243)]:
        assert sum(d * d for d in ds) % 2 == 0, ds
    # and directly: no odd n up to a range realizes k=6
    bad = []
    for n in range(1, 400000, 2):
        ds = smallest_divisors(n, 6)
        if len(ds) == 6 and sum(d * d for d in ds) == n:
            bad.append(n)
    assert bad == [], bad
    print("[ok] step 1: six odd squares sum to an even number; no odd n has k=6")


def test_step2_mod8_classes() -> None:
    """The three square classes mod 8 are exactly 1, 4, 0."""
    for name, expect in MOD8_BY_CLASS.items():
        vals = {(d * d) % 8 for d in range(1, 4000) if class_of(d) == name}
        assert vals == {expect}, (name, vals)
    # and the count identity n = A + 4B (mod 8) on real prefixes
    checked = 0
    for n in range(2, 200000):
        ds = smallest_divisors(n, 6)
        if len(ds) < 6:
            continue
        A, B, C = profile(ds)
        assert A + B + C == 6
        assert sum(d * d for d in ds) % 8 == (A + 4 * B) % 8, (n, ds)
        checked += 1
    print(f"[ok] step 2: n = A + 4B (mod 8) on all {checked} six-divisor prefixes")


def test_step3_v2_equals_one_impossible() -> None:
    """A = 2, B = 4 is the only arithmetic option, and the prefix rule kills it."""
    sols = [A for A in range(1, 7) if (5 * A) % 8 in (2, 6)]
    assert sols == [2, 6], sols
    # A=6 means no even divisor, contradicting n even; so A=2, B=4.
    # B counts elements 2d with d odd; each such d is forced into the prefix.
    bad = []
    for n in range(2, 600000, 2):
        if n % 4 == 0:
            continue
        ds = smallest_divisors(n, 6)
        if len(ds) < 6:
            continue
        A, B, C = profile(ds)
        assert C == 0, (n, ds)
        halves = {d // 2 for d in ds if class_of(d) == "2 mod 4"}
        odds = {d for d in ds if class_of(d) == "odd"}
        assert halves <= odds, (n, ds, halves, odds)   # the prefix rule
        assert B <= A, (n, ds, A, B)
        if A == 2 and B == 4:
            bad.append(n)
    assert bad == [], bad
    print("[ok] step 3: v_2(n)=1 forces A=2,B=4, but the prefix rule gives B<=A")


def test_step4_profile_forced() -> None:
    """IMPLICATION: if n = sum d_i^2 and 4 | n, the profile must be (4,1,1).
    This is a statement about solutions, so it is checked over the finite
    space of profiles, not over every n divisible by 4 (n = 12 has profile
    (2,2,2) and is simply not a solution)."""
    survivors = []
    for A in range(0, 7):
        for B in range(0, 7 - A):
            C = 6 - A - B
            if A < 1:
                continue            # d_1 = 1 is odd
            if B < 1 or C < 1:
                continue            # 2 and 4 are both in the prefix
            # n = sum d_i^2 = A + 4B (mod 8), and 4 | n means n = 0 (mod 4)
            if (A + 4 * B) % 4 == 0:
                survivors.append((A, B, C))
    assert survivors == [(4, 1, 1)], survivors
    print(f"[ok] step 4: over all profiles, 4 | n admits only (A,B,C) = "
          f"{survivors[0]}")


def test_step4_four_is_in_the_prefix() -> None:
    """4 | n puts 4 in the prefix: otherwise six distinct divisors would all
    have to be below 4."""
    checked = 0
    for n in range(4, 400000, 4):
        ds = smallest_divisors(n, 6)
        if len(ds) < 6:
            continue
        assert 4 in ds, (n, ds)
        checked += 1
    assert len({1, 2, 3}) < 6, "only three divisors are available below 4"
    print(f"[ok] step 4: 4 is in the prefix whenever 4 | n ({checked} cases)")


def test_step5_w_lt_2p_and_primality() -> None:
    """IMPLICATION: on a prefix with profile (4,1,1), w < 2p and p,q,w are
    prime. Checked on every n that actually realizes that profile."""
    checked = 0
    for n in range(4, 900000, 4):
        ds = smallest_divisors(n, 6)
        if len(ds) < 6:
            continue
        if profile(ds) != (4, 1, 1):
            continue
        odds = sorted(d for d in ds if class_of(d) == "odd" and d > 1)
        assert len(odds) == 3, (n, ds)
        p, q, w = odds
        assert w == max(ds), (n, ds)
        assert 2 * p > w, (n, ds)
        for x in (p, q, w):
            assert x > 2 and all(x % i for i in range(3, isqrt(x) + 1, 2)), (n, x)
        assert lcm_of(ds) == 4 * p * q * w, (n, ds)
        checked += 1
    assert checked > 50, checked
    print(f"[ok] step 5: on all {checked} realized (4,1,1) prefixes, w < 2p, "
          f"p,q,w prime, lcm = 4pqw")


def test_step6_bound() -> None:
    """4p^3 > 21 + 12p^2 for p >= 5, and fails at p = 3."""
    assert not step6_bound_holds(3)
    for p in primes_upto(20000):
        if p >= 5:
            assert step6_bound_holds(p), p
    print("[ok] step 6: 4p^3 > 21+12p^2 for every prime p >= 5 (fails at p=3)")


def test_step7_small_p_vacuous() -> None:
    """p = 3 and p = 5 admit no (q, w) at all."""
    assert step7_configurations(3) == []
    assert step7_configurations(5) == []
    assert step7_configurations(7) == [(11, 13)]
    print("[ok] step 7: p=3 and p=5 are vacuous; p=7 first admits (q,w)=(11,13)")


def test_step6_closes_every_configuration() -> None:
    """For every admissible (p,q,w) the lcm rule bites."""
    ps = primes_upto(4000)
    checked = 0
    for p in ps:
        if p < 5:
            continue
        if p > 1500:
            break
        for (q, w) in step7_configurations(p):
            n = 21 + p * p + q * q + w * w
            L = 4 * p * q * w
            assert n < L, (p, q, w, n, L)
            checked += 1
    assert checked > 5000, checked
    print(f"[ok] step 6 applied: n < 4pqw on all {checked} admissible (p,q,w)")


def test_brute_force_no_k6() -> None:
    """Level 2 cross-check of a Level 1 theorem."""
    LIM = 3_000_000
    hits = []
    for n in range(2, LIM):
        ds = []
        for i in range(1, isqrt(n) + 1):
            if n % i == 0:
                ds.append(i)
                if len(ds) > 8:
                    break
        ds = sorted(ds)[:6]
        if len(ds) == 6 and sum(d * d for d in ds) == n:
            hits.append(n)
    assert hits == [], hits
    print(f"[ok] direct scan to {LIM:,}: no k=6 solution (agrees with the theorem)")


def test_does_not_prove_too_much() -> None:
    """130 (k=4) and 1860 (k=11) survive, and 130 shows why k=6 differs."""
    for n, k in ((1, 1), (130, 4), (1860, 11)):
        ds = smallest_divisors(n, k)
        assert len(ds) == k and sum(d * d for d in ds) == n, (n, k, ds)
    ds = smallest_divisors(130, 4)
    A, B, C = profile(ds)
    assert (A, B, C) == (2, 2, 0), (ds, A, B, C)
    assert 130 % 4 == 2, "130 has v_2 = 1, the case step 3 kills at k=6"
    halves = {d // 2 for d in ds if class_of(d) == "2 mod 4"}
    odds = {d for d in ds if class_of(d) == "odd"}
    assert halves == odds, (ds, halves, odds)
    assert B <= A, "at k=4 the prefix rule permits B=2; at k=6 it demands B=4"
    print("[ok] anchors survive; 130 (A=2,B=2,v_2=1) shows exactly what k=6 breaks")


def self_test() -> None:
    test_step1_parity()
    test_step2_mod8_classes()
    test_step3_v2_equals_one_impossible()
    test_step4_profile_forced()
    test_step4_four_is_in_the_prefix()
    test_step5_w_lt_2p_and_primality()
    test_step6_bound()
    test_step7_small_p_vacuous()
    test_step6_closes_every_configuration()
    test_does_not_prove_too_much()
    test_brute_force_no_k6()
    print("\nAll self-tests passed.")
    print("THEOREM (k=6), Level 1: no n is the sum of the squares of its six")
    print("smallest divisors.")
    print("  step 1  parity          n is even")
    print("  step 3  mod 8 + prefix  v_2(n) = 1 impossible")
    print("  step 4  mod 8 + prefix  profile forced to A=4, B=C=1")
    print("  step 5  prefix rule     w < 2p, and p,q,w prime")
    print("  step 6  lcm rule        n < 4pqw for p >= 5")
    print("  step 7  counting        p = 3 (and p = 5) vacuous")


if __name__ == "__main__":
    self_test()
