# The 2D/3D vorticity distinction, and what it does to T418

Written because a claim reached this session that spatial cutoffs and bounding
exponents "must be injected to prevent the linearized operator R(u,p) from
collapsing into a finite-time singularity." That is not how the 3D problem
works, and the reason why is the same fact that grades T418's vortex row.

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

## 2. What this does to T418

`math/theorems/pinn_rt_phase_field.py` (Theorem 418, "Discrete Phase-Field
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
precisely the axis that matters. That is not an argument against T418's other
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

---

## 4. The remaining T418 rows, graded against T305

Every row of T418's correspondence table and its three residuals, graded by
T305's cuts. Verified computationally, not read off.

### Outright false — two of the three residuals

**R1 PHASE ADVECTION.** Claim: `chi_{-3}(f^k(n)) = chi_{-3}(n)` for all n with
3 not dividing n. **FALSE.** At k=1 it fails for 16 of the 24 eligible n:

    n = 1, 2, 4, 5, 11, 13, 14, 16, 22, 23, 25, 26, 31, 32, 34, 35
    n=1: f(1)=26, chi(26) = -1, chi(1) = +1

The written proof reads `chi(26n mod 37) = chi(26n)`. That step is false:
**37 = 1 (mod 3)**, so subtracting 37 shifts the class mod 3. The proof's other
step, gcd(26,3) = 1, is true and does not bear on it.

What IS true and trivial: f^3 = identity because ord_37(26) = 3, so
chi(f^3(n)) = chi(n) for every n. The period-3 statement holds; the per-step
statement does not.

**R3 MOMENTUM.** Claim: `SA = {4,9,25,30}` is fixed under the 137-map. **FALSE**,
and the file's own text breaks mid-sentence: *"9 -> 234 mod 37 = 12; wait -- SA
elements are fixed points of DR, not the 137-map."* The orbits are

    4 -> 30 -> 3      9 -> 12 -> 16      25 -> 21 -> 28      30 -> 3 -> 4

The fallback offered in that same sentence, DR(f(n)) = DR(n) for n in SA, also
fails — at 4, 9 and 25.

### True but scope-overstated

**INTERFACE THEOREM.** Claim: every twin prime (p, p+2), p>3, has
chi = (-1, 0, +1) across p, p+1, p+2. **TRUE** — verified on all 102 twin primes
below 4000. But it also holds for **all 666 integers n = 5 (mod 6)** in the same
range. Twin primality is never used. The content is "n = 5 mod 6", which every
twin prime p>3 satisfies for an unrelated reason. True, not a twin-prime fact.

### Genuinely strong — the best row in the file

**SPECTRAL GAP.** Claim: in Cay(Z_37, H u -H) with H = {1,10,26}, the gap is at
k* = 7, indexed by C3 u (-C3) = {3,4,7,30,33,34}. **CONFIRMED.**

    eigenvalues are constant on mu_3-cosets of j  (lambda_j = lambda_26j: True)
    max non-trivial eigenvalue 4.047813, attained at j = {3,4,7,30,33,34}
    C3 = {3,4,30},  -C3 = {7,33,34},  union = exactly that set
    spectral gap = 6 - 4.047813 = 1.952187
    only 6 distinct eigenvalues among 36 (coset structure)

"Minimum non-trivial eigenvalue" is correct under the Laplacian convention
(6 - lambda), which is the standard spectral-gap reading. The index set matches
C3 u (-C3) exactly. This is a real computed fact with a nontrivial match.

Native rigor: theorem. Correspondence rigor: still L1 — calling it "the
dominant instability mode" imports a fluid role the computation does not supply.

### Level-1 rows

| row | grade |
|---|---|
| phase field alpha in [0,1] -> chi in {-1,0,+1} | CUT1 structural, CUT2 L1. Both are 3-valued; that is the shared role. alpha is continuous, chi is a character. |
| heavy / light phase -> 5-chamber / 1-chamber | L1, and definitional: it restates chi's own values. |
| continuity div u = 0 -> orbit closure (R2) | native: theorem (gcd(26,37)=1 gives a bijection, all 12 orbits size 3, verified). correspondence: L1 — "volume-preserving" is a shared role. |
| 6^2 = -1 -> "imaginary unit = pipe width" | 36 = -1 mod 37 is true. "= pipe width (interface thickness)" identifies nothing defined. No content. |
| mushroom rollup -> 3-cycles | L1, and blind to 2D/3D — see section 2. |

---

## 5. The structural finding: a claim-assertion gap

T418 runs clean. It passes because **its assertions test only true sub-steps,
never the claims that are false.** The complete assert list:

    assert gcd(26, 3) == 1            <- the only R1-related assert, and it is
                                         the IRRELEVANT step of a broken proof
    assert image == list(range(P))    <- supports R2
    assert orbit_sizes == {3}         <- supports R2
    assert len(v_left) == len(v_ctr) == len(v_right) == 0
    assert pow(6, 2, P) == P - 1      <- true; "pipe width" not asserted

R1 and R3 live in the docstring and are never tested. So the file is green
while two of its three residuals are false, and the single assertion touching
R1 checks the one step of its proof that does not matter.

This is a failure mode distinct from the two in `notes/theorem_corpus_audit.md`.
That audit measured whether assertions can fail (mutation) and whether they
restate each other (redundancy). Neither detects **assertions that pass but do
not cover the file's claims**. Call it the claim-assertion gap: the asserts test
A, the docstring claims B, and nothing checks B.

It is not statically detectable in general — deciding whether an assert covers a
prose claim needs the claim formalised. What IS mechanisable is a weaker proxy:
flag any file whose docstring states a universally quantified claim ("for all n
with ...") that no assertion quantifies over. T418 would be caught by that.
Recorded as a proposal, not built.
