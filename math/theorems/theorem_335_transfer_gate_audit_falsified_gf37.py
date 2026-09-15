# CLASS: THEOREM
"""
Theorem 335: auditing the T333 transfer gate -- row 5 is falsified for
parameter-free rules and the gate itself is under-constrained
Author: Michael Warren Song (CyclicAmp)

Instructed: audit the Tier-2 -> Tier-3 transfer before extending anything.
Done.  The verdict is step 5 of the proposed procedure -- mark it, do not
extend the framework.

=== A CONSTRAINT DISCREPANCY, SETTLED FIRST ===

    The proposal states R(1) == 12 and R(2) == 33.  T333 registered
    R(d=1 stack) == 35 and R(d=2 stack) == 33.  These differ because
    12 is a ROAD residue and 33 is a STACK-SUM residue:

        road residues   d=1 -> 12    d=2 -> 24
        stack sums      d=1 -> 35    d=2 -> 33

    (12, 33) mixes the two levels.  The consistent pairs are (12,24) or
    (35,33).  This audit uses the REGISTERED pair (35,33); adopting (12,33)
    after the fact would be moving the goalposts, which is the one thing
    pre-registration exists to prevent.

=== EXCLUSION 1: PARAMETER-FREE RULES ARE DEAD ON DIVISIBILITY ===

    Every row of the array is divisible by 3:

        12321 = 3 x 4107   123 = 3 x 41   246 = 3 x 82   369 = 3 x 123

    and 38515 == 1 (mod 3).  So no Z-linear combination of the rows, and no
    polynomial in them with zero constant term, can equal 38515.  A rule
    must import an additive constant K with K == 1 (mod 3) from outside the
    array.

=== EXCLUSION 2: NO DIGIT RULE EITHER ===

    Digits occurring in rows 1-4:  {1, 2, 3, 4, 6, 9}
    Digits required by 38515:      {1, 3, 5, 8}      missing 5 and 8

    So no selection, permutation or rearrangement of the array's digits
    produces row 5.  Creating a 5 and an 8 requires arithmetic that makes
    new digits, not a reading of the figure.

=== THE GATE ITSELF IS UNDER-CONSTRAINED ===

    A linear rule R = a*s1 + b*s2 + c*s3 + K sees a,b,c only through
    t = a + 2b + 3c, because the stack rows are road*(1,2,3).  So

        R(road stack) = road * t + K

    The registered d=2 stack is [246, 492, 738], and 246 = 2 x 123, so that
    stack is literally 2x the d=1 stack.  The gate's three legs reduce to:

        (1) 123t + K = 38515                    one exact equation
        (2) implied by (1)
        (3) 12t + 35 == 33  ->  t == 6 (mod 37) one modular equation

    Two free parameters, one real constraint.  K absorbs leg (1) for any t
    in the class.  The gate cannot fail.

    Worse, extra legs add nothing:

      * Other d=1 roads are useless: 234-123 = 111, 345-123 = 222,
        456-123 = 333, all == 0 (mod 37).  Every d=1 road gives the same
        congruence.
      * The d=3 leg is automatic: with t == 6, R(3 x stack) == 31, which is
        exactly the d=3 target 6 x 36 == 31.  No information.
      * Even two DISTINCT road classes only force t == 6 and K == 0
        (mod 37) -- and then 123t + K = 38515 becomes 37(123j + k) = 37777
        = 37 x 1021, solvable for every j.  K remains a free integer.

=== VERDICT ===

    K = 0 (parameter-free):  EXCLUDED.  123t = 38515 needs t = 313.13, and
                             the mod-3 argument kills it structurally.
    K free:                  VACUOUS.  The gate is satisfiable by tuning
                             and has no discriminating power.

    There is no middle.  So the row-5 claim is FALSIFIED for the class of
    parameter-free rules over the array, and UNDERDETERMINED for any rule
    allowed a free constant -- which is step 5's disposition exactly.  The
    framework is not extended to accommodate it.

=== HOW TO REPAIR THE GATE (for any future attempt) ===

    (a) Declare a finite constant set IN ADVANCE and require every constant
        in R to come from it.  A rule with a free integer K is not a rule.
    (b) Require more independent constraints than free parameters, counted
        explicitly.  Two parameters and one constraint is not a test.
    (c) Do not use 246 as the d=2 transfer road: it is simultaneously a d=2
        AP road and 2 x the d=1 road, so it tests scaling rather than
        transfer.  135, 357, 468 or 579 are d=2 roads that are not scalar
        multiples of 123 -- though note that mod 37 they give the SAME
        congruence, since all d=2 roads are == 24.  The degeneracy is deep:
        road-stack legs can never yield more than one condition per residue
        class.

    Until (a) and (b) are met there is nothing to test, and the row-5
    observation stays where T330 put it: suggestive, n=1, not established.

=== FALSIFICATION ===
    Exhibit a rule over the array rows, using only constants declared in
    advance, that outputs 38515 on the d=1 stack.
"""

P = 37
ROWS = {'row1': 12321, 'row2': 123, 'row3': 246, 'row4': 369}
ROW5 = 38515


