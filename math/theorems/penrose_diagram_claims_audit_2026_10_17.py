# CLASS: AUDIT
"""
Audit of the pasted text on Penrose diagrams (owner_work #311, 2026-10-17). The paste is another tool's text, relayed by the
owner with no words of their own; it is checked, not attributed to the owner. Typos in the paste (one line each):
"l+" for I+ (future null infinity), "arows" for grows, "c 90 wedge" for a 90-degree wedge, "ose" for lose, "causa" for causal.

HOLDS -- reproduced below for Minkowski space (1+1, or the radial plane), the model case
  Put u = t - r, v = t + r, U = arctan u, V = arctan v. Then  -du dv = -(1/Omega^2) dU dV  with  Omega = cos U cos V  (identity checked
  symbolically), and with T = (U + V)/2, R = (V - U)/2:   ds^2 = Omega^-2 ( -dT^2 + dR^2 ).
  * "squeezed into a finite picture": U and V lie in (-pi/2, pi/2), so T and R are bounded: the whole plane becomes the diamond
    |T| + |R| < pi/2 (with r >= 0 only, the right half: a triangle).
  * "conformal rescaling ... shrinks distances by an amount that grows toward infinity": the factor Omega -> 0 as U or V -> +-pi/2
    (infinity); physical lengths are diagram lengths divided by Omega.
  * "light always travels at 45 degrees": null curves have dT = +-dR, slope exactly 1; "every light cone is a 90 degree wedge":
    the two null directions at a point are 90 degrees apart.
  * "anything with mass stays inside its cone, path leans more up than sideways": a worldline x = v t with |v| < 1 has
    |dR/dT| < 1 (checked for v = +-0.5, +-0.9, +-0.99 at several times); a null one has |dR/dT| = 1; a spacelike one has > 1.
  * "keep the causal structure perfectly": a conformal factor leaves the null cones, hence causal order, unchanged. True sizes
    (lengths, proper times) are lost.

NEEDS CARE (not faults)
  * The 45 degree rule is exact for RADIAL light rays. In 3+1 dimensions each point of the diagram is a 2-sphere, so sideways
    (angular) light is not drawn; such diagrams exist for spherically symmetric or 1+1 spacetimes, not for a general spacetime.
  * I+ is itself a 45 degree line in the Minkowski diagram (V = pi/2).
  * "preserving angles" means angles measured with the Lorentzian metric, not the angles of the picture; the picture's 45 degrees is a
    drawing convention that the conformal factor makes possible.
NOT SETTLED: what the owner wants with this text. The owner's earlier lines (#7, 2026-10-06: "I showed you how I make an X. I showed you
  how I made a diamond ...", owner_work/TERMS.md "M / W") use the shapes X and diamond; an X is the light cone through a point and the
  diamond is the Minkowski diagram. Whether that is meant is not stated.

FALSIFICATION: any assertion failing.
"""
import math
import sympy as sp

U, V, T, R, t, v = sp.symbols("U V T R t v", real=True)
Omega = sp.cos(U) * sp.cos(V)
assert sp.simplify(sp.diff(sp.tan(U), U) * sp.diff(sp.tan(V), V) - 1 / Omega ** 2) == 0          # -du dv = -Omega^-2 dU dV
dU, dV = sp.symbols("dU dV")
dT, dR = sp.symbols("dT dR")
assert sp.expand((dT - dR) * (dT + dR) - (dT ** 2 - dR ** 2)) == 0                               # U = T - R, V = T + R: dU dV = dT^2 - dR^2
assert sp.limit(Omega.subs(V, sp.Rational(1, 3)), U, sp.pi / 2) == 0 and sp.limit(Omega.subs(U, -sp.Rational(1, 5)), V, sp.pi / 2) == 0
# finite range: T +- R = U, V in (-pi/2, pi/2), so |T| + |R| < pi/2
for a in (-1.5, -0.4, 0.0, 0.9, 1.5):
    for b in (-1.5, -0.1, 0.3, 1.5):
        T_, R_ = (a + b) / 2, (b - a) / 2
        assert abs(T_) + abs(R_) < math.pi / 2 + 1e-12
# slopes dR/dT along x = v t, with T = (atan(t + x) + atan(t - x))/2, R = (atan(t + x) - atan(t - x))/2
x = v * t
Tt = (sp.atan(t + x) + sp.atan(t - x)) / 2
Rt = (sp.atan(t + x) - sp.atan(t - x)) / 2
slope = sp.simplify(sp.diff(Rt, t) / sp.diff(Tt, t))
for vv in (0.5, -0.5, 0.9, -0.9, 0.99, -0.99):
    for tt in (0.3, 1.0, 7.0, 40.0):
        assert abs(slope.subs({v: vv, t: tt})) < 1                                              # timelike: steeper than 45 degrees
for tt in (0.3, 1.0, 7.0):
    assert abs(float(slope.subs({v: 1, t: tt})) - 1) < 1e-12                                     # null: exactly 45 degrees
    assert abs(float(slope.subs({v: 1.5, t: tt}))) > 1                                           # spacelike: shallower than 45 degrees
# I+ is the line V = pi/2 with U fixed: dV = 0, so dT = -dR: a 45 degree line
T_scri, R_scri = (U + sp.pi / 2) / 2, (sp.pi / 2 - U) / 2                                         # points of I+: V = pi/2
assert sp.diff(R_scri, U) / sp.diff(T_scri, U) == -1                                            # slope -1: a 45 degree line

if __name__ == "__main__":
    print("Penrose diagram claims hold for Minkowski space: ds^2 = Omega^-2 (-dT^2 + dR^2), Omega = cos U cos V; null at 45 degrees, timelike steeper")
