# CLASS: THEOREM
"""
Theorem 319: the lift machine — a seed row forces its grid, and the lift
partitions 1..9 exactly when the seed meets each +3-orbit once
Author: Michael Warren Song (CyclicAmp)

=== THE MACHINE ===

    Digits live on the 9-cycle 1-2-...-9-1.  adv(v,k) = ((v-1+k) mod 9) + 1.

    SEED    R0 = (a, b, c)
    LIFT    R1 = R0 + 3,  R2 = R0 + 6      (digit-wise on the 9-cycle)

    The seed is the control: change R0 and every row below is rewritten.

    S_in   (x,y,z) -> (y,z,x)        circulate inside a row      order 3
    S_out  (R0,R1,R2) -> (R1,R2,R0)  circulate the rows          order 3
    M_in   (x,y,z) -> (z,y,x)        flip a row                  order 2
    M_out  (R0,R1,R2) -> (R2,R1,R0)  flip the stack              order 2

    S_in and S_out COMMUTE — verified on all 162 lift grids, zero failures.
    Inner spin and outer spin are independent.

=== WHEN DOES THE LIFT PARTITION 1..9? ===

    +3 preserves residue mod 3, so the 9-cycle splits into three +3-orbits:

        {1,4,7}      {2,5,8}      {3,6,9}

    The lift covers 1..9 exactly once  <=>  the seed takes ONE element from
    EACH orbit. Not "the seed must be a consecutive window" -- consecutive is
    sufficient, not necessary.

        27 valid seed-sets  ->  9 distinct grids

    The three step-3 grids from consecutive windows are three of the nine:

        123 456 789     126 459 378     129 345 678
        135 468 279     138 246 579     156 489 237
        159 348 267     168 249 357     189 234 567

    CORRECTION RECORDED. It was claimed that 156 cannot lift because
    "156+6 = 712 repeats a 1". The correct value is 156+6 = 723, and
    156/489/723 partitions 1..9 cleanly. The lift works for 156. What is true
    is the CONCLUSION it was offered for: the mix grid 156/234/789 is not a
    lift -- but because the lift lands on 489/723 instead, not because it
    fails.

=== +3 ON THE SEED IS S_out OF THE GRID ===

    Advancing the seed by one 3-step rotates the stack. Verified on all 162.
    So window-step and row-circulation are the same 9-cycle at two scales:

        digit inside a row   S_in    period 3
        seed / first row     +1      period 9
        whole row-block      S_out   period 3
        family               +3      period 3

    The nine consecutive-window columns are therefore three grids, each
    appearing three times under S_out: columns 1,4,7 are one grid; 2,5,8
    another; 3,6,9 the third.

=== THE PAIR LAYER IS NOT EXTRA DATA ===

    For seed (a,b,c):   singles  a b c
                        pairs L  ab ac ba
                        pairs R  bc ca cb

    S_in on the seed circulates the pair block with it: (a,b,c)->(b,c,a)
    sends ab->bc, ac->ba, ba->cb, and so on, so

        12 13 21 | 23 31 32   ->   23 21 32 | 31 12 13

    verified. After the lift, rows 2 and 3 inherit the same circulation
    automatically, since they are the seed advanced by 3 and 6.

=== SCOPE ===

    Machine 1 (this file) is closed on 1..9 and is what "the first row
    controls everything below" means. The mix-vs-789 construction is a
    different object: row 3 frozen, row 2 the leftover digits. It admits
    S_out but has no S_in unless a separate action is defined on the
    leftover row. The two are not the same machine and neither generates
    the other.

=== FALSIFICATION ===
    Any assert below failing.
"""

from itertools import permutations

N = 9


def adv(v, k):
    return ((v - 1 + k) % N) + 1


def lift(seed):
    return [tuple(adv(v, 3 * t) for v in seed) for t in range(3)]


def S_in(g):
    return [(r[1], r[2], r[0]) for r in g]


def S_out(g):
    return [g[1], g[2], g[0]]


def M_in(g):
    return [(r[2], r[1], r[0]) for r in g]


def M_out(g):
    return [g[2], g[1], g[0]]


def seed_adv(g, k):
    return lift(tuple(adv(v, k) for v in g[0]))


def covers(g):
    return sorted(d for r in g for d in r) == list(range(1, N + 1))


def orbit3(v):
    return {adv(v, 0), adv(v, 3), adv(v, 6)}


def order_of(f, g):
    k, h = 1, f(g)
    while h != g:
        h = f(h)
        k += 1
    return k


def pairs(r):
    a, b, c = r
    return [f"{a}{b}", f"{a}{c}", f"{b}{a}", f"{b}{c}", f"{c}{a}", f"{c}{b}"]


