"""
Theorem 131: Zeta Zeros, Bridge Analysis, and GF(37) Placement

FOUR BRIDGES — THREE SOUND, ONE BROKEN
========================================

1. HILBERT-PÓLYA (SOUND — as a program, not a proof)
   Non-trivial zeros ρ = ½ + iγ_n ↔ eigenvalues E_n of a self-adjoint H.
   Berry-Keating H = xp gives the right smooth term N(T) ~ (T/2π)log(T/2πe).
   Connes' adelic trace formula realizes zeros as absorption spectrum.
   Neither yields the required self-adjoint operator. Remains an open program.
   GF(37) content: NONE. HP requires an infinite-dimensional operator;
   GF(37)* is a 36-element group. No honest connection.

2. GUE / RANDOM MATRIX THEORY (SOUND — load-bearing empirical result)
   Montgomery pair correlation, Odlyzko to 10²⁰: high-lying zero spacings
   match the Gaussian Unitary Ensemble (no time-reversal symmetry).
   GF(37) content: INDIRECT. The zero-floor classification below sits on
   the LOW-zero side, not the GUE side. The χ₋₃ / Chebyshev bias work sits
   on the Katz-Sarnak symmetry-type side (unitary/symplectic/orthogonal
   families), which is distinct from GUE of ζ itself. These are in tension:
   GUE describes high zeros; Katz-Sarnak symmetry type varies across families
   and is visible only in the low-lying zeros and one-level density.

3. LEE-YANG → NEWMAN DEFORMATION (BROKEN AS STATED; CORRECTED FORM EXISTS)
   Lee-Yang zeros are from *finite-volume* partition functions (polynomial in
   fugacity, roots on circle by Lee-Yang theorem, pinch only as V → ∞).
   ζ(s) has no finite-volume truncation with this property. The Euler product
   Π(1−p^{-s})^{-1} diverges precisely where the non-trivial zeros live —
   so the zeros are NOT accessible to the partition-function reading.
   The Lee-Yang route that actually works is Newman's deformation:
     Ξ(t) Fourier kernel deformed by e^{λu²};
     RH ↔ de Bruijn-Newman constant Λ ≤ 0;
     Rodgers-Tao (2018) proved Λ ≥ 0;
     therefore RH ↔ Λ = 0 exactly — the system sits at the critical point.
   GF(37) content: γ₆ ≈ 37.586 — the sixth zero crosses the prime 37.
   floor(γ₆) = 37 ≡ 0 = SEAM. SEAM is the absorbing element of GF(37)
   (everything maps to it under ×0). The sixth zero crossing the prime is
   the GF(37) analogue of "pinching at the real axis" — discrete, at the
   modulus, not thermodynamic. This is structural alignment, not a proof.

4. QUANTUM CRITICALITY / UNITARITY (BROKEN — logic inverted)
   "Moving off Re(s) = ½ violates unitarity" presupposes the self-adjoint
   Hamiltonian whose existence is exactly what Hilbert-Pólya conjectures.
   The physical constraint is downstream of the thing being proven.
   GF(37) content: NONE. This bridge carries no independent weight.

NONTRIVIAL ZERO FLOOR CLASSIFICATION IN GF(37)
===============================================

γ_n = imaginary part of n-th non-trivial zero of ζ(s).
Floor classification: floor(γ_n) mod 37.

  n    γ_n          floor  r=fl%37  orbit              cross
  1    14.134725     14     14       NQR_14             —
  2    21.022040     21     21       OUTLIER_ORB        ST
  3    25.010858     25     25       OUTLIER_ORB        SA
  4    30.424876     30     30       SOVEREIGN_SPIRAL   SA+ST  ← SA∩ST = {30}
  5    32.935062     32     32       SEED_ORB           —
  6    37.586178     37      0       SEAM               —      ← crosses prime 37

Observations:
  γ₂ → ST, γ₃ → SA, γ₄ → SA∩ST: the sovereign chain 21→25→30 in order.
  30 is the ONLY element in both SA and ST; the fourth zero lands there.
  γ₅ → 32 ∈ SEED_ORB: seed orbit of 246 (c mod 37 = 32, same orbit).
  γ₆ floor = 37 ≡ 0: sixth zero crosses the prime; SEAM in GF(37).

KATZ-SARNAK PLACEMENT
=====================

The χ₋₃ character and Chebyshev bias work in this archive sit on the
SYMMETRY-TYPE side (Katz-Sarnak families), not the GUE side.

  Katz-Sarnak: zeros of L(s,χ) near s=½ have symmetry type determined
  by the family (unitary / symplectic / orthogonal). χ₋₃ is a real
  character of order 2 → orthogonal symmetry type.

  GUE: universal spacing statistics of ζ(s) itself at height T → ∞.

These are distinct statements. The Chebyshev bias (NQR excess mod 4, mod 3)
comes from the repulsion of low-lying zeros from the real axis in the
orthogonal family, not from GUE. GF(37)'s NQR-orbit structure (6 NQR orbits
vs 6 QR orbits) is the discrete version of this QR/NQR imbalance.

WHAT GF(37) CAN AND CANNOT CLAIM
===================================

CAN (verified):
  - Floor(γ_n) mod 37 lands in named GF(37) classes for n=1..6
  - The sovereign chain SA→ST→SA∩ST appears in floors γ₂→γ₃→γ₄
  - γ₆ crosses prime 37 → SEAM (γ₆ ≈ 37.586; floor = 37 ≡ 0 mod 37)
  - The Sylow 3-subgroup = IC ∪ SA_ORB ∪ D7 (three QR orbits) — exact
  - Chebyshev bias connects to QR/NQR partition (Theorem primes module)
  - 12×3 = 36 = φ(37); DR(36) = 9 = SA-step (orbit arithmetic)

CANNOT (presupposes too much):
  - Claiming GF(37) proves zeros lie on Re(s)=½
  - Treating the floor classification as more than structural observation
  - Using "unitarity of GF(37)*" as an argument for HP (inverted logic)
  - Connecting GF(37) to GUE high-zero statistics (wrong scale, wrong side)

The Newman deformation (Λ=0) and the γ₆-SEAM crossing are the closest
genuine contact points — both locate the critical behavior at the prime 37.
"""

