# CLASS: LEMMA
"""
The prime row run on the ladder rows (owner, 2026-10-05).
The prime row (rotation_grids_x.py): digital roots of the first nine primes,
2357 (1|1) 4815 -- left block, the seam 11 split 1|1, right block. Its steps:
total (37), halves at the seam (18 | 19), the left block as two pairs
(23+57 = 80 -> 8), and the blocks stacked (2357 over 4815 -> 6263, first
column 2, 4, 6).

APPLIED to each nine-digit ladder row (ladder_x_grid.py): left block = digits
1-4, seam = digit 5 (the centre), right block = digits 6-9.
    row  blocks          total  halves   left pairs        right pairs      stacked
     1   1231 (2) 2130    15    9 | 8    12+31 = 43 -> 7   21+30 = 51 -> 6  3361
     2   2351 (4) 2332    25   15 | 14   23+51 = 74 -> 2   23+32 = 55 -> 1  4683
     3   3471 (6) 2534    35   21 | 20   34+71 = 105 -> 6  25+34 = 59 -> 5  5915
     4   4591 (8) 2736    45   27 | 26   45+91 = 136 -> 1  27+36 = 63 -> 9  6337
     5   5622 (0) 2938    37   15 | 22   56+22 = 78 -> 6   29+38 = 67 -> 4  7651
     6   6742 (2) 3140    29   21 | 10   67+42 = 109 -> 1  31+40 = 71 -> 8  9882
     7   7862 (4) 3342    39   27 | 16   78+62 = 140 -> 5  33+42 = 75 -> 3  1214
     8   8982 (6) 3544    49   33 | 22   89+82 = 171 -> 9  35+44 = 79 -> 7  2536
     9   9112 (8) 3746    41   21 | 28   91+12 = 103 -> 4  37+46 = 83 -> 2  3858
  ROW 5 TOTALS 37, the same as the prime row (the only one of rows 1-9).
  Totals reduce to a + 5 (forced, ladder_x_grid.py).
  The stacked blocks' first column reads 123, 224, 325, 426, 527, 639, 731,
  832, 933 (left digit, right digit, their root); the prime row's read 246.
  Row 8's is 832, the owner's chain number -- one match found by looking.

FRAME AND INSIDE (owner, 2026-10-05: "2)357(2)481(5 / 2+2 = 4+5 = 9 / 357 over
  481: 7+4 = 11+8 = 1+9 = 1"): the prime row's two ends and seam are the frame,
  2 + 2 + 5 = 9; the inner blocks 357 over 481 add by column to 7, 13 -> 4, 8,
  and 7 + 4 + 8 = 19 -> 10 -> 1. The frame (9) and the inside (28) make 37.
  On a ladder row the frame is digits 1, 5, 9 and the inside is 234 over 678.

ROWS 1-36 (owner: "keep going to row 36"): totals of the nine-digit rows 1-35
  are in TOT35. Row 5 is the ONLY row that totals 37.
  THE STARRED STEP (owner: "... = 1+9* = 1"): the inside's root plus the frame's
  root gives the whole row's root -- 1 + 9 = 10 -> 1 for the prime row (37). On
  the ladder rows frame + inside reduces to a + 5 every time (forced). Frame and
  inside have the SAME root only in rows 1, 2, 3, 4 and 25 (3|3, 8|8, 4|4, 9|9,
  6|6); the prime row's are 9 and 1. Row 36 split like the prime row at a
  two-digit seam, 9118 (2|9) 1100: frame 20 -> 2, inside columns 2, 2, 8 -> 3,
  together 5 = 32 -> 5. Frame + inside always
  equals the total (forced). Row 36, 9118291100, has ten digits (total 32).

BLOCK ROOTS AND THE (11) (owner, 2026-10-05):
    357 = 3+5 = 8+7 = 1+5 = 6;  481 = 4+8 = 12+1 = 1+3 = 4
    7+4 = 11+8 = 1+9 = (1)+6 = 7+4 = (11)
    753 -> 6;  184 -> 4  (reversals keep the root)
  The inner columns' root always equals the root of the two blocks' roots
  together (the columns hold the same digits), so (1) + 6 + 4 doubles them:
  2 x (6 + 4) -> 2, written 11. For the prime row that is the (11) -- the
  prime in its seam.
  On the ladder rows (inner blocks = digits 2-4 and 6-8) the same three
  numbers, column root + top root + bottom root, are in BLOCKS below; none
  of rows 1-35 gives exactly 11. Row 36 at its two-digit seam: 118 / 110,
  roots 1 and 2, columns 3, total 3+1+2 = 6.

FALSIFICATION: any assertion below failing.
"""
def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9

