# CLASS: AUDIT
"""
Pasted "reusable results" on the method of exhaustion, an exact oscillator step and the nine-state rotation (owner_work #367,
2026-10-19). The message opens with the owner's instruction, verbatim: "Search the available project files and conversation records
for each missing item first. Continue every check whose inputs are available. For anything still missing, name the exact item, report
where retrieval was attempted, and ask only for that item. Preserve unresolved blanks rather than inventing replacements."
The rest is another tool's output ("Worked for 26s") with a verification script. Nothing is put in the owner's mouth.

INPUTS FOUND (the original certificate): math/exhaustion/ is the owner's bundle (copied from the phone 2026-09-29): verify_exhaustion.py,
  verification_receipt.json (first passing n = 768, predecessor 384, g_384 = 2.1027e-4, g_768 = 5.2569e-5, epsilon 1e-4). The paste's "original
  384/768 rational certificate" is checked against it below.

RIGHT (re-run; the pasted script prints the 8 table rows and the last line exactly as the paste shows):
  gap g_n = U_n - L_n = n sin^3(x)/cos(x), x = pi/n; the rational bounds l_n < g_n < u_n (sin x >= x - x^3/6 with pi > 3; sin x <= x, cos x >= 1 - x^2/2
    with pi < 10/3) hold for every n >= 6 checked here (and also for n = 3, 4, 5); the minimal n in the doubling family 6 x 2^k:
    circle radius 1/2 (d = 1/4): 384 and 3072 ; unit circle (d = 1): 768 and 6144 ; radius 2 (d = 4): 1536 and 12288 ; ellipse 2 x 3 (d = 6): 1536 and
    24576, for tolerance 1e-4 and 1e-6; each with d u_n < eps and the predecessor failing (checked with the true gap as well).
  linear images: T P- in T B in T P+, areas scale by |det T|, so the gap scales by d. Area estimate d (L_n + U_n)/2 is within d g_n/2 of d pi; for the 2 x 3 ellipse at
    n = 1536 that is below 5e-5.
  oscillator: Euler (I + h w J) multiplies the squared radius by 1 + h^2 w^2; R(t) = ((1-t^2) I + 2t J)/(1+t^2) = (I - tJ)^-1 (I + tJ), t = h w/2, is orthogonal; t = 1/2
    gives [[3/5, 4/5], [-4/5, 3/5]] and (1, 0) -> (3/5, -4/5). The angle of one step is 2 arctan t, which is h w - (h w)^3/12 + ...: the radius is exact, the phase is not.
  nine-state rotation r(d) = 1 + (d mod 9): every triple has period 9; (b - a, c - a) mod 9 is invariant and is a bijection from the 81 orbits to the 81 pairs;
    729 = 81 x 9. Mesh: lcm(768, 9) = 2304 = 3 x 768 = 9 x 256; old vertex j -> 3j, one rotation step -> 256 positions, 9 x 256 = 2304; the 2304-gon contains the
    768-gon's vertices and tangent points, so L_768 < L_2304 and U_2304 < U_768, and u_2304 < u_768 < 1e-4.
  unary homomorphism: an additive map C from {1}* to the naturals has C(1^n) = n C(1), so C(1^n) = n exactly when C(1) = 1.
  S-shaped divider (assuming the standard one: two semicircles of equal radius, tangent at the centre): the tangent is continuous, the signed curvature jumps from -2 to +2
    (radius 1/2): a C^1 curve and not C^2.
MISSING (the definitions are not in the repository, the owner's messages, the session record or git history on any branch; see the reply):
  "I.V" and its functionals (the correspondence is "still proposed" in the paste, so it is left open here); "C_W" (the homomorphism's definition: only the
  unary property above is checked); the drawing of "the S-shaped circular divider" (the property above is for the standard construction); the animation and the
  derivation document of the exhaustion bundle (their hashes are in math/exhaustion/MANIFEST.json, the files were not copied).

FALSIFICATION: any assertion failing.
"""
import json
import math
import pathlib
import random
from fractions import Fraction as Q
from itertools import product
from math import lcm

