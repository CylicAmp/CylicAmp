# CLASS: THEOREM
"""
Theorem 313: n + 9 = rev(n) selects exactly the a-b = -1 diagonal
Author: Michael Warren Song (CyclicAmp)

=== THE RESULT ===

    Among the 90 two-digit numbers, n + 9 = rev(n) holds for exactly

        12, 23, 34, 45, 56, 67, 78, 89

    -- eight of ninety. And the solution set is not a list to be checked;
    it is forced:

        n = 10a + b,  rev(n) = 10b + a
        10a + b + 9 = 10b + a
             9a + 9 = 9b
                  b = a + 1                    i.e.  a - b = -1

    So "adding 9 reverses the number" and "the digits sit on the a-b = -1
    diagonal" are the same condition written two ways. The eight-element
    solution set is the diagonal, not a sample of it.

=== WHY THE TWO HALVES MUST BE SEPARATED ===

    The observation that prompted this (9 + 12 read as landing on 12) has
    two independent parts, one forced and one not:

    FORCED   dr(n + 9) = dr(n) for every n. 9 = 0 (mod 9), so adding it
             cannot move the digital root. Zero exceptions, n = 1..2999.
             This part carries no information -- it is true of every
             number, so it distinguishes nothing.

    NOT FORCED   n + 9 = rev(n) holds for 8 of 90. This is the part that
             selects. It is a decimal fact (it needs base 10's 10a + b),
             not a modular one.

    Both are true of 12. Only the second one says anything about 12.

=== WHAT THE EIGHT CARRY ===

    Digital roots run 3,5,7,9,2,4,6,8 -- every root except 1, each once.
    The missing root is 1, because a = 0 is not a two-digit number: the
    diagonal's first rung 01 is excluded by the leading digit, and dr(01)
    would have been 1. The gap is a notation artifact, recorded as such.

    GF(37) orbits are scattered across the taxonomy (SA_ST_A, TESLA, D7,
    TESLA, CAS_EXT, C3, C3, DARK_A) with no clustering. Expected: the
    selecting condition is base-10, and mod 37 does not see it.

    Sums n + rev(n) = 11(a + b) = 11(2a + 1), always odd x 11.
    Differences rev(n) - n = 9 by construction -- the theorem restated.

=== THE 12/21 PAIR SPECIFICALLY ===

    12 mod 37 = 12 (SA_ST_A), 21 mod 37 = 21 (SA_ST_B).
    12 + 21 = 33, NOT 37: they are NOT additive antipodes. The antipode
    of 12 is 25 and of 21 is 16. Recorded because 33 is a live constant
    elsewhere in this repo (T268's shift, the birthday->Easter gap) and
    the coincidence of the number invites a false reading here.

    What IS true: 12 and 21 both lie in the sovereign target set
    ST = {3,12,21,30}. That is why they share dr 3 -- ST is defined as
    the DR=3 residues, so this is the definition, not a find.

=== THE SUM LADDER 33, 55, 77, 99, ... ===

    n + rev(n) = 11(2a + 1) runs 33, 55, 77, 99, 121, 143, 165, 187 down
    the diagonal -- 11 times the odd numbers. Two of those are live
    constants in this repo, and both are FORCED here, not found:

      33 is the a=1 rung (11 x 3). 33 is T268's shift constant and the
         birthday->Easter gap. Same number, different derivation -- here
         it is 11 x 3 because a = 1 is the diagonal's first admissible
         rung. No mechanism connects the two occurrences.

      55 is the a=2 rung (11 x 5). 55 = T_10 and has recurred through
         this session's pair work. Again forced by the ladder.

    Recorded as a rung index, not as evidence. Anything of the form
    11 x odd will appear on this ladder somewhere; hitting 33 and 55 is
    guaranteed by the ladder existing, not by those constants mattering.

=== THE ZERO TALLY (protocol 12) ===

    0 -> 1, 00 -> 3: the triangular ladder T_k = k(k+1)/2 counted on the
    number of zeros. T_1 = 1, T_2 = 3, T_3 = 6, ... and T_6 = 21, which
    is the output of line one. The two lines meet at 3 (dr of 12 and 21;
    T_2) and again at 21 (the sum; T_6). Both meetings are recorded as
    arithmetic coincidences between two small sequences, not as a
    mechanism -- small integers collide often, and there is no derivation
    linking the triangular ladder to the reversal diagonal.

=== FALSIFICATION ===
    Any assert below failing.
"""

P = 37


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


def tri(k):
    return k * (k + 1) // 2


def rev(n):
    return int(str(n)[::-1])


DIAG = [12, 23, 34, 45, 56, 67, 78, 89]


