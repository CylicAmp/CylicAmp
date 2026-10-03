# CLASS: THEOREM
"""
Theorem 350: the Kaprekar step is 99(a-c), and it subtracts the reversal
class from the own class
Author: Michael Warren Song (CyclicAmp)

"358-853" was supplied earlier and analysed as two separate numbers.  It is
one operation: 853 - 358 = 495, the Kaprekar step on the digits {3,5,8}.

=== THE STEP HAS A CLOSED FORM ===

    For digits a >= b >= c, descending is 100a+10b+c and ascending is
    100c+10b+a, so

        Kaprekar(n) = 99(a - c)

    The middle digit cancels entirely.  Zero counterexamples over all 900
    three-digit words.  The step depends only on the SPREAD of the digits.

    Consequences, all forced:

      * the entire range of the step is nine numbers, 99k for k = 1..9
      * 99 == 25 (mod 37), so the output is 25k mod 37
      * 495 is the fixed point because it is the unique k in 1..9 with
        99k having digit spread k: 495 has digits 4,9,5, max-min = 5,
        and 99 x 5 = 495.  Checked for every k; only k = 5 closes.

        k    99k    mod 37   orbit
        1     99      25     SA_ST_B
        2    198      13     CAS_EXT
        3    297       1     IC
        4    396      26     IC
        5    495      14     C9        <- fixed point
        6    594       2     DARK_A
        7    693      27     NEG_H
        8    792      15     DARK_A
        9    891       3     C3

=== AND IT IS A ROTATION-CLASS DIFFERENCE ===

    Descending and ascending are REVERSALS of each other, and reversal
    swaps the two rotation classes (T325).  So the Kaprekar step is always

        (an element of the own class) - (an element of the reversal class)

    For 495: 954 lies in {495,549,954} = C9, and 459 lies in
    {594,459,945} = DARK_A.  In residues, 29 - 15 = 14.

    Reversal is NOT negation here, and should not be read as such: T326's
    reversal-is-negation holds for arithmetic-progression triples, and
    4,9,5 is not one (differences 5 and -4).  Indeed -C9 = TESLA, not
    DARK_A.

=== THE SUPPLIED PAIR ===

        358 ascending, 853 descending, spread 8 - 3 = 5
        853 - 358 = 495 = 99 x 5

    139 of the 900 three-digit words have spread 5, and every one of them
    reaches 495 in a single step.  358 and 853 are two of them; so is 495.

=== FALSIFICATION ===
    A three-digit word whose Kaprekar step is not 99(max - min).
"""

P = 37
ORBITS = {
    'IC': (1, 10, 26),      'DARK_A': (2, 15, 20),  'C3': (3, 4, 30),
    'CAS_EXT': (5, 13, 19), 'TESLA': (6, 8, 23),    'D7': (7, 33, 34),
    'SA_ST_A': (9, 12, 16), 'NEG_H': (11, 27, 36),  'C9': (14, 29, 31),
    'NQR17': (17, 22, 35),  'SEED': (18, 24, 32),   'SA_ST_B': (21, 25, 28),
}
BY = {r: n for n, o in ORBITS.items() for r in o}


def kaprekar(n):
    d = f"{n:03d}"
    return int("".join(sorted(d, reverse=True))) - int("".join(sorted(d)))


def spread(n):
    d = f"{n:03d}"
    return int(max(d)) - int(min(d))


def rotclass(n):
    d = f"{n:03d}"
    return {int(d[k:] + d[:k]) for k in (0, 2, 1)}


def run():
    # --- the closed form ---
    for n in range(100, 1000):
        assert kaprekar(n) == 99 * spread(n), n
    assert 99 % P == 25

    # --- the nine outputs ---
    out = {99 * k: (99 * k) % P for k in range(1, 10)}
    assert list(out) == [99, 198, 297, 396, 495, 594, 693, 792, 891]
    assert [v for v in out.values()] == [25, 13, 1, 26, 14, 2, 27, 15, 3]
    assert all((99 * k) % P == (25 * k) % P for k in range(1, 10))

    # --- 495 is the unique fixed point ---
    assert [k for k in range(1, 10) if spread(99 * k) == k] == [5]
    assert kaprekar(495) == 495 and spread(495) == 5 and 99 * 5 == 495
    x, chain = 321, []
    for _ in range(12):
        x = kaprekar(x)
        chain.append(x)
        if x == 495:
            break
    assert chain == [198, 792, 693, 594, 495]

    # --- own class minus reversal class ---
    for n in (495, 321, 853, 762, 187):
        d = f"{n:03d}"
        hi = int("".join(sorted(d, reverse=True)))
        lo = int("".join(sorted(d)))
        assert lo == int(str(hi).zfill(3)[::-1])          # exact reversals
        assert lo in rotclass(int(str(hi).zfill(3)[::-1]))
        assert hi in rotclass(n) or spread(n) == 0
    assert rotclass(495) == {495, 549, 954}
    assert {x % P for x in rotclass(495)} == set(ORBITS['C9'])
    assert rotclass(594) == {594, 459, 945}
    assert {x % P for x in rotclass(594)} == set(ORBITS['DARK_A'])
    assert (954 - 459) % P == (29 - 15) % P == 14

    # --- reversal is not negation here ---
    assert {(P - x) % P for x in ORBITS['C9']} == set(ORBITS['TESLA'])
    assert BY[459 % P] == 'DARK_A' != 'TESLA'
    assert (9 - 4, 5 - 9) == (5, -4)                      # not an AP

    # --- the supplied pair ---
    assert 853 - 358 == 495 == 99 * 5
    assert spread(358) == spread(853) == 5
    s5 = [n for n in range(100, 1000) if spread(n) == 5]
    assert len(s5) == 139
    assert all(kaprekar(n) == 495 for n in s5)
    assert 358 in s5 and 853 in s5 and 495 in s5

    print("All assertions passed.\n")
    print("THEOREM 350.  Kaprekar(n) = 99(max - min).\n")
    print("   the middle digit cancels; 0 counterexamples in 900 words")
    print(f"   99 == {99%P} mod 37, so the output is 25k\n")
    print("    k    99k   mod 37   orbit")
    for k in range(1, 10):
        v = 99 * k
        print(f"    {k}   {v:4d}     {v%P:3d}    {BY[v%P]}"
              + ("   <- fixed point" if k == 5 else ""))
    print("\n   495 is fixed because it is the unique k with spread(99k) = k")
    print(f"   routine from 321: {' -> '.join(map(str,chain))}\n")
    print("  OWN CLASS MINUS REVERSAL CLASS")
    print("   descending and ascending are reversals, and reversal swaps the")
    print("   two rotation classes (T325), so every step has that form.")
    print(f"   495: 954 in {sorted(rotclass(495))} = C9")
    print(f"        459 in {sorted(rotclass(594))} = DARK_A")
    print(f"        residues 29 - 15 = 14\n")
    print("   reversal is NOT negation here: -C9 = TESLA, and 4,9,5 is not")
    print("   an AP, so T326's reversal-is-negation does not apply.\n")
    print("  THE SUPPLIED PAIR")
    print("   358 ascending, 853 descending, spread 8-3 = 5")
    print(f"   853 - 358 = {853-358} = 99 x 5")
    print(f"   {len(s5)} of 900 words have spread 5; every one reaches 495")
    print("   in a single step. 358, 853 and 495 are all among them.")


if __name__ == "__main__":
    run()
