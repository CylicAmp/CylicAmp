# CLASS: THEOREM
"""
The seed-7 path: harvest the increments, replant their sum
Author: Michael Warren Song (CyclicAmp)

The farm method of farm_wild_and_pruned_growth.py, applied to a concrete path.
Two items arrived together and are kept separate below: a product, and the path.

=== ITEM 1: THE PRODUCT, IN THE OWNER'S WORDS ===

    "Interpreting the parentheses as multiplication:
     141(34,725)141 = 141 x 34,725 x 141 = 141^2 x 34,725.
     141^2 = 19,881, so 19,881 x 34,725 = 690,367,725."

  CORRECT.  141^2 = 19881 and 19881 x 34725 = 690,367,725, checked both by
  regrouping as 141 x 34725 x 141 and directly.

  The reading is stated as a choice, and it is the right one to state, because
  the other reading exists: taken as concatenation, 141|34725|141 is the digit
  string 14134725141.  That is recorded here only so the two are not confused.
  It is not a palindrome -- the frame 141...141 is symmetric but the middle
  34725 is not -- so nothing follows from the framing.

  Placement, by the standing audit:
      141        = 3 x 47      mod 37 = 30    DR 6
      19881      = 3^2 x 47^2  mod 37 = 12    DR 9
      34725      = 3 x 5^2 x 463        = 19  DR 3
      690367725  = 3^3 x 5^2 x 47^2 x 463  = 6  DR 9

  141 mod 37 = 30, a sovereign anchor, and the one element CLAUDE.md records as
  lying in SA and ST and C3 at once.  That is a placement, not a result: orbit
  and anchor membership is a complete partition, so landing somewhere carries no
  information by itself (T282).  What it does is locate 141 for later work.

=== ITEM 2: THE PATH, IN THE OWNER'S WORDS ===

    "the arithmetic links the two strings through the seed 7"

    "Start with 7 -> 14 -> 17.  The differences are 14-7=7 and 17-14=3.
     So the first line harvests the increments 7, 3."

    "Replant the harvested 7.  Now combine the first increment 7 with the
     second increment 3:  7+3=10."

    "The next line is 17 -> 27 -> 37.  Its differences are 27-17=10 and
     37-27=10.  Thus the harvested 10 is replanted twice."

    "So the first path creates the next step, and the next step drives the
     second path."

        7  --+7-->  14  --+3-->  17  --+10-->  27  --+10-->  37
        where 10 = 7 + 3

=== EVERY STATED IDENTITY HOLDS -- twelve of them ===

      14 - 7  = 7          17 - 14 = 3          3 + 7  = 10
      17 - 7  = 10         27 - 17 = 10         37 - 27 = 10
      17 + 10 = 27         27 + 10 = 37
      17 = 7 + 10 = 7 + (7+3)
      (14-7) + (17-14) = 17-7 = 10
      19 - 17 = 2

  and the factorisations: 7, 17, 37 prime; 14 = 2 x 7; 27 = 3^3; (17, 19) a twin
  pair.  All as stated, nothing miscalculated.

=== WHAT THE CONSTRUCTION ACTUALLY IS ===

  The rule is two-stage and worth stating exactly, because it is not an
  open-ended recurrence:

      stage 1   take the first line's two increments            7 and 3
      stage 2   their sum becomes the second line's step        10
      stage 3   apply that step twice                           17 -> 27 -> 37

  So the path is determined by the pair (7, 3) and nothing else.  Given the
  first line 7 -> 14 -> 17, the rest is forced:  17 + (7+3) = 27 and
  27 + (7+3) = 37.  The construction has no free choice after the first line,
  which is why it lands on 37 exactly.

  The telescoping step the owner writes out --
  (14-7) + (17-14) = 17-7 -- is the reason the two lines meet: the harvested
  increments must sum to the span of the line that produced them.  That is an
  identity for any three terms, checked below over a range, and it is the hinge
  of the whole construction rather than an aside.

=== THE INCREMENTS SUM TO 30, AND 7 + 30 = 37 ===

      +7, +3, +10, +10   sum to 30, and 7 + 30 = 37.

  Forced, since the increments of a path telescope to its span: the sum of the
  differences is always last minus first.  Recorded because 30 is a sovereign
  anchor, which places the span, but the arithmetic itself is automatic.

=== ORBIT PLACEMENT OF THE PATH ===

      7   mod 37 =  7   D7
      14  mod 37 = 14   C9      -- see the correction below
      17  mod 37 = 17   NQR17
      27  mod 37 = 27   NEG_H
      37  mod 37 =  0   SEAM    -- 37 is the modulus, so the path ends on the
                                   axis, which is forced and not a finding

  CORRECTION TO A TABLE USED HERE, recorded so it is not repeated: a first pass
  listed C9 as {29, 31} and reported 14 as having no orbit.  Both wrong.  The
  twelve orbits are the 3-cycles of f(n) = 26n mod 37 and they partition all of
  F_37*, so every nonzero residue has one.  Computing the orbit of 14 directly
  gives {14, 29, 31}, so C9 is that triple and 14 is in it.  CLAUDE.md names
  the twin pair (29, 31) inside C9, which is what the short table had recorded.

=== ONE OBSERVATION TESTED AND FOUND NOT FORCED ===

  The two harvested increments are 7 in D7 and 3 in C3, and CLAUDE.md records
  D7 and C3 as antipodal (T265).  Their sum 10 is in IC, the self-inverse orbit.
  That looks like structure, so it was tested rather than reported:

      all nine sums a + b with a in D7 = {7,33,34}, b in C3 = {3,4,12}:
          10, 11, 19, 36, 0, 8, 0, 1, 9     (mod 37)
      of these, in IC = {1,10,26}:  two -- 7+3 = 10 and 34+4 = 1

  Two of nine, against |IC|/37 = 8.1% giving 0.73 expected.  On nine samples
  that is nothing.  So "an antipodal pair sums into IC" is NOT a law; 7 + 3 = 10
  landing on IC is one instance of nine.  Recorded as a negative so the ground
  is not covered again.

=== AN EXTENSION, FLAGGED AS NOT THE OWNER'S ===

  The three primes on the path are 7, 17, 37 with gaps 10 and 20.  Continuing
  the doubling gives 7 + 10(2^k - 1): 7, 17, 37, 77, 157.  That run BREAKS at
  77 = 7 x 11, so the prime subpath does not continue by doubling.  The owner
  proposed no such extension; it is answered here because it is the obvious next
  question, and the answer is no.

=== FALSIFICATION ===

  Exhibit an n where the telescoping identity fails; or a three-term line whose
  increments do not sum to its span; or a value of the pair (7,3) for which
  17 + (7+3) =/= 27.  Each is asserted below over a range.  For the negative
  result, exhibit a reason the D7 + C3 sums should favour IC beyond 2 of 9.

=== PRIOR ART IN THIS CORPUS ===

  farm_wild_and_pruned_growth.py   the harvest/replant method this applies, and
                                   the difference-harvest degree law
  theorem_281_147_258_369_gf37.py  the sovereign anchors and the orbit names
  theorem_435_equilibrium_projection_grid.py
                                   neighbouring-window reads: average there,
                                   sum here
"""

