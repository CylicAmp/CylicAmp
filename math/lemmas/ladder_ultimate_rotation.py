# CLASS: LEMMA
"""
The ultimate rotation run on the ladder rows (owner, 2026-10-05).
Builds on ultimate_rotation_1_9.py (123456789 turned through its 9-cycle,
stacked 9x9, X balanced at 45 with 5 at the centre) and ladder_x_grid.py
(the nine-digit rows DR(a) | DR(a+1) | DR(2a+1) | 2a+10 | 2a+19 | 2a+28).

THE RULE (proved for any row of n digits, n odd, here n = 9 and n = 5): stack
the n turns of the row. Every row and column then sums to S, the digit sum.
One diagonal repeats a single digit d (n copies, sum n*d); the other passes
through every position once (because 2 has an inverse mod n), sum S. So the X
balances exactly when S = n*d for a digit d that is in the row; d sits at the
centre.

NINE-DIGIT ROWS 1-9 (sums 15, 25, 35, 45, 37, 29, 39, 49, 41):
  Only row 4, 459182736, balances -- S = 45 = 9 x 5 and 5 is in it. Row 4 is
  also the only row whose nine digits are 1..9 each once: the ultimate
  rotation, scrambled. Four balanced grids, all with 5 at the centre (one grid
  with its mirror, flip and double mirror). Row 4 is the all-nines row again
  (chain 9, 18, 27, 36, 45; DR of every grid line 9).
  Over all nine-digit rows (1-35) exactly four balance: rows 4, 13, 22, 31 --
  every ninth row, all opening 459, all with digit sum exactly 45 and a 5:
  459182736, 459364554, 459546372, 459728190. Only row 4 uses each of 1..9 once.
FIVE-DIGIT ROWS 1-9 (12312 ... 91128): only row 2, 23514, balances -- S = 15 =
  5 x 3 and 3 is in it; centre 3.
ROW 36 (owner: "keep going to row 36"): 9118291100 has ten digits, sum 32; 32
  is not 10 x a digit, so no stacking balances (and with n even the
  through-every-position argument fails anyway).
Figure: math/lemmas/figures/ladder_ultimate_rotation_row4.png.

FALSIFICATION: any assertion below failing.
"""
def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9

def row9(a):
    return "".join(map(str, [dr(a), dr(a + 1), dr(2 * a + 1)] + [2 * a + 1 + 9 * j for j in range(1, 4)]))

def row5(a):
    return f"{dr(a)}{dr(a + 1)}{dr(2 * a + 1)}{2 * a + 10}"

def rot_l(s):
    return s[1:] + s[0]

def rot_r(s):
    return s[-1] + s[:-1]

def cycle(s, f):
    out = [s]
    while f(out[-1]) != s:
        out.append(f(out[-1]))
    return out

def balanced(s):
    n, S, out = len(s), sum(map(int, s)), []
    for st in sorted(set(cycle(s, rot_l)) | set(cycle(s[::-1], rot_l))):
        for f in (rot_l, rot_r):
            rows = cycle(st, f)
            if len(rows) != n:
                continue
            g = [[int(c) for c in r] for r in rows]
            assert all(sum(r) == S for r in g) and all(sum(c) == S for c in zip(*g))
            a, b = sum(g[i][i] for i in range(n)), sum(g[i][n - 1 - i] for i in range(n))
            assert len({g[i][i] for i in range(n)}) == 1 or len({g[i][n - 1 - i] for i in range(n)}) == 1
            if a == b == S:
                out.append(rows)
    return out

def rule(s):
    n, S = len(s), sum(map(int, s))
    return S % n == 0 and str(S // n) in s

assert [sum(map(int, row9(a))) for a in range(1, 10)] == [15, 25, 35, 45, 37, 29, 39, 49, 41]
assert [a for a in range(1, 10) if balanced(row9(a))] == [4]
assert row9(4) == "459182736" and sorted(row9(4)) == list("123456789")
assert [a for a in range(1, 36) if sorted(row9(a)) == list("123456789")] == [4]
B4 = balanced(row9(4))
assert len(B4) == 4 and all(int(r[4][4]) == 5 for r in B4)
G = B4[0]
assert sorted([G, [r[::-1] for r in G], G[::-1], [r[::-1] for r in G[::-1]]]) == sorted(B4)
BAL9 = [a for a in range(1, 36) if len(row9(a)) == 9 and balanced(row9(a))]
assert BAL9 == [4, 13, 22, 31] and all(row9(a)[:3] == "459" and sum(map(int, row9(a))) == 45 for a in BAL9)
assert [row9(a) for a in BAL9] == ["459182736", "459364554", "459546372", "459728190"]
for a in range(1, 36):
    assert bool(balanced(row9(a))) == rule(row9(a))
assert [a for a in range(1, 10) if balanced(row5(a))] == [2] and row5(2) == "23514"
assert all(int(r[2][2]) == 3 for r in balanced("23514"))
for a in range(1, 30):
    assert bool(balanced(row5(a))) == rule(row5(a))
assert row9(36) == "9118291100" and sum(map(int, row9(36))) == 32 and not balanced(row9(36))

def draw(path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(1, 2, figsize=(12, 6.4), facecolor="#0b1020")
    for ax, rows, title in ((axs[0], cycle("459182736", rot_l), "ladder row 4: 459182736 turned 9 times"),
                            (axs[1], G, "row 4 balanced: every line = 45, centre 5")):
        g = [[int(c) for c in r] for r in rows]
        ax.imshow(g, cmap="twilight", vmin=0, vmax=10)
        for i in range(9):
            for j in range(9):
                ax.text(j, i, g[i][j], ha="center", va="center", color="white", fontsize=13, weight="bold")
        ax.plot([-0.5, 8.5], [-0.5, 8.5], color="#ffb347", lw=2.5)
        ax.plot([8.5, -0.5], [-0.5, 8.5], color="#ffb347", lw=2.5)
        a, b = sum(g[i][i] for i in range(9)), sum(g[i][8 - i] for i in range(9))
        ax.set_title(f"{title}\ndiagonals {a} and {b}", color="white", fontsize=10)
        ax.set_xticks([]); ax.set_yticks([])
    fig.savefig(path, dpi=140, bbox_inches="tight", facecolor=fig.get_facecolor())

if __name__ == "__main__":
    print("balanced nine-digit rows 1-35:", BAL9)
    for r in G:
        print(" ".join(r))
    draw("math/lemmas/figures/ladder_ultimate_rotation_row4.png")
    print("all assertions pass")
