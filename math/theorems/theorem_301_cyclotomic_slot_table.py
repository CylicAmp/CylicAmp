"""
T301 — The Cyclotomic Slot Table: Where 37 Actually Sits

Generalizes the cyclotomic form introduced in the T300 correction. There,
x^3 - 1 = Phi_1(x)*Phi_3(x) replaced T292's ad hoc split of 137^3 - 1.
The same machinery works for every d, and it locates 37 in a table rather
than at a distinguished point.

════════════════════════════════════════════════════════════════════════════
THE MECHANISM
════════════════════════════════════════════════════════════════════════════
    p | Phi_d(a)   =>   ord_p(a) = d,   unless p | d
    (and in that exceptional case p is the largest prime factor of d)

So the primes are partitioned by their order for a fixed base a: the primes
with ord_p(137) = d are exactly the prime factors of Phi_d(137), minus the
divisors of d. Verified for every prime p < 2000 with p != 137: each lands
in the cyclotomic factor indexed by its own order, zero misses.

════════════════════════════════════════════════════════════════════════════
THE TABLE FOR a = 137
════════════════════════════════════════════════════════════════════════════
    d   Phi_d(137)                  factorization
    1                        136    2^3 x 17
    2                        138    2 x 3 x 23
    3                      18907    7 x 37 x 73          <- the framework
    4                      18770    2 x 5 x 1877
    5                  354865621    11 x 101 x 319411
    6                      18633    3 x 6211
    7              6660472840687    8933 x 745603139
    8                  352275362    2 x 41 x 1409 x 3049
    9              6611858821963    19 x 27847 x 12496591
   10                  349722641    71 x 881 x 5591
   11     2346320474383711003267    prime
   12                  352256593    13 x 2473 x 10957

Every order claim checked: each prime factor p of Phi_d(137) has
ord_p(137) = d, or else p | d (the 2s in rows 2, 4, 8 and the 3 in row 6).

37 is one of three primes in the d=3 slot. The slot is not distinguished;
it is the slot the framework uses.

════════════════════════════════════════════════════════════════════════════
OTHER ROWS OF THE SAME TABLE
════════════════════════════════════════════════════════════════════════════
CORRECTION TO AN EARLIER FRAMING: these were called "frameworks that were
available", which gives them a status they do not have. Nobody built them,
and 37 was not selected off a menu. A k-orbit picture over F_p needs
ord_p(137) = k, hence p | Phi_k(137); for k=3 the primes are small and
include 37, and 137 = 26 (mod 37) is a root of Phi_3. That is why the plate
is drawn in F_37. The rows below are other values of Phi_k, not unused
alternatives.

The counterfactual in the next section is still mathematically real — it
says what WOULD hold at even k — but it describes the arithmetic, not a
choice anyone made.

    k    admissible primes         orbit counts (p-1)/k
    2    3, 23                     1, 11
    3    7, 37, 73                 2, 12, 24        <- chosen
    4    5, 1877                   1, 469
    5    11, 101, 319411           2, 20, 63882
    6    6211                      1035

Nothing forces k = 3 except that 137 reduces to a cube root of unity mod 37.

════════════════════════════════════════════════════════════════════════════
BUT ONE CONSTRAINT IS REAL: k MUST BE ODD
════════════════════════════════════════════════════════════════════════════
If k is even, then m^(k/2) has order 2, hence m^(k/2) = -1, so -1 lies INSIDE
<m>. Then -x sits in the same orbit as x: every orbit is self-antipodal and
the pairing of T283 collapses entirely.

    k    p        -1 in <m>?    antipodal structure
    2    3, 23    yes           COLLAPSES (every orbit self-paired)
    3    7        no            1 pair
    3    37       no            6 pairs
    3    73       no            12 pairs
    4    5, 1877  yes           COLLAPSES
    5    11       no            1 pair
    5    101      no            10 pairs
    5    319411   no            31941 pairs
    6    6211     yes           COLLAPSES

So T283, T284, T286's antipodal-closure, T289's twist pairs and T296's
180-degree rotation all require k odd. k = 3 is the smallest odd k > 1.
That is a genuine structural constraint the framework satisfies.

It does not single out k = 3. k = 5 was equally available and would have
given 20 orbits at p = 101, with 10 antipodal pairs and a Z/20Z quotient.

════════════════════════════════════════════════════════════════════════════
THIS AUDIT IS USE 1 ONLY  (T299 split, generalized to all d)
════════════════════════════════════════════════════════════════════════════
Everything above evaluates Phi_d in Z[x] at 137 and factors the result.
That is Use 1. It computes no class numbers and no traces.

Use 2 for general d is the ring Z[x]/(Phi_d) = Z[zeta_d], of degree phi(d).
Elliptic CM requires an imaginary quadratic ring, i.e. degree 2:

    d    phi(d)   Q(zeta_d)              elliptic CM?
    1      1      Q                      no
    2      1      Q                      no
    3      2      Q(sqrt(-3))            YES
    4      2      Q(i)                   YES
    5      4      degree-4 cyclotomic    no
    6      2      Q(sqrt(-3))            YES  (same field as d=3)
    7      6      degree-6 cyclotomic    no
   >=5     >=4    higher cyclotomic      no

So Use 2 yields elliptic CM for exactly two fields, Q(sqrt(-3)) and Q(i).
For d >= 5 (d != 6) the ring has degree >= 4 and belongs to abelian
varieties, not elliptic curves. Nothing in the Use-1 table above touches it.

This also closes T300's completeness claim. The imaginary quadratic orders
of class number one are the nine Heegner discriminants

    -3, -4, -7, -8, -11, -19, -43, -67, -163

and only -3 and -4 carry units beyond +-1 (six and four respectively). Hence
n in {2, 4, 6} exactly, which is why T300's list {5, 17, 37} is complete.

════════════════════════════════════════════════════════════════════════════
WHAT THIS SETTLES
════════════════════════════════════════════════════════════════════════════
The row the framework occupies is one row of an infinite table. Its size
(three primes) is unremarkable — d=5, d=9 and d=12 also have three. The
parity of k is the one property that matters, because that is what keeps the
antipodal structure alive.

Same split as before: Use 1 factors integers, Use 2 builds rings. This
theorem is entirely Use 1.
"""

