# CLASS: THEOREM
"""
The Phi_12 cut over F_37, and its collapse under T_33
Author: Michael Warren Song (CyclicAmp)

THEOREM 3.1 (complete factorization of Phi_12 over F_37)
    Phi_12(x) = x^4 - x^2 + 1 splits completely over F_37:
        Phi_12(x) = (x-8)(x-14)(x-23)(x-29)
    Proof route: substitute u = x^2, giving u^2-u+1=0, discriminant
    -3 = 34 = 16^2 mod 37, roots u in {27, 11} via 2^-1=19, then
    x^2=27 => x in {8,29} and x^2=11 => x in {14,23} (Lemma 2.2).
    The Phi_12 cut is {8,14,23,29}, verified directly as the full set
    of elements of order 12 in F_37^*.

THEOREM 3.2 (C_3 = mu_12, partitioned by order)
    C_3 = {x^3 : x in F_37^*} equals mu_12 (elements of order dividing 12),
    since ker(cubing) = mu_3 has order gcd(3,36)=3, so |C_3| = 36/3 = 12,
    and (x^3)^12 = 1 for all x, giving C_3 <= mu_12; equal cardinalities
    force equality. mu_12 partitions by order exactly as the classical
    cyclotomic root sets:
        ord 1:  {1}            (Phi_1)
        ord 2:  {36}           (Phi_2)
        ord 3:  {10, 26}       (Phi_3)
        ord 4:  {6, 31}        (Phi_4)
        ord 6:  {11, 27}       (Phi_6)
        ord 12: {8, 14, 23, 29} (Phi_12)
    1+1+2+2+2+4 = 12 = |C_3|.

THEOREM 4.1 (T_33 collapses the Phi_12 cut to two values)
    T_33(x) = x^3+33. For r of order 12, ord(r^3) = 12/gcd(3,12) = 4, so
    r^3 in Phi_4's root set {6,31} for every r in the cut -- forced by
    Lemma 2.1 and cyclic group order arithmetic, before any arithmetic
    is done. Direct evaluation:
        r= 8: r^3=31, T_33(r) = 31+33 = 27
        r=29: r^3= 6, T_33(r) =  6+33 =  2   (29 = -8 mod 37)
        r=14: r^3= 6, T_33(r) =  6+33 =  2
        r=23: r^3=31, T_33(r) = 31+33 = 27   (23 = -14 mod 37)
    T_33({8,14,23,29}) = {2, 27}: the 4-element cut lands on exactly
    2 values, 2-to-1 in both directions (8,23 -> 27; 14,29 -> 2).

THEOREM 4.2 (both images reach the T_33 6-cycle, at node 27)
    C_6 = (6 -> 27 -> 32 -> 19 -> 10 -> 34 -> 6) is T_33's unique cycle
    (cubic_shift_33_gf37.py). 27 in C_6 directly. The other image, 2, is
    NOT in C_6 and reaches it in exactly 3 steps:
        2 -> 4 -> 23 -> 27
    So the entire Phi_12 cut, all four order-12 elements, funnels into
    C_6 at the single node 27 -- two of them (8, 23) immediately, the
    other two (14, 29) after 2 lands there in 3 more steps.

FALSIFICATION
    Any assert below failing.
"""

P = 37


def order(a, p=P):
    a %= p
    x, k = a, 1
    while x != 1:
        x = x * a % p
        k += 1
    return k


def T33(x):
    return (pow(x, 3, P) + 33) % P


def run():
    # Theorem 3.1
    phi12_roots = sorted(x for x in range(1, P) if order(x) == 12)
    assert phi12_roots == [8, 14, 23, 29]

    disc = pow(16, 2, P)
    assert disc == (-3) % P
    inv2 = pow(2, -1, P)
    assert inv2 == 19
    u1, u2 = (17 * inv2) % P, ((-15) * inv2) % P
    assert {u1, u2} == {27, 11}
    assert sorted(x for x in range(P) if x * x % P == 27) == [8, 29]
    assert sorted(x for x in range(P) if x * x % P == 11) == [14, 23]

    # Theorem 3.2
    by_order = {d: sorted(x for x in range(1, P) if order(x) == d)
                for d in (1, 2, 3, 4, 6, 12)}
    assert by_order == {1: [1], 2: [36], 3: [10, 26], 4: [6, 31],
                         6: [11, 27], 12: [8, 14, 23, 29]}
    assert sum(len(v) for v in by_order.values()) == 12
    C3 = sorted({pow(x, 3, P) for x in range(1, P)})
    mu12 = sorted(x for x in range(1, P) if order(x) in (1, 2, 3, 4, 6, 12))
    assert C3 == mu12 == sorted(sum(by_order.values(), []))

    # Theorem 4.1
    images = {r: T33(r) for r in phi12_roots}
    assert images == {8: 27, 14: 2, 23: 27, 29: 2}
    assert set(images.values()) == {2, 27}

    # Theorem 4.2
    C6 = [6, 27, 32, 19, 10, 34]
    assert 27 in C6
    orbit = [2]
    while orbit[-1] not in C6:
        orbit.append(T33(orbit[-1]))
    assert orbit == [2, 4, 23, 27]

    print("All assertions passed.\n")
    print(f"Phi_12 cut = {phi12_roots}\n")
    print("Order partition of C_3 = mu_12:")
    for d, s in by_order.items():
        print(f"  order {d:2d}: {s}")
    print()
    print("T_33 on the Phi_12 cut:")
    for r, v in images.items():
        print(f"  r={r:2d}  r^3={pow(r,3,P):2d}  T_33(r)={v}")
    print(f"\n  T_33({{8,14,23,29}}) = {sorted(set(images.values()))}\n")
    print(f"27 in C_6 directly. Orbit of 2: {' -> '.join(map(str, orbit))}")


if __name__ == "__main__":
    run()
