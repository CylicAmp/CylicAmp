# CLASS: AUDIT
"""
9% to the powers 1% .. 7%, 9% times -7 .. -4, and 9% times e^3, e^33, e^333, e^3333 (owner_work #386, 2026-10-20). The message also repeats the
#385 tables (with "1%÷1÷2÷3÷4" added) and the #384 lines. Process entry: owner_work/PROCESS.md, #386.

THE OWNER'S NEW LINES, verbatim:
    1%÷1÷2÷3÷4=0.0004166667
    0.000
    41666=23
    67=1+3=4+23=2+7=9

    9%^(1%=0.(976)(208)(141)
    9%^(2%=0.(952)(982)(334)6
    9%^(3%=0.(930)(309)(1132)
    9%^(4%=0.(908)(175)33
    9%^(5%=0.(886(568)(150)6
    9%^(6%=0.(865)(475)(046)1+9=1
    9%^(7%=0.(844)(883)(785)9+1=1

    9%×(−7=−0.63
    9%×(−6=-0.54
    9%×(−5=−0.45
    9%×(−4=−0.36

    9%×e^(3,333=nothing
    9%×e^(333=3.75236419E+143
    9%×e^(33=19,317,922,180,732
    9%×e^(3=1.8076983231

CHECKED (50-digit arithmetic; the calculator shows 10 places and rounds the last):
  1% ÷ 1 ÷ 2 ÷ 3 ÷ 4 = 1% ÷ 24 = 0.0004166667, the same as 1% ÷ 4 ÷ 3 ÷ 2 ÷ 1 (the order of the dividing makes no difference) ; 6 7 → 6+7 = 13 → 4 → 4+23 = 27 → 9   right
  0.09^0.01 = 0.976208141 ; ^0.02 = 0.9529823346 ; ^0.03 = 0.9303091132 ; ^0.04 = 0.90817533 ; ^0.05 = 0.8865681506 ; ^0.06 = 0.8654750461 ;
    ^0.07 = 0.8448837859 -- every line right, digit for digit.
  The 6% line adds to 8+6+5+4+7+5+0+4+6+1 = 46 → 4+6 = 10 → 1, the 7% line to 8+4+4+8+8+3+7+8+5+9 = 64 → 6+4 = 10 → 1: the "=1" of both lines is right,
    and 46 and 64 are the owner's pair of #267 ("46=1 / 64=1"). Their last digits are 1 and 9: 1+9 = 9+1 = 10 → 1.
    (The other lines: 38 → 2, 51 → 6, 31 → 4, 36 → 9, 53 → 8.)
  9% x (-7) = -0.63 ; x(-6) = -0.54 ; x(-5) = -0.45 ; x(-4) = -0.36                                              right
    63 and 36 are a flip, 54 and 45 are a flip: -7 with -4 and -6 with -5 (7+4 = 6+5 = 11). Forced: 9 x k and 9 x (11-k) are always each other's flip.
  9% x e^3 = 1.8076983231 ; 9% x e^33 = 19,317,922,180,732 (.45 cut off by the display) ; 9% x e^333 = 3.75236419 x 10^143       right
  9% x e^3333 = "nothing": the number is 2.8691330815 x 10^1446 (1447 digits); the calculator cannot show a number that big.
FRAMEWORKS (gf37-audit): 63 = 26 IC (the 137-map multiplier) ; 54 = 17 NQR17 ; 45 = 8 TESLA ; 36 NEG_H ; 46 = 9 SA_ST_A ; 64 = 27 NEG_H.

FALSIFICATION: any assertion failing.
"""
from decimal import ROUND_HALF_UP, Decimal

from mpmath import exp, log10, mp, mpf, nstr, power

mp.dps = 50


def calc10(x):
    q = Decimal(nstr(x, 30)).quantize(Decimal("1e-10"), rounding=ROUND_HALF_UP)
    return format(q.normalize(), "f")


from fractions import Fraction as Q
assert Q(1, 100) / 1 / 2 / 3 / 4 == Q(1, 100) / 4 / 3 / 2 / 1 == Q(1, 100) / 24 == Q(1, 2400)
assert 6 + 7 == 13 and 4 + 23 == 27

owner = {1: "0.976208141", 2: "0.9529823346", 3: "0.9303091132", 4: "0.90817533", 5: "0.8865681506", 6: "0.8654750461", 7: "0.8448837859"}
shown = {k: calc10(power(mpf("0.09"), mpf(k) / 100)) for k in range(1, 8)}
assert shown == owner
sums = {k: sum(map(int, v.split(".")[1])) for k, v in owner.items()}
assert sums == {1: 38, 2: 51, 3: 31, 4: 36, 5: 53, 6: 46, 7: 64}
dr = lambda n: 0 if n == 0 else 1 + (n - 1) % 9
assert dr(46) == dr(64) == 1 and str(46)[::-1] == "64" and 1 + 9 == 9 + 1 == 10
assert [dr(sums[k]) for k in range(1, 6)] == [2, 6, 4, 9, 8]

assert [Decimal("0.09") * k for k in (-7, -6, -5, -4)] == [Decimal("-0.63"), Decimal("-0.54"), Decimal("-0.45"), Decimal("-0.36")]
assert all(int(str(9 * k)[::-1]) == 9 * (11 - k) for k in range(2, 10)) and 7 + 4 == 6 + 5 == 11

assert calc10(mpf("0.09") * exp(3)) == "1.8076983231"
assert int(mpf("0.09") * exp(33)) == 19317922180732
assert nstr(mpf("0.09") * exp(333), 9) == "3.75236419e+143"
big = mpf("0.09") * exp(3333)
assert int(log10(big)) == 1446 and nstr(big, 11) == "2.8691330815e+1446"

assert [n % 37 for n in (63, 54, 45, 36, 46, 64)] == [26, 17, 8, 36, 9, 27]

if __name__ == "__main__":
    print("#386: 9%^1%..7% right digit for digit; 6% and 7% lines add to 46 and 64 -> 1; 9%x(-7..-4) = -0.63 -0.54 -0.45 -0.36; 9% e^3333 = 2.869e1446")
