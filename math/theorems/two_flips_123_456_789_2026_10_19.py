# CLASS: AUDIT
"""
The grid 123/456/789 with two rows flipped (owner_work #358, 2026-10-19).

THE OWNER'S LINES, verbatim:
    123
    456
    789


    123
    654
    987

    what about with two flips
Reading used: the second grid is the first with rows 2 and 3 reversed (two flips); the paste of #357 had only row 2
reversed (123/654/789, one flip). The same chain is run on it.

IN THE OWNER'S NOTATION:
  123=6 ; 654=15=6 ; 987=24=6 : (6, 6, 6) again
  123=3x37+12 ; 654=17x37+25 ; 987=26x37+25 : 12, 25, 25 ; 12+25+25=62=25
  123+654+987=1764=1+7+6+4=18=9 ; 1764=47x37+25
  654-456=198 ; 987-789=198 ; 198+198=396=10x37+26 ; 1368+396=1764
  1368=36=-1 mod 37 ; 396=26 mod 37 ; -1+26=25
  1764=42x42=2x2x3x3x7x7 (42=24+18)
EVERY NUMBER OF FLIPS (each flip of 123, 456 or 789 adds 99x(c-a)=198, so only the count of flips matters, not which rows):
  0 flips 1368=-1=36 mod 37 ; 1 flip 1566=12 ; 2 flips 1764=25 ; 3 flips 1962=1 (1962=53x37+1) ; every one has root 9
  1368+198=1566, +198=1764, +198=1962 ; mod 999 they are 369, 567, 765, 963 (step 198; 369=9x41, 567=9x63, 765=9x85, 963=9x107)
  36+1=37 and 12+25=37: 0 flips and 3 flips are negatives, 1 flip and 2 flips are negatives mod 37
  1368+1962=3330=90x37=30x111 and 1566+1764=3330
THE COLUMNS (read downward): 147, 258, 369 step 111 | one flip 167, 258, 349 step 91 | two flips 169, 258, 347 step 89
  The step is 100x(row-1 direction)+10x(row-2 direction)+1x(row-3 direction) with directions +1 or -1:
  111, 91 (=100-10+1), 89 (=100-10-1). 169=13x13 ; 258=7x37-1 ; 347 is prime. 169+347=516=2x258.
  Column sums: 1+6+9=16, 2+5+8=15, 3+4+7=14 (originally 12, 15, 18). Diagonals 1+5+7=13 and 3+5+9=17 (originally 15 and 15).
  Row digit sums stay 6, 15, 24 under any flips.
FORCED: the offset 198 and the root 9 of every sum (198=9x22); the 3330 pairing (flips k and 3-k); the column steps.

FALSIFICATION: any assertion failing.
"""
from itertools import combinations

from sympy import factorint, isprime


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


rows = [123, 456, 789]
flip = lambda n: int(str(n)[::-1])
assert [flip(n) for n in rows] == [321, 654, 987] and flip(654) == 456

two = [123, 654, 987]
assert [dr(n) for n in two] == [6, 6, 6] and [(n // 37, n % 37) for n in two] == [(3, 12), (17, 25), (26, 25)]
assert 12 + 25 + 25 == 62 and 62 % 37 == 25
assert sum(two) == 1764 and dr(1764) == 9 and 1 + 7 + 6 + 4 == 18 and 1764 == 47 * 37 + 25
assert 654 - 456 == 987 - 789 == 198 and 198 + 198 == 396 == 10 * 37 + 26 and 1368 + 396 == 1764
assert sum(rows) % 37 == 36 and 396 % 37 == 26 and (36 + 26) % 37 == 25
assert 1764 == 42 * 42 and factorint(1764) == {2: 2, 3: 2, 7: 2} and 42 == 24 + 18

# every choice of flipped rows: the sum depends only on how many
tot = {}
for k in range(4):
    sums = set()
    for chosen in combinations(range(3), k):
        sums.add(sum(flip(n) if i in chosen else n for i, n in enumerate(rows)))
    assert len(sums) == 1
    tot[k] = sums.pop()
assert tot == {0: 1368, 1: 1566, 2: 1764, 3: 1962} and all(tot[k + 1] - tot[k] == 198 for k in range(3))
assert [tot[k] % 37 for k in range(4)] == [36, 12, 25, 1] and 1962 == 53 * 37 + 1
assert all(dr(v) == 9 for v in tot.values()) and [tot[k] % 999 for k in range(4)] == [369, 567, 765, 963]
assert [369 // 9, 567 // 9, 765 // 9, 963 // 9] == [41, 63, 85, 107] and 369 == 9 * 41
assert 36 + 1 == 37 and 12 + 25 == 37 and tot[0] + tot[3] == 3330 == tot[1] + tot[2] == 90 * 37 == 30 * 111

# columns, read downward
def columns(g):
    return [100 * g[0][j] + 10 * g[1][j] + g[2][j] for j in range(3)]


digits = lambda ns: [[int(c) for c in str(n)] for n in ns]
assert columns(digits([123, 456, 789])) == [147, 258, 369]
assert columns(digits([123, 654, 789])) == [167, 258, 349]
assert columns(digits(two)) == [169, 258, 347]
assert [258 - 147, 258 - 167, 258 - 169] == [111, 91, 89] and [369 - 258, 349 - 258, 347 - 258] == [111, 91, 89]
assert 100 + 10 + 1 == 111 and 100 - 10 + 1 == 91 and 100 - 10 - 1 == 89
assert 169 == 13 * 13 and 258 == 7 * 37 - 1 and isprime(347) and 169 + 347 == 516 == 2 * 258
g = digits(two)
assert [sum(g[i][j] for i in range(3)) for j in range(3)] == [16, 15, 14]
assert (g[0][0] + g[1][1] + g[2][2], g[0][2] + g[1][1] + g[2][0]) == (13, 17)
assert [sum(r) for r in g] == [6, 15, 24]

if __name__ == "__main__":
    print("two flips: 123+654+987=1764=42x42=25 mod 37, root 9; 0,1,2,3 flips give 1368, 1566, 1764, 1962 "
          "(36, 12, 25, 1 mod 37; step 198); columns 169, 258, 347 step 89")
