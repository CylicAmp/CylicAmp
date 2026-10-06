# CLASS: AUDIT
"""
Audit of a supplied HTML/JS dashboard (2026-10-06): a mod-9 carry table for
2a, a=0..9, and a "companion matrix spectrum" for P(x) = x^3 - x^2 - 2 --
the same dragon-boundary cubic audited in
dragon_boundary_supplied_audit_2026_10_06.py.

RESULT: the carry table's arithmetic is correct, but its "PHASE CHANGE"
tag at a=5 has no basis in the data it displays. The spectrum section's
matrix is correct, but its "computed" roots are not computed from it --
they are hardcoded values that solve a DIFFERENT polynomial.

FAULT 1 -- "PHASE CHANGE (a=5)" is not shown by the data.
  Mod 9 Preserved reads TRUE for every a = 0..9 (reproduced below), with no
  change in that column at a=5. The identity sum = 10*carry + d0 gives
  sum = carry + d0 (mod 9) for every a, since 10 = 1 (mod 9) -- this is
  forced by base 10, not something that starts being true at a=5. All that
  happens at a=5 is that 2a first reaches two digits (carry becomes 1); the
  table's own "Mod 9 Preserved" column does not register that as a change.

FAULT 2 -- the spectrum roots are hardcoded for the WRONG polynomial.
  The companion matrix shown is correct for x^3 - x^2 - 2 (verified: its
  characteristic polynomial is exactly that cubic). But the code does not
  diagonalize it. r1 = 2.0, r2 = -0.5 +- i*sqrt(3)/2 are the roots of
  x^3 - x^2 - x - 2 = (x-2)(x^2+x+1) -- a different polynomial, with an
  extra -x term. Checking the one that is actually labeled, x=2 does NOT
  satisfy x^3 - x^2 - 2 (gives 2, not 0).
  The true roots of x^3 - x^2 - 2 (sympy, and dragon_boundary_supplied_
  audit_2026_10_06.py, same session): real root 1.695621, complex pair
  -0.347810 +- 1.028852i. |complex root| = 1.086, not 1, so
  (lambda_2,3)^3 != 1: the "exact period-3 cyclic symmetry" claim is false
  for the polynomial the dashboard names. It is true only for the
  unrelated x^3 - x^2 - x - 2, which the dashboard never writes down.

FALSIFICATION: any assertion below failing.
"""
import cmath
import math
import sympy as sp

# --- Fault 1: reproduce the JS carry table exactly ---
def js_row(a):
    s = 2 * a
    carry = s // 10
    d0 = s % 10
    dr = 0 if s == 0 else 1 + ((s - 1) % 9)
    mod_preserved = (s % 9) == ((d0 + carry) % 9)
    return s, carry, d0, dr, mod_preserved

rows = [js_row(a) for a in range(10)]
assert all(r[4] for r in rows), "the dashboard's own column is TRUE for every a"
# the identity is forced by 10 = 1 (mod 9), for every integer a, not only a <= 9
for a in range(1000):
    s = 2 * a
    assert s % 9 == (s % 10 + s // 10) % 9
assert rows[5] == (10, 1, 0, 1, True)     # a=5's row is unremarkable among the ten

# --- Fault 2: the stated polynomial vs. the hardcoded roots ---
x = sp.symbols("x")
P = x**3 - x**2 - 2                        # the polynomial the dashboard names
WRONG_P = x**3 - x**2 - x - 2              # the polynomial the hardcoded roots solve

assert P.subs(x, 2) == 2 and WRONG_P.subs(x, 2) == 0     # 2 is a root of the wrong one only
assert sp.factor(WRONG_P) == (x - 2) * (x**2 + x + 1)

# the companion matrix as printed: char poly is exactly P, not WRONG_P
import sympy.matrices as sm
M = sm.Matrix([[0, 0, 2], [1, 0, 0], [0, 1, 1]])
lam = sp.symbols("lambda")
char = (lam * sm.eye(3) - M).det()
assert sp.expand(char - (lam**3 - lam**2 - 2)) == 0

true_roots = sorted(sp.nroots(P), key=lambda r: abs(complex(r).imag))
r1 = float(true_roots[0])
r2 = complex(true_roots[1])
assert abs(r1 - 1.695621) < 1e-5
assert abs(r2.real - (-0.347810)) < 1e-5 and abs(abs(r2.imag) - 1.028852) < 1e-5

dashboard_r1, dashboard_r2 = 2.0, complex(-0.5, math.sqrt(3) / 2)
assert abs(dashboard_r1 - r1) > 0.3            # the dashboard's "dominant mode" is wrong
assert abs(dashboard_r2 - r2) > 0.1

mag = abs(r2)
assert abs(mag - 1.086) < 1e-3 and abs(mag - 1) > 0.08     # not on the unit circle
assert abs(r2**3 - 1) > 0.2                                  # not a cube root of unity
assert abs(dashboard_r2**3 - 1) < 1e-9                        # true only for the OTHER polynomial

print("carry-spectrum dashboard audit: carry table arithmetic correct, 'PHASE")
print("CHANGE' tag unsupported by its own column; matrix correct, but its")
print("'computed roots' solve x^3-x^2-x-2, not the stated x^3-x^2-2. All assertions pass.")
