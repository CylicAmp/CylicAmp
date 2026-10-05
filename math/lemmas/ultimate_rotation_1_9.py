# CLASS: LEMMA
"""
The ultimate rotation (owner, 2026-10-05: "build out the ultimate rotation where
you go through one through nine, going through the whole cycle. I would like to
see what that looks like"). Builds on rotation_grids_x.py (rotation grids, the
balanced X, mirrors) and its 1..9 fold.

THE CYCLE: 123456789 turned one place at a time returns after nine turns:
    123456789 234567891 345678912 456789123 567891234
    678912345 789123456 891234567 912345678 -> 123456789
  Every turn keeps the digit sum 45 (so every one is divisible by 9).

THE 9x9 GRID: stacking the nine turns puts every digit once in every row and
every column -- all rows and columns sum to 45. One diagonal repeats a single
digit (9 copies); the other runs through all nine (sum 45).
THE BALANCED X (proved, as for 246): the repeated diagonal sums to 9d, so the X
balances at 45 exactly when d = 5, the middle digit. Then every row, column
and both diagonals are 45. Of the 36 stackings (9 starts x 2 directions, for
123456789 and for its mirror 987654321), exactly 4 do it -- starting
678912345 turning left, 567891234 turning right, and their mirrors
432198765 left, 543219876 right -- and they are one grid with its mirror,
flip and double mirror. All four have 5 at the centre.
Figure: math/lemmas/figures/ultimate_rotation_1_9.png (left: the cycle from
123456789; right: the balanced grid, X marked).

FALSIFICATION: any assertion below failing.
"""
def rot_l(s):
    return s[1:] + s[0]

def rot_r(s):
    return s[-1] + s[:-1]

def cycle(s, f):
    out = [s]
    while f(out[-1]) != s:
        out.append(f(out[-1]))
    return out

def grid(rows):
    return [[int(c) for c in r] for r in rows]

def diags(g):
    n = len(g)
    return sum(g[i][i] for i in range(n)), sum(g[i][n - 1 - i] for i in range(n))

CYCLE = cycle("123456789", rot_l)
assert CYCLE == ["123456789", "234567891", "345678912", "456789123", "567891234",
                 "678912345", "789123456", "891234567", "912345678"]
assert rot_l(CYCLE[-1]) == CYCLE[0] and all(int(x) % 9 == 0 for x in CYCLE)

BAL = []
for base in ("123456789", "987654321"):
    for st in cycle(base, rot_l):
        for f in (rot_l, rot_r):
            rows = cycle(st, f)
            g = grid(rows)
            assert all(sum(r) == 45 for r in g) and all(sum(c) == 45 for c in zip(*g))
            a, b = diags(g)
            assert len({g[i][i] for i in range(9)}) == 1 or len({g[i][8 - i] for i in range(9)}) == 1
            if a == b == 45:
                BAL.append(rows)
assert len(BAL) == 4 and all(grid(r)[4][4] == 5 for r in BAL)
G = cycle("678912345", rot_l)
FAM = [G, [r[::-1] for r in G], G[::-1], [r[::-1] for r in G[::-1]]]
assert sorted(FAM) == sorted(BAL)

def draw(path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(1, 2, figsize=(12, 6.4), facecolor="#0b1020")
    for ax, rows, title in ((axs[0], CYCLE, "the whole cycle: 123456789 turned 9 times"),
                            (axs[1], G, "balanced X: every row, column, diagonal = 45")):
        g = grid(rows)
        ax.imshow(g, cmap="twilight", vmin=0, vmax=10)
        for i in range(9):
            for j in range(9):
                ax.text(j, i, g[i][j], ha="center", va="center", color="white", fontsize=13, weight="bold")
        ax.plot([-0.5, 8.5], [-0.5, 8.5], color="#ffb347", lw=2.5)
        ax.plot([8.5, -0.5], [-0.5, 8.5], color="#ffb347", lw=2.5)
        a, b = diags(g)
        ax.set_title(f"{title}\ndiagonals {a} and {b}", color="white", fontsize=10)
        ax.set_xticks([]); ax.set_yticks([])
    fig.savefig(path, dpi=140, bbox_inches="tight", facecolor=fig.get_facecolor())

if __name__ == "__main__":
    for r in G:
        print(" ".join(r))
    draw("math/lemmas/figures/ultimate_rotation_1_9.png")
    print("all assertions pass")
