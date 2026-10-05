# CLASS: LEMMA
"""
The ultimate rotation run on the prime row (owner, 2026-10-05).
Prime row: digital roots of the first nine primes, 235724815 (11 -> 2), or
2357114815 with 11 split 1|1 (rotation_grids_x.py, prime_row_on_ladder.py).
Method and rule: ultimate_rotation_1_9.py, ladder_ultimate_rotation.py --
stacking the n turns makes every row and column sum to S; one diagonal repeats
a digit d (sum n*d), the other (n odd) passes through every position (sum S);
the X balances exactly when S = n*d for a digit d in the row.

NINE DIGITS, 235724815: turns 235724815, 357248152, 572481523, ... back in 9.
  Every row and column of every stacking sums to 37.
  NO STACKING BALANCES: 37 is prime, so it is never 9 x a digit. The closest
  are the four stackings whose repeated diagonal is all 4s: 9 x 4 = 36 against
  37 -- one short. Starts 427532518 and 481523572 (right), 275325184 and
  815235724 (left).
TEN DIGITS, 2357114815: sum 37 again; 37 is not 10 x a digit either; closest
  diagonals 48 and 50.
Figure: math/lemmas/figures/prime_row_ultimate_rotation.png (left: the cycle;
right: the nearest grid, diagonals 36 and 37).

TO KEEP IN MIND (owner, 2026-10-05): (2+3)57(24)81(2+3).
  The row opens with the primes 2 and 3 and its last prime is 23 -- the same
  two digits -- so both ends are 2+3 = 5. Inside: 57 (primes 5, 7), the
  centre 24 (11 -> 2, 13 -> 4), and 81 (17 -> 8, 19 -> 1). Total 37.

PRIMES BY DECADE (owner, 2026-10-05):
    2357 / 2481 -- roots of 2, 3, 5, 7 and of the teens 11, 13, 17, 19.
    "5 is not part of first 1 thru 22 (1+4 = 5)"; "in the 20s we get only
    23 + 29 = 5+2 = 7"; 43 (typed 42) = ... "pi's rotation".
  Below 23 the root 5 comes only from the prime 5 itself; the teens row 2481
  has no 5 and no 7 (14 -> 5 is not prime). The 20s hold just 23 and 29
  (roots 5 and 2): they bring 5 back, and 23 + 29 = 52 -> 7 brings 7 back.
  23 STACKED ON 29: 2+2 = 4 and 3+9 = 12 -> 3, giving 43 -- a prime with root
  7, the first prime after 7 itself with root 7 (16, 25, 34 are not prime).
  The two primes of the 20s build the prime that brings 7 back.
  The owner's chain: 43 = 7, + 2 = 9, + 5 = 14 -> 1+4 = 5 (either order gives
  14 -> 5) -- landing on 14, the "1+4 = 5" that was not prime in the teens.

THE L ON THE PRIME ROW (owner, 2026-10-05; the L is in
  prime_counts_supplied_audit_2026_10_05.py: doubling right R, 2R, 4R, counting
  down R, 2R, 3R):
  WHOLE ROW R = 235724815: 2R = 471449630, right 4R = 942899260, down
  3R = 707174445. Roots: right 1, 2, 4 -- the start of the forever cycle -- and
  down 3, NOT 9 as on every ladder row: the prime row totals 37, which 3 does
  not divide. (The ten-digit form 2357114815 gives the same roots.)
  DIGIT BY DIGIT (each of 2, 3, 5, 7, 2, 4, 8, 1, 5 as its own corner): the four
  positions total 37, 74, 148 (right) and 111 (down) -- 1, 2, 4 and 3 times 37,
  forced since the digits sum to 37; the down total 111 = 3 x 37 is the
  repdigit. Down-arm ends 3d reduce only to 3, 6, 9.

THE L DIGIT BY DIGIT ON THE NINE LADDER ROWS (nine-digit forms; totals of the
  corners, doubles, right ends 4d and down ends 3d = S, 2S, 4S, 3S):
    row 1 15 30 60 45     row 2 25 50 100 75    row 3 35 70 140 105
    row 4 45 90 180 135   row 5 37 74 148 111   row 6 29 58 116 87
    row 7 39 78 156 117   row 8 49 98 196 147   row 9 41 82 164 123
  Row 5 (562202938) gives exactly the prime row's 37, 74, 148, 111 -- both total
  37. The two arms always end S apart (4S - 3S = S).
  OWNER'S LINES: 147 - 111 = 36 -> 3+6 = 9 (correct; 147 is row 8's down total,
  111 row 5's and the prime row's). Stack 111 / 246 / 111 / 369: 246 + 111 =
  357, 369 - 111 = 258; adding 111 walks the plain grid's columns 147 -> 258 ->
  369. (The prime row's right total is 148, and 148 - 111 = 37.)

PASTED "SymPy Verification Engine" SCRIPT (2026-10-05) -- AUDIT:
  It does not run: dr() is used but never defined (NameError on the R2 line),
  so any output attributed to it was not produced by it. R2 (digital roots of
  the digits) would equal R1 anyway -- every digit is already its own root.
  Run correctly: 235724815 is not prime (ends in 5); 235724815 =
  5 x 23 x 971 x 2111 -- 23, the row's last prime, divides it.
  The pasted L table (ladder rows 1-9): every cell checked, all correct; row 2
  shows "->" where the others have an arrow glyph (formatting only).

FALSIFICATION: any assertion below failing.
"""
from sympy import isprime, prime

