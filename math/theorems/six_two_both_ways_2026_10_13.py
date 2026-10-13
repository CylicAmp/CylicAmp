# CLASS: AUDIT
"""
6 and 2 both ways round (owner_work #262, 2026-10-13).

THE OWNER'S LINES, verbatim:
    6+2=8
    6+2=12
    6÷2
    2÷6
    6-2=-4
    2-6=4+(-4)=0
    
    264 is on the 246 rotation 
    
    2% of 6
    6% of 2
    
    
    2--3--7--2
    8-12-16-20

CHECKED
  6+2 = 8: holds.
  6+2 = 12: not as written. Holds as 6x2 = 12, or as 8 written in base 6 (12 in base 6 = 8).
    Open: which one was meant.
  6/2 = 3 and 2/6 = 1/3: the same pair, reciprocal.
  6-2 = -4 and 2-6 = 4: the signs are swapped -- 6-2 = 4, 2-6 = -4. 4 + (-4) = 0 holds either way.
  "264 is on the 246 rotation": 264 is one of the six orderings of 246, but not on 246's own
    rotation cycle 246 -> 462 -> 624 (SEED). It is on the reversed cycle 642 -> 426 -> 264
    (CAS_EXT, the opposite orbit -- owner_work/drip_cycle.md).
  2% of 6 = 6% of 2 = 0.12 (3/25): always equal, since x% of y = xy/100 = y% of x. 0.12 -> 12 again.
  8-12-16-20 steps by 4; digital roots 8, 3, 7, 2. The row 2--3--7--2 matches them at 3, 7, 2;
    8's root is 8. Open: what the first 2 is.

FRAMEWORKS: 264 -> 5 CAS_EXT; 246 -> 24 SEED; 8 TESLA; 12 and 16 both SA_ST_A {9,12,16}; 20 DARK_A;
  3 and 4 C3; 7 D7; 2 DARK_A.

FALSIFICATION: any assertion failing.
"""
from fractions import Fraction as F

dr = lambda v: 0 if v == 0 else 1 + (v - 1) % 9
rot = lambda s: [s[i:] + s[:i] for i in range(len(s))]
assert 6 + 2 == 8 and 6 * 2 == 12 and int("12", 6) == 8 and 6 + 2 != 12
assert F(6, 2) == 3 and F(2, 6) == F(1, 3) and F(6, 2) * F(2, 6) == 1
assert 6 - 2 == 4 and 2 - 6 == -4 and 4 + (-4) == 0
assert "264" not in rot("246") and "264" in rot("642") and sorted("264") == sorted("246")
assert 246 % 37 == 24 and 264 % 37 == 5
assert F(2, 100) * 6 == F(6, 100) * 2 == F(12, 100)
assert [12 - 8, 16 - 12, 20 - 16] == [4, 4, 4] and [dr(v) for v in (8, 12, 16, 20)] == [8, 3, 7, 2]
assert 12 % 37 in {9, 12, 16} and 16 % 37 in {9, 12, 16}

if __name__ == "__main__":
    print("6+2=8; 6x2=12 (or 12 base 6 = 8); signs swapped in the subtractions; 264 on 642's cycle; 2% of 6 = 6% of 2")
