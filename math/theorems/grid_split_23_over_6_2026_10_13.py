# CLASS: AUDIT
"""
The owner's 1-9 grid split and the five-digit words (owner_work #259, 2026-10-13).

THE OWNER'S LINES, verbatim:
    (3x7=12 and 21)
    (1)2(3)2(1)
    (1)2(1)2(1)
    (2)2(2)2(2)=3 twos or 2 thress 
    
    1-23
    456
    789
    34
    2+6=8+9=(1+7=8)
    
    
    1---23
    456
    789
    346
    
    
    1---23
    45--6+2=8
    789
    346
    
    1---|23
    45--|6×2=1+2=(3+8=11)+45=5+6=11
    789
    346

EVERY EQUATION HOLDS
  3x7 = 21 (12 its reversal); 2+6 = 8; 8+9 = 17 -> 1+7 = 8; 6+2 = 8; 6x2 = 12 -> 1+2 = 3; 3+8 = 11;
  11+45 = 56 -> 5+6 = 11.  "3 twos or 2 threes": 3x2 = 2x3 = 6 (typo: "thress" for "threes").

THE FIVE-DIGIT WORDS (2s fixed in positions 2 and 4, the parenthesised digits around them)
  (1)2(3)2(1) = 12321 = 111^2 = 3^2 x 37^2 -> SEAM.  Prior art: T328, T330, T371; the ABCBA rule
                (a five-digit palindrome is SEAM exactly when C = A + B; here 3 = 1 + 2).
  (1)2(1)2(1) = 12121 = 17 x 23 x 31 -> 22 (NQR17).
  (2)2(2)2(2) = 22222 = 2 x 41 x 271 -> 22 (NQR17). 12121 and 22222 share the residue because
                their difference 10101 = 3 x 7 x 13 x 37.

THE GRID SPLIT
  1---|23 / 45--|6 puts 23 over 6 on the right -- the same "23/6" as in the owner's 0.25 lines
  (#255), here read as 23 stacked over 6. And 6, 8, 23 are exactly one 137-map orbit, TESLA
  {6, 8, 23} (6 -> 8 -> 23): the owner's 6+2 = 8 completes it. The left part 45 = 8 (mod 37) too.
  The rows 123, 456, 789 are all 12 (mod 37) -- the owner's 12 -- because they step by
  333 = 9 x 37 (T311's sub-grid difference).
  Open: 346 (and 34 in the first block) under the grid -- 346 = 2 x 173 -> 13 (CAS_EXT).

FRAMEWORKS (mod 37, orbit): 21 SA_ST_B; 12 SA_ST_A; 23 prime TESLA; 34 D7; 45 -> 8 TESLA;
  56 -> 19 CAS_EXT; 17 prime NQR17; 11 prime NEG_H; 8 TESLA.

FALSIFICATION: any assertion failing.
"""
from sympy import factorint, isprime

assert 3 * 7 == 21 and str(21)[::-1] == "12"
assert 2 + 6 == 8 and 8 + 9 == 17 and 1 + 7 == 8 and 6 + 2 == 8 and 6 * 2 == 12 and 1 + 2 == 3
assert 3 + 8 == 11 and 11 + 45 == 56 and 5 + 6 == 11 and 3 * 2 == 2 * 3 == 6
assert 12321 == 111 ** 2 == 9 * 37 ** 2 and 3 == 1 + 2
assert factorint(12121) == {17: 1, 23: 1, 31: 1} and factorint(22222) == {2: 1, 41: 1, 271: 1}
assert 12121 % 37 == 22222 % 37 == 22 and 22222 - 12121 == 10101 == 3 * 7 * 13 * 37
assert {6, 8, 23} == {6 * 26 ** k % 37 for k in range(3)} and 6 * 26 % 37 == 8 and 8 * 26 % 37 == 23
assert 45 % 37 == 8 and isprime(23)
assert 123 % 37 == 456 % 37 == 789 % 37 == 12 and 456 - 123 == 789 - 456 == 333 == 9 * 37
assert 346 == 2 * 173 and 346 % 37 == 13

if __name__ == "__main__":
    print("all hold; 12321 SEAM; 12121 = 22222 = 22 mod 37; 23 over 6 with 6+2=8 = TESLA {6,8,23}; rows = 12 mod 37")
