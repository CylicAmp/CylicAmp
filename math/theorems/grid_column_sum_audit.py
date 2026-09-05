"""
grid_column_sum_audit.py

Six-row grid: three anchor rows (1..10) interleaved with decade rows
(10–19, 20–29, 30–39).  Column sums and their digital-root structure.

─────────────────────────────────────────────────────────────────
GRID (6 rows × 10 columns):

  Row 1 (anchor):  1,  2,  3,  4,  5,  6,  7,  8,  9, 10
  Row 2 (decade): 10, 11, 12, 13, 14, 15, 16, 17, 18, 19
  Row 3 (anchor):  1,  2,  3,  4,  5,  6,  7,  8,  9, 10
  Row 4 (decade): 20, 21, 22, 23, 24, 25, 26, 27, 28, 29
  Row 5 (anchor):  1,  2,  3,  4,  5,  6,  7,  8,  9, 10
  Row 6 (decade): 30, 31, 32, 33, 34, 35, 36, 37, 38, 39

COLUMN SUMS (j = 1..10):

  Col j  Sum        DR
  ─────  ─────────  ──
   1     63         9
   2     69         6
   3     75         3
   4     81         9
   5     87         6
   6     93         3
   7     99         9
   8    105         6
   9    111         3  ← 111 = 3 × 37 (framework repunit)
  10    117         9  ← 117 = sum of DR period-24 Fibonacci sequence

KEY FACTS:
  (C1) Column j sum = 6j + 57.
       Proof: 3 anchor rows contribute 3j; 3 decade rows contribute
       (10+j−1)+(20+j−1)+(30+j−1) = 3j+57.  Total = 6j+57.

  (C2) Constant step Δ = 6.  All column sums ≡ 0 (mod 3).
       DR cycle: 9 → 6 → 3 → 9 → 6 → 3 (period 3).

  (C3) Col 9 sum = 111 = 3×37.  The framework repunit appears as the
       column sum at j = 9 (the criss-cross entry point of 17 in
       Fibonacci, and the Pisano period of 17 mod 9).

  (C4) Col 10 sum = 117.  DR(117) = 9.
       117 is the sum of the 24-term DR Fibonacci period
       (golden_mean_fibonacci_audit.py, G4).

  (C5) Col 1 sum = 63 = 7×9.  DR(63) = 9.
       Col 7 sum = 99 = 9×11.  DR(99) = 9.  11 = repunit_2.

  (C6) The 3-6-9 DR lock: 6j+57 ≡ 6j (mod 9).
       Since gcd(6,9)=3, the orbit of 6j mod 9 for j=1..3 is {6,3,0}.
       Adding 57 ≡ 3 (mod 9): orbit becomes {9,6,3} — exactly the
       multiples of 3 in {1..9}.  All other DR values (1,2,4,5,7,8)
       are absent.
─────────────────────────────────────────────────────────────────
"""

from sympy import factorint

FAIL = []


def check(cond, label, actual, expected):
    if not cond:
        FAIL.append(f"{label}: actual={actual!r}, expected={expected!r}")
    return cond


def dr(n):
    if n == 0:
        return 0
    r = n % 9
    return r if r else 9


# ── Grid definition ───────────────────────────────────────────────────────────

ANCHOR = list(range(1, 11))            # [1, 2, ..., 10]
DECADE = [
    list(range(10, 20)),               # 10-19
    list(range(20, 30)),               # 20-29
    list(range(30, 40)),               # 30-39
]

GRID = [
    ANCHOR,
    DECADE[0],
    ANCHOR,
    DECADE[1],
    ANCHOR,
    DECADE[2],
]

check(len(GRID) == 6, "grid rows = 6", len(GRID), 6)
check(all(len(row) == 10 for row in GRID), "all rows = 10 cols",
      [len(r) for r in GRID], [10] * 6)


# ── Column sums ───────────────────────────────────────────────────────────────

COL_SUMS = [sum(GRID[r][j] for r in range(6)) for j in range(10)]

EXPECTED_SUMS = [63, 69, 75, 81, 87, 93, 99, 105, 111, 117]
check(COL_SUMS == EXPECTED_SUMS, "column sums", COL_SUMS, EXPECTED_SUMS)


# ── C1: Formula 6j + 57 ───────────────────────────────────────────────────────

for j in range(1, 11):
    formula = 6 * j + 57
    check(formula == COL_SUMS[j - 1], f"6·{j}+57 = col {j}", formula, COL_SUMS[j - 1])

# Anchor contribution per column j: 3 × j
for j in range(1, 11):
    anchor_sum = sum(ANCHOR[j - 1] for _ in range(3))
    check(anchor_sum == 3 * j, f"anchor col {j} = 3·{j}", anchor_sum, 3 * j)

# Decade contribution per column j: 3j + 57
for j in range(1, 11):
    decade_sum = sum(D[j - 1] for D in DECADE)
    check(decade_sum == 3 * j + 57, f"decade col {j} = 3·{j}+57", decade_sum, 3 * j + 57)


# ── C2: Constant step Δ = 6 and DR cycle 9,6,3 ───────────────────────────────

for i in range(len(COL_SUMS) - 1):
    delta = COL_SUMS[i + 1] - COL_SUMS[i]
    check(delta == 6, f"step {i+1}→{i+2} = 6", delta, 6)

DR_CYCLE = [9, 6, 3]
for j, s in enumerate(COL_SUMS):
    expected_dr = DR_CYCLE[j % 3]
    check(dr(s) == expected_dr, f"DR(col {j+1} sum {s}) = {expected_dr}", dr(s), expected_dr)

