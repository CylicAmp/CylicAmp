# CLASS: THEOREM
"""
Theorem 346: the Collatz map and the 137-map generate only HALF of AGL(1,37)
-- and the half they miss is the quadratic character of differences
Author: Michael Warren Song (CyclicAmp)

T338 showed the Sophie Germain map and the 137-map generate the FULL affine
group, so they share no invariant at all.  The Collatz map behaves the
opposite way, and the reason is one line: 2 is a primitive root mod 37 and
3 is not.

T271 already has C(x) = 3x+1 as an affine bijection, its fixed point 18 in
SEED, its seam preimage 12, and the S/C duality.  What follows is about the
GROUP, which T271 does not treat.

=== THE ORDERS SPLIT THE THREE MAPS ===

        ord_37(2)  = 36      primitive root
        ord_37(3)  = 18      NOT primitive -- index 2
        ord_37(26) =  3

    and the cycle types follow directly:

        sigma(x) = 2x+1     1 fixed point + one 36-cycle        (T337)
        C(x)     = 3x+1     1 fixed point + TWO 18-cycles
        mu(x)    = 26x      1 fixed point + twelve 3-cycles     (T341)

    C is conjugate to multiplication by 3 in the coordinate y = x - 18,
    since 18 is its fixed point (3x+1 = x forces 2x = -1, x = 18).
    Verified for every x.

=== THE GROUPS ===

        <sigma, mu>        1332 = AGL(1,37) entire       (T338)
        <C, sigma>         1332 = entire
        <C, sigma, mu>     1332 = entire
        <C, mu>             666 = index 2                 <-- PROPER

    <C, mu> is the only proper one, and its linear parts are exactly the
    eighteen quadratic residues.  Forced: the linear parts generated are
    <3, 26> = <2^26, 2^12> = <2^gcd(26,12,36)> = <2^2>, the squares.

=== WHAT THE PROPER HALF PRESERVES ===

    For an affine map x -> ax+b,

        (ax+b) - (ay+b) = a(x-y)

    so differences scale by the linear part, and the Legendre symbol
    chi(x-y) is preserved exactly when a is a quadratic residue.  Since
    every linear part in <C, mu> is a QR:

        <C, mu>     PRESERVES chi(x-y)
        <sigma, mu> DESTROYS it

    Both verified over all 666 (resp. 1332) group elements and all 666
    unordered pairs.

    Note the shape of the invariant.  <C, mu> is still TRANSITIVE on the 37
    points, so no nonconstant function of a single point survives -- T338's
    rank computation would return dimension 1 here too.  What survives is a
    function of PAIRS.  It reaches 666 of the 1332 ordered pairs, exactly
    half, which is what failing 2-transitivity by index 2 means.

    So T338's conclusion ("no joint taxonomy") was correct for the maps it
    tested and does NOT generalise: swap sigma for C and a joint invariant
    appears immediately.  It is simply not a partition of points.

=== 666 HERE IS THE SAME FORMULA, NOT A SIGHTING ===

    |<C, mu>| = |QR| x p = 18 x 37 = 666, and T332's total sum(1..36) =
    p(p-1)/2 = 18 x 37 = 666.  Both are ((p-1)/2) x p.  One formula
    evaluated twice, not two occurrences of a number.

=== FALSIFICATION ===
    ord_37(3) != 18; |<C,mu>| != 666; or an element of <C,mu> whose linear
    part is a non-residue.
"""

P = 37
C = lambda x: (3 * x + 1) % P
S = lambda x: (2 * x + 1) % P
MU = lambda x: (26 * x) % P
QR = {(x * x) % P for x in range(1, P)}


def chi(d):
    d %= P
    return 0 if d == 0 else (1 if d in QR else -1)


def compose(f, g):
    return ((f[0] * g[0]) % P, (f[0] * g[1] + f[1]) % P)


def generate(*seeds):
    G, frontier = {(1, 0)}, [(1, 0)]
    while frontier:
        nxt = []
        for g in frontier:
            for h in seeds:
                v = compose(h, g)
                if v not in G:
                    G.add(v)
                    nxt.append(v)
        frontier = nxt
    return G


def cycle_type(f):
    from collections import Counter
    seen, out = set(), []
    for x in range(P):
        if x in seen:
            continue
        c, y = 0, x
        while y not in seen:
            seen.add(y)
            c += 1
            y = f(y)
        out.append(c)
    return Counter(out)


