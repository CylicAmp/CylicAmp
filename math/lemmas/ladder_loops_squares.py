# CLASS: LEMMA
"""
Loops drawn from the ladder rows, and the square on each (owner, 2026-10-04:
"draw the loops from each row and find the square").
Builds on square_peg_x.py (a square = an X with equal arms crossing at their
middles at right angles) and ladder_x_grid.py (the nine-digit rows).

CONSTRUCTION (a choice, stated so it can be changed): row a's digits
d_0..d_8 (DR(a) | DR(a+1) | DR(2a+1) | 2a+10 | 2a+19 | 2a+28) set the radius
1 + d_k at angle 2*pi*k/9, and a periodic cubic spline through those nine
points closes the loop. Where that spline would dip through the centre (only
row 36: 9118291100, ten digits, the 0, 0 next to the wrap to 9), the spline
is drawn through log(1 + d_k) instead, which passes through the same points
and stays positive. Each loop is smooth, so it must carry a square
(Schnirelmann); the search finds it as an X whose four ends lie on the curve.

Largest square found (side): row 1 3.644, row 2 4.213, row 3 5.002,
row 4 7.118, row 5 7.227, row 6 6.205, row 7 7.037, row 8 9.100, row 9 6.701.
Most loops carry several squares (rows 4, 5 and 9: five each found).

ROWS 10-36 (owner: "keep going to row 36 till we have the proof or not"):
every one of the 36 loops carries a square; largest side grows with the
digits, from 3.64 (row 1) to 13.76 (row 35); row 36 (ten digits) 4.87.
ROWS 8 AND 17 CARRY THE SAME SQUARE, MIRRORED: 898263544 read backwards
round the loop is 898445362 (reverse 445362898, start at the 898), so row 17's
loop is row 8's reflected and the squares match (side 9.0995251329, corner
radii 9.7227, 4.4786, 4.6669, 9.8108 in reverse order). It is the only such
pair in rows 1-36, and no row is its own mirror.

WHAT THIS RUN CAN AND CANNOT SHOW: every loop here is smooth, and every
smooth loop is already proved to carry a square (Schnirelmann 1929), so all
36 were guaranteed. The open square-peg case is non-smooth (corners, infinite
wiggling) continuous loops, which a smooth curve through digits never is.
Running more rows confirms the theorem on more loops; it cannot prove or
disprove the open case.
Results are in LARGEST (side length of the largest square found per row) and
the figure math/lemmas/figures/ladder_loops_squares.png. Different
constructions (other radii, other interpolation) give other loops and other
squares; the existence of a square does not depend on the choice.

FALSIFICATION: any assertion below failing.
"""
import math
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.optimize import fsolve

def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9

def row6(a):
    return "".join(map(str, [dr(a), dr(a + 1), dr(2 * a + 1)] + [2 * a + 1 + 9 * j for j in range(1, 4)]))

def make_loop(digits):
    th = np.linspace(0, 2 * math.pi, len(digits) + 1)
    rad = [1 + d for d in digits] + [1 + digits[0]]
    sp = CubicSpline(th, rad, bc_type="periodic")
    if min(sp(np.linspace(0, 2 * math.pi, 4000))) > 0.05:
        return lambda t: float(sp(t % (2 * math.pi)))
    lsp = CubicSpline(th, np.log(rad), bc_type="periodic")
    return lambda t: float(np.exp(lsp(t % (2 * math.pi))))

def find_squares(r):
    P = lambda t: np.array([r(t) * math.cos(t), r(t) * math.sin(t)])
    off = lambda x: float(np.hypot(*x)) - r(math.atan2(x[1], x[0]))
    def res(ts):
        p, q = P(ts[0]), P(ts[1])
        m, d = (p + q) / 2, (q - p) / 2
        j = np.array([-d[1], d[0]])
        return [off(m + j), off(m - j)]
    found = []
    for t1 in np.linspace(0, 2 * math.pi, 36, endpoint=False):
        for dt in (1.8, 2.4, 3.0, 3.5, 4.0):
            sol, _, ok, _ = fsolve(res, [t1, t1 + dt], full_output=True)
            if ok != 1 or max(map(abs, res(sol))) > 1e-10:
                continue
            p, q = P(sol[0]), P(sol[1])
            m, d = (p + q) / 2, (q - p) / 2
            j = np.array([-d[1], d[0]])
            C = [p, m + j, q, m - j]
            side = float(np.linalg.norm(C[1] - C[0]))
            if side > 0.5 and not any(abs(side - f[0]) < 1e-6 for f in found):
                found.append((side, C))
    return sorted(found, key=lambda f: -f[0])

