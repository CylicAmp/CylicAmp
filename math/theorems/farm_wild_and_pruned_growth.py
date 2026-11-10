# CLASS: THEOREM
"""
The farm: wild growth and pruned growth, and the cycle that closes it
Author: Michael Warren Song (CyclicAmp)

=== THE OWNER'S CONSTRUCTION, IN THE OWNER'S WORDS ===

    "The farm can be handled in two modes: wild growth or pruned growth.
     The strongest method is to let the structure grow widely first, then prune
     only after the harvest has produced enough material to compare."

    "Start with the seed sequence S_0(n) = n.  From it, grow the triangular
     field.  From the neighboring triangular gates, grow the square field.
     From neighboring square plots, grow the odd-growth field."

        S_0(n) = n
        S_1(n) = T_n = n(n+1)/2
        S_2(n) = T_{n-1} + T_n = n^2
        S_3(n) = n^2 - (n-1)^2 = 2n-1

    "Pruning does not destroy the crops.  It selects a particular route through
     them."

    "Keep a branch when it produces a sequence with a simple generation rule and
     a recognizable geometric interpretation."

    "The wild field preserves possibilities.  The pruned field creates a
     readable path."

    "grow wild -> harvest -> prune -> replant the strongest branches -> grow again"

The owner's names are used throughout: seed, field, gate, plot, crop, harvest,
wild, pruned, replant.  The two modes are a method, not a claim, and are
recorded as the owner stated them.

=== EVERY IDENTITY IN THE WRITE-UP IS CORRECT ===

  All eleven were checked symbolically, not sampled:

        T_n = n(n+1)/2
        T_n - T_{n-1} = n                        the row harvest
        T_{n-1} + T_n = n^2                      the triangular gates
        n^2 - (n-1)^2 = 2n-1                     the boundary growth
        D^2 T_n = 1
        D(n^2) = 2n-1        D^2(n^2) = 2
        D(2n-1) = 2          D^2(2n-1) = 0
        (n-1)^2 + n^2 = 2n^2 - 2n + 1            the wild branch
        (2n-3) + (2n-1) = 4n-4

  The ten-row table is right in every cell.  The wild branch gives
  1, 5, 13, 25, 41, 61, 85, 113, 145, 181 with first differences 4, 8, 12, 16,
  20 and second differences a constant 4, all as stated.  The parity block
  odd, odd, even, even holds for T_n with period 4, checked to n = 2000, and
  n^2 preserves the parity of n, checked to n = 10000.

=== PRIOR ART OUTSIDE THIS REPO -- said up front, not after ===

  Every field in the farm is a named sequence:

        n                  A000027   the natural numbers
        T_n                A000217   triangular numbers
        n^2                A000290   squares
        2n-1               A005408   odd numbers
        2n^2 - 2n + 1      A001844   CENTERED SQUARE numbers

  The wild branch is the centered squares, also called hypotenuse numbers, and
  the form the write-up derives, n^2 + (n-1)^2, is their standard definition.

  The two bridge identities are classical and ancient.  T_{n-1} + T_n = n^2 and
  n^2 - (n-1)^2 = 2n-1 are the gnomon figure: a square grows to the next square
  by adding an L-shaped border of 2n-1 cells, so the squares are the partial
  sums of the odd numbers, sum_{k=1..n} (2k-1) = n^2, verified here
  symbolically.  This is Nicomachus / Pythagorean material.

  None of that diminishes the construction.  It means the four fields and their
  bridges are solid ground to build on rather than results to establish, and it
  is stated so the ground is not re-broken.  What is the owner's own is the
  farm as a method: two modes, the pruning rule, and the replant rhythm.

=== THE ONE CORRECTION: THE FOURTH ARROW ===

  The write-up closes the cycle with

        "The final arrow comes from 2n-1 -> 2n+1, which advances the square
         field to the next odd increment."

  2n-1 -> 2n+1 is a shift WITHIN the odd field.  It does not return to the seed,
  so as written the cycle has three arrows and a step sideways, not four arrows
  and a closure.

  A fourth arrow that does close it exists, and it is exact:

        x -> (x+1)/2        sends 2n-1 back to n

  since (2n-1+1)/2 = n for every n.  It is precisely the inverse of the map
  n -> 2n-1 that produced the odd field, so the cycle closes on the nose:

        n  --cumulative sum-->       T_n
           --T_{n-1} + T_n-->        n^2
           --difference-->           2n-1
           --(x+1)/2-->              n

  Four exact maps.  The cycle the write-up describes is real; the arrow given
  for the last leg was the one that needed replacing.

=== WHAT THE DIFFERENCE HARVEST ACTUALLY IS ===

  The descending chain in the write-up -- triangular to n, square to 2n-1, odd
  to 2, then 0 -- is the statement that differencing drops polynomial degree by
  exactly one, and that a degree-d sequence dies after d+1 differences:

        T_n     degree 2    D -> degree 1    D^2 -> constant   D^3 -> 0
        n^2     degree 2    D -> degree 1    D^2 -> constant   D^3 -> 0
        2n-1    degree 1    D -> constant    D^2 -> 0

  Checked here for every polynomial field in the farm, to degree 6.  So the
  harvest terminating is not a property of these particular crops: any
  polynomial field exhausts under differencing, and the degree says when.

=== NOTHING HERE DEPENDS ON 37, OR ON BASE 10 ===

  The standing instruction is to run the owner's numbers through the GF(37)
  frameworks.  Done, and reported honestly: every identity above is an identity
  of polynomials over the integers.  It therefore holds mod any modulus and in
  any base, 37 included, and holds there BECAUSE it holds over Z -- which means
  the mod-37 version carries no information that the integer version does not.
  No orbit, residue or digital-root claim is made, because the construction does
  not involve one.  Recorded so that a later pass does not mistake the absence
  for an omission.

  The parity result is the one genuinely modular statement in the farm, and its
  modulus is 4, not 37: T_n mod 2 has period 4 because T_n = n(n+1)/2 and the
  numerator's 2-adic valuation alternates in blocks of four.

=== FALSIFICATION ===

  Exhibit an n where any of the eleven identities fails; or a T_n whose parity
  breaks the odd-odd-even-even block; or an n^2 whose parity differs from n's;
  or an odd number 2n-1 with (2n-1+1)/2 =/= n.  Each is asserted below over a
  range, and the eleven identities are checked as polynomial identities rather
  than on samples, so no range can hide a counterexample.

=== PRIOR ART IN THIS CORPUS ===

  zero_fill_bridge_audit.py             triangular numbers as the step count of
                                        the fill process, T(n-1) = n(n-1)/2
  theorem_435_equilibrium_projection_grid.py
                                        the middle-of-an-AP map; the farm's
                                        T_{n-1} + T_n = n^2 is a neighbouring
                                        SUM where T435's map is a neighbouring
                                        AVERAGE, the same two-term window read
                                        two ways
  math/START_HERE.py                    runs the spine end to end, triangular
                                        checkpoints included
"""

