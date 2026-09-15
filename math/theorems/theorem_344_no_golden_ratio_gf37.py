# CLASS: THEOREM
"""
Theorem 344: there is NO golden ratio in GF(37) -- 37 == 1 (mod 3) builds
the corpus, 37 == 2 (mod 5) forbids phi
Author: Michael Warren Song (CyclicAmp)

Prompted by an "8,5,3 Golden Circle" construction.  3, 5, 8 are consecutive
Fibonacci numbers, and 8/5, 5/3 are convergents to phi, so the natural
question is where phi sits in GF(37).  It does not sit anywhere.

=== THE PROHIBITION ===

    phi satisfies x^2 = x + 1, i.e. x^2 - x - 1 = 0, whose discriminant is
    5.  A root exists mod p only if 5 is a quadratic residue mod p, which
    happens exactly when p == +-1 (mod 5).

        37 mod 5 = 2

    so 5 is a NON-residue mod 37 and x^2 - x - 1 has NO root.  Verified by
    exhaustion: the solution set over all 37 residues is empty.

    THERE IS NO GOLDEN RATIO IN GF(37).  phi lives in GF(37^2) and nowhere
    smaller.  Any construction placing phi inside this field is not
    approximate or hard to find -- it does not exist.

=== THE CONTRAST THAT MATTERS ===

    Two congruence conditions on 37, pulling opposite ways:

        37 == 1 (mod 3)   =>  x^2 + x + 1 SPLITS, roots 10 and 26
                          =>  cube roots of unity exist
                          =>  the twelve orbits, and everything in T331,
                              T333, T340, T341, T343

        37 == 2 (mod 5)   =>  x^2 - x - 1 does NOT split
                          =>  no phi, no Fibonacci ratio limit in-field

    The corpus is built on the first.  The second forbids a whole family of
    constructions that people habitually pair with the first.  Both are one
    line of quadratic reciprocity; neither is deep; both are worth having
    written down, because the enabling one gets used constantly and the
    forbidding one keeps getting assumed away.

    Primes below 60 where phi DOES exist:  11, 19, 29, 31, 41, 59
    Primes below 60 where it does not:     2, 3, 7, 13, 17, 23, 37, 43,
                                           47, 53

=== THE PISANO PERIOD IS MAXIMAL ===

    When 5 is a residue the Fibonacci period divides p-1; when it is a
    non-residue it divides 2(p+1).  Here

        pi(37) = 76 = 2 x 38 = 2(37 + 1)

    exactly the maximum.  Fibonacci mod 37 takes the longest cycle the
    field allows, precisely BECAUSE phi is absent -- the sequence is driven
    by an element of GF(37^2) whose norm is -1, not by anything in GF(37).

=== A NON-UNIFORMITY THAT IS NOT ABOUT 37 ===

    Over one complete period the 72 nonzero Fibonacci residues distribute
    over the twelve orbits as 8, 6 or 4 -- four orbits each -- and the
    grouping is exactly by index mod 3 (T339's index, i.e. the cubic
    residue class):

        idx == 0 (mod 3)  IC, TESLA, NEG_H, C9         6 each, 24 total
        idx == 1 (mod 3)  DARK_A, SA_ST_A, NQR17, SA_ST_B  4 each, 16
        idx == 2 (mod 3)  C3, CAS_EXT, D7, SEED        8 each, 32

    This is exact, not sampled -- a full period is finite and complete.  It
    is also TIER A and carries no information about 37: every prime p == 1
    (mod 3) tested (7, 13, 19, 31, 37, 43, 61, 67, 73, 79, 97, 103, 109)
    shows a non-uniform cubic split.  Checked before claiming, which is the
    point.

=== THE TWO NUMBERS ===

        358 == 25  SA_ST_B        853 == 2  DARK_A

    For digits (a, b, a+b) the closed forms are abc = 101a + 11b and
    cba = 101a + 110b, so 358 = 303 + 55 and 853 = 303 + 550.  Mod 37 that
    is 27a + 11b and 27a - b, since 110 == -1.  No further structure found,
    and none claimed.

=== FALSIFICATION ===
    A root of x^2 - x - 1 in GF(37); or pi(37) != 76.
"""

P = 37
ORBITS = {
    'IC': (1, 10, 26),      'DARK_A': (2, 15, 20),  'C3': (3, 4, 30),
    'CAS_EXT': (5, 13, 19), 'TESLA': (6, 8, 23),    'D7': (7, 33, 34),
    'SA_ST_A': (9, 12, 16), 'NEG_H': (11, 27, 36),  'C9': (14, 29, 31),
    'NQR17': (17, 22, 35),  'SEED': (18, 24, 32),   'SA_ST_B': (21, 25, 28),
}
BY = {r: n for n, o in ORBITS.items() for r in o}
IDX = {BY[pow(2, j, P)]: j for j in range(12)}


def is_prime(n):
    return n > 1 and all(n % k for k in range(2, int(n ** .5) + 1))


def pisano(p):
    a, b, n = 0, 1, 0
    while True:
        a, b = b, (a + b) % p
        n += 1
        if (a, b) == (0, 1):
            return n