from sympy import factorint, isprime, n_order, cyclotomic_poly, Poly
from sympy.abc import x

BASE = 137


def phi(d, a=BASE):
    return int(Poly(cyclotomic_poly(d, x)).eval(a))


def admissible(k, a=BASE):
    """Primes p with ord_p(a) = k, i.e. factors of Phi_k(a) not dividing k."""
    return sorted(p for p in factorint(phi(k, a))
                  if a % p and n_order(a, p) == k)


# ─── Part 1: the order rule holds throughout the table ──────────────────────

def verify_order_rule(dmax=12):
    rows = {}
    for d in range(1, dmax + 1):
        v = phi(d)
        f = factorint(v)
        for p in f:
            if BASE % p == 0:
                continue
            o = n_order(BASE, p)
            assert o == d or d % p == 0, \
                f"Phi_{d}: p={p} has order {o}, and p does not divide d"
        rows[d] = (v, f)
    return rows


def verify_partition(limit=2000):
    """Every prime p != 137 lands in the cyclotomic factor of its own order."""
    misses = []
    for p in range(3, limit):
        if not isprime(p) or BASE % p == 0:
            continue
        d = n_order(BASE, p)
        if phi(d) % p != 0:
            misses.append((p, d))
    assert misses == [], f"misses: {misses}"
    return limit


# ─── Part 2: the framework's row ────────────────────────────────────────────

def verify_framework_row():
    assert phi(3) == 18907
    assert factorint(18907) == {7: 1, 37: 1, 73: 1}
    assert admissible(3) == [7, 37, 73]
    assert phi(1) == 136 == 2 ** 3 * 17
    assert 17 not in factorint(18907)
    return admissible(3)


# ─── Part 3: k must be odd for the antipodal structure ──────────────────────

def antipodal_profile(k, p):
    """Return (-1 in <m>, #orbits, #self-antipodal orbits)."""
    m = BASE % p
    assert n_order(BASE, p) == k
    H = {pow(m, i, p) for i in range(k)}
    inside = (p - 1) in H
    seen, tot, selfa = set(), 0, 0
    for xx in range(1, p):
        if xx in seen:
            continue
        o = {(xx * pow(m, i, p)) % p for i in range(k)}
        seen |= o
        tot += 1
        if {((p - 1) * e) % p for e in o} == o:
            selfa += 1
    return inside, tot, selfa


def verify_parity_constraint():
    rows = []
    for k in (2, 3, 4, 5, 6):
        for p in admissible(k):
            if p > 20000:            # keep the enumeration cheap
                rows.append((k, p, k % 2 == 0, None, None))
                continue
            inside, tot, selfa = antipodal_profile(k, p)
            # -1 in <m>  iff  k even
            assert inside == (k % 2 == 0), f"k={k}, p={p}: inside={inside}"
            if k % 2 == 0:
                assert selfa == tot, f"k={k}, p={p}: expected total collapse"
            else:
                assert selfa == 0, f"k={k}, p={p}: expected no self-antipodal"
            rows.append((k, p, inside, tot, selfa))
    return rows


