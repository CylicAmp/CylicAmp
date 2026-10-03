# CLASS: THEOREM
"""
Theorem 355: the conjugate C o T o C^-1 completes the series, and the
Layer III d=7 intersection is forced by counting
Author: Michael Warren Song (CyclicAmp)

Third and last of the trajectory series (T353 f_a, T354 f_b), plus an
assessment of a supplied Layer III encoding.

=== THE CONJUGATE ===

    T : 18 -> [19 -> 10 -> 34 ->  6 -> 27 -> 32] -> 19 -> ...
    CJ: 18 -> [21 -> 31 -> 29 -> 19 ->  8 -> 23] -> 21 -> ...

    where CJ = C o T o C^-1.  PREPERIOD 1 INTO A 6-CYCLE, for both.

    Same mechanism as T354.  C^-1(18) = 18 because 18 is C's unique fixed
    point, so CJ^n(18) = C(T^n(C^-1(18))) = C(T^n(18)) and the orbit is T's
    pushed through C term by term.  Verified over thirteen terms, with

        C{19, 10, 34, 6, 27, 32} = {21, 31, 29, 19, 8, 23}

    Globally both maps have cycle lengths 6 on all 37 states -- a single
    6-cycle with tails, max preperiod 4 -- as T349 recorded.

=== THE SERIES, COMPLETE ===

        map        preperiod   cycle              global type
        T              1       (19,10,34,6,27,32)  one 6-cycle
        CJ = CTC^-1    1       C of the above      one 6-cycle
        f_a = T o C    5       (10, 2, 6)          3-cycle + fixed 27
        f_b = C o T    5       C of the above      3-cycle + fixed 8

    Two conjugacy classes, and within each class the orbit of 18 is
    literally the same sequence in C-coordinates.  18 is the only seed for
    which that is visible from the first term, because C fixes it.

    So of the four trajectories, exactly ONE carries information: T's.
    The other three are determined by it.

=== THE LAYER III ENCODING, ASSESSED ===

    E(N) = 10L + d for the repdigit of digit d and length L.  The L = 3
    column encodes to 31..39.

    WHAT IS TRUE.  Every entry of the L = 3 column vanishes in Layer II,
    because ddd = d x 111 and 111 = 3 x 37.  That holds for all nine d.
    And exactly one entry also vanishes in Layer III: d = 7, where
    E(777) = 37 == 0.  The arithmetic is right.

    WHAT IT IS WORTH.  Forced, by counting.  E over the L = 3 column runs
    through the NINE CONSECUTIVE INTEGERS 31, 32, ..., 39, and a run of
    nine consecutive integers contains exactly one multiple of 37 whenever
    it straddles one.  Nothing selects d = 7 beyond the fact that
    10(3) + 7 = 37.  Calling it "an exact algebraic coincidence between
    two representation layers" overstates it: one layer vanishes
    identically down the column, the other vanishes once because the
    encoding is an arithmetic progression of step 1 crossing the modulus.

    THE MOD-9 CLAIM IS ALSO RIGHT AND ALSO DEFINITIONAL.  10 == 1 (mod 9)
    gives E == L + d, so at L = 3 the encoding is a +3 shift.  And {3,6,9}
    is closed under +3 because it is the ideal (3) in Z/9Z, which T137 and
    T347 already record.  Closure under +3 is the statement that (3) is a
    subgroup of order 3 -- true, and not a property of the encoding.

=== FALSIFICATION ===
    CJ^n(18) != C(T^n(18)) for some n; or a second d in 1..9 with
    10(3) + d == 0 (mod 37).
"""

P = 37
T = lambda x: (pow(x, 3, P) + 33) % P
C = lambda x: (3 * x + 1) % P
Ci = lambda y: (25 * (y - 1)) % P
CJ = lambda x: C(T(Ci(x)))
FA = lambda x: T(C(x))
FB = lambda x: C(T(x))
E = lambda L, d: 10 * L + d


def orbit(f, x, n=12):
    o = [x]
    for _ in range(n):
        o.append(f(o[-1]))
    return o


def prep_cycle(o):
    idx = {}
    for i, v in enumerate(o):
        if v in idx:
            return idx[v], o[idx[v]:i]
        idx[v] = i


def census(f):
    info = {}
    for x in range(P):
        o = orbit(f, x, 40)
        seen = {}
        for i, v in enumerate(o):
            if v in seen:
                info[x] = (seen[v], i - seen[v], tuple(sorted(o[seen[v]:i])))
                break
            seen[v] = i
    return info


