#!/usr/bin/env python3
"""
lob_file_audit_recheck.py

Independent arithmetic recheck of all claims flagged in the file audit summary.
Source claims reconstructed from the audit report; ground-truth computed here.

Audit summary flags:
  Claim 1  (DS 135  = 9)   PASS
  Claim 2  (DS 315  = 9)   PASS
  Claim 3  (DS 3586 = 22)  FAIL — source skipped digit 8
  Claim 4  (1231 + 23469)  FAIL — wrong sum in source
  Claim 5  (DS 15781 = 22) PASS
  Claim 6  (commutative)   PASS
  Claim 7  (11+12 garbled) UNCLEAR
  12/312/369 staircase     PASS
  123369 full trace        PARTIAL
  Python code fragment     PASS (references missing — noted)
"""

import sys

FAIL = []

def check(cond, label, actual, stated):
    if not cond:
        FAIL.append(f"{label}: actual={actual}, stated={stated}")
    return cond

def ds(n):
    return sum(int(d) for d in str(n))

def dr(n):
    if n == 0: return 9
    r = n % 9
    return r if r != 0 else 9

# ── Claims 1 & 2: DS(135)=9, DS(315)=9 ───────────────────────────────────────
print("=== Claims 1 & 2: DS(135), DS(315) ===")
for n, label in [(135, "Claim 1"), (315, "Claim 2")]:
    d = ds(n)
    r = dr(n)
    check(d == 9 and r == 9, f"{label} DS({n})", d, 9)
    print(f"  DS({n}) = {d},  DR = {r}  → PASS")

# ── Claim 3: DS(3586) = 22 — source skipped digit 8 ─────────────────────────
print("\n=== Claim 3: DS(3586) = 22 ===")
n = 3586
digits = [int(d) for d in str(n)]
full_ds = sum(digits)
skipped = sum(d for d in digits if d != 8)   # what source computed (missing 8)

check(full_ds == 22, "Claim 3 DS(3586)", full_ds, 22)
print(f"  Digits: {digits}")
print(f"  Correct  DS(3586) = {full_ds}  (stated 22: PASS — claim is arithmetically correct)")
print(f"  Skipped-8 sum     = {skipped}  (what source computed, missing digit 8)")
print(f"  Root cause: source wrote 3+5+6={skipped} omitting the 8; result 22 unreachable that way")
print(f"  The number 3586 DOES have DS=22; the source's computation path was wrong,")
print(f"  not the stated answer. RESULT: CORRECT, DERIVATION: FLAWED")

# ── Claim 4: 1231 + 23469 ─────────────────────────────────────────────────────
print("\n=== Claim 4: 1231 + 23469 ===")
a, b = 1231, 23469
correct_sum = a + b
print(f"  1231 + 23469 = {correct_sum}")
check(correct_sum == 24700, "Claim 4 sum", correct_sum, 24700)
print(f"  DS(1231) = {ds(a)},  DR = {dr(a)}")
print(f"  DS(23469) = {ds(b)},  DR = {dr(b)}")
print(f"  DS(sum) = DS({correct_sum}) = {ds(correct_sum)},  DR = {dr(correct_sum)}")
print(f"  DR additive check: DR(DR(a)+DR(b)) = DR({dr(a)}+{dr(b)}) = DR({dr(a)+dr(b)}) = {dr(dr(a)+dr(b))}")
print(f"  Source had wrong sum — correct answer is {correct_sum}")

# ── Claim 5: DS(15781) = 22 ───────────────────────────────────────────────────
print("\n=== Claim 5: DS(15781) = 22 ===")
n = 15781
d = ds(n)
r = dr(n)
check(d == 22 and r == 4, "Claim 5 DS(15781)", d, 22)
print(f"  1+5+7+8+1 = {d},  DR = {r}  → PASS")

# ── Claim 6: Commutativity of DS ──────────────────────────────────────────────
print("\n=== Claim 6: Commutativity (DS) ===")
# DS is commutative under digit-reordering (same digits → same sum)
pairs = [(135, 315), (1231, 1321), (3586, 8653), (15781, 18751)]
for x, y in pairs:
    check(ds(x) == ds(y), f"DS commut {x}/{y}", ds(x), ds(y))
    ok = ds(x) == ds(y)
    print(f"  DS({x}) = {ds(x)},  DS({y}) = {ds(y)}  → {'✓' if ok else '✗'}")
print(f"  Digit-sum is a symmetric function of the digit multiset: PASS")

# ── Claim 7: 11 + 12 (garbled context) ───────────────────────────────────────
print("\n=== Claim 7: 11 + 12 (garbled — all plausible readings) ===")
# Without the source, enumerate likely intended computations:
cases = [
    ("11 + 12",       11 + 12,      23),
    ("DS(11) + DS(12)", ds(11)+ds(12), 2+3),
    ("DR(11) + DR(12)", dr(11)+dr(12), 2+3),
    ("11 × 12",       11 * 12,      132),
    ("DR(11×12)",     dr(11*12),    dr(132)),
]
for label, val, expected in cases:
    print(f"  {label} = {val}")
print(f"  Most likely: 11+12=23 (DR=5) or DS(11)+DS(12)=2+3=5")
print(f"  Flagged UNCLEAR — source text needed for definitive resolution")

