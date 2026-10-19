# CLASS: AUDIT
"""
A pasted analysis of a "verification suite" (owner_work #364, 2026-10-19). Third-party text; the suite, its "Claim [7]" and its
report are not in the message, so what is checked is the mathematics the text states. Nothing is put in the owner's mouth.

RIGHT:
  (Z/37)* has order 36 ; 2 generates it ; 26x26=676=10, 26x26x26=1, so the order-3 orbit is {1, 26, 10}
  18 quadratic residues and 18 non-residues ; each set sums to 333 ; 3+3+3=9
  twin pair (18x-1, 18x+1), centre 18x ; if Q is the upper twin 18x+1 then C+Q = 36x+1 ; 2(36x+1)+7 = 72x+9 = 9(8x+1)
  M = [[1,1],[3,7]], det = 7-3 = 4 ; S=12, R=-8, C=-4, D=4 ; det = (SD-RC)/4 = (48-32)/4 = 4 (proved below)
  the Note is right: S^2-R^2-C^2-D^2 = 144-64-16-16 = 48, not 4 det = 16; it is not an identity
  130 = 2x5x13 ; 1+4+25+100 = 130
  gamma_9, gamma_10, gamma_11 = 48.005, 49.774, 52.971 are inside [48, 53] ; gamma_12 = 56.446
WRONG:
  "Its inverse pair is 11 ({1, 11, 10})": 26 x 10 = 260 = 7x37+1, so 26 and 10 are each other's inverse. 11 = 37-26 is the NEGATIVE of
    26 and has order 6 (11x11x11 = 36 = -1). {1, 11, 10} is not a subgroup.
  "the unique divisor solution": 130 is the only solution at k = 4 (T245, proved). Over all k there are more: 1860 (k = 11) and 148480 (k = 19).
FORCED (true without any twin prime, any 37 or any zeta zero):
  72x+9 = 9(8x+1) has digital root 9 for every x, prime pair or not.
  333: 37 = 1 mod 4, so -1 is a residue, the residues pair up as r and 37-r, and their sum is 18 x 37/2 = 333; the non-residues pair up too.
  (For p = 3 mod 4 the two sums differ: p = 7 gives 7 and 14.)
CAN'T CHECK:
  "Claim [7]", "the report", "the script verifies": none of them is in the message.
  "Automata & Regular Languages (REG)" and "Deterministic Polynomial / PSPACE": no complexity class attaches to one fixed finite check
    (the same note as for the Egor panel, dashboards/egor_checks/index.html); "sieve verification up to x = 500 ... match analytic
    expectations": no figures are given.

FALSIFICATION: any assertion failing.
"""
import json
import pathlib
import random
from fractions import Fraction

from sympy import n_order, primerange

ROOT = pathlib.Path(__file__).resolve().parents[2]
P = 37
assert n_order(2, P) == 36 and sorted(pow(2, k, P) for k in range(36)) == list(range(1, 37))
assert 26 * 26 % P == 10 and 26 ** 3 % P == 1 and sorted({1, 26, 10}) == sorted({pow(26, k, P) for k in range(3)})
assert 26 * 10 % P == 1 and (11 * 26) % P != 1 and 11 + 26 == 37 and n_order(11, P) == 6 and pow(11, 3, P) == 36
assert {pow(11, k, P) for k in range(6)} != {1, 11, 10} and n_order(10, P) == n_order(26, P) == 3

QR = {x * x % P for x in range(1, P)}
QNR = set(range(1, P)) - QR
assert len(QR) == len(QNR) == 18 and sum(QR) == sum(QNR) == 333 and 3 + 3 + 3 == 9
assert 18 * 37 // 2 == 333 and all((P - r) in QR for r in QR)
for p in primerange(5, 200):
    qr = {x * x % p for x in range(1, p)}
    s1, s2 = sum(qr), sum(set(range(1, p)) - qr)
    assert (s1 == s2 == p * (p - 1) // 4) if p % 4 == 1 else s1 != s2
assert sum({x * x % 7 for x in range(1, 7)}) == 7 and sum(set(range(1, 7)) - {x * x % 7 for x in range(1, 7)}) == 14

for x in range(0, 2000):
    C, Q = 18 * x, 18 * x + 1
    assert C + Q == 36 * x + 1 and 2 * (36 * x + 1) + 7 == 72 * x + 9 == 9 * (8 * x + 1)

# Hadamard coefficients and the determinant
def coeffs(a, b, c, d):
    return a + b + c + d, a + b - c - d, a - b + c - d, a - b - c + d


S, R, C, D = coeffs(1, 1, 3, 7)
assert (S, R, C, D) == (12, -8, -4, 4) and 7 - 3 == 4 and (S * D - R * C) // 4 == 4 and (S * D - R * C) % 4 == 0
assert S * S - R * R - C * C - D * D == 48 != 4 * 4
random.seed(37)
for _ in range(200):
    a, b, c, d = (Fraction(random.randint(-50, 50)) for _ in range(4))
    S, R, C, D = coeffs(a, b, c, d)
    assert a * d - b * c == (S * D - R * C) / 4
    assert S * S - R * R - C * C - D * D == 4 * (a + b) * (c + d) - 2 * (a - b) ** 2 - 2 * (c - d) ** 2

# divisor squares
assert 130 == 2 * 5 * 13 and 1 + 4 + 25 + 100 == 130
assert 1860 == 1 + 4 + 9 + 16 + 25 + 36 + 100 + 144 + 225 + 400 + 900

# the zeros
G = json.load(open(ROOT / "math" / "lemmas" / "data" / "zeta_zeros_gamma_1_1000.json"))
g9, g10, g11, g12 = G[8], G[9], G[10], G[11]
assert all(48 <= g <= 53 for g in (g9, g10, g11)) and round(g12, 3) == 56.446 and [round(g, 3) for g in (g9, g10, g11)] == [48.005, 49.774, 52.970]

if __name__ == "__main__":
    print("pasted suite analysis: arithmetic right; wrong: 11 is the negative of 26, not its inverse (26x10=260=7x37+1); "
          "130 is unique only at k=4; 72x+9 and 333 are forced; det = (SD-RC)/4 proved")
