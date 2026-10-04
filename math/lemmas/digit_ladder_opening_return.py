# CLASS: LEMMA
"""
Owner's reading of the right-extended ladder (2026-10-04):
    12-9=3+9=12+9=21
    1+2=3+9=12+9=21
  Row 1 flips the number (-9 +9): opens 12, ends 21.
  Row 2: the same 23 on both ends, not flipped.
  Row 3: 34 and 25, not the same, separated by 9: 25+9 = 34.
  Prediction: "it goes by 0,000 at 4".
Builds on digit_ladder_right_extension.py and digit_ladder_all_angles.py.

THE CHAIN: each row runs middle -> +9 -> +9 -> ...:
    row 1: 3, 12, 21, 30        row 3: 7, 16, 25, 34, 43
    row 2: 5, 14, 23, 32        row 4: 9, 18, 27, 36, 45, 54
The opening pair O = a,a+1 (12, 23, 34, 45) is 11a+1 = (2a+1) + 9a, so it sits
in the chain at step a. The new piece T = 2a+19 sits at step 2. So
    O - T = 9(a-2):  -9, 0, +9, +18
  row 1: O one step BEFORE T  (12 -> 21, the flip, -9+9)
  row 2: O = T                 (23 on both ends)
  row 3: O one step AFTER T    (25 + 9 = 34)
  row 4: O two steps after T   (27 -> 36 -> 45)
The opening moves one step further right each row.

THE FLIP: O + 9 is always O's reversal, because its digits are consecutive:
10b+(b+1)+9 = 10(b+1)+b. So the flip sits one step after the opening, every
row 1-8: 12->21, 23->32, 34->43, 45->54, ..., 89->98. In row 1 that step is T.

PREDICTION "0,000 at 4" -- confirmed: every piece of the chain is congruent to
2a+1 mod 9, and 2*4+1 = 9, so row 4's chain is 9, 18, 27, 36, 45, 54, ... --
every step is 0 mod 9. Row 4 is the only row of 1..9 where that happens (next:
rows 13, 22, ..., a = 4 mod 9). Its own digits fit: 45918-27 = 4+5 = 9, 9+9 = 18,
18+9 = 27; the row is 9 x 5102 and 4591827 = 9 x 510203.

ROW 9 BREAKS the pattern: its opening is 9,DR(10) = 91, not 11*9+1 = 100; 91
sits at step 8, and its flip 19 is the unreduced middle (step 0).

FALSIFICATION: any assertion below failing.
"""
def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9

def chain(a, k):
    return [2 * a + 1 + 9 * j for j in range(k)]

def opening(a):
    return int(f"{a}{dr(a + 1)}")

assert chain(1, 4) == [3, 12, 21, 30] and 12 - 9 == 3 and 1 + 2 == 3
assert chain(4, 6) == [9, 18, 27, 36, 45, 54]
for a in range(1, 9):
    c = chain(a, a + 3)
    O, T = opening(a), 2 * a + 19
    assert O == 11 * a + 1 and c[a] == O and c[2] == T
    assert O - T == 9 * (a - 2)
    assert c[a + 1] == int(str(O)[::-1])
assert [opening(a) - (2 * a + 19) for a in (1, 2, 3, 4)] == [-9, 0, 9, 18]
assert opening(1) + 9 == 21 == int("12"[::-1])
assert opening(2) == 23 == 2 * 2 + 19
assert 25 + 9 == 34 == opening(3)

for a in range(1, 200):
    zero = all(x % 9 == 0 for x in chain(a, 20))
    assert zero == (a % 9 == 4)
assert [a for a in range(1, 10) if all(x % 9 == 0 for x in chain(a, 10))] == [4]
assert 45918 == 9 * 5102 and 4591827 == 9 * 510203

assert opening(9) == 91 and chain(9, 9)[8] == 91 and chain(9, 1)[0] == 19

if __name__ == "__main__":
    for a in range(1, 5):
        print(a, chain(a, a + 3), "O", opening(a), "T", 2 * a + 19, "O-T", opening(a) - 2 * a - 19)
    print("all assertions pass")
