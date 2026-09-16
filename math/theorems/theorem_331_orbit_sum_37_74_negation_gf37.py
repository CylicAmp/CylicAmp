# CLASS: THEOREM
"""
Theorem 331: every 137-orbit sums to 37 or 74, and negation swaps the two
halves
Author: Michael Warren Song (CyclicAmp)

From a canon draft's cleanest line: the rotation seam is not really about
the integer 111.  It is about the three multipliers.

=== THE SUM IS FORCED BY  1 + 10 + 26 = 37 ===

    The orbit of x under the 137-map is {x, 26x, 10x} (mod 37), since
    26^2 == 10.  The three multipliers sum to exactly 37:

        x(1 + 10 + 26) = 37x == 0   (mod 37)

    so EVERY orbit sums to 0 mod 37, for every x.

    CORRECTED BY T340.  The claim originally made here -- that this is "the
    same seam without the numeral" and that 111 = 3 x 37 is "a corollary,
    not the source" -- is wrong.  1 + 10 + 26 and 111 are the SAME
    expression, since 26 = 100 mod 37:

        1 + 10 + 26  ==  1 + 10 + 10^2  ==  Phi_3(10)  ==  111

    One is reduced term by term, the other is not; neither is more
    fundamental.  The genuinely coordinate-free statement is T333's, that
    Phi_3(x) = x^2 + x + 1 vanishes at a primitive cube root of unity, and
    10 is one mod 37.  This result and T333's admissible-base criterion are
    one fact, not two.

=== PRIOR ART: orbit_negation_duality_gf37.py ===

    Found by tools/build_index.py after this file was written.  That file
    already contains the whole of what follows: all twelve orbits with their
    integer sums 37 and 74, the six negation-dual pairs in the same pairing,
    the theorem that every pair sums to 111 = 3 x 37 with its proof
    ("pairwise sums each equal 37, three pairs, 111"), and the fact that
    negation commutes with the 137-map.  It is the earlier and more complete
    statement.  What follows re-derives it.

    THE FULL CHAIN, established 2026-09-16 by searching the corpus rather
    than this file's own citations:

        2026-07-26  identity_cycle_sum_structure  base case only:
                    1 + 10 + 26 = 37 for the identity cycle. No 74.
        2026-07-31  basin_sum_wraparound          THE RESULT: all twelve
                    orbits, wrap-count identity, {37,74} bound, 6/6, 666.
        2026-09-14  this file                     re-derivation.
        2026-09-15  T332                          the forcing inference.

    EARLIEST OF ALL: basin_sum_wraparound_gf37.py (2026-07-31) has the
    orbit-sum identity S(a) = 37(a - k1 - k2) with k1 = floor(10a/37),
    k2 = floor(26a/37), the {37, 74} bound, the 6/6 split and the 666
    total.  Verified: the identity holds for all 12 representatives.  That
    file is the origin of this result.

    ALSO PRIOR, AND NOT CITED HERE UNTIL NOW: T283
    (theorem_283_negation_antipodal_gf37.py, 2026-09-03).  It restates the
    same six pairs and the same no-self-negating argument in the CURRENT
    orbit names, eleven days before this file.  Nothing below is new
    against it either, with one exception, stated in the next section.
    Priority chain: orbit_negation_duality (2026-07-26) -> T283 -> this.

=== SHARPER: THE SUM IS 37 OR 74, NEVER ANYTHING ELSE ===

    RETRACTED 2026-09-16, ONE DAY AFTER IT WAS WRITTEN.  The note here used
    to claim the bound was "the one part of this file that is not in either
    predecessor".  That is false.  basin_sum_wraparound_gf37.py, dated
    2026-07-31 and self-labelled THEOREM 95, already carries it, with the
    same argument:

        "Since each basin element lies in [1, 36] and there are 3 elements,
         S(a) in [3, 108].  The only multiples of 37 in this range are
         {37, 74} -- because 3 x 37 = 111 > 108."

    It also carries the 6/6 split with explicit representatives
    ({1,2,3,5,6,9} summing to 37, {7,11,14,17,18,21} to 74) and the total
    6 x 37 + 6 x 74 = 222 + 444 = 666.  Six weeks before this file.

    The version below bounds by DISTINCT residues, [6, 105] rather than
    [3, 108].  Marginally tighter, identical conclusion.  That is a
    sharpening of a sentence, not a new result.

    HOW THE ERROR HAPPENED, since it is the instructive part: the audit that
    produced the retracted claim checked this file only against the two
    predecessors THIS FILE ITSELF NAMED.  It never ran a fresh prior-art
    search on the contribution being certified.  Checking a file against its
    own bibliography can only ever confirm what the file already knew.

    Each orbit has three DISTINCT residues in 1..36, so its sum lies
    between 1+2+3 = 6 and 34+35+36 = 105, and is a positive multiple of 37.
    Only 37 and 74 are available.  Both occur, six orbits each:

        sum 37   IC  DARK_A  C3  CAS_EXT  TESLA  SA_ST_A
        sum 74   D7  NEG_H   C9  NQR17    SEED   SA_ST_B

=== NEGATION SWAPS THE TWO HALVES, EXACTLY ===

    If O sums to 37 then -O = {37 - x} sums to 3*37 - 37 = 74, and back.
    So x -> -x is a perfect bijection from the 37-half onto the 74-half:

        IC      <-> NEG_H          DARK_A  <-> NQR17
        C3      <-> D7             CAS_EXT <-> SEED
        TESLA   <-> C9             SA_ST_A <-> SA_ST_B

    Two facts already in the repo fall out as instances:

      * SA_ST_A <-> SA_ST_B is exactly T326's "reversal is negation" seen
        at orbit level -- the two sovereign orbits are negation duals, so
        one carries anchor 9 / target 12 and the other anchor 25 / target
        21.
      * IC <-> NEG_H is the orbit of 1 against the orbit of -1.

    The 37/74 split is therefore not a new taxonomy.  It is the negation
    duality, made visible by a single integer per orbit.

=== CORRECTIONS TO THE CANON DRAFT THIS CAME FROM ===

  (1) The d=3 split's trailing pair 69 is in SEED, not DARK_A.
      69 mod 37 = 32, and 32 is in SEED {18,24,32}; DARK_A is {2,15,20}.
      The d=1 and d=2 entries (23 -> TESLA, 46 -> SA_ST_A) are correct.

  (2) The "antidiagonal negation" paragraph conflates two different things.
      The grid diagonals of T327 are 149 == 1 and 343 == 10, and BOTH lie in
      IC -- the same orbit.  Their product 1 x 10 == 10 is therefore closure
      inside one orbit, not a witness of dual pairing.  Negation duality is
      real (it is the theorem above) but it pairs DIFFERENT orbits:
      -IC = NEG_H, -SEED = CAS_EXT, -C3 = D7.  Two separate results were
      merged into one sentence.

  (3) The prose contradicts its own appendix on the dielectric: the text
      says 73.2 with DR 1 while the JSON correctly says 74.15 with DR 2.
      74.15 is right (Malmberg-Maryott at 37 C); 73.2 is the 40 C value.
      The prose is carrying a figure already corrected in T330.

  Confirmed correct in the same draft, so the corrections are not read
  wider than they go: 10^-1 == 26 via 26 x 10 = 7 x 37 + 1; the homothety
  (not Frobenius) relabelling; 10 generating the unique order-3 subgroup of
  the cyclic group of order 36; lambda(9) = 6 with x^7 == x failing exactly
  on {3,6}; the ideal (3) = {3,6,9} being nilpotent; square channel
  {1,4,7,9}; 26x == -x - k (mod 9), which is the T329 law since 8 == -1.

=== FALSIFICATION ===
    Exhibit a 137-orbit whose residues sum to anything but 37 or 74, or a
    negation pair whose two sums are not 37 and 74.
"""