def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9

def rot_l(s):
    return s[1:] + s[0]

def rot_r(s):
    return s[-1] + s[:-1]

def cycle(s, f):
    out = [s]
    while f(out[-1]) != s:
        out.append(f(out[-1]))
    return out

def stackings(s):
    n, out = len(s), []
    for base in (s, s[::-1]):
        for st in cycle(base, rot_l):
            for f, name in ((rot_l, "L"), (rot_r, "R")):
                rows = cycle(st, f)
                g = [[int(c) for c in r] for r in rows]
                a = sum(g[i][i] for i in range(n))
                b = sum(g[i][n - 1 - i] for i in range(n))
                out.append((abs(a - b), a, b, st, name, rows))
    return sorted(out)

ROW9 = "".join(str(dr(prime(k))) for k in range(1, 10))
ROW10 = "2357114815"
assert ROW9 == "235724815" and sum(map(int, ROW9)) == 37 == sum(map(int, ROW10)) and isprime(37)
S9 = stackings(ROW9)
for _, a, b, _, _, rows in S9:
    g = [[int(c) for c in r] for r in rows]
    assert all(sum(r) == 37 for r in g) and all(sum(c) == 37 for c in zip(*g))
assert all(x[0] > 0 for x in S9) and not any(37 == 9 * int(d) for d in ROW9)
NEAR = [x for x in S9 if x[0] == 1]
assert len(NEAR) == 4 and all(sorted((x[1], x[2])) == [36, 37] for x in NEAR)
assert sorted((x[3], x[4]) for x in NEAR) == sorted([("427532518", "R"), ("481523572", "R"),
                                                    ("275325184", "L"), ("815235724", "L")])
assert all(int(x[5][4][4]) == 4 for x in NEAR)
S10 = stackings(ROW10)
assert all(x[0] > 0 for x in S10) and S10[0][0] == 2