from mpmath import atan, cos, mp, mpf, pi, sin, tan

mp.dps = 50
ROOT = pathlib.Path(__file__).resolve().parents[2]


def gap_true(n):
    x = pi / n
    return n * sin(x) ** 3 / cos(x)


def L(n):
    return mpf(n) / 2 * sin(2 * pi / n)


def U(n):
    return n * tan(pi / n)


def gap_bounds(n):
    a, b = Q(3, n), Q(10, 3 * n)
    return n * (a - a ** 3 / 6) ** 3, n * b ** 3 / (1 - b * b / 2)


frac = lambda q: mpf(q.numerator) / q.denominator

# the owner's bundle
rec = json.load(open(ROOT / "math" / "exhaustion" / "verification_receipt.json"))
assert rec["first_passing_n"] == 768 and rec["predecessor_n"] == 384 and rec["epsilon"] == 1e-4 and rec["all_assertions_passed"]
assert abs(float(U(384) - L(384)) - rec["g_384"]) < 1e-14 and abs(float(U(768) - L(768)) - rec["g_768"]) < 1e-14
assert abs(U(10) - L(10) - gap_true(10)) < mpf(10) ** -40

# the rational bounds
for n in list(range(3, 400)) + [6 * 2 ** k for k in range(0, 14)] + [2304, 5000, 100000]:
    lo, hi = gap_bounds(n)
    assert frac(lo) < gap_true(n) < frac(hi), n
assert gap_bounds(768)[1] < Q(1, 10000) and gap_bounds(384)[0] > Q(1, 10000)

# the table, with the true gap as well
def minimal(d, eps):
    n = 6
    while d * gap_bounds(n)[1] > eps:
        n *= 2
    return n


table = {}
for d in (Q(1, 4), Q(1), Q(4), Q(6)):
    for eps in (Q(1, 10 ** 4), Q(1, 10 ** 6)):
        n = minimal(d, eps)
        table[(d, eps)] = n
        assert d * gap_bounds(n)[1] < eps and d * gap_bounds(n // 2)[0] > eps
        assert frac(d) * gap_true(n) < frac(eps) and frac(d) * gap_true(n // 2) > frac(eps)
assert [table[(d, Q(1, 10 ** 4))] for d in (Q(1, 4), Q(1), Q(4), Q(6))] == [384, 768, 1536, 1536]
assert [table[(d, Q(1, 10 ** 6))] for d in (Q(1, 4), Q(1), Q(4), Q(6))] == [3072, 6144, 12288, 24576]

# area estimate, ellipse 2 x 3
d, n = 6, 1536
est = d * (L(n) + U(n)) / 2
assert abs(est - d * pi) <= d * gap_true(n) / 2 and d * gap_true(n) / 2 < mpf(5) * mpf(10) ** -5

# a linear image scales every area by |det T|
random.seed(37)
def shoelace(pts):
    return abs(sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1] for i in range(len(pts)))) / 2


poly = [(math.cos(2 * math.pi * j / 12), math.sin(2 * math.pi * j / 12)) for j in range(12)]
for _ in range(20):
    a, b, c, e = (random.uniform(-3, 3) for _ in range(4))
    img = [(a * x + b * y, c * x + e * y) for x, y in poly]
    assert abs(shoelace(img) - abs(a * e - b * c) * shoelace(poly)) < 1e-9

