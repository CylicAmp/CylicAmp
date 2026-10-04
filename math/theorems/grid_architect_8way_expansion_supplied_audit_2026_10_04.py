# CLASS: AUDIT
"""
Audit of supplied blocks (2026-10-04): universal grid architect, 8-way rotation engine,
connected grids 1-3 / 1-4, maximum expansion engine. (The 1-1..1-9 expansion repeats
grip_81_and_one_x_supplied_audit_2026_10_04.py T9: correct and forced.) Mathematics only.

GRID ARCHITECT (pair 1-3)
  X1 The script's own seed rule gives rows 2 and 3 = [1,1,1,1] for d1 = 1, so its assertion
     g_prm[1] == [P,P,1,P,P,1,P,P] FAILS (the row is all "1"). The integer, primality and
     mod-5 grids printed in the text (rows 3 1 1 3 / P P 1 P) are not what the code builds.
     Its other assertion (parity row 0 = E O O E E O O E) holds.
8-WAY ROTATION OF 4 3 1 4 -- CORRECT, and forced
  X2 Rows 4314 / 3144 / 1443 / 4431: every row and column sums to 12, main diagonal 10,
     anti-diagonal 16, total 48. Rows and columns are forced equal: in a cyclic rotation stack
     every column holds each entry once. "Forward = reverse" sums are the same sum.
CONNECTED GRIDS -- arithmetic CORRECT
  X3 5145 stack: rows and columns 15, total 60; 48 + 60 = 108, root 9; 108 = 3 mod 5;
     column sums 12 + 15 = 27, root 9. The connection script lost its rows in the paste
     (SyntaxError).
MAXIMUM EXPANSION ENGINE -- the script's OWN output contradicts the text
  X4 Text: total 34,965, 0 mod 5, 777 full 45-containers. The script computes 23,328 (the same
     total as the tensor audit -- an 8x8 field is four copies of its seed), 3 mod 5, 518 full
     containers with 18 left over. Its `assert master_fives == 0` FAILS.
  X5 Its "shape registry" only sorts pairs by digit parity: 16 even-even, 40 mixed, 24 odd-odd
     plus 99 -- not 20 / 40 / 20 / 1.
NOT IN THE REPOSITORY: none of these scripts exists on all-work.
FALSIFICATION: any assertion failing.
"""
dr = lambda n: 9 if n % 9 == 0 else n % 9


def seed(d1, d2):
    r1, r4 = dr(int(f"{d1}{d2}")), dr(int(f"{d2}{d1}"))
    return [[r1, d1, d2, r1], [d1, 1, d1, d1], [d1, d1, 1, d1], [d2, d2, d1, r4]]


def f8(s):
    t = [r[::-1] + r for r in s]
    return t + t[::-1]


pr = lambda n: "1" if n == 1 else ("P" if n in (2, 3, 5, 7) else "C")
par = lambda n: "E" if n % 2 == 0 else "O"
s13 = seed(1, 3)
assert s13[1] == s13[2] == [1, 1, 1, 1]                                                  # X1
assert f8([[pr(x) for x in r] for r in s13])[1] == ["1"] * 8
assert f8([[par(x) for x in r] for r in s13])[0] == list("EOOEEOOE")


def rot_stack(v):
    return [v[k:] + v[:k] for k in range(len(v))]


m = rot_stack([4, 3, 1, 4])
assert m == [[4, 3, 1, 4], [3, 1, 4, 4], [1, 4, 4, 3], [4, 4, 3, 1]]                       # X2
assert {sum(r) for r in m} == {12} == {sum(c) for c in zip(*m)}
assert sum(m[i][i] for i in range(4)) == 10 and sum(m[i][3 - i] for i in range(4)) == 16
n = rot_stack([5, 1, 4, 5])
assert sum(map(sum, n)) == 60 and 48 + 60 == 108 and dr(108) == 9 and 108 % 5 == 3      # X3
assert dr(12 + 15) == 9
tot = sum(sum(map(sum, f8(seed(a, b)))) for a in range(1, 10) for b in range(1, 10))
assert tot == 23328 and tot % 5 == 3 and divmod(tot, 45) == (518, 18)                     # X4
reg = {"ee": 0, "mixed": 0, "oo": 0, "99": 0}
for a in range(1, 10):
    for b in range(1, 10):
        reg["99" if (a, b) == (9, 9) else "ee" if a % 2 == b % 2 == 0 else "oo" if a % 2 and b % 2 else "mixed"] += 1
assert reg == {"ee": 16, "mixed": 40, "oo": 24, "99": 1}                                   # X5
