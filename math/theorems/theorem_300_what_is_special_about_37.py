"""
T300 — What Is Actually Special About 37: a Complete Classification

The whole thread has circled one question. T292, T293, T297 and T299 make it
answerable exactly. Every property the framework attributes to 37 falls into
one of three tiers.

════════════════════════════════════════════════════════════════════════════
TIER A — TRUE FOR EVERY PRIME p = 1 (mod 3).  Nothing to do with 37.
════════════════════════════════════════════════════════════════════════════
    mu_3 exists; the multiplier orbit has size 3
    (p-1)/3 orbits, quotient cyclic of that order
    antipodal pairing exists and is fixed-point-free (-1 has order 2, 2 does
        not divide 3, so -1 is never in mu_3 for odd p)
    |P^1(F_p)| = p+1 = 2 + ((p-1)/3) x 3
    the subgroup lattice above mu_3: orders 3d for d | (p-1)/3
    j=0 curves fall into gcd(6, p-1) isomorphism classes
    CM: 4p = L^2 + 27M^2 determines six traces

The 12 orbits at p=37 are just (37-1)/3. Twelve is not a property of 37,
it is a property of 36.

════════════════════════════════════════════════════════════════════════════
TIER B — TRUE FOR {7, 37, 73} AND NO OTHER PRIME.               (T292)
════════════════════════════════════════════════════════════════════════════
    ord_p(137) = 3, i.e. 137 reduces to a primitive cube root of unity.
    Forced by 137^3 - 1 = 2^3 x 17 x (7 x 37 x 73), with the 136 branch
    excluded because 137 = 1 (mod 2) and (mod 17).

This is the only tier where the number 137 does any work at all.

════════════════════════════════════════════════════════════════════════════
TIER C — UNIQUE TO 37 AMONG ALL PRIMES
════════════════════════════════════════════════════════════════════════════
THE RESULT. Let R be the CM ring of a family of curves, n = |R^*| the number
of units. The reduction of R^* modulo a prime above p has order n; the n-th
powers in F_p^* form a subgroup of order (p-1)/gcd(n, p-1). These two
subgroups coincide iff

    n * gcd(n, p-1) = p - 1.

When n | p-1 the gcd is n and the condition collapses to

    p - 1 = n^2,     i.e.     p = n^2 + 1.

So for each CM family there is AT MOST ONE prime where the reduced unit
group is the n-th power subgroup, and it is n^2 + 1.

The possible CM unit-group sizes are exactly 2, 4, 6 (an imaginary quadratic
order has units {+-1}, or Z[i] with four, or Z[omega] with six). Hence the
complete list is three primes:

    n = 2   generic       R = Z          p = 2^2+1 =  5
    n = 4   Gaussian      R = Z[i]       p = 4^2+1 = 17     j = 1728
    n = 6   Eisenstein    R = Z[omega]   p = 6^2+1 = 37     j = 0

Verified by exhaustive search over all primes below 100000: exactly one
prime satisfies the condition for each n, and it is n^2+1 in each case.
Verified directly at each:

    p= 5, n=2:  units {1,4}                 = squares       yes
    p=17, n=4:  units {1,4,13,16}           = 4th powers    yes
    p=37, n=6:  units {1,10,11,26,27,36}    = 6th powers    yes

37 IS THE EISENSTEIN MEMBER OF A THREE-ELEMENT LIST.

That is the precise sense in which 37 is distinguished, and it is the only
sense that survives the T297/T299 audit. It explains T288 (twist classes are
cosets of the reduced unit group) and it is entirely Tier-A in character —
cyclic-group order arithmetic — with the CM families supplying only n.

════════════════════════════════════════════════════════════════════════════
A NEAR-MISS, FLAGGED SO IT IS NOT LATER READ AS STRUCTURE
════════════════════════════════════════════════════════════════════════════
17 is the Gaussian member of the list above, and 17 also divides 137 - 1
(136 = 2^3 x 17), where it appears as the excluded branch in T292.
Those are unrelated. 17 | 136 because 137 = 1 (mod 17) — a fact about 137.
The list membership is a fact about 4^2+1. Two different reasons, one numeral.

════════════════════════════════════════════════════════════════════════════
WHAT 137 DOES AND DOES NOT DO
════════════════════════════════════════════════════════════════════════════
Does:   picks out {7, 37, 73} via ord_p(137) = 3.                (Tier B)
Does not: supply the orbit structure (any cube root of unity does — T295),
        supply the traces (CM does), or explain Tier C (which never
        mentions 137).
"""

