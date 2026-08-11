"""
Theorem 170: QHO Operator Separation — Six Mathematical Layers

THE COMPLETE CLASSIFICATION
=============================

Every visual or computational feature of the C6-symmetric quantum harmonic
oscillator belongs to exactly one of six mathematical layers.  These must not
be conflated:

  Layer 1:  Numerical grid          (x_i, y_j)
  Layer 2:  Potential boundary      V(r,θ) = V_c
  Layer 3:  Probability density     |ψ(x,y)|² = ρ_c
  Layer 4:  Phase contour           arg ψ(x,y) = φ_c
  Layer 5:  Wavefunction node       ψ(x,y) = 0
  Layer 6:  Dynamical trajectory    Γ(t) = (r(t), θ(t))

THE C6 POTENTIAL
=================

  V(r,θ) = ½mω²r² + ε r⁶ cos(6θ)

  [H, R₆] = 0  →  joint eigenstates |n,μ⟩

The Hamiltonian itself generates the sixfold symmetry.  Visual hexagonal
structure comes from this equation, not from an overlay.

SIX LAYER OPERATORS
=====================

  Layer 1: Grid sampling operator    Π: f ↦ {f(x_i, y_j)}
  Layer 2: Level set operator        L_V: f ↦ {r: V(r)=V_c}
  Layer 3: Density contour           L_ρ: ψ ↦ {r: |ψ(r)|²=ρ_c}
  Layer 4: Phase contour             L_φ: ψ ↦ {r: arg ψ(r)=φ_c}
  Layer 5: Node set                  N: ψ ↦ {r: ψ(r)=0}
  Layer 6: Phase-space trajectory    Γ: t ↦ (r(t),θ(t))

These operators act on different objects and produce different sets:
  Layer 1  acts on any function; produces a sampled array.
  Layer 2  acts on V; produces a potential boundary.
  Layers 3,4,5 act on ψ; produce subsets of the spatial domain.
  Layer 6  acts on the dynamics; produces a time-parametric curve.

QUANTITATIVE TESTS (from the numerical experiment)
=====================================================

  ε_comm  = ||[H_FD, R₆_FD]|| / (||H_FD|| ||R₆_FD||)    →  0

  For each joint eigenstate |n,μ⟩:
    ε_H  = ||H_FD v - E v|| / ||v||                       →  0
    ε_R  = ||R₆ v - λ v|| / ||v||                         →  0

  For predicted GF(37) node locations r_{n,μ}:
    δ_node = d_node / Δx                                   →  0

  For predicted spiral trajectory:
    d_spiral = d_H(C_numerical, C_predicted)               →  0

A visual coincidence between a GF(37) node location and a bright density
contour is not evidence. Evidence is δ_node → 0 under grid refinement.

TRAJECTORY vs EIGENSTATE
==========================

A stationary eigenstate has no radial dynamics.
For a coherent state: α(t) = α₀ e^{−iωt} → phase-space circle, not spiral.

A spiral trajectory r = r(t), θ = ωt requires additional physics:
  - Damping:  α(t) = α₀ e^{−(γ+iω)t}  →  r(t) = r₀ e^{−γt}
  - Driving or nonlinear Hamiltonian

The spiral is a dynamical object (Layer 6), not an eigenfunction density
feature (Layers 3–5).

THE HIERARCHY
==============

  GF(37) ──Φ──↔── (C₆, H_FD) ──→── |ψ_{nμ}(r)|² ──→── Γ_V, Γ(t)

  Layer 0: GF(37) algebraic structure        [Theorems 163, 164]
  Layer 1: C₆ Hamiltonian eigenspaces        [ε_comm → 0: numerical]
  Layer 2: Probability density ρ_{nμ}        [eigenstate computation]
  Layer 3: Potential boundary and trajectory  [V_c, dynamical Γ(t)]

  δ_node → 0 under grid refinement would connect Layer 0 to Layer 2.
  This is the open test.

GF(37) LAYER COUNTS
=====================

  The six classification layers exactly match the six μ-sectors in H_mod:
    μ = 0,1,2,3,4,5 → six angular sectors → six T₆-orbit positions.

  This is a counting coincidence, not a proof.  The layers are different
  mathematical objects; the sectors are algebraic cosets.
"""

