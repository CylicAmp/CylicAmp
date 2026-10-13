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

FOLLOW-UP (owner_work #260), verbatim:
    1---------------2-----3
    4|5
    7|8|9
    3+4=7+9=7+2=9+3=1+2=3

  The chain is a running digital root: 3+4 = 7; 7+9 = 16 -> 7 (adding 9 never changes a root);
  7+2 = 9; 9+3 = 12 -> 1+2 = 3. Its addends 3, 4, 9, 2, 3 sum to 21 -> 3, the chain's end.
  The grid: row 2 is 4|5 -- the 6 is gone (in #259 it stood split off as 45|6 and became 6+2 = 8);
  without it the grid totals 45 - 6 = 39 -> 3. The top row has 15 dashes between 1 and 2 and
  5 between 2 and 3.

FOLLOW-UP 2 (owner_work #261), verbatim:
    1---------------2-----3
    4|5
    7|8|9
    3+4=7+9=7+2=9+3=1+2=3
    
    159-7
    48-84
    7-951 
    
    
    block of 6×2=1+2=3

  The block reads the same backwards: 7-951 is 159-7 reversed, and 48-84 is its own reverse.
  "block of 6x2 = 1+2 = 3": it uses exactly six digits -- 1, 5, 9, 7, 4, 8 -- each exactly twice;
  6 x 2 = 12 -> 1+2 = 3. Left out: 2, 3, 6.
  Both mirrored pairs land on the opposite orbits NEG_H <-> IC:
    159 = 11 (NEG_H), 951 = 26 (IC); 159 + 951 = 1110 = 30 x 37 (forced: 1+9 = 10, middle 5);
    48 = 11 (NEG_H), 84 = 10 (IC); 84 + 26 x 48 = 1332 = 36 x 37 (forced: 8 = 2 x 4, as 24/42).
  159 and 48 share the residue 11 (159 - 48 = 111 = 3 x 37). 7 -> D7.

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

# follow-up: the running-root chain and the grid without 6
_dr = lambda v: 0 if v == 0 else 1 + (v - 1) % 9
_walk, _r = [], 0
for _a in (3, 4, 9, 2, 3):
    _r = _dr(_r + _a); _walk.append(_r)
assert _walk == [3, 7, 7, 9, 3] and 3 + 4 == 7 and _dr(7 + 9) == 7 and 7 + 2 == 9 and 9 + 3 == 12 and 1 + 2 == 3
assert sum((3, 4, 9, 2, 3)) == 21 and _dr(21) == 3 and sum(range(1, 10)) - 6 == 39 and _dr(39) == 3

# follow-up 2: the mirrored block
from collections import Counter as _C
_blk = ["159-7", "48-84", "7-951"]
assert _blk[2] == _blk[0][::-1] and _blk[1] == _blk[1][::-1]
_cnt = _C(ch for l in _blk for ch in l if ch.isdigit())
assert len(_cnt) == 6 and set(_cnt.values()) == {2} and set("123456789") - set(_cnt) == set("236")
assert 6 * 2 == 12 and 1 + 2 == 3
assert 159 % 37 == 48 % 37 == 11 and 951 % 37 == 26 and 84 % 37 == 10
assert 159 + 951 == 1110 == 30 * 37 and 84 + 26 * 48 == 1332 == 36 * 37 and 159 - 48 == 111

if __name__ == "__main__":
    print("all hold; 12321 SEAM; 12121 = 22222 = 22 mod 37; 23 over 6 with 6+2=8 = TESLA {6,8,23}; rows = 12 mod 37")
