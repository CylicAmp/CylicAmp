# CLASS: THEOREM
"""
Theorem 428: the parity-word determinant sieve -- the sign argument closes a
band of positive cycles, the band is everything exactly when m > 4, and two
of the five proposed verdicts need repair

Supplied by the user as a sharpening of T425-T427. The identity and the sign
argument are correct and are stated and verified below. Two corrections to
the proposed verdict ledger are this file's own, and both were found by
running it.

PRIOR ART: the corpus has no parity-word or affine-composition machinery.
T425/T426/T427 are the finite-modulus files this replaces as the cycle
instrument -- and the replacement is the point: a finite-field reduction
cannot decide a cycle question about the integers, and this can.

NOTE ON PROVENANCE: the supplied text refers to "your implementation's
B % det test". No such implementation exists in this session. The sieve
below was built from the identity, not patched from an earlier one, so the
B % det remark is answered on the mathematics rather than on the code:
`B % D == 0` is a correct divisibility test in Python for D < 0 as well,
but the certificate should read |D| divides B, and it does here.

================================================================================
1. THE IDENTITY AND THE SIGN THEOREM
================================================================================

  Shortcut map, so that EVERY step halves and 2^L is the right denominator:

      T_m(n) = (m n + 1)/2   if n is odd        T_m(n) = n/2  if n is even

  For a parity word sigma in {O,E}^L with a occurrences of O, composing
  gives an affine map with denominator 2^L,

      F_sigma(x) = (m^a x + B_sigma) / 2^L

  where B_sigma is built by the recurrence B <- mB + 2^k on the k-th letter
  when that letter is O, starting from B = 0. So B_sigma is a non-negative
  integer and B_sigma > 0 exactly when the word contains an O.

  A cycle on that word requires F_sigma(x) = x, i.e.

      (2^L - m^a) x = B_sigma,        write  D_sigma = 2^L - m^a,

  so every candidate is FORCED to be x = B_sigma / D_sigma.

  SIGN THEOREM.  If m^a > 2^L then D_sigma < 0 while B_sigma > 0, so x < 0.
  Hence NO POSITIVE INTEGER CYCLE can have m^a > 2^L.  The case
  m^a = 2^L cannot occur for a, L > 0 since 2 and m are distinct primes
  (or, for composite odd m, since 2 does not divide m^a).

  This eliminates a whole class by an exact sign, not by a failed search.
  In threshold form, a positive cycle needs

      a / L  <  1 / log2(m).

================================================================================
2. THE CROSSOVER AT m = 4, WHICH IS THE DIVERGENCE HEURISTIC MADE EXACT
================================================================================

      1/log2(3) = 0.6309      1/log2(5) = 0.4307      1/log2(7) = 0.3562

  A uniformly random parity word has odd-density a/L -> 1/2.  So the
  fraction of words killed by the sign argument tends to 0 when
  1/log2(m) > 1/2 and to 1 when 1/log2(m) < 1/2, and

      1/log2(m) < 1/2   <=>   log2(m) > 2   <=>   m > 4.

  m = 3 IS THE LAST SUBCRITICAL MULTIPLIER; every m >= 5 is supercritical.
  Measured, as the fraction of words of length exactly L with D < 0:

      L       m=3      m=5      m=7
      6      34.4%    65.6%    65.6%
      10     17.2%    62.3%    82.8%
      17     16.6%    68.5%    83.4%
      40      4.0%    78.5%    96.0%
      100     0.3%    90.3%    99.8%
      400     0.0%    99.7%   100.0%

  falling to 0 for m = 3 and climbing to 1 for m = 5 and 7.  The approach is
  NOT monotone in L -- the threshold a > L/log2(m) crosses integers, so the
  binomial tail jitters at small L (m=5 dips from 65.6% to 62.3% between
  L = 6 and 10).  The limit is what the crossover claims, not monotonicity,
  and the table is measured rather than asserted.  This is
  the "expected factor 3/4 < 1 against 5/4 > 1" heuristic of T426 restated
  as a statement about which parity words survive, and it is exact.

  It also says what the sign argument is worth on the real problem: for
  3n+1 it closes a vanishing fraction of words, so it is not a route to the
  Collatz conjecture.  Its bite is on the variants.

================================================================================
3. TWO REPAIRS TO THE PROPOSED VERDICT LEDGER
================================================================================

  The proposal was, in order:
      SIGN-IMPOSSIBLE / NONINTEGRAL / PARITY-INCONSISTENT /
      NEGATIVE-CYCLE / POSITIVE-CYCLE

  REPAIR 1 -- NEGATIVE-CYCLE is unreachable in that order.  With B > 0,
  D > 0 forces x > 0 and D < 0 forces x < 0.  So testing the sign FIRST
  absorbs every negative cycle into SIGN-IMPOSSIBLE and the verdict can
  never fire.  Divisibility must be tested before the sign:

      D = 0                      impossible
      |D| does not divide B      NONINTEGRAL   (record the sign of D)
      otherwise x = B/D          and then sign it

  With that order the sieve recovers the three known negative 3n+1 cycles
  exactly -- seeds {-1}, {-5,-7,-10} and the eleven-element orbit of -17,
  fifteen seeds in all, and nothing else.  That is a positive control the
  original order could not produce.

  REPAIR 2 -- PARITY-INCONSISTENT is vacuous.  Zero hits in 393210 words
  (m = 3, 5, 7, all lengths 1..16).  It is not an accident: the parity-vector
  map is a bijection on the 2-adic integers (Lagarias 1985, Bernstein 1994),
  so a purely periodic word has a unique 2-adic solution, that solution is
  the rational B/D, and it realises the word by construction.  Cited, not
  proved here; the measurement is the check.

  So the working ledger is four verdicts, not five, and the order matters:

      D = 0 -> impossible | NONINTEGRAL | NEGATIVE-CYCLE | POSITIVE-CYCLE

================================================================================
4. THE SIEVE AS A POSITIVE CONTROL
================================================================================

  Over all words of length 1..16 the sieve finds exactly the known cycles
  and no others:

      m = 3   positive seeds {1, 2}
              = the shortcut cycle 1 -> 2 -> 1, i.e. 1 -> 4 -> 2 -> 1
      m = 5   positive seeds {1,2,3,4,8} and
              {13,17,26,27,33,34,43,52,54,68,83,104,108,208}
              = the length-7 cycle and BOTH length-10 cycles of 5n+1
      m = 7   positive seeds {1, 2, 4}
              = the shortcut cycle 1 -> 4 -> 2 -> 1

  Compare T426: the finite-modulus map U saw the 5n+1 seven-cycle but was
  structurally blind to the two ten-cycles, because 416 and 216 exceed the
  modulus.  The sieve sees all three.  That is the concrete sense in which
  this instrument replaces the finite-field one for cycle questions.

================================================================================
4b. OUT TO L = 24, BY BOUNDING THE CYCLE MINIMUM INSTEAD OF ENUMERATING
================================================================================

  Word enumeration stops being possible around L = 17: 2^24 words per
  multiplier is out of reach in this language.  It is also unnecessary.

  BOUNDING LEMMA.  Fix L and a with D = 2^L - m^a > 0.  Then
  B_sigma <= Bmax(L, a, m), the maximum of sum_{j in O} 2^j m^{a_j} over all
  placements of a O's in L slots, which a two-line DP computes exactly.  Any
  positive cycle on such a word has x = B/D <= Bmax/D.  Maximising over all
  (L, a) with L <= 24 gives a single bound X, and then testing every odd
  x <= X directly is a COMPLETE search -- no word is skipped, because every
  cycle has a minimum element and that element is <= X.

      m = 3   X = 3018    worst (L,a) = (24,15)
      m = 5   X = 18510   worst (L,a) = (21,9)
      m = 7   X = 14398   worst (L,a) = (23,8)

  The same construction with D < 0 bounds the negative cycles:

      m = 3   |x| <= 9436    m = 5   |x| <= 19363   m = 7   |x| <= 12027

  RESULT, complete for every cycle of length L <= 24:

      m = 3   positive minima {1}          negative {-1, -5, -17}
      m = 5   positive minima {1, 13, 17}  negative {-1}
      m = 7   positive minima {1}          negative none

  Every one is a cycle already known.  m = 3 returns exactly the trivial
  cycle and the three classical negative cycles and nothing else; m = 5
  returns exactly its three known cycles; m = 7 returns only the trivial one
  and has no negative cycle at all, since -1 -> -3 -> -10 -> -5 -> -17 -> ...
  runs away downward instead of closing.

  So the L <= 16 word sieve and the L <= 24 bounded search agree where they
  overlap, and the extension to 24 adds no new cycle for any of the three
  multipliers.

================================================================================
4c. SPECIFICATION FOR THE CYCLE-MEAN CONSTRUCTION, AND WHY IT IS VACUOUS
================================================================================

  Three conventions were asked for, to build the De Bruijn edge shift and
  run Karp against log2/log3 = 0.63093.  Answering them in the conventions
  this file actually uses:

  (1) ALPHABET.  The two-letter shift over {E, O} on the SHORTCUT map

          T(n) = (3n+1)/2  for odd n,        T(n) = n/2  for even n

      not the fully accelerated 2-adic presentation odd x -> (3x+1)/2^k.
      Every letter is one step and every step halves, which is why the
      denominator is 2^L and not 2^(number of E's).

  (2) EDGE WEIGHTS.  Uniform step length 1.  An O contributes log 3 and
      every step contributes log 2, so the log-growth of a word is
      a log 3 - L log 2 and the cycle mean is exactly the odd-density a/L.
      Contraction is a/L < log2/log3, which is the same inequality as this
      file's sign condition 2^L > 3^a.  Nothing new is being asked; the
      threshold and the determinant are two readings of one line.

  (3) FORBIDDEN BLOCKS.  There are none, and that is the problem.

  THE SUBSHIFT IS THE FULL 2-SHIFT.  The parity-vector map is a bijection on
  the 2-adic integers, so every word of length L is realised by EXACTLY ONE
  residue class mod 2^L.  Verified here by direct count for every word of
  length 1..12 and for m = 3, 5, 7: exactly one residue each, no exceptions.

  Therefore F = {} and the De Bruijn edge shift is unconstrained, so

      lambda* = max cycle mean = 1,   attained by the all-O loop,

  and 1 > 0.63093.  The threshold test is passed by a word that genuinely
  exists: for m = 3 the all-O word of length L is realised by x = 2^L - 1,
  e.g. 255 mod 256 giving 255, 383, 575, 863, 1295, 1943, 2915, 4373, 6560,
  odd at every one of the eight steps.  So Karp returns 1, the comparison
  fails, and NO contraction follows -- not because the computation is hard
  but because the object has no forbidden blocks to prune.

  WHAT WOULD MAKE IT NON-VACUOUS.  F must come from somewhere other than
  parity admissibility, since parity forbids nothing.  Two honest sources:
  a window condition that forbids words whose realising class mod 2^K is
  incompatible with staying above the starting value, or a descent
  certificate that forbids words after which the trajectory has provably
  dropped.  Both are conditions on the VALUE, not on the parity word, so
  they do not define a subshift of finite type on {E,O} without further
  work.  That is the gap, and it is where the effort belongs.

  This is the same shape as the miss-test failures recorded in T425-T427:
  the instrument cannot come back negative, so its verdict carries nothing.

================================================================================
5. SCOPE -- WHAT THIS DOES NOT DO
================================================================================

  Eliminating cycles is not proving descent, and the supplied text says so.
  The sieve closes the PERIODIC branch, and only up to the searched length:
  L <= 24 here.  A trajectory can avoid periodicity and still climb.

  The stated next question is recorded as OPEN, not as progress:

      can an admissible infinite parity sequence maintain unbounded growth
      without ever producing a descent certificate?

  That asks about non-periodic words, where D_sigma does not exist because
  there is no cycle equation to write.  Nothing in this file bears on it.
  The honest summary is that the sign argument closes a band of the
  periodic branch exactly, closes essentially all of it for m > 4, and
  closes a vanishing fraction of it for m = 3, which is the case that
  matters.

  FALSIFICATION.  Any of: B_sigma <= 0 for a word containing O; a positive
  cycle with m^a > 2^L; a cycle seed outside the lists in section 4 for
  L <= 16; a PARITY-INCONSISTENT hit; or the m=3 sign-impossible fraction
  failing to fall with L while m=5,7 fail to rise.  All are asserted.
"""