def run():
    from collections import Counter

    # --- the conjugate orbit ---
    oT, oJ = orbit(T, 18), orbit(CJ, 18)
    assert oT == [18, 19, 10, 34, 6, 27, 32, 19, 10, 34, 6, 27, 32]
    assert oJ == [18, 21, 31, 29, 19, 8, 23, 21, 31, 29, 19, 8, 23]
    assert [C(x) for x in oT] == oJ
    pt, ct = prep_cycle(oT)
    pj, cj = prep_cycle(oJ)
    assert (pt, pj) == (1, 1)
    assert ct == [19, 10, 34, 6, 27, 32]
    assert cj == [21, 31, 29, 19, 8, 23]
    assert [C(x) for x in ct] == cj

    # --- 18 is why the orbits align from term zero ---
    assert C(18) == 18 == Ci(18)
    assert [x for x in range(P) if C(x) == x] == [18]
    for n in range(1, 15):
        a = b = 18
        for _ in range(n):
            a = T(a)
            b = CJ(b)
        assert b == C(a)

    # --- global types ---
    iT, iJ = census(T), census(CJ)
    assert dict(Counter(v[1] for v in iT.values())) == {6: 37}
    assert dict(Counter(v[1] for v in iJ.values())) == {6: 37}
    assert max(v[0] for v in iT.values()) == 4
    assert max(v[0] for v in iJ.values()) == 4
    iA, iB = census(FA), census(FB)
    assert dict(Counter(v[1] for v in iA.values())) == {3: 31, 1: 6}
    assert dict(Counter(v[1] for v in iB.values())) == {3: 31, 1: 6}
    assert prep_cycle(orbit(FA, 18))[0] == 5
    assert prep_cycle(orbit(FB, 18))[0] == 5

    # --- Layer III ---
    col = [(d, int(str(d) * 3), E(3, d)) for d in range(1, 10)]
    assert [e for _, _, e in col] == list(range(31, 40))
    for d, n, e in col:
        assert n == d * 111 and n % P == 0          # whole column vanishes
    zeros = [d for d, _, e in col if e % P == 0]
    assert zeros == [7]
    assert E(3, 7) == 37
    # forced: nine consecutive integers contain at most one multiple of 37
    assert len([e for e in range(31, 40) if e % P == 0]) == 1
    assert 111 == 3 * P
    # mod 9
    assert 10 % 9 == 1
    for L in range(1, 5):
        for d in range(1, 10):
            assert E(L, d) % 9 == (L + d) % 9
    shift = {x: (x + 3 - 1) % 9 + 1 for x in (3, 6, 9)}
    assert set(shift.values()) == {3, 6, 9}
    assert shift == {3: 6, 6: 9, 9: 3}

    print("All assertions passed.\n")
    print("THEOREM 355.  The conjugate, and the Layer III assessment.\n")
    print(f"   T : 18 -> {ct}  -> ...")
    print(f"   CJ: 18 -> {cj}  -> ...")
    print(f"   both preperiod 1 into a 6-cycle, and C(cycle_T) = cycle_CJ\n")
    print("   C fixes 18, so CJ^n(18) = C(T^n(18)) -- same orbit, other")
    print("   coordinates. Checked to n = 14.\n")
    print("  THE SERIES, COMPLETE")
    print("   map          preperiod  cycle                 global")
    print("   T                1      (19,10,34,6,27,32)    one 6-cycle")
    print("   C T C^-1         1      C of the above        one 6-cycle")
    print("   f_a = T o C      5      (10, 2, 6)            3-cycle + fix 27")
    print("   f_b = C o T      5      C of the above        3-cycle + fix 8")
    print("   exactly ONE of the four carries information: T's.\n")
    print("  LAYER III,  E(N) = 10L + d")
    print("   TRUE: the whole L=3 column vanishes in Layer II, since")
    print("   ddd = d x 111 and 111 = 3 x 37 -- all nine d.")
    print(f"   TRUE: exactly one also vanishes in Layer III, d = {zeros[0]},")
    print(f"   where E(777) = {E(3,7)} == 0.")
    print("   FORCED: E runs over the nine CONSECUTIVE integers 31..39, and")
    print("   such a run contains exactly one multiple of 37. Nothing picks")
    print("   d = 7 beyond 10(3) + 7 = 37. 'Exact algebraic coincidence")
    print("   between two representation layers' overstates it.\n")
    print("   mod 9: 10 == 1 gives E == L + d, so L=3 is a +3 shift --")
    print(f"   and {{3,6,9}} is closed under +3 {shift} because it is the")
    print("   ideal (3) in Z/9Z, already in T137 and T347. Closure is a fact")
    print("   about the ideal, not about the encoding.")


if __name__ == "__main__":
    run()
