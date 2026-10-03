# CLASS: AUDIT
"""
Audit of supplied text (2026-10-03): a correction of an earlier singular-series draft for
k-term prime arithmetic progressions, with replacement code
(tools/supplied/singular_series_interval_2026_10_03.py, verbatim).
The draft it corrects is not in this repo; its claims about the draft are not checkable here.

CORRECT (checked below)
  S1 General prime-tuple local factor (1 - nu_p/p) / (1 - 1/p)^k, with nu_p = 1 if p | d;
     nu_p = p if p <= k, p not | d; nu_p = k if p > k, p not | d.
  S2 log f_k(p) = -sum_{r>=2} (m^r - m)/(r p^r), m = k-1. The p^-2 coefficient is
     (k-1)(k-2)/2 and the p^-3 coefficient (k-1)(k-2)k/3 (sympy series).
  S3 The tail enclosure exp(-E_k(B)) < prod_{p>B} f_k(p) < 1 is valid: each f_k(p) < 1
     for p > k, the r >= 3 terms are bounded by m^3/(3 p^3 (1 - m/(B+1))), and
     sum_{p>B} p^-2 < 1/B, sum_{p>B} p^-3 < 1/(2B^2) (primes are a subset of integers).
     Checked against the actual product from 10^4 to 10^6.
  S4 Using Decimal throughout (no math.log / math.exp) is right.
  S5 Admissibility: k# | d AND gcd(a, k#) = 1 removes every obstruction from p <= k; k# | d
     alone does not (p | a and p | d makes every term divisible by p). The AP-27 record
     satisfies both (k = 27: 27# = 23#).
  S6 0.6601618158... is C_2 = prod_{p>2} p(p-2)/(p-1)^2, not 2*C_2.

WRONG
  W1 The p^-4 coefficient. Supplied: (k-1)(k^2+k-1)/4. Correct: (k-1)(k-2)(k^2-k+1)/4
     (from (m^4 - m)/4). E.g. k = 3: supplied 11/2, correct 7/2.
  W2 Section 1 says that taking d = k# "hence" gives
        S_k = 1/(2(k-1)) * prod_{p<=k} (1/p)(p/(p-1))^(k-1) * prod_{p>k} f_k(p).
     For FIXED d = k# the S1 factor at p <= k is (p/(p-1))^(k-1), with no 1/p and no
     1/(2(k-1)) -- the supplied text's own Section 8 table says so. The 1/p factors come
     from averaging over all d (p | d with probability 1/p), and 1/(2(k-1)) from counting
     progressions with terms <= N: the formula is the AP-COUNT constant (the constant in
     #{k-term prime APs <= N} ~ C_k N^2/(log N)^k), not the singular series of the
     d = k# pattern. The two differ by 2(k-1) * k#: for k = 3, 0.33008 vs 7.9219.
  W3 Section 6 is right that the number is C_2, but the corrected code does NOT produce
     C_2 at k = 3: it produces C_2 / 2 = 0.3300809... (checked). Under W2's fixed-d
     reading the value is 12 C_2.
  W4 "Certified" overstates two things: (a) Decimal rounding in the finite product is
     not enclosed (negligible at 80 digits, but not bounded); (b) the interval is wide --
     printing 15 places suggests far more than is certified. At B = 2*10^5 the width is
     1.7e-6 (k = 3) and 3.4e-3 (k = 10). The 1/B bound ignores that primes are sparse; an
     explicit prime-counting bound would narrow it by about a factor log B.

FALSIFICATION: any assertion failing.
"""
import math
import sys
from decimal import Decimal
from fractions import Fraction as F
from pathlib import Path

import sympy as sp
from sympy import isprime, primerange

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools" / "supplied"))
import singular_series_interval_2026_10_03 as sup

