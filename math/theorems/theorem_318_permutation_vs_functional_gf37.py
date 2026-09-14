# CLASS: THEOREM
"""
Theorem 318: two structures on one partition — the 3-cycles of x -> 26x are the
mu_3-cosets, and T(x) = x^3+33 acts on those blocks as a NON-bijection
Author: Michael Warren Song (CyclicAmp)

=== THE DISTINCTION ===

    Two different things in this repo are called "cycle". Only one of them is
    a permutation cycle type.

    PERMUTATION CYCLE TYPE belongs to a bijection. F_37* = C_36, and
    left-multiplication by a is a permutation whose cycle type is
    ord(a) repeated 36/ord(a) times:

        x -> 1x    ord 1     1^36
        x -> 26x   ord 3     3^12     <- these twelve 3-cycles ARE the cosets
        x -> 10x   ord 3     3^12        (26 and 10 are the two generators)
        x -> 3x    ord 18    18^2
        x -> 2x    ord 36    36^1     (2 is a primitive root)

    FUNCTIONAL-GRAPH CYCLE belongs to iterating a non-bijection. T's 6-cycle
    is an attractor of iteration, not a factor of a cycle index.

    T IS NOT A PERMUTATION: |T(F_37*)| = 12 < 36, and T restricted to the
    twelve shelves sends 12 points to 10 images, with in-degree 0 at shelves
    2 and 22.

    So do not write "T has cycle type 6". For T the correct statement is:
    one 6-cycle, two tails of quotient-length 3, in-degree 0 at 2 and 22.

=== THE POINT ===

    The twelve mu_3-cosets arise twice, from two different maps:

      as the CYCLES of the permutation x -> 26x        (cycle type 3^12)
      as the FIBRES of the non-bijection T(x) = x^3+33 (T constant on each)

    The 12-node quotient graph of T317 is therefore the permutation-cycle
    partition of x -> 26x, carrying a DIFFERENT map acting on those blocks.
    Two structures on the same partition, not one structure seen twice.

=== POWER MAPS ===

    x -> x^k is a permutation of F_37* iff gcd(k, 36) = 1, and then its cycle
    type is that of multiplication by k on the exponent group Z/36Z.

        k = 17   gcd 1    2^16 1^4    (almost an involution)
        k = 35   gcd 1    2^17 1^2    (x^35 = x^-1)
        k =  3   gcd 3    NOT a permutation, |image| = 12
        k =  2   gcd 2    NOT a permutation, |image| = 18

    The two non-permutations are exactly cubing and squaring, the maps the
    rest of this work is built on: cubing gives T's fibres, squaring gives the
    quadratic residues.

=== TRANSLATIONS AND AFFINE MAPS ON ALL OF F_37 ===

        x -> x + 33     a single 37-cycle, type 37^1
        x -> 26x + 33   a permutation, type 3^12 1^1, fixed point x = 12

    Neither is T. The shift 33 appearing in both x+33 and T(x) = x^3+33 is the
    same constant used in two unrelated ways; the translation's 37-cycle has
    nothing to do with T's 6-cycle. Recorded because the shared 33 invites the
    conflation.

    The affine map's fixed point solves 26x + 33 = x, i.e. 25x = 4, x = 12.

=== FALSIFICATION ===
    Any assert below failing.
"""

import math

P = 37
MU3 = {1, 10, 26}


def order(a, n=P):
    k, x = 1, a % n
    while x != 1:
        x = x * a % n
        k += 1
    return k


def cycle_type(perm, dom):
    seen, t = set(), {}
    for s in dom:
        if s in seen:
            continue
        c, y = 0, s
        while y not in seen:
            seen.add(y)
            y = perm(y)
            c += 1
        t[c] = t.get(c, 0) + 1
    return dict(sorted(t.items()))


def T(x):
    return (pow(x, 3, P) + 33) % P