def run():
    from math import gcd

    # --- orders ---
    o = lambda a: next(k for k in range(1, P) if pow(a, k, P) == 1)
    assert o(2) == 36 and o(3) == 18 and o(26) == 3
    assert len(QR) == 18

    # --- cycle types ---
    assert dict(cycle_type(S)) == {1: 1, 36: 1}
    assert dict(cycle_type(C)) == {1: 1, 18: 2}
    assert dict(cycle_type(MU)) == {1: 1, 3: 12}

    # --- C is x3 about its fixed point 18 ---
    assert C(18) == 18
    assert (2 * 18) % P == (P - 1)                      # 3x+1=x -> 2x=-1
    for x in range(P):
        assert (C(x) - 18) % P == (3 * (x - 18)) % P

    # --- the groups ---
    Cm, Sm, Mm = (3, 1), (2, 1), (26, 0)
    Gc, Gs = generate(Cm, Mm), generate(Sm, Mm)
    assert len(Gs) == 1332 == 36 * P                     # T338
    assert len(generate(Cm, Sm)) == 1332
    assert len(generate(Cm, Sm, Mm)) == 1332
    assert len(Gc) == 666 == 18 * P
    assert 1332 // len(Gc) == 2
    assert {a for a, _ in Gc} == QR                      # linear parts = QRs
    # forced by the discrete logs
    assert pow(2, 26, P) == 3 and pow(2, 12, P) == 26
    assert gcd(26, 12, 36) == 2

    # --- the invariant ---
    pairs = [(x, y) for x in range(P) for y in range(x + 1, P)]
    assert len(pairs) == 666
    assert all(chi(a * (x - y)) == chi(x - y)
               for a, _ in Gc for x, y in pairs)
    assert not all(chi(a * (x - y)) == chi(x - y)
                   for a, _ in Gs for x, y in pairs)

    # --- still transitive, not 2-transitive ---
    assert {(a * 0 + b) % P for a, b in Gc} == set(range(P))
    reach = {((a * 0 + b) % P, (a * 1 + b) % P) for a, b in Gc}
    assert len(reach) == 666 == P * (P - 1) // 2
    assert len({((a * 0 + b) % P, (a * 1 + b) % P) for a, b in Gs}) == 1332

    # --- 666 is one formula ---
    assert len(Gc) == len(QR) * P == (P - 1) // 2 * P
    assert sum(range(1, P)) == P * (P - 1) // 2 == 666

    print("All assertions passed.\n")
    print("THEOREM 346.  Collatz and the 137-map generate only half.\n")
    print("   ord_37(2)  = 36   primitive root")
    print("   ord_37(3)  = 18   NOT primitive, index 2")
    print("   ord_37(26) =  3\n")
    print("   sigma 2x+1    cycle type 1 + 36        one long cycle")
    print("   C     3x+1    cycle type 1 + 18 + 18   TWO cycles")
    print("   mu     26x    cycle type 1 + 12x3\n")
    print("   C is x3 about its fixed point 18: (C(x)-18) = 3(x-18), all x\n")
    print("  THE GROUPS, inside AGL(1,37) of order 1332")
    for nm, G in (("<sigma, mu>", Gs), ("<C, sigma>", generate(Cm, Sm)),
                  ("<C, sigma, mu>", generate(Cm, Sm, Mm)), ("<C, mu>", Gc)):
        print(f"    {nm:16s} {len(G):5d}   index {1332//len(G)}"
              + ("   <-- PROPER" if len(G) < 1332 else ""))
    print("\n    linear parts of <C,mu> are exactly the 18 QRs, because")
    print("    <3, 26> = <2^26, 2^12> = <2^gcd(26,12,36)> = <2^2>.\n")
    print("  WHAT IT PRESERVES")
    print("    (ax+b) - (ay+b) = a(x-y), so chi(x-y) survives iff a is a QR.")
    print("      <C, mu>     preserves chi(x-y)")
    print("      <sigma, mu> destroys it")
    print("    <C,mu> is still TRANSITIVE, so no nonconstant point function")
    print("    survives -- T338's rank test returns 1 here too.  The invariant")
    print(f"    is a PAIR function: it reaches {len(reach)} of 1332 ordered")
    print("    pairs, exactly half.\n")
    print("    T338's 'no joint taxonomy' was right for sigma and mu and does")
    print("    NOT generalise. Swap sigma for C and an invariant appears.\n")
    print("  666 HERE IS ONE FORMULA, NOT A SIGHTING")
    print(f"    |<C,mu>| = |QR| x p = 18 x 37 = {len(Gc)}")
    print(f"    sum(1..36) = p(p-1)/2      = {sum(range(1,P))}")
    print("    both are ((p-1)/2) x p.")


if __name__ == "__main__":
    run()
