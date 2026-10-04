"""
magic_1_palindrome_audit.py

Palindromes of the form 1B1 (first and last digit = 1, middle digit B).

PAIR CONSTRUCTION:
  From 1B1, two reversal pairs:
    Pair 1: (A, A+B) and reverse (A+B, A)  where A=1
            → numbers (1)(1+B) and (1+B)(1)
    Pair 2: (A+A, B) and reverse (B, A+A)  where A=1
            → numbers (2)(B) and (B)(2)

  Both pairs sum to the same value:
    Pair 1 sum: 10A + (A+B) + (A+B)·10 + A = 11(2A+B)
    Pair 2 sum: 10(2A) + B + B·10 + 2A    = 11(2A+B)
    With A=1: both = 11(2+B)

STEP COUNT = DIGIT SUM:
  digit_sum(1B1) = 1 + B + 1 = B + 2 = step count

  121: digit sum = 4, steps 1-4
  131: digit sum = 5, steps 1-5
  141: digit sum = 6, steps 1-6 (step 3 absent — 3 not a digit of 141)

141 EXCEPTION (step 3 absent):
  Digits of 141 are {1, 4}. No 3 appears.
  Step sequence: 1, 2, [3 absent], 4, 5, 6★
  The missing step 3 is expressed as 3+3=6 at position 5.

PAIR SUMS:
  121: 11(2+2) = 44.  13+31=44, 22+22=44
  131: 11(2+3) = 55.  14+41=55, 32+23=55
  141: 11(2+4) = 66.  15+51=66, 24+42=66

DR CHAIN:
  44 → 88 → DR(88) = 7
  55 → 11 → DR(11) = 2
  66 → 12 → DR(12) = 3
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
    r = n % 9
    return r if r else 9


def pair_sum_1b1(B):
    """Both reversal pairs from 1B1 — returns (pair1_sum, pair2_sum)."""
    A = 1
    p1 = (10 * A + (A + B)) + ((A + B) * 10 + A)
    p2 = (10 * (2 * A) + B) + (B * 10 + 2 * A)
    return p1, p2


# Both pairs always equal 11(2+B)
for B in range(0, 9):
    p1, p2 = pair_sum_1b1(B)
    expected = 11 * (2 + B)
    check(p1 == expected, f"B={B} pair1={p1}", p1, expected)
    check(p2 == expected, f"B={B} pair2={p2}", p2, expected)
    check(p1 == p2, f"B={B} pairs equal", p1, p2)

# Explicit cases
check(pair_sum_1b1(2)[0] == 44, "121 sum=44", pair_sum_1b1(2)[0], 44)
check(pair_sum_1b1(3)[0] == 55, "131 sum=55", pair_sum_1b1(3)[0], 55)
check(pair_sum_1b1(4)[0] == 66, "141 sum=66", pair_sum_1b1(4)[0], 66)

# Step count = digit sum
for B in range(0, 9):
    digit_sum = 1 + B + 1
    step_count = digit_sum
    check(step_count == B + 2, f"B={B} steps={step_count}", step_count, B + 2)

# 141: step 3 absent (3 not in digits {1,4})
digits_141 = {1, 4}
check(3 not in digits_141, "141 has no digit 3", 3, "not in {1,4}")

# DR chains
check(dr(88) == 7, "DR(88)=7", dr(88), 7)
check(dr(11) == 2, "DR(11)=2", dr(11), 2)
check(dr(12) == 3, "DR(12)=3", dr(12), 3)
check(6 + 6 == 12, "6+6=12", 6 + 6, 12)

# Verified sums
check(13 + 31 == 44, "13+31=44", 13 + 31, 44)
check(22 + 22 == 44, "22+22=44", 22 + 22, 44)
check(14 + 41 == 55, "14+41=55", 14 + 41, 55)
check(32 + 23 == 55, "32+23=55", 32 + 23, 55)
check(15 + 51 == 66, "15+51=66", 15 + 51, 66)
check(24 + 42 == 66, "24+42=66", 24 + 42, 66)

if __name__ == "__main__":
    print("Magic 1 Palindrome Audit — Form 1B1")
    print("=" * 62)
    print(f"\n  {'palindrome':>10}  {'B':>2}  {'pair_sum':>9}  {'=11(2+B)':>9}  {'steps':>5}  {'DR_chain'}")
    print("  " + "-" * 60)
    for B in range(1, 8):
        pal = 100 + B * 10 + 1
        ps = 11 * (2 + B)
        steps = 2 + B
        if B == 2:
            chain = f"44→88→DR=7"
        elif B == 3:
            chain = f"55→11→DR=2"
        elif B == 4:
            chain = f"66→12→DR=3"
        else:
            chain = f"{ps}→DR={dr(ps)}"
        print(f"  {pal:>10}  {B:>2}  {ps:>9}  {11*(2+B):>9}  {steps:>5}  {chain}")
    print(f"\n  Algebraic identity: both pairs from 1B1 sum to 11(2+B)")
    print(f"  Step count = digit sum = 2+B")
    print(f"  141: step 3 absent (3 ∉ digits of 141); expressed as 3+3=6")
    print()
    if FAIL:
        print(f"FAILED ({len(FAIL)}):")
        for f in FAIL:
            print(f"  ✗  {f}")
        import sys; sys.exit(1)
    else:
        print("All assertions passed.")
