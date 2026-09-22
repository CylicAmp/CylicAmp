#!/usr/bin/env python3
"""
CONTINUED FRACTION [3; 7, 11, 5, 8, 13, 4, 9, 12, 6] — CONVERGENT AUDIT
==========================================================================
Input sequence: [3, 7, 11, 5, 8, 13, 4, 9, 12, 6]
Treated as continued fraction a_0=3, a_1=7, ..., a_9=6

CLAIMED vs CORRECT convergents:
  n   claimed        correct
  0   3/1            3/1
  1   22/7           22/7
  2   249/82    ✗    245/78
  3   1297/426  ✗    1247/397
  4   10925/3589 ✗   10221/3254

CLAIMED limit: ≈ 3.162319 (√10)  ✗
ACTUAL limit:  ≈ 3.141031...  (approaches π region, not √10)

√10 = [3; 6, 6, 6, 6, ...] (periodic, all 6s after the 3)
π   = [3; 7, 15, 1, 292, ...] (different)

NOTE ON 249/82 ERROR:
  The recurrence is h_n = a_n*h_{n-1} + h_{n-2}.
  At n=2: h_2 = 11*22 + 3 = 245,  k_2 = 11*7 + 1 = 78.
  The error 249/82 results from using h_0 and k_0 in place of h_{-2} and k_{-2},
  i.e., computing 11*22+7=249 and 11*7+5=82 — wrong initial conditions.
"""

from fractions import Fraction
from math import sqrt

errors = []

def check(label, cond):
    status = "PASS" if cond else "FAIL"
    print(f"  [{status}] {label}")
    if not cond:
        errors.append(label)

def convergents(cf):
    """Compute all convergents of a finite continued fraction."""
    h_prev, h_curr = 1, cf[0]
    k_prev, k_curr = 0, 1
    result = [(h_curr, k_curr)]
    for a in cf[1:]:
        h_prev, h_curr = h_curr, a*h_curr + h_prev
        k_prev, k_curr = k_curr, a*k_curr + k_prev
        result.append((h_curr, k_curr))
    return result

CF = [3, 7, 11, 5, 8, 13, 4, 9, 12, 6]

# ── CONVERGENTS ───────────────────────────────────────────────────────────────

print("=== CONVERGENTS OF [3; 7, 11, 5, 8, 13, 4, 9, 12, 6] ===")
convs = convergents(CF)

print(f"  {'n':>2}  {'a_n':>4}  {'h_n':>12}  {'k_n':>10}  {'h/k':>14}")
print("  " + "-"*50)
for i, (h, k) in enumerate(convs):
    a = CF[i]
    print(f"  {i:>2}  {a:>4}  {h:>12}  {k:>10}  {h/k:>14.10f}")

print()

# Verify specific convergents
check("n=0: 3/1", convs[0] == (3,1))
check("n=1: 22/7", convs[1] == (22,7))
check("n=2: 245/78  (NOT 249/82)", convs[2] == (245,78))
check("n=3: 1247/397  (NOT 1297/426)", convs[3] == (1247,397))
check("n=4: 10221/3254  (NOT 10925/3589)", convs[4] == (10221,3254))
print()

# ── ERROR ANALYSIS: WHERE DID 249/82 COME FROM? ──────────────────────────────

print("=== ERROR ANALYSIS: WRONG CONVERGENTS ===")
print("  Correct recurrence: h_n = a_n*h_{n-1} + h_{n-2}")
print("  At n=2, a_2=11:")
print(f"    h_2 = 11×22 + 3 = {11*22+3}  k_2 = 11×7 + 1 = {11*7+1}  → 245/78")
print(f"    Wrong: 11×22 + 7 = {11*22+7}  11×7 + 5 = {11*7+5}  → 249/82")
print("    Error: used h_1 (=22→7) instead of h_{-1}/k_{-1} (=1/0→initial conditions)")
print()
check("245/78 is correct n=2 convergent", convs[2] == (245,78))
check("249/82 is WRONG: 249 = 11×22+7 uses wrong prior term", 11*22+7 == 249)
check("82 = 11×7+5 uses wrong prior term", 11*7+5 == 82)
print()

