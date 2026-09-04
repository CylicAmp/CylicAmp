"""
T299 — Two Maps Out of Phi_3, and Why They Land on the Same Subgroup at p=37

Sharpest form of the T297 separation. The seam is not between two sets of
results; it is between two DIFFERENT THINGS ONE CAN DO with a single
polynomial:

    Phi_3(x) = x^2 + x + 1

════════════════════════════════════════════════════════════════════════════
USE 1 — EVALUATE IT (stays in Z and F_p)
════════════════════════════════════════════════════════════════════════════
    Phi_3(137) = 137^2 + 137 + 1 = 18907 = 7 x 37 x 73        (T292)
    A root of Phi_3 in F_p generates mu_3 = {1, 10, 26} at p=37.
    Orbits, cosets, Z/12Z, the subgroup lattice, P^1.          (T285-T296)

Needs: unique factorization of 18907, if you want the three primes.
Never mentions an elliptic curve, a trace, or an endomorphism ring.

════════════════════════════════════════════════════════════════════════════
USE 2 — QUOTIENT BY IT (leaves Z entirely)
════════════════════════════════════════════════════════════════════════════
    Z[x]/(Phi_3) = Z[omega], the Eisenstein integers, disc -3.
    End(y^2 = x^3 + a) = Z[omega] over C.
    Units {+-1, +-omega, +-omega^2} -> six traces of Frobenius.
    p = 1 mod 3  =>  p = pi * conj(pi),  4p = L^2 + 27M^2.
    At p=37: 4*37 = 148 = 11^2 + 27 -> traces {+-1, +-10, +-11}.  (T288)

Needs: 4p = L^2 + 27M^2. Never evaluates Phi_3(137), never partitions F_37*.

════════════════════════════════════════════════════════════════════════════
WHAT THEY SHARE: A ROOT. NOTHING ELSE.
════════════════════════════════════════════════════════════════════════════
                            Use 1                    Use 2
    object            Phi_3 in Z[x]            Z[omega] = Z[x]/(Phi_3)
    output            Phi_3(a) in Z, mu_3      traces of y^2=x^3+a /F_p
    needs a curve     no                       yes
    needs 18907 = 7x37x73   yes                no
    needs 4p=L^2+27M^2      no                 yes

Sharing a reduction of omega does not make the factorization of Phi_3(137)
compute a trace, and does not make a CM trace factor 18907.

════════════════════════════════════════════════════════════════════════════
CORRECTION: THE REDUCED UNIT GROUP HAS SIX ELEMENTS, NOT THREE
════════════════════════════════════════════════════════════════════════════
mu_3 = {1, 10, 26} is the reduction of {1, omega, omega^2} only.
The FULL unit group {+-1, +-omega, +-omega^2} reduces to six elements:

    {1, 10, 11, 26, 27, 36}  =  <11>  =  IC u NEG_H     (T284)

════════════════════════════════════════════════════════════════════════════
THE FORCED COINCIDENCE AT p=37
════════════════════════════════════════════════════════════════════════════
Three separately-defined objects turn out to be one subgroup:

    reduction of Z[omega]*      {1,10,11,26,27,36}   order 6
    the sixth powers (F_37*)^6  {1,10,11,26,27,36}   order 6
    <11>                        {1,10,11,26,27,36}   order 6

WHY IT IS FORCED: F_37* is cyclic of order 36, so it contains exactly one
subgroup of each order dividing 36. Three order-6 subgroups must be equal.
That is a BLOCK 1 fact — pure cyclic group theory, no curve involved.

CONSEQUENCE (explains T288): the twist classes of y^2=x^3+a are cosets of
the sixth powers, hence cosets of the reduced unit group. The "six units
giving six traces" and the "six twist classes" are literally the same six.
T288 recorded this correspondence; here it has a reason.

════════════════════════════════════════════════════════════════════════════
THE COINCIDENCE IS SPECIAL TO j=0 AT p=37
════════════════════════════════════════════════════════════════════════════
For a CM family with n units, the reduced unit group has order n and the
n-th powers have order (p-1)/gcd(n, p-1). These coincide iff

    n * gcd(n, p-1) = p - 1

    j=0     n=6, p=37:   6 * 6 = 36 = p-1     COINCIDE
    j=0     n=6, p=73:   6 * 6 = 36 != 72     differ
    j=1728  n=4, p=37:   4 * 4 = 16 != 36     differ
    j=1728  n=4, p=73:   4 * 4 = 16 != 72     differ

j=1728 at p=37 makes the failure concrete:
    reduced Z[i]*      {1, 6, 31, 36}                     order 4
    fourth powers      {1,7,9,10,12,16,26,33,34}          order 9
    not equal, and not equal at any admissible prime.

So the j=0 alignment needs 6^2 = 36 = p-1. It holds at p=37 and nowhere
else in the admissible set {7, 37, 73}. Unlike the trace-containment
coincidence tested in T297, this one IS structural — it follows from
cyclic-group uniqueness plus an arithmetic identity on p-1.

And it still computes no traces. The two maps land on the same subgroup;
they do not thereby become the same map.
"""

