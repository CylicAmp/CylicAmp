# CLASS: THEOREM
"""
Theorem 322: the lift criterion, stated once
Author: Michael Warren Song (CyclicAmp)

Compresses T319-T321 into a single statement with explicit hypotheses.

=== SETUP ===

    Identify 1..9 with Z_3 x Z_3 by

        d  <->  (w(d), f(d)),     w(d) = (d-1) mod 3      "orbit"
                                  f(d) = (d-1) div 3      "phase"
        d = 1 + w + 3f

    For a seed s = (s_0, s_1, s_2) of distinct digits let G(s) be the lift:
    row t is (s_0+3t, s_1+3t, s_2+3t) on the 9-cycle. Then

        w(s_j + 3t) = w(s_j)              orbit is INVARIANT
        f(s_j + 3t) = f(s_j) + t          phase SHIFTS by t

    so immediately

        L_orb[t][j] = w(s_j)              independent of t
        L_ph [t][j] = f(s_j) + t          column j is a full Z_3 cycle

=== THEOREM ===

    Let s have distinct digits and write w = w o s, f = f o s in S_3-notation.

    (a) COVERING.  G(s) is a bijection onto {1..9}  <=>  w is injective.

    (b) ORBIT ARRAY.  Under (a), L_orb = (p; p; p) with p = w, the same row
        three times. Hence every column is constant and L_orb is NEVER Latin,
        for any seed. Its cyclic class sgn(p) in {+1,-1} is the orientation:
        ABC ~ BCA ~ CAB (even) and ACB ~ CBA ~ BAC (odd).

    (c) PHASE ARRAY.  L_ph is column-Latin for EVERY seed, since column j is
        { f(s_j) + t : t in Z_3 } = Z_3. The column condition is automatic;
        only the row condition can fail.

    (d) CRITERION.  Under (a), the following are equivalent:
            (i)   f is injective          (the seed is a phase-transversal)
            (ii)  L_ph is a Latin square
            (iii) the three row sums are equal
            (iv)  every row sum equals 15

        PROOF of (iii)<=>(i). Under (a), sum(w) = 0+1+2 = 3, so

            row_t = SUM_j [ 1 + w_j + 3((f_j + t) mod 3) ]
                  = 3 + 3 + 3 * SUM_j ((f_j + t) mod 3)
                  = 6 + 3 * SUM_j ((f_j + t) mod 3).

        If f is injective the inner sum is 0+1+2 = 3 for every t, so every
        row is 6 + 9 = 15. If not, two phases coincide and the multiset
        {f_j + t} changes with t, so the sum does.

    (e) ORIENTATIONS ARE INDEPENDENT.  Over the 36 phase-transversal seeds,
        all four combinations of (sgn w, sgn f) occur, 9 seeds each.

    (f) THE CANONICAL CONVENTION FIXES ONE OF THEM.  Increasing seeds through
        1 force f = (0,1,2), so the canonical pair exhibits both ORBIT
        orientations at a single phase orientation:

            159 -> w = ABC (even),  168 -> w = ACB (odd),  both f = 012.

        The 2x2 of (e) is invisible in the canonical nine.

=== WHAT IS AND IS NOT AVAILABLE ===

    Latin on phases: yes, exactly under (d), and then L_ph is one of the two
    reduced order-3 Latin squares.
    Latin on orbits: never, by (b).
    Graeco-Latin: never, since (b) makes L_orb degenerate.
    Magic: never -- the columns are the x=c parallel class of AG(2,3) and sum
    to 12, 15, 18 (T320). Row-magic 15 is the most that (d) delivers.

=== FALSIFICATION ===
    Any assert below failing.
"""

from itertools import permutations

w = lambda d: (d - 1) % 3
f = lambda d: (d - 1) // 3


def adv(v, k):
    return ((v - 1 + k) % 9) + 1


def lift(s):
    return [tuple(adv(v, 3 * t) for v in s) for t in range(3)]


def covers(g):
    return sorted(d for r in g for d in r) == list(range(1, 10))


def latin(sq):
    n = len(sq)
    return (all(len(set(r)) == n for r in sq)
            and all(len({sq[r][c] for r in range(n)}) == n for c in range(n)))


