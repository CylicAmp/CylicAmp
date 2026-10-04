# CLASS: LEMMA
"""
Right extension of the digit ladder (owner, 2026-10-04):
    12312-21
    23515-23   (typo for 23514, confirmed by owner)
    34716-25
Builds on math/lemmas/digit_ladder_12312_91128.py (row a = a | DR(a+1) | DR(2a+1) | 2a+10).

RULE: each new piece on the right is the previous one + 9:
    12 -> 21, 14 -> 23, 16 -> 25,  i.e. the 5th piece is 2a+19.
So after the first two pieces every piece is 2a+1 + 9j, and every piece has the
same digital root DR(2a+1) -- the "12=3" relation repeated down the row.

ROW 2 AS WRITTEN DOES NOT FIT: 23515 has last piece 15, but the ladder image has
23514 (2a+10 = 14), and 14 + 9 = 23 matches the supplied 23. With 15 the step
would be 8. The whole-row step also breaks: with 23514 the rows 1231221,
2351423, 3471625 step by 1120202 twice; with 23515 the steps are 1120302 and
1120102. Owner confirmed 2026-10-04: typo, the row is 23514.

PROVED FOR EVERY ROW LENGTH P (pieces) AND EVERY a:
  - DR(row) = DR((P-1)(2a+1)): the first two pieces sum to 2a+1 and every later
    piece is congruent to 2a+1 mod 9.
      P=4: 9,6,3 repeating     (3 | P-1: every row divisible by 3)
      P=5: 3,2,1,9,8,7,6,5,4   (8a+4: falls by 1 each row)
      P=6: 6,7,8,9,1,2,3,4,5   (10a+5: rises by 1 each row)
      P=7: 9,3,6 repeating
      P=10: DR 9 in every row  (9 | P-1)
  - Pieces alternate odd/even (2a+1, 2a+10, 2a+19, ...), so a row is even iff P
    is even: the 5-piece rows are odd and lose the divisibility by 6.
  - Row-to-row step: 11202, 1120202, 112020202, ... -- each piece added appends
    "02", because every appended piece grows by 2 per row. The two wraps
    (rows 4->5 middle 9->2, rows 8->9 second 9->1) subtract 900 and 9900 times
    100^(P-4): each added piece moves the wrapped digits two places left.
  - Within a row, adjacent tail pieces differ by 9; down a column they differ by 2.

5-PIECE ROWS 1..3, all registers (digit-protocols engine):
  1231221: digits 1+2+3+1+2+2+1=12, DR 3, triad;   = 3*97*4231;   rev 1221321 = 3*421*967
  2351423: digits sum 20, DR 2, circuit;           = 17*138319;   rev 3241532 = 2^2*7*115769
  3471625: digits sum 28, DR 1, circuit;           = 5^3*27773;   rev 5261743 is prime
  (2351523, the row as typed: sum 21, DR 3, = 3*29*151*179.)
  |N - rev| is a multiple of 9 for every N: forced, not a finding.
  Tail pairs (2a+10, 2a+19): (12,21) sum 33, (14,23) sum 37, (16,25) sum 41: 4a+29.
  12 and 21 are reversals of each other; 14/23 and 16/25 are not: row 1 only.

FALSIFICATION: any assertion below failing.
"""
from sympy import factorint, isprime

def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9

def pieces(a, P):
    return [a, dr(a + 1), dr(2 * a + 1)] + [2 * a + 1 + 9 * j for j in range(1, P - 2)]

def row(a, P):
    return int("".join(map(str, pieces(a, P))))

SUPPLIED = [(12312, 21), (23515, 23), (34716, 25)]
assert [(row(a, 4), pieces(a, 5)[-1]) for a in (1, 2, 3)] == [(12312, 21), (23514, 23), (34716, 25)]
assert 23515 != row(2, 4) and 23 - 15 == 8 and 23 - 14 == 9

R5 = [1231221, 2351423, 3471625, 4591827, 5622029, 6742231, 7862433, 8982635, 9112837]
assert [row(a, 5) for a in range(1, 10)] == R5
assert [R5[i + 1] - R5[i] for i in range(2)] == [1120202, 1120202]
assert 2351523 - 1231221 == 1120302 and 3471625 - 2351523 == 1120102

for P in range(4, 16):
    for a in range(1, 300):
        r = row(a, P)
        assert dr(r) == dr((P - 1) * (2 * a + 1))
        assert (r % 2 == 0) == (P % 2 == 0)
        ps = pieces(a, P)
        assert len({dr(x) for x in ps[2:]}) == 1
assert [dr(row(a, 5)) for a in range(1, 10)] == [3, 2, 1, 9, 8, 7, 6, 5, 4]
assert [dr(row(a, 6)) for a in range(1, 10)] == [6, 7, 8, 9, 1, 2, 3, 4, 5]
assert all(dr(row(a, 10)) == 9 for a in range(1, 300))

for P, step in ((4, 11202), (5, 1120202), (6, 112020202), (7, 11202020202)):
    R = [row(a, P) for a in range(1, 10)]
    d = [R[i + 1] - R[i] for i in range(8)]
    assert d[0] == d[1] == d[2] == d[4] == d[5] == d[6] == step
    assert step - d[3] == 900 * 100 ** (P - 4) and step - d[7] == 9900 * 100 ** (P - 4)

assert factorint(1231221) == {3: 1, 97: 1, 4231: 1}
assert factorint(2351423) == {17: 1, 138319: 1}
assert factorint(3471625) == {5: 3, 27773: 1}
assert factorint(2351523) == {3: 1, 29: 1, 151: 1, 179: 1}
assert isprime(5261743) and factorint(1221321) == {3: 1, 421: 1, 967: 1}
assert [x + y for x, y in ((12, 21), (14, 23), (16, 25))] == [4 * a + 29 for a in (1, 2, 3)]

if __name__ == "__main__":
    for P in (4, 5, 6, 7):
        print(P, [row(a, P) for a in range(1, 10)])
    print("all assertions pass")
