"""
mirror_cycle_audit.py

Doubling-cycle mirror subtraction grid.

─────────────────────────────────────────────────────────────────
STRUCTURE:

  Each row has a 6-digit number A whose digits follow the pattern
  [d, 0, d, d, d, next(d)] where d is a doubling-cycle value and
  next(d) is the following element in the cycle 1→2→4→8→7→5→1.
  B = reverse(A).

  Doubling cycle: 1 → 2 → 4 → 8 → 7 → 5 → (1, loop)

─────────────────────────────────────────────────────────────────
THE GRID (verified):

  Row  A        B        A−B        DR(|A−B|)
  1    101112   211101   −109989    9
  2    202224   422202   −219978    9
  3    404448   844404   −439956    9
  4    808887   788808    +20079    9
  5    707775   577707   +130068    9
  6    505551   155505   +350046    9
  7    101112   211101   −109989    (loop closes)

─────────────────────────────────────────────────────────────────
CLOSED FORM:

  A = d·101110 + next(d)          (digit structure [d,0,d,d,d,e])
  B = next(d)·100000 + d·11101   (reverse)

  A − B = d·90009 − next(d)·99999
        = 9 · (10001·d − 11111·next(d))

  90009 = 9 × 10001
  99999 = 9 × 11111
  ∴ every result is divisible by 9 → DR(|result|) = 9 always.

─────────────────────────────────────────────────────────────────
THE 9 PRINCIPLE (why every result collapses to DR=9):

  n ≡ digit_sum(n) (mod 9) for any n.
  digit_sum(n) = digit_sum(reverse(n))  (same digits, different order).
  ∴ n ≡ reverse(n) (mod 9)  →  n − reverse(n) ≡ 0 (mod 9).
  This holds for ANY number; it is not specific to this sequence.

─────────────────────────────────────────────────────────────────
DOUBLING IN THE RESULTS — PARTIAL:

  Rows 1→2→3 double exactly:
    Result(d=1) = −109989
    Result(d=2) = −219978 = 2 × Result(d=1)   ✓
    Result(d=4) = −439956 = 2 × Result(d=2)   ✓

  This holds because for d=1,2,4: next(d) = 2d (literal doubling),
  so Result(d) = 9(10001·d − 11111·2d) = 9·d·(10001−22222) = −109989·d.

  Rows 4→5→6 do NOT double in the results:
    Row4/Row3: 20079 / −439956 ≈ −0.046   (not −2)
    Row5/Row4: 130068 / 20079 ≈ 6.48      (not 2)
    Row6/Row5: 350046 / 130068 ≈ 2.69     (not 2)

  Why: at d=8, next(d)=7 (not 2×8=16). The doubling cycle tracks
  DR values (digital roots), not literal doublings. 2×8=16, DR(16)=7.
  The result formula uses actual digits, not DRs.

─────────────────────────────────────────────────────────────────
TOTALS:

  Negative rows (1,2,3): −769923    DR=9
  Positive rows (4,5,6): +500193    DR=9
  Net total:             −269730    DR=9

  Proof via closed form:
    Total = Σ(d·90009 − next(d)·99999) over cycle [1,2,4,8,7,5]
          = 90009·Σd − 99999·Σnext(d)
    Σd = Σnext(d) = 1+2+4+8+7+5 = 27  (same set, cyclic permutation)
    Total = 27·(90009 − 99999) = 27·(−9990) = −269730

─────────────────────────────────────────────────────────────────
"""

FAIL = []


def check(cond, label, actual, expected):
    if not cond:
        FAIL.append(f"{label}: actual={actual!r}, expected={expected!r}")
    return cond


def dr(n):
    if n == 0:
        return 0
    r = abs(n) % 9
    return r if r else 9


DOUBLING_CYCLE = [1, 2, 4, 8, 7, 5]

ROWS = [
    (101112, 211101),
    (202224, 422202),
    (404448, 844404),
    (808887, 788808),
    (707775, 577707),
    (505551, 155505),
]

EXPECTED_DIFFS = [-109989, -219978, -439956, 20079, 130068, 350046]


# ── Arithmetic ────────────────────────────────────────────────────────────────

for i, ((a, b), expected) in enumerate(zip(ROWS, EXPECTED_DIFFS)):
    diff = a - b
    check(diff == expected,
          f"row {i+1}: {a} − {b}", diff, expected)

# Row 7 (unstored) would repeat row 1 because cycle period = 6
check(DOUBLING_CYCLE[6 % 6] == DOUBLING_CYCLE[0],
      "row 7 d = row 1 d (cycle period 6)", DOUBLING_CYCLE[6 % 6], DOUBLING_CYCLE[0])


# ── Digit structure: B = reverse(A) ──────────────────────────────────────────

for i, (a, b) in enumerate(ROWS):
    check(str(a) == str(b)[::-1],
          f"row {i+1}: B = reverse(A)", str(b)[::-1], str(a))