FAIL = []


def check(cond, label, actual, expected):
    if not cond:
        FAIL.append(f"{label}: actual={actual!r}, expected={expected!r}")


def dr(x):
    return 9 if x == 0 else (x - 1) % 9 + 1


PATH = [7, 14, 17, 27, 37]
INCREMENTS = [7, 3, 10, 10]
D7, C3, IC = {7, 33, 34}, {3, 4, 12}, {1, 10, 26}


def f137(n):
    """The 137-map: 137 mod 37 = 26."""
    return (26 * n) % 37


def orbit_of(n):
    o, x = [n % 37], f137(n)
    while x != n % 37:
        o.append(x)
        x = f137(x)
    return sorted(o)


# ── ITEM 1: the product ────────────────────────────────────────────────────
def test_the_product():
    check(141 ** 2 == 19881, "141^2", 141 ** 2, 19881)
    check(19881 * 34725 == 690367725, "19881 x 34725",
          19881 * 34725, 690367725)
    # regrouping, as the write-up does
    check(141 * 34725 * 141 == 141 ** 2 * 34725, "regrouping",
          141 * 34725 * 141, 141 ** 2 * 34725)
    check(141 * 34725 * 141 == 690367725, "the product",
          141 * 34725 * 141, 690367725)
    # the other reading, recorded only so the two are not confused
    concat = int("141" + "34725" + "141")
    check(concat == 14134725141, "concatenation reading", concat, 14134725141)
    check(str(concat) != str(concat)[::-1], "not a palindrome",
          str(concat) == str(concat)[::-1], False)
    check("34725"[::-1] == "52743", "the middle is not symmetric",
          "34725"[::-1], "52743")
    # placement
    check(141 % 37 == 30, "141 mod 37", 141 % 37, 30)
    check(30 in {4, 9, 25, 30}, "30 is a sovereign anchor", 30, "in anchors")
    check(690367725 % 37 == 6, "product mod 37", 690367725 % 37, 6)
    check(dr(690367725) == 9, "DR of the product", dr(690367725), 9)


