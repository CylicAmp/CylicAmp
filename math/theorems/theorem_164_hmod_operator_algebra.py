"""
Theorem 164: H_mod Operator Algebra — The Full Modular Hilbert Space

THE MODULAR HILBERT SPACE
==========================

  H_mod = C[GF(37)*] ≅ C^36

Orthonormal basis: {|x⟩ : x ∈ (Z/37Z)*},  dim = 36.

TWO OPERATORS
==============

  T6 |x⟩ = |27x mod 37⟩         ord(27) = 6,  27 ∈ ORBIT_11
  T3 |x⟩ = |26x mod 37⟩         ord(26) = 3,  26 ∈ IC = 137-map

ALGEBRAIC IDENTITY: T3 = T6^2
================================

  27^2 mod 37 = 729 mod 37 = 26.

  T6^2 = T3  (the 137-map is the square of the C6 generator).

Consequences:
  T6^6 = T3^3 = I
  T3 = T6^2,  T3^2 = T6^4,  T3^3 = T6^6 = I

The generator 27 (T6, ∈ ORBIT_11) and the 137-map multiplier 26 (T3, ∈ IC)
are in DIFFERENT GF(37) orbits but are powers of the same group element.

THE SIX T6-ORBITS
==================

  r=0:  x_0=1   orbit: [1, 27, 26, 36, 10, 11]   IC ↔ ORBIT_11
  r=1:  x_1=2   orbit: [2, 17, 15, 35, 20, 22]   DARK_A ↔ NQR_17
  r=2:  x_2=4   orbit: [4, 34, 30, 33, 3, 7]     SOVEREIGN_SPIRAL ↔ D7
  r=3:  x_3=8   orbit: [8, 31, 23, 29, 6, 14]    TESLA_ORB ↔ NQR_14
  r=4:  x_4=16  orbit: [16, 25, 9, 21, 12, 28]   SA_ORB ↔ OUTLIER_ORB
  r=5:  x_5=32  orbit: [32, 13, 18, 5, 24, 19]   SEED_ORB ↔ NQR_5

FOURIER MODE DECOMPOSITION
===========================

For each orbit r, the Fourier modes are:

  |O_r; μ⟩ = (1/√6) Σ_{k=0}^{5} e^{-2πiμk/6} |27^k x_r⟩

These satisfy:

  T6 |O_r; μ⟩ = e^{2πiμ/6} |O_r; μ⟩
  T3 |O_r; μ⟩ = e^{4πiμ/6} |O_r; μ⟩ = e^{2πiμ/3} |O_r; μ⟩

T3 has only 3 distinct eigenvalues (cube roots of unity):
  μ=0,3: eigenvalue 1
  μ=1,4: eigenvalue ω   = e^{2πi/3}
  μ=2,5: eigenvalue ω²  = e^{4πi/3}

This matches: T3 = T6^2, so T3's eigenvalues are squares of T6's.

FULL DECOMPOSITION
===================

  H_mod = ⊕_{r=0}^{5} ⊕_{μ=0}^{5} H_{r,μ}

  Each H_{r,μ} is 1-dimensional, spanned by |O_r; μ⟩.
  dim(H_mod) = 6 × 6 = 36.  ✓

THE THREE INTERTWINER CONDITIONS
==================================

The proposed intertwiner Φ: H_mod → H_geom maps:

  Φ: |O_r; μ⟩_mod ↦ |n_r, μ⟩_geom

For Φ to be an intertwining representation of the full operator algebra,
three conditions must hold:

  (1)  Φ T6 = R6 Φ          [C6 symmetry correspondence]
  (2)  Φ T3 = R6^2 Φ        [137-map correspondence; follows from T3=T6^2]
  (3)  Φ H_mod = H_FD Φ     [Hamiltonian correspondence]

Conditions (1) and (2) are algebraically implied by each other given T3=T6^2.
Condition (3) is independent — it requires:

  H_mod |O_r; μ⟩ = E_{n_r} |O_r; μ⟩

for the same eigenvalues E_{n_r} as the physical Hamiltonian at radial level n_r.

THE CORRECTION: r IS NOT INTRINSICALLY RADIAL
===============================================

The orbit label r = 0,...,5 is a combinatorial label from the T6-orbit structure.
The identification r ↦ n_r (a physical radial quantum number) is an additional
proposed correspondence, NOT a consequence of the GF(37) structure.

GF(37)* has no natural Euclidean magnitude that maps to oscillator radius.
The rigorous chain is:

  GF(37) orbit label r → proposed → n_r (radial QN)

not:

  GF(37) magnitude = radial QN.

Condition (3) is precisely the statement that this identification is consistent
with the Hamiltonian spectrum.

THE FULL FALSIFIABLE HIERARCHY
================================

  GF(37) ──Φ──↔── (C6, H_FD) ──→── |ψ_{nμ}(r)|² ──→── Γ_V, Γ(t)

Layer 1: Algebraic  — T6, T3, Fourier modes, H_mod.  Proven here.
Layer 2: Geometric  — H_FD, R6, joint eigenspaces |n,μ⟩. Compute ε_comm → 0.
Layer 3: Density    — ρ_{nμ}(x,y) = |ψ_{nμ}|². Compare predicted vs observed nodes.
Layer 4: Dynamical  — Γ(t), spiral, Γ_V intersections.

Layers 1 and 2 are independent. Condition (3) connects them.
Visual coincidence between GF(37) nodes and density contours is not the proof.
The proof is δ_node = d_node/Δx → 0 under grid refinement.

SUMMARY OF WHAT IS PROVEN
===========================

  27^2 ≡ 26 (mod 37)  →  T3 = T6^2  (exact algebraic identity)
  ord(27) = 6,  ord(26) = 3  (exact)
  H_mod = ⊕_{r,μ} H_{r,μ},  dim = 36  (exact)
  |O_r; μ⟩ are simultaneous eigenstates of T6 and T3  (exact)
  ΦT6 = R6Φ  holds as algebraic identity  (proven in Theorem 163)
  ΦT3 = R6^2 Φ  follows immediately  (proven here)

  ΦH_mod = H_FD Φ  is the open condition that the numerical test would decide.
"""