# S2 + W1: coefficients of -log f
x, m, k = sp.symbols("x m k", positive=True)
ser = sp.series(sp.log(1 - m * x) - m * sp.log(1 - x), x, 0, 6).removeO()
coef = {r: sp.factor(sp.expand(-ser.coeff(x, r)).subs(m, k - 1)) for r in range(2, 5)}
assert sp.simplify(coef[2] - (k - 1) * (k - 2) / 2) == 0
assert sp.simplify(coef[3] - (k - 1) * (k - 2) * k / 3) == 0
assert sp.simplify(coef[4] - (k - 1) * (k - 2) * (k**2 - k + 1) / 4) == 0
assert sp.simplify(coef[4] - (k - 1) * (k**2 + k - 1) / 4) != 0                 # W1
assert coef[4].subs(k, 3) == sp.Rational(7, 2) and ((k - 1) * (k**2 + k - 1) / 4).subs(k, 3) == sp.Rational(11, 2)


def f(kk, p):
    return (1 - F(kk - 1, p)) * F(p, p - 1) ** (kk - 1)


# S1: nu_p by direct count of residues of {0, d, ..., (k-1)d}
def nu(kk, d, p):
    return len({(j * d) % p for j in range(kk)})
for kk in range(2, 9):
    for p in (2, 3, 5, 7, 11, 13):
        for d in (p, 1):
            want = 1 if d % p == 0 else (p if p <= kk else kk)
            assert nu(kk, d, p) == want

# S3: the tail bound holds on the stretch 10^4 < p <= 10^6 (a lower bound on the full tail
# must also lie below this partial product, since every factor is < 1)
for kk in (3, 5, 10):
    B = 10 ** 4
    logpart = sum(math.log1p(-(kk - 1) / p) - (kk - 1) * math.log1p(-1 / p)
                  for p in primerange(B + 1, 10 ** 6))
    lo, hi = sup.rigorous_tail_interval(kk, B, 40)
    assert float(lo.ln()) < logpart < 0, (kk, float(lo.ln()), logpart)
    assert all(f(kk, p) < 1 for p in primerange(kk + 1, 2000))

# S5: AP-27 admissibility
A27, D27 = 224584605939537911, 81292139 * 223092870
assert sp.primorial(9) == math.prod(primerange(2, 28))
assert all(D27 % p == 0 for p in primerange(2, 28)) and math.gcd(A27, 223092870) == 1
assert all(len({(1 * 0 + j * 1) % p for j in range(27)}) == p for p in primerange(2, 28))  # p not|d covers all residues

# S6, W2, W3: values
C2 = 1.0
for p in primerange(3, 2 * 10 ** 6):
    C2 *= p * (p - 2) / (p - 1) ** 2
assert abs(C2 - 0.6601618158) < 1e-6
head3, lo3, hi3 = sup.compute_singular_series_interval(3, B=200_000, precision=40)
assert head3 == F(3, 8)
assert float(lo3) < C2 / 2 < float(hi3) + 1e-6                              # W3: C_2/2
assert not (float(lo3) <= C2 <= float(hi3))
fixed_d_k3 = 4 * F(9, 4) * F(4, 3)                                           # prod_{p<=3}(p/(p-1))^2 / f(3)
assert fixed_d_k3 == 12
assert abs(float(fixed_d_k3) * C2 / (float(lo3) + float(hi3)) * 2 - 2 * (3 - 1) * 6) < 1e-3   # ratio 2(k-1)*k# = 24

# W4: widths
h10, lo10, hi10 = sup.compute_singular_series_interval(10, B=200_000, precision=40)
assert 1e-6 < float(hi3 - lo3) < 2e-6 and 3e-3 < float(hi10 - lo10) < 4e-3

if __name__ == "__main__":
    print("p^-4 coefficient: (k-1)(k-2)(k^2-k+1)/4, not (k-1)(k^2+k-1)/4")
    print(f"k=3 code value {float(lo3):.7f}..{float(hi3):.7f} = C_2/2 = {C2/2:.7f} (AP-count constant)")
    print(f"fixed d = 3# singular series = 12 C_2 = {12*C2:.4f}")
    print(f"interval widths at B=2e5: k=3 {float(hi3-lo3):.1e}, k=10 {float(hi10-lo10):.1e}")