def check_square(C, r):
    off = lambda x: float(np.hypot(*x)) - r(math.atan2(x[1], x[0]))
    s = [np.linalg.norm(C[i] - C[(i + 1) % 4]) for i in range(4)]
    d1, d2 = C[2] - C[0], C[3] - C[1]
    return (all(abs(off(c)) < 1e-9 for c in C) and max(s) - min(s) < 1e-9
            and abs(np.linalg.norm(d1) - np.linalg.norm(d2)) < 1e-9 and abs(float(d1 @ d2)) < 1e-8)

ROWS = {a: row6(a) for a in range(1, 37)}
LOOPS = {a: make_loop(list(map(int, s))) for a, s in ROWS.items()}
SQUARES = {a: find_squares(LOOPS[a]) for a in ROWS}
LARGEST = {a: round(SQUARES[a][0][0], 6) for a in ROWS}

for a in ROWS:
    assert min(LOOPS[a](t) for t in np.linspace(0, 2 * math.pi, 2000)) > 0
    assert SQUARES[a], f"no square found on row {a}"
    assert all(check_square(C, LOOPS[a]) for _, C in SQUARES[a])

assert {a: LARGEST[a] for a in range(1, 10)} == {1: 3.643522, 2: 4.213216, 3: 5.002141, 4: 7.118411,
                   5: 7.226726, 6: 6.205219, 7: 7.036868, 8: 9.099525, 9: 6.701184}

assert all(SQUARES[a] for a in range(1, 37))
assert abs(SQUARES[8][0][0] - SQUARES[17][0][0]) < 1e-9
def _rots(t):
    return {t[i:] + t[:i] for i in range(len(t))}
assert ROWS[17] in _rots(ROWS[8][::-1])
assert [(a, b) for a in ROWS for b in ROWS if a < b and len(ROWS[a]) == len(ROWS[b])
        and (ROWS[b] in _rots(ROWS[a]) or ROWS[b] in _rots(ROWS[a][::-1]))] == [(8, 17)]
assert (LARGEST[35], LARGEST[36]) == (13.758478, 4.873784) and ROWS[36] == "9118291100"

def draw(path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(6, 6, figsize=(18, 19), facecolor="#0b1020")
    for a, ax in zip(ROWS, axs.flat):
        r = LOOPS[a]
        t = np.linspace(0, 2 * math.pi, 600)
        ax.plot([r(x) * math.cos(x) for x in t], [r(x) * math.sin(x) for x in t], color="#9fc3ff", lw=1.8)
        side, C = SQUARES[a][0]
        for i, k in ((0, 2), (1, 3)):
            ax.plot([C[i][0], C[k][0]], [C[i][1], C[k][1]], color="#ffb347", lw=1.8)
        sq = np.array(C + [C[0]])
        ax.plot(sq[:, 0], sq[:, 1], color="#ffe7a8", lw=1, ls="--")
        for c in C:
            ax.plot(*c, "o", color="#fff3d0", ms=5)
        s = ROWS[a]
        ax.set_title(f"row {a}: {s}  side {side:.2f}", color="white", fontsize=8)
        ax.set_facecolor("#0b1020"); ax.set_aspect("equal"); ax.axis("off")
    fig.suptitle("Ladder rows as loops -- the X and its square on each", color="white")
    fig.savefig(path, dpi=130, bbox_inches="tight", facecolor=fig.get_facecolor())

if __name__ == "__main__":
    for a in ROWS:
        print(a, ROWS[a], "squares found:", len(SQUARES[a]), "largest side:", LARGEST[a])
    draw("math/lemmas/figures/ladder_loops_squares.png")
    print("all assertions pass")