def run():
    # --- the discrepancy ---
    assert 123 % P == 12 and 246 % P == 24                   # road residues
    assert sum([123, 246, 369]) % P == 35                    # d=1 stack sum
    assert sum([246, 492, 738]) % P == 33                    # d=2 stack sum
    assert 12 != 35 and 33 == 33                             # the two levels

    # --- exclusion 1: divisibility by 3 ---
    assert all(v % 3 == 0 for v in ROWS.values())
    assert ROW5 % 3 == 1
    for a in range(-6, 7):
        for b in range(-6, 7):
            for c in range(-6, 7):
                for e in range(-6, 7):
                    v = a * 123 + b * 246 + c * 369 + e * 12321
                    assert v % 3 == 0 and v != ROW5

    # --- exclusion 2: digit inventory ---
    have = set("".join(str(v) for v in ROWS.values()))
    assert have == set("123469")
    assert set(str(ROW5)) - have == {"5", "8"}

    # --- the gate collapses to two parameters, one constraint ---
    assert [2 * x for x in (123, 246, 369)] == [246, 492, 738]
    # a linear rule a*s1+b*s2+c*s3+K on rows road*(1,2,3) collapses to
    # road*(a+2b+3c) + K, i.e. road*t + K
    for a in range(-4, 5):
        for b in range(-4, 5):
            for c in range(-4, 5):
                t_ = a + 2 * b + 3 * c
                for road in (123, 246, 135):
                    s = [road, 2 * road, 3 * road]
                    assert a * s[0] + b * s[1] + c * s[2] == road * t_
    # leg (3) alone: 12t + 35 == 33
    assert [t for t in range(P) if (12 * t + 35) % P == 33] == [6]
    # and K then absorbs leg (1) exactly
    t = 6
    K = ROW5 - 123 * t
    assert 123 * t + K == ROW5 and (246 * t + K) % P == 33
    assert K == 37777 == 37 * 1021                  # a tuned constant

    # --- extra legs add nothing ---
    for r in (234, 345, 456):
        assert (r - 123) % 111 == 0 and 111 % P == 0
        assert (r * t + K) % P == (123 * t + K) % P
    assert (6 * 36) % P == 31                        # d=3 target
    assert (369 * t + K) % P == 31                   # automatic
    # two distinct road classes force only t == 6, K == 0 (mod 37)
    sols = [(u, k) for u in range(P) for k in range(P)
            if (12 * u + k) % P == (6 * 12) % P
            and (24 * u + k) % P == (6 * 24) % P]
    assert sols == [(6, 0)]
    assert 37777 == 37 * 1021                        # still solvable for all j

    # --- the verdict ---
    assert ROW5 % 123 != 0                           # K = 0 impossible
    assert ROW5 / 123 != ROW5 // 123
    assert not any(123 * u == ROW5 for u in range(1, 1000))

    print("All assertions passed.\n")
    print("THEOREM 335.  Transfer gate audited.  Verdict: do not extend.\n")
    print("  CONSTRAINT DISCREPANCY")
    print("   proposal says R(1)==12, R(2)==33; registered is R(1)==35.")
    print("   12 is a ROAD residue, 33 a STACK SUM -- the pair mixes levels.")
    print("   consistent pairs: (12,24) roads, or (35,33) stacks.")
    print("   audited against the REGISTERED (35,33).\n")
    print("  EXCLUSION 1 -- divisibility")
    for k, v in ROWS.items():
        print(f"   {k:5s} {v:6d} = 3 x {v//3}")
    print(f"   38515 mod 3 = {ROW5%3}  -> no Z-combination of the rows,")
    print( "   and no zero-constant polynomial in them, can equal it.\n")
    print("  EXCLUSION 2 -- digit inventory")
    print(f"   rows 1-4 use digits {sorted(have)}")
    print(f"   38515 needs {sorted(set(str(ROW5)))}, missing"
          f" {sorted(set(str(ROW5))-have)}")
    print( "   -> no selection or permutation of the figure's digits.\n")
    print("  THE GATE IS UNDER-CONSTRAINED")
    print( "   a linear rule sees a,b,c only via t = a+2b+3c, so")
    print( "     R(road stack) = road*t + K")
    print( "   and [246,492,738] is literally 2 x the d=1 stack, so the legs")
    print( "   reduce to ONE exact equation and ONE congruence, against TWO")
    print(f"   free parameters.  t == 6 and K = {K} = 37 x 1021 passes.\n")
    print( "   extra legs add nothing: other d=1 roads differ by multiples of")
    print( "   111 == 0; the d=3 leg is automatic; two road classes force only")
    print( "   t == 6, K == 0 (mod 37), after which K is still free over Z.\n")
    print("  VERDICT")
    print(f"   K = 0  -> EXCLUDED: 123t = 38515 needs t = {ROW5/123:.4f}")
    print( "   K free -> VACUOUS: satisfiable by tuning, no discriminating power")
    print( "   => row 5 FALSIFIED for parameter-free rules, UNDERDETERMINED")
    print( "      otherwise.  Framework NOT extended.\n")
    print("  TO REPAIR THE GATE")
    print( "   (a) declare the constant set in advance; a free K is not a rule")
    print( "   (b) count constraints against parameters and require more of")
    print( "       the former; 2 params and 1 constraint is not a test")
    print( "   (c) 246 is a bad transfer road -- it is 2 x 123, so it tests")
    print( "       scaling, not transfer.  But all d=2 roads are == 24, so no")
    print( "       road leg ever gives more than one condition per class.")


if __name__ == "__main__":
    run()
