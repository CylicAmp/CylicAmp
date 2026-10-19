# CLASS: AUDIT
"""
The pasted note on updating pair sums of zeta-zero ordinates when one more zero is added (owner_work #363, 2026-10-19).
Third-party text ("Your update is correct ..."); the earlier message it answers is not in the repository. Nothing is put in the
owner's mouth.

RIGHT (every line re-run; the ordinates are math/lemmas/data/zeta_zeros_gamma_1_1000.json, double precision, and the same four
zeros from mpmath at 30 digits agree to 15 digits):
  P_f(m+1) = P_f(m) + sum of f(y - x_i), i = 1..m : the old pairs stay, the new pairs are y-x_1, ..., y-x_m.
  f = 1: P = C(m,2), the step is C(m+1,2) - C(m,2) = m ; m = 3: C(4,2) - C(3,2) = 6 - 3 = 3.
  f = d: gamma_9..gamma_12 give 28.519779447731 ; the new distances 8.441096815896, 6.672415219391, 3.475926219349 add to 18.589438254636 ;
         28.519779447731 - 18.589438254636 = 9.930341193095 (the three-zero total).
  f = d^2: sum over i<j of (x_j - x_i)^2 = m (sum x^2) - (sum x)^2 ; for the four zeros 165.853998967677 ;
         P_2(m+1) = P_2(m) + m y^2 - 2 y (sum x) + (sum x^2): from P_2(3) = 37.998695570024 it gives 165.853998967677.
  "four low-lying zeros do not establish RH or Montgomery's pair correlation": right, both are statements about all zeros / large heights.
NOTE: "zero ordinate" means the imaginary part gamma of a zero 1/2 + i gamma; that the real part is 1/2 is RH (checked by computation for the first
  10^13 zeros), and the identities do not use it: they hold for any numbers.
STANDING ANALYSIS (the owner's floor(gamma_n) mod 37 frame): floor(gamma_9..12) = 48, 49, 52, 56 = 11, 12, 15, 19 mod 37 (NEG_H, SA_ST_A, DARK_A, CAS_EXT).

FALSIFICATION: any assertion failing.
"""
import json
import pathlib
import random
from fractions import Fraction
from math import comb, floor

ROOT = pathlib.Path(__file__).resolve().parents[2]
G = json.load(open(ROOT / "math" / "lemmas" / "data" / "zeta_zeros_gamma_1_1000.json"))
x = [G[8], G[9], G[10], G[11]]                         # gamma_9 .. gamma_12
close = lambda a, b, tol=5e-13: abs(a - b) < tol

# the update rule, exact, for three choices of f
random.seed(37)
for f in (lambda d: Fraction(1), lambda d: d, lambda d: d * d):
    for _ in range(50):
        m = random.randint(2, 9)
        xs = sorted(Fraction(random.randint(0, 10 ** 6), 997) for _ in range(m + 1))
        old, y = xs[:m], xs[m]
        P = lambda v: sum(f(v[j] - v[i]) for i in range(len(v)) for j in range(i + 1, len(v)))
        assert P(old + [y]) == P(old) + sum(f(y - xi) for xi in old)
        S, Q = sum(old), sum(v * v for v in old)
        P2 = lambda v: sum((v[j] - v[i]) ** 2 for i in range(len(v)) for j in range(i + 1, len(v)))
        assert P2(old) == m * Q - S * S
        assert P2(old + [y]) == P2(old) + m * y * y - 2 * y * S + Q
assert comb(4, 2) - comb(3, 2) == 3 and all(comb(m + 1, 2) - comb(m, 2) == m for m in range(1, 50))

# the numbers in the note
pairs = [(i, j) for i in range(4) for j in range(i + 1, 4)]
P1 = sum(x[j] - x[i] for i, j in pairs)
P2 = sum((x[j] - x[i]) ** 2 for i, j in pairs)
assert close(P1, 28.519779447731) and close(P2, 165.853998967677)
new = [x[3] - x[0], x[3] - x[1], x[3] - x[2]]
assert [close(a, b) for a, b in zip(new, (8.441096815896, 6.672415219391, 3.475926219349))] == [True] * 3
assert close(sum(new), 18.589438254636) and close(P1 - sum(new), 9.930341193095)
S3, Q3, y = sum(x[:3]), sum(v * v for v in x[:3]), x[3]
P2_3 = sum((x[j] - x[i]) ** 2 for i in range(3) for j in range(i + 1, 3))
assert close(P2_3, 37.998695570024) and close(P2_3 + 3 * y * y - 2 * y * S3 + Q3, 165.853998967677, 1e-9)
assert close(4 * sum(v * v for v in x) - sum(x) ** 2, 165.853998967677, 1e-9)

# the same four zeros from mpmath, when it is installed
try:
    from mpmath import mp, zetazero
    mp.dps = 30
    for n in range(9, 13):
        assert abs(float(zetazero(n).imag) - G[n - 1]) < 1e-13
except ImportError:
    pass

assert [floor(v) for v in x] == [48, 49, 52, 56] and [floor(v) % 37 for v in x] == [11, 12, 15, 19]

if __name__ == "__main__":
    print("zeta pair sums: update rule exact; gamma_9..12: 28.519779447731, 165.853998967677; new distances add to 18.589438254636; all right")