def run():
    G = lift((1, 2, 3))
    assert [tuple(r) for r in G] == [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
    assert covers(G)

    # --- the +3 orbits ---
    assert orbit3(1) == {1, 4, 7}
    assert orbit3(2) == {2, 5, 8}
    assert orbit3(3) == {3, 6, 9}
    assert {frozenset(orbit3(v)) for v in range(1, 10)} == \
           {frozenset({1, 4, 7}), frozenset({2, 5, 8}), frozenset({3, 6, 9})}

    # --- the covering criterion: one per orbit, iff ---
    good = [p for p in permutations(range(1, 10), 3) if covers(lift(p))]
    for p in permutations(range(1, 10), 3):
        one_each = len({frozenset(orbit3(v)) for v in p}) == 3
        assert covers(lift(p)) == one_each, p
    assert len(good) == 162
    assert len({frozenset(p) for p in good}) == 27 == 3 ** 3
    grids = {frozenset(frozenset(r) for r in lift(p)) for p in good}
    assert len(grids) == 9

    # --- 156 lifts; 156+6 is 723, not 712 ---
    assert tuple(adv(v, 3) for v in (1, 5, 6)) == (4, 8, 9)
    assert tuple(adv(v, 6) for v in (1, 5, 6)) == (7, 2, 3)
    assert covers(lift((1, 5, 6)))
    assert covers(lift((1, 2, 6)))
    # ... but the mix grid is a different object
    assert [tuple(r) for r in lift((1, 5, 6))] != [(1, 5, 6), (2, 3, 4), (7, 8, 9)]

    # --- group structure ---
    allg = [lift(p) for p in good]
    for g in allg:
        assert S_in(S_out(g)) == S_out(S_in(g)), g       # commute
        assert order_of(S_in, g) == 3
        assert order_of(S_out, g) == 3
        assert order_of(M_in, g) == 2
        assert order_of(M_out, g) == 2
        assert seed_adv(g, 3) == S_out(g)                # +3 == S_out
        assert seed_adv(g, 9) == g                       # +9 is identity
        assert covers(S_in(g)) and covers(S_out(g))
    # inner D3 has exactly 6 elements
    inner = {tuple(map(tuple, f(G))) for f in
             (lambda g: g, S_in, lambda g: S_in(S_in(g)), M_in,
              lambda g: S_in(M_in(g)), lambda g: M_in(S_in(g)))}
    assert len(inner) == 6

    # --- consecutive windows: 9 columns, 3 grids, each thrice ---
    wins = [tuple(adv(1 + j, i) for j in range(3)) for i in range(9)]
    cols = [lift(w) for w in wins]
    assert all(covers(c) for c in cols)
    assert len({frozenset(frozenset(r) for r in c) for c in cols}) == 3
    for i in range(9):
        assert cols[(i + 3) % 9] == S_out(cols[i]), i

    # --- pair layer circulates with S_in ---
    assert pairs((1, 2, 3)) == ["12", "13", "21", "23", "31", "32"]
    assert pairs((2, 3, 1)) == ["23", "21", "32", "31", "12", "13"]
    for p in good:
        assert set(pairs(p)) == set(pairs((p[1], p[2], p[0])))

    print("All assertions passed.\n")
    print("THE 9 LIFT GRIDS  (seed takes one digit from each +3-orbit)")
    shown = set()
    for p in sorted({tuple(sorted(x)) for x in {frozenset(q) for q in good}}):
        key = frozenset(frozenset(r) for r in lift(p))
        if key in shown:
            continue
        shown.add(key)
        rows = ["".join(map(str, r)) for r in lift(p)]
        tag = "   <- all consecutive windows" if rows == ["123", "456", "789"] else ""
        print(f"  {'  '.join(rows)}{tag}")
    print("\nSEED WALK — nine consecutive windows, three grids under S_out")
    for i in range(9):
        c = cols[i]
        print(f"  +{i}: " + "  ".join("".join(map(str, r)) for r in c))
    print("\nINNER D3 ON THE BASE STACK")
    obs = [[("".join(map(str, r))) for r in f(G)] for f in
           (lambda g: g, S_in, lambda g: S_in(S_in(g)), M_in,
            lambda g: S_in(M_in(g)), lambda g: M_in(S_in(g)))]
    for row in zip(*obs):
        print("   " + "   ".join(row))
    print("\nPAIR LAYER")
    for r in G:
        p = pairs(r)
        print(f"  {''.join(map(str,r))} | {' '.join(p[:3])} | {' '.join(p[3:])}")
    print("  after S_in:")
    for r in S_in(G):
        p = pairs(r)
        print(f"  {''.join(map(str,r))} | {' '.join(p[:3])} | {' '.join(p[3:])}")


if __name__ == "__main__":
    run()
