# CLASS: LEMMA
"""
Owner's lines on 1413 and the reversal pairs (2026-10-04):
    1413
    43+11=5+4=9
    42-3=3+9=1+2=3
    2+8=1+2=3
    14=5+1==6
    41=5+4==9
    8+2=1+8=9
    41/14  13/31  31/13  33/44
Builds on reversal_spans_supplied_audit_2026_10_04.py (1413 splits, the pairs
14/41, 13/31, 12/21 and doublings 28, 82).

DECODED -- the rule ab -> (a+b) + a = 2a + b, the digit sum plus the first digit:
    14 -> 5+1 = 6        41 -> 5+4 = 9
    28 -> 10+2 = 12 -> 1+2 = 3        82 -> 10+8 = 18 -> 1+8 = 9
  The lines write the intermediate 12 and 18 as "1+2" and "1+8", so the
  unreduced 2a+b fits every line. 28 = 2 x 14 and 82 = 2 x 41.
  For a reversal pair: (2a+b) + (2b+a) = 3(a+b), and (2a+b) - (2b+a) = a-b:
    14, 41 -> 6, 9 (sum 15 = 3 x 5);  13, 31 -> 5, 7 (sum 12 = 3 x 4);
    12, 21 -> 4, 5 (sum 9 = 3 x 3).

1413, 43+11 = 54 -> 5+4 = 9: 11 is 1413's 1st and 3rd digits, 43 its 2nd and
  4th. Any regrouping of a number's digits into new numbers keeps the value
  mod 9, so 11 + 43 reduces to 9 like every split of 1413. (54 is 45 reversed.)

42-3 = 39 -> 3+9 = 12 -> 1+2 = 3: arithmetic correct. One reading from 1413:
  1 | 41 | 3 with the last part subtracted, 1 + 41 - 3 = 39. Flipping the sign
  of a part moves the total by twice that part, so 9 - 2 x 3 = 3 mod 9. 39 is
  the number of the zero carrying ladder row 4. (Whether 42 and 3 come from
  1+41 and 3 is the owner's to confirm.)

33 / 44: the sums of the reversal pairs, 12+21 = 33 and 13+31 = 44 (and
  14+41 = 55): ab + ba = 11(a+b).

SECOND PAGE (owner, 2026-10-04): the first block again in reverse order
    8+2=1+8=9, 41=5+4=9, 14=5+1=6, 2+8=1+2=3     (82, 41, 14, 28 -> 9, 9, 6, 3)
and a new block that takes one more step -- digit sum, + first digit,
+ second digit = 2(a+b):
    26 = 8+2 = 10, +6 = 16 -> 1+6 = 7
    13 = 4+1 = 5,  +3 = 8
    31 = 4+3 = 7,  +1 = 8
    62 = 8+6 = 14 -> 1+4 = 5, +2 = 7
  The full rule 2(a+b) is the same for a number and its reversal, so 13 and 31
  both give 8, and 26 and 62 both give 16 -> 7. Stopping after the first digit
  (2a+b, page one) is not symmetric: 14 -> 6 but 41 -> 9.
  2(a+b) = 2(ab + ba)/11: 13+31 = 44 -> 8, 26+62 = 88 -> 16, 12+21 = 33 -> 6.
  26 = 2 x 13 and 62 = 2 x 31; 2(a+b) = 2n mod 9, so doubling the number
  doubles the result mod 9: 8 -> 16 -> 7.

THE 26, 13, 31, 62 BLOCK, INSIDE AND OUTSIDE (owner, 2026-10-04: "look closely
at row 3 ... in the middle is 44 outside 88"):
    inside  13 + 31 = 44,  digit sums 4, 4:  4+4 = 8
    outside 26 + 62 = 88,  digit sums 8, 8:  8+8 = 16 -> 7
  Outside = 2 x inside, since 26 = 2 x 13 and 62 = 2 x 31 (forced).
  Crosses: 62 + 13 = 75 -> 7+5 = 12 -> 1+2 = 3, and 26 + 31 = 57 -> 3.
    75 and 57 are reversals of each other (no carries, so reversing the
    addends reverses the sum). Digit sums agree: (1+3) + (6+2) = 4 + 8 = 12 -> 3.
  The two crosses: 3 + 3 = 6. The whole block: 44 + 88 = 132 -> 6, the same
  as 8 + 7 = 15 -> 6. ("3+3+6" read as 3 + 3 -> 6.)

LADDER ROW 3, 34716-25 (owner: "run it on ladder row 3"):
  Pieces 3 | 4 | 7 | 16 | 25; 3+4 = 7, the middle. Chain 7, 16, 25, 34, 43, 52
  (digit_ladder_opening_return.py): every piece has digit sum 7, so the
  three-step rule 2(a+b) gives 14 -> 5 on every one of them; the two-step
  2a+b differs: 34 -> 10 -> 1, 43 -> 11 -> 2, 16 -> 8, 25 -> 9.
  Block built like 26, 13, 31, 62 from the opening 34, its reversal 43 and
  their doubles 68, 86:
    inside  34 + 43 = 77,  digit sums 7, 7:    7+7 = 14 -> 5
    outside 68 + 86 = 154, digit sums 14, 14:  14+14 = 28 -> 1
    crosses 86 + 34 = 120 -> 3,  68 + 43 = 111 -> 3   (carries, so not reversals)
    block   77 + 154 = 231 -> 6 = 3 + 3
  The same 3, 3, 6 as the 13/31 block. Forced: each cross is ab + 2ba (or
  2ab + ba) = 3(a+b) mod 9, and the block is 33(a+b) = 6(a+b) mod 9, so only
  (a+b) mod 3 matters -- 1+3 = 4 and 3+4 = 7 both leave 1. Over the nine
  ladder rows: rows 3, 6, 9 give 3, 3, 6; rows 2, 5, 8 give 6, 6, 3;
  rows 1, 4, 7 give 9, 9, 9.
  Inside row 3's own chain, 16, 25, 34, 43: outside 16+43 = inside 25+34 = 59,
  forced because the chain steps by 9 (any four in a row: ends sum = middles sum).

FALSIFICATION: any assertion below failing.
"""
def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9