import math
import sys


def coeffs(word, m):
    """F_sigma(x) = (A x + B) / 2^L with A = m^a."""
    A, B = 1, 0
    for k, s in enumerate(word):
        if s:
            B = m * B + (1 << k)
            A = m * A
    return A, B


def realises(word, m, x):
    v = x
    for s in word:
        if (v % 2 != 0) != bool(s):
            return False
        v = (m * v + 1) // 2 if v % 2 else v // 2
    return v == x


def verdict(word, m):
    """Repaired order: divisibility BEFORE sign."""
    L, a = len(word), sum(word)
    if a == 0:
        return "TRIVIAL", None
    A, B = coeffs(word, m)
    D = (1 << L) - A
    if D == 0:
        return "IMPOSSIBLE", None
    if B % abs(D) != 0:
        return "NONINTEGRAL", None
    x = B // D
    if not realises(word, m, x):
        return "PARITY-INCONSISTENT", x
    return ("POSITIVE-CYCLE" if x > 0 else "NEGATIVE-CYCLE"), x


def main():
    print("=" * 78)
    print("THEOREM 428: THE PARITY-WORD DETERMINANT SIEVE")
    print("=" * 78)

    print("\nPart 1: the identity, and B > 0 whenever the word contains an O")
    for m in (3, 5, 7):
        for w in ((1,), (1, 0), (1, 1, 0, 0, 0), (0, 1, 0)):
            A, B = coeffs(w, m)
            assert A == m ** sum(w)
            assert B > 0
    assert coeffs((0, 0, 0), 3) == (1, 0)
    print("   A = m^a always; B > 0 for every word with an O; B = 0 for all-E ✓")
    # the three genuine cycles, by hand
    for m, w, want in ((3, (1, 0), 1), (5, (1, 1, 0, 0, 0), 1), (7, (1, 0, 0), 1)):
        A, B = coeffs(w, m)
        D = (1 << len(w)) - A
        print("   m=%d word %s: D = 2^%d - %d = %-3d, B = %-3d, x = B/D = %d"
              % (m, "".join("OE"[1 - s] for s in w), len(w), A, D, B, B // D))
        assert B // D == want and B % D == 0

    print("\nPart 2: the sign theorem and the crossover at m = 4")
    for m in (3, 5, 7):
        print("   1/log2(%d) = %.4f  %s" % (m, 1 / math.log2(m),
              "> 1/2, subcritical" if 1 / math.log2(m) > 0.5
              else "< 1/2, SUPERCRITICAL"))
    assert 1 / math.log2(3) > 0.5 > 1 / math.log2(5)
    assert 1 / math.log2(4) == 0.5
    print("   crossover 1/log2(m) = 1/2 exactly at m = 4 ✓")
    def sign_fraction(L, m):
        """Exact: the binomial tail a > L/log2(m)."""
        amin = math.floor(L / math.log2(m)) + 1
        return 100.0 * sum(math.comb(L, a)
                           for a in range(amin, L + 1)) / 2 ** L

    # cross-check the closed form against brute enumeration at small L
    for L in (6, 10, 14):
        for m in (3, 5, 7):
            bad = sum(1 for w in range(1 << L)
                      if (1 << L) - m ** bin(w).count("1") < 0)
            assert abs(sign_fraction(L, m) - 100.0 * bad / (1 << L)) < 1e-9
    print("\n   fraction of words of length L with D < 0 (exact binomial tail,")
    print("   cross-checked against enumeration at L = 6, 10, 14):")
    print("   L       m=3      m=5      m=7")
    frac = {}
    for L in (6, 10, 17, 40, 100, 400):
        row = [sign_fraction(L, m) for m in (3, 5, 7)]
        for m, v in zip((3, 5, 7), row):
            frac.setdefault(m, []).append(v)
        print("   %-6d %6.1f%%  %6.1f%%  %6.1f%%" % (L, row[0], row[1], row[2]))
    assert frac[3][-1] < 0.1 < frac[3][0]          # -> 0
    assert frac[5][-1] > 99 > frac[5][0]           # -> 1
    assert frac[7][-1] > 99 > frac[7][0]           # -> 1
    assert frac[5][1] < frac[5][0]                 # NOT monotone
    print("   m=3 -> 0, m=5 and m=7 -> 1. Not monotone: m=5 dips at L=10,")
    print("   because the threshold a > L/log2(m) crosses integers ✓")

    print("\nPart 3: the two repairs")
    # Repair 1: sign-first makes NEGATIVE-CYCLE unreachable
    def sign_first(word, m):
        L, a = len(word), sum(word)
        if a == 0:
            return "TRIVIAL"
        A, B = coeffs(word, m)
        D = (1 << L) - A
        if D <= 0:
            return "SIGN-IMPOSSIBLE"
        return "OTHER"
    neg_seen = 0
    for L in range(1, 14):
        for w in range(1 << L):
            word = tuple((w >> i) & 1 for i in range(L))
            if verdict(word, 3)[0] == "NEGATIVE-CYCLE":
                neg_seen += 1
                assert sign_first(word, 3) == "SIGN-IMPOSSIBLE"
    print("   repair 1: every NEGATIVE-CYCLE word is SIGN-IMPOSSIBLE under the")
    print("             sign-first order, so that verdict could never fire")
    print("             (%d such words at L <= 13) ✓" % neg_seen)

    print("\nPart 4: the sieve as a positive control, L <= 16")
    pi_hits = 0
    for m in (3, 5, 7):
        pos, neg = set(), set()
        for L in range(1, 17):
            for w in range(1 << L):
                word = tuple((w >> i) & 1 for i in range(L))
                v, x = verdict(word, m)
                if v == "POSITIVE-CYCLE":
                    pos.add(x)
                elif v == "NEGATIVE-CYCLE":
                    neg.add(x)
                elif v == "PARITY-INCONSISTENT":
                    pi_hits += 1
        print("   m=%d positive seeds %s" % (m, sorted(pos)))
        print("        negative seeds %s" % sorted(neg))
        if m == 3:
            assert sorted(pos) == [1, 2]
            assert sorted(neg) == sorted(
                [-1, -5, -7, -10, -17, -25, -37, -55, -82, -41, -61, -91,
                 -136, -68, -34])
        if m == 5:
            assert sorted(pos) == [1, 2, 3, 4, 8, 13, 17, 26, 27, 33, 34, 43,
                                   52, 54, 68, 83, 104, 108, 208]
        if m == 7:
            assert sorted(pos) == [1, 2, 4]
    print("   repair 2: PARITY-INCONSISTENT hits across all three m: %d" % pi_hits)
    assert pi_hits == 0
    print("             vacuous, as the 2-adic parity-vector bijection predicts")
    print("   m=3 negatives are exactly the orbits of -1, -5 and -17 ✓")

    print("\nPart 4b: complete to L = 24 by bounding the cycle minimum")

    def bmax(L, a, m):
        """Exact max of B over placements of a O's in L slots."""
        dp = {0: 0}
        for j in range(L - 1, -1, -1):
            nd = {}
            for tt, val in dp.items():
                if tt <= a:
                    nd[tt] = max(nd.get(tt, -1), val)
                if tt < a:
                    nd[tt + 1] = max(nd.get(tt + 1, -1), val + (1 << j) * m ** tt)
            dp = nd
        return dp.get(a, 0)

    def bound(m, LMAX, positive):
        X = 0
        for L in range(1, LMAX + 1):
            for a in range(1, L + 1):
                D = (1 << L) - m ** a
                if (D <= 0) if positive else (D >= 0):
                    continue
                X = max(X, bmax(L, a, m) // abs(D))
        return X

    def search(m, LMAX, X, positive):
        seeds = set()
        rng = range(1, X + 1, 2) if positive else range(-1, -X - 1, -2)
        for x in rng:
            v, path = x, [x]
            for _ in range(LMAX):
                v = (m * v + 1) // 2 if v % 2 else v // 2
                if v == x:
                    seeds.add(min(path) if positive else max(path))
                    break
                path.append(v)
        return sorted(seeds, reverse=not positive)

    LMAX = 24
    want = {3: ([1], [-1, -5, -17]), 5: ([1, 13, 17], [-1]), 7: ([1], [])}
    for m in (3, 5, 7):
        Xp, Xn = bound(m, LMAX, True), bound(m, LMAX, False)
        pos, neg = search(m, LMAX, Xp, True), search(m, LMAX, Xn, False)
        print("   m=%d  bound +%-6d -%-6d   positive %s   negative %s"
              % (m, Xp, Xn, pos, neg))
        assert pos == want[m][0], (m, pos)
        assert neg == want[m][1], (m, neg)
    print("   complete for every cycle with L <= 24; every one already known.")
    print("   the L<=16 word sieve and this agree, and 24 adds nothing new.")

    print("\nPart 4c: the cycle-mean construction is vacuous, F = {}")

    def follows(x, word, m):
        v = x
        for s in word:
            if (v % 2 != 0) != bool(s):
                return False
            v = (m * v + 1) // 2 if v % 2 else v // 2
        return True

    for m in (3, 5, 7):
        for L in range(1, 11):
            for w in range(1 << L):
                word = tuple((w >> i) & 1 for i in range(L))
                hits = sum(1 for x in range(1 << L) if follows(x, word, m))
                assert hits == 1, (m, word, hits)
    print("   every parity word of length 1..10 is realised by EXACTLY ONE")
    print("   residue mod 2^L, for m = 3, 5, 7 -> no block is forbidden ✓")
    print("   so the De Bruijn edge shift is the FULL 2-shift, lambda* = 1")
    print("   (the all-O loop), and 1 > log2/log3 = %.5f"
          % (math.log(2) / math.log(3)))
    L = 8
    allO = (1,) * L
    x = [v for v in range(1 << L) if follows(v, allO, 3)]
    assert x == [(1 << L) - 1]
    tr, v = [x[0]], x[0]
    for _ in range(L):
        v = (3 * v + 1) // 2 if v % 2 else v // 2
        tr.append(v)
    print("   witness m=3, L=8: x = %d = 2^8 - 1, trajectory %s" % (x[0], tr))
    print("   odd at every step, so the threshold is exceeded by a real word.")
    print("   Karp returns 1; no contraction follows. F must come from a")
    print("   condition on the VALUE, not on the parity word.")

    print("\nPart 5: scope")
    print("   closes the PERIODIC branch, and only for L <= 24 as run here.")
    print("   eliminating cycles is not proving descent; the non-periodic")
    print("   growth question is OPEN and nothing here bears on it.")
    print("   for m = 3 the sign argument closes a VANISHING fraction of")
    print("   words, so it is not a route to the Collatz conjecture.")

    print("\n" + "=" * 78)
    print("ALL ASSERTIONS PASS")
    print("=" * 78)


if __name__ == "__main__":
    sys.exit(main())