# Digit pattern [d, 0, d, d, d, next(d)]
for i, (a, b) in enumerate(ROWS):
    d    = DOUBLING_CYCLE[i]
    nd   = DOUBLING_CYCLE[(i + 1) % 6]
    digits_a = [int(x) for x in str(a)]
    check(digits_a == [d, 0, d, d, d, nd],
          f"row {i+1} digit pattern [d,0,d,d,d,next(d)]",
          digits_a, [d, 0, d, d, d, nd])


# ── The 9 principle ───────────────────────────────────────────────────────────

# n - reverse(n) ≡ 0 (mod 9) for any n
for i, (a, b) in enumerate(ROWS):
    diff = a - b
    check(diff % 9 == 0,
          f"row {i+1}: (A−B) divisible by 9", diff % 9, 0)
    check(dr(abs(diff)) == 9,
          f"row {i+1}: DR(|A−B|) = 9", dr(abs(diff)), 9)

# General proof: same digit sum → same mod-9 residue
for a, b in ROWS:
    check(sum(int(x) for x in str(a)) == sum(int(x) for x in str(b)),
          f"digit_sum({a}) = digit_sum({b})",
          sum(int(x) for x in str(a)), sum(int(x) for x in str(b)))


# ── Closed form ───────────────────────────────────────────────────────────────

# A = d*101110 + next(d);  B = next(d)*100000 + d*11101
# A - B = d*90009 - next(d)*99999

check(101110 - 11101 == 90009, "101110 − 11101 = 90009", 101110 - 11101, 90009)
check(100000 - 1 == 99999, "100000 − 1 = 99999", 100000 - 1, 99999)

for i, (a, b) in enumerate(ROWS):
    d   = DOUBLING_CYCLE[i]
    nd  = DOUBLING_CYCLE[(i + 1) % 6]
    cf  = 90009 * d - 99999 * nd
    diff = a - b
    check(cf == diff,
          f"row {i+1}: closed form 90009·{d} − 99999·{nd} = {diff}",
          cf, diff)

