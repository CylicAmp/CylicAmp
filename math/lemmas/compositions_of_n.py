# CLASS: LEMMA
"""
Owner, 2026-10-04: building numbers from smaller ones, order counting
(compositions):
    2 = 1+1
    3 = 111, 2+1, 1+2
    4 = 1+3, 3+1, 11+2, 2+11, 1111   "at 4 it gets way more complicated"
    "double check I am not missing any combinations of 123 to make 4"
Context: the splits of 6 and 8 into equal parts (rotation_grids_x.py,
ladder_loops_squares.py) -- this is the unequal, ordered version.

CHECKED: 2 and 3 are complete. 4 has 7 ways from 1, 2, 3; the list gave 5 and
is missing 2+2 and 1+2+1:
    1+1+1+1, 1+1+2, 1+2+1, 2+1+1, 1+3, 3+1, 2+2

WHY 4 IS WHERE IT GETS COMPLICATED:
  - First number with a repeated part bigger than 1 (2+2), and the first with
    a mirrored middle (1+2+1).
  - Counting every way except the number itself gives 1, 3, 7, 15, 31, 63 for
    n = 2..7: 2^(n-1) - 1, each one double the last plus 1 -- doubling again.
  - Up to 4, the pieces 1, 2, 3 are all that is ever needed. From 5 on they
    are not: 5 has 15 ways but only 13 from 1, 2, 3 (4+1 and 1+4 need a 4).
    With pieces 1, 2, 3 only, the counts 1, 2, 4, 7, 13, 24, 44 (including the
    number itself up to 3) each equal the sum of the previous three.

FALSIFICATION: any assertion below failing.
"""
def comps(n, parts):
    if n == 0:
        return [[]]
    return [[p] + r for p in parts if p <= n for r in comps(n - p, parts)]

def show(c):
    return "+".join(map(str, c))

assert sorted(show(c) for c in comps(2, (1,))) == ["1+1"]
assert sorted(show(c) for c in comps(3, (1, 2))) == ["1+1+1", "1+2", "2+1"]
FOUR = sorted(show(c) for c in comps(4, (1, 2, 3)))
assert FOUR == ["1+1+1+1", "1+1+2", "1+2+1", "1+3", "2+1+1", "2+2", "3+1"]
GIVEN = {"1+3", "3+1", "1+1+2", "2+1+1", "1+1+1+1"}
assert sorted(set(FOUR) - GIVEN) == ["1+2+1", "2+2"]

assert [len(comps(n, range(1, n))) for n in range(2, 8)] == [1, 3, 7, 15, 31, 63]
assert all(len(comps(n, range(1, n))) == 2 ** (n - 1) - 1 for n in range(2, 12))
assert [len(comps(n, (1, 2, 3))) for n in range(1, 8)] == [1, 2, 4, 7, 13, 24, 44]
T = [len(comps(n, (1, 2, 3))) for n in range(1, 15)]
assert all(T[i] == T[i - 1] + T[i - 2] + T[i - 3] for i in range(3, len(T)))
assert len([c for c in comps(5, (1, 2, 3)) if len(c) > 1]) == 13 and len(comps(5, range(1, 5))) == 15

if __name__ == "__main__":
    print("4 =", ", ".join(FOUR))
    print("all assertions pass")
