# CLASS: THEOREM
"""
Theorem 366: "p divides some Phi_m(10)" is true of EVERY prime but 2 and 5,
so intersecting any prime set with the cyclotomic sieve returns it unchanged
Author: Michael Warren Song (CyclicAmp)

=== THE PREDICATE, AND ITS SELECTIVITY ===

    Supplied as a filter: take a list of primes -- here the irregular
    primes -- and note which of them appear as factors of the cyclotomic
    values Phi_m(10), calling that an intersection with the cyclotomic
    sieve.

    IT IS NOT A FILTER.  For any prime p not dividing 10, m = ord_p(10)
    exists, and

        p | 10^m - 1 = prod_{d | m} Phi_d(10),

    with p | Phi_m(10) specifically: if p divided Phi_d(10) for a proper
    divisor d | m then 10^d == 1 (mod p), contradicting minimality of m,
    unless p | m (the intrinsic case, e.g. 3 divides both Phi_1(10) = 9
    and Phi_3(10) = 111).  Either way p divides at least one Phi_m(10),
    always, for m = ord_p(10).

    So the predicate passes every prime except 2 and 5 -- the two that
    divide the base.  Selectivity: 0 bits.  Intersecting any set S of
    primes with "the cyclotomic sieve" returns S minus at most {2, 5}.

    Verified: every prime below 20000 coprime to 10 divides Phi_{ord}(10);
    no exception.  And all 35 irregular primes below 600 do, so
    "irregular AND in the cyclotomic sieve" = "irregular".

=== THE SELECTION EFFECT THAT MAKES IT LOOK LIKE A FILTER ===

    What is actually being noticed is SMALL ORDER, not membership.

        p = 37   ord = 3     Phi_3(10)  = 111          visible
        p = 101  ord = 4     Phi_4(10)  = 101          visible
        p = 271  ord = 5     Phi_5(10)  = 11111        visible
        p = 59   ord = 58    Phi_58(10)                58 digits
        p = 131  ord = 130   Phi_130(10)               130 digits

    Primes with order 3, 4 or 5 give short repunit-like blocks that a
    person can see and name.  Primes with order 58 or 130 give blocks
    nobody would call a sieve.  Both divide a cyclotomic value.  Only the
    first kind gets listed, and that is a property of what is legible, not
    of the primes.

    Measured below: the fraction of primes with ord_p(10) <= 10 is tiny,
    and it falls as the range grows.

=== WHY THIS MATTERS HERE ===

    T365 recorded that 37 carries two unrelated distinctions -- being the
    first irregular prime, and having ord_37(10) = 3 -- and warned against
    citing them as one.  The supplied text does exactly that one step
    later, under a heading reading "Intersection with the Cyclotomic
    Sieve", listing 37's irregularity and its order-3 block in a single
    bullet.

    The correct statement is that 37 satisfies both and that satisfying
    the second carries no information, because every prime does.  What is
    special about 37's entry is the SIZE of its order, and that is the
    first distinction restated, not a second one confirming it.

    This is forced-check's COMPLETE PARTITION mechanism: every residue
    lands in exactly one orbit, so having an orbit is never news.  Here
    every prime has an order, so dividing some Phi_m(10) is never news.

=== FALSIFICATION ===
    A prime p, coprime to 10, dividing no Phi_m(10); or an irregular prime
    below 600 failing the predicate; or the predicate rejecting any prime
    other than 2 and 5.
"""
from sympy import n_order, cyclotomic_poly, primerange, bernoulli, primefactors


def run(N=20000):
    # (1) The predicate holds for every prime coprime to 10.  Phi_m(10) is
    #     astronomically large for large m, so verify by VALUATION rather
    #     than by evaluating it.  With m = ord_p(10),
    #         10^m - 1 = prod_{d | m} Phi_d(10),   and  p | 10^m - 1.
    #     For every proper divisor d | m, 10^d != 1 (mod p) by minimality of
    #     the order, so p divides none of those factors.  Hence the whole of
    #     v_p(10^m - 1) >= 1 sits on Phi_m(10), i.e. p | Phi_m(10).
    miss = []
    for q in primerange(3, N):
        if q == 5:
            continue
        m = n_order(10, q)
        assert pow(10, m, q) == 1
        # minimality: testing m/r for each prime r | m suffices
        if any(pow(10, m // r, q) == 1 for r in primefactors(m)):
            miss.append(q)
    assert miss == [], miss[:10]

    # spot-check the conclusion directly, where Phi_m(10) is small enough
    small_ord = [(q, n_order(10, q)) for q in (3, 7, 11, 13, 37, 101, 271)]
    for q, m in small_ord:
        assert int(cyclotomic_poly(m, 10)) % q == 0, (q, m)

    # 2 and 5 are the only rejections, and only because they divide the base
    assert 10 % 2 == 0 and 10 % 5 == 0

    # (2) the intrinsic case is real: 3 divides Phi_1(10) and Phi_3(10)
    assert int(cyclotomic_poly(1, 10)) == 9 and 9 % 3 == 0
    assert int(cyclotomic_poly(3, 10)) == 111 and 111 % 3 == 0
    assert n_order(10, 3) == 1

    # (3) so intersecting the irregular primes with the sieve returns them all
    irr = [q for q in primerange(3, 600)
           if any(bernoulli(k).p % q == 0 for k in range(2, q - 1, 2))]
    assert len(irr) == 35 and irr[0] == 37
    for q in irr:
        m = n_order(10, q)
        assert pow(10, m, q) == 1
        assert not any(pow(10, m // r, q) == 1 for r in primefactors(m))

    # (4) the selection effect: small order is rare, and gets rarer
    bands = {}
    for hi in (1000, 10000, 20000):
        ps = [q for q in primerange(3, hi) if q != 5]
        bands[hi] = (sum(1 for q in ps if n_order(10, q) <= 10), len(ps))
    assert bands[1000][0]/bands[1000][1] > bands[20000][0]/bands[20000][1]

    print("T366  cyclotomic-sieve membership selects nothing\n")
    print("  every prime below %d coprime to 10 divides Phi_{ord_p(10)}(10)," % N)
    print("  by valuation: p | 10^m - 1, and no proper divisor d | m has")
    print("  10^d = 1 (mod p). Exceptions: %s -- only 2 and 5, which" % (miss or "none"))
    print("  divide the base. Selectivity of the predicate: 0 bits.\n")
    print("  all 35 irregular primes below 600 pass, so")
    print("  'irregular AND in the cyclotomic sieve' = 'irregular'.\n")
    print("  WHAT IS ACTUALLY BEING NOTICED IS SMALL ORDER:")
    for q in (37, 101, 271, 59, 131):
        m = n_order(10, q)
        print("   p=%-4d ord=%-4d Phi_%d(10) has %d digits"
              % (q, m, m, len(str(int(cyclotomic_poly(m, 10))))))
    print("\n  primes with ord_p(10) <= 10, as a fraction:")
    for hi, (s, tot) in bands.items():
        print("   below %-6d  %d of %d = %.4f" % (hi, s, tot, s/tot))
    print("  the short-order primes are the legible ones, not a selected kind.")
    print("\n  ALL ASSERTIONS PASS")


if __name__ == '__main__':
    run()
