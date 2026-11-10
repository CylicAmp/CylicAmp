# CLASS: THEOREM
"""
Theorem 435: the equilibrium projection -- a 3-term AP collapses to its middle,
and that collapse sends residue 12d to 0 mod 37
Author: Michael Warren Song (CyclicAmp)

=== THE OWNER'S CONSTRUCTION, IN THE OWNER'S WORDS ===

    "This extends the previous grid by placing each equilibrium triplet
     beside the original triplet:

        equilibrium side | original side
        -----------------|---------------
               222       |      123
               555       |      456
               888       |      789
               222       |      123

     So the full array is

        2 2 2 1 2 3
        5 5 5 4 5 6
        8 8 8 7 8 9
        2 2 2 1 2 3 "

    "The rule is (n-1, n, n+1) -> (n, n, n), because one unit moves from the
     right entry to the left entry:  (n-1)+1 = n,  n = n,  (n+1)-1 = n."

    "each row has the form  equilibrium state | source state"

    "The left half is not a separate pattern added arbitrarily: it is the
     equilibrium projection of the right half."

Everything the owner stated is reproduced below and holds.  One generalisation
the write-up uses without naming it is named in RESULT 2.  The GF(37) content in
RESULTS 4-6 is new and is forced by 111 = 3 x 37, which the construction already
contains -- it is not routed there.

=== KEY RESULTS ===

1. THE MAP, AND WHY IT CONSERVES THE SUM
   T(n-1, n, n+1) = (n, n, n).
   One unit moves left, one unit moves right, and they cancel:
       (n-1) + 1 = n,   n = n,   (n+1) - 1 = n.
   So sum is invariant, and the fixed value is the mean:
       ((n-1) + n + (n+1)) / 3 = n.
   123 -> 222 (sum 6), 456 -> 555 (sum 15), 789 -> 888 (sum 24).

2. THE RULE IS NOT ABOUT STEP 1 -- IT IS THE MIDDLE OF ANY 3-TERM AP
   The write-up applies T horizontally at step d = 1 and then vertically to
   147, 258, 369, which have step d = 3.  The same formula covers both:
       ((n-d) + n + (n+d)) / 3 = n   for every d.
   So T is "replace a 3-term arithmetic progression by its middle term,
   repeated".  The horizontal and vertical halves of the construction are one
   rule at two values of d, not two rules.  This is the only point in the
   write-up left implicit; the arithmetic is unaffected.

3. THE COLUMN FAMILIES
   The six columns of the 4x6 array read
       2582  2582  2582  1471  2582  3693
   so the three distinct vertical families are 147, 258, 369, with sums
   12, 15, 18 and digital roots 3, 6, 9 -- the trinity.  Their equilibria are
   444, 555, 666, giving middles 4, 5, 6.
   Horizontally the three row sums are 6, 15, 24, all == 6 (mod 9), so all
   three rows share digital root 6.

4. (NEW)  EVERY EQUILIBRIUM STATE IS 0 MOD 37
   A repdigit is nnn = 111n, and 111 = 3 x 37, so
       nnn == 0  (mod 37)   for every n.
   The equilibrium side of the owner's array is therefore the zero residue,
   all four rows of it, and so are the vertical equilibria 444, 555, 666.
   T does not move the residue around: it annihilates it.

5. (NEW)  THE MULTIPLIER OF 37 IS THE ROW SUM
   nnn = 111n = 37 x 3n, and the source triple sums to 3n, so
       T(source) = 37 x sum(source).
   Checked on all six triples in the array:
       123 sum  6 -> 222 = 37 x  6
       456 sum 15 -> 555 = 37 x 15
       789 sum 24 -> 888 = 37 x 24
       147 sum 12 -> 444 = 37 x 12
       258 sum 15 -> 555 = 37 x 15
       369 sum 18 -> 666 = 37 x 18
   The owner's RESULT "the row sums are conserved" and the factor of 37 are the
   same fact seen twice: conserving the sum is what makes the multiplier the sum.

6. (NEW)  T SENDS 12d TO 0, SO IT KILLS BOTH T326 AND T281 IN ONE STEP
   T326 proved that an AP triple a, a+d, a+2d satisfies
       n = 111a + 12d == 12d  (mod 37),
   the start a dropping out because 111 = 3 x 37.  Combined with RESULT 4:
       T : 12d  |-->  0   (mod 37)   for every d.
   The two instances present in this array:
       d = 1  rows      123, 456, 789  ==  12  (mod 37)  ->  0
       d = 3  columns   147, 258, 369  ==  36  (mod 37)  ->  0
   and 36 == -1, which is exactly T281's "-1 identity" for 147/258/369.  So
   T281's identity is T326 evaluated at d = 3, and this theorem adds that the
   equilibrium projection sends it, and every other 12d, to zero.

7. (NEW)  THE FRAMEWORK PLACEMENT -- T LANDS EVERYTHING ON THE SEAM
   Running the owner's numbers through the standing audit:
       rows      123, 456, 789  ->  residue 12, orbit SA_ST_A {9, 12, 16}
       columns   147, 258, 369  ->  residue 36, orbit NEG_H   {11, 27, 36}
       all equilibria           ->  residue  0, the SEAM: no orbit, no class,
                                    the rotation axis (T302)
   So T collapses two different orbits onto the same axis.
   Behind it: every source triple is already divisible by 3, since its digit
   sum is 3n.  The 3 is present before T runs.  What T installs is the 37 --
   verified both ways, 3 | source for all six, and 37 does not divide any of
   the six sources while it divides every equilibrium.

=== WHAT IS FORCED AND WHAT IS NOT ===

   FORCED by base-10 rendering, carrying no information about 37 beyond
   111 = 3 x 37:
     - nnn == 0 (mod 37), and the multiplier being the sum (RESULTS 4, 5)
     - the residue 12d of an AP triple (T326's law, quoted not reproved)
   FORCED by arithmetic, in any base:
     - the mean of a 3-term AP is its middle term (RESULTS 1, 2)
     - sum conservation under T
   FORCED, and the orbit names are a complete partition so membership alone
   carries no information (T282):
     - the SA_ST_A / NEG_H / SEAM placement of RESULT 7.  What is not forced
       there is that T collapses two distinct orbits to one axis.
   CONTINGENT on the digits 1..9 being used:
     - the particular families 147/258/369 and their DRs 3, 6, 9 (RESULT 3)
     - the common row DR of 6

   What is NOT claimed: that 37 is distinguished here.  Any prime p with
   111 == 0 (mod p) does the same, and 111 = 3 x 37 has exactly the divisors
   1, 3, 37, 111 -- so the claim holds verbatim for p = 3 and p = 37 and for
   no other prime.  That two-element set is the whole content, and it is
   recorded as such rather than as evidence for 37.

=== FALSIFICATION ===

   Exhibit a 3-term arithmetic progression whose mean is not its middle term;
   or a digit n in 0..9 with 111n not divisible by 37; or an AP triple whose
   3-digit concatenation is not congruent to 12d mod 37.  Any one of these
   fails an assertion below.

=== PRIOR ART IN THIS CORPUS ===

   theorem_326_all_roads_ap_triples_gf37.py   n == 12d (mod 37); the step, not
                                              the start, fixes the residue
   theorem_281_147_258_369_gf37.py            147 == 258 == 369 == 36 == -1;
                                              shown here to be T326 at d = 3
   zero_fill_bridge_audit.py                  the other "equilibrium": units
                                              redistributed to a repunit, sum
                                              and DR conserved.  Same mechanism
                                              -- a unit moved between positions
                                              with the total fixed -- different
                                              fixed point: repunit there, the
                                              repdigit nnn here.
   theorem_432_carry_map_digital_root_rings_gf37.py   the carry map on DR rings

New beyond those three: the map T itself as a projection onto repdigits
(RESULTS 1, 2), the annihilation 12d -> 0 (RESULT 6), and the identity
T(source) = 37 x sum(source) (RESULT 5).
"""

