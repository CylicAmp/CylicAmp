# CLASS: LEMMA
"""
The square-peg problem as an X (owner, 2026-10-04: "we can make a X with
anything -- the X is like an inverted diamond or square").
Context: math/lemmas/digit_rule_2a_plus_b_1413.py (the 832 chain, written after
a video on the inscribed square problem).

THE REFORMULATION (exact): four points on a loop form a square exactly when
they are the four ends of an X whose two arms
    (1) cross at their common midpoint,
    (2) have equal length, and
    (3) are perpendicular.
(1)+(2) alone give a rectangle; (1)+(3) alone give a rhombus ("diamond");
all three give a square. Turned 45 degrees, the X's ends are a diamond.

WHAT IS KNOWN, BY WHICH ARMS OF THE X:
  (1)+(2), an X with equal arms bisecting each other, exists on EVERY closed
  loop, however wild: every Jordan curve has an inscribed rectangle
  (Vaughan, 1977; the proof pairs up chords by midpoint and length and uses
  a Mobius strip). So "we can make an X with anything" is a theorem, for the
  rectangle X.
  Adding (3), right angles, is the square-peg problem itself: proved for convex
  and for smooth loops, OPEN for general continuous loops.

DEMONSTRATED BELOW on a smooth blob r(t) = 1 + 0.3 cos 3t + 0.2 sin 2t: the
search finds an X whose four ends are on the curve to 1e-10, arms equal and
perpendicular -- an inscribed square -- and an X without the right angle
(a rectangle).

Figure: math/lemmas/figures/square_peg_x.png (the X in orange, the square dashed).

FALSIFICATION: any assertion below failing.
"""
import math
import numpy as np
from scipy.optimize import fsolve

def r(t):
    return 1 + 0.3 * math.cos(3 * t) + 0.2 * math.sin(2 * t)

def P(t):
    return np.array([r(t) * math.cos(t), r(t) * math.sin(t)])

def off_curve(x):
    return float(np.hypot(*x)) - r(math.atan2(x[1], x[0]))

def square_residual(ts):
    p, q = P(ts[0]), P(ts[1])
    m, d = (p + q) / 2, (q - p) / 2
    j = np.array([-d[1], d[0]])
    return [off_curve(m + j), off_curve(m - j)]

def find_square():
    best = None
    for t1 in np.linspace(0, 2 * math.pi, 24, endpoint=False):
        for dt in (2.0, 2.6, 3.1, 3.6):
            sol, info, ok, _ = fsolve(square_residual, [t1, t1 + dt], full_output=True)
            if ok != 1:
                continue
            p, q = P(sol[0]), P(sol[1])
            size = np.linalg.norm(q - p)
            if size > 0.5 and max(map(abs, square_residual(sol))) < 1e-10:
                if best is None or size > best[0]:
                    best = (size, sol)
    return best

def corners(sol):
    p, q = P(sol[0]), P(sol[1])
    m, d = (p + q) / 2, (q - p) / 2
    j = np.array([-d[1], d[0]])
    return [p, m + j, q, m - j]

best = find_square()
assert best is not None
C = corners(best[1])
assert all(abs(off_curve(c)) < 1e-9 for c in C)
sides = [np.linalg.norm(C[i] - C[(i + 1) % 4]) for i in range(4)]
diag1, diag2 = C[2] - C[0], C[3] - C[1]
assert max(sides) - min(sides) < 1e-9
assert abs(np.linalg.norm(diag1) - np.linalg.norm(diag2)) < 1e-9
assert abs(float(diag1 @ diag2)) < 1e-9
assert np.allclose((C[0] + C[2]) / 2, (C[1] + C[3]) / 2)

def rect_residual(ts, angle):
    p, q = P(ts[0]), P(ts[1])
    m, d = (p + q) / 2, (q - p) / 2
    c, s = math.cos(angle), math.sin(angle)
    e = np.array([c * d[0] - s * d[1], s * d[0] + c * d[1]])
    return [off_curve(m + e), off_curve(m - e)]

rect = None
for t1 in np.linspace(0, 2 * math.pi, 24, endpoint=False):
    sol, info, ok, _ = fsolve(lambda ts: rect_residual(ts, math.pi / 3), [t1, t1 + 3.0], full_output=True)
    if ok == 1 and max(map(abs, rect_residual(sol, math.pi / 3))) < 1e-10 and np.linalg.norm(P(sol[1]) - P(sol[0])) > 0.5:
        rect = sol
        break
assert rect is not None
p, q = P(rect[0]), P(rect[1])
m, d = (p + q) / 2, (q - p) / 2
e = np.array([math.cos(math.pi / 3) * d[0] - math.sin(math.pi / 3) * d[1],
              math.sin(math.pi / 3) * d[0] + math.cos(math.pi / 3) * d[1]])
R4 = [p, m + e, q, m - e]
rs = [np.linalg.norm(R4[i] - R4[(i + 1) % 4]) for i in range(4)]
assert abs(rs[0] - rs[2]) < 1e-9 and abs(rs[1] - rs[3]) < 1e-9 and abs(rs[0] - rs[1]) > 1e-3
assert all(abs(float((R4[(i + 1) % 4] - R4[i]) @ (R4[(i + 2) % 4] - R4[(i + 1) % 4]))) < 1e-9 for i in range(4))

if __name__ == "__main__":
    print("square corners:", [tuple(round(float(x), 6) for x in c) for c in C])
    print("side", round(sides[0], 6), "diagonals", round(float(np.linalg.norm(diag1)), 6), round(float(np.linalg.norm(diag2)), 6))
    print("rectangle sides", [round(float(x), 6) for x in rs])
    print("all assertions pass")
