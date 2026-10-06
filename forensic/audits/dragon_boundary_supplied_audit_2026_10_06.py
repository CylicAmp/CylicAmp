#!/usr/bin/env python3
"""
Audit of supplied text (2026-10-06): "dragon boundary x^3 - x^2 - 2,
the n = 2 (mod 9) prime track, and the streamfunction oscillator", plus a
reply about a "page 14 cutoff" in an unnamed paper. Both were pasted from
another AI. The displayed equations were lost in the paste, so only claims
whose numbers survive in the text are checked here.

Prior art (outside the repo): the real root of x^3 - x^2 - 2 sets the
boundary dimension of the Knuth twindragon, 2*log2(lambda) = 1.5236
(Wikipedia, "List of fractals by Hausdorff dimension"; Akiyama, Grosskopf,
Loridant and Steiner, arXiv:2402.18371; boundary-dimension method from
Duvall and Keesling). Nothing in the repo used this polynomial before this file.
"""
import cmath
import math

from sympy import Poly, discriminant, factorint, symbols, factor_list, GF

x = symbols("x")
f = x**3 - x**2 - 2

# 1. Roots
roots = sorted(Poly(f).nroots(n=30), key=lambda r: abs(complex(r).imag))
l1 = float(roots[0])
l2 = complex(roots[1])
assert abs(l1 - 1.69562) < 1e-5
assert abs(l2.real - (-0.3478)) < 1e-4 and abs(abs(l2.imag) - 1.0288) < 1e-4
rho = abs(l2)
assert rho > 1 and abs(rho - math.sqrt(2 / l1)) < 1e-12        # |l2|^2 = 2/l1 (product of roots = 2)
phi = math.degrees(math.atan2(abs(l2.imag), l2.real))
assert abs(phi - 108.68) < 0.01                                  # supplied 108.68 deg: correct
dim = 2 * math.log2(l1)
assert abs(dim - 1.5236) < 1e-4                                  # known twindragon boundary dimension

# 2. Silver-ratio substitution: x^2 - 2x - 1 has root 1+sqrt2 = 2.414..., which is
#    not 1.69562. The text gives two different inflation rates for one boundary.
silver = 1 + math.sqrt(2)
assert abs(silver - l1) > 0.7

# 3. Discriminant: -116 = -2^2 * 29. Supplied "29" is correct.
D = discriminant(f, x)
assert D == -116 and factorint(-D) == {2: 2, 29: 1}

# 4. Is Z[theta] maximal at 2? Dedekind criterion.
#    f = x^2 (x+1) mod 2; g = x(x+1), h = x, F = (g*h - f)/2 = x^2 + 1 = (x+1)^2 mod 2.
#    gcd(F, g, h) mod 2 = 1, so 2 does not divide the index; field discriminant = -116.
g, h = x * (x + 1), x
F = Poly((g * h - f) / 2, x)
assert F == Poly(x**2 + 1, x)
assert Poly(f, x, modulus=2) == Poly(x**2 * (x + 1), x, modulus=2)
# 29 divides D exactly once, so Z[theta] is 29-maximal too.

# 5. Ramification: 2 = p^2 q and 29 = p^2 r, read off f mod p (Dedekind-Kummer).
fl2 = factor_list(f, modulus=2)[1]
fl29 = factor_list(f, modulus=29)[1]
assert sorted(e for _, e in fl2) == [1, 2]
assert sorted(e for _, e in fl29) == [1, 2]
# Supplied ramification pattern: correct.

# 6. "29 is not an accident ... third octave of the 9-boundary shifted by +2":
#    29 = 3*9 + 2 is only 29 = 2 (mod 9). The discriminant comes from the
#    coefficients of f and does not depend on base 10.
assert 29 % 9 == 2
#    Of the primes up to 200, a fixed proportion are 2 mod 9; that 29 is among
#    them carries no information about f.
from sympy import primerange
p2 = [p for p in primerange(5, 200) if p % 9 == 2]
assert 29 in p2 and len(p2) >= 7

# 7. "Dispersion relation: set nu * Laplacian(v) equal to ln(lambda1)":
#    nu*Lap(v) has units m/s^2; ln(lambda1) = 0.528 is dimensionless (per step).
#    The proposed equation is dimensionally inconsistent as stated.
assert abs(math.log(l1) - 0.528) < 1e-3

# 8. Page-14 cutoff remark (unnamed paper). Cutoffs chi(a_j q) with chi = 1 on
#    |q| <= c: chi(a_j q) = 1 on |q| <= c/a_j. All equal 1 on a common
#    neighbourhood iff inf_j c/a_j > 0, i.e. iff a_j is bounded. So "no single
#    neighbourhood" needs a_j -> infinity; "increasing" alone is not enough.
c = 1.0
bounded = [2 - 1 / (j + 1) for j in range(1000)]           # increasing, bounded by 2
unbounded = [j + 1 for j in range(1000)]                    # increasing, unbounded
assert min(c / a for a in bounded) > 0.5                    # common neighbourhood |q| <= 0.5 exists
assert min(c / a for a in unbounded) <= 1e-3                # shrinks toward 0

print("dragon boundary audit: roots, angle, discriminant, ramification correct;")
print("silver-ratio rate inconsistent; 29 mod 9 link and the dispersion relation unsupported;")
print("cutoff remark needs a_j unbounded, not just increasing. All assertions pass.")