def run():
    # --- the result ---
    hits = [n for n in range(10, 100) if n + 9 == rev(n)]
    assert hits == DIAG
    assert len(hits) == 8

    # --- the derivation, checked against the brute force ---
    for n in range(10, 100):
        a, b = n // 10, n % 10
        assert (n + 9 == rev(n)) == (b == a + 1)
        assert (n + 9 == rev(n)) == (a - b == -1)
    assert [n // 10 for n in DIAG] == list(range(1, 9))
    assert [n % 10 for n in DIAG] == list(range(2, 10))

    # --- forced half: adding 9 never moves the digital root ---
    assert not [n for n in range(1, 3000) if dr(n + 9) != dr(n)]
    assert 9 % 9 == 0

    # --- not-forced half: only 8 of 90 ---
    assert len([n for n in range(10, 100)]) == 90
    assert len(hits) * 90 == 8 * 90     # 8/90, stated as a ratio not a rate

    # --- the eight digital roots: all but 1, each once ---
    roots = [dr(n) for n in DIAG]
    assert roots == [3, 5, 7, 9, 2, 4, 6, 8]
    assert sorted(roots) == [2, 3, 4, 5, 6, 7, 8, 9]
    assert 1 not in roots
    # the missing rung is 01, excluded by the leading digit
    assert 1 + 9 == 10 and rev(10) == 1 and 1 + 9 != rev(1)

    # --- sums and differences ---
    for n in DIAG:
        a, b = n // 10, n % 10
        assert n + rev(n) == 11 * (a + b) == 11 * (2 * a + 1)
        assert rev(n) - n == 9
    assert [(n + rev(n)) // 11 for n in DIAG] == [3, 5, 7, 9, 11, 13, 15, 17]
    sums = [n + rev(n) for n in DIAG]
    assert sums == [33, 55, 77, 99, 121, 143, 165, 187]
    assert sums == [11 * (2 * a + 1) for a in range(1, 9)]
    assert sums[0] == 33 and sums[1] == 55        # both forced by the ladder
    assert tri(10) == 55

    # --- 12 and 21: NOT antipodes ---
    assert 12 + 21 == 33 != P
    assert (P - 12, P - 21) == (25, 16)
    ST = {3, 12, 21, 30}
    assert 12 in ST and 21 in ST
    assert all(dr(t) == 3 for t in ST)          # ST is the DR=3 set, by definition
    assert dr(12) == dr(21) == 3
    assert rev(12) == 21 and 12 + 9 == 21

    # --- the zero tally ---
    assert tri(1) == 1 and tri(2) == 3
    assert [tri(k) for k in range(1, 7)] == [1, 3, 6, 10, 15, 21]
    assert tri(6) == 21 == 12 + 9               # the two lines meet at 21
    assert tri(2) == 3 == dr(12) == dr(21)      # and at 3

    print("All assertions passed.\n")
    print("n + 9 = rev(n)  ON TWO DIGITS")
    print(f"  {'n':>4} {'a':>2} {'b':>2} {'rev':>4} {'dr':>3} {'mod37':>6} "
          f"{'n+rev':>6}")
    for n in DIAG:
        a, b = n // 10, n % 10
        print(f"  {n:>4} {a:>2} {b:>2} {rev(n):>4} {dr(n):>3} {n % P:>6} "
              f"{n + rev(n):>6}")
    print(f"\n  {len(DIAG)} of 90. condition b = a+1, i.e. a-b = -1.")
    print(f"  roots {[dr(n) for n in DIAG]} -- every root but 1, each once.")
    print(f"  the missing rung is 01, excluded by the leading digit.\n")

    print("SUM LADDER  n + rev(n) = 11(2a+1)")
    print(f"  {[n + rev(n) for n in DIAG]}")
    print("  33 (a=1) and 55 (a=2) are rungs of this ladder -- forced by")
    print("  11 x odd, not evidence for those constants elsewhere.\n")

    print("THE TWO HALVES")
    print("  forced     dr(n+9) = dr(n) for all n -- 0 exceptions in 2999.")
    print("             says nothing about 12 in particular.")
    print("  selecting  n+9 = rev(n) for 8 of 90 -- a base-10 condition.")
    print("             this is the half that picks out the diagonal.\n")

    print("12 AND 21")
    print(f"  12 + 21 = {12 + 21}, not 37 -- NOT antipodes.")
    print(f"  antipodes are {P - 12} and {P - 21}.")
    print(f"  both in ST = {{3,12,21,30}}, which is the DR=3 set by")
    print(f"  definition -- so the shared dr 3 is definitional.\n")

    print("ZERO TALLY (protocol 12)")
    print(f"  0 -> T_1 = {tri(1)}    00 -> T_2 = {tri(2)}")
    print(f"  ladder {[tri(k) for k in range(1, 7)]}")
    print(f"  meets line one at 3 (T_2 = dr 12 = dr 21)")
    print(f"  and at 21 (T_6 = 12 + 9). coincidence, not mechanism.")


if __name__ == "__main__":
    run()
