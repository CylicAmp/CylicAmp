# CLASS: AUDIT
"""
The owner's chains of 2026-10-18 (owner_work #326): decoded and checked. The owner's lines are first; the readings are mine.

THE OWNER'S LINES, verbatim (the same block is in owner_work/messages/2026-10-18.txt):
    41=4+1=5 / 66=1+2=3 / 1+7+5+3+8=(2+4=6)poly
    135=9 / 246=12 / 789=24 / 12+24=(3+6=(9)+(9)=1+8=(9)
    231=6 / 457=1+7=8 / 689=(2+3=5***)
    (235+11=246) / 246÷2=123÷2=
    23.5=23+5=2+8=1 / 24.6=24+6=3+0=3 / 47.11=1+3=4 / 3n+1=4+4=8= (44222211111111)
    235+11 / 246+2+11=4(3+1) / 248 / 257
    257=5 / 431=8 / 689=5 / 378=36+9=45+3=4+8=1+(2=3+2=5)
    23=5 / 25=7 / 48=24+5=29+2=(3+1=4)

WHAT HOLDS (each "=" step is arithmetic or a digital root):
  41, 66 and 1+7+5+3+8 = 24 -> 6; 135 = 9, 246 = 12, 789 = 24; 12 + 24 = 36 -> 9, 9 + 9 = 18 -> 9 (the bracket is unbalanced: typo);
  231 = 6; 689 = 23 -> 5; 235 + 11 = 246; 246 / 2 = 123 (123 / 2 = 61.5, left open);
  decimals: the point is dropped, 23.5 -> 10 -> 1, 24.6 -> 12 -> 3, 47.11 -> 13 -> 4, and 1 + 3 = 4 (23.5 + 24.6 = 48.1, root 4 too);
  3n + 1 with n = 1 is 4, 4 + 4 = 8, and 8 is the owner's halving string 44|2222|11111111 of #263 (14 digits, digit sum 24);
  246 + 2 = 248 and 246 + 11 = 257, both root 5; 257 = 5, 431 = 8, 689 = 5, and 257 + 431 + 1 = 689: the owner's +1 "to begin again" (#264),
  roots 5 + 8 = 13 -> 4, +1 = 5;
  23 = 5, 25 = 7, 23 + 25 = 48 = 2 x 24, 24 + 5 = 29, 29 + 2 = 31, 3 + 1 = 4: the walk goes 24 -> 29 -> 31, and 29, 31 are a twin prime pair
  (with 2 = 7 - 5, so the walk is 24 + 5 then + (7 - 5), ending at 24 + 7 = 31).
  235 = 5 x 47, so 47 in 47.11 is 235 / 5 and the .11 is the 11 of 235 + 11 = 246; roots 235 -> 1, 11 -> 2, 246 -> 3 = 1 + 2.

WHAT DOES NOT HOLD AS WRITTEN (reported, not argued):
  457 = 1+7 = 8: 4+5+7 = 16 -> 1+6 = 7; the line ends in 8 = 7 + 1 (the +1 rule), or "1+7" is a typo for "1+6".
  246+2+11 = 4(3+1): the sum is 259 (root 7); 4 = 3 + 1 is 246's root plus 1; the line does not say which.
  378 = 36+9 = 45+3 = 48 -> 12 -> 3, +2 = 5: each step is arithmetic; where 36, 9, 3 and 2 come from is not stated (378 has digit sum 18
  = 2 x 9 and 36 = 2 x 18). "poly" after the first block is the owner's word and is not defined in the record.

FRAMEWORKS (gf37-audit): 41 C3; 66 C9; 135 SEED; 246 SEED; 789 SA_ST_A; 231 SA_ST_A; 457 CAS_EXT; 689 TESLA; 235 CAS_EXT; 248 IC; 257 NQR17;
  431 SEED; 378 TESLA.
FALSIFICATION: any assertion failing.
"""
from sympy import factorint, isprime


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


def ds(n):
    return sum(int(c) for c in str(n) if c.isdigit())


assert dr(41) == 5 and dr(66) == 3 and 1 + 7 + 5 + 3 + 8 == 24 and dr(24) == 6
assert (ds(135), ds(246), ds(789)) == (9, 12, 24) and 12 + 24 == 36 and dr(36) == 9 and 9 + 9 == 18 and dr(18) == 9
assert ds(231) == 6 and ds(689) == 23 and dr(689) == 5 and 235 + 11 == 246 and 246 // 2 == 123 and 123 / 2 == 61.5
assert [dr(ds(x)) for x in ("23.5", "24.6", "47.11")] == [1, 3, 4] and 23 + 5 == 28 and 24 + 6 == 30 and abs(23.5 + 24.6 - 48.1) < 1e-9 and dr(48 + 1) == 4
assert 3 * 1 + 1 == 4 and 4 + 4 == 8 and "44" + "2222" + "1" * 8 == "44222211111111" and len("44222211111111") == 14 and ds(44222211111111) == 24
assert 246 + 2 == 248 and 246 + 11 == 257 and dr(248) == dr(257) == 5 and (dr(257), dr(431), dr(689)) == (5, 8, 5)
assert 257 + 431 + 1 == 689 and dr(dr(257) + dr(431)) == 4 and dr(257 + 431) == 4 and dr(689) == 5
assert (dr(23), dr(25)) == (5, 7) and 23 + 25 == 48 == 2 * 24 and 24 + 5 == 29 and 29 + 2 == 31 and 2 == 7 - 5 and 24 + 7 == 31 and dr(31) == 4
assert isprime(29) and isprime(31) and factorint(235) == {5: 1, 47: 1} and 235 // 5 == 47 and (dr(235), dr(11), dr(246)) == (1, 2, 3)
# what does not hold as written
assert ds(457) == 16 and dr(457) == 7 and dr(457) + 1 == 8 and 1 + 7 == 8 and 1 + 6 == 7
assert 246 + 2 + 11 == 259 and dr(259) == 7 and dr(246) + 1 == 4
assert 36 + 9 == 45 and 45 + 3 == 48 and dr(48) == 3 and 3 + 2 == 5 and ds(378) == 18 and 2 * ds(378) == 36
assert [n % 37 for n in (41, 66, 135, 246, 789, 231, 457, 689, 235, 248, 257, 431, 378)] == [4, 29, 24, 24, 12, 9, 13, 23, 13, 26, 35, 24, 8]

if __name__ == "__main__":
    print("owner chains of 2026-10-18 hold except 457 = 1+7 = 8 (digit root 7) and 246+2+11 = 4(3+1); 257 + 431 + 1 = 689; the 48 walk is 24, 29, 31")
