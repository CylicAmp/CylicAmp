"""
doubling_mirror_audit.py

Doubling-mirror engine: L(n) = 101112 × 2^n; R(n) = reverse(L(n)).

─────────────────────────────────────────────────────────────────
TWO SEEDINGS IN THE USER'S CODE:

  rows_data  : row 7 uses L = 101112, then doubles.  row k → L = 101112 × 2^(k-7).
  while_loop : doubles FIRST;         row k → L = 101112 × 2^(k-6).

  The two seedings are offset by exactly one doubling (one row).
  The user cited rows 29–31 from while_loop and rows 34–35 from rows_data.
  All arithmetic is correct; row labels are off by 1 between the two codes.

─────────────────────────────────────────────────────────────────
CONSISTENT NUMBERING (rows_data, row 7 = 101112):

  L(k) = 101112 × 2^(k-7)

  The user's "row 29" data (L=848188932096) is rows_data row 30.
  The user's "row 34" collapse is rows_data row 34 (correct).
  The user's "row 35" collapse is rows_data row 35 (correct).

─────────────────────────────────────────────────────────────────
THE COLLAPSE EVENT:

  Row 34 (14 digits): 13,571,022,913,536 − 63,531,922,017,531 = −49,960,899,103,995
  Row 35 (14 digits): 27,142,045,827,072 − 27,072,854,024,172 =         +69,191,802,900

  Difference magnitude drops by factor ≈ 722×:  49.96T → 69.19B.
  Both still have DR = 9.

  Mechanism: 27,142,045,827,072 starts with "2714..." and its reverse starts with
  "2707..." — the leading digits almost agree, causing massive high-order cancellation.
  This is a Diophantine coincidence of 101112 × 2^28, not a universal geometric law.

─────────────────────────────────────────────────────────────────
COLLAPSE RECURRENCE: local minima of |L−R|

  Row  10: |diff| =         110,088   (6  digits)
  Row  15: |diff| =       1,764,180   (8  digits)
  Row  19: |diff| =     156,703,338   (9  digits)
  Row  22: |diff| =   2,795,085,117   (10 digits)
  Row  26: |diff| =  12,269,002,779   (11 digits)
  Row  30: |diff| = 157,949,050,248   (12 digits)   ← user's "row 29" (while_loop)
  Row  35: |diff| =  69,191,802,900   (14 digits)   ← the main collapse event
  Row  39: |diff| = 182,940,395,960,718   (15 digits)
  ...
  These are NOT at digit-length boundaries. They are arithmetic coincidences —
  points where L(n) happens to look nearly palindromic.

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


def mirror_diff(n):
    s = str(n)
    return n - int(s[::-1])


SEED = 101112

# ── Seeding verification ──────────────────────────────────────────────────────

# rows_data: L(k) = SEED × 2^(k-7)
def L_rd(k):
    return SEED * (2 ** (k - 7))

# while_loop: L(k) = SEED × 2^(k-6)
def L_wl(k):
    return SEED * (2 ** (k - 6))

# User's cited values and which seeding matches
check(L_wl(29) == 848188932096,   "while_loop row 29 = 848188932096",   L_wl(29),  848188932096)
check(L_wl(30) == 1696377864192,  "while_loop row 30 = 1696377864192",  L_wl(30), 1696377864192)
check(L_wl(31) == 3392755728384,  "while_loop row 31 = 3392755728384",  L_wl(31), 3392755728384)

check(L_rd(34) == 13571022913536, "rows_data row 34 = 13571022913536",  L_rd(34), 13571022913536)
check(L_rd(35) == 27142045827072, "rows_data row 35 = 27142045827072",  L_rd(35), 27142045827072)

# Offset: while_loop row k = rows_data row k+1
for k in range(7, 40):
    check(L_wl(k) == L_rd(k + 1),
          f"while_loop row {k} = rows_data row {k+1}",
          L_wl(k), L_rd(k + 1))


# ── Generation 1 (rows 1–6, base engine) ────────────────────────────────────

BASE_ROWS = [
    (101112, 211101, -109989),
    (202224, 422202, -219978),
    (404448, 844404, -439956),
    (808887, 788808,  20079),
    (707775, 577707, 130068),
    (505551, 155505, 350046),
]

for i, (L, R, expected_diff) in enumerate(BASE_ROWS):
    check(L - R == expected_diff, f"gen1 row {i+1}: {L}−{R}", L - R, expected_diff)
    check(dr(expected_diff) == 9, f"gen1 row {i+1}: DR=9", dr(expected_diff), 9)
    check(str(L) == str(R)[::-1], f"gen1 row {i+1}: R=reverse(L)", str(R)[::-1], str(L))


# ── DR=9 lock — universal proof ───────────────────────────────────────────────

# n ≡ reverse(n) mod 9 → n − reverse(n) ≡ 0 mod 9 → DR(|n−reverse(n)|) = 9
# Verify for all rows up to row 49 (rows_data)
current = SEED
for k in range(7, 50):
    diff = mirror_diff(current)
    if diff != 0:
        check(diff % 9 == 0,
              f"rows_data row {k}: (L−R) divisible by 9", diff % 9, 0)
        check(dr(diff) == 9,
              f"rows_data row {k}: DR(|L−R|) = 9", dr(diff), 9)
    current *= 2


# ── Specific cited rows (while_loop seeding) ──────────────────────────────────

WL_CLAIMS = [
    (29, 848188932096,  690239881848,  157949050248),
    (30, 1696377864192, 2914687736961, -1218309872769),
    (31, 3392755728384, 4838275572933, -1445519844549),
]

for row, L, R, diff_expected in WL_CLAIMS:
    check(str(L) == str(R)[::-1], f"wl row {row}: R=reverse(L)", str(R)[::-1], str(L))
    check(L - R == diff_expected, f"wl row {row}: diff", L - R, diff_expected)
    check(dr(diff_expected) == 9, f"wl row {row}: DR=9", dr(diff_expected), 9)
    check(len(str(L)) >= 12, f"wl row {row}: ≥12 digits", len(str(L)), len(str(L)))

check(len(str(848188932096)) == 12, "wl row 29: 12 digits (last 12-digit)",
      len(str(848188932096)), 12)
check(len(str(1696377864192)) == 13, "wl row 30: 13 digits (first 13-digit)",
      len(str(1696377864192)), 13)


# ── Collapse event (rows_data row 34/35) ─────────────────────────────────────

L34 = 13571022913536
R34 = 63531922017531
D34 = -49960899103995

L35 = 27142045827072
R35 = 27072854024172
D35 = 69191802900

check(str(L34) == str(R34)[::-1], "row 34: R = reverse(L)", str(R34)[::-1], str(L34))
check(str(L35) == str(R35)[::-1], "row 35: R = reverse(L)", str(R35)[::-1], str(L35))
check(L34 - R34 == D34, "row 34: diff = −49,960,899,103,995", L34 - R34, D34)
check(L35 - R35 == D35, "row 35: diff = +69,191,802,900",     L35 - R35, D35)
check(dr(D34) == 9, "row 34: DR=9", dr(D34), 9)
check(dr(D35) == 9, "row 35: DR=9", dr(D35), 9)
check(len(str(L34)) == 14 and len(str(L35)) == 14, "rows 34,35: 14 digits each", True, True)

# Verify L35 = 2 × L34
check(L35 == 2 * L34, "L35 = 2×L34", L35, 2 * L34)

# Collapse ratio: how much smaller is |D35| vs |D34|?
collapse_ratio = abs(D34) / abs(D35)
check(collapse_ratio > 700, f"collapse ratio |D34|/|D35| ≈ {collapse_ratio:.0f} > 700",
      collapse_ratio > 700, True)

# Mechanism: leading digits of L35 nearly equal leading digits of R35
L35_lead = str(L35)[:5]   # "27142"
R35_lead = str(R35)[:5]   # "27072"
check(L35_lead[:2] == R35_lead[:2],
      "L35 and R35 share same 2 leading digits", L35_lead[:2], R35_lead[:2])
lead_diff = int(L35_lead) - int(R35_lead)
check(lead_diff == 70,
      "leading 5-digit blocks: 27142 − 27072 = 70", lead_diff, 70)


# ── Digit-root check on user's digit sums ────────────────────────────────────

# Row 34: 4+9+9+6+0+8+9+9+1+0+3+9+9+5 = 81 → 9
check(sum(int(d) for d in str(abs(D34))) == 81,
      "digit_sum(49960899103995) = 81", sum(int(d) for d in str(abs(D34))), 81)
check(dr(81) == 9, "DR(81) = 9", dr(81), 9)

# Row 35: 6+9+1+9+1+8+0+2+9+0+0 = 45 → 9
check(sum(int(d) for d in str(abs(D35))) == 45,
      "digit_sum(69191802900) = 45", sum(int(d) for d in str(abs(D35))), 45)
check(dr(45) == 9, "DR(45) = 9", dr(45), 9)


# ── Local minima (collapse recurrence) ───────────────────────────────────────

current = SEED
rows = []
for k in range(7, 50):
    diff = mirror_diff(current)
    rows.append((k, current, abs(diff), len(str(current))))
    current *= 2

EXPECTED_MINIMA = [10, 15, 19, 22, 26, 30, 35, 39, 42, 46]

actual_minima = []
for i in range(1, len(rows) - 1):
    k, L, ad, nd = rows[i]
    if ad < rows[i-1][2] and ad < rows[i+1][2]:
        actual_minima.append(k)

check(actual_minima == EXPECTED_MINIMA,
      "local minima rows match expected", actual_minima, EXPECTED_MINIMA)

# Row 35 is a local minimum
check(35 in actual_minima, "row 35 is a local minimum of |L−R|", 35 in actual_minima, True)

# Minima are NOT exclusively at digit-length transitions
digit_transitions = []
prev_len = len(str(SEED))
current = SEED
for k in range(7, 50):
    current *= 2
    curr_len = len(str(current))
    if curr_len > prev_len:
        digit_transitions.append(k)
    prev_len = curr_len

# Check that minima and transitions are different sets
overlap = set(actual_minima) & set(digit_transitions)
check(len(overlap) < len(actual_minima),
      "not all minima coincide with digit-length transitions",
      len(overlap) < len(actual_minima), True)


# ── Output ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Doubling Mirror Audit")
    print("=" * 66)

    print(f"\n── Seeding note ──")
    print(f"  User's rows 29–31 come from while_loop (row 7 = 202224 = 101112×2).")
    print(f"  User's rows 34–35 come from rows_data (row 7 = 101112).")
    print(f"  while_loop row k  =  rows_data row k+1  (offset by 1).")
    print(f"  All arithmetic is correct; only the row labels differ.")

    print(f"\n── Generation 1 (base engine) ──")
    for i, (L, R, d) in enumerate(BASE_ROWS):
        print(f"  Row {i+1}: {L} − {R} = {d:+}  DR={dr(d)}")

    print(f"\n── While-loop rows 29–31 (user's cited values) ──")
    for row, L, R, diff in WL_CLAIMS:
        print(f"  Row {row} ({len(str(L))}d): {L} − {R} = {diff:+}  DR={dr(diff)}")
    print(f"  These are rows_data rows 30–32 (same arithmetic, one label higher).")

    print(f"\n── Collapse event (rows_data rows 34–35) ──")
    print(f"  Row 34 ({len(str(L34))}d): {L34} − {R34} = {D34:+}")
    print(f"  Row 35 ({len(str(L35))}d): {L35} − {R35} = {D35:+}")
    print(f"  Magnitude ratio: {collapse_ratio:.0f}× collapse (49.96T → 69.19B)")
    print(f"  DR: row 34 = {dr(D34)}, row 35 = {dr(D35)}")
    print(f"\n  Mechanism: L35 = 27 142 045 827 072")
    print(f"             R35 = 27 072 854 024 172")
    print(f"  First 5 digits: L35={L35_lead}, R35={R35_lead}, gap={lead_diff}")
    print(f"  The leading blocks nearly agree → high-order cancellation.")
    print(f"  This is a Diophantine coincidence of 101112×2^28, not a universal law.")

    print(f"\n── Collapse recurrence (local minima of |L−R|, rows_data) ──")
    for k, L, ad, nd in [(r[0],r[1],r[2],r[3]) for r in rows if r[0] in actual_minima]:
        print(f"  Row {k:2} ({nd}d): |diff| = {ad:,}")
    print(f"  Digit-length transitions occur at rows: {digit_transitions[:8]}...")
    print(f"  Overlap with minima: {sorted(set(actual_minima) & set(digit_transitions))}")
    print(f"  → Collapses are NOT tied to digit-length boundaries.")

    print(f"\n── DR=9 lock ──")
    print(f"  For any n: n ≡ reverse(n) mod 9  (same digits → same digit sum → same residue)")
    print(f"  ∴ n − reverse(n) ≡ 0 mod 9 → DR(|n−reverse(n)|) = 9 always.")
    print(f"  Verified for all rows 7–49. No exceptions.")

    print()
    if FAIL:
        print(f"FAILED ({len(FAIL)}):")
        for f in FAIL:
            print(f"  ✗  {f}")
        import sys; sys.exit(1)
    else:
        print("All assertions passed.")
