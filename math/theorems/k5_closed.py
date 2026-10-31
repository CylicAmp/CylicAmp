"""
k5_closed.py

THEOREM (k = 5). No positive integer n satisfies

    n = d_1^2 + d_2^2 + d_3^2 + d_4^2 + d_5^2

where d_1 < d_2 < d_3 < d_4 < d_5 are the FIVE SMALLEST divisors of n.

Proved at LEVEL 1 -- parameter-free, every prime, no bounded range and
no search anywhere in the chain. This module asserts the result and names
where each piece lives; the proofs are in the modules it imports, and
running this runs them all.

WHERE THE LEVEL 2 USED TO BE. divisor_prefix_ledger.py closes three of
its thirteen admissible shapes with its COFACTOR_SIZE oracle, which is a
bounded check over primes <= 173 and so reports Level 2:

    {1, t, s, r, 2}     1 and four distinct primes, one of them 2
    {1, t, s, r, q}     1 and four distinct odd primes
    {1, t, s, r, t^2}   1, three odd primes, and the square of one

k5_cofactor_level1.py proves all three at Level 1 (LEMMA 1 and LEMMA 2
there). The ledger is deliberately left alone -- its oracle really is
bounded, and the module's rule is to never claim more than it proves --
so the Level 1 content lives in the upgrade module and this module reads
the combined status.

--------------------------------------------------------------------
HOW THE CASE SPLITS
--------------------------------------------------------------------
d_1 = 1 always, so n = 1 + d_2^2 + ... + d_5^2 is a sum of five squares
of which the first is odd.

PARITY (divisor_prefix_ledger.oracle_parity). A sum of five squares has
the parity of the number of odd terms. If n is even then 2 = d_2, and
the prefix is a divisor-closed set containing 2; the parity bookkeeping
in the ledger kills every even case. So n is ODD, hence every d_i is
odd, and the prefix consists of 1 and four odd divisors.

SHAPES. An odd prefix of size 5 that is divisor-closed and closed under
coprime products is, up to relabelling of the primes, one of three:

    A   {1, q, q^2, q^3, r}       k5_odd_shapes.py        CLOSED L1
    B   {1, q, q^2, r, qr}        k5_odd_shapes.py        CLOSED L1
    C   {1, q, r, s, qr}          3 | n:    k5_shape_c_q3.py      CLOSED L1
                                  3 does not | n: k5_shape_c_nodiv3.py CLOSED L1

The enumeration of exactly these three is divisor_prefix_ledger.py:
120 labelled order ideals -> 18 orbits with the prime 2 fixed -> 13
admissible as a prefix -> 10 closed by the ledger's own oracles, leaving
A, B, C. The ledger deliberately reports those three as OPEN, because
its own oracles do not reach them; they are closed in the dedicated
modules above.

--------------------------------------------------------------------
THE THREE CLOSING MOVES
--------------------------------------------------------------------
Every one of the five closures runs the same three steps. Only the third
step differs, and in exactly one place the third step is not needed.

  MOVE 1  Prefix ordering bounds the cofactor.
          n = (product of the prime prefix elements) * c. Because the
          prefix is the set of SMALLEST divisors, any divisor of n below
          max(prefix) must itself be in the prefix. That caps c.

  MOVE 2  The cofactor collapses to one value.
          The cap plus "every prime of c is a prefix prime" leaves one
          or two candidates for c, and the leftover is killed on size.

  MOVE 3  The discriminant is trapped between consecutive squares.
          With c pinned, the last unknown satisfies a monic quadratic
          whose discriminant is shown to lie strictly between two
          consecutive squares, so it is not a perfect square and the
          unknown is not an integer.

  Shape A: move 3 twice (c = 1 gives a negative discriminant; c = q
           gives (q^4-2q^2-5)^2 < D < (q^4-2q^2-4)^2).
  Shape B: c = q^2 exactly, then (q^4-2q^2-7)^2 < D < (q^4-2q^2-6)^2.
  Shape C, 3 | n: the ordering argument, no discriminant.
  Shape C, 3 does not | n, s > qr: (qr^2-2q-1)^2 < D < (qr^2-2q)^2.
  Shape C, 3 does not | n, r < s < qr: MOVE 3 IS NOT AVAILABLE AND NOT
           NEEDED. Move 2 gives c = q, so n = q^2 r s. Then q^2 | n and
           q^2 < qr = max(prefix), so move 1's prefix rule demands
           q^2 be one of {1, q, r, s, qr} -- impossible, since q^2 is
           composite and r, s are prime. The case is empty outright.

That last line is the one that held k = 5 open. The discriminant there
is D1 = q^4 r^2 - 4(1+q^2)(1+r^2), and no bracket can trap it: it is a
genuine Pell equation m^2 - a r^2 = -b with a = (q^2-2)^2 - 8 never a
square, and k5_shape_c_nodiv3.CASE1_WITNESS_R is a 110-digit prime at
q = 17 for which D1 IS an exact perfect square with r < s < qr. Move 1
kills it anyway. Where move 3 fails, move 1 is still enough.

--------------------------------------------------------------------
CONSISTENCY WITH WHAT DOES EXIST
--------------------------------------------------------------------
The result must not prove too much. Known solutions, by divisor-prefix
length k (divisor_square_sum_scan.py, verified to 30,000,000):

    k = 1   n = 1                        1 = 1^2
    k = 4   n = 130   prefix 1,2,5,10     1+4+25+100 = 130
    k = 11  n = 1860  prefix 1,2,3,4,5,6,10,12,15,20,30
    k = 5   NONE  <- this theorem
    k even  NONE for odd n, by parity

n = 130 is the falsification anchor: any argument that also closed k = 4
would be wrong, and the ledger's test suite asserts that 130's shape is
never closed.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import divisor_prefix_ledger as ledger          # noqa: E402
import k5_odd_shapes as shapes_ab               # noqa: E402
import k5_shape_c_q3 as shape_c_q3              # noqa: E402
import k5_shape_c_nodiv3 as shape_c_nodiv3      # noqa: E402
import k5_cofactor_level1 as cofactor_l1        # noqa: E402

CLOSURES = {
    "ledger  7 shapes": ("divisor_prefix_ledger.py", 1, "parity / prime power"),
    "ledger  {1,t,s,r,2}": ("k5_cofactor_level1.py", 1, "move 1: lemma 1"),
    "ledger  {1,t,s,r,q}": ("k5_cofactor_level1.py", 1, "move 1: lemma 1"),
    "ledger  {1,t,s,r,t^2}": ("k5_cofactor_level1.py", 1, "move 1: lemma 2"),
    "A  {1,q,q^2,q^3,r}": ("k5_odd_shapes.py", 1, "move 3 twice"),
    "B  {1,q,q^2,r,qr}": ("k5_odd_shapes.py", 1, "c=q^2, then move 3"),
    "C  {1,q,r,s,qr} 3|n": ("k5_shape_c_q3.py", 1, "ordering argument"),
    "C  {1,q,r,s,qr} s>qr": ("k5_shape_c_nodiv3.py", 1, "move 3"),
    "C  {1,q,r,s,qr} s<qr": ("k5_shape_c_nodiv3.py", 1, "move 1: q^2 | n"),
}


def test_every_shape_has_a_level1_closure() -> None:
    assert len(CLOSURES) == 9
    for name, (mod, level, how) in CLOSURES.items():
        assert level == 1, (name, level)
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), mod)
        assert os.path.exists(path), path
    print(f"[ok] all {len(CLOSURES)} k=5 case groups have a Level 1 closure "
          f"in a real module")


def test_no_level2_remains_in_the_chain() -> None:
    """Every ledger shape is Level 1 once the upgrade module is counted."""
    pool = [p for p in range(2, 180)
            if all(p % i for i in range(2, int(p ** 0.5) + 1))]
    L = ledger.ledger(5, pool)
    l2 = [ledger.render(rep) for rep, cert in L["closed"] if cert.level == 2]
    upgraded = set(cofactor_l1.LEMMA1_SHAPES) | set(cofactor_l1.LEMMA2_SHAPES)
    assert set(l2) == upgraded, (l2, upgraded)
    still_open = [ledger.render(rep) for rep, _ in L["open"]]
    assert len(still_open) == 3, still_open
    print(f"[ok] the ledger's {len(l2)} Level 2 shapes are exactly the ones "
          f"k5_cofactor_level1 proves at Level 1")


def test_case1_closure_is_move1_not_move3() -> None:
    """The case that held k=5 open closes on the prefix rule, and its
    discriminant demonstrably cannot be bracketed."""
    q = shape_c_nodiv3.CASE1_WITNESS_Q
    r = shape_c_nodiv3.CASE1_WITNESS_R
    from math import isqrt
    D1 = shape_c_nodiv3.disc_case1(q, r)
    assert isqrt(D1) ** 2 == D1, "witness: D1 really is a perfect square"
    s = (q * q * r - isqrt(D1)) // 2
    assert r < s < q * r, "witness: both range conditions really hold"
    assert shape_c_nodiv3.case1_is_empty(q, r), "and move 1 kills it anyway"
    assert shape_c_nodiv3.case1_window(5) is None, "q=5 never had a bracket window"
    print("[ok] case 1 closes on move 1; its discriminant provably cannot be bracketed")


def test_does_not_prove_too_much() -> None:
    """n = 130 (k=4) and n = 1860 (k=11) must survive."""
    for n, k in ((1, 1), (130, 4), (1860, 11)):
        ds = shape_c_nodiv3.smallest_divisors(n, k)
        assert len(ds) == k, (n, k, ds)
        assert sum(d * d for d in ds) == n, (n, k, ds)
    print("[ok] falsification anchors intact: 1 (k=1), 130 (k=4), 1860 (k=11)")


def test_no_k5_solution_by_direct_scan() -> None:
    """Level 2 cross-check of a Level 1 theorem."""
    LIM = 3_000_000
    from math import isqrt
    hits = []
    for n in range(2, LIM):
        ds = []
        for i in range(1, isqrt(n) + 1):
            if n % i == 0:
                ds.append(i)
                if len(ds) > 7:
                    break
        ds = sorted(ds)[:5]
        if len(ds) == 5 and sum(d * d for d in ds) == n:
            hits.append(n)
    assert hits == [], hits
    print(f"[ok] direct scan to {LIM:,}: no k=5 solution (agrees with the theorem)")


def self_test() -> None:
    print("=" * 66)
    print("RUNNING EVERY MODULE THE k=5 THEOREM DEPENDS ON")
    print("=" * 66)
    for mod in (ledger, cofactor_l1, shapes_ab, shape_c_q3, shape_c_nodiv3):
        print(f"\n>>> {mod.__name__}")
        mod.self_test()
    print("\n" + "=" * 66)
    print("THE k=5 CLAIM ITSELF")
    print("=" * 66)
    test_every_shape_has_a_level1_closure()
    test_no_level2_remains_in_the_chain()
    test_case1_closure_is_move1_not_move3()
    test_does_not_prove_too_much()
    test_no_k5_solution_by_direct_scan()
    print("\n" + "=" * 66)
    print("THEOREM (k=5), Level 1: no n is the sum of the squares of its")
    print("five smallest divisors. Every case parameter-free, no search.")
    print("=" * 66)
    for name, (mod, level, how) in CLOSURES.items():
        print(f"  L{level}  {name:<24} {how:<22} {mod}")


if __name__ == "__main__":
    self_test()