# Both constants divisible by 9
check(90009 % 9 == 0, "90009 = 9×10001", 90009 % 9, 0)
check(99999 % 9 == 0, "99999 = 9×11111", 99999 % 9, 0)
check(90009 // 9 == 10001, "90009/9 = 10001", 90009 // 9, 10001)
check(99999 // 9 == 11111, "99999/9 = 11111", 99999 // 9, 11111)


# ── Doubling in results — rows 1–3 only ──────────────────────────────────────

# For d=1,2,4: next(d) = 2d exactly, so Result(d) = -109989*d
check(EXPECTED_DIFFS[0] == -109989, "row 1 result = −109989", EXPECTED_DIFFS[0], -109989)
check(EXPECTED_DIFFS[1] == 2 * EXPECTED_DIFFS[0],
      "row 2 = 2 × row 1", EXPECTED_DIFFS[1], 2 * EXPECTED_DIFFS[0])
check(EXPECTED_DIFFS[2] == 2 * EXPECTED_DIFFS[1],
      "row 3 = 2 × row 2", EXPECTED_DIFFS[2], 2 * EXPECTED_DIFFS[1])

# Factor: -109989 × d for d in {1,2,4}
BASE = -109989
for i in range(3):
    d = DOUBLING_CYCLE[i]
    check(EXPECTED_DIFFS[i] == BASE * d,
          f"row {i+1}: result = {BASE}×{d}", EXPECTED_DIFFS[i], BASE * d)

# Rows 4–6: doubling breaks because next(d) ≠ 2d
for i in range(3, 6):
    d  = DOUBLING_CYCLE[i]
    nd = DOUBLING_CYCLE[(i + 1) % 6]
    check(nd != 2 * d,
          f"row {i+1}: next({d})={nd} ≠ 2×{d}={2*d} (doubling stops)",
          nd, f"≠{2*d}")
    check(EXPECTED_DIFFS[i] != 2 * EXPECTED_DIFFS[i - 1],
          f"row {i+1}: result is not 2×row{i}",
          EXPECTED_DIFFS[i] != 2 * EXPECTED_DIFFS[i - 1], True)

# Why: the cycle tracks DR values (2×8=16, DR=7), not literal digit doubling
check(dr(2 * 8) == 7, "DR(2×8) = DR(16) = 7 = next(8) in cycle", dr(2 * 8), 7)
check(dr(2 * 7) == 5, "DR(2×7) = DR(14) = 5 = next(7) in cycle", dr(2 * 7), 5)
check(dr(2 * 5) == 1, "DR(2×5) = DR(10) = 1 = next(5) in cycle", dr(2 * 5), 1)


# ── Totals ────────────────────────────────────────────────────────────────────

neg_sum  = sum(x for x in EXPECTED_DIFFS if x < 0)
pos_sum  = sum(x for x in EXPECTED_DIFFS if x > 0)
total    = sum(EXPECTED_DIFFS)

check(neg_sum == -769923, "negative sum = −769923", neg_sum, -769923)
check(pos_sum ==  500193, "positive sum = +500193", pos_sum,  500193)
check(total   == -269730, "net total = −269730", total, -269730)

check(dr(abs(neg_sum)) == 9, "DR(769923) = 9", dr(abs(neg_sum)), 9)
check(dr(pos_sum) == 9,      "DR(500193) = 9", dr(pos_sum), 9)
check(dr(abs(total)) == 9,   "DR(269730) = 9", dr(abs(total)), 9)

# Proof via closed form: Σd = Σnext(d) = 27 (same cycle)
CYCLE_SUM = sum(DOUBLING_CYCLE)
check(CYCLE_SUM == 27, "Σ(cycle) = 1+2+4+8+7+5 = 27", CYCLE_SUM, 27)
check(dr(27) == 9, "DR(27) = 9 = NULL", dr(27), 9)
check(27 * (90009 - 99999) == -269730,
      "total = 27×(90009−99999) = 27×(−9990) = −269730",
      27 * (90009 - 99999), -269730)
check(27 * (-9990) == -269730, "27×(−9990) = −269730", 27 * (-9990), -269730)

# DR of the net total
check(dr(9990) == 9, "DR(9990) = 9 = NULL", dr(9990), 9)
check(dr(27) == 9, "DR(27) = 9", dr(27), 9)
check(dr(269730) == 9, "DR(269730) = DR(net) = 9", dr(269730), 9)


# ── Output ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Mirror Cycle Audit — Doubling-Cycle Subtraction Grid")
    print("=" * 66)

    print(f"\n── The grid (verified) ──")
    print(f"  {'Row':<4} {'A':>8} {'B':>8} {'A−B':>10}  DR")
    for i, (a, b) in enumerate(ROWS):
        diff = a - b
        d  = DOUBLING_CYCLE[i]
        nd = DOUBLING_CYCLE[(i + 1) % 6]
        print(f"  {i+1:<4} {a:>8} {b:>8} {diff:>+10}  {dr(abs(diff))}  "
              f"[d={d}→next={nd}]")
    print(f"  (Row 7 = Row 1; loop closes)")

    print(f"\n── Closed form: A−B = 90009·d − 99999·next(d) ──")
    print(f"  90009 = 9 × 10001")
    print(f"  99999 = 9 × 11111")
    print(f"  Every result = 9 × (10001·d − 11111·next(d)) → DR=9 always")

    print(f"\n── 9 Principle ──")
    print(f"  reverse(n) has same digits as n → same digit sum → n ≡ reverse(n) mod 9")
    print(f"  ∴ n − reverse(n) ≡ 0 mod 9 for ANY n.  Universal, not specific to this grid.")

    print(f"\n── Doubling in results ──")
    print(f"  Rows 1→2→3: exact ×2 each step")
    print(f"    row 1 = {BASE}×1 = {BASE}")
    print(f"    row 2 = {BASE}×2 = {BASE*2}")
    print(f"    row 3 = {BASE}×4 = {BASE*4}")
    print(f"  Holds because next(1)=2, next(2)=4, next(4)=8 are literal doublings.")
    print(f"  Rows 4→5→6: doubling STOPS.")
    print(f"    next(8)=7 (not 16); next(7)=5 (not 14); next(5)=1 (not 10).")
    print(f"    The cycle tracks DR values: DR(2×8)=DR(16)=7, etc.")
    print(f"    Row4/Row3: {EXPECTED_DIFFS[3]/EXPECTED_DIFFS[2]:.4f}  (not 2)")
    print(f"    Row5/Row4: {EXPECTED_DIFFS[4]/EXPECTED_DIFFS[3]:.4f}  (not 2)")
    print(f"    Row6/Row5: {EXPECTED_DIFFS[5]/EXPECTED_DIFFS[4]:.4f}  (not 2)")

    print(f"\n── Totals ──")
    print(f"  Negatives (rows 1,2,3): {neg_sum}   DR={dr(abs(neg_sum))}")
    print(f"  Positives (rows 4,5,6): +{pos_sum}    DR={dr(pos_sum)}")
    print(f"  Net:                   {total}    DR={dr(abs(total))}")
    print(f"  Proof: Σd = Σnext(d) = 27; net = 27×(90009−99999) = 27×(−9990) = −269730")
    print(f"  DR(27)=9, DR(9990)=9, DR(269730)=9: NULL through every layer")

    print()
    if FAIL:
        print(f"FAILED ({len(FAIL)}):")
        for f in FAIL:
            print(f"  ✗  {f}")
        import sys; sys.exit(1)
    else:
        print("All assertions passed.")
