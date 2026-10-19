# CLASS: AUDIT
"""
9 / 2 / 2 / 2 = 1.125, 1.125 + 0.012 = 1.137, and two ones that "make two" (owner_work #368, 2026-10-19).

THE OWNER'S LINES, verbatim:
    check this out
    1 +3 twos
    9÷2÷2÷2=

    1.125+0.012=1.137

    do you see it?

    1125

    its not two ones, its 11 it eleven because two ones are a 2...or its 101 and so on 1001  100010001
    2 one that make two must be separated by only zeros..Or they will immediately have their path of least resistance broken if now they have
    and numver filling the space and if all the space filled up with 9 amd no more room left than what was once sperated by space is now apart of
  The last sentence stops at "apart of": its end is missing and is left blank here.

CHECKED, in the owner's notation:
  9/2=4.5, 4.5/2=2.25, 2.25/2=1.125 ; 1.125 = 1+0.125 = 1 + 1/2/2/2 ("1 +3 twos")        right
  1.125+0.012=1.137                                                                    right
  0.125+0.012=0.137, so 125+12=137 and 1137=1000+137 ; 1137=3x379 ; 1125=9x125=3x3x5x5x5
  11 is eleven, its digits add 1+1=2. The ones that add to 2 with nothing else: 11, 101, 1001, 10001, ... (10^k + 1, digit sum 2).
  10001 = 73x137: the owner's July result 10^4+1 = 73x137 (digits_137_and_7.py), why 1/137 repeats every 8 digits.
  1001 = 7x11x13 ; 101 prime ; 11 prime.
  100010001 has three ones: 1+1+1=3, and 100010001 = 111x91x9901 = 3x7x13x37x9901 (37 divides it). The next number with two ones after 1001 is 10001.
  A digit between the ones adds to the sum: 121 -> 1+2+1=4. Nines are the exception for the root: 191 -> 1+9+1=11=2, 1991 -> 20=2, 19991 -> 29=11=2:
    the root stays 2, because 9 counts as 0 in a digital root. When the space is all 9s and one more is added, the carry runs through:
    191+9=200, 1991+9=2000, 19991+9=20000: the two ones end as one 2 at the front.
  The same carry is why 1/81 = 0.012345679... has no 8 (pasted_123456789_output_audit_2026_10_19.py), and 0.012 is how 1/81 begins.
FRAMEWORKS (gf37-audit): 9 SA_ST_A ; 1125 = 15 DARK_A ; 12 SA_ST_A ; 1137 = 27 NEG_H ; 137 = 26 IC (twin with 139) ; 11 NEG_H (twin, Sophie Germain: 23) ;
  101 = 27 NEG_H (twin with 103) ; 1001 = 2 DARK_A ; 10001 = 11 NEG_H ; 100010001 = 0 (37 divides it).
PRIOR ART: T234 (theorem_234_1137_decimal_shift.py) starts from 1.137 too (digits 1, 1, 3, 7); the route 9/2/2/2 + 0.012 is new here.

FALSIFICATION: any assertion failing.
"""
from fractions import Fraction as Q

from sympy import factorint, isprime


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


assert Q(9) / 2 / 2 / 2 == Q(9, 8) == Q(1125, 1000) == 1 + Q(1, 2 * 2 * 2)
assert [Q(9) / 2, Q(9) / 4, Q(9) / 8] == [Q(45, 10), Q(225, 100), Q(1125, 1000)]
assert Q(1125, 1000) + Q(12, 1000) == Q(1137, 1000) and Q(125, 1000) + Q(12, 1000) == Q(137, 1000)
assert 125 + 12 == 137 and 1137 == 1000 + 137 and factorint(1137) == {3: 1, 379: 1} and 1125 == 9 * 125 and factorint(1125) == {3: 2, 5: 3}

ones = [10 ** k + 1 for k in range(1, 9)]
assert ones[:4] == [11, 101, 1001, 10001] and all(sum(map(int, str(n))) == 2 for n in ones)
assert all(str(n)[0] == str(n)[-1] == "1" and set(str(n)[1:-1]) <= {"0"} for n in ones)
assert isprime(11) and isprime(101) and factorint(1001) == {7: 1, 11: 1, 13: 1} and factorint(10001) == {73: 1, 137: 1}
assert pow(10, 4, 137) == 136 and pow(10, 8, 137) == 1 and all(pow(10, k, 137) != 1 for k in range(1, 8))
assert str(10 ** 8 // 137).zfill(8) == "00729927" and 72 + 9927 == 9999

assert sum(map(int, "100010001")) == 3 and 100010001 == 111 * 91 * 9901 and factorint(100010001) == {3: 1, 7: 1, 13: 1, 37: 1, 9901: 1}
assert 100010001 % 37 == 0 and 100010001 == 10 ** 8 + 10 ** 4 + 1

# a digit in the space adds to the sum; nines keep the root at 2; one more 9 carries the two ones into a 2
assert sum(map(int, "121")) == 4
for m in range(1, 9):
    n = int("1" + "9" * m + "1")
    assert dr(n) == 2 and sum(map(int, str(n))) == 2 + 9 * m
    assert n + 9 == 2 * 10 ** (m + 1)
assert (191 + 9, 1991 + 9, 19991 + 9) == (200, 2000, 20000)
assert [sum(map(int, s)) for s in ("191", "1991", "19991")] == [11, 20, 29] and [dr(x) for x in (11, 20, 29)] == [2, 2, 2]

# 1/81 begins 0.012 and skips 8 by the same carry
assert str(10 ** 9 // 81).zfill(9) == "012345679" and str(10 ** 3 // 81).zfill(3) == "012"
assert sum(k * 10 ** (8 - k) for k in range(9)) == 12345678 and 10 ** 9 // 81 == 12345679

# frameworks
ORB = {"IC": {1, 10, 26}, "NEG_H": {11, 27, 36}, "SA_ST_A": {9, 12, 16}, "C3": {3, 4, 30}, "D7": {7, 33, 34},
       "SEED": {18, 24, 32}, "TESLA": {6, 8, 23}, "CAS_EXT": {5, 13, 19}, "NQR17": {17, 22, 35},
       "DARK_A": {2, 15, 20}, "SA_ST_B": {21, 25, 28}, "C9": {14, 29, 31}}
orbit = lambda n: next((k for k, v in ORB.items() if n % 37 in v), "SEAM")
assert [orbit(n) for n in (9, 1125, 12, 1137, 137, 11, 101, 1001, 10001, 100010001)] == [
    "SA_ST_A", "DARK_A", "SA_ST_A", "NEG_H", "IC", "NEG_H", "NEG_H", "DARK_A", "NEG_H", "SEAM"]
assert isprime(139) and isprime(13) and isprime(103) and isprime(23) and 2 * 11 + 1 == 23

if __name__ == "__main__":
    print("9/2/2/2 = 1.125, 1.125 + 0.012 = 1.137 (125 + 12 = 137); two ones adding to 2: 11, 101, 1001, 10001 = 73 x 137; "
          "nines keep the root 2 and carry the ones into a 2 (1991 + 9 = 2000)")
