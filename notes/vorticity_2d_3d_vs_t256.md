# The 2D/3D vorticity distinction, and what it does to T256

Written because a claim reached this session that spatial cutoffs and bounding
exponents "must be injected to prevent the linearized operator R(u,p) from
collapsing into a finite-time singularity." That is not how the 3D problem
works, and the reason why is the same fact that grades T256's vortex row.

---

## 1. The mathematics, verified symbolically

The vorticity equation for incompressible Navier-Stokes:

    D(omega)/Dt  =  (omega . grad) u  +  nu * lap(omega)
                    ^^^^^^^^^^^^^^^^
                    vortex stretching

**In 2D that term vanishes identically.** Take any stream function psi(x,y,t);
u = (psi_y, -psi_x, 0) is automatically divergence-free, and

    omega = (0, 0, -(psi_xx + psi_yy))

is purely out-of-plane. Since a 2D field has no z-dependence, omega_z * d/dz
annihilates every component:

    (omega . grad) u  =  [0, 0, 0]      identically, for ANY psi

(verified with sympy on a general unspecified psi, not a worked example.)

**In 3D it is generally nonzero.** For the divergence-free strain field
u = (x, y, -2z) with omega = (0,0,w0):

    (omega . grad) u  =  [0, 0, -2*w0]      nonzero whenever w0 != 0

That is axial strain amplifying vorticity — the stretching mechanism itself.

### What follows

- **2D:** with the stretching term absent, D(omega)/Dt = nu*lap(omega) is an
  advection-diffusion equation. It obeys a maximum principle, so ||omega||_inf
  cannot grow. Global regularity follows. This is classical (Leray 1933,
  Ladyzhenskaya).
- **3D:** the term is present and can amplify omega. Whether it does so
  without bound in finite time is **OPEN** — the Clay Millennium Problem,
  confirmed against claymath.org: six of seven remain unsolved, only Poincare
  is resolved.

### Two corrections to how this gets stated

1. **"In 2D vorticity is conserved" is imprecise.** It is materially conserved
   in 2D *Euler* (inviscid). In 2D Navier-Stokes it is advected AND diffused.
   What is exactly true — and is the sharper statement — is that the
   *stretching term* vanishes.
2. **You cannot prevent blowup by choosing cutoffs.** If a choice of spatial
   cutoff and bounding exponents settled 3D regularity, that would BE the
   proof. Relatedly, linearizing removes the difficulty rather than confronting
   it: the entire problem lives in the nonlinear (u . grad)u, and a linearized
   operator does not develop finite-time singularities. Singularities are also
   a property of *solutions*, not of operators.

What IS known in 3D, for completeness: global weak solutions exist (Leray
1934) but are not known to be unique or smooth; local-in-time strong solutions
exist; Beale-Kato-Majda says blowup at T requires the time-integral of
||omega||_inf to diverge; Caffarelli-Kohn-Nirenberg bounds the singular set's
parabolic Hausdorff dimension by 1.

---

## 2. What this does to T256

`math/theorems/pinn_rt_phase_field.py` (Theorem 256, "Discrete Phase-Field
Correspondence") maps GF(37)/the 137-map onto two-phase Navier-Stokes of
Rayleigh-Taylor class. Its correspondence table includes:

    Mushroom rollup (vortex struct.)   ->   3-cycles: ord_37(26) = 3

**Grade that row against T305's own cuts** (`theorem_305_claim_strength_cuts.py`),
whose CUT 1 gives as its example: *"structural: calling that 6-cycle 'discrete
curl'."* The vortex row is the same shape.

- **CUT 1, literal vs structural: STRUCTURAL.** A 3-cycle in (Z/37Z)* and a
  vortex are not the same object, nor is one a defined discretization of the
  other. Only a role is shared — "something that comes back around."
- **The decisive point:** the correspondence **cannot distinguish 2D from 3D.**
  ord_37(26) = 3 is a fact about a finite cyclic group. There is no discrete
  counterpart of (omega . grad)u, because there is no strain tensor and no
  dimension in which vorticity could be perpendicular or parallel to it. The
  2D/3D difference is the *entire* mathematical content of the regularity
  question, and a 3-cycle is blind to it.

So the vortex row is a level-1 correspondence at best, and it is blind on
precisely the axis that matters. That is not an argument against T256's other
rows — the phase-advection residual R1 in that file is a genuine, proved
statement about the 137-map (f(n) = 26n preserves chi_{-3} class when 3 does
not divide n, since gcd(26,3) = 1). It is an argument for keeping that row
labelled as analogy and never letting it carry weight about regularity.

---

## 3. The scope line worth keeping

Anything in this repo that reaches toward Navier-Stokes should say: the 2D
theory is settled and the mechanism is the vanishing of vortex stretching; the
3D theory is open and no discrete cyclic structure bears on it. A
correspondence that produces the same object in 2D and 3D has, by that fact,
said nothing about the only question anyone is asking.

---

## Reproduction

```bash
python3 - <<'EOF'
import sympy as sp
x,y,z,t = sp.symbols('x y z t')
psi = sp.Function('psi')(x,y,t)
u = sp.Matrix([sp.diff(psi,y), -sp.diff(psi,x), 0])
om = sp.Matrix([sp.diff(u[2],y)-sp.diff(u[1],z),
                sp.diff(u[0],z)-sp.diff(u[2],x),
                sp.diff(u[1],x)-sp.diff(u[0],y)])
st = sp.Matrix([sum(om[j]*sp.diff(u[i],(x,y,z)[j]) for j in range(3))
                for i in range(3)])
print([sp.simplify(c) for c in st])      # -> [0, 0, 0] for ANY psi
EOF
```