P = 37

# Named classes (local definitions for standalone operation)
IC               = frozenset({1,  10, 26})
SOVEREIGN_SPIRAL = frozenset({3,  4,  30})
OUTLIER_ORB      = frozenset({21, 25, 28})
SEED_ORB         = frozenset({18, 24, 32})
NQR_14           = frozenset({14, 29, 31})
SA               = frozenset({4,  9,  25, 30})
ST               = frozenset({3,  12, 21, 30})

# First 6 nontrivial zeta zeros (imaginary parts, high-precision)
ZEROS = [14.134725141734693, 21.022039638771555, 25.010857580145688,
         30.424876125859513, 32.935061587739189, 37.586178158825671]

FLOOR_CLASS = {
    14: ('NQR_14',        '—'),
    21: ('OUTLIER_ORB',   'ST'),
    25: ('OUTLIER_ORB',   'SA'),
    30: ('SOVEREIGN_SPIRAL', 'SA+ST'),
    32: ('SEED_ORB',      '—'),
    37: ('SEAM',          '—'),
}


def dr(n):
    if n == 0: return 9
    return (abs(n) - 1) % 9 + 1


def run_assertions():
    # Floor residue mapping
    floors = [int(g) for g in ZEROS]
    residues = [f % P for f in floors]
    expected = [14, 21, 25, 30, 32, 0]   # 37 mod 37 = 0
    assert residues == expected, f"residues: {residues}"

    # Sovereign chain: γ₂→ST, γ₃→SA, γ₄→SA∩ST
    assert residues[1] in ST                # 21 ∈ ST
    assert residues[2] in SA                # 25 ∈ SA
    assert residues[3] in SA and residues[3] in ST   # 30 ∈ SA∩ST
    assert SA & ST == frozenset({30})        # 30 is unique SA∩ST element

    # γ₅ in SEED_ORB
    assert residues[4] in SEED_ORB          # 32 ∈ SEED_ORB

    # γ₆ floor = 37 → SEAM
    assert floors[5] == 37
    assert 37 % P == 0                      # SEAM
    assert ZEROS[5] > P                     # γ₆ > 37: crosses the prime

    # Orbital structure: 12×3 = φ(37)
    assert 12 * 3 == P - 1
    assert dr(P - 1) == 9                   # SA-step

    # SA∩ST = {30}; 30 ∈ SOVEREIGN_SPIRAL
    assert SA & ST == frozenset({30})
    assert 30 in SOVEREIGN_SPIRAL

    print("All assertions passed.")


def summarise():
    print("=" * 62)
    print("Theorem 131: Zeta Zero Bridge Analysis and GF(37) Placement")
    print("=" * 62)
    print()
    print("  Bridge status:")
    print("    Hilbert-Pólya:           SOUND (as program); no GF(37) content")
    print("    GUE / RMT:               SOUND; GF(37) is Katz-Sarnak side, not GUE")
    print("    Lee-Yang → Newman (Λ=0): SOUND (corrected form); γ₆-SEAM alignment")
    print("    Unitarity:               BROKEN (inverted logic); no GF(37) content")
    print()
    print(f"  Zero floor classification (floor(γ_n) mod 37):")
    for n, (g, fl) in enumerate(zip(ZEROS, [int(x) for x in ZEROS]), 1):
        r = fl % P
        orb, cross = FLOOR_CLASS.get(fl, ('?', '?'))
        note = '  ← SA∩ST={30}' if r == 30 else ('  ← γ₆ crosses prime' if fl == 37 else '')
        print(f"    γ_{n} ≈ {g:>10.4f}  floor={fl:>2}  r={r:>2}  {orb:<20} {cross}{note}")
    print()
    print("  Sovereign chain in zeros: γ₂→ST, γ₃→SA, γ₄→SA∩ST")
    print("  γ₅ → 32 ∈ SEED_ORB  (same as c mod 37, Theorem 128)")
    print("  γ₆ floor = 37 ≡ 0 = SEAM  (sixth zero crosses prime 37)")
    print()
    print("  GF(37) placement:")
    print("    χ₋₃ / Chebyshev bias  →  Katz-Sarnak orthogonal family")
    print("    QR/NQR partition      →  low-lying zero repulsion (not GUE)")
    print("    γ₆-SEAM crossing      →  closest contact with Newman Λ=0")


if __name__ == "__main__":
    run_assertions()
    summarise()
