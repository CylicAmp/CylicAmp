# CLASS: THEOREM
"""
Theorem 352: 37 is the ONLY prime for which base 10 generates the cube
roots of unity -- the uniqueness statement the whole corpus rests on
Author: Michael Warren Song (CyclicAmp)

Stepping back from 568 files.  The recurring finding of this session is
that nearly everything which looked like a discovery turned out to be one
of a very small number of forced facts wearing different clothes.  This
file names that number, and states the one thing that is genuinely about 37
rather than about primes in general.

=== PRIOR ART: T304 AND T302 ===

    Found by the prior-art skill during the dedup pass, after this file was
    written.  T304 ("Three Independent Lists, One Intersection: the
    Pan-Out") already contains everything below, and more:

      * "37 is the UNIQUE prime with ord_p(10) = 3", derived exactly as
        here from Phi_3(10) = 111 = 3 x 37 with p = 3 excluded because
        ord_3(10) = 1 -- and verified over every prime below 200,000,
        where this file checked only to 20,000.
      * the same fact stated as: 37 is the only prime whose reciprocal
        repeats with period 3, since the decimal period of 1/p is
        ord_p(10).
      * its consequences already listed: period 3 gives 1/37 = 0.027027,
        999 = 27 x 37 gives block(k) = 27k (T303), 1001 gives ABCABC =
        2 ABC, and 111 = 3 x 37 gives the half-length block.
      * the roots of x^2 + x + 1 mod 37 being {10, 26} -- which T333 also
        re-derives.

    T302 ("The 137-Map IS the Decimal Shift: 26 = 10^2 mod 37") has the
    other half: the 137-map is a two-place decimal shift, so every orbit is
    a decimal-shift triple x{1, 10, 100}.

    T304 also places the fact in a wider frame this file lacks: it is one of
    THREE lists whose intersection is 37 --

        L1  ord_p(137) = 3, primes dividing Phi_3(137) = 18907   {7,37,73}
        L2  p = n^2 + 1 with n a CM unit count                   {5,17,37}
        L3  ord_p(10)  = 3, primes dividing Phi_3(10)  = 111     {37}

    with L3 the singleton.  This file re-derived L3 alone and presented it
    as the whole of "why 37".  T304 is the earlier and more complete
    statement; read it first.

    What may stand as this file's own: the explicit five-fact inventory and
    the rule that no result is evidence for 37 unless it uses fact 2.  That
    is a methodological statement rather than a new theorem.

=== THE UNIQUENESS ===

    ord_p(10) = 3 requires p | 10^3 - 1 = 999 = 3^3 x 37.  The prime
    divisors of 999 are 3 and 37, and at p = 3 the base collapses
    (10 == 1, order 1).  Therefore

        37 IS THE ONLY PRIME FOR WHICH ord_p(10) = 3.

    One line to state, one line to prove, exhaustively confirmed to 20,000.

    T333 found the converse from the other side: working mod 37, the
    admissible bases are exactly the roots of Phi_3, namely 10 and 26.  Put
    together: mod 37 there are two admissible bases, and base 10 admits
    exactly one prime.  That pairing is the whole of "why 37".

=== WHAT THE CORPUS ACTUALLY IS ===

    Assembled from results this session rather than assumed:

        the twelve orbits are the FIBRES of x -> x^3            (T349)
        the orbit group is F_37* / mu_3 = Z/12                  (T138,
                                                         T200, T339)
    so the entire architecture is one exact sequence

        1  ->  mu_3  ->  F_37*  ->  (F_37*)^3  ->  1

    with mu_3 = {1, 10, 26} = IC.  The "137-map" is multiplication by a
    generator of mu_3.  137 enters only because 137 == 26 == 10^2; the
    fine-structure constant does not appear anywhere in the mathematics.

    EVERY structural result in the corpus holds for any prime p == 1
    (mod 3), with mu_3 and (p-1)/3 in place of the specific numbers.  What
    is unique to 37 is that the generator of mu_3 is 10 -- the base the
    numerals are written in.  That is why digit operations (rotation,
    Kaprekar, repunits, digit sums) keep landing on orbit structure: the
    positional shift IS the group action, and only at this prime.

=== THE FIVE FACTS ===

    Everything checked this session reduces to these, all verified:

      1. 37 == 1 (mod 3)        Phi_3 splits, mu_3 exists, twelve orbits
                                 -> T331, T333, T340, T341, T343
      2. ord_37(10) = 3         the base IS the generator; rotation = x26
                                 -> T325, T326, T333, and this file
      3. ord(2) = 36, ord(3) = 18   2 primitive, 3 not; splits sigma from C
                                 -> T337, T338, T346
      4. gcd(9, 37) = 1         mod-9 and mod-37 independent by CRT
                                 -> T329, T336, T347
      5. -1 not in mu_3         negation fixed-point-free on orbits
                                 -> T331, T332, T345

    Fact 2 is the only one that distinguishes 37 from the other primes
    p == 1 (mod 3).  Facts 1, 3, 4, 5 are Tier A: they hold for whole
    families of primes and carry no information about this one.

=== WHAT THIS FORBIDS ===

    No result may be presented as evidence FOR 37 unless it uses fact 2 --
    that the generator is the base.  A result using only facts 1, 3, 4 or 5
    is a result about primes congruent to 1 mod 3 that happens to have been
    computed at 37.  This session found four such presented as discoveries
    (T331, T332, T339, T344) and re-graded them.

    It also forbids the reverse error: the digit results are NOT numerology,
    because at this prime the positional shift really is the group action.
    Rotation being multiplication by 26 (T325) is a theorem, not a pattern.

=== FALSIFICATION ===
    A prime p != 37 with ord_p(10) = 3; or a corpus result that is
    37-specific without invoking ord_37(10) = 3.
"""