from math import gcd

P = 37


def phi3(x):
    return x * x + x + 1


def factor(n):
    f, d = {}, 2
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f


def subgroup(g, p):
    s, x = set(), 1
    while x not in s:
        s.add(x)
        x = (x * g) % p
    return sorted(s)


# ─── Use 1: evaluate Phi_3 ──────────────────────────────────────────────────

def verify_use1():
    assert phi3(137) == 18907
    assert factor(18907) == {7: 1, 37: 1, 73: 1}
    # a root of Phi_3 in F_37 generates mu_3
    roots = [x for x in range(1, P) if phi3(x) % P == 0]
    assert sorted(roots) == [10, 26]
    for r in roots:
        assert subgroup(r, P) == [1, 10, 26]
    return roots


# ─── Use 2: quotient by Phi_3 ───────────────────────────────────────────────

def verify_use2():
    """4p = L^2+27M^2 gives the six j=0 traces; check against brute force."""
    L, M = 11, 1
    assert 4 * P == L * L + 27 * M * M == 148
    h1, h2 = (L + 9 * M) // 2, (L - 9 * M) // 2
    pred = sorted({L, -L, h1, -h1, h2, -h2})
    assert pred == [-11, -10, -1, 1, 10, 11]

    obs = set()
    for a in range(1, P):
        n = 1
        for x in range(P):
            r = (x ** 3 + a) % P
            for y in range(P):
                if (y * y) % P == r:
                    n += 1
        obs.add(P + 1 - n)
    assert sorted(obs) == pred, f"{sorted(obs)} != {pred}"
    return pred


# ─── The reduced unit group ─────────────────────────────────────────────────

def reduced_units(omega, p):
    """Reduction of {+-1, +-w, +-w^2} for a root w of Phi_3."""
    w2 = (omega * omega) % p
    return sorted({1, (-1) % p, omega, (-omega) % p, w2, (-w2) % p})


def verify_unit_reduction():
    u = reduced_units(26, P)
    assert len(u) == 6, f"expected 6 units, got {len(u)}"
    assert u == [1, 10, 11, 26, 27, 36]
    # mu_3 is only half of it
    assert subgroup(26, P) == [1, 10, 26]
    assert set(subgroup(26, P)) < set(u)

    sixth = sorted({pow(x, 6, P) for x in range(1, P)})
    g11 = subgroup(11, P)
    assert u == sixth == g11, f"{u} {sixth} {g11}"

    # forced: C_36 has exactly one subgroup per divisor
    divs = [d for d in range(1, 37) if 36 % d == 0]
    for d in divs:
        subs = set()
        for g in range(1, P):
            s = subgroup(g, P)
            if len(s) == d:
                subs.add(tuple(s))
        assert len(subs) == 1, f"order {d}: {len(subs)} subgroups"
    return u, sixth, g11


# ─── The coincidence condition ──────────────────────────────────────────────

def coincidence(n, p):
    """Reduced unit group (order n) equals the n-th powers?"""
    return n * gcd(n, p - 1) == p - 1