FAIL = []


def check(cond, label, actual, expected):
    if not cond:
        FAIL.append(f"{label}: actual={actual!r}, expected={expected!r}")


def dr(x):
    """Digital root, with DR(0) = 9 as this corpus defines it."""
    return 9 if x == 0 else (x - 1) % 9 + 1


# ── the owner's array, verbatim ───────────────────────────────────────────────
ARRAY = [[2, 2, 2, 1, 2, 3],
         [5, 5, 5, 4, 5, 6],
         [8, 8, 8, 7, 8, 9],
         [2, 2, 2, 1, 2, 3]]

ROWS_SOURCE = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
COLS_SOURCE = [(1, 4, 7), (2, 5, 8), (3, 6, 9)]


def T(triple):
    """Replace a 3-term arithmetic progression by its middle term, repeated."""
    a, b, c = triple
    if b - a != c - b:
        raise ValueError(f"not an arithmetic progression: {triple}")
    return (b, b, b)


def concat3(triple):
    a, b, c = triple
    return 100 * a + 10 * b + c


# ── RESULT 1: the map, sum conservation, mean = middle ───────────────────────
def test_map_and_conservation():
    for src in ROWS_SOURCE:
        eq = T(src)
        a, b, c = src
        check(eq == (b, b, b), f"T{src}", eq, (b, b, b))
        check(sum(eq) == sum(src), f"sum {src}", sum(eq), sum(src))
        # the unit-moving description: (n-1)+1, n, (n+1)-1
        check((a + 1, b, c - 1) == eq, f"unit move {src}", (a + 1, b, c - 1), eq)
        check(3 * b == sum(src), f"mean {src}", 3 * b, sum(src))
    check([T(s) for s in ROWS_SOURCE] == [(2, 2, 2), (5, 5, 5), (8, 8, 8)],
          "the three rows", [T(s) for s in ROWS_SOURCE],
          [(2, 2, 2), (5, 5, 5), (8, 8, 8)])