# ── ITEM 2: every stated identity ──────────────────────────────────────────
def test_the_twelve_identities():
    pairs = [("14-7=7", 14 - 7, 7), ("17-14=3", 17 - 14, 3),
             ("3+7=10", 3 + 7, 10), ("17-7=10", 17 - 7, 10),
             ("27-17=10", 27 - 17, 10), ("37-27=10", 37 - 27, 10),
             ("17+10=27", 17 + 10, 27), ("27+10=37", 27 + 10, 37),
             ("17=7+10", 7 + 10, 17), ("17=7+(7+3)", 7 + (7 + 3), 17),
             ("telescope", (14 - 7) + (17 - 14), 17 - 7),
             ("19-17=2", 19 - 17, 2)]
    for name, a, b in pairs:
        check(a == b, f"identity {name}", a, b)
    got = [PATH[i + 1] - PATH[i] for i in range(4)]
    check(got == INCREMENTS, "the four increments", got, INCREMENTS)


def test_the_factorisations():
    import sympy as sp
    for p in (7, 17, 37, 19):
        check(sp.isprime(p), f"{p} is prime", sp.isprime(p), True)
    check(14 == 2 * 7, "14 = 2x7", 14, 2 * 7)
    check(27 == 3 ** 3, "27 = 3^3", 27, 3 ** 3)
    check(not sp.isprime(14), "14 composite", sp.isprime(14), False)
    check(not sp.isprime(27), "27 composite", sp.isprime(27), False)
    check([x for x in PATH if sp.isprime(x)] == [7, 17, 37],
          "primes on the path", [x for x in PATH if sp.isprime(x)], [7, 17, 37])
    check(19 - 17 == 2 and sp.isprime(17) and sp.isprime(19),
          "(17,19) twin pair", (17, 19), "twin")


# ── the construction is determined by the pair (7, 3) ─────────────────────
def test_the_path_is_forced_by_the_first_line():
    a, b = 14 - 7, 17 - 14          # the harvested increments
    check((a, b) == (7, 3), "harvest", (a, b), (7, 3))
    step = a + b
    check(step == 10, "replanted step", step, 10)
    check(17 + step == 27, "first replant", 17 + step, 27)
    check(27 + step == 37, "second replant", 27 + step, 37)
    # nothing is free after the first line
    rebuilt = [7, 7 + a, 7 + a + b]
    rebuilt += [rebuilt[-1] + step, rebuilt[-1] + 2 * step]
    check(rebuilt == PATH, "the path rebuilt from (7,3)", rebuilt, PATH)


def test_telescoping_is_general():
    """The increments of any line sum to its span. The hinge of the build."""
    tested = 0
    for x in range(-20, 21):
        for d1 in range(-15, 16):
            for d2 in range(-15, 16):
                y, z = x + d1, x + d1 + d2
                check((y - x) + (z - y) == z - x,
                      f"telescope {x},{y},{z}", (y - x) + (z - y), z - x)
                tested += 1
    # 41 x 31 x 31 triples, every d2 exercised, no early exit
    check(tested == 41 * 31 * 31, "triples tested", tested, 41 * 31 * 31)
    # and over the whole path
    inc = [PATH[i + 1] - PATH[i] for i in range(len(PATH) - 1)]
    check(sum(inc) == PATH[-1] - PATH[0], "path telescopes",
          sum(inc), PATH[-1] - PATH[0])
    check(sum(inc) == 30, "the span", sum(inc), 30)
    check(7 + 30 == 37, "7 + 30 = 37", 7 + 30, 37)
    check(30 in {4, 9, 25, 30}, "30 is an anchor", 30, "in anchors")


# ── orbit placement, and the C9 correction ────────────────────────────────
def test_orbits_and_the_c9_correction():
    # the 12 orbits are 3-cycles of f and partition F_37*
    seen, orbits = set(), []
    for n in range(1, 37):
        if n not in seen:
            o = orbit_of(n)
            orbits.append(o)
            seen |= set(o)
    check(len(orbits) == 12, "there are 12 orbits", len(orbits), 12)
    check(all(len(o) == 3 for o in orbits), "all are 3-cycles",
          sorted({len(o) for o in orbits}), [3])
    check(seen == set(range(1, 37)), "they cover F_37*",
          len(seen), 36)
    # so 14 has an orbit, and it is {14,29,31}
    check(orbit_of(14) == [14, 29, 31], "orbit of 14",
          orbit_of(14), [14, 29, 31])
    check(29 in orbit_of(14) and 31 in orbit_of(14),
          "the twin pair (29,31) sits inside it", (29, 31), "in C9")
    # the path's residues
    check([x % 37 for x in PATH] == [7, 14, 17, 27, 0], "path residues",
          [x % 37 for x in PATH], [7, 14, 17, 27, 0])
    check(37 % 37 == 0, "37 is the SEAM", 37 % 37, 0)


