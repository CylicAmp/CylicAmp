# CLASS: AUDIT
"""
Audit of a supplied package (2026-10-04): src/qnm45/{core, s_pattern, cheeger42, bridges}.py and
tests/test_all_74.py. The code was run here. Mathematics only.

TESTS THAT PASS, AND WHY (all forced)
  Q1 lambda_+ - lambda_- = (2m^3 + m^2 - 1) - (m - 1) = m(2m - 1)(m + 1): an identity.
  Q2 lambda_+ mod 5 for m = 0..4 is [4, 2, 4, 2, 3]; it is never 0, so 5 | det G(m) exactly when
     5 | (m - 1), i.e. m = 1 mod 5 -- checked to m = 100 by the code, and for all m by the cycle.
  Q3 Gamma0(+)/Gamma0(-) = (3/2)/(1/2) = 3 -- the two constants are typed in; the "3:1 ratio" is the
     input, not a result.
  Q4 Both 14-cell shapes have 20 internal edges and perimeter 16 (also in
     polyomino14_cut_gram_supplied_audit_2026_10_04.py).
  Q5 DOMAIN_SIZE == 42 because the code sets BOUNDARY_REMOVED = 22; it checks a constant against
     itself. (The natural placements of the 26-node wave leave 41 cells -- dirichlet_cheeger_42 audit.)

TEST THAT FAILS
  Q6 test_unique_intersection_q19 asserts Q(1, 9) == 1538 == lambda_+(9). lambda_+(9) = 1538, but
     Q(1, 9) = 2 + 17*81 + 18 - 1 = 1396. Worse, Q(x, y) = 2x^2 + 2xy + 17y^2 - 1 NEVER equals 1538:
     the form is positive definite (discriminant 4 - 136 < 0), so |y| <= 9 and |x| <= 28 cover every
     candidate, and none works. The "unique intersection" has no solution at all.

NOT ESTABLISHED
  Q7 kemeny_constant_factor(m) = 14 / (2m + 1) is called a "closed-form hitting-time factor on the
     42-cell quotient" with no derivation; S_m returns the constant 14; omega0, kappa, Gamma_n,
     is_null are defined but unused by any test.
  Q8 The package is not in this repository; the file named test_all_74 contains 6 tests.
FALSIFICATION: any assertion failing.
"""
from fractions import Fraction

Q = lambda x, y: 2 * x * x + 17 * y * y + 2 * x * y - 1
lam = lambda m: (2 * m ** 3 + m ** 2 - 1, m - 1)
assert all(lam(m)[0] - lam(m)[1] == m * (2 * m - 1) * (m + 1) for m in range(-30, 30))   # Q1
assert [lam(m)[0] % 5 for m in range(5)] == [4, 2, 4, 2, 3]                               # Q2
assert all(((lam(m)[0] * lam(m)[1]) % 5 == 0) == (m % 5 == 1) for m in range(-200, 200))
assert Fraction(3, 2) / Fraction(1, 2) == 3                                               # Q3
assert 64 - 22 == 42                                                                     # Q5
assert lam(9)[0] == 1538 and Q(1, 9) == 1396                                             # Q6
assert 4 - 4 * 2 * 17 < 0
assert not [(x, y) for x in range(-40, 41) for y in range(-12, 13) if Q(x, y) == 1538]
assert all(Q(x, y) > 1538 for x in range(-200, 201) for y in (10, -10, 11, -11))
