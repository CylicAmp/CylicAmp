# CLASS: AUDIT
"""
Audit: the Easter day / year-interval digit correspondence 2->7, 3->8
Author: Michael Warren Song (CyclicAmp)
Verdict: the arithmetic is correct.  The correspondence is not.

=== THE SUPPLIED CLAIM, VERBATIM ===

    "2 -> 7,  3 -> 8   using the day number of the Easter date and the last
     digit of the year interval from April 3, 1979."

        Easter date        Year difference from 1979   Reduced   Alignment
        April 2, 2056      2056 - 1979 = 77            7         2 -> 7
        April 3, 2067      2067 - 1979 = 88            8         3 -> 8

    "year-interval digit = day number + 5"
    "2 + 5 = 7,   3 + 5 = 8"

=== WHAT IS CORRECT -- checked first, and all of it holds ===

  Both Easter dates are right, by the anonymous Gregorian algorithm, which was
  itself cross-checked against seven independently known Easters (1979, 2000,
  2024, 2025, 2026, 2027, 2038) before being trusted:

        Easter 2056 = Sunday, April 2, 2056     as claimed
        Easter 2067 = Sunday, April 3, 2067     as claimed

  Both subtractions are right:   2056 - 1979 = 77,   2067 - 1979 = 88.
  Both offsets are right:        2 + 5 = 7,          3 + 5 = 8.

  And the caveat stated in the write-up is right and worth keeping: April 2,
  2056 is one day short of a whole 77 years from April 3, so the exact elapsed
  interval is 77 years minus a day.  The correspondence is at the year-label
  level, which is how it was stated.

=== ONE PIECE OF MISSING INFORMATION, NOT GUESSED AT ===

  The anchor is given as April 3, 1979.  Easter 1979 was April 15, 1979, so
  April 3 that year is not Easter.  What April 3, 1979 is has not been
  supplied and is not inferred here.  Everything below holds for that anchor
  whatever it turns out to be, since only the year 1979 enters the arithmetic.

=== "REDUCED" HERE MEANS LAST DIGIT, NOT DIGITAL ROOT ===

  Elsewhere in this corpus reduction means the digital root.  It cannot mean
  that here:

        DR(77) = 5, not 7        DR(88) = 7, not 8

  Under digital roots the offsets are 3 and 4, not a constant 5, and the
  correspondence does not exist.  The claim works only under last-digit
  reduction.  That is a different operation and is labelled as such throughout.

=== WHY THE LAST-DIGIT STEP CARRIES NO INFORMATION ===

  77 and 88 are two-digit repdigits, and every two-digit repdigit is 11k:

        11k  has last digit  k,  for k = 1..9  -- forced, all nine checked

  So "77 reduces to 7" and "88 reduces to 8" are not observations about 1979,
  2056 or 2067.  They are the definition of a repdigit.  The only arithmetic
  content left in the claim is therefore the pairing itself: that the Easter
  day happens to be the repeated digit minus 5.

=== THE BASELINE, ESTABLISHED BEFORE ANY INTERPRETATION ===

  The rule "last digit of (y - 1979) = Easter day + c" was run at every offset
  c, not only at c = 5, over the 95 April Easters from 1979 to 2100:

        c = 5   ->  2 matches   (2056, 2067)
        mean over the 31 offsets that match at all  ->  3.06
        maximum at any offset                       ->  6   (at c = -12 and c = -3)

  The claimed offset is BELOW the average offset.  It is near the floor of the
  distribution, not a peak.  Nothing distinguishes 5 from any other value, and
  several other offsets do better.

  The structural reason: a last digit lies in 0..9, so c = 5 can only ever fire
  when the Easter day is 1..4.  There are 16 such years in 1979-2100, and if
  the last digit were unrelated to the day, about 16/10 = 1.6 of them would
  match by chance.  Two do.

        1979-2100   rule can fire 16    fires  2    expected 1.6    ratio 1.25
        1583-2300   rule can fire 91    fires  8    expected 9.1    ratio 0.88

  Widening the window moves the ratio to below one.  The effect does not
  survive leaving the two years it was read off.

=== VERDICT ===

  Every number in the supplied write-up is correct.  The two Easter dates, the
  two subtractions, the two sums.  Nothing in it is miscalculated.

  What it does not establish is a correspondence.  The offset 5 was read off
  the same two data points it is then said to govern -- two points and one free
  parameter -- and once the parameter is swept, 5 is an unremarkable value that
  performs worse than most.  Over the full Gregorian range the rule fires
  slightly less often than chance.

  Recorded as a negative result rather than discarded, so the ground is not
  covered twice.  The miss condition was declared in advance (sweep c; compare
  against the chance rate for the firing window) and it fired.

=== FALSIFICATION OF THIS AUDIT ===

  Supply a rule fixed independently of 2056 and 2067 -- an offset derived from
  something other than these two years -- that then selects them.  Or show that
  c = 5 beats the offset distribution on a range not containing them.  Either
  would overturn the verdict below, and both are tested for here and fail.
"""

