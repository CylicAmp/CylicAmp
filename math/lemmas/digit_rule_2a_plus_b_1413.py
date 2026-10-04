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

if __name__ == "__main__":
    print("all assertions pass")
