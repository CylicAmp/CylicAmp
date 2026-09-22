"""
division_582739_937285_audit.py

Division 937285 / 582739: decimal tail collapse and Z/37Z slot structure.

─────────────────────────────────────────────────────────────────
NUMBERS:
  num1 = 582739 = 149 × 3911
  num2 = 937285 = 5 × 31 × 6047

DIVISION:
  937285 / 582739 ≈ 1.60841302881736…
  First 12 decimal digits: 608413028817
  Digit sum: 6+0+8+4+1+3+0+2+8+8+1+7 = 48 → DR = 3

KEY FACTS:
  (D1) Both numbers share digit sum 34 and DR 7.
       digit_sum(582739) = 5+8+2+7+3+9 = 34
       digit_sum(937285) = 9+3+7+2+8+5 = 34
       34 = F(9) = 2×17 (Fibonacci entry point of 17; 17 is the
       slot difference between 191 and 100 in Z/37Z).

  (D2) Slot assignments in Z/37Z:
       582739 mod 37 = 26  (slot 26: same as 137, 100, 248, 359)
       937285 mod 37 =  1  (unity slot)

  (D3) Modular ratio in Z/37Z:
       26⁻¹ mod 37 = 10  (since 26×10 = 260 = 7×37+1 ≡ 1)
       937285/582739 in Z/37Z = 1 × 10 = 10
       10 = repunit_2 − 1 = 11 − 1

  (D4) Difference and sum:
       937285 − 582739 = 354546   DR = 9    mod 37 = 12
       937285 + 582739 = 1520024  DR = 5    mod 37 = 27

  (D5) Decimal tail DR collapses:
       First  6 decimal digits → DR = 4
       First  9 decimal digits → DR = 5
       First 12 decimal digits → DR = 3  (user's result)
       First 18 decimal digits → DR = 2
─────────────────────────────────────────────────────────────────
"""

from sympy import factorint
from decimal import Decimal, getcontext

getcontext().prec = 60

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


def digit_sum(n):
    return sum(int(c) for c in str(n))


def decimal_dr(num, denom, n_digits):
    d = Decimal(num) / Decimal(denom)
    dec_str = str(d).split('.')[1][:n_digits]
    s = sum(int(c) for c in dec_str)
    while s >= 10:
        s = sum(int(c) for c in str(s))
    return s


NUM1 = 582739
NUM2 = 937285


# ── Factorizations ────────────────────────────────────────────────────────────

check(factorint(NUM1) == {149: 1, 3911: 1}, "582739 = 149×3911",
      factorint(NUM1), {149: 1, 3911: 1})
check(factorint(NUM2) == {5: 1, 31: 1, 6047: 1}, "937285 = 5×31×6047",
      factorint(NUM2), {5: 1, 31: 1, 6047: 1})


# ── D1: Shared digit sum 34 and DR 7 ─────────────────────────────────────────

check(digit_sum(NUM1) == 34, "digit_sum(582739) = 34", digit_sum(NUM1), 34)
check(digit_sum(NUM2) == 34, "digit_sum(937285) = 34", digit_sum(NUM2), 34)
check(dr(NUM1) == 7, "DR(582739) = 7", dr(NUM1), 7)
check(dr(NUM2) == 7, "DR(937285) = 7", dr(NUM2), 7)

# 34 = F(9) = 2×17
def fibonacci(n):
    fibs = [1, 1]
    while len(fibs) < n:
        fibs.append(fibs[-1] + fibs[-2])
    return fibs[:n]

FIBS = fibonacci(20)
check(FIBS[8] == 34, "F(9) = 34", FIBS[8], 34)
check(34 == 2 * 17, "34 = 2×17", 34, 2 * 17)
check(digit_sum(NUM1) == FIBS[8], "digit_sum = F(9) = 34", digit_sum(NUM1), FIBS[8])


# ── D2: Slot assignments in Z/37Z ────────────────────────────────────────────

check(NUM1 % 37 == 26, "582739 mod 37 = 26 (slot of 137)", NUM1 % 37, 26)
check(NUM2 % 37 == 1,  "937285 mod 37 = 1 (unity slot)",  NUM2 % 37, 1)

# Slot 26 family: 137, 100, 248, 359, 582739
for v in [100, 137, 248, 359, NUM1]:
    check(v % 37 == 26, f"{v} mod 37 = 26", v % 37, 26)


# ── D3: Modular ratio in Z/37Z ───────────────────────────────────────────────

# 26 × 10 ≡ 1 (mod 37)
check(26 * 10 % 37 == 1, "26×10 ≡ 1 (mod 37)", 26 * 10 % 37, 1)
check(pow(26, -1, 37) == 10, "26⁻¹ mod 37 = 10", pow(26, -1, 37), 10)

