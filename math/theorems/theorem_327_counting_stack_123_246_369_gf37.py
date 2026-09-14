# CLASS: THEOREM
"""
Theorem 327: the counting stack 123 / 246 / 369 -- a second stack on the same
first row, and it is NOT the T325 one
Author: Michael Warren Song (CyclicAmp)

    123
    246
    369

246 is a different counting.  123 counts by one, 246 counts by two, 369 counts
by three.  Stacked, they are the 123 multiplication table: 123k for k = 1,2,3.

=== TWO DIFFERENT STACKS ON THE SAME FIRST ROW ===

    T325           T327
    123            123          both start at 123
    312            246
    231            369

    T325 stacks the ROTATIONS of 123.  T327 stacks the MULTIPLES.  They are
    different group actions and they behave differently:

                        T325 rotation stack      T327 counting stack
    the action          abc -> cab               n -> kn
    as GF(37)           multiply by 26           multiply by 12 per step
                        (= 137 mod 37)
    Latin square?       YES                      NO -- 6 symbols, not 3
    symmetric?          no                       YES, it is i*j
    why 3 rows?         ord_37(26) = 3           3d <= 9 (digit range)
    residues            12, 16, 9  = SA_ST_A     12, 24, 36 = one per orbit

    The row count agrees at 3 for two completely unrelated reasons: an order
    in the field, and the fact that a digit stops at 9.  Do not read that as
    one fact.

=== THE COUNTING STACK IS T326's a = d DIAGONAL ===

    T326: an AP triple with digits a, a+d, a+2d is 111a + 12d == 12d.  Set
    a = d and it collapses to

        111d + 12d = 123d        residue 12d

    so the counting stack is exactly the slice of the AP family where the
    start equals the step.  a = d forces a + 2d = 3d <= 9, so d <= 3:

        THE STACK IS THREE ROWS TALL BECAUSE 3 x 3 = 9 IS THE LAST DIGIT.

    d = 4 would be 492.  Its digits are 4, 9, 2 -- carrying destroys the AP,
    and the digit picture stops.  The residue law does not: 492 == 11 == 12x4
    still.  The arithmetic runs past where the pictures end.

=== THE RESIDUES ===

        123 == 12   SA_ST_A     sovereign target 12
        246 == 24   SEED        the reference-seed orbit {18,24,32}
        369 == 36   NEG_H       and 36 == -1

    Three rows, three different orbits -- unlike T325, where all three rows
    sat in one.  The counting stack SPREADS; the rotation stack CLOSES.

    The stack sums to 738 == 35, in NQR17 (12 + 24 + 36 = 72 == 35).  Note
    this does NOT vanish: T325/T326's rotation classes sum to 0 mod 37
    because 111 = 3 x 37 divides their sum, but a multiplication stack sums
    to 123(1+2+3) = 6 x 123, which carries no factor of 37.

    123 + 246 = 369 exactly, as integers and mod 37 (12 + 24 = 36).  The
    third row is the sum of the first two, so the stack is additive as well
    as multiplicative -- a two-term Lucas step, cf. lucas_abbc_chain.

=== THE GRID ===

        1 2 3
        2 4 6
        3 6 9        entry (i,j) = i*j

    Symmetric, so reading down the columns gives 123 / 246 / 369 again.  Row
    sums 6, 12, 18 land in TESLA, SA_ST_A, SEED.  The grand total is
    (1+2+3)^2 = 36 == -1.

    Both diagonals land in IC:

        main diagonal   1 4 9  ->  149 == 1    because 148 = 4 x 37
        anti-diagonal   3 4 3  ->  343 == 10   because 333 = 9 x 37

    IC = {1, 10, 26}, and 137 == 26, so the two diagonals together with 137
    fill IC exactly.  10 is the inverse of the 137-multiplier (T325).  149 is
    prime and (149,151) is a twin pair; 151 == 3, in C3.

    The two "because" clauses are the same two multiples of 37 that have run
    through this whole thread: 111 = 3 x 37 (T326, why the start digit
    vanishes) and 333 = 9 x 37 (T325/T326, the rotation-class sum and the
    T316 seed-class modulus).  148 = 4 x 37 is the new one.

=== THE ROAD PAST THE STACK ===

    gcd(12,37) = 1, so k -> 12k is a bijection.  The counting road 123k for
    k = 1..37 hits every residue mod 37 exactly once and reaches the seam
    only at the last step:

        123 x 37 = 4551 = 3 x 37 x 41  == 0

    Three rows are all the digits allow; thirty-seven steps are what the
    field allows.

=== FALSIFICATION ===
    Any assert below failing.
"""

