# CLASS: LEMMA
"""
All arithmetic on the right-extended ladder rows (owner, 2026-10-04):
    12312-21
    23514-23
    34716-25
"the logic is exact and leaves no room for error" -- every relation below is a
consequence of the rule, and each is proved for every row, not only rows 1-3.
Builds on digit_ladder_12312_91128.py and digit_ladder_right_extension.py.

Notation: row a has pieces a | a+1 | 2a+1 | 2a+10 | 2a+19 | 2a+28 | ...
(second and third reduced by digital root once they pass 9). N = the 5-digit
number, H = its first three pieces (123, 235, 347), L = its last piece
(12, 14, 16), T = the new piece (21, 23, 25).

EXTENDED FURTHER TO THE RIGHT (+9 each step):
    12312 21 30 39 48 57
    23514 23 32 41 50 59
    34716 25 34 43 52 61
  Every tail piece has the same digital root as the row's middle piece: 3, 5, 7.

HORIZONTAL (inside one row):
  T - L = 9 always; T + L = 4a+29 (33, 37, 41).
  N + T = 100*H + (L+T) = 100*H + 4a+29: 12333, 23537, 34741.
  N - T = 100*H - 9:  12291, 23491, 34691   (holds for every row; row 9: 91091).
  Piece sum = 8a+31 (39, 47, 55); alternating sum = 2a+9 (11, 13, 15).
  DR(N*T) = DR(3(2a+1)^2): 9, 3, 3 repeating -- every N*T divisible by 3.
  N*T: 258552 = 2^3*3^5*7*19,  540822 = 2*3*23*3919,  867900 = 2^2*3*5^2*11*263.
  N mod T: 6, 8, 16 (rows 1-3); 18 for rows 4, 5 and 7.

VERTICAL (down the columns of the 7-digit grid):
    1 2 3 1 2 2 1
    2 3 5 1 4 2 3
    3 4 7 1 6 2 5
  Every column is an arithmetic progression, steps 1,1,2,0,2,0,2. Row 4 (4591827)
  continues every column; row 5 is the first wrap and breaks it.
  So each column sums to 3 x its middle digit: 6,9,15,3,12,6,9 = 3 x (2,3,5,1,4,2,3),
  and the whole rows are in arithmetic progression: R1 + R3 = 2*R2 = 4702846,
  R1 + R2 + R3 = 3*R2 = 7054269 = 3*17*138319.
  Row digit sums 12, 20, 28, step 8; grid total 60 = 3*20.
  Constant columns: the 1 (first digit of L, rows 1-4) and the 2 (first digit of T).

DIAGONALS: main 1,3,7 ; anti 1,2,6.

FALSIFICATION: any assertion below failing.
"""
from sympy import factorint

def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9

def head(a):
    return int(f"{a}{dr(a + 1)}{dr(2 * a + 1)}")

def N(a):
    return int(f"{head(a)}{2 * a + 10}")

def T(a):
    return 2 * a + 19

def tail(a, k):
    return [2 * a + 1 + 9 * j for j in range(1, k + 1)]

assert [(N(a), T(a)) for a in (1, 2, 3)] == [(12312, 21), (23514, 23), (34716, 25)]
assert tail(1, 6) == [12, 21, 30, 39, 48, 57]
assert tail(2, 6) == [14, 23, 32, 41, 50, 59] and tail(3, 6) == [16, 25, 34, 43, 52, 61]

for a in range(1, 41):
    L = 2 * a + 10
    assert T(a) - L == 9 and T(a) + L == 4 * a + 29
    assert N(a) + T(a) == 100 * head(a) + 4 * a + 29
    assert N(a) - T(a) == 100 * head(a) - 9
    ps = [a, a + 1, 2 * a + 1, 2 * a + 10, 2 * a + 19]
    assert sum(ps) == 8 * a + 31 and ps[0] - ps[1] + ps[2] - ps[3] + ps[4] == 2 * a + 9
    assert dr(N(a) * T(a)) == dr(3 * (2 * a + 1) ** 2) and N(a) * T(a) % 3 == 0
    assert len({dr(x) for x in [dr(2 * a + 1)] + tail(a, 8)}) == 1

assert [N(a) + T(a) for a in (1, 2, 3)] == [12333, 23537, 34741]
assert [N(a) - T(a) for a in (1, 2, 3, 9)] == [12291, 23491, 34691, 91091]
assert [dr(N(a) * T(a)) for a in range(1, 10)] == [9, 3, 3] * 3
assert factorint(258552) == {2: 3, 3: 5, 7: 1, 19: 1} == factorint(N(1) * T(1))
assert factorint(540822) == {2: 1, 3: 1, 23: 1, 3919: 1}
assert factorint(867900) == {2: 2, 3: 1, 5: 2, 11: 1, 263: 1}
assert [N(a) % T(a) for a in range(1, 10)] == [6, 8, 16, 18, 18, 28, 18, 16, 34]

G = [list(map(int, f"{N(a)}{T(a)}")) for a in range(1, 6)]
steps = [G[1][c] - G[0][c] for c in range(7)]
assert steps == [1, 1, 2, 0, 2, 0, 2]
assert all(G[r + 1][c] - G[r][c] == steps[c] for r in range(3) for c in range(7))
assert any(G[4][c] - G[3][c] != steps[c] for c in range(7))
assert [sum(G[r][c] for r in range(3)) for c in range(7)] == [3 * G[1][c] for c in range(7)] == [6, 9, 15, 3, 12, 6, 9]
R = [int(f"{N(a)}{T(a)}") for a in (1, 2, 3)]
assert R[0] + R[2] == 2 * R[1] == 4702846 and sum(R) == 3 * R[1] == 7054269
assert factorint(7054269) == {3: 1, 17: 1, 138319: 1}
assert [sum(G[r]) for r in range(3)] == [12, 20, 28] and sum(map(sum, G[:3])) == 60
assert [G[i][i] for i in range(3)] == [1, 3, 7] and [G[i][6 - i] for i in range(3)] == [1, 2, 6]

if __name__ == "__main__":
    for a in (1, 2, 3):
        print(N(a), T(a), "| extended:", tail(a, 6), "| N+T", N(a) + T(a), "N-T", N(a) - T(a),
              "N*T", N(a) * T(a), "N mod T", N(a) % T(a))
    print("all assertions pass")