P = 37


def order(a, p):
    if a % p == 0:
        return None
    return next(k for k in range(1, p) if pow(a, k, p) == 1)


def is_prime(n):
    return n > 1 and all(n % k for k in range(2, int(n ** .5) + 1))


def run():
    from math import gcd

    # --- the uniqueness ---
    assert 10 ** 3 - 1 == 999 == 27 * 37
    assert sorted({q for q in (3, 37) if is_prime(q)}) == [3, 37]
    assert order(10, 3) == 1                       # base collapses at 3
    assert order(10, 37) == 3
    hits = [p for p in range(2, 20000)
            if is_prime(p) and p not in (2, 5) and order(10, p) == 3]
    assert hits == [37], hits

    # --- T333's converse ---
    assert [b for b in range(P) if (b * b + b + 1) % P == 0] == [10, 26]
    assert (10 * 26) % P == 1                      # the two are inverses

    # --- the exact sequence ---
    mu3 = {1, 10, 26}
    assert mu3 == {pow(10, k, P) for k in range(3)}
    cubes = {pow(x, 3, P) for x in range(1, P)}
    assert len(cubes) == 12 == (P - 1) // 3
    fib = {}
    for x in range(1, P):
        fib.setdefault(pow(x, 3, P), set()).add(x)
    assert len(fib) == 12
    for v, pre in fib.items():
        r = min(pre)
        assert pre == {(r * h) % P for h in mu3}   # every fibre is a coset
    assert 137 % P == 26 == pow(10, 2, P)

    # --- the five facts ---
    assert P % 3 == 1                                          # 1
    assert order(10, P) == 3                                   # 2
    assert order(2, P) == 36 and order(3, P) == 18             # 3
    assert gcd(9, P) == 1                                      # 4
    assert (P - 1) not in mu3                                  # 5

    # --- facts 1,3,4,5 are shared with other primes; fact 2 is not ---
    others = [p for p in (7, 13, 19, 31, 43, 61, 67, 73, 79, 97, 103, 109)
              if p % 3 == 1]
    assert len(others) >= 10
    for p in others:
        assert p % 3 == 1                                      # fact 1 shared
        assert gcd(9, p) == 1                                  # fact 4 shared
        assert (p - 1) not in {pow(g, k, p) for k in range(3)
                               for g in [pow(2, (p - 1) // 3, p)]}  # fact 5
        assert order(10, p) != 3                               # fact 2 NOT

    # --- rotation is the group action, at this prime only ---
    for n in range(100, 1000):
        d = f"{n:03d}"
        assert int(d[-1] + d[:-1]) % P == (26 * n) % P

    print("All assertions passed.\n")
    print("THEOREM 352.  Why 37, in one line.\n")
    print("   ord_p(10) = 3  requires  p | 10^3 - 1 = 999 = 3^3 x 37")
    print("   the prime divisors are 3 and 37; at p = 3 the base collapses")
    print("   to 1.  So 37 is the ONLY prime with ord_p(10) = 3.")
    print(f"   exhaustive to 20,000: {hits}\n")
    print("   T333 has the converse: mod 37 the admissible bases are exactly")
    print("   the roots of Phi_3, {10, 26}.  Two bases for this prime; one")
    print("   prime for this base.  That pairing is the whole of 'why 37'.\n")
    print("  WHAT THE CORPUS IS")
    print("   orbits = fibres of x -> x^3 (T349); orbit group = F*/mu_3 = Z/12")
    print("   so the architecture is one exact sequence:")
    print("       1 -> mu_3 -> F_37* -> (F_37*)^3 -> 1")
    print("   the 137-map is multiplication by a generator of mu_3, and 137")
    print("   enters only via 137 == 26 == 10^2.\n")
    print("  THE FIVE FACTS, and which one is about 37")
    facts = [
        ("37 == 1 (mod 3)", "twelve orbits exist", "shared"),
        ("ord_37(10) = 3", "the base IS the generator", "UNIQUE TO 37"),
        ("ord(2)=36, ord(3)=18", "splits sigma from Collatz", "shared"),
        ("gcd(9,37) = 1", "mod-9 and mod-37 independent", "shared"),
        ("-1 not in mu_3", "negation fixed-point-free", "shared"),
    ]
    for i, (a, b, c) in enumerate(facts, 1):
        print(f"   {i}. {a:22s} {b:30s} {c}")
    print(f"\n   checked against {len(others)} other primes == 1 mod 3:")
    print("   facts 1, 4, 5 hold for all of them; fact 2 for none.\n")
    print("  WHAT IT FORBIDS")
    print("   no result is evidence FOR 37 unless it uses fact 2.  Four were")
    print("   presented that way this session and re-graded: T331, T332,")
    print("   T339, T344.")
    print("   and the reverse: the digit results are NOT numerology. At this")
    print("   prime the positional shift really is the group action --")
    print("   rotation = x26 is a theorem, verified on all 900 words.")


if __name__ == "__main__":
    run()