def verify_coincidence():
    rows = []
    for n, lab in ((6, 'j=0'), (4, 'j=1728')):
        for p in (37, 73):
            rows.append((lab, n, p, n * gcd(n, p - 1), p - 1,
                         coincidence(n, p)))
    assert coincidence(6, 37) is True
    assert coincidence(6, 73) is False
    assert coincidence(4, 37) is False
    assert coincidence(4, 73) is False

    # concrete failure for j=1728 at p=37
    i_ = 6
    assert (i_ * i_) % P == P - 1
    u4 = sorted({1, (-1) % P, i_, (-i_) % P})
    fourth = sorted({pow(x, 4, P) for x in range(1, P)})
    assert len(u4) == 4 and len(fourth) == 9 and u4 != fourth
    return rows, u4, fourth


def run():
    print("=" * 76)
    print("T299 — Two Maps Out of Phi_3 = x^2 + x + 1")
    print("=" * 76)

    roots = verify_use1()
    print("\n--- USE 1: evaluate it (stays in Z and F_p) ---")
    print(f"  Phi_3(137) = {phi3(137)} = {factor(18907)}")
    print(f"  roots of Phi_3 in F_37: {roots}; each generates mu_3 = "
          f"{subgroup(26, P)}")
    print("  Needs: factorization of 18907. Mentions no curve, trace, or ring.")

    pred = verify_use2()
    print("\n--- USE 2: quotient by it (leaves Z entirely) ---")
    print("  Z[x]/(Phi_3) = Z[omega], disc -3, End(y^2=x^3+a) over C")
    print(f"  4*37 = 148 = 11^2 + 27*1^2  ->  traces {pred}")
    print("  Verified against brute-force point counts.")
    print("  Needs: 4p = L^2+27M^2. Never evaluates Phi_3(137).")

    u, sixth, g11 = verify_unit_reduction()
    print("\n--- CORRECTION: the reduced unit group has SIX elements ---")
    print(f"  mu_3 = reduction of {{1, w, w^2}}        = {subgroup(26,P)}")
    print(f"  reduction of the FULL unit group      = {u}")
    print("  The second is <11> = IC u NEG_H (T284), not IC.")

    print("\n--- THE FORCED COINCIDENCE AT p=37 ---")
    print(f"  reduced Z[omega]*   {u}   order {len(u)}")
    print(f"  sixth powers        {sixth}   order {len(sixth)}")
    print(f"  <11>                {g11}   order {len(g11)}")
    print("  All equal. FORCED: F_37* is cyclic of order 36, so it has")
    print("  exactly one subgroup of each order dividing 36 (verified for")
    print("  all nine divisors). Three order-6 subgroups must coincide.")
    print("  This is a BLOCK 1 fact — no curve appears in the argument.")
    print("\n  Consequence: T288's twist classes are cosets of the sixth")
    print("  powers = cosets of the reduced unit group. The 'six units ->")
    print("  six traces' and the 'six twist classes' are the same six.")

    rows, u4, fourth = verify_coincidence()
    print("\n--- THE COINCIDENCE IS SPECIAL TO j=0 AT p=37 ---")
    print("  reduced unit group has order n; n-th powers have order")
    print("  (p-1)/gcd(n,p-1). Equal iff  n * gcd(n, p-1) = p - 1.")
    print(f"\n  {'family':>8} {'n':>2} {'p':>4} {'n*gcd(n,p-1)':>14} {'p-1':>5}  result")
    for lab, n, p, lhs, rhs, ok in rows:
        print(f"  {lab:>8} {n:>2} {p:>4} {lhs:>14} {rhs:>5}  "
              f"{'COINCIDE' if ok else 'differ'}")
    print(f"\n  j=1728 at p=37, concretely:")
    print(f"    reduced Z[i]*  {u4}   order {len(u4)}")
    print(f"    fourth powers  {fourth}   order {len(fourth)}")
    print("  The j=0 alignment needs 6^2 = 36 = p-1. True at p=37, and")
    print("  nowhere else in the admissible set {7, 37, 73}.")
    print("\n  Unlike the trace-containment coincidence of T297, this one IS")
    print("  structural: cyclic-group uniqueness plus an identity on p-1.")
    print("  It still computes no traces. The two maps land on the same")
    print("  subgroup; they do not thereby become the same map.")

    print("\nAll T299 assertions passed.")


if __name__ == '__main__':
    run()
