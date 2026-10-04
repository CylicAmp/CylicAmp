# CLASS: AUDIT
"""
Audit of a supplied description (2026-10-04) of two images: a post on R. Singer, "The Myth of
Hamel's Paradox" (arXiv:2609.35857), and a plot of Forman curvature as shortcut edges are added.
The images themselves were not attached here; only the text is checked. Mathematics only.

HAMEL / CHAPLYGIN SLEIGH -- CORRECT
  H1 The preprint exists: arXiv:2609.35857, R. Singer, submitted 25 Sept 2026; its abstract says
     what the post says (substituting the constraint before forming Lagrange's equations is wrong
     in general; known since the 1890s -- Hadamard, Chaplygin, Hamel; legitimate when the
     constraint distribution is integrable).
  H2 Sleigh with contact point (x, y), heading theta, centre of mass a distance s ahead, mass m,
     inertia I about the centre of mass. In body coordinates the contact-point velocity is
     (u, w); the centre of mass moves at (u, w + s theta'), so
        T = (1/2) m (u^2 + (w + s theta')^2) + (1/2) I theta'^2,
     with cross term m s theta' w, and dT/dw at w = 0 is m s theta' -- nonzero, as stated.
  H3 Derived below with a Lagrange multiplier (sympy): the true equations are
        m u' = m s theta'^2          (the centrifugal term)
        (I + m s^2) theta'' = -m s u theta'   (the gyroscopic coupling)
     while Lagrange's equations on the substituted T(w = 0) give u' = 0 and theta'' = 0 -- both
     terms are lost, exactly as stated.

FORMAN CURVATURE PLOT -- the reported values follow from the formula
  F1 For an unweighted graph without 2-cells, F(e) = 4 - deg(u) - deg(v). On a 4-regular graph
     every edge starts at -4. One shortcut between two fresh vertices makes both degree 5: that
     edge is 4 - 10 = -6 (the first drop). An edge between a degree-6 vertex (two shortcuts) and a
     degree-5 vertex is -7 (the second step). Mean curvature falls as shortcuts add degree.
  F2 NOT CHECKED: the slope of the mean (-4 to about -5.1 over 20 shortcuts) depends on the graph
     size, which the description does not give (on the 8 x 8 torus, 20 shortcuts on distinct
     vertices would give -5.35).
FALSIFICATION: any assertion failing.
"""
import sympy as sp

t = sp.symbols("t")
m, s, I = sp.symbols("m s I", positive=True)
x, y, th, lam = [sp.Function(n)(t) for n in ("x", "y", "th", "lam")]
X, Y = x + s * sp.cos(th), y + s * sp.sin(th)
T = sp.Rational(1, 2) * m * (sp.diff(X, t) ** 2 + sp.diff(Y, t) ** 2) + sp.Rational(1, 2) * I * sp.diff(th, t) ** 2
a = {x: -sp.sin(th), y: sp.cos(th), th: 0}                       # no side slip: -x' sin + y' cos = 0
eqs = [sp.diff(sp.diff(T, sp.diff(q, t)), t) - sp.diff(T, q) - lam * a[q] for q in (x, y, th)]
u = sp.diff(x, t) * sp.cos(th) + sp.diff(y, t) * sp.sin(th)
# project the x, y equations onto the heading direction (eliminates lam)
along = sp.simplify(eqs[0] * sp.cos(th) + eqs[1] * sp.sin(th))
w0 = {sp.diff(y, t): sp.diff(x, t) * sp.tan(th)}                  # impose the constraint
along_c = sp.simplify(along.subs(sp.diff(y, t, 2), sp.diff(sp.diff(x, t) * sp.tan(th), t)).subs(w0))
du = sp.simplify(sp.diff(u, t).subs(sp.diff(y, t, 2), sp.diff(sp.diff(x, t) * sp.tan(th), t)).subs(w0))
uc = sp.simplify(u.subs(w0))
assert sp.simplify(along_c - m * (du - s * sp.diff(th, t) ** 2)) == 0                       # H3 u-equation
rot = sp.simplify(eqs[2].subs(sp.diff(y, t, 2), sp.diff(sp.diff(x, t) * sp.tan(th), t)).subs(w0))
assert sp.simplify(rot - ((I + m * s ** 2) * sp.diff(th, t, 2) + m * s * uc * sp.diff(th, t))) == 0   # H3 theta-equation

U, W, Om = sp.symbols("U W Om")
Tb = sp.Rational(1, 2) * m * (U ** 2 + (W + s * Om) ** 2) + sp.Rational(1, 2) * I * Om ** 2   # H2
assert sp.expand(Tb).coeff(W).coeff(Om) == m * s and sp.diff(Tb, W).subs(W, 0) == m * s * Om

F = lambda du_, dv_: 4 - du_ - dv_                                                            # F1
assert (F(4, 4), F(5, 5), F(6, 5)) == (-4, -6, -7)
Tdag = Tb.subs(W, 0)                     # substituted ("illegitimate") energy: depends on U, Om only
assert sp.expand(Tdag) == sp.expand(sp.Rational(1, 2) * m * U ** 2 + sp.Rational(1, 2) * (I + m * s ** 2) * Om ** 2)
assert not Tdag.free_symbols & {s * 0}   # no position dependence -> naive Lagrange gives m U' = 0, (I + m s^2) Om' = 0
