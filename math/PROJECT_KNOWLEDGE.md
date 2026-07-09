# Project Knowledge — Mathematical Framework Map

## The Central Thread

Every system in this repo is studying the same question in a different language:

> **What happens when order matters — and what does that tell you about the structure underneath?**

---

## The Unified Map

```
Digital Root Algebra (Z/9Z)
│
│  DR(n) = (n-1)%9+1 for n>0
│  Multiplicative homomorphism mod 9
│  Group under addition, isomorphic to Z/9Z
│  Files: math/primes/dr_algebra.py
│         math/theorems/dr_algebra.py
│         math/primes/core.py
│
├──► D₄ Group Algebra
│    │
│    │  Non-abelian: r·s ≠ s·r
│    │  Wedderburn decomposition: ℂ[D₄] ≅ ℂ⊕ℂ⊕M₂(ℂ)
│    │  E-representation: r=[[0,-1],[1,0]], s=[[1,0],[0,-1]]
│    │  Files: math/theorems/dr_pattern_suite.py (Sections L–R)
│    │
│    ├──► Sovereign Matrix M_E
│    │    │
│    │    │  M_E = Σ(U⊗U) for U in {r,r⁻¹,s,r²s}
│    │    │  Eigenvalues: {-4, 0, 0, 4}  Rank=2
│    │    │  ker(M_E) dim=2
│    │    │  Basis: k1=[0,1,-1,0]=vec(iσ_y)
│    │    │         k2=[1,0,0,-1]=vec(σ_z)
│    │    │  Files: math/theorems/dr_pattern_suite.py (Sections O,P)
│    │    │         math/theorems/sovereign_matrix_charpoly.py
│    │    │
│    │    ├──► Commutant of M_E
│    │    │    │
│    │    │    │  dim=6 in M₄(ℂ) = 1+4+1
│    │    │    │  On kernel: full M₂(ℂ), dim=4
│    │    │    │  Generators: P_ij = k_i⊗k_j (outer products)
│    │    │    │  File: dr_pattern_suite.py (Section P)
│    │    │    │
│    │    │    └──► Weyl Algebra connection
│    │    │         [x,p] = xp - px = iℏ  (quantum)
│    │    │         [M_E, Q] = 0  but Q≠0  (accidental symmetry)
│    │    │         Same structure: non-zero commutator = information
│    │    │
│    │    └──► Accidental Zero Modes (Section R)
│    │         Q = P₁₁ - P₂₂ commutes with ALL D₄ elements
│    │         M_E + ε·Q has eigenvalues {-4,-ε,+ε,+4}
│    │         Zero modes are NOT D₄-protected → accidental
│    │
│    └──► Motif Gradient Word (Section N)
│         Gradients: [1,1,1,-1,-1,-1,-1,1,-1,-1,-1,3]
│         Bulk word = r² (NOT e — documented error in prior literature)
│         r² is the center of D₄
│
├──► Differential Geometry / Parallel Transport
│    │
│    │  Going around a loop ≠ returning to start
│    │  Holonomy = the commutator of infinitesimal transports
│    │  Same non-commutativity as D₄, same as Weyl algebra
│    │  Files: math/differential-geometry/tensors_riemann_parallel_transport.py
│    │         cylicamp/diff_geometry.py
│    │
│    └──► Riemann Curvature Tensor
│         R(X,Y) = [∇_X, ∇_Y] - ∇_[X,Y]
│         A commutator. Order of covariant derivatives matters.
│
└──► H_E Perturbation Matrix (Sections Q, R)
     │
     │  Separate 4×4 matrix (NOT M_E)
     │  Exact char poly: λ⁴-[(4+t)²+(4-t)²+δ²]λ²+(4+t)²(4-t)²=0
     │  Splitting is O(δ²) not O(δ)
     │  Zero modes at t=4 are permanent for all δ
     │
     └──► Key corrections to prior literature:
          - ker(M_E) dim=2 not 4
          - Bulk word = r² not e
          - T_z=σ_z⊗I does NOT preserve kernel
          - H_E spectral table in prior doc was fabricated
          - H_E zero modes are accidental not D₄-protected

---

## Secondary Systems

| System | File | Connection to main thread |
|---|---|---|
| Eisenstein primes | `math/theorems/eisenstein_primes.py` | Norm `a²-ab+b²` — quadratic form over Z[ω] |
| Kaprekar 6174 | `math/theorems/kaprekar_6174.py` | Fixed point under digit-sort operation |
| Repunit sequence | `math/primes/repunit_sequence.py` | Period-9 structure under DR |
| Fibonacci DR | `cylicamp/fib_dr.py` | Pisano period — DR(Fib) is periodic |
| 120-cell entropy | `cylicamp/entropy_120cell.py` | 120 = order of icosahedral symmetry group |
| Riemann zeta zeros | `math/primes/riemann_zeta_zeros.py` | Spectral interpretation of zeta zeros |

---

## BaseRate Tool (in development)

```
baserate/
├── modules/
│   └── intent_extractor.py   ← COMPLETE, 6/6 tests passing
│       Measures coherence gap between stated and core intent
│       Outputs manipulation_probability (0.0-1.0)
│
└── meeps/                    ← DESIGNED, not yet built
    ├── demon.py              Spreads like water, finds everything, no judgment
    ├── angel.py              Assesses what was found, determines containment
    └── purgatory.py          Sealed gate — nothing passes without verification
                              Human required for highest anomaly tier
```

Connection to math thread: IntentExtractor measures coherence gap.
A coherence gap IS a commutator — the distance between what an operator
claims to do and what it actually does. Same structure as [x,p] = iℏ.

---

## Key Constants (do not re-derive)

| Constant | Value | Source |
|---|---|---|
| DR formula | `(n-1)%9+1` for n>0 | Sign-invariant, multiplicative homomorphism |
| M_E eigenvalues | {-4, 0, 0, 4} | Rank 2, kernel dim=2 |
| ker basis k1 | [0,1,-1,0] | vec(iσ_y) |
| ker basis k2 | [1,0,0,-1] | vec(σ_z) |
| D₄ on kernel | r⊗r=diag(+1,-1), s⊗s=diag(-1,+1) | Abelian Z₂×Z₂ image |
| Commutant dim | 6 in M₄(ℂ), 4 on kernel | 1+4+1 decomposition |
| Motif bulk word | r² | Verified Section N — prior "e" claim is wrong |

---

## File Index (complete)

| File | What it does |
|---|---|
| `math/theorems/dr_pattern_suite.py` | Main suite Sections A–R |
| `math/theorems/run_all_math_tests.py` | Runs all math files, exits 1 on failure |
| `math/theorems/eisenstein_primes.py` | Eisenstein norm and primality |
| `math/theorems/kaprekar_6174.py` | Kaprekar fixed point |
| `math/theorems/sovereign_matrix_charpoly.py` | 9×9 sovereign matrix char poly |
| `math/primes/core.py` | DR lattice, build_full_lattice |
| `math/primes/dr_algebra.py` | Z/9Z group structure, Cayley table |
| `math/differential-geometry/tensors_riemann_parallel_transport.py` | Curvature, holonomy |
| `baserate/modules/intent_extractor.py` | Manipulation probability scorer |
| `cylicamp/diff_geometry.py` | Curve, Surface, Geodesic classes |
| `cylicamp/fib_dr.py` | Fibonacci digital root |
| `cylicamp/entropy_120cell.py` | 120-cell entropy |