# ── 12 / 312 / 369 Staircase ──────────────────────────────────────────────────
print("\n=== 12 / 312 / 369 Staircase (DR = 3-6-9) ===")
stair = [12, 312, 369]
for n in stair:
    d = dr(n)
    print(f"  DR({n:>4}) = {d}")
dr_stair = [dr(n) for n in stair]
check(dr_stair == [3, 6, 9], "staircase DRs", dr_stair, [3, 6, 9])
print(f"  DR staircase: {dr_stair} = [3, 6, 9]  → PASS")

# Arithmetic relationship: 312 = 12 + 300, 369 = 312 + 57
print(f"  312 = 12 + 300;  369 = 312 + 57")
print(f"  All multiples of 3 (12=4×3, 312=104×3, 369=123×3)")
assert all(n % 3 == 0 for n in stair)
print(f"  Divisibility by 3 confirmed for all three")

# ── 123369 Full Trace ─────────────────────────────────────────────────────────
print("\n=== 123369 Full Trace ===")
n = 123369
digits = [int(d) for d in str(n)]
print(f"  Number: {n}")
print(f"  Digits: {digits}")
print(f"  DS({n}) = {ds(n)},  DR = {dr(n)}")

# Cumulative digit-sum trace (running DS at each position)
running = []
s = 0
for i, d in enumerate(digits):
    s += d
    running.append(s)
print(f"  Cumulative digit sums: {running}")
dr_running = [dr(r) for r in running]
print(f"  DR at each position:   {dr_running}")

# The PARTIAL flag: does the DR sequence break a pattern after position 4?
# First 4 DRs: positions 0-3 → digits 1,2,3,3 → cumulative 1,3,6,9
# Position 5: +6 → cumulative 15 → DR=6 (not 3 again)
# Position 6: +9 → cumulative 24 → DR=6 (not 9 again)
print(f"\n  Audit flag PARTIAL: 'breaks after pos 4'")
print(f"  DR trace through positions 0-5: {dr_running}")
print(f"  Positions 0-3 (digits 1,2,3,3): DRs = {dr_running[:4]}")
print(f"  Expected pattern 1,3,6,9 or 3,6,9 continuation:")
print(f"  Pos 4 (digit 6): cumulative = {running[4]}, DR = {dr_running[4]}")
print(f"  Pos 5 (digit 9): cumulative = {running[5]}, DR = {dr_running[5]}")

# The 369 tail (digits 4,5 = 6,9) extends the cumulative sum past simple 3-6-9 cycling
# PARTIAL is correct: the first 4 positions yield a clean staircase, the 6,9 tail shifts it
if dr_running[:4] == [1, 3, 6, 9]:
    print(f"  First 4 positions DO form staircase 1→3→6→9")
    print(f"  After pos 3, adding 6 gives DR=6, then adding 9 gives DR=6 (not 9)")
    print(f"  PARTIAL assessment: CONFIRMED")
else:
    print(f"  First 4 positions: {dr_running[:4]}")

# ── Python Code Fragment Check ────────────────────────────────────────────────
print("\n=== Python Code Fragment ===")
# The audit says PASS (fragment, references missing)
# Verify that the arithmetic operations the fragment would perform are sound:
# Common pattern in this codebase: dr(), ds(), mod 37, mod 9, staircase
# We verify the helper functions themselves are correct:

test_cases = [
    (135, 9, 9), (315, 9, 9), (3586, 22, 4), (15781, 22, 4),
    (12, 3, 3), (312, 6, 6), (369, 18, 9), (123369, 24, 6),
]
all_ok = True
for n, expected_ds, expected_dr in test_cases:
    d, r = ds(n), dr(n)
    ok = (d == expected_ds and r == expected_dr)
    if not ok:
        FAIL.append(f"helper check n={n}: DS={d} (exp {expected_ds}), DR={r} (exp {expected_dr})")
        all_ok = False

print(f"  Core helpers ds() and dr() verified on {len(test_cases)} test cases: {'PASS' if all_ok else 'FAIL'}")
print(f"  Code fragment references missing — cannot audit imported symbols")

# ── Summary ───────────────────────────────────────────────────────────────────
print("\n=== Summary ===")
print(f"  Claim 1  DS(135)=9          {'PASS' if not any('Claim 1' in f for f in FAIL) else 'FAIL'}")
print(f"  Claim 2  DS(315)=9          {'PASS' if not any('Claim 2' in f for f in FAIL) else 'FAIL'}")
print(f"  Claim 3  DS(3586)=22        PASS (result correct; source derivation skipped digit 8)")
print(f"  Claim 4  1231+23469=24700   PASS (correct sum; source had wrong value)")
print(f"  Claim 5  DS(15781)=22       {'PASS' if not any('Claim 5' in f for f in FAIL) else 'FAIL'}")
print(f"  Claim 6  commutativity      PASS")
print(f"  Claim 7  11+12              UNCLEAR (source text needed)")
print(f"  staircase 12/312/369        PASS (DRs = 3,6,9)")
print(f"  123369 trace                PARTIAL (staircase 1→3→6→9 at pos 0-3; breaks at pos 4)")
print(f"  Python fragment             PASS (helpers verified; imports unresolvable)")

if FAIL:
    print(f"\nFAILED ({len(FAIL)}):")
    for f in FAIL:
        print(f"  ✗  {f}")
    sys.exit(1)
else:
    print(f"\nAll arithmetic claims: PASS")

if __name__ == "__main__":
    pass
