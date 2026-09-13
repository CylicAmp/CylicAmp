# CLASS: THEOREM
"""
Theorem 315: the block 10..18 -- base at one end, seed orbit at the other,
and the 10 -> 27 chain from ord_37(10)=3 to its own cofactor
Author: Michael Warren Song (CyclicAmp)

=== PART I: THE 10+11 SPLIT IS THE ONLY ONE THAT SURVIVES REVERSAL ===

    21 splits ten ways as a+b with 1 <= a <= b. Exactly one satisfies
    rev(a) + rev(b) = rev(21):

        10 + 11 = 21    rev: 1 + 11 = 12 = rev(21)   YES
         9 + 12 = 21    rev: 9 + 21 = 30             no
        ... 8 others                                  no

    DERIVED, not counted. rev(a)+rev(b) = rev(a+b) needs both:
      (i)  a and b have equal digit length  -- positions must align
      (ii) the addition is carry-free       -- every column < 10
    10+11 has both (lengths 2,2; columns 1+1=2, 0+1=1). 9+12 fails (i)
    before (ii) is even reached. The rule matches brute force on all ten.

=== PART II: 10 IS THE RUNG T313 COULD NOT SEE ===

    forward   n + 9 = rev(n) : 12 23 34 45 56 67 78 89        (8)
    mirror    n - 9 = rev(n) : 10 21 32 43 54 65 76 87 98     (9)
    reverses of the forward  :    21 32 43 54 65 76 87 98
    mirror MINUS that        : 10

    The sets are not the same size, and the whole asymmetry is 10.
    Reason, exact: rev(10) = 1 drops a digit, and 10 - 9 = 1 = rev(10).
    Its forward partner would be 01 (01 + 9 = 10), which is not a
    two-digit number. T313 recorded "the missing rung is 01, excluded by
    the leading digit" as a notation artifact. It is not lost -- on the
    mirror side that rung is 10. Forward 8, mirror 9, difference one rung.

=== PART II-B: THE SAME GAP IN ROOT COORDINATES ===

    The mirror set is an AP of step 11, and 11 = 2 (mod 9) with 2 a unit
    mod 9. So its digital roots step by 2 and are FORCED to exhaust all
    nine residues:

        mirror  10 21 32 43 54 65 76 87 98  ->  roots 1 3 5 7 9 2 4 6 8
        forward 12 23 34 45 56 67 78 89     ->  roots   3 5 7 9 2 4 6 8

    The forward set cannot produce root 1; the mirror set can, and the
    number that supplies it is 10 (dr 10 = 1). So the 8-vs-9 MEMBERSHIP
    gap of Part II and this MISSING-ROOT gap are the same gap, seen in
    two coordinate systems. 10 fills both.

    No 0/9 ambiguity arises anywhere in either set: dr(n) = 0 only at
    n = 0, and every member is a positive two-digit integer.

    Scope: the step-3 law of Part IV (dr(n+3) = dr(n)+3) does NOT govern
    these sets. That law applies to {12,15,18} inside the block, which is
    step 3. The mirror is step 11. The two must not be welded.

=== PART II-C: THE 0/9 SPLIT DOES NOT REACH THE ORBITS ===

    gcd(37, 9) = 1, so by CRT the mod-37 and mod-9 coordinates are
    independent. dr is a mod-9 labelling; the 137-orbits are defined by
    x -> 26x (mod 37). A labelling convention on one cannot affect the
    other, and the orbits are exact integer 3-cycles with nothing to
    destabilise.

    The one true adjacent fact: of the seed orbit {18,24,32}, only 18
    lies in the ambiguous class (18 = 0 mod 9, dr 18 = 9); 24 -> 6 and
    32 -> 5. That is a fact about 18's label and changes nothing about
    the cycle. Recorded so the question is not asked again.

=== PART II-D: THE MIRROR SET IN MOD-37 COORDINATES ===

    M mod 37 = [10, 21, 32, 6, 17, 28, 2, 13, 24]

    Successive differences are a constant 11 mod 37 -- the step survives
    reduction. gcd(11,37) = 1, so all nine terms are distinct residues.
    The set is an AP of step 11 in Z/37 as well as in Z.

    Its endpoints echo Part IV's block:
        first  M[0] = 10, residue 10 in IC   {1,10,26}    the base
        last   M[8] = 98, residue 24 in SEED {18,24,32}   the seed orbit

    The block 10..18 opens on the base and closes on the seed orbit
    (18 itself). The mirror set does the same in mod-37 coordinates,
    opening on residue 10 and closing on residue 24. Two members land in
    SEED: 32 (residue 32) and 98 (residue 24).

    SCOPE: this is an observation, not a mechanism. Both sets begin at 10
    for the same reason -- it is the least two-digit solution of each --
    but the endpoints landing in SEED is arithmetic (98 = 10 + 8x11, and
    98 mod 37 = 24) with no derivation connecting the mirror set to the
    pipeline seed. Recorded at observation grade.

    Practical note, from an off-by-one that surfaced this: iterating the
    pair (M, F) with range(len(F)) drops M[8] = 98 -- which is exactly
    the member on the seed residue. The correct pairing is
    M[i+1] = rev(F[i]) for i = 0..7, leaving M[0] = 10 unpaired (Part II).
    Index-aligning M[i] with F[i] instead returns a constant -2 (= 35
    mod 37), which is only the offset between two step-11 APs -- a fact
    about listing order. The correctly aligned difference is a constant 9,
    which is the defining relation itself, not a finding.

    Checked and negative: the relation between M and F is additive only.
    M[i+1]/F[i] mod 37 and M[i]/F[i] mod 37 are both non-constant.

=== PART III: WHY 10 IS WHERE THE DIGIT WORK MEETS THE 137-MAP ===

    ord_37(10) = 3.  Hence 37 | 10^3 - 1 = 999, hence 111 = 3 x 37,
    hence aba + bab = 111(a+b) = 0 (mod 37). Every digit law in this
    repo -- the 999 antipodal blocks (T303), the 111 seam (T310), the
    333 = 37x9 sub-grid (T311), the 99(a-c) reversal law, the repdigit
    chain (T312) -- descends from that one order.

    And:  137 mod 37 = 26,  26 x 10 = 260 = 1 (mod 37).
    So 10 = 26^-1 mod 37. The base of the notation is the multiplicative
    inverse of the 137-map multiplier, and 10's 137-orbit is {1, 10, 26}:
    the identity, the base, and 137. One 3-cycle, IC.

    Scope: ord_37(26) = 3 as well, but that is FORCED -- inverses share
    an order -- so it is not a second observation. The content is the
    placement (base and 137 are inverse, in one orbit with 1), not the
    equality of orders.

=== PART IV: THE BLOCK 10..18 ===

    T314 showed 9 + dr(n) = n holds exactly on 10..18. That block carries
    four distinct roles at four distinct rungs:

        10   opens it         dr 1   IC        {1,10,26}   base, = 26^-1
        12   doubly closed    dr 3   SA_ST_A   {9,12,16}   T314's unique n
        15   triad middle     dr 6   DARK_A    {2,15,20}
        18   closes it        dr 9   SEED      {18,24,32}  pipeline seed orbit

    The triad rungs {12,15,18} are the multiples of 3 in the block, with
    roots 3,6,9.

    RECORDED AS ONE FACT, NOT TWO: this is T311's triad lock seen through
    a different window. T311 locks on the multiples of 3 among digits
    1..9; this locks on the multiples of 3 among 10..18. Both are
    "exactly 3 multiples of 3 in any 9 consecutive integers". Verified
    over 9-blocks k=1..499 with zero exceptions. It must not be counted
    as independent confirmation of the triad.

    What IS new: the map is step-preserving, not merely set-to-set.
    12,15,18 is an AP of step 3 and its image 3,6,9 is an AP of step 3,
    because dr(n+3) = dr(n)+3 whenever dr(n) <= 6 (no wrap inside the
    block). Zero exceptions n=1..499.

=== PART V: THE CHAIN 10 -> 21 -> 27 ===

    10 + 11 = 21,  21 + 6 = 27,  2 + 7 = 9.
    Roots: dr(10)=1, dr(21)=3, dr(27)=9 -- that is 3^0, 3^1, 3^2. Each
    step triples the root, and it halts at 9 because 9 = 0 (mod 9) is the
    fixed point of tripling. Two steps is the maximum ladder length.

    The chain begins at 10 and ends at 27 = (10^3 - 1)/37 = 999/37 = 3^3
    -- the cofactor 10^3-1 leaves behind once 37 is removed. Start and
    end are the two halves of 10^3 - 1 = 27 x 37.

    NOT FORCED: the addends 11 and 6 were chosen; no rule produces them,
    and 10+11+6 = 27 is arithmetic. What is forced is that 27, once
    reached, IS the cofactor. The chain is a route to a structural
    number, not a derivation of one.

    Also not a convergence: both lines end at 9, one as 3^2 and one as
    3+3+3. They agree because 3^2 = 3+3+3. Recorded so it does not read
    as two routes meeting.

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


BLOCK = list(range(10, 19))
TRIAD_RUNGS = [12, 15, 18]


def run():
    # --- I: the unique reversal-additive split of 21 ---
    splits = [(a, 21 - a) for a in range(1, 11)]
    good = [(a, b) for a, b in splits if rev(a) + rev(b) == rev(21)]
    assert good == [(10, 11)]
    assert len(good) == 1 and len(splits) == 10
    assert rev(10) + rev(11) == 12 == rev(21)
    assert rev(9) + rev(12) == 30 != rev(21)
    # the derived rule reproduces the brute force
    for a, b in splits:
        sa, sb = str(a), str(b)
        rule = (len(sa) == len(sb)
                and all(int(x) + int(y) < 10 for x, y in zip(sa, sb)))
        assert rule == (rev(a) + rev(b) == rev(a + b))

    # --- II: forward 8, mirror 9, and the extra rung is 10 ---
    fwd = [n for n in range(10, 100) if n + 9 == rev(n)]
    mir = [n for n in range(10, 100) if n - 9 == rev(n)]
    assert len(fwd) == 8 and len(mir) == 9
    assert sorted(set(mir) - {rev(n) for n in fwd}) == [10]
    assert rev(10) == 1 and 10 - 9 == rev(10)
    assert 1 + 9 == 10 and rev(10) != 10          # 01 is not two-digit

    # --- II-B: the same gap in root coordinates ---
    import math as _m
    assert [mir[i + 1] - mir[i] for i in range(len(mir) - 1)] == [11] * 8
    assert 11 % 9 == 2 and _m.gcd(2, 9) == 1
    assert [dr(n) for n in mir] == [1, 3, 5, 7, 9, 2, 4, 6, 8]
    assert sorted(dr(n) for n in mir) == list(range(1, 10))
    assert sorted(dr(n) for n in fwd) == list(range(2, 10))
    assert sorted(set(dr(n) for n in mir) - set(dr(n) for n in fwd)) == [1]
    assert dr(10) == 1
    assert not [n for n in mir + fwd if dr(n) == 0]
    # the mirror is step 11, NOT step 3 -- different sets, different laws
    assert [mir[i + 1] - mir[i] for i in range(len(mir) - 1)] != [3] * 8

    # --- II-D: the mirror set in mod-37 coordinates ---
    m37 = [n % P for n in mir]
    assert m37 == [10, 21, 32, 6, 17, 28, 2, 13, 24]
    assert [(m37[i + 1] - m37[i]) % P for i in range(8)] == [11] * 8
    assert _m.gcd(11, 37) == 1 and len(set(m37)) == 9
    assert m37[0] == 10 and sorted(_orbit_triple(10)) == [1, 10, 26]
    assert mir[8] == 98 and m37[8] == 24
    assert 246 % P == 24                       # the pipeline seed residue
    assert sorted(_orbit_triple(24)) == [18, 24, 32]
    assert [n for n in mir if n % P in (18, 24, 32)] == [32, 98]
    # the two alignments, and which constant each returns
    assert all(rev(fwd[i]) == mir[i + 1] for i in range(8))
    assert [mir[i + 1] - fwd[i] for i in range(8)] == [9] * 8    # definition
    assert [(mir[i] - fwd[i]) % P for i in range(8)] == [35] * 8  # AP offset
    assert [mir[i] - fwd[i] for i in range(8)] == [-2] * 8
    assert (-2) % P == 35 and 35 + 2 == P
    # checked and negative: no constant multiplicative relation
    assert len(set((mir[i + 1] * pow(fwd[i], P - 2, P)) % P
                   for i in range(8))) > 1
    assert len(set((mir[i] * pow(fwd[i], P - 2, P)) % P
                   for i in range(8))) > 1

    # --- II-C: mod 9 and mod 37 are independent ---
    assert _m.gcd(37, 9) == 1
    assert [26 * 18 % P, 26 * 24 % P, 26 * 32 % P] == [24, 32, 18]
    assert [v % 9 for v in (18, 24, 32)] == [0, 6, 5]
    assert [dr(v) for v in (18, 24, 32)] == [9, 6, 5]
    assert [v for v in (18, 24, 32) if v % 9 == 0] == [18]

    # --- III: ord_37(10) = 3, and 10 = 26^-1 ---
    assert pow(10, 3, P) == 1
    assert all(pow(10, k, P) != 1 for k in (1, 2))
    assert (10 ** 3 - 1) == 999 == 27 * 37
    assert 111 == 3 * 37
    assert all((101 * a + 10 * b + 101 * b + 10 * a) % P == 0
               for a in range(10) for b in range(10))
    assert 137 % P == 26
    assert 26 * 10 % P == 1                        # 10 = 26^-1
    assert sorted(_orbit_triple(10)) == [1, 10, 26]
    assert pow(26, 3, P) == 1                      # forced: inverses share order

    # --- IV: the block, its rungs, and the one-fact caveat ---
    assert [n for n in range(1, 10000) if 9 + dr(n) == n] == BLOCK
    assert [n for n in BLOCK if dr(n) in (3, 6, 9)] == TRIAD_RUNGS
    assert TRIAD_RUNGS == [n for n in BLOCK if n % 3 == 0]
    assert [dr(n) for n in TRIAD_RUNGS] == [3, 6, 9]
    # "3 multiples of 3 in any 9 consecutive integers" -- the shared fact
    for k in range(1, 500):
        assert len([n for n in range(k, k + 9) if dr(n) in (3, 6, 9)]) == 3
        assert len([n for n in range(k, k + 9) if n % 3 == 0]) == 3
    # the genuinely new part: the map preserves the step
    assert not [n for n in range(1, 500) if dr(n) <= 6 and dr(n + 3) != dr(n) + 3]
    assert [TRIAD_RUNGS[i + 1] - TRIAD_RUNGS[i] for i in (0, 1)] == [3, 3]
    assert [dr(TRIAD_RUNGS[i + 1]) - dr(TRIAD_RUNGS[i]) for i in (0, 1)] == [3, 3]
    # the four roles
    assert sorted(_orbit_triple(10)) == [1, 10, 26]
    assert 9 + dr(12) == 12 and 12 + 9 == rev(12)  # T314, both readings
    assert sorted(_orbit_triple(18)) == [18, 24, 32]   # the pipeline seed orbit

    # --- V: the chain ---
    assert 10 + 11 == 21 and 21 + 6 == 27 and 2 + 7 == 9
    assert [dr(v) for v in (10, 21, 27)] == [1, 3, 9]
    assert [3 ** k for k in (0, 1, 2)] == [1, 3, 9]
    assert dr(9 * 3) == 9 and 9 % 9 == 0           # tripling halts at 9
    assert 27 == 3 ** 3 == 999 // 37 == (10 ** 3 - 1) // 37
    assert 10 + 11 + 6 == 27
    assert 21 == tri(6) and 27 == tri(6) + 6
    assert 3 ** 2 == 3 + 3 + 3                     # why both lines end at 9

    print("All assertions passed.\n")
    print("I.  SPLITS OF 21 THAT SURVIVE REVERSAL")
    for a, b in splits:
        mark = "  <-- only one" if (a, b) in good else ""
        print(f"    {a:>2} + {b:>2} = 21   rev sum {rev(a) + rev(b):>3}"
              f"   rev(21) = {rev(21)}{mark}")
    print("    rule: equal digit length AND carry-free. derived, matches all 10.\n")

    print("II. FORWARD 8, MIRROR 9 -- THE EXTRA RUNG IS 10")
    print(f"    forward  n+9=rev(n): {fwd}")
    print(f"    mirror   n-9=rev(n): {mir}")
    print(f"    difference: {sorted(set(mir) - {rev(n) for n in fwd})}")
    print(f"    rev(10) = 1 drops a digit; the forward partner 01 is not")
    print(f"    two-digit. T313's 'missing rung' is 10 on the mirror side.\n")

    print("II-B. THE SAME GAP IN ROOT COORDINATES")
    print(f"    mirror steps by 11, and 11 = 2 mod 9 (a unit), so its roots")
    print(f"    step by 2 and must exhaust all nine:")
    print(f"      mirror  roots {[dr(n) for n in mir]}  -> all 9")
    print(f"      forward roots {[dr(n) for n in fwd]}    -> 8, missing 1")
    print(f"      difference "
          f"{sorted(set(dr(n) for n in mir) - set(dr(n) for n in fwd))}"
          f" = dr(10) = {dr(10)}")
    print(f"    the membership gap and the missing-root gap are ONE gap.")
    print(f"    the step-3 law of part IV does not apply here (step 11).")
    print()
    print("II-C. THE 0/9 SPLIT DOES NOT REACH THE ORBITS")
    print(f"    gcd(37,9) = 1 -> mod-9 and mod-37 independent (CRT)")
    print(f"    seed orbit 18 -> {26 * 18 % P} -> {26 * 24 % P} -> "
          f"{26 * 32 % P}, exact 3-cycle")
    print(f"    of {{18,24,32}} only 18 is in the 0/9 class (18 = 0 mod 9)")
    print(f"    -- a fact about its label, not about the cycle.")
    print()
    print("II-D. THE MIRROR SET MOD 37")
    print(f"    M mod 37 = {[n % P for n in mir]}")
    print(f"    step 11 mod 37 throughout; gcd(11,37)=1 so all 9 distinct")
    print(f"    opens on residue 10 (IC, the base), closes on residue 24")
    print(f"    (SEED, the pipeline seed residue 246 mod 37 = {246 % P})")
    print(f"    members landing in SEED: "
          f"{[n for n in mir if n % P in (18, 24, 32)]}")
    print(f"    observation grade -- no derivation links M to the seed.")
    print(f"    alignment: M[i+1]-F[i] = 9 (the definition);")
    print(f"    M[i]-F[i] = -2 = 35 mod 37 (only the AP offset).")
    print(f"    multiplicative relation: checked, non-constant, none.")
    print()

    print("III. 10 IS THE HINGE")
    print(f"    ord_37(10) = 3  ->  37 | 999  ->  111 = 3x37  ->  all digit laws")
    print(f"    137 mod 37 = 26,  26 x 10 mod 37 = {26 * 10 % P}  ->  10 = 26^-1")
    print(f"    10's 137-orbit = {sorted(_orbit_triple(10))}"
          f"  = identity, base, 137\n")

    print("IV. THE BLOCK 10..18")
    for n, role in ((10, "opens / base / 26^-1"), (12, "doubly closed (T314)"),
                    (15, "triad middle"), (18, "closes / seed orbit")):
        print(f"    {n:>3}  dr {dr(n)}  mod37 {n % P:>2}  "
              f"triple {str(sorted(_orbit_triple(n))):<14} {role}")
    print(f"    triad rungs {TRIAD_RUNGS} -> roots {[dr(n) for n in TRIAD_RUNGS]}")
    print(f"    same fact as T311 (3 multiples of 3 per 9-block), NOT a second.")
    print(f"    new: the map is step-preserving, AP(3) -> AP(3).\n")

    print("V.  THE CHAIN 10 -> 21 -> 27")
    print(f"    10 + 11 = 21,  21 + 6 = 27,  2 + 7 = 9")
    print(f"    roots {[dr(v) for v in (10, 21, 27)]} = 3^0, 3^1, 3^2;"
          f" halts at 9 (= 0 mod 9)")
    print(f"    27 = 3^3 = 999/37 = (10^3-1)/37 -- the cofactor of 37")
    print(f"    start 10 and end 27 are the two halves of 10^3-1 = 27 x 37")
    print(f"    addends 11 and 6 are chosen, not forced. the route is yours;")
    print(f"    the destination's identity is not.")


def _orbit_triple(x):
    x %= P
    return [x, 26 * x % P, 26 * 26 * x % P]


if __name__ == "__main__":
    run()
