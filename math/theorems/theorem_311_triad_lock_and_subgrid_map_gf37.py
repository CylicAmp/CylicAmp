# CLASS: THEOREM
"""
Theorem 311: The {3,6,9} triad is exactly the fixed set of dr(2A) = dr(T_A),
plus the 9x9 sub-grid map -- with three claims corrected
Author: Michael Warren Song (CyclicAmp)

=== THE RESULT ===

    Over the 9 diagonal coordinates (A,A) of the 81-pair matrix, ask where
    the pair's digital root matches the triangular cycle root:

        dr(2A) = dr(T_A),    T_A = A(A+1)/2

    This holds for A = 3, 6, 9 and for no other digit. Exactly three of
    nine lock -- a real count, not a guaranteed one.

MECHANISM (derived, then stress-tested before being written down)
    dr(2A) = dr(T_A)  <=>  4A = A(A+1)  (mod 9)
                      <=>  A^2 - 3A = 0 (mod 9)
                      <=>  A(A-3)     = 0 (mod 9)
                      <=>  A          = 0 (mod 3)
    So the lock set is exactly the multiples of 3. Verified with zero
    counterexamples for A = 1..499, not just the nine digits.

=== VERIFIED FROM THE SUB-GRID MAP ===

    Sub-grid forward differences (B-A over blocks 123/456/789) are exactly
      [[0,+333,+666], [-333,0,+333], [-666,-333,0]]
    and 333 = 37 x 9 -- the same 37 that runs through 111 = 3 x 37 (T310)
    and the block map B=27x (T303).

    Diagonal sub-grid block sums all reduce to DR 3:
      123+123 = 246 (DR 3),  456+456 = 912 (DR 3),  789+789 = 1578 (DR 3)
    The first of those is 246 -- the pipeline's reference seed, reached
    here as a diagonal block sum rather than as a bounded prime gap.

    Reversal shift: rev(b) - b = 198 for b in {123,456,789}, and
    dr(198) = 9. This is the reversal-difference law 99(a-c) with
    a-c = -2 (T398's 198 = 18 x 11).

    Sliding-window DRs for 123,234,...,912 lock to 6,9,3 repeating.
    Step sizes 111,102,21,789 are all multiples of 3 (111 = 3 x 37).

    {3,6,9} is closed under addition-then-DR (it is the subgroup 3Z/9Z),
    and triad + non-triad is never triad (a coset argument, forced).

    n x 3 for n=1..6 gives 3,6,9,12,15,18 with DRs 3,6,9,3,6,9.
    Channel weights (1,2,3,2,1) squared give the palindrome 1,4,9,4,1.

=== THREE CLAIMS CORRECTED (kept with the numbers that killed them) ===

 1. "For ALL consecutive 3-digit spans, number minus reverse is 198."
    VERDICT: FALSIFIED at the wrap-around.
      891 - 198 = 693,  912 - 219 = 693,  not 198.
    198 holds for the seven non-wrapping windows 123..789 only. The true
    law is 99(a-c): a-c = -2 for a non-wrapping window (giving 198), but
    the wrap makes a-c = 7 (giving 693). The constant is a property of
    the window not wrapping, not of 3-digit spans generally.

 2. "Non-triad numbers can never enter the triad sub-circuit."
    VERDICT: FALSIFIED as stated. 18 counterexamples, e.g.
      1+2 -> 3,  1+5 -> 6,  1+8 -> 9.
    Two non-triad digits CAN sum into the triad. What is true is the
    narrower statement: triad + non-triad is never triad (0 exceptions).
    That is the coset fact; the broader claim is not.

 3. "The root stream mirrors about the center step n=5 (R_5=6)."
    VERDICT: FALSIFIED. The mirror axis is n=4, not n=5:
      stream = 1,3,6,1,6,3,1,9,9 and R_n = R_(8-n), since
      T_(8-n) - T_n = 36 - 9n = 0 (mod 9).
    About n=5 it fails immediately: R_4 = 1 but R_6 = 3.

=== VERDICT LABELS CORRECTED (added after review; originals left verbatim) ===

    The three verdicts above are kept exactly as first written. Two of the
    three labels are wrong, and this is the correction rather than an edit
    of the text -- corrections stay in place in this repo.

 1. Labelled FALSIFIED. Should be SCOPE CLARIFIED.
    The claim's mechanism survives intact: rev(n) - n = 99(a-c) for every
    3-digit span, wrapping or not. The stated constant 198 was the value
    of that mechanism on a sub-domain (a-c = -2, the seven non-wrapping
    windows). The wrap does not break the law, it changes a-c to 7 and
    the same law returns 693. Nothing was refuted; the domain on which
    the constant is 198 was narrowed. Both values come out of one formula.

 2. Labelled FALSIFIED. Correct as labelled -- no change.
    "Non-triad numbers can never enter the triad sub-circuit" is false as
    a statement, not merely over-broad: 1+2 = 3 contradicts it directly.
    The true statement (triad + non-triad is never triad) is a DIFFERENT
    statement over different operands, not a restriction of this one.
    FALSIFIED is the right label.

 3. Labelled FALSIFIED. Should be PARAMETER CORRECTED.
    The claimed phenomenon -- that the root stream has a mirror symmetry --
    is real and forced: R_n = R_(8-n), because T_(8-n) - T_n = 36 - 9n = 0
    (mod 9). Only the axis was wrong (n=4, not n=5). A theorem that names
    the right symmetry and the wrong constant has a bad constant, not a
    dead claim.

    Net: of three "corrections", one claim died (2) and two were
    re-scoped (1, 3). The earlier tally of three falsifications
    overstated how much was refuted. Recorded, not rewritten.

=== FALSIFICATION ===
    Any assert below failing.
"""