# ratio in Z/37Z
mod_ratio = (NUM2 % 37 * pow(NUM1 % 37, -1, 37)) % 37
check(mod_ratio == 10, "937285/582739 in Z/37Z = 10", mod_ratio, 10)

# 10 = 11 - 1 = repunit_2 - 1
check(10 == 11 - 1, "10 = repunit_2 - 1", 10, 11 - 1)
check(11 % 37 == 11, "11 = repunit_2 slot", 11 % 37, 11)


# ── D4: Difference and sum ────────────────────────────────────────────────────

diff = NUM2 - NUM1
total = NUM2 + NUM1
check(diff == 354546, "937285 - 582739 = 354546", diff, 354546)
check(dr(diff) == 9, "DR(354546) = 9", dr(diff), 9)
check(diff % 37 == 12, "354546 mod 37 = 12", diff % 37, 12)

check(total == 1520024, "937285 + 582739 = 1520024", total, 1520024)
check(dr(total) == 5, "DR(1520024) = 5", dr(total), 5)
check(total % 37 == 27, "1520024 mod 37 = 27", total % 37, 27)


# ── D5: Decimal tail DR collapses ─────────────────────────────────────────────

check(decimal_dr(NUM2, NUM1, 6)  == 4, "first  6 decimal digits → DR = 4",
      decimal_dr(NUM2, NUM1, 6),  4)
check(decimal_dr(NUM2, NUM1, 9)  == 5, "first  9 decimal digits → DR = 5",
      decimal_dr(NUM2, NUM1, 9),  5)
check(decimal_dr(NUM2, NUM1, 12) == 3, "first 12 decimal digits → DR = 3",
      decimal_dr(NUM2, NUM1, 12), 3)
check(decimal_dr(NUM2, NUM1, 18) == 2, "first 18 decimal digits → DR = 2",
      decimal_dr(NUM2, NUM1, 18), 2)

# User's manual: decimal digits 608413028817, sum=48, DR=3
dec_str_12 = str(Decimal(NUM2) / Decimal(NUM1)).split('.')[1][:12]
check(dec_str_12 == "608413028817", "first 12 decimal digits", dec_str_12, "608413028817")
check(sum(int(c) for c in dec_str_12) == 48, "digit sum = 48",
      sum(int(c) for c in dec_str_12), 48)
check(dr(48) == 3, "DR(48) = 3", dr(48), 3)


# ── Output ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    ratio = float(NUM2) / NUM1
    print("Division 937285 / 582739 Audit")
    print("=" * 62)

    print(f"\n── Numbers ──")
    print(f"  num1 = {NUM1} = 149 × 3911  digit_sum={digit_sum(NUM1)}  DR={dr(NUM1)}")
    print(f"  num2 = {NUM2} = 5 × 31 × 6047  digit_sum={digit_sum(NUM2)}  DR={dr(NUM2)}")

    print(f"\n── D1: Shared digit sum ──")
    print(f"  digit_sum(num1) = digit_sum(num2) = 34 = F(9) = 2×17")
    print(f"  17 = criss-cross prime; slot(191)−slot(100) = 17 in Z/37Z")

    print(f"\n── D2: Slots in Z/37Z ──")
    print(f"  num1 = 582739  mod 37 = {NUM1%37}  (slot 26: same as 137, 100, 248, 359)")
    print(f"  num2 = 937285  mod 37 = {NUM2%37}  (unity slot)")

    print(f"\n── D3: Modular ratio ──")
    print(f"  26⁻¹ mod 37 = 10  (26×10 = 260 = 7×37+1 ≡ 1)")
    print(f"  937285/582739 in Z/37Z = {mod_ratio}  (= repunit_2 − 1 = 11 − 1)")

    print(f"\n── D4: Difference and sum ──")
    print(f"  {NUM2} − {NUM1} = {diff}  DR={dr(diff)}  mod37={diff%37}")
    print(f"  {NUM2} + {NUM1} = {total}  DR={dr(total)}  mod37={total%37}")

    print(f"\n── D5: Decimal collapse ──")
    print(f"  {NUM2}/{NUM1} ≈ {ratio}")
    print(f"  First 12 decimal digits: {dec_str_12}  sum=48  DR=3")
    for n in [6, 9, 12, 18]:
        print(f"  First {n:2d} digits → DR = {decimal_dr(NUM2, NUM1, n)}")

    print()
    if FAIL:
        print(f"FAILED ({len(FAIL)}):")
        for f in FAIL:
            print(f"  ✗  {f}")
        import sys; sys.exit(1)
    else:
        print("All assertions passed.")