def run():
    from collections import Counter

    # --- the prohibition ---
    assert P % 5 == 2
    QR = {(x * x) % P for x in range(1, P)}
    assert 5 not in QR
    assert [x for x in range(P) if (x * x - x - 1) % P == 0] == []
    # and it DOES exist in GF(37^2): x^2-x-1 factors there
    # (checked via the discriminant having a square root in the extension)
    assert pow(5, (P - 1) // 2, P) == P - 1            # Euler: 5 is a non-residue

    # --- the contrast ---
    assert P % 3 == 1
    assert [x for x in range(P) if (x * x + x + 1) % P == 0] == [10, 26]
    yes = [p for p in range(2, 60) if is_prime(p) and p % 5 in (1, 4)]
    no = [p for p in range(2, 60) if is_prime(p) and p % 5 in (2, 3)]
    assert yes == [11, 19, 29, 31, 41, 59] and P in no

    # --- the Pisano period is maximal ---
    n = pisano(P)
    assert n == 76 == 2 * (P + 1)

    # --- the cubic split, exact over one period ---
    fib, a, b = [], 0, 1
    for _ in range(n):
        fib.append(a)
        a, b = b, (a + b) % P
    assert len(fib) == 76
    z = sum(1 for x in fib if x == 0)
    assert z == 4
    c = Counter(BY[x] for x in fib if x)
    assert sum(c.values()) == 72
    assert sorted(set(c.values())) == [4, 6, 8]
    groups = {m: sorted(o for o in ORBITS if IDX[o] % 3 == m) for m in range(3)}
    for m, want in ((0, 6), (1, 4), (2, 8)):
        assert len(groups[m]) == 4
        assert all(c[o] == want for o in groups[m]), (m, [c[o] for o in groups[m]])
    assert groups[0] == sorted(['IC', 'TESLA', 'NEG_H', 'C9'])

    # --- but it is Tier A: generic, not about 37 ---
    def cubic_split(p):
        g = next(g for g in range(2, p)
                 if len({pow(g, k, p) for k in range(p - 1)}) == p - 1)
        dl = {pow(g, k, p): k for k in range(p - 1)}
        m = pisano(p)
        x, y, cc = 0, 1, Counter()
        for _ in range(m):
            if x:
                cc[dl[x] % 3] += 1
            x, y = y, (x + y) % p
        return cc
    for p in (7, 13, 19, 31, 37, 43, 61, 67, 73, 79, 97, 103, 109):
        assert p % 3 == 1
        cc = cubic_split(p)
        assert len(set(cc.values())) > 1, p       # non-uniform EVERYWHERE

    # --- the two numbers ---
    assert 358 % P == 25 and BY[25] == 'SA_ST_B'
    assert 853 % P == 2 and BY[2] == 'DARK_A'
    assert 358 == 101 * 3 + 11 * 5 and 853 == 101 * 3 + 110 * 5
    assert 110 % P == P - 1
    assert 3 + 5 == 8                                   # consecutive Fibonacci
    assert [x for x in fib[:8]] == [0, 1, 1, 2, 3, 5, 8, 13]

    print("All assertions passed.\n")
    print("THEOREM 344.  There is no golden ratio in GF(37).\n")
    print("   phi solves x^2 - x - 1 = 0, discriminant 5.")
    print(f"   37 mod 5 = {P%5}, so 5 is a non-residue and the equation has")
    print(f"   NO root: solution set over all 37 residues is empty.")
    print( "   phi lives in GF(37^2) and nowhere smaller.  A construction")
    print( "   placing phi in this field is not approximate -- it does not\n"
           "   exist.\n")
    print("  THE CONTRAST")
    print(f"   37 == 1 (mod 3)  ->  x^2+x+1 splits, roots 10, 26")
    print( "                    ->  cube roots of unity, the twelve orbits,")
    print( "                        T331 T333 T340 T341 T343")
    print(f"   37 == 2 (mod 5)  ->  x^2-x-1 does not split  ->  no phi")
    print( "   One congruence builds the corpus, the other forbids a family")
    print( "   of constructions habitually paired with it.\n")
    print(f"   phi exists mod:     {yes}")
    print(f"   phi does not mod:   {no}\n")
    print(f"  PISANO PERIOD MAXIMAL:  pi(37) = {n} = 2 x 38 = 2(37+1)")
    print( "   the longest cycle the field allows, precisely BECAUSE phi is")
    print( "   absent: the driver lives in GF(37^2) with norm -1.\n")
    print("  A NON-UNIFORMITY THAT IS NOT ABOUT 37")
    print( "   over one complete period the 72 nonzero residues split by")
    print( "   index mod 3 -- the cubic residue class:")
    for m, want in ((0, 6), (1, 4), (2, 8)):
        print(f"     idx == {m} (mod 3)  {want} each, {4*want} total"
              f"   {groups[m]}")
    print( "   exact, not sampled.  But TIER A: every p == 1 (mod 3) tested")
    print( "   is non-uniform too, so it says nothing about 37.  Checked")
    print( "   before claiming, which is the point.\n")
    print("  THE TWO NUMBERS")
    print(f"   358 == {358%P} {BY[358%P]}      853 == {853%P} {BY[853%P]}")
    print( "   digits (a,b,a+b): abc = 101a + 11b, cba = 101a + 110b,")
    print( "   and 110 == -1 mod 37.  No further structure found or claimed.")


if __name__ == "__main__":
    run()