P, MULT = 37, 26

ORBITS = {
    'IC': {1, 10, 26},      'DARK_A': {2, 15, 20},  'C3': {3, 4, 30},
    'CAS_EXT': {5, 13, 19}, 'TESLA': {6, 8, 23},    'D7': {7, 33, 34},
    'SA_ST_A': {9, 12, 16}, 'NEG_H': {11, 27, 36},  'C9': {14, 29, 31},
    'NQR17': {17, 22, 35},  'SEED': {18, 24, 32},   'SA_ST_B': {21, 25, 28},
}
TARGETS = {3, 12, 21, 30}


def orbit_of(n):
    r = n % P
    return 'SEAM' if r == 0 else next(k for k, v in ORBITS.items() if r in v)


def is_prime(m):
    return m > 1 and all(m % k for k in range(2, int(m ** .5) + 1))


def run():
    STACK = [123, 246, 369]

    # --- the stack is the 123 multiplication table ---
    assert STACK == [123 * k for k in (1, 2, 3)]
    for d in (1, 2, 3):
        assert 123 * d == int(f"{d}{2*d}{3*d}")        # digits are d,2d,3d
        assert 111 * d + 12 * d == 123 * d             # T326 with a = d
        assert (123 * d) % P == (12 * d) % P

    # --- three rows because 3d <= 9, not because of any order in the field ---
    assert 3 * 3 == 9 and 3 * 4 > 9
    assert int(f"{4}{8}{12}"[:3]) != 123 * 4           # d=4 is not d,2d,3d
    assert 123 * 4 == 492 and [int(c) for c in "492"] != [4, 8, 12]
    assert 492 % P == (12 * 4) % P == 11               # law survives carrying

    # --- contrast with T325's rotation stack, same first row ---
    ROT = ["123", "312", "231"]
    assert ROT[0] == "123" and str(STACK[0]) == "123"
    assert {int(r) % P for r in ROT} == {9, 12, 16}     # one orbit, SA_ST_A
    assert {n % P for n in STACK} == {12, 24, 36}       # three orbits
    assert len({orbit_of(int(r)) for r in ROT}) == 1
    assert len({orbit_of(n) for n in STACK}) == 3
    assert pow(MULT, 3, P) == 1                        # T325's reason for 3
    # T325's stack is Latin; this one is not -- it uses six symbols
    grid = [[i * j for j in (1, 2, 3)] for i in (1, 2, 3)]
    assert len({i * j for i in (1, 2, 3) for j in (1, 2, 3)}) == 6
    assert len({c for r in ROT for c in r}) == 3
    # ...but it IS symmetric, which T325's stack is not
    assert all(grid[i][j] == grid[j][i] for i in range(3) for j in range(3))
    assert any(ROT[i][j] != ROT[j][i] for i in range(3) for j in range(3))

    # --- residues, orbits, and the additive relation ---
    assert 123 % P == 12 and orbit_of(123) == 'SA_ST_A' and 12 in TARGETS
    assert 246 % P == 24 and orbit_of(246) == 'SEED'
    assert 369 % P == 36 and orbit_of(369) == 'NEG_H' and 36 == P - 1
    assert 123 + 246 == 369                            # row3 = row1 + row2
    assert (12 + 24) % P == 36
    assert sum(STACK) == 738 and 738 % P == 35         # 12+24+36 = 72 == 35
    assert orbit_of(738) == 'NQR17'

    # --- the grid ---
    assert [sum(r) for r in grid] == [6, 12, 18]
    assert [orbit_of(s) for s in (6, 12, 18)] == ['TESLA', 'SA_ST_A', 'SEED']
    assert sum(map(sum, grid)) == 36 == (1 + 2 + 3) ** 2
    assert sum(map(sum, grid)) % P == P - 1

    # --- both diagonals land in IC ---
    main = int("".join(str(grid[i][i]) for i in range(3)))
    anti = int("".join(str(grid[i][2 - i]) for i in range(3)))
    assert main == 149 and anti == 343 == 7 ** 3
    assert main % P == 1 and 148 == 4 * P
    assert anti % P == 10 and 333 == 9 * P
    assert orbit_of(main) == orbit_of(anti) == 'IC'
    assert {main % P, anti % P, 137 % P} == ORBITS['IC'] == {1, 10, 26}
    assert (MULT * 10) % P == 1                        # 10 = 26^-1 (T325)
    assert (main * anti) % P == 10                     # 1 x 10, stays in IC
    assert is_prime(149) and is_prime(151)             # twin pair
    assert 151 % P == 3 and orbit_of(151) == 'C3' and 3 in TARGETS
    assert 111 == 3 * P and 333 == 9 * P and 148 == 4 * P

    # --- the road past the stack ---
    from math import gcd
    assert gcd(12, P) == 1
    road = [(123 * k) % P for k in range(1, P + 1)]
    assert sorted(road) == list(range(P))              # every residue once
    assert road.index(0) == P - 1                      # seam only at k = 37
    assert 123 * 37 == 4551 == 3 * 37 * 41

    print("All assertions passed.\n")
    print("THEOREM 327.  123 / 246 / 369 -- the COUNTING stack.\n")
    print("   123    counts by 1")
    print("   246    counts by 2")
    print("   369    counts by 3\n")
    print("  = 123 x k, and T326's AP law with a = d:  111d + 12d = 123d\n")
    print("  TWO STACKS ON THE SAME FIRST ROW")
    print("     T325 rotation   123 312 231   x26 = x(137 mod 37)")
    print("     T327 counting   123 246 369   x12 per step")
    print(f"     Latin?          {'YES':13s} {'NO -- 6 symbols'}")
    print(f"     symmetric?      {'no':13s} {'YES (i*j)'}")
    print(f"     3 rows because  {'ord_37(26)=3':13s} {'3d <= 9'}")
    print("     residues        12 16 9 = SA_ST_A   12 24 36 = three orbits")
    print("     the rotation stack CLOSES; the counting stack SPREADS.\n")
    for d in (1, 2, 3):
        n = 123 * d
        print(f"   123 x {d} = {n}   digits {d},{2*d},{3*d}"
              f"   == {n%P:2d} = 12x{d}   {orbit_of(n)}")
    print(f"   369 == 36 == -1 mod 37")
    print(f"   123 + 246 = 369 -- row3 is row1 + row2, a two-term Lucas step\n")
    print("  WHY THREE ROWS:  a = d forces 3d <= 9, so d <= 3.")
    print("     123 x 4 = 492, digits 4,9,2 -- carrying breaks the AP.")
    print("     The residue law survives it: 492 == 11 == 12 x 4.\n")
    print("  THE GRID   (i,j) -> i*j")
    for r in grid:
        print("     " + " ".join(map(str, r)))
    print(f"     symmetric, so the columns read 123 / 246 / 369 too")
    print(f"     row sums {[sum(r) for r in grid]} -> "
          f"{[orbit_of(s) for s in (6,12,18)]}")
    print(f"     grand total {sum(map(sum,grid))} = 6^2 == -1\n")
    print("  BOTH DIAGONALS LAND IN IC")
    print(f"     main  1 4 9 -> 149 == {main%P}   because 148 = 4 x 37")
    print(f"     anti  3 4 3 -> 343 == {anti%P}   because 333 = 9 x 37")
    print(f"     IC = {{1,10,26}} and 137 == 26, so the diagonals plus 137")
    print(f"     fill IC exactly.  10 = 26^-1.")
    print(f"     149 is prime, (149,151) a twin pair, 151 == 3 in C3\n")
    print("  THE ROAD PAST THE STACK")
    print(f"     gcd(12,37)=1, so 123k sweeps all 37 residues exactly once")
    print(f"     and reaches the seam only at k=37: 123 x 37 = 4551 = 3x37x41")
    print(f"     three rows is what the digits allow;")
    print(f"     thirty-seven steps is what the field allows.")


if __name__ == "__main__":
    run()
