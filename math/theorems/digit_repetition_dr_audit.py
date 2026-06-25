"""
digit_repetition_dr_audit.py

Three charts for each digit k = 1..9:
  Chart 1: k       (one repetition)
  Chart 2: 11k     (two repetitions: kk)
  Chart 3: 111k    (three repetitions: kkk)

─────────────────────────────────────────────────────────────────
k  |  k    11k   111k  |  DR(k) DR(11k) DR(111k)
───┼────────────────────┼──────────────────────────
1  |  1     11    111  |  1      2       3
2  |  2     22    222  |  2      4       6
3  |  3     33    333  |  3      6       9
4  |  4     44    444  |  4      8       3
5  |  5     55    555  |  5      1       6
6  |  6     66    666  |  6      3       9
7  |  7     77    777  |  7      5       3
8  |  8     88    888  |  8      7       6
9  |  9     99    999  |  9      9       9

CLAIMS:
  (R1) DR(11k) = DR(2k)  for all k.     [11 ≡ 2 (mod 9)]
  (R2) DR(111k) = DR(3k) for all k.     [111 ≡ 3 (mod 9)]
  (R3) Each row is an arithmetic sequence in DR-space with step k:
         DR(k), DR(2k), DR(3k)  — step k (mod 9).
  (R4) k=9 is the fixed point: DR(9) = DR(99) = DR(999) = 9.
  (R5) k=1 gives the unit sequence 1,2,3; numbers are 1, 11, 111.
  (R6) 111 = 3×37 (framework modulus 37 appears in the unit triple).
  (R7) Sum of all 27 DR values = 144 = 12².  DR(144) = 9.
       (144 also appears in the descent sequence 191→100 as the row 1-4-4.)

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


DIGITS = list(range(1, 10))


# ── Three charts ──────────────────────────────────────────────────────────────

CHART = {k: (k, 11 * k, 111 * k) for k in DIGITS}

CHART_EXPECTED = {
    1: (1,    11,   111),
    2: (2,    22,   222),
    3: (3,    33,   333),
    4: (4,    44,   444),
    5: (5,    55,   555),
    6: (6,    66,   666),
    7: (7,    77,   777),
    8: (8,    88,   888),
    9: (9,    99,   999),
}

for k, expected in CHART_EXPECTED.items():
    check(CHART[k] == expected, f"chart({k})", CHART[k], expected)


# ── DR table ──────────────────────────────────────────────────────────────────

DR_TABLE = {k: (dr(k), dr(11*k), dr(111*k)) for k in DIGITS}

DR_EXPECTED = {
    1: (1, 2, 3),
    2: (2, 4, 6),
    3: (3, 6, 9),
    4: (4, 8, 3),
    5: (5, 1, 6),
    6: (6, 3, 9),
    7: (7, 5, 3),
    8: (8, 7, 6),
    9: (9, 9, 9),
}

for k, expected in DR_EXPECTED.items():
    check(DR_TABLE[k] == expected, f"DR_table({k})", DR_TABLE[k], expected)


# ── R1: DR(11k) = DR(2k) ──────────────────────────────────────────────────────

check(11 % 9 == 2, "11 ≡ 2 (mod 9)", 11 % 9, 2)
for k in DIGITS:
    check(dr(11 * k) == dr(2 * k), f"R1 k={k}", dr(11 * k), dr(2 * k))


# ── R2: DR(111k) = DR(3k) ─────────────────────────────────────────────────────

check(111 % 9 == 3, "111 ≡ 3 (mod 9)", 111 % 9, 3)
for k in DIGITS:
    check(dr(111 * k) == dr(3 * k), f"R2 k={k}", dr(111 * k), dr(3 * k))


# ── R3: arithmetic sequence in DR-space with step k ──────────────────────────

for k in DIGITS:
    d1, d2, d3 = DR_TABLE[k]
    step = (d2 - d1) % 9
    step2 = (d3 - d2) % 9
    check(step == k % 9, f"R3 step1 k={k}", step, k % 9)
    check(step2 == k % 9, f"R3 step2 k={k}", step2, k % 9)


# ── R4: k=9 fixed point ───────────────────────────────────────────────────────

check(DR_TABLE[9] == (9, 9, 9), "R4 k=9 fixed", DR_TABLE[9], (9, 9, 9))
check(dr(9 * 9) == 9, "DR(81)=9", dr(81), 9)
check(9 % 9 == 0, "9 ≡ 0 (mod 9) → step=0", 9 % 9, 0)


# ── R5: k=1 unit sequence ────────────────────────────────────────────────────

check(CHART[1] == (1, 11, 111), "R5 unit triple", CHART[1], (1, 11, 111))
check(DR_TABLE[1] == (1, 2, 3), "R5 unit DRs", DR_TABLE[1], (1, 2, 3))


# ── R6: 111 = 3×37 ────────────────────────────────────────────────────────────

check(factorint(111) == {3: 1, 37: 1}, "R6 111=3×37", factorint(111), {3: 1, 37: 1})
check(111 == 3 * 37, "R6 value", 111, 3 * 37)


# ── R7: sum of all 27 DR values = 135, DR(135) = 9 ──────────────────────────

all_dr_values = [v for k in DIGITS for v in DR_TABLE[k]]
check(len(all_dr_values) == 27, "27 DR values", len(all_dr_values), 27)
total = sum(all_dr_values)
check(total == 144, "R7 DR sum = 144", total, 144)
check(dr(144) == 9, "R7 DR(144)=9", dr(144), 9)
check(144 == 12 ** 2, "144=12²", 144, 144)


# ── Output ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Digit Repetition DR Audit: k / 11k / 111k for k=1..9")
    print("=" * 62)

    print(f"\n── Three charts ──")
    print(f"  {'k':>2}  {'k':>4}  {'11k':>4}  {'111k':>5}  DRs")
    for k in DIGITS:
        v1, v2, v3 = CHART[k]
        d1, d2, d3 = DR_TABLE[k]
        print(f"  {k:>2}  {v1:>4}  {v2:>4}  {v3:>5}  {d1},{d2},{d3}")

    print(f"\n── Modular basis ──")
    print(f"  11  ≡ 2 (mod 9)  →  DR(11k) = DR(2k)   for all k")
    print(f"  111 ≡ 3 (mod 9)  →  DR(111k) = DR(3k)  for all k")

    print(f"\n── R3: each row is arithmetic in DR-space ──")
    for k in DIGITS:
        d1, d2, d3 = DR_TABLE[k]
        step = k % 9
        print(f"  k={k}: DRs {d1},{d2},{d3}  step={step}")

    print(f"\n── Special cases ──")
    print(f"  k=1: 1, 11, 111  DRs 1,2,3  (unit sequence)")
    print(f"  k=9: 9, 99, 999  DRs 9,9,9  (fixed point; step=0)")
    print(f"  111 = 3×37  (framework modulus 37 in unit triple)")

    print(f"\n── R7: DR sum ──")
    print(f"  Sum of all 27 DR values = {total} = 12²")
    print(f"  DR({total}) = {dr(total)}")
    print(f"  (144 also appears in the 191→100 descent as row 1-4-4)")

    print()
    if FAIL:
        print(f"FAILED ({len(FAIL)}):")
        for f in FAIL:
            print(f"  ✗  {f}")
        import sys; sys.exit(1)
    else:
        print("All assertions passed.")
