# CLASS: AUDIT
"""
The pasted running sum on the digits of 1.137 x 1.137 = 1.292769 (owner_work #409, 2026-10-22).
Audit on arrival.

THE PASTE: text from another tool, relayed by the owner ("Look at what you just extracted from the
digits of the square ... Following your progressive running sum of these digits"). Nothing below
puts a claim of the paste in the owner's mouth.

PRIOR ART: owner_1125_1137_ones_by_zeros_2026_10_19.py (#368: 9 ÷ 2 ÷ 2 ÷ 2 = 1.125,
1.125 + 0.012 = 1.137); owner_0137_all_forms_count_2026_10_20.py (#380). No earlier record of
1.292769, of a "Vedic cross", or of 441 and 529 in owner_work/.

RIGHT (re-run):
  1137 x 1137 = 1292769, so 1.137 x 1.137 = 1.292769; the digits after the point are 2 9 2 7 6 9
  12 + 9 = 21 -> 21 + 2 = 23 -> 23 + 7 = 30 -> 30 + 6 = 36 -> 36 + 9 = 45 -> 4 + 5 = 9
  the steps 21 -> 23 -> 30 -> 36 -> 45 are +2 +7 +6 +9
  1 + 1 + 3 + 7 = 12 -> 1 + 2 = 3, and 3 x 3 = 9
  any number whose root is 3 has a square whose root is 9 (3k x 3k = 9 x k x k); 6 and 9 do too
  21 x 21 = 441, 23 x 23 = 529

WRONG:
  1. "Start with the lead 12 (or 1 + 2 = 3)": the two starts do not give the same ladder.
     The paste counts the lead 1 2 as the number twelve, so its ladder is 9 more than the digit
     sum all the way: it ends at 45, while the digits of 1292769 add to 36.
       start 12 (the paste)        12 21 23 30 36 45 -> 9
       start 3 (1 + 2)              3 12 14 21 27 36 -> 9
       digit by digit from 1     1  3 12 14 21 27 36 -> 9
     Both end on root 9, because 12 - 3 = 9. But 23, 30 and 45 come only from the start at 12,
     so "your running sum ladder hits ... 21, 23, 36, 45" is right only for that start.
  2. "The step sizes" are the digits themselves (2, 7, 6, 9): adding a digit steps by that digit.
     Right as arithmetic, and nothing more than the digits read again.

THE ONE LINE LEFT UNCHECKED: "21 and 23 ... are the exact base elements whose squares gave the
  Vedic cross differences from earlier". 21 x 21 = 441 and 23 x 23 = 529 are right; the link to the
  "Vedic cross differences" needs that earlier work, which is not in the paste or in owner_work/.

BOTH WAYS:
  the whole square 1292769 (with the lead 1):   1+2+9+2+7+6+9 = 36 -> 9
  the part after the point only (2 9 2 7 6 9):  2+9+2+7+6+9 = 35 -> 3+5 = 8
    running: 2 11 13 20 26 35 -> 8
  no zero in 1.292769, and the point changes nothing: 1.292769 and 1292769 have the same digits.

NEW LINES, owner's notation:
  1.137 x 1.137 = 1 + 0.137 + 0.137 + 0.137 x 0.137 = 1 + 0.274 + 0.018769 = 1.292769
    137 x 137 = 18769;  1137 x 1137 = 1000000 + 274000 + 18769 = 1292769
  1137 = 3 x 379 (379 prime), so 1292769 = 9 x 379 x 379
  roots: 1137 -> 3;  379 -> 3+7+9 = 19 -> 1;  1292769 -> 36 -> 9 = 3 x 3 x 1 x 1

RESIDUES mod 37 (gf37-audit): 1137 -> 27 NEG_H; 1292769 -> 26 IC (27 x 27 = 729 = 19 x 37 + 26);
  12 SA_ST_A, 21 SA_ST_B, 23 TESLA (prime: cousin with 19, Sophie Germain 47, safe from 11),
  30 C3, 36 NEG_H, 45 -> 8 TESLA, 441 -> 34 D7, 529 -> 11 NEG_H, 379 -> 9 SA_ST_A (prime).

FALSIFICATION: any assertion failing.
"""
from fractions import Fraction as F
from itertools import accumulate
from sympy import factorint, isprime


def root(n):
    while n > 9:
        n = sum(map(int, str(n)))
    return n


# --- RIGHT ---
assert 1137 * 1137 == 1292769 and F(1137, 1000) ** 2 == F(1292769, 1000000)
digits = [int(d) for d in str(1292769)]
after_point = digits[1:]
assert after_point == [2, 9, 2, 7, 6, 9]
ladder = list(accumulate([12] + after_point[1:]))
assert ladder == [12, 21, 23, 30, 36, 45] and root(45) == 9
assert [ladder[i + 1] - ladder[i] for i in range(1, 5)] == [2, 7, 6, 9] == after_point[2:]
assert 1 + 1 + 3 + 7 == 12 and root(1137) == 3 and 3 * 3 == 9 and root(1292769) == 9
assert all(root((3 * k) ** 2) == 9 for k in range(1, 3000))
assert all(root(n * n) == 9 for n in range(1, 3000) if root(n) in (3, 6, 9))
assert 21 * 21 == 441 and 23 * 23 == 529

# --- WRONG 1: the two starts ---
from_3 = list(accumulate([3] + after_point[1:]))
from_1 = list(accumulate(digits))
assert from_3 == [3, 12, 14, 21, 27, 36] and from_1 == [1, 3, 12, 14, 21, 27, 36]
assert all(a - b == 9 for a, b in zip(ladder, from_3)) and sum(digits) == 36 != 45
assert root(ladder[-1]) == root(from_3[-1]) == root(from_1[-1]) == 9
assert {23, 30, 45} & set(from_3 + from_1) == set()

# --- BOTH WAYS ---
assert sum(after_point) == 35 and root(35) == 8
assert list(accumulate(after_point)) == [2, 11, 13, 20, 26, 35]
assert "0" not in "1.292769" and "1.292769".replace(".", "") == "1292769"

# --- NEW LINES ---
assert F(1137, 1000) ** 2 == 1 + 2 * F(137, 1000) + F(137, 1000) ** 2 == 1 + F(274, 1000) + F(18769, 1000000)
assert 137 * 137 == 18769 and 1000000 + 274000 + 18769 == 1292769
assert factorint(1137) == {3: 1, 379: 1} and isprime(379) and factorint(1292769) == {3: 2, 379: 2}
assert root(379) == 1 and root(1292769) == root(3 * 3 * 1 * 1)

# --- RESIDUES mod 37 ---
assert [x % 37 for x in (1137, 1292769, 12, 21, 23, 30, 36, 45, 441, 529, 379)] == \
    [27, 26, 12, 21, 23, 30, 36, 8, 34, 11, 9]
assert 27 * 27 == 729 == 19 * 37 + 26
assert isprime(23) and isprime(47) and isprime(11) and isprime(19)

if __name__ == "__main__":
    print("1.137 x 1.137 = 1.292769 and the ladder 12 21 23 30 36 45 -> 9: right; starting at 3 gives "
          "3 12 14 21 27 36 -> 9, not the same ladder (23, 30, 45 only from 12); digit sum 36, after the point 35 -> 8; "
          "1.292769 = 1 + 0.274 + 0.018769")
