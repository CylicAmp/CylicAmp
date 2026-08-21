# -*- coding: utf-8 -*-
"""
================================================================================
THEOREM 253: 1/998001 — Repunit Square and the Concatenation Sequence
================================================================================

CORE FACT:
  1/998001 = 0.000001002003004005...995996997000001002...
  Period = 2997. Concatenates every three-digit number 000-997 then repeats.

PROOF:

A. SERIES IDENTITY (corrected):
  Standard identity: sum_{n=0}^{inf} n * x^n = x / (1-x)^2
  Multiply both sides by x:
    sum_{n=0}^{inf} n * x^{n+1} = x^2 / (1-x)^2

  Set x = 10^{-3} = 1/1000:
    x^2 / (1-x)^2 = (10^{-3})^2 / (1 - 10^{-3})^2
                  = 10^{-6} / (0.999)^2
                  = 10^{-6} / 0.998001
                  = 10^{-6} * 10^6 / 998001
                  = 1 / 998001   [correct]

  And:
    sum_{n=0}^{inf} n * x^{n+1} at x=10^{-3}
    = sum_{n=0}^{inf} n * 10^{-3(n+1)}
    = 0*10^{-3} + 1*10^{-6} + 2*10^{-9} + 3*10^{-12} + ...
    = 0.000 001 002 003 004 ...

  Therefore: 1/998001 = 0.000001002003004...

B. PERIOD = 2997:
  998001 = 999^2 = (10^3 - 1)^2
  The decimal period of 1/(10^k - 1)^2 is k*(10^k - 1).
  For k=3: period = 3 * 999 = 2997.
  The sequence runs 000, 001, ..., 997 (998 terms * 3 digits = 2994 digits),
  then 998 would carry and break the pattern — hence period 2997, not 2994.

C. GRID AND DIAGONALS (W=74, step=75):
  Arrange the 2997-digit period in rows of width 74.
  Diagonal step = W+1 = 75.
  Since 75 = 3 * 25, each diagonal step advances exactly 25 full three-digit
  numbers in the sequence.

  For offsets that are multiples of 3:
    offset 0  -> three-digit numbers 000, 025, 050, 075, ...  (AP, diff 25)
    offset 3  -> three-digit numbers 001, 026, 051, 076, ...  (AP, diff 25)
    offset 6  -> three-digit numbers 002, 027, 052, 077, ...  (AP, diff 25)
    ...
    offset 3j -> three-digit numbers j, j+25, j+50, j+75, ...  (AP, diff 25)

  For offsets NOT multiples of 3: digits span across number boundaries — not
  clean three-digit reads.

  Note: the diagonal does NOT produce single digits 0,1,2,3,... at step=75.
  Single-digit sequential access requires step=1 (trivial column-by-column).

D. GF(37) CONNECTION:
  999 = 27 * 37 = 3^3 * 37.
  998001 = 999^2 = 3^6 * 37^2.
  Period 2997 = 3 * 999 = 3 * 3^3 * 37 = 3^4 * 37.
  2997 mod 37 = 2997 - 81*37 = 2997 - 2997 = 0.  SEAM.
  The period is a SEAM of GF(37): it is a multiple of 37.
  DR(2997) = DR(2+9+9+7) = DR(27) = 9 in SA.
================================================================================
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 3200

P = 37
SA = {4, 9, 25, 30}
ST = {3, 12, 21, 30}
H_SET = {1, 10, 26}
SEED_ORBIT = {18, 24, 32}


def dr(n):
    n = abs(n)
    if n == 0: return 0
    r = n % 9
    return 9 if r == 0 else r


def flags(r):
    f = []
    if r == 0:          f.append("SEAM")
    if r in H_SET:      f.append("H")
    if r in SA:         f.append("SA")
    if r in ST:         f.append("ST")
    if r in SEED_ORBIT: f.append("SEED")
    return ','.join(f) or '-'


def run():
    print("=" * 70)
    print("THEOREM 253: 1/998001 — REPUNIT SQUARE AND CONCATENATION SEQUENCE")
    print("=" * 70)

    # A: Series identity (corrected)
    print("\nA. SERIES IDENTITY (x^2/(1-x)^2 at x=10^-3):")
    x = Fraction(1, 1000)
    result = x**2 / (1 - x)**2
    assert result == Fraction(1, 998001), f"Expected 1/998001, got {result}"
    print(f"  x^2/(1-x)^2 at x=1/1000 = {result} = 1/998001  check")

    wrong = x / (1 - x)**2
    assert wrong == Fraction(1000, 998001)
    print(f"  x/(1-x)^2  at x=1/1000 = {wrong}  [WRONG — off by 1000]  check")

    # Verify series numerically
    s = Fraction(0)
    for n in range(1, 3000):
        s += n * x**(n + 1)
    diff = abs(float(s) - 1/998001)
    assert diff < 1e-12
    print(f"  sum_{{n=0}}^{{2999}} n*x^(n+1) ≈ {float(s):.13f}")
    print(f"  1/998001                    = {1/998001:.13f}  check")

    # B: Period
    print(f"\nB. PERIOD = 2997:")
    assert 998001 == 999**2
    assert 999 == 10**3 - 1
    period = 3 * 999
    assert period == 2997
    print(f"  998001 = 999^2 = (10^3-1)^2  check")
    print(f"  period = 3 * 999 = {period}  check")

    # Get digit string
    d = Decimal(1) / Decimal(998001)
    digit_str = str(d)[2:2 + period]
    assert len(digit_str) == period
    print(f"  First 30 digits: {digit_str[:30]}")
    print(f"  Last  30 digits: {digit_str[-30:]}")

    # Verify concatenation: first three-digit blocks
    for k in range(0, 10):
        block = digit_str[3*k:3*k+3]
        assert int(block) == k, f"Block {k}: expected {k:03d}, got {block}"
    print(f"  Blocks 000..009 verified  check")
    for k in range(990, 998):
        block = digit_str[3*k:3*k+3]
        assert int(block) == k, f"Block {k}: expected {k:03d}, got {block}"
    print(f"  Blocks 990..997 verified  check")

    # C: Grid diagonals
    print(f"\nC. GRID W=74, STEP=75 — THREE-DIGIT DIAGONAL APs:")
    W = 74
    step = W + 1  # 75
    assert step == 75
    assert step % 3 == 0
    advance = step // 3  # = 25 full numbers per step
    assert advance == 25
    print(f"  Step={step} = 3 * {advance}  (advances {advance} full numbers per diagonal step)")

    for j in range(5):
        offset = 3 * j
        nums = []
        for i in range(8):
            pos = (offset + i * step) % period
            nums.append(int(digit_str[pos:pos+3]))
        diffs = [nums[i+1] - nums[i] for i in range(len(nums)-1)]
        assert all(d == 25 for d in diffs), f"offset {offset}: diffs={diffs}"
        print(f"  offset {offset:2d} -> {nums[:6]}  diff=25  check")

    # Confirm non-multiple-of-3 offsets are garbled
    offset = 1
    nums = [int(digit_str[(offset + i*step) % period:(offset + i*step) % period + 3])
            for i in range(6)]
    print(f"  offset  1 (not mult of 3) -> {nums}  [garbled, crosses boundaries]")

    # D: GF(37) connection
    print(f"\nD. GF(37) CONNECTION:")
    assert 999 == 3**3 * 37
    assert 998001 == 999**2
    assert period % P == 0
    assert dr(period) == 9 and 9 in SA
    print(f"  999 = 3^3 * 37  check")
    print(f"  998001 = 999^2 = 3^6 * 37^2  check")
    print(f"  period 2997 mod{P} = {period % P}  [{flags(period % P)}]  check")
    print(f"  DR(2997) = {dr(period)}  in SA:{dr(period) in SA}  check")
    print(f"  The period is a SEAM of GF(37)  check")

    print(f"\nAll verifications passed.")


if __name__ == "__main__":
    run()
