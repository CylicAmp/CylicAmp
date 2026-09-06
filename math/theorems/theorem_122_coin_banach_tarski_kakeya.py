"""
Theorem 122: Coin Paradox, Banach-Tarski, and Kakeya — One Algebraic Engine

The coin paradox, Banach-Tarski decomposition, and Besicovitch Kakeya set are
three manifestations of the same algebraic engine: a free group (or free semigroup)
of rigid or affine motions acting on a space.

CHAIN
=====

Theorem 1 (Coin Paradox):
  A coin of radius r rolling without slipping once around a fixed coin of equal
  radius rotates exactly twice (4π total). The rolling loop is a representative
  of the nontrivial element of π₁(SO(3)) ≅ ℤ₂. A 4π rotation is contractible
  in SO(3) (lifts to a loop in the universal cover SU(2)).

Theorem 2 (Hausdorff — free subgroup of SO(3)):
  Generators ρ (rotation by arccos(1/3) about z-axis) and
  σ (rotation by arccos(1/3) about x-axis) generate F₂ ≤ SO(3).
  cos θ = 1/3,  sin θ = 2√2/3,  sin²θ = 8/9.

Theorem 3 (Banach-Tarski):
  The free group's paradoxical decomposition (F₂ = W(a) ∪ aW(a⁻¹)) transfers
  via a free action on S² \ D to duplicate the sphere using only rotations.
  Pieces are non-measurable because F₂ is non-amenable.

Theorem 4 (Kakeya — Besicovitch):
  Two affine similarity maps f₁, f₂ (scaling 1/2, rotations ±α) generate a free
  semigroup. The iterated images cover all directions while area → 0.

Theorem 5 (Unifying):
  Double cover (coin) → free subgroup in SO(3) → Banach-Tarski (isometric)
  → Kakeya (contractive). Same branching tree; different measure behavior
  because generators are contractions (Kakeya) vs isometries (Banach-Tarski).

GF(37) CONNECTIONS
==================

cos θ = 1/3  →  3⁻¹ ≡ 25 (mod 37),  25 ∈ SA (sovereign anchors)
denominator 3  →  3 ∈ ST (sovereign targets)
sin²θ = 8/9  →  numerator 8 ∈ CB = {8, 13, 24} (cascade base)
π₁(SO(3)) ≅ ℤ₂  →  index-2 structure mirrors [(ℤ/37ℤ)*:QR₃₇] = 2
4π rotation period  →  ord₃₇(6) = 4 (TESLA_FLOW order)
F₂ on 2 generators  →  2 is primitive root mod 37, ord₃₇(2) = 36 = φ(37)
"""

import math
import numpy as np

P = 37

# Hausdorff generator angle
THETA = math.acos(1/3)
C = 1/3               # cos θ
S = 2*math.sqrt(2)/3  # sin θ

RHO = np.array([[C, -S, 0],
                [S,  C, 0],
                [0,  0, 1]])

SIGMA = np.array([[1, 0,  0],
                  [0, C, -S],
                  [0, S,  C]])

# GF(37) classes
SA = frozenset({4, 9, 25, 30})
ST = frozenset({3, 12, 21, 30})
CB = frozenset({8, 13, 24})
QR37 = frozenset(n for n in range(1, P) if pow(n, (P-1)//2, P) == 1)


def run_assertions():
    # Trigonometry
    assert abs(math.cos(THETA) - 1/3) < 1e-12
    assert abs(S - 2*math.sqrt(2)/3) < 1e-12
    assert abs(S**2 - 8/9) < 1e-12

    # Matrices are valid rotation matrices
    I = np.eye(3)
    assert abs(np.linalg.det(RHO) - 1) < 1e-10
    assert abs(np.linalg.det(SIGMA) - 1) < 1e-10
    assert np.allclose(RHO @ RHO.T, I)
    assert np.allclose(SIGMA @ SIGMA.T, I)

    # No generator is the identity
    assert not np.allclose(RHO, I)
    assert not np.allclose(SIGMA, I)

    # GF(37) connections
    inv3 = pow(3, -1, P)       # 3⁻¹ mod 37
    assert inv3 == 25
    assert 25 in SA             # cos θ denominator inverse → sovereign anchor
    assert 3 in ST              # cos θ denominator → sovereign target
    assert 8 in CB              # sin²θ numerator → cascade base

    # Index-2 structure: π₁(SO(3)) ≅ ℤ₂ mirrors QR subgroup at index 2
    assert len(QR37) == 18
    assert (P - 1) // len(QR37) == 2

    # 4π rotation period ↔ ord₃₇(6) = 4
    assert pow(6, 4, P) == 1
    assert all(pow(6, k, P) != 1 for k in [1, 2])

    # F₂ on 2 generators ↔ ord₃₇(2) = 36
    assert pow(2, 36, P) == 1
    assert all(pow(2, k, P) != 1 for k in [1, 2, 3, 4, 6, 9, 12, 18])

    # Free group check: no 1-letter word is identity; all non-trivial 2-letter
    # reduced words (length-2 words that don't cancel) are non-identity
    gens = [RHO, RHO.T, SIGMA, SIGMA.T]
    names = ['ρ', 'ρ⁻¹', 'σ', 'σ⁻¹']
    pairs_that_cancel = {(0,1),(1,0),(2,3),(3,2)}  # (gen, its inverse)
    for i, g in enumerate(gens):
        for j, h in enumerate(gens):
            if (i,j) not in pairs_that_cancel:
                assert not np.allclose(g @ h, I), f"Reduced word {names[i]}{names[j]} = I"

    print("All assertions passed.")


def summarise():
    print("=" * 62)
    print("Theorem 122: Coin–Banach-Tarski–Kakeya Chain")
    print("=" * 62)
    print(f"  Hausdorff angle θ = arccos(1/3) ≈ {math.degrees(THETA):.4f}°")
    print(f"  cos θ = 1/3 → 3⁻¹ ≡ 25 ∈ SA (mod 37)")
    print(f"  sin²θ = 8/9  → 8 ∈ CB (cascade base)")
    print(f"  3 ∈ ST (sovereign targets)")
    print(f"  π₁(SO(3)) ≅ ℤ₂  ↔  [(ℤ/37ℤ)*:QR] = 2")
    print(f"  4π rotation    ↔  ord₃₇(6) = 4 (TESLA_FLOW)")
    print(f"  F₂ generators  ↔  ord₃₇(2) = 36 = φ(37)")
    print()
    print("  Chain: double cover → free subgroup → Banach-Tarski → Kakeya")
    print("  Isometric vs contractive generators = measure preserved vs zero")


if __name__ == "__main__":
    run_assertions()
    summarise()