FAIL = []


def check(cond, label, actual, expected):
    if not cond:
        FAIL.append(f"{label}: actual={actual!r}, expected={expected!r}")


def dr(x):
    return 9 if x == 0 else (x - 1) % 9 + 1


def easter(y):
    """Anonymous Gregorian algorithm. Returns (month, day)."""
    a = y % 19
    b, c = y // 100, y % 100
    d, e = b // 4, b % 4
    g = (8 * b + 13) // 25
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 19 * l) // 433
    n = (h + l - 7 * m + 90) // 25
    p = (h + l - 7 * m + 33 * n + 19) % 32
    return n, p


ANCHOR_YEAR = 1979
KNOWN_EASTERS = {1979: (4, 15), 2000: (4, 23), 2024: (3, 31), 2025: (4, 20),
                 2026: (4, 5), 2027: (3, 28), 2038: (4, 25)}


# ── the algorithm is trusted only after it reproduces known Easters ─────────
def test_easter_algorithm_is_sound():
    for y, md in KNOWN_EASTERS.items():
        check(easter(y) == md, f"Easter {y}", easter(y), md)
    # Easter is always a Sunday, and always between March 22 and April 25
    import datetime
    for y in range(1583, 2301):
        mo, dy = easter(y)
        d = datetime.date(y, mo, dy)
        check(d.weekday() == 6, f"Easter {y} is a Sunday", d.strftime('%A'), 'Sunday')
        check((mo, dy) >= (3, 22) and (mo, dy) <= (4, 25),
              f"Easter {y} in range", (mo, dy), "March 22 .. April 25")


# ── WHAT IS CORRECT in the supplied write-up ────────────────────────────────
def test_the_supplied_numbers_are_right():
    check(easter(2056) == (4, 2), "Easter 2056", easter(2056), (4, 2))
    check(easter(2067) == (4, 3), "Easter 2067", easter(2067), (4, 3))
    check(2056 - ANCHOR_YEAR == 77, "2056 - 1979", 2056 - ANCHOR_YEAR, 77)
    check(2067 - ANCHOR_YEAR == 88, "2067 - 1979", 2067 - ANCHOR_YEAR, 88)
    check(2 + 5 == 7, "2 + 5", 2 + 5, 7)
    check(3 + 5 == 8, "3 + 5", 3 + 5, 8)
    # the stated caveat: April 2 is a day short of a full 77 years from April 3
    import datetime
    span = datetime.date(2056, 4, 2) - datetime.date(ANCHOR_YEAR, 4, 3)
    full = datetime.date(2056, 4, 3) - datetime.date(ANCHOR_YEAR, 4, 3)
    check(span.days == full.days - 1, "77 years minus one day",
          full.days - span.days, 1)


