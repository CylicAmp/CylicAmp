#!/usr/bin/env python3
"""
CONTINUED FRACTION [3; 4, 8, 6, 9, 11, 7, 5, 13, 10, 8] — CONVERGENT AUDIT
=============================================================================
11-term sequence: a_0=3, then [4, 8, 6, 9, 11, 7, 5, 13, 10, 8]
This is the "next quality sum layer" with 3 prepended as integer part.

Contrast with prior layer [3; 7, 11, 5, 8, 13, 4, 9, 12, 6]:
  Prior layer limit: ≈ 3.14105717  (near π region)
  This layer limit:  ≈ 3.24257161  (different region)

All convergents verified correct — no arithmetic errors in this layer.
"""

from fractions import Fraction
from math import sqrt, pi

errors = []

def check(label, cond):
    status = "PASS" if cond else "FAIL"
    print(f"  [{status}] {label}")
    if not cond:
        errors.append(label)

def convergents(cf):
    h_prev, h_curr = 1, cf[0]
    k_prev, k_curr = 0, 1
    result = [(h_curr, k_curr)]
    for a in cf[1:]:
        h_prev, h_curr = h_curr, a*h_curr + h_prev
        k_prev, k_curr = k_curr, a*k_curr + k_prev
        result.append((h_curr, k_curr))
    return result

CF = [3, 4, 8, 6, 9, 11, 7, 5, 13, 10, 8]

# ── CONVERGENTS ───────────────────────────────────────────────────────────────

print("=== CONVERGENTS OF [3; 4, 8, 6, 9, 11, 7, 5, 13, 10, 8] ===")
convs = convergents(CF)

CLAIMED = [
    (3,      1),
    (13,     4),
    (107,    33),
    (655,    202),
    (6002,   1851),
    (66677,  20563),
    (472741, 145792),
    (2430382,749523),
    (32067707,9889591),
    (323107452,99645433),
    (2616927323,807053055),
]

print(f"  {'n':>2}  {'a_n':>4}  {'claimed h/k':>30}  {'correct h/k':>30}  match")
print("  " + "-"*80)
for i, ((ch,ck),(h,k)) in enumerate(zip(CLAIMED, convs)):
    a = CF[i]
    match = "✓" if (ch==h and ck==k) else "✗"
    print(f"  {i:>2}  {a:>4}  {ch:>14}/{ck:<14}  {h:>14}/{k:<14}  {match}")

print()

# Individual checks
check("n=0:  3/1", convs[0] == (3,1))
check("n=1:  13/4", convs[1] == (13,4))
check("n=2:  107/33", convs[2] == (107,33))
check("n=3:  655/202", convs[3] == (655,202))
check("n=4:  6002/1851", convs[4] == (6002,1851))
check("n=5:  66677/20563", convs[5] == (66677,20563))
check("n=6:  472741/145792", convs[6] == (472741,145792))
check("n=7:  2430382/749523", convs[7] == (2430382,749523))
check("n=8:  32067707/9889591", convs[8] == (32067707,9889591))
check("n=9:  323107452/99645433", convs[9] == (323107452,99645433))
check("n=10: 2616927323/807053055", convs[10] == (2616927323,807053055))
print()

# Decimal values
print("=== DECIMAL VALUES ===")
print(f"  {'n':>2}  {'decimal':>20}  {'claimed':>20}  match")
print("  " + "-"*70)

CLAIMED_DEC = [
    3.000000000000000,
    3.250000000000000,
    3.242424242424242,
    3.242574257425743,
    3.242571582928147,
    3.242571609200992,
    3.242571608867427,
    3.242571608876579,
    3.242571608876444,
    3.242571608876445,
    3.242571608876445,
]

for i, ((h,k), cd) in enumerate(zip(convs, CLAIMED_DEC)):
    actual = h/k
    match = "✓" if abs(actual - cd) < 1e-13 else "✗"
    print(f"  {i:>2}  {actual:>20.15f}  {cd:>20.15f}  {match}")

print()

# ── LIMIT ANALYSIS ───────────────────────────────────────────────────────────

print("=== LIMIT ANALYSIS ===")
limit = convs[-1][0] / convs[-1][1]
limit_frac = Fraction(convs[-1][0], convs[-1][1])

print(f"  Exact value:  {convs[-1][0]}/{convs[-1][1]}")
print(f"  Decimal:      {limit:.15f}")
print(f"  limit²:       {limit**2:.10f}")
print(f"  √10:          {sqrt(10):.15f}")
print(f"  √(10.5):      {sqrt(10.5):.15f}")
print(f"  π:            {pi:.15f}")
print()

check("Limit ≠ √10  (differ by 0.021)", abs(limit - sqrt(10)) > 0.01)
check("Limit > π", limit > pi)
check("Limit < √11", limit < sqrt(11))
check("limit² ≈ 10.514...", abs(limit**2 - 10.514) < 0.001)

# Check if limit² is rational-ish
lsq = limit**2
print(f"\n  limit² = {lsq:.10f}")
print(f"  Nearest simple fractions:")
for num in range(90, 115):
    for den in range(8, 12):
        if abs(num/den - lsq) < 0.001:
            print(f"    {num}/{den} = {num/den:.6f}  diff={abs(num/den-lsq):.6f}")
print()

# ── CONVERGENCE RATE ─────────────────────────────────────────────────────────

print("=== CONVERGENCE RATE ===")
ref = limit
print(f"  {'n':>2}  {'|error|':>20}  {'log10|error|':>14}")
for i, (h, k) in enumerate(convs):
    err = abs(h/k - ref)
    if err > 0:
        import math
        le = math.log10(err)
    else:
        le = float('-inf')
    print(f"  {i:>2}  {err:>20.2e}  {le:>14.2f}")
print()

# ── COMPARISON WITH PRIOR LAYER ──────────────────────────────────────────────

print("=== COMPARISON: PRIOR LAYER vs THIS LAYER ===")
prior_limit = 372253523/118512177
this_limit  = 2616927323/807053055

print(f"  Prior [3;7,11,5,8,13,4,9,12,6]:  {prior_limit:.15f}")
print(f"  This  [3;4,8,6,9,11,7,5,13,10,8]: {this_limit:.15f}")
print(f"  Difference: {abs(this_limit - prior_limit):.10f}")
print(f"  Prior is closer to π ({pi:.6f}); this layer moves away from π")
print()
check("This layer limit > prior layer limit", this_limit > prior_limit)
check("Prior layer limit < π", prior_limit < pi)
check("This layer limit > π", this_limit > pi)
print()

if errors:
    print(f"FAILURES: {errors}")
else:
    print("All convergents verified correct.")
