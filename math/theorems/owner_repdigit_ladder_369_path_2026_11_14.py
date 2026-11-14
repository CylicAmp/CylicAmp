# CLASS: COMPUTATION
"""
The owner's marks on the printed list "Every multiple of 3 creates repeating digits" (image, 2026-11-14):
  3 x 37 = 111, 6 x 37 = 222, ..., 27 x 37 = 999, and the owner's additions:
    "111" written between every two rows;
    each row's root, coloured: 3 6 9 | 3 6 9 | 3 6 9 (red 3, green 6, blue 9);
    a path of 3s down the side, with small 1 and 2 marks, boxes at 222, 666 and 888, a cross at 555;
    and three lines:
        "3+3=6+6=12"           (at 222)
        "3x4=12+6=1+8=9"       (at 555)
        "+3+1=4+9=1+3=4"       (at 777)

CLEANED (the owner's = chain carries each result on; a two-digit total is written as its digits):
    each row = the row above + 111          right: 37 x (3k + 3) = 37 x 3k + 111
    roots 3 6 9 3 6 9 3 6 9                 right: 111 has root 3, so each step adds 3 to the root
    3 + 3 = 6 -> 6 + 6 = 12                 right
    3 x 4 = 12 -> 12 + 6 = 18 -> 1 + 8 = 9  right
    3 + 1 = 4 -> 4 + 9 = 13 -> 1 + 3 = 4    right

FORCED (true for the list, nothing to find): 37 x 3k = 111k for k = 1 .. 9 because 111 = 3 x 37 (T302: 111 is Phi_3
  at 10); the root of 111k is the root of 3k, so the roots run 3 6 9 three times -- the owner's 3 6 9 (cipher_123_1234:
  the trinity 3 6 9 by 9). 555 is the middle row (5th of 9), the one marked with the cross.
The 1 and 2 marks beside the 3s are recorded as drawn; no check here depends on them.

FALSIFICATION: any assertion failing.
"""


def root(n):
    return 1 + (n - 1) % 9


rows = [37 * 3 * k for k in range(1, 10)]
assert rows == [111 * k for k in range(1, 10)] == [int(str(k) * 3) for k in range(1, 10)]
assert all(rows[i + 1] - rows[i] == 111 for i in range(8)) and root(111) == 3
assert [root(r) for r in rows] == [3, 6, 9] * 3
assert [(root(rows[i]) + 3 - 1) % 9 + 1 for i in range(8)] == [root(r) for r in rows[1:]]

# the three lines, as chains
assert 3 + 3 == 6 and 6 + 6 == 12
assert 3 * 4 == 12 and 12 + 6 == 18 and 1 + 8 == 9
assert 3 + 1 == 4 and 4 + 9 == 13 and 1 + 3 == 4

assert rows[4] == 555 and len(rows) // 2 == 4                    # 555 is the middle row
assert 111 == 3 * 37 == 10 ** 2 + 10 + 1

if __name__ == "__main__":
    print("each row + 111; roots 3 6 9 x 3; 3+3=6, 6+6=12; 3x4=12, 12+6=18 -> 9; 3+1=4, 4+9=13 -> 4: all right")