P = 37


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


def tri(n):
    return n * (n + 1) // 2


def rev(n):
    return int(str(n)[::-1])


def digit_sum(n):
    return sum(int(c) for c in str(n))


BLOCKS = [123, 456, 789]
WINDOWS = [123, 234, 345, 456, 567, 678, 789, 891, 912]


def run():
    # --- the result: triad lock ---
    lock = [A for A in range(1, 10) if dr(2 * A) == dr(tri(A))]
    assert lock == [3, 6, 9]
    # mechanism, checked far past the nine digits
    for A in range(1, 500):
        assert (dr(2 * A) == dr(tri(A))) == ((A * (A - 3)) % 9 == 0) == (A % 3 == 0)

    # --- sub-grid map ---
    diffs = [[b - a for b in BLOCKS] for a in BLOCKS]
    assert diffs == [[0, 333, 666], [-333, 0, 333], [-666, -333, 0]]
    assert 333 == 37 * 9 and 111 == 3 * 37
    assert [dr(b + b) for b in BLOCKS] == [3, 3, 3]
    assert 123 + 123 == 246                      # the pipeline seed
    assert [rev(b) - b for b in BLOCKS] == [198, 198, 198]
    assert dr(198) == 9
    assert [dr(digit_sum(w)) for w in WINDOWS] == [6, 9, 3] * 3
    steps = [WINDOWS[i + 1] - WINDOWS[i] for i in range(8)] + [123 - 912]
    assert all(s % 3 == 0 for s in steps)
    assert [dr(3 * n) for n in range(1, 7)] == [3, 6, 9, 3, 6, 9]
    assert [c * c for c in (1, 2, 3, 2, 1)] == [1, 4, 9, 4, 1]

    # --- {3,6,9} closure, and the exact scope of it ---
    assert all(dr(a + b) in (3, 6, 9) for a in (3, 6, 9) for b in (3, 6, 9))
    assert not any(dr(a + b) in (3, 6, 9)
                   for a in (3, 6, 9) for b in range(1, 10) if b % 3)

    # --- correction 1: 198 fails at the wrap ---
    assert rev(891) == 198 and 891 - rev(891) == 693
    assert 912 - rev(912) == 693
    assert all(rev(w) - w == 198 for w in WINDOWS[:7])
    assert 99 * (8 - 1) == 693 and 99 * 2 == 198

    # --- correction 2: non-triad pairs DO reach the triad ---
    entrants = [(a, b) for a in range(1, 10) for b in range(1, 10)
                if a % 3 and b % 3 and dr(a + b) in (3, 6, 9)]
    assert len(entrants) == 18
    assert (1, 2) in entrants

    # --- correction 3: mirror axis is n=4, not n=5 ---
    assert all(dr(tri(n)) == dr(tri(8 - n)) for n in range(1, 8))
    assert dr(tri(4)) == 1 and dr(tri(6)) == 3     # kills the n=5 axis

    # --- label correction 1: one law covers both 198 and 693 ---
    # rev(n) - n = 99(a - c) for EVERY 3-digit n, wrap included.
    for n in range(100, 1000):
        a, c = n // 100, n % 10
        assert rev(n) - n == 99 * (c - a)
    for w in WINDOWS:
        a, c = w // 100, w % 10
        assert rev(w) - w == 99 * (c - a)
    assert [w // 100 - w % 10 for w in WINDOWS] == [-2] * 7 + [7, 7]

    # --- label correction 3: the mirror is forced, only the axis moved ---
    assert all(tri(8 - n) - tri(n) == 36 - 9 * n for n in range(0, 9))
    assert all((36 - 9 * n) % 9 == 0 for n in range(0, 9))
    # the congruence is exact for all n in 0..8:
    assert all((tri(8 - n) - tri(n)) % 9 == 0 for n in range(0, 9))
    # the dr form holds on 1..7. it fails ONLY at the n=0/n=8 endpoint,
    # and only because of the dr(0)=0 convention: tri(0)=0 -> dr 0, while
    # tri(8)=36 -> dr 9. same residue class, different label. recorded.
    assert all(dr(tri(n)) == dr(tri(8 - n)) for n in range(1, 8))
    assert dr(tri(0)) == 0 and dr(tri(8)) == 9 and (36 - 0) % 9 == 0

    print("All assertions passed.\n")
    print("TRIAD LOCK  dr(2A) vs dr(T_A):")
    for A in range(1, 10):
        a, b = dr(2 * A), dr(tri(A))
        print(f"  A={A}  dr(2A)={a}  dr(T_{A})={b}  {'LOCK' if a == b else ''}")
    print(f"\n  lock set = {lock} = multiples of 3, forced by A(A-3)=0 mod 9\n")

    print("SUB-GRID MAP (blocks 123/456/789):")
    for i, a in enumerate(BLOCKS):
        row = "  ".join(f"{diffs[i][j]:+5d}" for j in range(3))
        print(f"  row {a}:  {row}      centers ({(a//100)+1},*)")
    print(f"  333 = 37 x 9    diagonal block sums DR: {[dr(b + b) for b in BLOCKS]}")
    print(f"  123+123 = 246 (pipeline seed), mod 37 = {246 % P}\n")

    print("CORRECTIONS:")
    print(f"  1. rev-diff 198 holds for 7 windows; wrap gives 693 "
          f"(891->{891 - rev(891)}, 912->{912 - rev(912)})")
    print(f"  2. non-triad pairs reaching triad: {len(entrants)} "
          f"(e.g. 1+2=3) -- only triad+non-triad is closed off")
    print(f"  3. mirror axis n=4 (R_n=R_(8-n)), not n=5: "
          f"R_4={dr(tri(4))} vs R_6={dr(tri(6))}")

    print("\nVERDICT LABELS (corrected after review, originals kept):")
    print("  1. SCOPE CLARIFIED -- rev(n)-n = 99(a-c) holds for all 900")
    print(f"     3-digit n; 198 is that law at a-c=-2, 693 at a-c=7.")
    print("  2. FALSIFIED -- stands. 1+2=3 contradicts the claim outright.")
    print("  3. PARAMETER CORRECTED -- the mirror R_n=R_(8-n) is forced by")
    print("     T_(8-n)-T_n = 36-9n = 0 mod 9; only the axis was wrong.")
    print("  net: 1 claim dead, 2 re-scoped -- not 3 falsifications.")


if __name__ == "__main__":
    run()
