# CLASS: LEMMA
"""
The X run on the ladder rows (owner, 2026-10-04: "run the X on the ladder rows").
The X from square_peg_x.py (two arms crossing at their middles; equal arms +
right angle = square). On a 3x3 digit grid the two diagonals always cross at
the centre at a right angle, so the grid's X is "square" exactly when its two
arms have EQUAL SUMS -- the digit version of equal arms.

THE GRIDS: a ladder row taken to six pieces,
    DR(a) | DR(a+1) | DR(2a+1) | 2a+10 | 2a+19 | 2a+28,
has exactly nine digits for a = 1..35, laid out in threes like 832|462|268:
    row 1: 123/122/130  arms 1+2+0 = 3,   3+2+1 = 6
    row 2: 235/142/332  arms 8, 12        row 3: 347/162/534  arms 13, 18
    row 4: 459/182/736  arms 18, 24       row 5: 562/202/938  arms 13, 11
    row 6: 674/223/140  arms 8, 7
    row 7: 786/243/342  arms 7+4+2 = 13, 6+4+3 = 13   <- EQUAL
    row 8: 898/263/544  arms 18, 19       row 9: 911/283/746  arms 23, 16
  (832/462/268 itself: arms 8+6+8 = 22, 2+6+2 = 10.)

THEOREM (proved below for every a): among the nine-digit rows, the X has equal
arms exactly when a = 7 mod 9 -- rows 7, 16, 25, 34, all opening 786.
  Proof: arms are equal iff top-left + bottom-right = top-right + bottom-left,
  i.e. DR(a) + u(2a+28) = DR(2a+1) + u(2a+19), u = units digit. 2a+19 is odd,
  so its units digit is never 0, and adding 9 lowers it by exactly 1:
  u(2a+19) - u(2a+28) = 1 always. So the condition is DR(a) - DR(2a+1) = 1,
  i.e. -a - 1 = 1 mod 9, a = 7 mod 9 (then DR(a) = 7, DR(2a+1) = 6).
  Arm sums on those rows: 13, 9, 15, 21.

ALSO FORCED: the centre digit is the units digit of 2a+10 -- 2, 4, 6, 8, 0
repeating; the grid total reduces to DR(5(2a+1)) = a + 5 mod 9
(digit_ladder_right_extension.py): rows 1-9 give 6, 7, 8, 9, 1, 2, 3, 4, 5.

FALSIFICATION: any assertion below failing.
"""
def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9

def row6(a):
    return "".join(map(str, [dr(a), dr(a + 1), dr(2 * a + 1)] + [2 * a + 1 + 9 * j for j in range(1, 4)]))

def arms(s):
    g = list(map(int, s))
    return g[0] + g[4] + g[8], g[2] + g[4] + g[6]

NINE = [a for a in range(1, 500) if len(row6(a)) == 9]
assert NINE == list(range(1, 36))
assert [row6(a) for a in (1, 7, 9)] == ["123122130", "786243342", "911283746"]
assert [arms(row6(a)) for a in range(1, 10)] == [(3, 6), (8, 12), (13, 18), (18, 24), (13, 11),
                                                (8, 7), (13, 13), (18, 19), (23, 16)]
EQUAL = [a for a in NINE if arms(row6(a))[0] == arms(row6(a))[1]]
assert EQUAL == [7, 16, 25, 34] and all(row6(a).startswith("786") for a in EQUAL)
assert [arms(row6(a))[0] for a in EQUAL] == [13, 9, 15, 21]
for a in NINE:
    u19, u28 = (2 * a + 19) % 10, (2 * a + 28) % 10
    assert u19 != 0 and u19 - u28 == 1
    assert (arms(row6(a))[0] == arms(row6(a))[1]) == (a % 9 == 7)
    g = list(map(int, row6(a)))
    assert g[4] == (2 * a) % 10 and dr(sum(g)) == dr(a + 5)
assert (8 + 6 + 8, 2 + 6 + 2) == (22, 10)

if __name__ == "__main__":
    for a in range(1, 10):
        s = row6(a)
        print(a, s[:3], s[3:6], s[6:], "arms", arms(s))
    print("equal arms:", EQUAL)
    print("all assertions pass")