def run():
    print("=" * 76)
    print("T301 — The Cyclotomic Slot Table: Where 37 Actually Sits")
    print("=" * 76)

    rows = verify_order_rule()
    lim = verify_partition()
    print("\n--- Part 1: p | Phi_d(a) => ord_p(a) = d, unless p | d ---")
    print(f"  {'d':>3} {'Phi_d(137)':>24}  factorization")
    for d in sorted(rows):
        v, f = rows[d]
        fs = ' x '.join(f"{b}^{e}" if e > 1 else str(b)
                        for b, e in sorted(f.items()))
        fs = 'prime' if len(f) == 1 and list(f.values())[0] == 1 and v > 10**12 else fs
        print(f"  {d:>3} {v:>24}  {fs}")
    print(f"\n  Order rule verified for every factor above.")
    print(f"  Every prime p < {lim} with p != 137 lands in the cyclotomic")
    print(f"  factor indexed by its own order. Zero misses.")

    fw = verify_framework_row()
    print("\n--- Part 2: the framework's row ---")
    print(f"  Phi_3(137) = 18907 = 7 x 37 x 73   ->  admissible {fw}")
    print(f"  Phi_1(137) = 136 = 2^3 x 17, and 17 does NOT divide 18907.")
    print("  37 is one of three primes in the d=3 slot. The slot is not")
    print("  distinguished; it is the slot the framework uses.")

    print("\n--- Part 3: other rows of the same table ---")
    print("  (These are other values of Phi_k, not unused alternatives.")
    print("   A k-orbit picture needs ord_p(137)=k, hence p | Phi_k(137);")
    print("   for k=3 the primes are small and include 37.)")
    print(f"  {'k':>3}  {'primes with ord=k':<28} orbit counts (p-1)/k")
    for k in (2, 3, 4, 5, 6):
        ps = admissible(k)
        oc = [(p - 1) // k for p in ps]
        mark = '   <- the row in use' if k == 3 else ''
        print(f"  {k:>3}  {str(ps):<28} {oc}{mark}")

    prof = verify_parity_constraint()
    print("\n--- Part 4: k must be ODD or the antipodal structure collapses ---")
    print("  k even => m^(k/2) has order 2 => m^(k/2) = -1 => -1 in <m>,")
    print("  so -x shares an orbit with x and every orbit is self-antipodal.")
    print(f"\n  {'k':>3} {'p':>8} {'-1 in <m>':>10} {'orbits':>8} {'self-anti':>10}  structure")
    for k, p, inside, tot, selfa in prof:
        if tot is None:
            print(f"  {k:>3} {p:>8} {str(inside):>10} {'--':>8} {'--':>10}  (large)")
            continue
        s = "COLLAPSES" if selfa == tot else f"{tot//2} pairs"
        print(f"  {k:>3} {p:>8} {str(inside):>10} {tot:>8} {selfa:>10}  {s}")
    print("\n  T283, T284, T286 antipodal-closure, T289 twist pairs and T296's")
    print("  180-degree rotation ALL require k odd. k=3 is the smallest odd")
    print("  k > 1 — a genuine constraint the arithmetic satisfies here.")
    print("  This is a fact about even k, not about a choice anyone made:")
    print("  at k=5 the same structure appears, 10 pairs at p=101.")

    print("\n--- Part 5: this audit is USE 1 only (T299 split, all d) ---")
    print("  Everything above evaluates Phi_d at 137 and factors it.")
    print("  Use 2 is the ring Z[x]/(Phi_d) = Z[zeta_d], of degree phi(d).")
    print("  Elliptic CM needs degree 2:")
    print(f"    {'d':>3} {'phi(d)':>7}  {'field':<22} elliptic CM?")
    from sympy import totient
    for d in (1, 2, 3, 4, 5, 6, 7):
        ph = int(totient(d))
        fld = {1: 'Q', 2: 'Q', 3: 'Q(sqrt(-3))', 4: 'Q(i)',
               6: 'Q(sqrt(-3))'}.get(d, f'degree-{ph} cyclotomic')
        print(f"    {d:>3} {ph:>7}  {fld:<22} {'YES' if d in (3,4,6) else 'no'}")
    print("  Exactly two fields: Q(sqrt(-3)) and Q(i). For d >= 5 (d != 6)")
    print("  the degree is >= 4 — abelian varieties, not elliptic curves.")
    print("\n  This also closes T300: the class-number-one imaginary quadratic")
    print("  discriminants are -3,-4,-7,-8,-11,-19,-43,-67,-163, and only")
    print("  -3 and -4 carry units beyond +-1 (six and four). Hence n in")
    print("  {2,4,6} exactly, so T300's list {5,17,37} is complete.")

    print("\n" + "=" * 76)
    print("  The row in use is one row of an infinite table. Three primes is")
    print("  unremarkable (d=5, d=9, d=12 also have three). The parity of k is")
    print("  the one property that matters, because it keeps the antipodal")
    print("  structure alive.  Use 1 factors integers; Use 2 builds rings.")
    print("  This theorem is entirely Use 1.")
    print("=" * 76)
    print("\nAll T301 assertions passed.")


if __name__ == '__main__':
    run()
