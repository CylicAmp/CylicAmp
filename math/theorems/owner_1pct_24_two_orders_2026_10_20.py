# CLASS: AUDIT
"""
0.0004166666666666666666666666668 versus 0.0004166666666666666666666666666 (owner_work #394, 2026-10-20). Process entry: owner_work/PROCESS.md, #394.

THE OWNER'S LINE, verbatim:
    0.0004166666666666666666666666668 versus 0.0004166666666666666666666666666.

WHAT THEY ARE: the two orders of #386 on a calculator that keeps 28 digits (counting from the 4):
    1% ÷ 1 ÷ 2 ÷ 3 ÷ 4 = 0.0004166666666666666666666666668
    1% ÷ 4 ÷ 3 ÷ 2 ÷ 1 = 0.0004166666666666666666666666666
  The true value is 1% ÷ 24 = 1 ÷ 2400 = 0.000416666... with 6s for ever; kept to 28 digits in one step it is ...667.
WHY THE LAST DIGIT DIFFERS (right, reproduced exactly with 28-digit arithmetic, round half to even):
  ÷1 ÷2 ÷3 ÷4 : 0.01 → 0.005 → 0.005 ÷ 3 = 0.001666...667 (the 6s are cut, the last one rounded UP to 7) → ÷ 4 = 0.000416...66675 → kept: ...668
  ÷4 ÷3 ÷2 ÷1 : 0.01 → 0.0025 → 0.0025 ÷ 3 = 0.000833...333 (the 3s are cut, nothing to round up) → ÷ 2 = 0.000416...6665 → kept: ...666
  The rounding happens at the ÷ 3 step, and it happens in opposite directions in the two orders. With exact fractions both orders are 1/2400.
THE TWO NUMBERS IN THE OWNER'S CHAIN:
  ...668 : 4 + 1 + 25 sixes + 8 = 4+1+150+8 = 163 → 1+6+3 = 10 → 1
  ...666 : 4 + 1 + 26 sixes = 4+1+156 = 161 → 1+6+1 = 8
  the difference is 2 in the last place (8 − 6), and 8 + 2 = 10 → 1, so the chains differ by the same 2.
  Against the true value: ...668 is 1.33 of the last place too high, ...666 is 0.67 too low; ...667 is the closest.

FALSIFICATION: any assertion failing.
"""
from decimal import ROUND_HALF_EVEN, Decimal, localcontext
from fractions import Fraction as Q

A, B = "0.0004166666666666666666666666668", "0.0004166666666666666666666666666"
with localcontext() as ctx:
    ctx.prec, ctx.rounding = 28, ROUND_HALF_EVEN
    up = Decimal("0.01") / 1 / 2 / 3 / 4
    down = Decimal("0.01") / 4 / 3 / 2 / 1
    one = Decimal("0.01") / 24
    third_a = Decimal("0.005") / 3
    third_b = Decimal("0.0025") / 3
assert (str(up), str(down), str(one)) == (A, B, "0.0004166666666666666666666666667")
assert str(third_a).endswith("667") and str(third_b).endswith("333")
assert Q(1, 100) / 1 / 2 / 3 / 4 == Q(1, 100) / 4 / 3 / 2 / 1 == Q(1, 2400)

da, db = A.split(".")[1], B.split(".")[1]
assert da[:3] == db[:3] == "000" and len(da.lstrip("0")) == len(db.lstrip("0")) == 28
assert da.lstrip("0") == "41" + "6" * 25 + "8" and db.lstrip("0") == "41" + "6" * 26
chain = lambda n: n if n < 10 else chain(sum(map(int, str(n))))
assert sum(map(int, da)) == 163 and chain(163) == 1 and sum(map(int, db)) == 161 and chain(161) == 8 and (8 + 2) % 9 == 1
true = Q(1, 2400)
ulp = Q(1, 10 ** 31)
assert (Q(A) - true) / ulp == Q(4, 3) and (true - Q(B)) / ulp == Q(2, 3)

if __name__ == "__main__":
    print("#394: ...668 is 1%/1/2/3/4 and ...666 is 1%/4/3/2/1 on 28 digits; the ÷3 step rounds up in one order and down in the other; true 1/2400 = ...666 forever")
