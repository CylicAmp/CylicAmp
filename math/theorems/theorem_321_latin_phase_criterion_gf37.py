# CLASS: THEOREM
"""
Theorem 321: phase-Latin <=> all row sums equal <=> all row sums 15
Author: Michael Warren Song (CyclicAmp)

Resolves the Latin-square structure of T319's lift grids and unifies three
conditions that looked independent.

=== THE TWO COORDINATE ARRAYS ===

    Every digit is a pair (orbit, phase) under 1..9 = Z_3 x Z_3:

        orbit(d) = (d-1) mod 3      phase(d) = (d-1) div 3
        orbit A {1,4,7}   B {2,5,8}   C {3,6,9}
        phase 0 {1,2,3}   1 {4,5,6}   2 {7,8,9}

    A 3x3 holding 1..9 once is a filling of all nine pairs. Whether the two
    coordinate arrays L_orb and L_ph are Latin is a separate question.

    For every lift grid:
        L_orb  columns CONSTANT (each column is one whole orbit) -> never
               column-Latin. Rows are always a permutation of A,B,C.
        L_ph   columns always a +1 cycle on Z_3 -> ALWAYS column-Latin.
               Rows are Latin exactly when the seed hits all three phases.

    So a lift is always row-Latin on orbits and column-Latin on phases, and it
    is never Graeco-Latin: L_orb has constant columns.

=== THE UNIFICATION ===

    For a lift grid these three are the SAME condition:

        (1) the seed is a phase-transversal (phases {0,1,2})
        (2) L_ph is a Latin square of order 3
        (3) all three row sums are equal

    and when they hold the common sum is 15. Verified with zero exceptions
    over all 162 valid seeds; 36 of them are phase-transversals and every one
    gives 15.

    MECHANISM. +3 sends v -> v+3 for v <= 6 and v -> v-6 for v >= 7. With k
    digits <= 6 the row sum changes by

        3k - 6(3-k) = 9k - 18

    which is zero exactly when k = 2, i.e. exactly ONE digit lies in {7,8,9}
    = phase 2. A phase-transversal has exactly one digit of each phase, and
    +3 cycles phases 0,1,2 -> 1,2,0, so the condition survives every step.

    Among the nine canonical seeds only 159 and 168 qualify. Their L_ph are
    the two reduced order-3 Latin squares, the cyclic table and its opposite.

=== CORRECTIONS RECORDED ===

    1. The row sums of the 189 grid are 18, 9, 18 -- not 18, 15, 12.
       189 -> 423 (sum 9) -> 756 (sum 18).

    2. Exactly ONE +3-orbit is a 15-line, namely {2,5,8}. The orbits sum to
       12, 15 and 18. A source claimed "two" and then named one; the
       conclusion drawn from it (Lo Shu has only one orbit-line, so a lift
       cannot be Lo Shu) is correct and unaffected.

    3. "A 15-triple that is also an orbit-transversal keeps sum 15 under the
       lift" is FALSE. Counterexample 456: a 15-triple, an orbit-transversal,
       and 456 -> 789 with sum 24. Its phases are 1,1,1. The criterion is
       PHASE-transversal, not 15-triple-plus-orbit-transversal.

=== VERIFIED AS STATED ===

    The eight 3-subsets of 1..9 summing to 15 are exactly the eight lines of
    the Lo Shu square -- checked by direct comparison.

        159 168 249 258 267 348 357 456

    A lift needs three parallel orbit-columns and Lo Shu contains only one
    orbit-line, so no lift grid is Lo Shu. Row-magic, never magic: the columns
    are the x = c class and sum 12, 15, 18 (T320).

=== FALSIFICATION ===
    Any assert below failing.
"""

from itertools import combinations, permutations

orbit = lambda d: (d - 1) % 3
phase = lambda d: (d - 1) // 3


def adv(v, k):
    return ((v - 1 + k) % 9) + 1


def lift(seed):
    return [tuple(adv(v, 3 * t) for v in seed) for t in range(3)]


def covers(g):
    return sorted(d for r in g for d in r) == list(range(1, 10))


def latin(sq):
    n = len(sq)
    return (all(len(set(r)) == n for r in sq)
            and all(len({sq[r][c] for r in range(n)}) == n for c in range(n)))


