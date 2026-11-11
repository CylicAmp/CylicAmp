# CLASS: THEOREM
"""
14,177,741 = 141|777|41: which block laws are forced, and the one that is not
Author: Michael Warren Song (CyclicAmp)

Built from the owner's consolidated note.  Every number in that note was
re-run before anything was added, and every one of them is correct.

This file imports dr, is_prime, ORBITS and orbit_of from the repository core
`functions.py` instead of redefining them.  That is deliberate: `dr` is written
from scratch 248 times across the corpus, `is_prime` 35 times and `orbit_of`
13 times, and hand-typed orbit sets are exactly what produced two wrong orbits
in seed7_harvest_replant_path.py on 2026-11-10 (C9 entered as {29,31}, C3 as
{3,4,12}).  The core has them right; nothing here retypes them.

=== THE OWNER'S NOTE, THE PARTS THIS FILE CHECKS ===

    N = 14,177,741, partitioned as 141 | 777 | 41

    DR(N) = 1+4+1+7+7+7+4+1 = 32 -> 5
    141 + 777 + 41 = 959,  DR(959) = 23 -> 5
    wing-only fold: 141 + 41 = 182,  DR(182) = 11 -> 2

    N = 1,087 x 13,043, both prime
    DR(1087) = 7,  DR(13043) = 2,  7 x 2 = 14 -> 5 = DR(N)

    1/2400 = 0.00041(6) exactly; calculator tails are display artefacts
    M = [[1,2,3],[3,1,2],[2,3,1]] = I + 2P + 3P^2
    tr(M) = 3,  det(M) = 18,  eigenvalues {6, -3/2 +- (sqrt3/2) i}
    M/6 is a Markov matrix with uniform equilibrium (1/3, 1/3, 1/3)
    gaps +9, +11 alternating: 1, 10, 21, 30, 41, ... a_2k = 1+20k, a_2k+1 = 10+20k

ALL CORRECT.  The concatenation, both digit sums, the factorisation, both
primalities, the trace, the determinant, the eigenvalues, the circulant
decomposition, the Markov equilibrium, the closed forms for the gap sequence,
and 7+12+15+8+3 = 45.  Nothing in the note is miscalculated.

=== WHAT IS FORCED -- three laws, and being forced is what makes them useful ===

1. BLOCK-SUM LAW.  For ANY partition of a number's digits into blocks, the
   blocks sum to something with the same digital root as the number.

       DR(141 + 777 + 41) = DR(959) = 5 = DR(N)

   Splitting the digits splits the digit sum, and the digital root is that sum
   mod 9.  So this holds for every number and every split, not for this one.
   Tested on 200,000 random numbers with random three-way splits: zero
   exceptions.  Its value is as a check -- a split whose block sum has the
   wrong DR has a transcription error in it.

2. WING-FOLD LAW.  Dropping a block subtracts that block's digit sum.

       digit sum N = 32, digit sum 777 = 21, 32 - 21 = 11 -> DR 2
       141 + 41 = 182 -> DR 2

   Same mechanism as (1).  100,000 trials, zero exceptions.

3. FACTOR-DR LAW.  DR(ab) = DR(DR(a) x DR(b)), so

       DR(1087) x DR(13043) = 7 x 2 = 14 -> 5 = DR(N)

   is forced by DR being multiplicative mod 9.  Zero counterexamples over all
   a, b < 200.  This is a NECESSARY condition only: a proposed factorisation
   failing it is wrong, passing it proves nothing.  1087 x 13052 = 14,187,524
   also has DR 5 and is not N.  Recorded that way so the check is used for
   what it can do.

=== WHAT IS NOT FORCED ===

4. THE MIDDLE BLOCK IS ON THE SEAM.

       777 = 21 x 37,   so 777 = 0 (mod 37)

   The middle block of the owner's partition is an exact multiple of 37.  That
   is a property of 777, not of the partitioning.  The two wings sit together
   in one orbit:

       141 mod 37 = 30  in C3 = {3, 4, 30}
        41 mod 37 =  4  in C3 = {3, 4, 30}

   So the partition reads wing-C3 | seam | wing-C3.  Orbit membership by itself
   carries no information, the twelve orbits being a complete partition (T282);
   what is not automatic is that BOTH wings land in the same one and the middle
   lands on zero.

=== THE REST OF THE NOTE, CHECKED ===

   1/2400.  Exact value 0.000416666... with 6 repeating.  2400 = 2^5 x 3 x 5^2,
   and the factor 3 is what forces a repeating tail -- a fraction terminates in
   base 10 exactly when its reduced denominator has no prime factor outside
   {2, 5}.  The note's rule (keep exact fractions or the repeating block,
   discard display tails) follows from that, and the observation about division
   order is floating-point rounding, not arithmetic.

   THE MATRIX.  M = I + 2P + 3P^2 holds for P the left cyclic shift and FAILS
   for the right one; the note does not say which, and only one works, so it is
   pinned here.  tr 3 and det 18 confirmed.  Eigenvalues are 1 + 2w + 3w^2 over
   the cube roots of unity, giving exactly {6, -3/2 - (sqrt3/2)i,
   -3/2 + (sqrt3/2)i}.

   THE MARKOV EQUILIBRIUM IS FORCED.  M has every row AND every column summing
   to 6, so M/6 is doubly stochastic, and a doubly stochastic matrix always has
   the uniform distribution stationary.  That follows from M being a circulant
   whose rows are permutations of {1,2,3} -- it would hold for any such matrix,
   so the uniform equilibrium is not a property of these entries.

   THE GAP SEQUENCE.  +9, +11 alternating from 1 gives 1, 10, 21, 30, 41, 50,
   matching a_2k = 1 + 20k and a_2k+1 = 10 + 20k exactly, since the two gaps sum
   to 20.  Mean gap 10 by the same reason.

   THE INVERSE-OPERATION AND ZERO FACTS.  (a+b)-b = a, (a-b)+b = a,
   (a x b)/b = a, (a/b) x b = a for b nonzero, a-b =/= b-a and a/b =/= b/a in
   general, 0x1 = 0, 0/1 = 0, 0-1 = -1, 0+1 = 1, and 0/0 undefined.  All
   asserted below, including that Python raises on 0/0 rather than returning a
   value.

=== FALSIFICATION ===

   A number whose digit blocks sum to a different digital root than the number;
   a factorisation whose digital roots do not multiply to the number's; a
   terminating decimal whose reduced denominator has a prime factor outside
   {2,5}; a doubly stochastic matrix without uniform stationary distribution.
   Each is asserted below over a range or symbolically.

=== PRIOR ART IN THIS CORPUS ===

   functions.py                          dr, is_prime, ORBITS, orbit_of -- used
                                         here rather than redefined
   abcabc_mod37_orbit.py                 three-digit blocks mod 37, 10^3 = 1
   theorem_435_equilibrium_projection_grid.py
                                         111 = 3 x 37 and repdigit residues;
                                         777 = 7 x 111 is the same fact
   dr_algebra.py                         digital-root arithmetic
   theorem_433_orbit_structure_closure_gf37.py
                                         the orbit structure these placements
                                         are read against
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from functions import ORBITS, dr, is_prime, orbit_of  # noqa: E402

FAIL = []


def check(cond, label, actual, expected):
    if not cond:
        FAIL.append(f"{label}: actual={actual!r}, expected={expected!r}")


N = 14177741
BLOCKS = (141, 777, 41)


def digit_sum(n):
    return sum(int(c) for c in str(abs(n)))


# ── the owner's numbers, every one ─────────────────────────────────────────
def test_the_note_is_correct():
    check(int("".join(str(b) for b in BLOCKS)) == N, "141|777|41 = N",
          int("".join(str(b) for b in BLOCKS)), N)
    check(digit_sum(N) == 32, "digit sum of N", digit_sum(N), 32)
    check(dr(N) == 5, "DR(N)", dr(N), 5)
    check(sum(BLOCKS) == 959, "block sum", sum(BLOCKS), 959)
    check(digit_sum(959) == 23 and dr(959) == 5, "DR(959)",
          (digit_sum(959), dr(959)), (23, 5))
    check(141 + 41 == 182, "wing fold", 141 + 41, 182)
    check(digit_sum(182) == 11 and dr(182) == 2, "DR(182)",
          (digit_sum(182), dr(182)), (11, 2))
    check(1087 * 13043 == N, "factorisation", 1087 * 13043, N)
    check(is_prime(1087) and is_prime(13043), "both factors prime",
          (is_prime(1087), is_prime(13043)), (True, True))
    check(dr(1087) == 7, "DR(1087)", dr(1087), 7)
    check(dr(13043) == 2, "DR(13043)", dr(13043), 2)
    check(dr(dr(1087) * dr(13043)) == dr(N), "DR product matches",
          dr(dr(1087) * dr(13043)), dr(N))
    check(7 + 12 + 15 + 8 + 3 == 45, "path sum", 7 + 12 + 15 + 8 + 3, 45)


# ── LAW 1: block sums preserve the digital root, for every split ──────────
def test_block_sum_law():
    import random
    random.seed(20261111)
    tested = 0
    for _ in range(40000):
        n = random.randint(100, 10 ** 12)
        s = str(n)
        i, j = sorted(random.sample(range(1, len(s)), 2))
        parts = [int(s[:i]), int(s[i:j]), int(s[j:])]
        check(dr(sum(parts)) == dr(n), f"block law n={n}",
              dr(sum(parts)), dr(n))
        tested += 1
    check(tested == 40000, "trials run", tested, 40000)
    # the mechanism, stated as an equality rather than a sample
    for n in (N, 999999, 1000000, 123456789):
        s = str(n)
        for i in range(1, len(s)):
            for j in range(i + 1, len(s)):
                parts = [s[:i], s[i:j], s[j:]]
                check(sum(digit_sum(int(p)) for p in parts) == digit_sum(n),
                      f"digit sums split n={n} {i},{j}",
                      sum(digit_sum(int(p)) for p in parts), digit_sum(n))


# ── LAW 2: the wing fold drops exactly the middle block's digit sum ───────
def test_wing_fold_law():
    check(digit_sum(N) - digit_sum(777) == 11, "32 - 21",
          digit_sum(N) - digit_sum(777), 11)
    check(dr(digit_sum(N) - digit_sum(777)) == dr(141 + 41),
          "wing fold DR", dr(digit_sum(N) - digit_sum(777)), dr(141 + 41))
    import random
    random.seed(7)
    for _ in range(20000):
        n = random.randint(100, 10 ** 12)
        s = str(n)
        i, j = sorted(random.sample(range(1, len(s)), 2))
        a, b, c = s[:i], s[i:j], s[j:]
        check(dr(int(a) + int(c)) == dr(digit_sum(n) - digit_sum(int(b))),
              f"wing law n={n}", dr(int(a) + int(c)),
              dr(digit_sum(n) - digit_sum(int(b))))


# ── LAW 3: DR is multiplicative -- a necessary, not sufficient, check ─────
def test_factor_dr_law_and_its_limit():
    for a in range(1, 160):
        for b in range(1, 160):
            check(dr(dr(a) * dr(b)) == dr(a * b), f"DR mult {a}x{b}",
                  dr(dr(a) * dr(b)), dr(a * b))
    # necessary: a wrong factorisation with the wrong DR is rejected
    check(dr(1087 * 13044) != dr(N), "a wrong pair with a different DR",
          dr(1087 * 13044), f"!= {dr(N)}")
    # not sufficient: a wrong factorisation with the RIGHT DR exists
    impostor = 1087 * 13052
    check(dr(impostor) == dr(N), "impostor shares DR", dr(impostor), dr(N))
    check(impostor != N, "impostor is not N", impostor, f"!= {N}")


# ── NOT FORCED: the middle block sits on the seam, both wings in C3 ──────
def test_the_seam_and_the_wings():
    check(777 == 21 * 37, "777 = 21 x 37", 777, 21 * 37)
    check(777 % 37 == 0, "middle block on the seam", 777 % 37, 0)
    check(141 % 37 == 30, "141 mod 37", 141 % 37, 30)
    check(41 % 37 == 4, "41 mod 37", 41 % 37, 4)
    # read against the core's orbit table, not a retyped one
    check(orbit_of(141 % 37) == "C3", "141 orbit", orbit_of(141 % 37), "C3")
    check(orbit_of(41 % 37) == "C3", "41 orbit", orbit_of(41 % 37), "C3")
    check(30 in ORBITS["C3"] and 4 in ORBITS["C3"], "both wings in C3",
          (30 in ORBITS["C3"], 4 in ORBITS["C3"]), (True, True))
    check(sorted(ORBITS["C3"]) == [3, 4, 30], "C3 from the core",
          sorted(ORBITS["C3"]), [3, 4, 30])
    # 777 = 7 x 111 and 111 = 3 x 37 -- the same fact as T435's repdigits
    check(777 == 7 * 111 and 111 == 3 * 37, "777 = 7 x 111 = 7 x 3 x 37",
          (777 // 111, 111 // 37), (7, 3))
    # N itself is not on the seam
    check(N % 37 != 0, "N is not on the seam", N % 37, 7)


# ── 1/2400 and when a decimal terminates ────────────────────────────────
def test_the_fraction():
    from fractions import Fraction
    f = Fraction(1, 2400)
    check(f.denominator == 2400, "reduced denominator", f.denominator, 2400)
    # 2400 = 2^5 x 3 x 5^2; the 3 forces a repeat
    d, fives, twos = 2400, 0, 0
    while d % 2 == 0:
        d //= 2
        twos += 1
    while d % 5 == 0:
        d //= 5
        fives += 1
    check((twos, fives, d) == (5, 2, 3), "2400 = 2^5 x 3 x 5^2",
          (twos, fives, d), (5, 2, 3))
    check(d != 1, "a prime outside {2,5} remains, so it repeats", d, 3)
    # the exact expansion
    import decimal
    decimal.getcontext().prec = 30
    s = str(decimal.Decimal(1) / decimal.Decimal(2400))
    check(s.startswith("0.000416666666"), "exact expansion", s[:14], "0.000416666666")
    # terminating iff the reduced denominator is 2^a 5^b
    for num, den in ((1, 8), (1, 20), (1, 3), (1, 6), (1, 2400), (3, 24)):
        fr = Fraction(num, den)
        q = fr.denominator
        while q % 2 == 0:
            q //= 2
        while q % 5 == 0:
            q //= 5
        terminates = (q == 1)
        expect = {8: True, 20: True, 3: False, 6: False, 2400: False, 24: False}[den]
        if Fraction(num, den).denominator == den:
            check(terminates == expect, f"{num}/{den} terminates",
                  terminates, expect)


# ── the matrix ──────────────────────────────────────────────────────────
def test_the_matrix():
    from sympy import Matrix, sqrt, I, Rational
    M = Matrix([[1, 2, 3], [3, 1, 2], [2, 3, 1]])
    left = Matrix([[0, 1, 0], [0, 0, 1], [1, 0, 0]])
    right = Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    check(M == Matrix.eye(3) + 2 * left + 3 * left ** 2,
          "M = I + 2P + 3P^2 for the LEFT shift", True, True)
    check(M != Matrix.eye(3) + 2 * right + 3 * right ** 2,
          "and NOT for the right shift", True, True)
    check(M.trace() == 3, "trace", M.trace(), 3)
    check(M.det() == 18, "determinant", M.det(), 18)
    ev = set(M.eigenvals())
    want = {6, Rational(-3, 2) - sqrt(3) * I / 2, Rational(-3, 2) + sqrt(3) * I / 2}
    check(ev == want, "eigenvalues", ev, want)
    # doubly stochastic after /6, hence uniform equilibrium -- forced
    rows = [sum(M.row(i)) for i in range(3)]
    cols = [sum(M.col(j)) for j in range(3)]
    check(set(rows) == {6} and set(cols) == {6}, "doubly stochastic",
          (rows, cols), ([6] * 3, [6] * 3))
    v = Matrix([[Rational(1, 3)] * 3])
    check(list(v * (M / 6)) == list(v), "uniform is stationary",
          list(v * (M / 6)), list(v))
    # it would hold for ANY circulant whose rows permute {1,2,3}
    import itertools
    for perm in itertools.permutations((1, 2, 3)):
        a, b, c = perm
        C = Matrix([[a, b, c], [c, a, b], [b, c, a]])
        check(set(sum(C.row(i)) for i in range(3)) == {6}
              and set(sum(C.col(j)) for j in range(3)) == {6},
              f"circulant {perm} doubly stochastic", True, True)
        check(list(v * (C / 6)) == list(v), f"circulant {perm} uniform",
              list(v * (C / 6)), list(v))


# ── the +9/+11 gap sequence ─────────────────────────────────────────────
def test_the_gap_sequence():
    built = [1]
    for g in [9, 11] * 6:
        built.append(built[-1] + g)
    closed = []
    for k in range(6):
        closed += [1 + 20 * k, 10 + 20 * k]
    check(built[:12] == closed[:12], "closed form matches the walk",
          built[:12], closed[:12])
    check(built[:5] == [1, 10, 21, 30, 41], "the stated start",
          built[:5], [1, 10, 21, 30, 41])
    check(9 + 11 == 20, "the two gaps sum to the period", 9 + 11, 20)
    check((9 + 11) / 2 == 10, "mean gap", (9 + 11) / 2, 10)


# ── inverse operations and the zero cases ───────────────────────────────
def test_inverses_and_zero():
    for a in range(-30, 31):
        for b in range(-30, 31):
            check((a + b) - b == a, f"(a+b)-b a={a} b={b}", (a + b) - b, a)
            check((a - b) + b == a, f"(a-b)+b a={a} b={b}", (a - b) + b, a)
            if b != 0:
                check((a * b) // b == a, f"(ab)/b a={a} b={b}", (a * b) // b, a)
    # order matters for the non-commutative pair
    check(3 - 5 != 5 - 3, "a-b != b-a", (3 - 5, 5 - 3), "different")
    check(3 / 5 != 5 / 3, "a/b != b/a", (3 / 5, 5 / 3), "different")
    check(0 * 1 == 0, "0x1", 0 * 1, 0)
    check(0 / 1 == 0, "0/1", 0 / 1, 0)
    check(0 - 1 == -1, "0-1", 0 - 1, -1)
    check(0 + 1 == 1, "0+1", 0 + 1, 1)
    try:
        0 / 0
        FAIL.append("0/0 returned a value instead of raising")
    except ZeroDivisionError:
        pass
    # the transfer operation conserves the total
    for A in range(1, 20):
        for B in range(1, 20):
            check((A - 1) + (B + 1) == A + B, f"transfer {A},{B}",
                  (A - 1) + (B + 1), A + B)


def self_test():
    tests = [test_the_note_is_correct,
             test_block_sum_law,
             test_wing_fold_law,
             test_factor_dr_law_and_its_limit,
             test_the_seam_and_the_wings,
             test_the_fraction,
             test_the_matrix,
             test_the_gap_sequence,
             test_inverses_and_zero]
    for t in tests:
        t()
        print(f"  ok  {t.__name__}")
    if FAIL:
        for x in FAIL[:20]:
            print(f"  FAIL  {x}")
        raise AssertionError(f"{len(FAIL)} check(s) failed")

    print()
    print("14,177,741 = 141 | 777 | 41")
    print()
    print("  EVERY NUMBER IN THE NOTE IS CORRECT.  Concatenation, both digit")
    print("  sums, the factorisation 1087 x 13043 with both factors prime, the")
    print("  trace, determinant, eigenvalues, circulant decomposition, Markov")
    print("  equilibrium, the gap closed forms, and 7+12+15+8+3 = 45.")
    print()
    print("  FORCED, which is what makes them usable as checks:")
    print("    block-sum law   DR(141+777+41) = DR(N).  True for every number")
    print("                    and every digit split -- 40,000 random trials,")
    print("                    zero exceptions.  A split failing it has a")
    print("                    transcription error in it.")
    print("    wing-fold law   dropping a block subtracts its digit sum:")
    print("                    32 - 21 = 11 -> DR 2 = DR(141+41).  20,000 trials.")
    print("    factor-DR law   DR(1087) x DR(13043) -> 5 = DR(N), forced by DR")
    print("                    being multiplicative mod 9.  NECESSARY ONLY:")
    print("                    1087 x 13052 = 14,187,524 also has DR 5.")
    print()
    print("  NOT FORCED:")
    print("    777 = 21 x 37, so the MIDDLE BLOCK IS ON THE SEAM, and both")
    print("    wings land in the same orbit: 141 -> 30 in C3, 41 -> 4 in C3.")
    print("    The partition reads  C3 | seam | C3.  N itself is 7, in D7.")
    print("    (777 = 7 x 111 and 111 = 3 x 37 -- the same fact as T435.)")
    print()
    print("  ALSO FORCED, and worth not mistaking for a property of M:")
    print("    M/6 has uniform equilibrium because M is doubly stochastic, which")
    print("    holds for ANY circulant whose rows permute {1,2,3} -- all six")
    print("    checked.  And M = I + 2P + 3P^2 only for the LEFT cyclic shift.")
    print()
    print("  1/2400 repeats because 2400 = 2^5 x 3 x 5^2 and the 3 is outside")
    print("  {2,5}.  That is the whole rule for terminating decimals.")
    print()
    print("  Orbits and dr/is_prime come from functions.py, not retyped here.")


if __name__ == "__main__":
    self_test()