import numpy as np

P = 37


def run_assertions():
    # T3 = T6^2: 27^2 = 26 mod 37
    assert (27**2) % P == 26

    # Orders
    assert pow(27, 6, P) == 1 and pow(27, 3, P) != 1
    assert pow(26, 3, P) == 1 and pow(26, 1, P) != 1

    # T6 orbits
    orbits = {}
    for r in range(6):
        x_r = pow(2, r, P)
        orbit = [pow(27, k, P) * x_r % P for k in range(6)]
        orbits[r] = orbit
        # T6 acts cyclically
        assert [(27*x) % P for x in orbit] == orbit[1:] + [orbit[0]]

    # All 36 covered
    all_els = sorted(x for orb in orbits.values() for x in orb)
    assert all_els == list(range(1, 37))

    # Fourier mode eigenvalues: T6 eigenvalue = e^{2πiμ/6}
    for mu in range(6):
        lam6 = np.exp(2j * np.pi * mu / 6)
        lam3 = lam6**2  # T3 = T6^2
        expected_lam3 = np.exp(2j * np.pi * mu / 3)
        assert abs(lam3 - expected_lam3) < 1e-12

    # T3 has only 3 distinct eigenvalues
    lam3_vals = {mu: np.exp(2j*np.pi*mu/3) for mu in range(6)}
    assert abs(lam3_vals[0] - lam3_vals[3]) < 1e-12  # μ=0,3 both give 1
    assert abs(lam3_vals[1] - lam3_vals[4]) < 1e-12  # μ=1,4 both give ω
    assert abs(lam3_vals[2] - lam3_vals[5]) < 1e-12  # μ=2,5 both give ω²

    # ΦT3 = R6^2 Φ: T3 advances μ by 2
    for r in range(6):
        x_r = pow(2, r, P)
        for mu in range(6):
            x = pow(27, mu, P) * x_r % P
            t3x = (26 * x) % P
            # Find position of t3x in orbit r
            orbit = orbits[r]
            if t3x in orbit:
                new_mu = orbit.index(t3x)
                assert new_mu == (mu + 2) % 6, f'T3 should advance μ by 2, got {new_mu-mu}'

    print("All assertions passed.")


def summarise():
    print("=" * 62)
    print("Theorem 164: H_mod Operator Algebra")
    print("=" * 62)
    print()
    print("  H_mod = C[GF(37)*] ≅ C^36")
    print()
    print("  T6: multiplication by 27  (ord=6, 27 ∈ ORBIT_11)")
    print("  T3: multiplication by 26  (ord=3, 26 ∈ IC = 137-map)")
    print(f"  27^2 mod 37 = {(27**2)%P}  =>  T3 = T6^2")
    print()
    print("  Six T6-orbits:")
    for r in range(6):
        x_r = pow(2, r, P)
        orbit = [pow(27, k, P) * x_r % P for k in range(6)]
        print(f"    r={r}: {orbit}")
    print()
    print("  Fourier modes |O_r;μ⟩:")
    print("    T6 |O_r;μ⟩ = e^{2πiμ/6} |O_r;μ⟩")
    print("    T3 |O_r;μ⟩ = e^{2πiμ/3} |O_r;μ⟩   (cube roots of unity × 2)")
    print()
    print("  H_mod = ⊕_{r=0}^5 ⊕_{μ=0}^5 H_{r,μ}   dim=36")
    print()
    print("  Intertwiner conditions:")
    print("    (1) Φ T6 = R6 Φ        [proven in Theorem 163]")
    print("    (2) Φ T3 = R6^2 Φ      [follows: T3=T6^2]")
    print("    (3) Φ H_mod = H_FD Φ   [open — numerical test decides]")
    print()
    print("  r is a combinatorial orbit label, NOT intrinsically radial.")
    print("  r → n_r is an additional proposed identification.")
    print()
    print("  Falsifiable hierarchy:")
    print("    GF(37) ─Φ─↔─ (C6,H_FD) ─→─ |ψ_{nμ}|² ─→─ Γ_V, Γ(t)")


if __name__ == "__main__":
    run_assertions()
    summarise()