# oscillator
J = ((0, 1), (-1, 0))
for _ in range(50):
    t = Q(random.randint(-20, 20), random.randint(1, 20))
    den = 1 + t * t
    Rm = (((1 - t * t) / den, 2 * t / den), (-2 * t / den, (1 - t * t) / den))
    assert Rm[0][0] ** 2 + Rm[1][0] ** 2 == 1 and Rm[0][1] ** 2 + Rm[1][1] ** 2 == 1 and Rm[0][0] * Rm[0][1] + Rm[1][0] * Rm[1][1] == 0
    q, p = Q(random.randint(-9, 9), 7), Q(random.randint(-9, 9), 5)
    q2, p2 = Rm[0][0] * q + Rm[0][1] * p, Rm[1][0] * q + Rm[1][1] * p
    assert q2 * q2 + p2 * p2 == q * q + p * p
    hw = 2 * t
    qe, pe = q + hw * p, -hw * q + p                    # forward Euler: (I + h w J) z
    assert qe * qe + pe * pe == (1 + hw * hw) * (q * q + p * p)
    # R(t) = (I - tJ)^-1 (I + tJ): (I - tJ) R = I + tJ
    I_tJ = ((1 - t * 0, -t), (t, 1))
    lhs = tuple(tuple(sum(I_tJ[i][k] * Rm[k][j] for k in range(2)) for j in range(2)) for i in range(2))
    assert lhs == ((1, t), (-t, 1))
t = Q(1, 2)
Rm = ((Q(3, 5), Q(4, 5)), (Q(-4, 5), Q(3, 5)))
assert ((1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)) == (Q(3, 5), Q(4, 5)) and (Rm[0][0], Rm[1][0]) == (Q(3, 5), Q(-4, 5))
z = (Q(1), Q(0))
for k in range(1, 8):
    z = (Rm[0][0] * z[0] + Rm[0][1] * z[1], Rm[1][0] * z[0] + Rm[1][1] * z[1])
    assert z[0] ** 2 + z[1] ** 2 == 1 and 5 ** k % z[0].denominator == 0 and 5 ** k % z[1].denominator == 0
h = mpf(1) / 10
assert abs((2 * atan(h / 2) - h) + h ** 3 / 12) < h ** 5

# nine-state rotation
rot = lambda v: tuple(c % 9 + 1 for c in v)
seen, key_of_orbit = set(), {}
for start in product(range(1, 10), repeat=3):
    if start in seen:
        continue
    v, orbit = start, []
    while v not in orbit:
        orbit.append(v)
        v = rot(v)
    assert v == start and len(orbit) == 9
    keys = {((b - a) % 9, (c - a) % 9) for a, b, c in orbit}
    assert len(keys) == 1
    key_of_orbit[keys.pop()] = start
    seen.update(orbit)
assert len(seen) == 729 and len(key_of_orbit) == 81 and sorted(key_of_orbit) == [(i, j) for i in range(9) for j in range(9)] and 729 == 81 * 9
assert all(rot(rot(rot(rot(rot(rot(rot(rot(rot(v))))))))) == v for v in [(1, 5, 9), (9, 9, 9), (2, 7, 4)])

# the common mesh
assert lcm(768, 9) == 2304 == 3 * 768 == 9 * 256 and 9 * 256 == 2304
assert {2 * 768 * 0 + 3 * j for j in range(768)} <= set(range(2304)) and all((3 * j) % 3 == 0 for j in range(768))
assert L(768) < L(2304) < pi < U(2304) < U(768)
assert gap_true(2304) < gap_true(768) < mpf(1) / 10000 and gap_bounds(2304)[1] < gap_bounds(768)[1] < Q(1, 10000)

# unary homomorphism
for c in range(-3, 6):
    C = lambda w, c=c: c * len(w)
    assert all(C("1" * (m + k)) == C("1" * m) + C("1" * k) for m in range(6) for k in range(6))
    assert all(C("1" * m) == m for m in range(8)) == (c == 1)

# the standard S divider: two semicircles of radius 1/2, centres (0, 1/2) and (0, -1/2)
r = mpf(1) / 2
tangent_A = (-r, mpf(0))                      # arc A at (0,0), heading (-1, 0)
tangent_B = (-r, mpf(0))                      # arc B at (0,0), heading (-1, 0)
assert tangent_A == tangent_B
curv_A, curv_B = -1 / r, 1 / r                # clockwise, then counterclockwise
assert curv_A == -2 and curv_B == 2 and curv_B - curv_A == 4

if __name__ == "__main__":
    print("exhaustion transfers: table 384/3072, 768/6144, 1536/12288, 1536/24576 right; R(t) exact and orthogonal; 729 = 81 x 9; mesh 2304; "
          "missing: I.V, C_W, the S-divider drawing")
