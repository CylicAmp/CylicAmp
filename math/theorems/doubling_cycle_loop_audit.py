"""
doubling_cycle_loop_audit.py

Seven-row loop: the complete DR doubling cycle as mirrored subtractions,
closing back to row 1 on row 7.

─────────────────────────────────────────────────────────────────
MATRIX (L / R   →   L − R):

  Row  d   Left     Right     L − R
   1   1   101112 − 211101 = −109,989
   2   2   202224 − 422202 = −219,978
   3   4   404448 − 844404 = −439,956
   4   8   808887 − 788808 =  +20,079
   5   7   707775 − 577707 = +130,068
   6   5   505551 − 155505 = +350,046
   7   1   101112 − 211101 = −109,989  ← loop closure (= row 1)

STRUCTURE:
  Each left string has the form [d, 0, d, d, d, DR(2d)].
  Right string = exact reversal of left string.
  d runs through the full DR doubling cycle: 1→2→4→8→7→5→(1…)

KEY FACTS:
  (L1) Mirror-subtraction theorem: DR(|L − R|) = 9 for all rows.
       Any number and its digit-reversal share the same digit sum,
       so their difference is divisible by 9; DR = 9 when nonzero.

  (L2) Rows 1→2→3 form an exact doubling chain:
         L₂ = 2·L₁,  R₂ = 2·R₁  →  diff₂ = 2·diff₁
         L₃ = 2·L₂,  R₃ = 2·R₂  →  diff₃ = 2·diff₂
       The differences −109,989 → −219,978 → −439,956 double exactly.
       This breaks at row 4 because DR(2d) is non-linear at the cycle bend.

  (L3) Sign split: rows 1–3 give negative differences (right > left),
       rows 4–6 give positive differences (left > right).

  (L4) Sum of negatives = −769,923   DR = 9   mod 37 = 27
       Sum of positives = +500,193   DR = 9   mod 37 = 27
       Net              = −269,730   DR = 9   mod 37 =  0

  (L5) |Net| = 269,730 = 9³ × 10 × 37.
       The framework modulus 37 and the nine-principle meet in the net.
       27 = 3³ appears in both subtotals mod 37;
       27 = −10 mod 37, and 10 = 26⁻¹ mod 37 (modular ratio from
       division_582739_937285_audit.py, D3).

  (L6) Row 7 = Row 1: the cycle closes.  The 6-step period
       1→2→4→8→7→5→1 maps d back to 1, and the matrix loops.
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


def digit_sum(s):
    return sum(int(c) for c in s)


# ── Matrix definition ─────────────────────────────────────────────────────────

LEFT  = ["101112", "202224", "404448", "808887", "707775", "505551"]
RIGHT = ["211101", "422202", "844404", "788808", "577707", "155505"]
D_STEPS = [1, 2, 4, 8, 7, 5]

DIFFS = [int(L) - int(R) for L, R in zip(LEFT, RIGHT)]
EXPECTED_DIFFS = [-109989, -219978, -439956, 20079, 130068, 350046]

check(DIFFS == EXPECTED_DIFFS, "subtraction differences", DIFFS, EXPECTED_DIFFS)


# ── L1: Mirror-subtraction theorem — every |diff| has DR = 9 ─────────────────

for i, d in enumerate(DIFFS):
    check(dr(d) == 9, f"row {i+1} DR(|{d}|) = 9", dr(d), 9)

# Proof structure: L and R have the same digit sum → diff ≡ 0 (mod 9) and ≠ 0
for i, (L, R) in enumerate(zip(LEFT, RIGHT)):
    check(digit_sum(L) == digit_sum(R), f"row {i+1} digit sums equal",
          digit_sum(L), digit_sum(R))


# ── L2: Exact doubling chain for rows 1–3 ─────────────────────────────────────

check(DIFFS[1] == 2 * DIFFS[0], "diff2 = 2 × diff1", DIFFS[1], 2 * DIFFS[0])
check(DIFFS[2] == 2 * DIFFS[1], "diff3 = 2 × diff2", DIFFS[2], 2 * DIFFS[1])

# Source: left and right strings both double exactly for d=1,2,4
check(int(LEFT[1]) == 2 * int(LEFT[0]), "L2 = 2·L1", int(LEFT[1]), 2 * int(LEFT[0]))
check(int(RIGHT[1]) == 2 * int(RIGHT[0]), "R2 = 2·R1", int(RIGHT[1]), 2 * int(RIGHT[0]))
check(int(LEFT[2]) == 2 * int(LEFT[1]), "L3 = 2·L2", int(LEFT[2]), 2 * int(LEFT[1]))
check(int(RIGHT[2]) == 2 * int(RIGHT[1]), "R3 = 2·R2", int(RIGHT[2]), 2 * int(RIGHT[1]))

# Chain breaks at row 4: DR(2×8) = DR(16) = 7, not 8×2=16 mod 10
check(int(LEFT[3]) != 2 * int(LEFT[2]), "L4 ≠ 2·L3 (cycle bends here)",
      int(LEFT[3]) == 2 * int(LEFT[2]), False)


# ── L3: Sign split ────────────────────────────────────────────────────────────

NEGATIVES = [d for d in DIFFS if d < 0]
POSITIVES = [d for d in DIFFS if d > 0]

check(NEGATIVES == [-109989, -219978, -439956], "negative diffs (rows 1-3)",
      NEGATIVES, [-109989, -219978, -439956])
check(POSITIVES == [20079, 130068, 350046], "positive diffs (rows 4-6)",
      POSITIVES, [20079, 130068, 350046])


# ── L4: Sums and net ──────────────────────────────────────────────────────────

NEG_SUM = sum(NEGATIVES)
POS_SUM = sum(POSITIVES)
NET = NEG_SUM + POS_SUM

check(NEG_SUM == -769923, "sum of negatives = -769923", NEG_SUM, -769923)
check(POS_SUM == 500193,  "sum of positives = 500193",  POS_SUM, 500193)
check(NET == -269730,     "net = -269730",               NET,     -269730)

check(dr(NEG_SUM) == 9, "DR(|neg sum|) = 9", dr(NEG_SUM), 9)
check(dr(POS_SUM) == 9, "DR(pos sum) = 9",   dr(POS_SUM), 9)
check(dr(NET) == 9,     "DR(|net|) = 9",     dr(NET),     9)

# Both subtotals ≡ 27 mod 37
check(abs(NEG_SUM) % 37 == 27, "|neg sum| mod 37 = 27", abs(NEG_SUM) % 37, 27)
check(POS_SUM % 37 == 27,      "pos sum mod 37 = 27",    POS_SUM % 37,     27)
check(abs(NET) % 37 == 0,      "|net| mod 37 = 0",       abs(NET) % 37,    0)

# 27 = 3^3 and 27 ≡ −10 mod 37; 10 = 26^{-1} mod 37
check(27 == 3 ** 3, "27 = 3³", 27, 3 ** 3)
check((27 + 10) % 37 == 0, "27 ≡ −10 mod 37", (27 + 10) % 37, 0)
check(26 * 10 % 37 == 1, "10 = 26⁻¹ mod 37", 26 * 10 % 37, 1)


# ── L5: |Net| = 9³ × 10 × 37 ─────────────────────────────────────────────────

check(abs(NET) == 9 ** 3 * 10 * 37, "|net| = 9³×10×37",
      abs(NET), 9 ** 3 * 10 * 37)
check(9 ** 3 == 729, "9³ = 729", 9 ** 3, 729)
check(729 * 10 == 7290, "729×10 = 7290", 729 * 10, 7290)
check(7290 * 37 == 269730, "7290×37 = 269730", 7290 * 37, 269730)

# 37 is the framework modulus; 9 is the DR base
check(abs(NET) % 37 == 0, "37 | |net|", abs(NET) % 37, 0)
check(abs(NET) % 9 == 0,  "9  | |net|", abs(NET) % 9,  0)


# ── L6: Loop closure — row 7 = row 1 ─────────────────────────────────────────

# Row 7 data (same as row 1)
L7, R7 = "101112", "211101"
check(L7 == LEFT[0],  "row 7 left = row 1 left",  L7,  LEFT[0])
check(R7 == RIGHT[0], "row 7 right = row 1 right", R7, RIGHT[0])
check(int(L7) - int(R7) == DIFFS[0], "row 7 diff = row 1 diff",
      int(L7) - int(R7), DIFFS[0])

# DR doubling cycle period = 6; d returns to 1 after 6 steps
DR_CYCLE = [1, 2, 4, 8, 7, 5]
check(D_STEPS == DR_CYCLE, "6 rows cover full DR doubling cycle",
      D_STEPS, DR_CYCLE)
# Next step after 5 in the cycle: DR(2×5) = DR(10) = 1 → back to start
check(dr(2 * 5) == 1, "DR(2×5) = DR(10) = 1 (cycle returns to 1)", dr(2 * 5), 1)


# ── Output ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Doubling Cycle Loop Audit")
    print("=" * 62)

    print("\n── Matrix and subtractions ──")
    print(f"  {'Row':>3}  {'d':>2}  {'Left':>8}  {'Right':>8}  {'L − R':>10}  {'DR':>3}")
    for i, (L, R, d, diff) in enumerate(zip(LEFT, RIGHT, D_STEPS, DIFFS)):
        print(f"  {i+1:>3}  {d:>2}  {L:>8} − {R:>8} = {diff:>10}    {dr(diff)}")
    print(f"    7   1  {LEFT[0]:>8} − {RIGHT[0]:>8} = {DIFFS[0]:>10}    {dr(DIFFS[0])}  ← loop closure")

    print(f"\n── L1: Mirror-subtraction theorem ──")
    print(f"  L and R share digit sum → L−R ≡ 0 (mod 9) → DR(|L−R|) = 9")
    for i, (L, R) in enumerate(zip(LEFT, RIGHT)):
        print(f"  Row {i+1}: digit_sum({L}) = digit_sum({R}) = {digit_sum(L)}")

    print(f"\n── L2: Doubling chain (rows 1–3) ──")
    print(f"  diff1 = {DIFFS[0]}")
    print(f"  diff2 = {DIFFS[1]} = 2 × {DIFFS[0]}")
    print(f"  diff3 = {DIFFS[2]} = 2 × {DIFFS[1]}")
    print(f"  (chain breaks at row 4: DR cycles non-linearly at d=8→7)")

    print(f"\n── L3: Sign split ──")
    print(f"  Rows 1–3 (right > left): {NEGATIVES}")
    print(f"  Rows 4–6 (left > right): {POSITIVES}")

    print(f"\n── L4: Sums ──")
    print(f"  Sum of negatives: {NEG_SUM}   DR={dr(NEG_SUM)}   mod 37 = {abs(NEG_SUM)%37}")
    print(f"  Sum of positives: {POS_SUM}    DR={dr(POS_SUM)}   mod 37 = {POS_SUM%37}")
    print(f"  Net:             {NET}   DR={dr(NET)}   mod 37 = {abs(NET)%37}")
    print(f"  27 = 3³ = −10 mod 37;  10 = 26⁻¹ mod 37 (modular ratio of slot 26)")

    print(f"\n── L5: |Net| = 9³ × 10 × 37 ──")
    print(f"  |{NET}| = 9³ × 10 × 37 = 729 × 370 = {9**3 * 10 * 37}")
    print(f"  37: framework modulus (Z/37Z)")
    print(f"  9³: the nine-principle cubed")
    print(f"  10: 26⁻¹ mod 37 = modular ratio from division_582739_937285_audit")

    print(f"\n── L6: Loop closure ──")
    print(f"  DR doubling cycle: 1→2→4→8→7→5→1  (period 6)")
    print(f"  DR(2×5) = DR(10) = 1: cycle returns")
    print(f"  Row 7 identical to row 1: matrix closes its own loop")

    print()
    if FAIL:
        print(f"FAILED ({len(FAIL)}):")
        for f in FAIL:
            print(f"  ✗  {f}")
        import sys; sys.exit(1)
    else:
        print("All assertions passed.")
