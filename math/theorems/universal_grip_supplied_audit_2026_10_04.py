# CLASS: AUDIT
"""
Audit of six supplied blocks (2026-10-04) on the owner's "universal grip":

    6 = 24 = 6 = 42 = 6
    3 = 12 = 3 = 21 = 3
    3 = 21 = 3 = 12 = 3
    4 = 42 = 6 = 24 = 6

Each 2-digit middle number has the digit sum written beside it (2+4 = 6, 1+2 = 3), and the
rows pair a number with its reversal. Mathematics only.

G1 2-DIGIT GRIP -- CORRECT: gaps 42-24 = 18, 21-12 = 9, -9, -18, total 0; mod 9 / mod 5 of
   24, 12, 21, 42 = 6/4, 3/2, 3/1, 6/2; 81 two-digit numbers with nonzero digits (11..99).
   FORCED: ab - ba = 9(a - b), always a multiple of 9; and the rows come in reversal pairs,
   so the gaps cancel to 0. WRONG: "the roots 6,3,3,6 match the outer anchor columns" -- the
   right column does; the left column is 6,3,3,4. Row 4's left anchor 4 is the one entry that
   is not the digit sum (4 + 2 = 6); it is recorded as written.
G2 PARITY OF THE WHOLE NUMBERS -- CORRECT: rows E E E / O E O / O O O / E E E, left and right
   anchors always the same parity.
G3 PRIME/COMPOSITE OF THE WHOLE NUMBERS -- CORRECT values (C C C / P C P / P C P / C C C) and
   anchors match. The supplied script does NOT run: f"{p_row:<10}" on a tuple is a TypeError,
   `assert p_row == p_row` checks nothing, and comparing the list processed_matrix to a tuple
   is always False.
G4 DIGIT-BY-DIGIT (6246 / 3123 / 3213 / 4426) -- CORRECT: each middle pair (2,4) (1,2) (2,1)
   (4,2) has exactly one prime digit -- forced, since every pair contains a 2 and the other
   digit is 1 or 4; rows 1/4 and 2/3 are reversals. WRONG: the "anchor sync" (left middle
   digit shares the prime status of the right anchor, and vice versa) fails -- row 1: 2 is
   prime, 6 is not. The script's __main__ never calls the audit, so it checks nothing.
G5 8x8 PARITY FIELD -- CORRECT, and stronger than stated: with the 4-panel mirroring, BOTH full
   diagonals of the 8x8 are all even -- a real X. Rows 1, 4, 5, 8 are all even. WRONG: "square
   perimeter": the side columns are odd on rows 2, 3, 6, 7, so the frame is two horizontal
   bands, not a closed square.
G6 8x8 PRIME/COMPOSITE FIELD -- CORRECT layout. WRONG: (a) the 1s do not lie on an X: they sit
   at (1,2) (1,5) (2,1) (2,6) and mirrors, a ring of 8 around the centre, off both diagonals;
   (b) "C tokens wall rows 1, 4, 5, 8": those rows contain P (row 1 = C C P C C P C C), so
   there is no solid C frame -- only the four corners are C.
NOT IN THE REPOSITORY: none of the six t325_*grip*_2026_10_03.py files exists on all-work
   (checked 2026-10-04 after fetching origin); the universal-grip script itself was cut off in
   the paste (`cat > ... &1 | tail -1`).
FALSIFICATION: any assertion failing.
"""
from sympy import isprime

ds = lambda n: sum(map(int, str(n)))
root = lambda n: n % 9 or 9
GRIP = [(6, 24, 6, 42, 6), (3, 12, 3, 21, 3), (3, 21, 3, 12, 3), (4, 42, 6, 24, 6)]

# G1
assert [r[3] - r[1] for r in GRIP] == [18, 9, -9, -18] and sum(r[3] - r[1] for r in GRIP) == 0
assert all(int(f"{a}{b}") - int(f"{b}{a}") == 9 * (a - b) for a in range(1, 10) for b in range(1, 10))
assert [(root(n), n % 5) for n in (24, 12, 21, 42)] == [(6, 4), (3, 2), (3, 1), (6, 2)]
assert len([n for n in range(11, 100) if "0" not in str(n)]) == 81
assert [r[4] for r in GRIP] == [6, 3, 3, 6] and [r[0] for r in GRIP] == [6, 3, 3, 4]
assert all(ds(r[1]) == r[2] for r in GRIP) and ds(42) == 6 != 4

# G2, G3
par = lambda n: "E" if n % 2 == 0 else "O"
pc = lambda n: "P" if isprime(n) else "C"
W = [(6, 24, 6), (3, 12, 3), (3, 21, 3), (4, 42, 6)]
assert ["".join(map(par, r)) for r in W] == ["EEE", "OEO", "OOO", "EEE"]
assert ["".join(map(pc, r)) for r in W] == ["CCC", "PCP", "PCP", "CCC"]
try:
    f"{('Composite',) * 3:<10}"
    raise AssertionError("expected TypeError")
except TypeError:
    pass
assert [("Composite",) * 3] != ("Composite",) * 3

# G4
D = [(6, 2, 4, 6), (3, 1, 2, 3), (3, 2, 1, 3), (4, 4, 2, 6)]
P1 = lambda d: d in (2, 3, 5, 7)
assert all(P1(a) != P1(b) for _, a, b, _ in D)
assert (D[0][1], D[0][2]) == (D[3][2], D[3][1]) and (D[1][1], D[1][2]) == (D[2][2], D[2][1])
assert P1(D[0][1]) and not P1(D[0][3])                          # anchor sync fails on row 1


def field(seed):
    top = [row[::-1] + row for row in seed]
    return top + top[::-1]


# G5
digits = ["6246", "3123", "3213", "4426"]
pf = field([["e" if int(c) % 2 == 0 else "o" for c in s] for s in digits])
assert all(pf[i][i] == "e" and pf[i][7 - i] == "e" for i in range(8))
assert all(set(pf[r]) == {"e"} for r in (0, 3, 4, 7)) and pf[1][0] == "o"
# G6
cls = lambda c: "1" if c == "1" else ("P" if c in "2357" else "C")
qf = field([[cls(c) for c in s] for s in digits])
ones = sorted((r, c) for r in range(8) for c in range(8) if qf[r][c] == "1")
assert ones == [(1, 2), (1, 5), (2, 1), (2, 6), (5, 1), (5, 6), (6, 2), (6, 5)]
assert not any(r == c or r + c == 7 for r, c in ones)
assert qf[0] == list("CCPCCPCC") and all(qf[r][c] == "C" for r in (0, 7) for c in (0, 7))

if __name__ == "__main__":
    for name, f in (("parity field", pf), ("prime/composite field", qf)):
        print(name)
        for row in f:
            print("  " + " ".join(row[:4]) + " | " + " ".join(row[4:]))
