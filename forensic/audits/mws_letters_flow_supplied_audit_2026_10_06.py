#!/usr/bin/env python3
"""
Audit of supplied text (2026-10-06): "M / W / S / X letters as container flow"
(M = peak, W = basin, S = inflection membrane, X = hyperbolic stagnation
point), built on psi(x,z) = K sin(pi x) sin(pi z) on [-1,1] x [0,1] and the
dragon cubic x^3 - x^2 - 2 (see dragon_boundary_supplied_audit_2026_10_06.py).
The paste is from another AI; its displayed equations for the S and X curves
and the vortex sheet were lost, so those are not checked.

Velocity convention: u = d(psi)/dz, w = -d(psi)/dx (incompressible).
"""
import math
import sympy as sp

x, z, K = sp.symbols("x z K", real=True)
psi = K * sp.sin(sp.pi * x) * sp.sin(sp.pi * z)
u, w = sp.diff(psi, z), -sp.diff(psi, x)

# 1. Stagnation points. Interior of [-1,1] x (0,1): only (+-1/2, 1/2).
#    sin(pi z) != 0 there, so cos(pi x) = 0 -> x = +-1/2, then cos(pi z) = 0 -> z = 1/2.
H = sp.hessian(psi, (x, z))
for xc in (sp.Rational(1, 2), -sp.Rational(1, 2)):
    pt = {x: xc, z: sp.Rational(1, 2)}
    assert u.subs(pt) == 0 and w.subs(pt) == 0
    assert sp.simplify(H.det().subs(pt)) == sp.pi**4 * K**2   # det > 0: elliptic (vortex centre)
# (0,0): a stagnation point, hyperbolic (det < 0) -- supplied "X is hyperbolic" holds there,
# but (0,0) lies on the wall z = 0, not in the interior. No interior X-point exists.
o = {x: 0, z: 0}
assert u.subs(o) == 0 and w.subs(o) == 0
assert sp.simplify(H.det().subs(o)) == -sp.pi**4 * K**2

# 2. Strain rate: S_xz = 0 everywhere; |S_xx| = K pi^2 |cos(pi x) cos(pi z)|.
#    Maximum at (0,0) -- true, but shared with (+-1,0), (0,1), (+-1,1).
Sxz = sp.simplify((sp.diff(u, z) + sp.diff(w, x)) / 2)
Sxx = sp.simplify(sp.diff(u, x))
assert Sxz == 0
assert sp.simplify(Sxx - K * sp.pi**2 * sp.cos(sp.pi * x) * sp.cos(sp.pi * z)) == 0

# 3. "Velocity jump between the M-cell and the W-cell creates a vortex sheet; Kelvin-Helmholtz
#    rolls it up." psi is smooth, so u and w are continuous across x = 0: there is no jump,
#    no vortex sheet, and no Kelvin-Helmholtz instability in the stated flow.
for f in (u, w):
    assert sp.simplify(sp.limit(f, x, 0, "+") - sp.limit(f, x, 0, "-")) == 0
# psi is a Laplacian eigenfunction (Lap psi = -2 pi^2 psi): vorticity is a linear function
# of psi, so this is a steady Euler flow.
assert sp.simplify(sp.diff(psi, x, 2) + sp.diff(psi, z, 2) + 2 * sp.pi**2 * psi) == 0

# 4. "Placing M directly against W without an interface results in infinite shear":
#    in psi the two cells meet at x = 0 with bounded gradients (|grad v| <= K pi^2).
assert sp.simplify(sp.diff(w, x).subs(x, 0)) == 0

# 5. "Mass cannot bypass the node without passing through the singularity": near a
#    hyperbolic point, linearised flow x' = s x gives arrival time ln(x0/x)/s -> infinity.
#    Fluid approaches the stagnation point along the separatrix but never reaches it.
s = math.pi**2   # strain rate at (0,0) for K = 1
t = [math.log(1 / eps) / s for eps in (1e-3, 1e-6, 1e-12)]
assert t[0] < t[1] < t[2] and t[2] > 2.7

# 6. "S boundary dimension 1.5236" vs "S = smooth inflection curve, d2x/dz2 = 0":
#    a smooth (C^2) curve has Hausdorff dimension 1. 1.5236 is the twindragon boundary.
#    The two descriptions of S contradict each other.
lam = max(r.real for r in [complex(v) for v in sp.Poly(sp.Symbol('y')**3 - sp.Symbol('y')**2 - 2).nroots()] if abs(r.imag) < 1e-12)
assert abs(2 * math.log2(lam) - 1.5236) < 1e-4 and 2 * math.log2(lam) != 1

# 7. Mod-9 table: {1,4,7} is the order-3 subgroup of (Z/9)^*; {1,2,4} is not a subgroup
#    (2*4 = 8). Neither set is derived from the flow; the table is an assignment.
units9 = [a for a in range(1, 9) if math.gcd(a, 9) == 1]
closed = lambda S: all((a * b) % 9 in S for a in S for b in S)
assert closed({1, 4, 7}) and not closed({1, 2, 4})

# 8. "W <-> lambda^-1 (binary contraction)": 1/1.69562 = 0.5898, not 1/2 and not
#    1/|-1+i| = 1/sqrt2 = 0.7071. The "binary" label does not match the number.
assert abs(1 / lam - 0.5898) < 1e-4 and abs(1 / lam - 0.5) > 0.08 and abs(1 / lam - 2**-0.5) > 0.1

print("letters-flow audit: X at (0,0) is hyperbolic but on the wall; strain max at (0,0) shared;")
print("no velocity jump / vortex sheet / KH in psi; fluid never passes a stagnation point;")
print("S both smooth and dim 1.5236 (contradiction); mod-9 sets and lambda^-1 label not derived.")