def row9(a):
    return "".join(map(str, [dr(a), dr(a + 1), dr(2 * a + 1)] + [2 * a + 1 + 9 * j for j in range(1, 4)]))

PRIME = [2, 3, 5, 7, 1, 1, 4, 8, 1, 5]
assert sum(PRIME) == 37 and (sum(PRIME[:5]), sum(PRIME[5:])) == (18, 19)
assert [dr(x + y) for x, y in zip([2, 3, 5, 7], [4, 8, 1, 5])] == [6, 2, 6, 3]

TOT, HALF, LP, RP, ST = [], [], [], [], []
for a in range(1, 10):
    d = list(map(int, row9(a)))
    L, c, R = d[:4], d[4], d[5:]
    TOT.append(sum(d))
    HALF.append((sum(L) + c, c + sum(R)))
    LP.append(10 * L[0] + L[1] + 10 * L[2] + L[3])
    RP.append(10 * R[0] + R[1] + 10 * R[2] + R[3])
    ST.append("".join(str(dr(x + y)) for x, y in zip(L, R)))
assert TOT == [15, 25, 35, 45, 37, 29, 39, 49, 41] and [a for a in range(1, 10) if TOT[a - 1] == 37] == [5]
assert all(dr(TOT[a - 1]) == dr(a + 5) for a in range(1, 10))
assert HALF == [(9, 8), (15, 14), (21, 20), (27, 26), (15, 22), (21, 10), (27, 16), (33, 22), (21, 28)]
assert LP == [43, 74, 105, 136, 78, 109, 140, 171, 103] and RP == [51, 55, 59, 63, 67, 71, 75, 79, 83]
assert ST == ["3361", "4683", "5915", "6337", "7651", "9882", "1214", "2536", "3858"]
FIRST = [row9(a)[0] + row9(a)[5] + ST[a - 1][0] for a in range(1, 10)]
assert FIRST == ["123", "224", "325", "426", "527", "639", "731", "832", "933"]

assert 2 + 2 + 5 == 9 and [dr(x + y) for x, y in zip([3, 5, 7], [4, 8, 1])] == [7, 4, 8]
assert dr(7 + 4 + 8) == 1 and 7 + 4 + 8 == 19 and 3 + 5 + 7 + 4 + 8 + 1 == 28 and 9 + 28 == 37
TOT35 = [sum(map(int, row9(a))) for a in range(1, 36)]
assert all(len(row9(a)) == 9 for a in range(1, 36)) and len(row9(36)) == 10 and sum(map(int, row9(36))) == 32
assert [a for a in range(1, 36) if TOT35[a - 1] == 37] == [5]
for a in range(1, 36):
    d = list(map(int, row9(a)))
    frame, inside = d[0] + d[4] + d[8], d[1] + d[2] + d[3] + d[5] + d[6] + d[7]
    assert frame + inside == TOT35[a - 1]
    assert dr(sum(dr(x + y) for x, y in zip(d[1:4], d[5:8]))) == dr(inside)

EQ = []
for a in range(1, 36):
    d = list(map(int, row9(a)))
    f = dr(d[0] + d[4] + d[8])
    i = dr(sum(dr(x + y) for x, y in zip(d[1:4], d[5:8])))
    assert dr(f + i) == dr(a + 5)
    if f == i:
        EQ.append(a)
assert EQ == [1, 2, 3, 4, 25] and dr(1 + 9) == dr(37) == 1
assert dr(9 + 2 + 9 + 0) == 2 and [dr(int(x) + int(y)) for x, y in zip("118", "110")] == [2, 2, 8] and dr(2 + 3) == dr(32)

assert dr(3 + 5 + 7) == 6 == dr(7 + 5 + 3) and dr(4 + 8 + 1) == 4 == dr(1 + 8 + 4)
assert dr(7 + 4 + 8) + 6 + 4 == 11
BLOCKS = []
for a in range(1, 36):
    r = row9(a)
    top, bot = r[1:4], r[5:8]
    rt, rb = dr(sum(map(int, top))), dr(sum(map(int, bot)))
    rc = dr(sum(dr(int(x) + int(y)) for x, y in zip(top, bot)))
    assert rc == dr(rt + rb) and dr(sum(map(int, top[::-1]))) == rt
    BLOCKS.append(rc + rt + rb)
    assert dr(BLOCKS[-1]) == dr(2 * (rt + rb))
assert 11 not in BLOCKS
assert dr(1 + 1 + 8) == 1 and dr(1 + 1 + 0) == 2 and dr(sum(dr(int(x) + int(y)) for x, y in zip("118", "110"))) == 3

if __name__ == "__main__":
    print("totals", TOT)
    print("all assertions pass")