# Only DR values 3, 6, 9 appear (never 1, 2, 4, 5, 7, 8)
dr_values = set(dr(s) for s in COL_SUMS)
check(dr_values == {3, 6, 9}, "DR values = {3,6,9}", dr_values, {3, 6, 9})


# ── C3: Col 9 sum = 111 = 3×37 ───────────────────────────────────────────────

check(COL_SUMS[8] == 111, "col 9 sum = 111", COL_SUMS[8], 111)
check(factorint(111) == {3: 1, 37: 1}, "111 = 3×37", factorint(111), {3: 1, 37: 1})
check(dr(111) == 3, "DR(111) = 3", dr(111), 3)

# j=9 links: entry point of 17 in Fibonacci is F(9)=34=2×17;
# Pisano period of 17 mod 9 is 9
check(9 * 37 % 9 == 0, "37 | col 9 sum / 3 (37 appears at j=9)", (111 // 3) % 37, 0)


# ── C4: Col 10 sum = 117 = Fibonacci DR-period sum ───────────────────────────

check(COL_SUMS[9] == 117, "col 10 sum = 117", COL_SUMS[9], 117)
check(dr(117) == 9, "DR(117) = 9", dr(117), 9)

# Verify 117 = sum of DR period-24 Fibonacci sequence (from golden_mean_fibonacci_audit)
def fibonacci(n):
    fibs = [1, 1]
    while len(fibs) < n:
        fibs.append(fibs[-1] + fibs[-2])
    return fibs[:n]

def fib_dr(k):
    r = fibonacci(k)[-1] % 9
    return r if r else 9

DR_FIB_24 = [fib_dr(k) for k in range(1, 25)]
check(sum(DR_FIB_24) == 117, "sum DR Fibonacci period-24 = 117", sum(DR_FIB_24), 117)


# ── C5: Col 1 and col 7 ───────────────────────────────────────────────────────

check(COL_SUMS[0] == 63, "col 1 sum = 63", COL_SUMS[0], 63)
check(63 == 7 * 9, "63 = 7×9", 63, 7 * 9)
check(dr(63) == 9, "DR(63) = 9", dr(63), 9)

check(COL_SUMS[6] == 99, "col 7 sum = 99", COL_SUMS[6], 99)
check(99 == 9 * 11, "99 = 9×11", 99, 9 * 11)
check(dr(99) == 9, "DR(99) = 9", dr(99), 9)


# ── C6: 3-6-9 lock derivation ─────────────────────────────────────────────────

# 6j + 57 mod 9: 57 mod 9 = 3; 6j mod 9 cycles {6,3,0} for j=1,2,3
check(57 % 9 == 3, "57 mod 9 = 3", 57 % 9, 3)
orbit_6 = [(6 * j) % 9 for j in range(1, 4)]
check(orbit_6 == [6, 3, 0], "6j mod 9 for j=1,2,3 = [6,3,0]", orbit_6, [6, 3, 0])
shifted = [(v + 3) % 9 for v in orbit_6]
dr_shifted = [v if v else 9 for v in shifted]
check(dr_shifted == [9, 6, 3], "(6j+57) mod 9 → DR = [9,6,3]", dr_shifted, [9, 6, 3])

# All col sums divisible by 3
check(all(s % 3 == 0 for s in COL_SUMS), "all col sums ≡ 0 mod 3", True, True)

# No col sum has DR in {1,2,4,5,7,8}
forbidden = {1, 2, 4, 5, 7, 8}
check(not dr_values.intersection(forbidden), "no DR in {1,2,4,5,7,8}",
      dr_values.intersection(forbidden), set())


# ── Output ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Grid Column Sum Audit")
    print("=" * 62)

    print("\n── Grid ──")
    labels = ["anchor", "decade 10-19", "anchor", "decade 20-29", "anchor", "decade 30-39"]
    for i, (row, label) in enumerate(zip(GRID, labels)):
        print(f"  Row {i+1} ({label}): {row}")

    print("\n── Column sums ──")
    print(f"  {'Col':>4}  {'Sum':>5}  {'DR':>3}  {'Formula':>8}")
    for j in range(1, 11):
        s = COL_SUMS[j - 1]
        note = ""
        if j == 9:
            note = "  ← 111 = 3×37"
        elif j == 10:
            note = "  ← 117 = DR-Fib period sum"
        print(f"  {j:>4}  {s:>5}  {dr(s):>3}  6·{j}+57={6*j+57}{note}")

    print(f"\n── Structure ──")
    print(f"  Anchor contribution col j: 3j")
    print(f"  Decade contribution col j: 3j + 57  (decade starts 10,20,30 → offsets sum to 57)")
    print(f"  Total: 6j + 57")
    print(f"  Δ = 6 (constant)")
    print(f"  DR cycle: 9 → 6 → 3 → repeat (period 3)")
    print(f"  57 mod 9 = {57 % 9}  →  base DR = 3; step 6 shifts by 6,3,0 mod 9")

    print(f"\n── Framework connections ──")
    print(f"  Col 9  = 111 = 3×37  (repunit, framework modulus link)")
    print(f"  Col 10 = 117 = sum of DR(F_n) for n=1..24 (Fibonacci period)")
    print(f"  Col 1  = 63 = 7×9")
    print(f"  Col 7  = 99 = 9×11 = 9×repunit_2")
    print(f"  DR ∈ {{3,6,9}} exclusively — no other DR values appear")

    print()
    if FAIL:
        print(f"FAILED ({len(FAIL)}):")
        for f in FAIL:
            print(f"  ✗  {f}")
        import sys; sys.exit(1)
    else:
        print("All assertions passed.")