# ── RESULT 2: the rule is the middle of ANY 3-term AP, not just d = 1 ────────
def test_rule_is_d_agnostic():
    # horizontal d = 1, vertical d = 3, both covered by the same formula
    for src in ROWS_SOURCE:
        check(src[1] - src[0] == 1, f"row step {src}", src[1] - src[0], 1)
    for src in COLS_SOURCE:
        check(src[1] - src[0] == 3, f"col step {src}", src[1] - src[0], 3)
    # ((n-d) + n + (n+d)) / 3 == n for every d, over a wide sweep
    for n in range(-50, 51):
        for d in range(-20, 21):
            trip = (n - d, n, n + d)
            check(sum(trip) == 3 * n, f"AP mean n={n} d={d}", sum(trip), 3 * n)
            check(T(trip) == (n, n, n), f"T n={n} d={d}", T(trip), (n, n, n))
    # a non-AP triple is rejected rather than silently averaged
    try:
        T((1, 2, 4))
    except ValueError:
        pass
    else:
        FAIL.append("T((1,2,4)) should have raised ValueError")


# ── RESULT 3: the array, its columns, the families, the digital roots ───────
def test_array_structure():
    # left half is the equilibrium image of the right half
    right = [tuple(r[3:]) for r in ARRAY[:3]]
    left = [tuple(r[:3]) for r in ARRAY[:3]]
    check(right == ROWS_SOURCE, "right half", right, ROWS_SOURCE)
    check([T(r) for r in right] == left, "left = Eq(right)",
          [T(r) for r in right], left)
    # the fourth row repeats the first
    check(ARRAY[3] == ARRAY[0], "row 4 repeats row 1", ARRAY[3], ARRAY[0])
    # the six columns
    cols = [''.join(str(ARRAY[r][c]) for r in range(4)) for c in range(6)]
    check(cols == ['2582', '2582', '2582', '1471', '2582', '3693'],
          "columns", cols, ['2582', '2582', '2582', '1471', '2582', '3693'])
    # three distinct vertical families, sums 12/15/18, DRs 3/6/9
    sums = [sum(f) for f in COLS_SOURCE]
    check(sums == [12, 15, 18], "family sums", sums, [12, 15, 18])
    check([dr(s) for s in sums] == [3, 6, 9], "family DRs",
          [dr(s) for s in sums], [3, 6, 9])
    # their equilibria give middles 4, 5, 6
    check([T(f)[0] for f in COLS_SOURCE] == [4, 5, 6], "family middles",
          [T(f)[0] for f in COLS_SOURCE], [4, 5, 6])
    # row sums 6, 15, 24 all have DR 6
    rsums = [sum(r) for r in ROWS_SOURCE]
    check(rsums == [6, 15, 24], "row sums", rsums, [6, 15, 24])
    check({dr(s) for s in rsums} == {6}, "row DRs all 6",
          {dr(s) for s in rsums}, {6})
    check({s % 9 for s in rsums} == {6}, "row sums mod 9",
          {s % 9 for s in rsums}, {6})


