# CLASS: THEOREM
"""
Theorem 353: the orbit of 18 under f_a is preperiod 5 into a 3-cycle, not
preperiod 1 into a 7-cycle
Author: Michael Warren Song (CyclicAmp)

A supplied record stated, for f_a = T o C with T(x) = x^3 + 33 and
C(x) = 3x + 1 on GF(37):

    18 -> 19 -> 7 -> 25 -> 4 -> 10 -> 2 -> 6 -> 19
    "preperiod 1, followed by the 7-cycle (19, 7, 25, 4, 10, 2, 6)"

The first eight entries are right.  The ninth is not.

=== THE CORRECTION ===

        f_a(6) = 10,  not 19.

    C(6) = 19, and T(19) = 19^3 + 33 = 6859 + 33.  6859 == 14 (mod 37),
    so 14 + 33 = 47 == 10.

    The orbit is therefore

        18 -> 19 -> 7 -> 25 -> 4 -> [10 -> 2 -> 6] -> 10 -> 2 -> 6 -> ...
         |______ preperiod 5 ______|   3-cycle

    PREPERIOD 5 INTO THE 3-CYCLE (10, 2, 6).  The value 10 already occurs
    at position 5; the sequence returns to it rather than closing at 19.

=== WHY A 7-CYCLE WAS IMPOSSIBLE ===

    T349 established f_a's cycle type as [1, 3] by independent computation.
    Recomputed here over all 37 states:

        cycle lengths      3 (31 states),  1 (6 states)
        distinct cycles    (2, 6, 10) and the fixed point (27)
        basins             31 and 6
        max preperiod      5

    There is no 7-cycle to be had.  The claimed one came from closing the
    loop by hand at 6 -> 19.

=== WHAT THE SUPPLIED RECORD GOT RIGHT, AND THE REASON IT MATTERS ===

    The conjugacy was given as a one-line formal proof and needs no
    computation at all:

        C o f_a = C o (T o C) = (C o T) o C = f_b o C
        =>  f_b = C o f_a o C^-1

    That is better than the pointwise verification used in T349, which
    checked 37 values to establish something that follows from
    associativity.  Likewise C^-1(y) = 25(y - 1) is immediate from
    3 x 25 = 75 == 1 (mod 37).

    The distinction the record draws -- formal proof against computational
    verification -- is correct, and it is exactly what separates the three
    claims.  The conjugacy and the inverse are provable in a line and are
    right.  The trajectory is not that kind of statement; it is a
    computation, and it was the one item asserted without running.

=== FALSIFICATION ===
    f_a(6) != 10; or a cycle of f_a of length other than 1 or 3.
"""

P = 37
T = lambda x: (pow(x, 3, P) + 33) % P
C = lambda x: (3 * x + 1) % P
Ci = lambda y: (25 * (y - 1)) % P
FA = lambda x: T(C(x))
FB = lambda x: C(T(x))


def run():
    from collections import Counter

    # --- the single wrong step ---
    assert C(6) == 19
    assert 19 ** 3 == 6859 and 6859 % P == 14
    assert (14 + 33) % P == 10
    assert T(19) == 10
    assert FA(6) == 10 != 19

    # --- the corrected orbit ---
    orb = [18]
    for _ in range(12):
        orb.append(FA(orb[-1]))
    assert orb[:8] == [18, 19, 7, 25, 4, 10, 2, 6]      # supplied part, right
    assert orb[8] == 10                                  # the correction
    assert orb == [18, 19, 7, 25, 4, 10, 2, 6,
                   10, 2, 6, 10, 2]
    # preperiod and cycle
    idx, pre, cyc = {}, None, None
    for i, v in enumerate(orb):
        if v in idx:
            pre, cyc = idx[v], orb[idx[v]:i]
            break
        idx[v] = i
    assert pre == 5 and cyc == [10, 2, 6]

    # --- no 7-cycle exists ---
    info = {}
    for x in range(P):
        o, seen = [x], {}
        for _ in range(40):
            o.append(FA(o[-1]))
        for i, v in enumerate(o):
            if v in seen:
                info[x] = (seen[v], i - seen[v], tuple(sorted(o[seen[v]:i])))
                break
            seen[v] = i
    lens = Counter(v[1] for v in info.values())
    assert set(lens) == {1, 3} and lens[3] == 31 and lens[1] == 6
    assert {v[2] for v in info.values()} == {(2, 6, 10), (27,)}
    assert max(v[0] for v in info.values()) == 5
    assert 7 not in lens

    # --- the conjugacy, formally rather than pointwise ---
    assert (3 * 25) % P == 1                             # C^-1 coefficient
    assert all(C(Ci(y)) == y for y in range(P))
    # C o f_a = C o T o C = f_b o C, so f_b = C f_a C^-1
    assert all(C(FA(x)) == FB(C(x)) for x in range(P))   # the identity itself
    assert all(FB(x) == C(FA(Ci(x))) for x in range(P))  # rearranged

    print("All assertions passed.\n")
    print("THEOREM 353.  The trajectory closes one step too early.\n")
    print("   claimed  18 -> 19 -> 7 -> 25 -> 4 -> 10 -> 2 -> 6 -> 19")
    print("   actual   18 -> 19 -> 7 -> 25 -> 4 -> 10 -> 2 -> 6 -> 10\n")
    print(f"   f_a(6) = {FA(6)}: C(6) = {C(6)}, 19^3 = 6859 == 14,")
    print(f"   14 + 33 = 47 == {T(19)}.\n")
    print(f"   orbit: {orb[:9]} ...")
    print(f"   preperiod {pre}, then the 3-cycle {cyc}")
    print("   10 already occurs at position 5; the sequence returns to it.\n")
    print("  NO 7-CYCLE EXISTS")
    print(f"   cycle lengths over all 37 states: {dict(lens)}")
    print(f"   cycles: (2, 6, 10) and the fixed point (27)")
    print(f"   basins 31 and 6, max preperiod {max(v[0] for v in info.values())}")
    print("   consistent with T349's independently computed type [1, 3].\n")
    print("  WHAT WAS RIGHT, AND WHY THE DISTINCTION MATTERS")
    print("   C o f_a = C o (T o C) = (C o T) o C = f_b o C")
    print("   so f_b = C o f_a o C^-1 by associativity alone -- better than")
    print("   T349's 37-point check of the same thing.")
    print("   C^-1(y) = 25(y-1) is immediate from 3 x 25 = 75 == 1.")
    print("   Those two are provable in a line and are right. The trajectory")
    print("   is not that kind of statement, and it was the one item")
    print("   asserted without being run.")


if __name__ == "__main__":
    run()