def run():
    good = [p for p in permutations(range(1, 10), 3) if covers(lift(p))]
    assert len(good) == 162

    # --- L_orb / L_ph shape, every lift ---
    for p in good:
        g = lift(p)
        Lo = [[orbit(d) for d in r] for r in g]
        Lp = [[phase(d) for d in r] for r in g]
        for c in range(3):
            assert len({Lo[r][c] for r in range(3)}) == 1     # orbit col constant
            assert len({Lp[r][c] for r in range(3)}) == 3     # phase col Latin
        for r in range(3):
            assert len(set(Lo[r])) == 3                        # orbit row Latin
        assert not latin(Lo)                                   # never Latin
        assert latin(Lp) == (sorted(phase(d) for d in p) == [0, 1, 2])

    # --- THE UNIFICATION, zero exceptions ---
    for p in good:
        g = lift(p)
        pt = sorted(phase(d) for d in p) == [0, 1, 2]
        lp = latin([[phase(d) for d in r] for r in g])
        eq = len({sum(r) for r in g}) == 1
        assert pt == lp == eq, p
        if pt:
            assert {sum(r) for r in g} == {15}
    pts = [p for p in good if sorted(phase(d) for d in p) == [0, 1, 2]]
    assert len(pts) == 36

    # --- the 9k - 18 mechanism ---
    for p in good:
        k = sum(1 for v in p if v <= 6)
        delta = sum(adv(v, 3) for v in p) - sum(p)
        assert delta == 9 * k - 18, p
        assert (delta == 0) == (k == 2)
        assert (k == 2) == (sum(1 for v in p if phase(v) == 2) == 1)

    # --- correction 1: the 189 grid ---
    g189 = lift((1, 8, 9))
    assert [tuple(r) for r in g189] == [(1, 8, 9), (4, 2, 3), (7, 5, 6)]
    assert [sum(r) for r in g189] == [18, 9, 18] != [18, 15, 12]

    # --- correction 2: exactly one orbit is a 15-line ---
    ORBS = [{1, 4, 7}, {2, 5, 8}, {3, 6, 9}]
    assert sorted(sum(o) for o in ORBS) == [12, 15, 18]
    assert [sorted(o) for o in ORBS if sum(o) == 15] == [[2, 5, 8]]
    assert len([o for o in ORBS if sum(o) == 15]) == 1

    # --- correction 3: 456 is the counterexample ---
    assert sum((4, 5, 6)) == 15
    assert len({orbit(d) for d in (4, 5, 6)}) == 3          # orbit-transversal
    assert sorted(phase(d) for d in (4, 5, 6)) == [1, 1, 1]  # NOT phase-transversal
    assert [tuple(r) for r in lift((4, 5, 6))][1] == (7, 8, 9)
    assert sum((7, 8, 9)) == 24 != 15

    # --- the 15-subsets are the Lo Shu lines ---
    S15 = sorted(sorted(c) for c in combinations(range(1, 10), 3) if sum(c) == 15)
    assert len(S15) == 8
    LO = [[4, 9, 2], [3, 5, 7], [8, 1, 6]]
    ls = [sorted(r) for r in LO]
    ls += [sorted(LO[r][c] for r in range(3)) for c in range(3)]
    ls += [sorted(LO[i][i] for i in range(3)),
           sorted(LO[i][2 - i] for i in range(3))]
    assert sorted(ls) == S15

    print("All assertions passed.\n")
    print("THE UNIFICATION — three conditions, one criterion")
    print(f"  {'seed':>5} {'phases':>10} {'L_ph Latin':>11} {'row sums':>15} {'equal':>7}")
    seen, grids = set(), []
    for p in sorted({tuple(sorted(x)) for x in {frozenset(q) for q in good}}):
        k = frozenset(frozenset(r) for r in lift(p))
        if k in seen:
            continue
        seen.add(k)
        grids.append(lift(p))
    for g in grids:
        s = g[0]
        print(f"  {''.join(map(str,s)):>5} {str([phase(d) for d in s]):>10} "
              f"{str(latin([[phase(d) for d in r] for r in g])):>11} "
              f"{str([sum(r) for r in g]):>15} "
              f"{str(len({sum(r) for r in g})==1):>7}")
    print(f"\n  162 valid seeds, 0 exceptions. 36 are phase-transversals,")
    print(f"  and all 36 give row sums 15.\n")
    print("MECHANISM:  +3 changes a row sum by 9k - 18, k = #digits <= 6")
    for c in ((1, 5, 9), (4, 5, 6), (2, 5, 8)):
        k = sum(1 for v in c if v <= 6)
        print(f"  {''.join(map(str,c))}: k={k}  change {9*k-18:+}   "
              f"{sum(c)} -> {sum(adv(v,3) for v in c)}")
    print("\n  456 is a 15-triple AND an orbit-transversal, yet fails:")
    print("  its phases are 1,1,1. The criterion is PHASE, not sum.")


if __name__ == "__main__":
    run()
