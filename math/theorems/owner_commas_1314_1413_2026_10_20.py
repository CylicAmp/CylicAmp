# CLASS: AUDIT
"""
Ones and zeros around the comma, 1314 and its halves swapped, 1413 (owner_work #372, 2026-10-20). Process entry: owner_work/PROCESS.md, #372.

THE OWNER'S LINES, verbatim:
    1,000
    1,0
    1+1

    11,000
    11,00
    2+2


    111,000=even amount of odds
    111,000=odd amount of even
    3+3

    now we have
    1,000  (1+3=4)1314(1+3=4|1=5)
    10,000  (2+3=5)2335(2+335
    100,000 (3+3=6)+3336(
    1,000,000

    1314
    1413
    5--4
    1--2


    1413
    4-3
    1+1+1

     14.13

    14|13
      5+4=9
    141+3=9
    1-44-1-4
    1-4-1


    =

CLEANED (the owner's dashes as spaces or arrows; readings marked; nothing filled into the cut lines):
  1,000 → 1,0 → 1+1 = 2            reading: one 1 and one 0
  11,000 → 11,00 → 2+2 = 4         two 1s and two 0s
  111,000 → 3+3 = 6                three 1s and three 0s
  111,000 = 1000 x 111 : an even number (1000) of odd numbers (111)
  111,000 = 111 x 1000 : an odd number (111) of even numbers (1000)                       right, both
  1,000     1 digit before the comma + 3 after = 4 ; with the comma 4 + 1 = 5             right
  10,000    2 + 3 = 5                                                                     right
  100,000   3 + 3 = 6                                                                     right
  1,000,000 (the line stops here)
  1314 → 1413      the halves 13 | 14 swapped to 14 | 13                                  right
  1413 → 14 13 → 1+4 = 5, 1+3 = 4 → 5 4                                                    right
  1413 → 4 − 3 = 1 → 1 + 1 + 1 = 3 (with the two 1s of 1413)        reading
  14.13 → 14 | 13 → 5 + 4 = 9                                                              right (= 1+4+1+3)
  141 + 3 → 1+4+1+3 = 9, and as numbers 141 + 3 = 144 → 1+4+4 = 9                           right, both
  1-4-1 → 141, which reads the same both ways
MISSING (kept blank, asked in the reply): the rule for the third digit of 1314, 2335, 3336 (the first is the digits before the comma: 1 2 3; the
  second the digits after: 3 3 3; the fourth all the digits: 4 5 6; the third is 1 3 3); the ends of "(2+335" and "(3+3=6)+3336(" and of the
  1,000,000 line; the step "1--2" after 5 4; the line "1-44-1-4"; and what follows the last "=".
FRAMEWORKS (gf37-audit): 1314 = 2x3x3x73 = 19 CAS_EXT ; 1413 = 3x3x157 = 7 D7 ; 2335 = 5x467 = 4 C3 ; 3336 = 2x2x2x3x139 = 6 TESLA ;
  111,000 = 2x2x2x3x5x5x5x37 = 0 ; 141 = 3x47 = 30 C3 ; 144 = 12x12 = 33 D7 ; 1314+1413 = 2727 = 27x101 = 26 IC ; 1413-1314 = 99 = 25 SA_ST_B.
  73 is the 73 of 10001 = 73x137 (#368) and 139 the twin of 137.

FALSIFICATION: any assertion failing.
"""
from sympy import factorint


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


assert (1 + 1, 2 + 2, 3 + 3) == (2, 4, 6)
assert [str(n).count("1") for n in (1000, 11000, 111000)] == [1, 2, 3] and str(111000).count("0") == 3
assert 111000 == 1000 * 111 == 111 * 1000 and 111 % 2 == 1 and 1000 % 2 == 0 and 111000 % 2 == 0

for n, before, after in ((1000, 1, 3), (10000, 2, 3), (100000, 3, 3)):
    s = f"{n:,}"
    left, right = s.split(",")
    assert (len(left), len(right)) == (before, after) and before + after == len(str(n)) and len(s) == before + after + 1
assert f"{1000:,}" == "1,000" and len("1,000") == 5 and 1 + 3 == 4 and 4 + 1 == 5
assert [int("1314"[i]) for i in (0, 1, 3)] == [1, 3, 4] and [int("2335"[i]) for i in (0, 1, 3)] == [2, 3, 5] and [int("3336"[i]) for i in (0, 1, 3)] == [3, 3, 6]
assert ["1314"[2], "2335"[2], "3336"[2]] == ["1", "3", "3"]           # the third digit, rule missing

assert "1314"[2:] + "1314"[:2] == "1413"
assert (1 + 4, 1 + 3) == (5, 4) and 5 + 4 == 9 == sum(map(int, "1413"))
assert 4 - 3 == 1 and 1 + 1 + 1 == 3 and "1413".count("1") == 2
assert 1 + 4 + 1 + 3 == 9 and 141 + 3 == 144 == 12 * 12 and 1 + 4 + 4 == 9 and str(141) == str(141)[::-1]

assert factorint(1314) == {2: 1, 3: 2, 73: 1} and factorint(1413) == {3: 2, 157: 1} and factorint(2335) == {5: 1, 467: 1}
assert factorint(3336) == {2: 3, 3: 1, 139: 1} and factorint(111000) == {2: 3, 3: 1, 5: 3, 37: 1} and factorint(141) == {3: 1, 47: 1}
assert 1314 + 1413 == 2727 == 27 * 101 and 1413 - 1314 == 99 and 10001 == 73 * 137
assert [n % 37 for n in (1314, 1413, 2335, 3336, 111000, 141, 144, 2727, 99)] == [19, 7, 4, 6, 0, 30, 33, 26, 25]

if __name__ == "__main__":
    print("#372: 1+1, 2+2, 3+3; 111,000 = 1000 x 111 = 111 x 1000; 1+3=4, 2+3=5, 3+3=6 around the comma; 1314 -> 1413; 5+4=9; 141+3=144")