P = 37

ORBITS = {
    'IC':               frozenset({1, 10, 26}),
    'SOVEREIGN_SPIRAL': frozenset({3, 4, 30}),
    'D7':               frozenset({7, 33, 34}),
    'SA_ORB':           frozenset({9, 12, 16}),
    'ORBIT_11':         frozenset({11, 27, 36}),
    'OUTLIER_ORB':      frozenset({21, 25, 28}),
    'DARK_A':           frozenset({2, 15, 20}),
    'NQR_5':            frozenset({5, 13, 19}),
    'TESLA_ORB':        frozenset({6, 8, 23}),
    'NQR_14':           frozenset({14, 29, 31}),
    'NQR_17':           frozenset({17, 22, 35}),
    'SEED_ORB':         frozenset({18, 24, 32}),
}


def orbit_of(v):
    v = v % P
    if v == 0:
        return 'SEAM'
    return next((name for name, s in ORBITS.items() if v in s), '?')


def run_assertions():
    # The six layers are a classification, not GF(37) facts.
    # What IS provable: the algebraic structure from Theorems 163/164.

    # T6 = ×27, ord=6; 6 sectors = 6 layers (counting match)
    assert pow(27, 6, P) == 1
    assert pow(27, 1, P) != 1

    # The C6 potential eigenvalue structure: e^{2πiμ/6} for μ=0..5
    import cmath
    for mu in range(6):
        lam = cmath.exp(2j * cmath.pi * mu / 6)
        assert abs(lam**6 - 1) < 1e-12  # 6th root of unity

    # V(r,θ) = ½mω²r² + ε r⁶ cos(6θ) has period π/3 = 60° in θ
    import math
    for theta in [0, math.pi/3, 2*math.pi/3, math.pi, 4*math.pi/3, 5*math.pi/3]:
        v1 = math.cos(6 * theta)
        v2 = math.cos(6 * (theta + math.pi/3))
        assert abs(v1 - v2) < 1e-12, f"V not periodic at θ={theta}"

    # 37 mod 37 = 0: field prime is SEAM — the ground
    assert P % P == 0
    assert orbit_of(P) == 'SEAM'

    print("All assertions passed.")


def summarise():
    print("=" * 62)
    print("Theorem 170: QHO Operator Separation — Six Mathematical Layers")
    print("=" * 62)
    print()
    layers = [
        ("1. Numerical grid",       "(x_i, y_j)",             "sampled array"),
        ("2. Potential boundary",   "V(r,θ) = V_c",           "equipotential"),
        ("3. Density contour",      "|ψ|² = ρ_c",             "probability"),
        ("4. Phase contour",        "arg ψ = φ_c",            "phase"),
        ("5. Wavefunction node",    "ψ = 0",                  "quantum node"),
        ("6. Dynamical trajectory", "Γ(t)=(r(t),θ(t))",       "dynamics"),
    ]
    for name, eq, kind in layers:
        print(f"  {name:<25} {eq:<22} [{kind}]")
    print()
    print("  C6 potential: V(r,θ) = ½mω²r² + ε r⁶ cos(6θ)")
    print("  [H, R₆] = 0  →  joint states |n,μ⟩")
    print()
    print("  Quantitative tests:")
    print("    ε_comm = ||[H_FD,R₆]|| / (||H|| ||R||)  →  0")
    print("    δ_node = d_node / Δx  →  0 under refinement")
    print()
    print("  Spiral requires damping/driving — NOT an eigenstate feature.")
    print()
    print("  Open: δ_node → 0 would connect GF(37) Layer 0 to density Layer 2.")


if __name__ == "__main__":
    run_assertions()
    summarise()
