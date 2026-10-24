# CLASS: COMPUTATION
"""
The odd/even 3 x 3 grid and 13,579 with and without its first digits (owner_work #437, 2026-10-24).
Process entry: owner_work/PROCESS.md, #437. The same message asks "What are you saying is not a discovery?" --
answered in the reply: only the two outputs of the long walks (the twin counts, published in OEIS A007508, and
"missed 0", forced for every n; owner_walk_what_it_shows_2026_10_24.py), nothing of the owner's operations.

THE OWNER'S LINES, verbatim (#437):
    oeo
    eoe
    oeo

    □■□
    ■□■
    □■□

    13,579
    3,579
    1,579
    579
    ■□■


    What are you saying is not a discovery?

CLEANED:
    the grid 1 2 3 / 4 5 6 / 7 8 9, odd (o, □) and even (e, ■):
        o e o        □ ■ □        1 2 3
        e o e        ■ □ ■        4 5 6
        o e o        □ ■ □        7 8 9
    the odd cells in order: 1 3 5 7 9 -> 13,579; then without the 1, without the 3, without both:
        13,579    3,579    1,579    579
    ■ □ ■ (even odd even): the middle row 4 5 6, or the middle column 2 5 8

PROCESS: mark the 1-to-9 grid odd and even; read the odd cells as one number; take the first digits off one at a time
and both together; mark the even-odd-even line.

CHECKED:
    the grid's odd/even marks: right (1 3 5 7 9 odd at the corners and the center, 2 4 6 8 even at the edges)
    odd cells 1 + 3 + 5 + 7 + 9 = 25 -> 7;  even cells 2 + 4 + 6 + 8 = 20 -> 2;  7 + 2 = 9 (all of 1 to 9 = 45 -> 9)
    13579 -> 25 -> 7    3579 -> 24 -> 6    1579 -> 22 -> 4    579 -> 21 -> 3
      taking off the 1 takes 1 off the root, taking off the 3 takes 3 off, both take 4 off
    ■□■: 4 + 5 + 6 = 15 -> 6 and 2 + 5 + 8 = 15 -> 6 (the center 5 and an even pair around it adding to 10)
    with the comma and without (#372): 13,579 -> 13 + 579 = 592;  3,579 -> 582;  1,579 -> 580; the groups give the
      same root as the whole number (7 6 4 3) and the same remainder by 37 (0 27 25 24), because 1000 = 27 x 37 + 1

FRAMEWORKS (gf37-audit): 13579 = 37 x 367 -> 0 (and 13 + 579 = 592 = 16 x 37); 1579 is prime -> 25 SA_ST_B
  (cousin with 1583); 3579 = 3 x 1193 -> 27 NEG_H; 579 = 3 x 193 -> 24 SEED.

FALSIFICATION: any assertion failing.
"""
from sympy import factorint, isprime


def root(m):
    while m > 9:
        m = sum(map(int, str(m)))
    return m


grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
marks = ["".join("o" if v % 2 else "e" for v in row) for row in grid]
assert marks == ["oeo", "eoe", "oeo"]
assert [r.replace("o", "□").replace("e", "■") for r in marks] == ["□■□", "■□■", "□■□"]
odd = [v for row in grid for v in row if v % 2]
even = [v for row in grid for v in row if not v % 2]
assert odd == [1, 3, 5, 7, 9] and int("".join(map(str, odd))) == 13579
assert sum(odd) == 25 and root(25) == 7 and sum(even) == 20 and root(20) == 2 and root(7 + 2) == 9
nums = [13579, 3579, 1579, 579]
assert [root(x) for x in nums] == [7, 6, 4, 3]
assert root(13579) - root(3579) == 1 and root(13579) - root(1579) == 3 and root(13579) - root(579) == 4
assert sum([4, 5, 6]) == sum([2, 5, 8]) == 15 and root(15) == 6 and 4 + 6 == 2 + 8 == 10
comma = [13 + 579, 3 + 579, 1 + 579, 579]
assert comma == [592, 582, 580, 579]
assert [root(x) for x in comma] == [7, 6, 4, 3] and [x % 37 for x in comma] == [x % 37 for x in nums] == [0, 27, 25, 24]
assert 1000 == 27 * 37 + 1
assert factorint(13579) == {37: 1, 367: 1} and 592 == 16 * 37 and isprime(1579) and isprime(1583)
assert factorint(3579) == {3: 1, 1193: 1} and factorint(579) == {3: 1, 193: 1}

if __name__ == "__main__":
    print("#437: odd/even grid right; odd cells 13579 = 37 x 367 (root 7), without 1 / 3 / both: roots 6 4 3; "
          "the comma groups keep the root and the remainder by 37")