# ── RESULT 4: every equilibrium state is 0 mod 37, because 111 = 3 x 37 ─────
def test_repdigit_is_zero_mod_37():
    check(111 == 3 * 37, "111 = 3 x 37", 111, 3 * 37)
    for n in range(10):
        check(111 * n % 37 == 0, f"{n}{n}{n} mod 37", 111 * n % 37, 0)
    # the equilibrium side of the owner's array, all four rows
    for row in ARRAY:
        eq = concat3(tuple(row[:3]))
        check(eq % 37 == 0, f"eq {eq} mod 37", eq % 37, 0)
    # and the vertical equilibria
    for f in COLS_SOURCE:
        v = concat3(T(f))
        check(v % 37 == 0, f"vertical eq {v} mod 37", v % 37, 0)


# ── RESULT 5: the multiplier of 37 is the source sum ────────────────────────
def test_multiplier_is_the_sum():
    for src in ROWS_SOURCE + COLS_SOURCE:
        eq = concat3(T(src))
        check(eq == 37 * sum(src), f"{src}: eq = 37 x sum",
              eq, 37 * sum(src))
        check(eq % 37 == 0 and eq // 37 == sum(src),
              f"{src}: quotient", eq // 37, sum(src))
    # the six stated lines, spelled out
    stated = {(1, 2, 3): (6, 222), (4, 5, 6): (15, 555), (7, 8, 9): (24, 888),
              (1, 4, 7): (12, 444), (2, 5, 8): (15, 555), (3, 6, 9): (18, 666)}
    for src, (s, eq) in stated.items():
        check(sum(src) == s, f"{src} sum", sum(src), s)
        check(concat3(T(src)) == eq, f"{src} eq", concat3(T(src)), eq)
        check(eq == 37 * s, f"{eq} = 37 x {s}", eq, 37 * s)
    # holds for every AP triple with single digits, not just these six
    for a in range(10):
        for d in range(-4, 5):
            trip = (a, a + d, a + 2 * d)
            if not all(0 <= x <= 9 for x in trip):
                continue
            eq = concat3(T(trip))
            check(eq == 37 * sum(trip), f"AP {trip}", eq, 37 * sum(trip))


# ── RESULT 6: T sends 12d to 0; T281 is T326 at d = 3 ──────────────────────
def test_annihilates_12d():
    # T326's law, quoted and re-checked on every single-digit AP triple
    for a in range(10):
        for d in range(-4, 5):
            trip = (a, a + d, a + 2 * d)
            if not all(0 <= x <= 9 for x in trip):
                continue
            n = concat3(trip)
            check(n % 37 == 12 * d % 37, f"{trip} == 12d",
                  n % 37, 12 * d % 37)
            check(n == 111 * a + 12 * d, f"{trip} = 111a + 12d",
                  n, 111 * a + 12 * d)
            # and T annihilates it
            check(concat3(T(trip)) % 37 == 0, f"T{trip} mod 37",
                  concat3(T(trip)) % 37, 0)
    # the two instances in this array
    for src in ROWS_SOURCE:
        check(concat3(src) % 37 == 12, f"row {src} mod 37",
              concat3(src) % 37, 12)
    for src in COLS_SOURCE:
        check(concat3(src) % 37 == 36, f"col {src} mod 37",
              concat3(src) % 37, 36)
    # 36 == -1, which is T281's identity, and it is 12 x 3
    check(36 == (-1) % 37, "36 = -1 mod 37", 36, (-1) % 37)
    check(12 * 3 % 37 == 36, "T281 is T326 at d=3", 12 * 3 % 37, 36)


# ── the forced/contingent boundary: which primes give RESULT 4 ──────────────
def test_only_3_and_37():
    """nnn == 0 (mod p) for every digit n iff p | 111.  111 = 3 x 37."""
    divisors = [d for d in range(1, 112) if 111 % d == 0]
    check(divisors == [1, 3, 37, 111], "divisors of 111",
          divisors, [1, 3, 37, 111])
    primes = [p for p in divisors if p > 1 and
              all(p % q for q in range(2, int(p ** 0.5) + 1))]
    check(primes == [3, 37], "primes dividing 111", primes, [3, 37])
    # for any other prime there is a digit whose repdigit is not 0 mod p
    for p in (2, 5, 7, 11, 13, 17, 19, 23, 29, 31, 41, 43):
        bad = [n for n in range(1, 10) if 111 * n % p != 0]
        check(bad != [], f"p={p} is not universal", bad, "non-empty")


# ── RESULT 7: the framework placement -- T lands everything on the SEAM ────
ORBITS = {"SA_ST_A": (9, 12, 16), "NEG_H": (11, 27, 36)}


def test_seam_landing():
    """Rows sit in SA_ST_A, columns in NEG_H, every equilibrium on the SEAM."""
    for src in ROWS_SOURCE:
        r = concat3(src) % 37
        check(r == 12 and r in ORBITS["SA_ST_A"], f"row {src} in SA_ST_A",
              r, "12 in (9,12,16)")
    for src in COLS_SOURCE:
        r = concat3(src) % 37
        check(r == 36 and r in ORBITS["NEG_H"], f"col {src} in NEG_H",
              r, "36 in (11,27,36)")
    # the SEAM is residue 0: no orbit, the rotation axis (T302)
    for src in ROWS_SOURCE + COLS_SOURCE:
        check(concat3(T(src)) % 37 == 0, f"T{src} on SEAM",
              concat3(T(src)) % 37, 0)
    # every source triple is already divisible by 3 -- its digit sum is 3n
    for src in ROWS_SOURCE + COLS_SOURCE:
        check(concat3(src) % 3 == 0, f"3 | {concat3(src)}",
              concat3(src) % 3, 0)
        check(sum(src) % 3 == 0, f"digit sum of {src}", sum(src) % 3, 0)
    # so the 3 is present before T; what T installs is the 37
    for src in ROWS_SOURCE + COLS_SOURCE:
        eq = concat3(T(src))
        check(eq % 3 == 0 and eq % 37 == 0, f"3 and 37 both divide {eq}",
              (eq % 3, eq % 37), (0, 0))
        check(concat3(src) % 37 != 0, f"37 does NOT divide source {concat3(src)}",
              concat3(src) % 37, "non-zero")


def self_test():
    tests = [test_map_and_conservation,
             test_rule_is_d_agnostic,
             test_array_structure,
             test_repdigit_is_zero_mod_37,
             test_multiplier_is_the_sum,
             test_annihilates_12d,
             test_only_3_and_37,
             test_seam_landing]
    for t in tests:
        t()
        print(f"  ok  {t.__name__}")
    if FAIL:
        for f in FAIL:
            print(f"  FAIL  {f}")
        raise AssertionError(f"{len(FAIL)} check(s) failed")
    print()
    print("T435  the equilibrium projection")
    print("  RESULT 1  T(n-d, n, n+d) = (n,n,n); sum conserved, middle = mean")
    print("  RESULT 2  one rule at two steps: d=1 across rows, d=3 down columns")
    print("  RESULT 3  columns 2582 2582 2582 1471 2582 3693; families 147/258/369")
    print("            family sums 12,15,18 -> DR 3,6,9;  row sums 6,15,24 -> DR 6")
    print("  RESULT 4  nnn = 111n and 111 = 3x37, so every equilibrium is 0 mod 37")
    print("  RESULT 5  T(source) = 37 x sum(source)  -- the multiplier IS the sum")
    print("  RESULT 6  T : 12d -> 0 (mod 37).  rows 12 -> 0,  columns 36 -> 0,")
    print("            and 36 = -1 is T281's identity, i.e. T326 at d = 3")
    print()
    print("  RESULT 7  rows in SA_ST_A{9,12,16}, columns in NEG_H{11,27,36},")
    print("            every equilibrium on the SEAM (residue 0, the rotation")
    print("            axis, T302).  The source already carries the 3 -- its")
    print("            digit sum is 3n -- and T is what installs the 37.")
    print()
    print("  scope: RESULT 4 holds for p = 3 and p = 37 and no other prime,")
    print("         since 111 has divisors 1, 3, 37, 111.  Not evidence for 37.")


if __name__ == "__main__":
    self_test()