P = 37
ORBITS = {
    'IC': (1, 10, 26),      'DARK_A': (2, 15, 20),  'C3': (3, 4, 30),
    'CAS_EXT': (5, 13, 19), 'TESLA': (6, 8, 23),    'D7': (7, 33, 34),
    'SA_ST_A': (9, 12, 16), 'NEG_H': (11, 27, 36),  'C9': (14, 29, 31),
    'NQR17': (17, 22, 35),  'SEED': (18, 24, 32),   'SA_ST_B': (21, 25, 28),
}
BY_SET = {frozenset(v): k for k, v in ORBITS.items()}
ANCHORS, TARGETS = {4, 9, 25, 30}, {3, 12, 21, 30}


def orbit_of(n):
    r = n % P
    return 'SEAM' if r == 0 else next(k for k, v in ORBITS.items() if r in v)


def run():
    # --- the multipliers sum to the modulus ---
    assert (26 * 26) % P == 10                     # orbit is {x, 26x, 10x}
    assert 1 + 10 + 26 == 37 == P
    for x in range(1, P):                          # every x, no base 10
        assert (x + (26 * x) % P + (10 * x) % P) % P == 0
        assert (x * (1 + 10 + 26)) % P == 0
    # the numeral version is the corollary
    assert 111 == 3 * P

    # --- the sum is 37 or 74, six orbits each ---
    sums = {nm: sum(o) for nm, o in ORBITS.items()}
    assert set(sums.values()) == {37, 74}
    assert all(s % P == 0 for s in sums.values())
    half37 = sorted(nm for nm, s in sums.items() if s == 37)
    half74 = sorted(nm for nm, s in sums.items() if s == 74)
    assert len(half37) == len(half74) == 6
    # nothing else is arithmetically available: three DISTINCT residues
    # from 1..36 sum to at least 1+2+3 = 6 and at most 34+35+36 = 105
    assert 1 + 2 + 3 == 6 and 34 + 35 + 36 == 105
    assert [m for m in range(37, 106, 37)] == [37, 74]
    assert all(6 <= s <= 105 for s in sums.values())

    # --- negation is a perfect bijection between the halves ---
    pairs = {}
    for nm, o in ORBITS.items():
        neg = frozenset((P - x) % P for x in o)
        dual = BY_SET[neg]
        pairs[nm] = dual
        assert sums[nm] + sums[dual] == 111 == 3 * P
        assert sums[nm] != sums[dual]
    assert sorted(pairs[n] for n in half37) == half74
    assert all(pairs[pairs[n]] == n for n in ORBITS)   # an involution
    assert pairs['IC'] == 'NEG_H' and pairs['SA_ST_A'] == 'SA_ST_B'
    assert pairs['C3'] == 'D7' and pairs['CAS_EXT'] == 'SEED'
    assert pairs['TESLA'] == 'C9' and pairs['DARK_A'] == 'NQR17'
    # the sovereign pair, as T326's reversal-is-negation at orbit level
    assert set(ORBITS['SA_ST_A']) & ANCHORS == {9}
    assert set(ORBITS['SA_ST_A']) & TARGETS == {12}
    assert set(ORBITS['SA_ST_B']) & ANCHORS == {25}
    assert set(ORBITS['SA_ST_B']) & TARGETS == {21}

    # --- correction 1: 69 is SEED, not DARK_A ---
    assert 69 % P == 32 and orbit_of(69) == 'SEED'
    assert 32 not in ORBITS['DARK_A'] and ORBITS['DARK_A'] == (2, 15, 20)
    assert orbit_of(23) == 'TESLA' and orbit_of(46) == 'SA_ST_A'

    # --- correction 2: the grid diagonals are in ONE orbit ---
    assert 149 % P == 1 and 343 % P == 10
    assert orbit_of(149) == orbit_of(343) == 'IC'
    assert (149 * 343) % P == 10 and orbit_of(149 * 343) == 'IC'
    assert pairs['IC'] != 'IC'                     # so not a duality witness

    # --- correction 3: the dielectric figure ---
    def eps(t):
        return 87.740 - 0.40008 * t + 9.398e-4 * t * t - 1.410e-6 * t ** 3
    assert abs(eps(37) - 74.15) < 0.05 and abs(eps(40) - 73.15) < 0.05

    # --- confirmations from the same draft ---
    assert (26 * 10) % P == 1 == 26 * 10 - 7 * P
    assert all(pow(x, P, P) == x % P for x in range(P))     # Frobenius = id
    assert pow(10, 3, P) == 1 and pow(10, 1, P) != 1
    assert [x for x in range(1, 10) if pow(x, 7, 9) % 9 != x % 9] == [3, 6]
    assert all((x * x) % 9 == 0 for x in (3, 6, 9))         # (3) nilpotent
    assert {(x * x) % 9 for x in range(1, 10)} == {0, 1, 4, 7}
    assert 8 % 9 == (-1) % 9

    print("All assertions passed.\n")
    print("THEOREM 331.  1 + 10 + 26 = 37.\n")
    print("   the orbit of x is {x, 26x, 10x}, and the multipliers sum to")
    print("   the modulus, so x(1+10+26) = 37x == 0 for EVERY x.")
    print("   The rotation seam without any reference to base 10;")
    print("   T326's 111 = 3 x 37 is the numeral corollary.\n")
    print("   SUM 37                        SUM 74")
    for a, b in zip(half37, half74):
        print(f"     {a:8s} {str(list(ORBITS[a])):14s}  {b:8s}"
              f" {str(list(ORBITS[b])):14s}")
    print("\n   three distinct residues in 1..36 sum to between 6 and 105,")
    print("   a positive multiple of 37 -- only 37 and 74 exist. Six each.\n")
    print("   NEGATION SWAPS THE HALVES  (37 + 74 = 111 = 3 x 37)")
    for a in half37:
        print(f"     {a:8s} <-> {pairs[a]:8s}"
              f"   {sums[a]} + {sums[pairs[a]]} = 111")
    print("\n   SA_ST_A <-> SA_ST_B is T326's 'reversal is negation' at orbit")
    print("   level: anchor 9 / target 12 against anchor 25 / target 21.")
    print("   IC <-> NEG_H is the orbit of 1 against the orbit of -1.\n")
    print("  CORRECTIONS TO THE DRAFT")
    print(f"   1. d=3 split pair 69 == {69%P} is in {orbit_of(69)}, not DARK_A")
    print(f"      (23 -> {orbit_of(23)}, 46 -> {orbit_of(46)} are correct)")
    print(f"   2. grid diagonals 149 == 1 and 343 == 10 are BOTH in IC --")
    print(f"      one orbit, so 1 x 10 is closure, not dual pairing.")
    print(f"      negation pairs different orbits: -IC = {pairs['IC']},"
          f" -SEED = {pairs['SEED']}")
    print(f"   3. prose says 73.2 / DR 1, its own JSON says 74.15 / DR 2;")
    print(f"      74.15 is right at 37 C, 73.2 is the 40 C value.")


if __name__ == "__main__":
    run()