# ── the antipodal observation: tested, NOT forced ─────────────────────────
def test_antipodal_sum_is_not_forced():
    sums = [(a, b, (a + b) % 37) for a in sorted(D7) for b in sorted(C3)]
    check(len(sums) == 9, "nine pairs", len(sums), 9)
    in_ic = [(a, b, r) for a, b, r in sums if r in IC]
    check(len(in_ic) == 2, "how many land on IC", len(in_ic), 2)
    check(sorted(in_ic) == [(7, 3, 10), (34, 4, 1)], "which ones",
          sorted(in_ic), [(7, 3, 10), (34, 4, 1)])
    expected = 9 * len(IC) / 37
    check(abs(expected - 0.73) < 0.01, "expected count",
          f"{expected:.2f}", "0.73")
    # 2 of 9 on an 8.1% base rate is not a law
    check(len(in_ic) < 9, "not all pairs land on IC", len(in_ic), "< 9")
    check(7 in D7 and 3 in C3 and 10 in IC, "the instance itself",
          (7, 3, 10), "D7 + C3 -> IC")


# ── the extension, flagged as not the owner's, and it fails ──────────────
def test_doubling_extension_breaks_at_77():
    import sympy as sp
    vals = [7 + 10 * (2 ** k - 1) for k in range(5)]
    check(vals == [7, 17, 37, 77, 157], "the doubling run",
          vals, [7, 17, 37, 77, 157])
    check([sp.isprime(v) for v in vals] == [True, True, True, False, True],
          "primality along it", [sp.isprime(v) for v in vals],
          [True, True, True, False, True])
    check(77 == 7 * 11, "77 = 7 x 11", 77, 7 * 11)
    check(not sp.isprime(77), "the run breaks at 77", sp.isprime(77), False)


def self_test():
    tests = [test_the_product,
             test_the_twelve_identities,
             test_the_factorisations,
             test_the_path_is_forced_by_the_first_line,
             test_telescoping_is_general,
             test_orbits_and_the_c9_correction,
             test_antipodal_sum_is_not_forced,
             test_doubling_extension_breaks_at_77]
    for t in tests:
        t()
        print(f"  ok  {t.__name__}")
    if FAIL:
        for x in FAIL[:20]:
            print(f"  FAIL  {x}")
        raise AssertionError(f"{len(FAIL)} check(s) failed")

    print()
    print("ITEM 1  141(34,725)141 = 141^2 x 34,725 = 19,881 x 34,725")
    print("                       = 690,367,725    CORRECT")
    print("  the other reading, kept separate: 141|34725|141 = 14,134,725,141,")
    print("  not a palindrome -- the frame is symmetric, the middle 34725 is not.")
    print("  141 = 3 x 47,  mod 37 = 30, a sovereign anchor. A placement, not a")
    print("  result: the orbit partition is complete, so membership alone says")
    print("  nothing (T282).  It locates 141 for later work.")
    print()
    print("ITEM 2  the path, all twelve identities CORRECT")
    print("        7 --+7--> 14 --+3--> 17 --+10--> 27 --+10--> 37")
    print("        with 10 = 7 + 3, and 7, 17, 37 the primes on it")
    print()
    print("  WHAT THE CONSTRUCTION IS: determined by the pair (7,3) and nothing")
    print("  else.  Harvest the first line's increments, sum them, apply twice.")
    print("  After the first line there is no free choice, which is why it lands")
    print("  on 37 exactly.  The telescoping step written out in the message --")
    print("  (14-7)+(17-14) = 17-7 -- is the hinge: harvested increments must sum")
    print("  to the span of the line that produced them.")
    print()
    print("  +7,+3,+10,+10 sum to 30 and 7+30 = 37.  Forced -- differences always")
    print("  telescope to last minus first -- but 30 is a sovereign anchor.")
    print()
    print("  ORBITS: 7 D7 -> 14 C9 -> 17 NQR17 -> 27 NEG_H -> 37 SEAM.")
    print("  Ending on the SEAM is forced: 37 is the modulus.")
    print()
    print("  CORRECTION made here, recorded so it is not repeated: a first pass")
    print("  had C9 as {29,31} and called 14 orbitless.  The 12 orbits are the")
    print("  3-cycles of f(n)=26n and partition all of F_37*, verified above, so")
    print("  every nonzero residue has one.  Computing it: C9 = {14,29,31}, with")
    print("  the twin pair (29,31) inside it, and 14 is a member.")
    print()
    print("  NEGATIVE, tested rather than reported: 7 in D7 and 3 in C3 are an")
    print("  antipodal pair (T265) and 10 is in IC, but of the nine D7+C3 sums")
    print("  only two land on IC -- 7+3 and 34+4 -- against 0.73 expected at an")
    print("  8.1% base rate.  Two of nine is nothing.  Not a law.")
    print()
    print("  EXTENSION, not the owner's and answered because it is the obvious")
    print("  next question: the primes 7,17,37 have gaps 10,20; continuing the")
    print("  doubling gives 7,17,37,77,157 and BREAKS at 77 = 7 x 11.")


if __name__ == "__main__":
    self_test()