# ── the anchor is not Easter 1979, and that is not guessed at ───────────────
def test_anchor_is_not_easter_1979():
    check(easter(ANCHOR_YEAR) == (4, 15), "Easter 1979", easter(ANCHOR_YEAR), (4, 15))
    check(easter(ANCHOR_YEAR) != (4, 3), "April 3 1979 is not Easter",
          easter(ANCHOR_YEAR), "not (4, 3)")


# ── "reduced" must mean last digit; the digital-root reading fails ──────────
def test_reduction_is_last_digit_not_digital_root():
    check(77 % 10 == 7 and 88 % 10 == 8, "last digits",
          (77 % 10, 88 % 10), (7, 8))
    check(dr(77) == 5, "DR(77)", dr(77), 5)
    check(dr(88) == 7, "DR(88)", dr(88), 7)
    # under last digit the offset is a constant 5
    check(77 % 10 - 2 == 5 and 88 % 10 - 3 == 5, "last-digit offsets",
          (77 % 10 - 2, 88 % 10 - 3), (5, 5))
    # under digital root it is not constant -- 3 and 4
    check(dr(77) - 2 != dr(88) - 3, "DR offsets are not equal",
          (dr(77) - 2, dr(88) - 3), "unequal")
    check((dr(77) - 2, dr(88) - 3) == (3, 4), "DR offsets",
          (dr(77) - 2, dr(88) - 3), (3, 4))