def run():
    U = range(1, P)

    # --- multiplication maps are permutations; type is ord repeated ---
    for a in (1, 26, 10, 3, 2):
        o = order(a)
        assert cycle_type(lambda x, a=a: x * a % P, U) == {o: (P - 1) // o}, a
    assert order(26) == order(10) == 3
    assert order(3) == 18 and order(2) == 36
    assert cycle_type(lambda x: 26 * x % P, U) == {3: 12}
    assert cycle_type(lambda x: 3 * x % P, U) == {18: 2}
    assert cycle_type(lambda x: 2 * x % P, U) == {36: 1}

    # --- the 3-cycles of x -> 26x ARE the mu_3-cosets ---
    blocks = set()
    seen = set()
    for x in U:
        if x in seen:
            continue
        c = tuple(sorted({x, 26 * x % P, 26 * 26 * x % P}))
        seen.update(c)
        blocks.add(c)
    assert len(blocks) == 12
    for b in blocks:
        assert set(b) == {b[0] * m % P for m in MU3}
    # ... and they are exactly the fibres of T
    for b in blocks:
        assert len({T(x) for x in b}) == 1
    assert len({T(b[0]) for b in blocks}) == 12
    for x in U:
        for y in U:
            assert (T(x) == T(y)) == (x * pow(y, P - 2, P) % P in MU3)

    # --- T is NOT a permutation ---
    assert len({T(x) for x in U}) == 12 < 36
    I = sorted({T(x) for x in U})
    assert len({T(y) for y in I}) == 10 < 12
    assert sorted(set(I) - {T(y) for y in I}) == [2, 22]      # in-degree 0

    # --- power maps: permutation iff gcd(k,36)=1 ---
    for k in range(1, 36):
        isperm = len({pow(x, k, P) for x in U}) == 36
        assert isperm == (math.gcd(k, P - 1) == 1), k
    assert cycle_type(lambda x: pow(x, 17, P), U) == {1: 4, 2: 16}
    assert cycle_type(lambda x: pow(x, 35, P), U) == {1: 2, 2: 17}
    assert all(pow(x, 35, P) == pow(x, P - 2, P) for x in U)   # x^35 = x^-1
    assert len({pow(x, 3, P) for x in U}) == 12
    assert len({pow(x, 2, P) for x in U}) == 18
    assert math.gcd(3, 36) == 3 and math.gcd(2, 36) == 2
    # the power-map type equals mult-by-k on Z/36
    for k in (17, 35, 5, 7):
        a = cycle_type(lambda x, k=k: pow(x, k, P), U)
        b = cycle_type(lambda e, k=k: (e * k) % (P - 1), range(P - 1))
        assert a == b, k

    # --- translation and affine, on all 37 points ---
    assert cycle_type(lambda x: (x + 33) % P, range(P)) == {37: 1}
    assert cycle_type(lambda x: (26 * x + 33) % P, range(P)) == {1: 1, 3: 12}
    fixed = [x for x in range(P) if (26 * x + 33) % P == x]
    assert fixed == [12] and 25 * 12 % P == 4 == (-33) % P

    print("All assertions passed.\n")
    print("PERMUTATIONS on F_37*  (cycle type = ord(a) repeated 36/ord(a) times)")
    print(f"  {'map':<14} {'ord':>4}   cycle type")
    for a in (1, 26, 10, 3, 2):
        o = order(a)
        print(f"  x -> {a:>2}x{'':<7} {o:>4}   {o}^{(P-1)//o}")
    print("\n  the twelve 3-cycles of x -> 26x ARE the mu_3-cosets,")
    print("  and those same twelve blocks are the FIBRES of T.\n")
    print("POWER MAPS  (permutation iff gcd(k,36) = 1)")
    for k in (17, 35, 3, 2):
        if math.gcd(k, 36) == 1:
            t = cycle_type(lambda x, k=k: pow(x, k, P), U)
            print(f"  x -> x^{k:<3} gcd {math.gcd(k,36)}  permutation   "
                  + " ".join(f"{a}^{b}" for a, b in t.items()))
        else:
            print(f"  x -> x^{k:<3} gcd {math.gcd(k,36)}  NOT a permutation, "
                  f"|image| = {len({pow(x,k,P) for x in U})}")
    print("\nON ALL OF F_37")
    print(f"  x -> x + 33     37^1              a single 37-cycle")
    print(f"  x -> 26x + 33   1^1 3^12          fixed point x = {fixed[0]}")
    print(f"  neither is T. the shared 33 is the same constant used two ways.\n")
    print("T IS A FUNCTIONAL GRAPH, NOT A PERMUTATION")
    print(f"  |T(F_37*)| = {len({T(x) for x in U})} < 36     "
          f"|T(I)| = {len({T(y) for y in I})} of {len(I)} shelves")
    print(f"  in-degree 0 at shelves {sorted(set(I)-{T(y) for y in I})}")
    print("  correct phrasing: one 6-cycle, two tails of quotient-length 3.")
    print("  NOT 'cycle type 6' -- cycle type is for bijections.")


if __name__ == "__main__":
    run()