def sgn(p):
    return (-1) ** sum(1 for i in range(3) for j in range(i + 1, 3) if p[i] > p[j])


def run():
    ALL = list(permutations(range(1, 10), 3))

    # --- the coordinate identity ---
    for d in range(1, 10):
        assert d == 1 + w(d) + 3 * f(d)
    for d in range(1, 10):
        for t in range(3):
            assert w(adv(d, 3 * t)) == w(d)                 # orbit invariant
            assert f(adv(d, 3 * t)) == (f(d) + t) % 3       # phase shifts

    # --- (a) covering iff w injective ---
    for s in ALL:
        assert covers(lift(s)) == (len({w(d) for d in s}) == 3), s
    good = [s for s in ALL if covers(lift(s))]
    assert len(good) == 162

    for s in good:
        g = lift(s)
        Lo = [[w(d) for d in r] for r in g]
        Lp = [[f(d) for d in r] for r in g]
        p = tuple(w(d) for d in s)

        # --- (b) L_orb is p repeated; never Latin ---
        assert Lo == [list(p)] * 3
        assert all(len({Lo[t][j] for t in range(3)}) == 1 for j in range(3))
        assert not latin(Lo)

        # --- (c) L_ph always column-Latin ---
        assert all({Lp[t][j] for t in range(3)} == {0, 1, 2} for j in range(3))

        # --- (d) the four-way equivalence ---
        i_  = len({f(d) for d in s}) == 3
        ii  = latin(Lp)
        iii = len({sum(r) for r in g}) == 1
        iv  = {sum(r) for r in g} == {15}
        assert i_ == ii == iii == iv, s

        # --- the closed form for a row sum ---
        for t in range(3):
            assert sum(g[t]) == 6 + 3 * sum((f(d) + t) % 3 for d in s)

    # --- (e) orientations independent over the 36 ---
    pt = [s for s in good if len({f(d) for d in s}) == 3]
    assert len(pt) == 36
    from collections import Counter
    c = Counter((sgn(tuple(w(d) for d in s)), sgn(tuple(f(d) for d in s)))
                for s in pt)
    assert set(c) == {(1, 1), (1, -1), (-1, 1), (-1, -1)}
    assert set(c.values()) == {9}

    # --- (f) the canonical convention pins the phase orientation ---
    seen, canon = set(), []
    for s in sorted({tuple(sorted(x)) for x in {frozenset(q) for q in good}}):
        k = frozenset(frozenset(r) for r in lift(s))
        if k in seen:
            continue
        seen.add(k)
        canon.append(s)
    assert len(canon) == 9
    cl = [s for s in canon if len({f(d) for d in s}) == 3]
    assert cl == [(1, 5, 9), (1, 6, 8)]
    for s in cl:
        assert tuple(f(d) for d in s) == (0, 1, 2)          # phase order forced
    assert sgn(tuple(w(d) for d in (1, 5, 9))) == 1         # ABC even
    assert sgn(tuple(w(d) for d in (1, 6, 8))) == -1        # ACB odd

    print("All assertions passed.\n")
    print("THEOREM 322.  s a seed of distinct digits, G(s) its +3 lift,")
    print("              w = orbit word, f = phase word.\n")
    print("  (a)  G(s) covers 1..9        <=>  w injective")
    print("  (b)  L_orb = (p;p;p), p = w  =>   never Latin, columns constant")
    print("  (c)  L_ph column-Latin for EVERY seed  -- column condition free")
    print("  (d)  f injective <=> L_ph Latin <=> rows equal <=> every row 15")
    print("       via  row_t = 6 + 3 * SUM_j ((f_j + t) mod 3)")
    print("  (e)  over the 36 phase-transversal seeds, (sgn w, sgn f) hits all")
    print("       four combinations, 9 each -- the orientations are independent")
    print("  (f)  increasing-through-1 forces f = 012, so the canonical pair")
    print("       shows both orbit orientations only:")
    print("         159  w = ABC  even        168  w = ACB  odd\n")
    print("  never Latin on orbits, never Graeco-Latin, never magic.")
    print("  row-magic 15 is the most the construction yields.")


if __name__ == "__main__":
    run()