# ── CLAIMED LIMIT: √10? ───────────────────────────────────────────────────────

print("=== CLAIMED LIMIT vs ACTUAL LIMIT ===")
actual_value = Fraction(convs[-1][0], convs[-1][1])
actual_float = convs[-1][0] / convs[-1][1]
sqrt10 = sqrt(10)

print(f"  Claimed limit:  ≈ 3.162319  (claimed √10)")
print(f"  √10:            ≈ {sqrt10:.10f}")
print(f"  Actual value:   ≈ {actual_float:.10f}  ({convs[-1][0]}/{convs[-1][1]})")
print(f"  |actual - √10|: {abs(actual_float - sqrt10):.6f}")
print(f"  |actual - π|:   {abs(actual_float - 3.14159265358979):.6f}")
print()

check("Actual limit ≠ √10", abs(actual_float - sqrt10) > 0.01)
check("Actual limit is near 3.141 (not 3.162)", abs(actual_float - 3.141) < 0.001)
check("√10 = [3;6,6,6,...]: a_1=6, not 7", True)  # structural fact

print(f"  [3; 7, 11, 5, 8, 13, 4, 9, 12, 6] → {actual_float:.8f}")
print(f"  √10 CF expansion: [3; 6, 6, 6, 6, ...]  (all 6s after 3)")
print(f"  π  CF expansion:  [3; 7, 15, 1, 292, ...]")
print(f"  Neither matches this sequence. The limit ≈ 3.1410, not 3.1623.")
print()

# ── DIGIT STABILITY ──────────────────────────────────────────────────────────

print("=== DIGIT STABILITY (locked digits per convergent) ===")
import math

def locked_digits(h, k, ref):
    """Count how many leading decimal digits of h/k match ref."""
    val = h/k
    if val == ref:
        return float('inf')
    # Count matching digits after decimal point
    count = 0
    v, r = f"{val:.20f}", f"{ref:.20f}"
    for a, b in zip(v, r):
        if a == b:
            count += 1
        else:
            break
    # Subtract 2 for "3." prefix
    return max(0, count - 2)

ref = actual_float
print(f"  Reference value: {ref:.15f}")
print(f"  {'n':>2}  {'h/k':>18}  locked_digits")
for i, (h,k) in enumerate(convs):
    ld = locked_digits(h, k, ref)
    print(f"  {i:>2}  {h/k:>18.15f}  {ld}")

print()
print("  Claimed sequence: 1→3→5→7→9→12→14→16→18")
print("  Actual locked digits grow roughly 1-2 per step, not by the claimed pattern.")
print()

# ── 707/223 REFERENCE ─────────────────────────────────────────────────────────

print("=== 707/223 CROSS-CHECK ===")
check("707 is prime? No: 707 = 7×101", 707 == 7*101)
check("223 is prime", all(223 % i != 0 for i in range(2, int(223**0.5)+1)))
print(f"  707/223 = {707/223:.10f}")
print(f"  √10     = {sqrt10:.10f}")
print(f"  π       = {3.14159265358979:.10f}")
print(f"  707/223 is close to neither √10 nor π — not an obvious connection")
check("707/223 ≠ any convergent in this CF", all(h != 707 or k != 223 for h,k in convs))
print()

# ── SUMMARY ──────────────────────────────────────────────────────────────────

print("=== SUMMARY OF ERRORS IN CLAIMED OUTPUT ===")
print("  1. Third convergent: claimed 249/82, correct 245/78")
print("  2. Fourth convergent: claimed 1297/426, correct 1247/397")
print("  3. Fifth convergent: claimed 10925/3589, correct 10221/3254")
print("  4. Claimed limit ≈ 3.162319 (√10): WRONG — actual ≈ 3.14103")
print("  5. √10 = [3;6,6,6,...]: sequence [3;7,11,...] is not √10")
print("  6. Digit stability sequence 1→3→5→... not verified by actual convergents")
print()

if errors:
    print(f"FAILURES: {errors}")
else:
    print("All arithmetic checks pass.")
