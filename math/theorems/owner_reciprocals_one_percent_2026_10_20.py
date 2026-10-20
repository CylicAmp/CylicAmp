# CLASS: AUDIT
"""
1 ÷ 9 .. 1 ÷ 1, 1% ÷ 1 .. 9, 1% ÷ 4 ÷ 3 ÷ 2 ÷ 1, and the halves of 3, 5, 7 (owner_work #385, 2026-10-20). Process entry: owner_work/PROCESS.md, #385.

THE OWNER'S LINES, verbatim:
    1÷9=0.1111111111
    1÷8=0.125
    1÷7=0.1428571429
    1÷6=0.1666666667
    1÷5=0.2
    1÷4=0.25
    1÷3=0.3333333333
    1÷2=0.5
    1÷1=1
    2÷2=1


    1%÷1=0.01
    1%÷2=0.005
    1%÷3=0.0033333333
    1%÷4=0.0025
    1%÷5=
    1%÷6=
    1%÷7=
    1%÷8=
    1%÷9=


    1%÷4÷3÷2÷1=0.0004166667
    0.000
    41666=23
    6+7=1+3=4+23=(2+7=(9)


    3÷2=1.5
    5÷2=2.5
    3.5=8+8=(1+6=7)
    6=6.1=1
    8=3.5=8
    8=5.3=8
    1=1.6=6

CHECKED (the calculator shows 10 places after the point and rounds the last one):
  every line 1÷9 .. 2÷2 and 1%÷1 .. 1%÷4 is right.
  The blanks, filled the same way: 1%÷5=0.002, 1%÷6=0.0016666667, 1%÷7=0.0014285714, 1%÷8=0.00125, 1%÷9=0.0011111111.
  1% ÷ n has the digits of 1 ÷ n moved two places to the right (1% = 0.01): with zero and without, only the zeros in front change.
  1% ÷ 4 ÷ 3 ÷ 2 ÷ 1 = 1% ÷ 24 = 0.0004166667                                                              right
  0.000 | 41666 : the zeros set apart (with zero and without) ; 4+1+6+6+6 = 23                              right
  6+7 = 13 → 1+3 = 4 ; 4+23 = 27 → 2+7 = 9                                                                  right
    (all digits: 4+1+6+6+6+6+7 = 36 → 9). The last 7 is the calculator rounding: the number goes on 0.000416666... with 6s for ever;
    cut there instead of rounded, the digits add to 35 → 8. The 9 comes from the rounded 7.
  3÷2 = 1.5 → 1+5 = 6 ; 5÷2 = 2.5 → 2+5 = 7 ; 7÷2 = 3.5 → 3+5 = 8 : the halves of 3, 5, 7 read 6, 7, 8         right
  1÷2, 1÷4, 1÷8 read 5, 2+5 = 7, 1+2+5 = 8 : the halving walk of #382 (5 → 7 → 8 → 4 → 2 → 1).
  The lines "3.5=8+8=(1+6=7)" .. "1=1.6=6" are #384 again; the question there (the two digits, or the sum 7) is still open.
FRAMEWORKS (gf37-audit): 24 = 4x3x2x1 SEED ; 23 prime TESLA (2x23+1 = 47) ; 27 NEG_H ; 41666 = 2x83x251 = 4 C3 ; 2400 = 32 SEED.

FALSIFICATION: any assertion failing.
"""
from decimal import ROUND_HALF_UP, Decimal, getcontext

from sympy import factorint, isprime

getcontext().prec = 40


def calc(x):
    q = Decimal(x).quantize(Decimal("1e-10"), rounding=ROUND_HALF_UP)
    return format(q.normalize(), "f")


owner_1 = {9: "0.1111111111", 8: "0.125", 7: "0.1428571429", 6: "0.1666666667", 5: "0.2", 4: "0.25", 3: "0.3333333333", 2: "0.5", 1: "1"}
assert all(calc(Decimal(1) / n) == v for n, v in owner_1.items()) and calc(Decimal(2) / 2) == "1"
owner_pct = {1: "0.01", 2: "0.005", 3: "0.0033333333", 4: "0.0025"}
assert all(calc(Decimal("0.01") / n) == v for n, v in owner_pct.items())
filled = {n: calc(Decimal("0.01") / n) for n in range(5, 10)}
assert filled == {5: "0.002", 6: "0.0016666667", 7: "0.0014285714", 8: "0.00125", 9: "0.0011111111"}
for n in range(1, 10):
    assert Decimal("0.01") / n == (Decimal(1) / n) / 100

v = calc(Decimal("0.01") / 4 / 3 / 2 / 1)
assert v == "0.0004166667" and 4 * 3 * 2 * 1 == 24 and Decimal("0.01") / 24 == Decimal(1) / 2400
digits = v.split(".")[1]
assert digits[:3] == "000" and digits[3:8] == "41666" and 4 + 1 + 6 + 6 + 6 == 23
assert 6 + 7 == 13 and 1 + 3 == 4 and 4 + 23 == 27 and 2 + 7 == 9 and sum(map(int, digits)) == 36
true_cut = str((Decimal(1) / 2400).quantize(Decimal("1e-10"), rounding="ROUND_DOWN"))
assert true_cut == "0.0004166666" and sum(map(int, true_cut.split(".")[1])) == 35

assert [sum(map(int, str(Decimal(n) / 2).replace(".", ""))) for n in (3, 5, 7)] == [6, 7, 8]
assert [sum(map(int, s.replace(".", ""))) for s in ("0.5", "0.25", "0.125")] == [5, 7, 8]
assert factorint(41666) == {2: 1, 83: 1, 251: 1} and (24 % 37, 23 % 37, 27 % 37, 41666 % 37, 2400 % 37) == (24, 23, 27, 4, 32) and isprime(23) and isprime(47)

if __name__ == "__main__":
    print("#385: table right; blanks 0.002 0.0016666667 0.0014285714 0.00125 0.0011111111; 1%/24 = 0.0004166667, 41666 -> 23, 6+7 -> 4, 4+23 = 27 -> 9 (with the rounded 7)")