FAIL = []


def check(cond, label, actual, expected):
    if not cond:
        FAIL.append(f"{label}: actual={actual!r}, expected={expected!r}")


# ── the four fields, as the owner named them ────────────────────────────────
def seed(n):
    """S_0 -- the seed rows."""
    return n


def triangular(n):
    """S_1 -- the tower harvest. T_n = n(n+1)/2."""
    return n * (n + 1) // 2


def square(n):
    """S_2 -- the square enclosure, grown from neighbouring triangular gates."""
    return triangular(n - 1) + triangular(n)


def odd_growth(n):
    """S_3 -- the boundary growth, grown from neighbouring square plots."""
    return square(n) - square(n - 1)


def back_to_seed(x):
    """The fourth arrow that closes the cycle: inverse of n -> 2n-1."""
    return (x + 1) // 2


def centered_square(n):
    """The wild branch: neighbouring square sum, (n-1)^2 + n^2."""
    return (n - 1) ** 2 + n ** 2


def diffs(seq):
    return [seq[i + 1] - seq[i] for i in range(len(seq) - 1)]


# ── the eleven identities, as POLYNOMIAL identities not samples ─────────────
def test_identities_hold_as_polynomials():
    """Checked with sympy, so no range can hide a counterexample."""
    import sympy as sp
    n = sp.symbols('n')
    T = lambda k: k * (k + 1) / 2
    pairs = [
        ("T_n = n(n+1)/2",        T(n),                                  n * (n + 1) / 2),
        ("T_n - T_{n-1} = n",     T(n) - T(n - 1),                       n),
        ("T_{n-1} + T_n = n^2",   T(n - 1) + T(n),                       n ** 2),
        ("n^2-(n-1)^2 = 2n-1",    n ** 2 - (n - 1) ** 2,                 2 * n - 1),
        ("D^2 T_n = 1",           T(n) - 2 * T(n - 1) + T(n - 2),        1),
        ("D(n^2) = 2n-1",         n ** 2 - (n - 1) ** 2,                 2 * n - 1),
        ("D^2(n^2) = 2",          n ** 2 - 2 * (n - 1) ** 2 + (n - 2) ** 2, 2),
        ("D(2n-1) = 2",           (2 * n - 1) - (2 * (n - 1) - 1),       2),
        ("D^2(2n-1) = 0",         (2 * n - 1) - 2 * (2 * (n - 1) - 1) + (2 * (n - 2) - 1), 0),
        ("(n-1)^2+n^2",           (n - 1) ** 2 + n ** 2,                 2 * n ** 2 - 2 * n + 1),
        ("(2n-3)+(2n-1) = 4n-4",  (2 * n - 3) + (2 * n - 1),             4 * n - 4),
    ]
    for name, lhs, rhs in pairs:
        check(sp.simplify(sp.expand(lhs - rhs)) == 0, f"identity {name}",
              sp.simplify(sp.expand(lhs - rhs)), 0)
    # squares are the partial sums of the odd numbers
    k, m = sp.symbols('k m', integer=True, positive=True)
    check(sp.simplify(sp.summation(2 * k - 1, (k, 1, m)) - m ** 2) == 0,
          "sum of odds = n^2", sp.simplify(sp.summation(2 * k - 1, (k, 1, m)) - m ** 2), 0)