# ── the last-digit step is forced and carries no information ────────────────
def test_repdigit_last_digit_is_forced():
    for k in range(1, 10):
        check(11 * k % 10 == k, f"last digit of {11*k}", 11 * k % 10, k)
    check(77 == 11 * 7 and 88 == 11 * 8, "77 and 88 are 11k",
          (77 // 11, 88 // 11), (7, 8))


# ── THE BASELINE: sweep the offset before interpreting c = 5 ───────────────
def april_easters(lo, hi):
    return [(y, easter(y)[1]) for y in range(lo, hi + 1) if easter(y)[0] == 4]


def matches_at(offset, lo=1979, hi=2100):
    return [y for y, day in april_easters(lo, hi)
            if (y - ANCHOR_YEAR) % 10 == day + offset]


def test_offset_5_is_below_average():
    apr = april_easters(1979, 2100)
    check(len(apr) == 95, "April Easters 1979-2100", len(apr), 95)

    at5 = matches_at(5)
    check(at5 == [2056, 2067], "c=5 selects exactly the two named years",
          at5, [2056, 2067])

    counts = {c: len(matches_at(c)) for c in range(-30, 31)}
    nonzero = [n for n in counts.values() if n > 0]
    mean = sum(nonzero) / len(nonzero)
    check(counts[5] == 2, "matches at c=5", counts[5], 2)
    check(max(counts.values()) == 6, "best offset", max(counts.values()), 6)
    # the claim's offset does worse than the average offset that fires at all
    check(counts[5] < mean, "c=5 is below the mean offset",
          f"{counts[5]} < {mean:.2f}", True)
    better = [c for c, n in counts.items() if n > counts[5]]
    check(len(better) >= 20, "many offsets beat c=5", len(better), ">= 20")


def test_against_the_chance_rate():
    # c = 5 can only fire when the Easter day is 1..4, since a last digit is <= 9
    for lo, hi in ((1979, 2100), (1583, 2300)):
        apr = april_easters(lo, hi)
        window = [(y, d) for y, d in apr if d + 5 <= 9]
        fires = [(y, d) for y, d in window if (y - ANCHOR_YEAR) % 10 == d + 5]
        expected = len(window) / 10          # a last digit, if unrelated, is uniform
        check(all(1 <= d <= 4 for _, d in window),
              f"{lo}-{hi} firing window is days 1-4",
              sorted({d for _, d in window}), [1, 2, 3, 4])
        if (lo, hi) == (1979, 2100):
            check(len(window) == 16, "window size 1979-2100", len(window), 16)
            check(len(fires) == 2, "fires 1979-2100", len(fires), 2)
        else:
            # on the wider range the rule fires LESS often than chance
            check(len(fires) < expected,
                  f"{lo}-{hi}: observed below expected",
                  f"{len(fires)} < {expected:.1f}", True)
            check(len(fires) == 8 and len(window) == 91,
                  "wide-range counts", (len(fires), len(window)), (8, 91))


# ── falsification attempts, both of which fail ─────────────────────────────
def test_cannot_be_rescued():
    # 1. an offset fixed on a range NOT containing 2056/2067, applied to them
    early = april_easters(1583, 2000)
    counts = {c: len([y for y, d in early
                      if (y - ANCHOR_YEAR) % 10 == d + c]) for c in range(-30, 31)}
    best = max(counts, key=lambda c: counts[c])
    check(best != 5, "the best offset on 1583-2000 is not 5", best, "not 5")

    # 2. 2078 has the SAME Easter day as 2067 (April 3) and fails the rule,
    #    so the rule is not a property of the Easter date
    check(easter(2078) == (4, 3), "Easter 2078", easter(2078), (4, 3))
    check((2078 - ANCHOR_YEAR) % 10 != 3 + 5,
          "2078 fails despite matching day", (2078 - ANCHOR_YEAR) % 10, "!= 8")
    check(2078 not in matches_at(5), "2078 not selected", 2078, "absent")


def self_test():
    tests = [test_easter_algorithm_is_sound,
             test_the_supplied_numbers_are_right,
             test_anchor_is_not_easter_1979,
             test_reduction_is_last_digit_not_digital_root,
             test_repdigit_last_digit_is_forced,
             test_offset_5_is_below_average,
             test_against_the_chance_rate,
             test_cannot_be_rescued]
    for t in tests:
        t()
        print(f"  ok  {t.__name__}")
    if FAIL:
        for f in FAIL:
            print(f"  FAIL  {f}")
        raise AssertionError(f"{len(FAIL)} check(s) failed")

    print()
    print("CORRECT in the supplied write-up -- all of it:")
    print("  Easter 2056 = April 2, 2056     Easter 2067 = April 3, 2067")
    print("  2056 - 1979 = 77                2067 - 1979 = 88")
    print("  2 + 5 = 7                       3 + 5 = 8")
    print("  and the stated caveat: April 2 is 77 years minus one day from April 3")
    print()
    print("MISSING, not guessed at:")
    print("  Easter 1979 was April 15.  What April 3, 1979 is has not been supplied.")
    print()
    print("THE REDUCTION:")
    print("  last digit, not digital root.  DR(77) = 5 and DR(88) = 7, giving")
    print("  offsets 3 and 4 -- not a constant.  Only last-digit gives 5.")
    print("  And 11k has last digit k for every k, so '77 -> 7' is the definition")
    print("  of a two-digit repdigit, not a fact about these years.")
    print()
    print("THE BASELINE -- swept before interpreting:")
    counts = {c: len(matches_at(c)) for c in range(-30, 31)}
    nz = [n for n in counts.values() if n > 0]
    print(f"  c = 5 matches {counts[5]} of 95 April Easters: {matches_at(5)}")
    print(f"  mean over offsets that match at all: {sum(nz)/len(nz):.2f}")
    print(f"  best offset: {max(counts.values())} matches")
    print(f"  offsets that beat c = 5: {len([c for c,n in counts.items() if n>counts[5]])}")
    print()
    print("  firing window is Easter day 1-4, so by chance:")
    print("    1979-2100   16 candidates, expected 1.6, observed 2   ratio 1.25")
    print("    1583-2300   91 candidates, expected 9.1, observed 8   ratio 0.88")
    print()
    print("VERDICT: every number correct; the correspondence is not established.")
    print("  The offset was read off the same two years it is said to govern.")
    print("  Swept, 5 is unremarkable and below average, and over the full")
    print("  Gregorian range the rule fires slightly less often than chance.")
    print("  2078 has Easter on April 3 like 2067 and fails, so the rule is not")
    print("  a property of the Easter date.  Recorded as a negative result.")


if __name__ == "__main__":
    self_test()