def rule(n):
    a, b = divmod(n, 10)
    return (a + b) + a

assert [rule(n) for n in (14, 41, 28, 82)] == [6, 9, 12, 18]
assert (1 + 4) + 1 == 6 and (4 + 1) + 4 == 9 and (2 + 8) + 2 == 12 and (8 + 2) + 8 == 18
assert dr(12) == 1 + 2 == 3 and dr(18) == 1 + 8 == 9
assert 28 == 2 * 14 and 82 == 2 * 41
for n in range(10, 100):
    a, b = divmod(n, 10)
    m = 10 * b + a
    assert rule(n) + rule(m) == 3 * (a + b) and rule(n) - rule(m) == a - b
assert [(rule(n), rule(int(str(n)[::-1]))) for n in (14, 13, 12)] == [(6, 9), (5, 7), (4, 5)]

assert ("1413"[0::2], "1413"[1::2]) == ("11", "43") and 11 + 43 == 54 and dr(54) == 9
assert 1 + 41 - 3 == 42 - 3 == 39 and dr(39) == 3 and (1 + 4 + 1 + 3) - 2 * 3 == 3
assert (12 + 21, 13 + 31, 14 + 41) == (33, 44, 55)

def rule2(n):
    a, b = divmod(n, 10)
    return (a + b) + a + b

assert [rule(n) for n in (82, 41, 14, 28)] == [18, 9, 6, 12]
assert [rule2(n) for n in (26, 13, 31, 62)] == [16, 8, 8, 16] and dr(16) == 7
assert (2 + 6) + 2 == 10 and 10 + 6 == 16 and (6 + 2) + 6 == 14 and dr(14) + 2 == 7
assert (1 + 3) + 1 + 3 == 8 and (3 + 1) + 3 + 1 == 8
for n in range(10, 100):
    m = int(str(n)[::-1]) if n % 10 else n // 10
    assert rule2(n) == 2 * sum(map(int, str(n))) and rule2(n) % 9 == 2 * n % 9
    if n % 10:
        assert rule2(n) == rule2(m) == 2 * (n + m) // 11
assert (13 + 31, 26 + 62, 12 + 21) == (44, 88, 33) and 26 == 2 * 13 and 62 == 2 * 31

def ds(n):
    return sum(map(int, str(n)))

assert (13 + 31, 26 + 62) == (44, 88) and 88 == 2 * 44
assert [ds(n) for n in (13, 31, 26, 62)] == [4, 4, 8, 8] and dr(8 + 8) == 7
assert (62 + 13, 26 + 31) == (75, 57) and dr(75) == dr(57) == 3 == dr(4 + 8)
assert dr(3 + 3) == dr(44 + 88) == dr(8 + 7) == 6 and 44 + 88 == 132

for n in (16, 25, 34, 43, 52):
    assert ds(n) == 7 and rule2(n) == 14 and dr(14) == 5
assert [rule(n) for n in (34, 43, 16, 25)] == [10, 11, 8, 9]
assert (34 + 43, 68 + 86) == (77, 154) and [ds(n) for n in (34, 43, 68, 86)] == [7, 7, 14, 14]
assert dr(7 + 7) == 5 and dr(14 + 14) == 1
assert (86 + 34, 68 + 43) == (120, 111) and dr(120) == dr(111) == 3 and dr(231) == 6 == dr(3 + 3)
def block(o):
    r = int(str(o)[::-1])
    return dr(o + 2 * r), dr(2 * o + r), dr(3 * (o + r))
ROWS = [int(f"{dr(a)}{dr(a + 1)}") for a in range(1, 10)]
assert [block(o) for o in ROWS] == [(9, 9, 9), (6, 6, 3), (3, 3, 6)] * 3
assert block(13) == block(34) == (3, 3, 6)
assert 16 + 43 == 25 + 34 == 59

if __name__ == "__main__":
    print("all assertions pass")