from math import gcd, isqrt

CM_FAMILIES = [
    # (n units, ring, j-invariant, label)
    (2, 'Z',        'any',  'generic'),
    (4, 'Z[i]',     '1728', 'Gaussian'),
    (6, 'Z[omega]', '0',    'Eisenstein'),
]


def is_prime(n):
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0:
        return False
    return all(n % i for i in range(3, isqrt(n) + 1, 2))


def coincidence(n, p):
    """Reduced unit group (order n) equals the n-th powers in F_p^*?"""
    return n * gcd(n, p - 1) == p - 1


# ─── Tier A: holds for every p = 1 mod 3 ────────────────────────────────────

def verify_tier_a(primes=(7, 13, 19, 31, 37, 43, 61, 73, 97, 103)):
    rows = []
    for p in primes:
        assert p % 3 == 1 and is_prime(p)
        roots = [x for x in range(2, p) if pow(x, 3, p) == 1]
        assert len(roots) == 2, f"p={p}: {roots}"
        w = roots[0]
        mu3 = {pow(w, i, p) for i in range(3)}
        assert len(mu3) == 3
        assert (p - 1) not in mu3            # antipodal pairing exists
        seen, norb = set(), 0
        for x in range(1, p):
            if x in seen:
                continue
            o = {(x * pow(w, i, p)) % p for i in range(3)}
            assert len(o) == 3
            seen |= o
            norb += 1
        assert norb == (p - 1) // 3
        assert p + 1 == 2 + norb * 3          # P^1
        assert len({pow(x, 6, p) for x in range(1, p)}) == (p - 1) // gcd(6, p - 1)
        rows.append((p, norb, (p - 1) // 3))
    return rows


# ─── Tier B: ord_p(137) = 3 pins {7, 37, 73} ────────────────────────────────

def order_mod(a, p):
    a %= p
    if a == 0:
        return None
    k, v = 1, a
    while v != 1:
        v = (v * a) % p
        k += 1
    return k


def verify_tier_b():
    valid = [p for p in range(2, 200) if is_prime(p) and 137 % p
             and order_mod(137, p) == 3]
    assert valid == [7, 37, 73], f"{valid}"
    assert 137 ** 3 - 1 == 136 * 18907
    assert 18907 == 7 * 37 * 73
    for p in (2, 17):                      # the excluded 136 branch
        assert 137 % p == 1 and order_mod(137, p) == 1
    return valid


# ─── Tier C: p = n^2 + 1, one prime per CM family ───────────────────────────

def verify_tier_c(limit=100000):
    out = {}
    for n, ring, j, label in CM_FAMILIES:
        hits = [p for p in range(3, limit) if is_prime(p) and coincidence(n, p)]
        assert hits == [n * n + 1], f"n={n}: {hits} != [{n*n+1}]"
        assert is_prime(n * n + 1)
        out[n] = (ring, j, label, n * n + 1)
    return out


def verify_directly():
    """Reduced unit group really equals the n-th powers at each of 5, 17, 37."""
    checks = {}

    # n=2, p=5: units {+-1}
    p, n = 5, 2
    u = sorted({1, (-1) % p})
    checks[p] = (n, u, sorted({pow(x, n, p) for x in range(1, p)}))

    # n=4, p=17: units {+-1, +-i}
    p, n = 17, 4
    i_ = next(x for x in range(1, p) if (x * x) % p == p - 1)
    u = sorted({1, (-1) % p, i_, (-i_) % p})
    checks[p] = (n, u, sorted({pow(x, n, p) for x in range(1, p)}))

    # n=6, p=37: units {+-1, +-w, +-w^2}
    p, n = 37, 6
    w = next(x for x in range(2, p) if pow(x, 3, p) == 1)
    w2 = (w * w) % p
    u = sorted({1, (-1) % p, w, (-w) % p, w2, (-w2) % p})
    checks[p] = (n, u, sorted({pow(x, n, p) for x in range(1, p)}))

    for p, (n, u, npow) in checks.items():
        assert len(u) == n, f"p={p}: {len(u)} units, expected {n}"
        assert u == npow, f"p={p}: {u} != {npow}"
    return checks


def verify_near_miss():
    assert 137 % 17 == 1                 # why 17 | 136
    assert 136 == 2 ** 3 * 17
    assert 4 * 4 + 1 == 17               # why 17 is on the Tier-C list
    return True


def run():
    print("=" * 78)
    print("T300 — What Is Actually Special About 37: a Complete Classification")
    print("=" * 78)

    rows = verify_tier_a()
    print("\n--- TIER A: true for EVERY prime p = 1 (mod 3) ---")
    print("  mu_3, orbits of size 3, cyclic quotient, antipodal pairing,")
    print("  P^1 = 2 + (p-1), subgroup lattice above mu_3, six j=0 classes,")
    print("  CM 4p = L^2+27M^2.")
    print(f"\n  {'p':>5} {'orbits':>7}  = (p-1)/3")
    for p, norb, expect in rows:
        print(f"  {p:>5} {norb:>7}  = {expect}")
    print("  The 12 orbits at p=37 are (37-1)/3. Twelve is a property of 36.")

    valid = verify_tier_b()
    print("\n--- TIER B: true for {7, 37, 73} and no other prime ---")
    print(f"  ord_p(137) = 3  =>  p in {valid}")
    print(f"  137^3 - 1 = 136 x 18907;  18907 = 7 x 37 x 73")
    print(f"  136 = 2^3 x 17 excluded: 137 = 1 mod 2 and mod 17, order 1.")
    print("  This is the ONLY tier where the number 137 does any work.")

    tc = verify_tier_c()
    checks = verify_directly()
    print("\n--- TIER C: unique to 37 among ALL primes ---")
    print("  Reduced CM unit group (order n) = n-th powers (order")
    print("  (p-1)/gcd(n,p-1))  iff  n * gcd(n,p-1) = p-1.")
    print("  With n | p-1 this collapses to  p - 1 = n^2,  i.e.  p = n^2 + 1.")
    print("\n  CM unit-group sizes are exactly 2, 4, 6, so the list is complete:")
    print(f"\n  {'n':>3} {'ring':>10} {'j':>6} {'family':>11} {'p = n^2+1':>10}")
    for n, (ring, j, label, p) in sorted(tc.items()):
        print(f"  {n:>3} {ring:>10} {j:>6} {label:>11} {p:>10}")
    print("\n  Exhaustive search over all primes below 100000 finds exactly")
    print("  one prime per family, and it is n^2+1 each time.")
    print("\n  Direct verification:")
    for p in sorted(checks):
        n, u, npow = checks[p]
        print(f"    p={p:>2}, n={n}: units {u}")
        print(f"              {n}th powers {npow}   equal={u == npow}")
    print("\n  ==> 37 is the EISENSTEIN MEMBER OF A THREE-ELEMENT LIST.")
    print("  That is the precise sense in which 37 is distinguished, and the")
    print("  only sense surviving the T297/T299 audit. It explains T288 and")
    print("  is Tier-A in character: cyclic-group order arithmetic, with the")
    print("  CM families supplying only the value of n.")

    verify_near_miss()
    print("\n--- NEAR-MISS, flagged ---")
    print("  17 is the Gaussian member above, and 17 also divides 137-1.")
    print(f"    136 = 2^3 x 17  because 137 = 1 (mod 17)  [a fact about 137]")
    print(f"    17 = 4^2+1                                [a fact about 4]")
    print("  Unrelated. Two reasons, one numeral.")

    print("\n" + "=" * 78)
    print("  137 DOES:     pick out {7,37,73} via ord_p(137)=3.        (Tier B)")
    print("  137 DOES NOT: supply the orbit structure (any cube root of unity")
    print("                does, T295), supply the traces (CM does), or")
    print("                explain Tier C (which never mentions 137).")
    print("=" * 78)
    print("\nAll T300 assertions passed.")


if __name__ == '__main__':
    run()