# ── the supplied ten-row table, cell by cell ────────────────────────────────
SUPPLIED_TABLE = [(1, 1, 1, 1), (2, 3, 4, 3), (3, 6, 9, 5), (4, 10, 16, 7),
                  (5, 15, 25, 9), (6, 21, 36, 11), (7, 28, 49, 13),
                  (8, 36, 64, 15), (9, 45, 81, 17), (10, 55, 100, 19)]


def test_the_supplied_table():
    for n, t, s, o in SUPPLIED_TABLE:
        check(seed(n) == n, f"S0({n})", seed(n), n)
        check(triangular(n) == t, f"S1({n})", triangular(n), t)
        check(square(n) == s, f"S2({n})", square(n), s)
        check(odd_growth(n) == o, f"S3({n})", odd_growth(n), o)
        # and the two field definitions agree with the closed forms
        check(square(n) == n * n, f"S2({n}) = n^2", square(n), n * n)
        check(odd_growth(n) == 2 * n - 1, f"S3({n}) = 2n-1", odd_growth(n), 2 * n - 1)


# ── the wild branch ─────────────────────────────────────────────────────────
def test_the_wild_branch():
    vals = [centered_square(n) for n in range(1, 11)]
    check(vals[:6] == [1, 5, 13, 25, 41, 61], "centered squares",
          vals[:6], [1, 5, 13, 25, 41, 61])
    d1 = diffs(vals)
    check(d1[:5] == [4, 8, 12, 16, 20], "first differences", d1[:5],
          [4, 8, 12, 16, 20])
    check(set(diffs(d1)) == {4}, "second differences constant 4",
          set(diffs(d1)), {4})
    # the closed form the write-up gives
    for n in range(1, 200):
        check(centered_square(n) == 2 * n * n - 2 * n + 1,
              f"centered_square({n})", centered_square(n), 2 * n * n - 2 * n + 1)


# ── THE FOURTH ARROW: the cycle closes, but not by the arrow given ─────────
def test_the_cycle_closes_by_the_corrected_arrow():
    for n in range(1, 500):
        # the three arrows the write-up gives, all exact
        check(triangular(n) - triangular(n - 1) == n, f"arrow 1 at {n}",
              triangular(n) - triangular(n - 1), n)
        check(triangular(n - 1) + triangular(n) == square(n), f"arrow 2 at {n}",
              triangular(n - 1) + triangular(n), square(n))
        check(square(n) - square(n - 1) == odd_growth(n), f"arrow 3 at {n}",
              square(n) - square(n - 1), odd_growth(n))
        # the corrected fourth arrow returns to the seed
        check(back_to_seed(odd_growth(n)) == n, f"arrow 4 at {n}",
              back_to_seed(odd_growth(n)), n)
    # the arrow as written is a shift inside the odd field, not a closure
    for n in range(1, 50):
        shifted = odd_growth(n) + 2
        check(shifted == odd_growth(n + 1), f"2n-1 -> 2n+1 at {n}",
              shifted, odd_growth(n + 1))
        check(shifted != n, f"the shift does not return to the seed at {n}",
              shifted, f"!= {n}")
    # and the fourth arrow is exactly the inverse of n -> 2n-1
    for n in range(1, 500):
        check(back_to_seed(2 * n - 1) == n, f"inverse at {n}",
              back_to_seed(2 * n - 1), n)


# ── parity: the one genuinely modular result, and its modulus is 4 ─────────
def test_parity_block_is_period_four():
    pattern = ['odd', 'odd', 'even', 'even']
    for start in range(1, 2000, 4):
        block = ['odd' if triangular(k) % 2 else 'even'
                 for k in range(start, start + 4)]
        check(block == pattern, f"parity block at n={start}", block, pattern)
    # n^2 preserves the parity of n
    for n in range(1, 10001):
        check((n * n) % 2 == n % 2, f"parity of {n}^2", (n * n) % 2, n % 2)
    # the modulus here is 4, and it is not 37
    check(len(pattern) == 4, "parity period", len(pattern), 4)


