# CLASS: LEMMA
"""
Owner, 2026-10-04: "extend it to row 5 and keep going", with four lines:
  L1  1,1+1,1=4+11=6+11=8+11=10+11=1(2=(3+1)=1,111
  L2  2+2=4+2=6+2=8+2=10+2=1+2=3+1=1,111
  L3  11+11=22+11=33+11=44+11=55+11=6+6=1+2=3+(1=4)
  L4  22+11=33+11=44+11=55+11=6+6=1+(2=3)
Builds on digit_ladder_opening_return.py (opening O = 11a+1 at chain step a,
new piece T = 2a+19 at step 2, O - T = 9(a-2)).

PART 1 -- ROWS 5 ONWARD
  Rows 1-8 all obey O - T = 9(a-2) and the flip O+9 one step after O:
    row 5: chain 11,20,29,38,47,56,65   O=56 three steps after T=29, flip 65
    row 6: 13,...,31,...,67,76           O-T = 36, flip 76
    row 7: O-T = 45, flip 87             row 8: O-T = 54, flip 98
  Row 9 breaks: O = 91 (DR(10) = 1), at step 8 like row 8, O-T = 54 again.
  Past row 9 (first piece read as DR(a), so O repeats 12, 23, ..., 91):
    within each 9-row cycle O - T still rises by 9 per row, and across the
    break it drops by 81, so each cycle the whole pattern lands ONE ROW LATER:
      flip  (O+9 = T, row 1's 12 -> 21):     rows 1, 12, 23, 34
      same  (O = T, row 2's 23 ... 23):      rows 2, 13, 24, 35   (+ row 36, a row-9 break)
      +9    (T+9 = O, row 3's 25 + 9 = 34):  rows 3, 14, 25
    The three return every 11 rows, then stop: O - T loses 9 per cycle, so
    after row 35 it never reaches 0 again. Row 12 is 34734-43 (34 flips to 43),
    row 13 is 45936-45, row 14 is 56238-47 (47 + 9 = 56).
  (Reading the first piece literally instead, O = 102, 113, ..., 179 for rows
  10-17, each at chain step a-1, and nothing returns.)

PART 2 -- THE FOUR LINES: one walk, written four ways
  The walk is the repdigits 22, 33, 44, 55, 66 (L3 starts at 11):
    L3/L4 write the repdigits; 66 -> 6+6 = 12 -> 1+2 = 3.
    L1 writes their digit sums: 1,1+1,1 = 1+1+1+1 = 4 = digits of 22;
      4+11 -> 15 -> 6 (=33), 6+11 -> 17 -> 8 (=44), 8+11 -> 19 -> 10 (=55),
      10+11 = 21 -> 3 (=66 -> 12 -> 3).   Adding 11 then summing digits
      is adding 2 mod 9, because 11 = 9 + 2.
    L2 writes the same as +2: 2+2 = 4, 6, 8, 10 -> 1, 1+2 = 3.
  The closing "+1": L1, L2, L3 end 3+1 = 4. Repdigit aa plus 1 is row a's
  opening pair, O = 11a+1 (12 = 11+1, ..., 67 = 66+1). So 66 + 1 = 67, the
  opening of row 6 (67422), whose digit sum 13 -> 4 is row 6's middle piece.
  The walk 4, 6, 8, 1, 3 is the chain residue of rows 6, 7, 8, 9, 10.
  "1,111": four ones, 1+1+1+1 = 4, the value both L1 and L2 close on. Read as
  a tally; 1111 = 11*101 is the other reading and no line distinguishes them.
  L4 stops at 3 without the +1 (66, not 67).

FALSIFICATION: any assertion below failing.
"""
def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9

def ds(n):
    return sum(map(int, str(n)))

def O(a):
    return int(f"{dr(a)}{dr(a + 1)}")

def T(a):
    return 2 * a + 19

def chain(a, k):
    return [2 * a + 1 + 9 * j for j in range(k)]

for a in range(1, 9):
    c = chain(a, a + 3)
    assert c[a] == O(a) == 11 * a + 1 and c[2] == T(a) and O(a) - T(a) == 9 * (a - 2)
    assert c[a + 1] == int(str(O(a))[::-1])
assert chain(5, 7) == [11, 20, 29, 38, 47, 56, 65]
assert O(9) == 91 and chain(9, 9)[8] == 91 and O(9) - T(9) == 54 == O(8) - T(8)

gaps = [O(a) - T(a) for a in range(1, 30)]
assert gaps[:9] == [-9, 0, 9, 18, 27, 36, 45, 54, 54]
assert gaps[9:18] == [-27, -18, -9, 0, 9, 18, 27, 36, 36]
flip = [a for a in range(1, 500) if int(str(O(a))[::-1]) == T(a)]
same = [a for a in range(1, 500) if O(a) == T(a)]
plus9 = [a for a in range(1, 500) if T(a) + 9 == O(a)]
assert flip == [1, 12, 23, 34] and same == [2, 13, 24, 35, 36] and plus9 == [3, 14, 25]
assert O(36) == 91 == T(36)
assert (O(12), T(12)) == (34, 43) and (O(13), T(13)) == (45, 45) and T(14) + 9 == O(14) == 56

assert 1 + 1 + 1 + 1 == 4 == ds(22)
w, L1 = 4, [4]
for _ in range(4):
    w = ds(w + 11)
    L1.append(w)
assert L1 == [4, 6, 8, 10, 3]
assert [ds(11 * k) for k in (2, 3, 4, 5)] == [4, 6, 8, 10] and ds(66) == 12 and ds(12) == 3
assert all(dr(x + 11) == dr(x + 2) for x in range(1, 1000))
assert [dr(x) for x in (4, 6, 8, 10, 12)] == [4, 6, 8, 1, 3]
assert all(11 * a + 1 == int(f"{a}{a + 1}") for a in range(1, 9))
assert 66 + 1 == 67 == O(6) and dr(67) == 4 == dr(2 * 6 + 1)
assert [(2 * a + 1) % 9 for a in (6, 7, 8, 9, 10)] == [4, 6, 8, 1, 3]

if __name__ == "__main__":
    for a in range(5, 15):
        print(a, "O", O(a), "T", T(a), "O-T", O(a) - T(a))
    print("flip", flip, "same", same, "+9", plus9)
    print("all assertions pass")