def draw(path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(1, 2, figsize=(12, 6.4), facecolor="#0b1020")
    for ax, rows, title in ((axs[0], cycle(ROW9, rot_l), "prime row 235724815 turned 9 times"),
                            (axs[1], NEAR[0][5], "nearest balance: 4s diagonal 36 vs 37")):
        g = [[int(c) for c in r] for r in rows]
        ax.imshow(g, cmap="twilight", vmin=0, vmax=10)
        for i in range(9):
            for j in range(9):
                ax.text(j, i, g[i][j], ha="center", va="center", color="white", fontsize=13, weight="bold")
        ax.plot([-0.5, 8.5], [-0.5, 8.5], color="#ffb347", lw=2.5)
        ax.plot([8.5, -0.5], [-0.5, 8.5], color="#ffb347", lw=2.5)
        a, b = sum(g[i][i] for i in range(9)), sum(g[i][8 - i] for i in range(9))
        ax.set_title(f"{title}\nrows and columns 37; diagonals {a} and {b}", color="white", fontsize=10)
        ax.set_xticks([]); ax.set_yticks([])
    fig.savefig(path, dpi=140, bbox_inches="tight", facecolor=fig.get_facecolor())

assert [prime(1), prime(2)] == [2, 3] and prime(9) == 23 and str(prime(9)) == "23"
assert dr(prime(9)) == 2 + 3 == 5 and (dr(11), dr(13), dr(17), dr(19)) == (2, 4, 8, 1)
assert (2 + 3) + 5 + 7 + 2 + 4 + 8 + 1 + (2 + 3) == 37

from sympy import primerange
assert [dr(p) for p in primerange(1, 10)] == [2, 3, 5, 7] and [dr(p) for p in primerange(10, 20)] == [2, 4, 8, 1]
assert [p for p in primerange(1, 23) if dr(p) == 5] == [5] and 5 not in [dr(p) for p in primerange(10, 23)]
assert 7 not in [dr(p) for p in primerange(10, 20)] and dr(14) == 5 and not isprime(14)
assert list(primerange(20, 30)) == [23, 29] and (dr(23), dr(29)) == (5, 2) and dr(23 + 29) == 7
assert (2 + 2, dr(3 + 9)) == (4, 3) and isprime(43) and dr(43) == 7
assert [p for p in primerange(8, 60) if dr(p) == 7] == [43]
assert dr(43) + 5 + 2 == 14 and dr(14) == 5 and dr(43) + 2 == 9 and 9 + 5 == 14

R = 235724815
assert (2 * R, 4 * R, 3 * R) == (471449630, 942899260, 707174445)
assert [dr(R), dr(2 * R), dr(4 * R), dr(3 * R)] == [1, 2, 4, 3]
R10 = 2357114815
assert [dr(R10), dr(2 * R10), dr(4 * R10), dr(3 * R10)] == [1, 2, 4, 3]
DIG = [2, 3, 5, 7, 2, 4, 8, 1, 5]
assert (sum(DIG), sum(2 * d for d in DIG), sum(4 * d for d in DIG), sum(3 * d for d in DIG)) == (37, 74, 148, 111)
assert 111 == 3 * 37 and 148 == 4 * 37 and set(dr(3 * d) for d in DIG) <= {3, 6, 9}

def r9(a):
    return "".join(map(str, [dr(a), dr(a + 1), dr(2 * a + 1)] + [2 * a + 1 + 9 * j for j in range(1, 4)]))
LT = [(sum(map(int, r9(a))), 2 * sum(map(int, r9(a))), 4 * sum(map(int, r9(a))), 3 * sum(map(int, r9(a)))) for a in range(1, 10)]
assert LT[4] == (37, 74, 148, 111) and LT[7][3] == 147 and LT[8][3] == 123 and LT[3][3] == 135
assert all(t[2] - t[3] == t[0] for t in LT)
assert 147 - 111 == 36 and dr(36) == 9 and 148 - 111 == 37 and 246 + 111 == 357 and 369 - 111 == 258
assert (147 + 111, 258 + 111) == (258, 369)

from sympy import factorint
src = 'row = [2, 3, 5, 7, 2, 4, 8, 1, 5]\nR2 = int("".join(map(str, [dr(d) for d in row])))'
try:
    exec(src, {})
    raise AssertionError("pasted script should fail without dr")
except NameError:
    pass
assert int("".join(str(dr(d)) for d in DIG)) == 235724815 and not isprime(235724815)
assert factorint(235724815) == {5: 1, 23: 1, 971: 1, 2111: 1}

if __name__ == "__main__":
    for r in NEAR[0][5]:
        print(" ".join(r))
    draw("math/lemmas/figures/prime_row_ultimate_rotation.png")
    print("all assertions pass")