# ── the difference harvest is degree, not these particular crops ───────────
def test_differencing_drops_degree_by_one():
    """A degree-d polynomial field dies after d+1 differences. Degree 1..6."""
    for deg in range(1, 7):
        seq = [sum(c * k ** p for p, c in enumerate([1, 2, 3, 1, 2, 1, 3][:deg + 1]))
               for k in range(0, deg + 12)]
        cur = seq
        for step in range(deg - 1):
            cur = diffs(cur)
            # still varying: a degree-d field is NOT constant before d diffs
            check(len(set(cur)) > 1,
                  f"degree {deg} still varying after {step + 1} diffs",
                  len(set(cur)), "> 1")
        cur = diffs(cur)
        # after deg differences it is constant
        check(len(set(cur)) == 1, f"degree {deg} constant after {deg} diffs",
              set(cur), "one value")
        # and after deg+1 it is zero
        check(set(diffs(cur)) == {0}, f"degree {deg} zero after {deg + 1} diffs",
              set(diffs(cur)), {0})


# ── nothing here depends on a modulus; the identities are over Z ───────────
def test_no_modulus_dependence():
    """Every identity holds mod m for every m, because it holds over Z."""
    for m in (2, 3, 4, 7, 9, 10, 11, 37, 101):
        for n in range(1, 60):
            check((triangular(n - 1) + triangular(n) - n * n) % m == 0,
                  f"gate identity mod {m} at {n}",
                  (triangular(n - 1) + triangular(n) - n * n) % m, 0)
            check((square(n) - square(n - 1) - (2 * n - 1)) % m == 0,
                  f"boundary identity mod {m} at {n}",
                  (square(n) - square(n - 1) - (2 * n - 1)) % m, 0)
    # so no residue claim is available that the integer statement does not give


def self_test():
    tests = [test_identities_hold_as_polynomials,
             test_the_supplied_table,
             test_the_wild_branch,
             test_the_cycle_closes_by_the_corrected_arrow,
             test_parity_block_is_period_four,
             test_differencing_drops_degree_by_one,
             test_no_modulus_dependence]
    for t in tests:
        t()
        print(f"  ok  {t.__name__}")
    if FAIL:
        for f in FAIL[:20]:
            print(f"  FAIL  {f}")
        raise AssertionError(f"{len(FAIL)} check(s) failed")

    print()
    print("THE FARM")
    print()
    print("  wild mode   keep every branch:  n, T_n, n^2, 2n-1, 2n^2-2n+1, ...")
    print("  pruned mode keep the cycle:     n -> T_n -> n^2 -> 2n-1 -> n")
    print("  rhythm      grow wild -> harvest -> prune -> replant -> grow again")
    print()
    print("  CORRECT, all of it: eleven identities, checked as polynomial")
    print("  identities rather than sampled; the ten-row table in every cell;")
    print("  the wild branch 1,5,13,25,41,61 with differences 4,8,12,16,20 and")
    print("  second differences a constant 4; T_n parity odd,odd,even,even with")
    print("  period 4 to n=2000; n^2 parity = n parity to n=10000.")
    print()
    print("  ONE CORRECTION -- the fourth arrow.  '2n-1 -> 2n+1' is a shift")
    print("  inside the odd field and does not reach the seed, so as written the")
    print("  cycle does not close.  The arrow that closes it is")
    print("        x -> (x+1)/2,   since (2n-1+1)/2 = n")
    print("  the exact inverse of n -> 2n-1.  The cycle is real; the last leg")
    print("  needed replanting.  Four exact maps:")
    print("        n -> T_n -> n^2 -> 2n-1 -> n")
    print()
    print("  PRIOR ART, said up front: every field is a named sequence --")
    print("    n A000027,  T_n A000217,  n^2 A000290,  2n-1 A005408,")
    print("    2n^2-2n+1 A001844, the CENTERED SQUARES.")
    print("  T_{n-1}+T_n = n^2 and n^2-(n-1)^2 = 2n-1 are the gnomon, classical")
    print("  Nicomachus material: a square grows by an L of 2n-1 cells, so the")
    print("  squares are the partial sums of the odds.  Solid ground to build on,")
    print("  not results to establish.  The farm as a METHOD is the owner's own.")
    print()
    print("  THE DIFFERENCE HARVEST is degree, not these crops: a degree-d field")
    print("  is constant after d differences and zero after d+1, checked to d=6.")
    print()
    print("  NO 37, AND NO BASE 10.  Every identity is an identity of polynomials")
    print("  over Z, so it holds mod every modulus -- checked at m = 2,3,4,7,9,10,")
    print("  11,37,101 -- and holds there because it holds over Z.  The mod-37")
    print("  version therefore carries nothing the integer version does not, and")
    print("  no orbit or residue claim is made.  The one genuinely modular result")
    print("  in the farm is the parity block, and its modulus is 4.")


if __name__ == "__main__":
    self_test()
