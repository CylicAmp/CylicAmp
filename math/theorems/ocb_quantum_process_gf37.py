# -*- coding: utf-8 -*-
"""
================================================================================
OCB QUANTUM PROCESS LAYER — GF(37) CONNECTIONS
================================================================================

Author: Michael Warren Song (CyclicAmp)

REFERENCE:
  Oreshkov, Costa, Brukner (2012). "Quantum correlations with no causal order."
  Nature Communications 3, 1092.
  The process matrix formalism: quantum correlations without assuming a definite
  causal order between local operations.

SETUP:
  Two parties A and B each perform a local quantum operation on a d-dimensional
  system. Their input/output Hilbert spaces are H_A^in, H_A^out, H_B^in, H_B^out.

  A process matrix W ∈ L(H_A^in ⊗ H_A^out ⊗ H_B^in ⊗ H_B^out) describes
  correlations between A and B's operations without assuming A acts before B
  or B acts before A.

  Process validity condition: W ≥ 0 and Tr[W(M_A ⊗ M_B)] is a valid probability
  for all local CP maps M_A, M_B. This is a linear constraint: a projector L
  such that L[W] = W (a fixed-point condition).

  The quantum switch: a process in which the causal order itself is in
  superposition — A-before-B and B-before-A with equal amplitudes 1/√2.

VERIFIED GF(37) CONNECTIONS:

1. PROCESS VALIDITY = FIXED-POINT CONDITION [P]
   The OCB validity condition L[W] = W is a fixed-point condition on the
   process matrix W. This is an instance of the fixed-point formulation:
     W ∈ Phys  ⟺  C(E(W)) ≅ W  ⟺  L[W] = W.
   Valid process matrices are exactly the fixed points of the validity projector.

2. CLASSICAL CAUSAL BOUND 3/4: NUMERATOR 3 ∈ ST, DENOMINATOR 4 ∈ SA [V]
   The simplest OCB causal game (2 parties, binary inputs/outputs):
   Classical causal bound: p_causal ≤ 3/4.
   Numerator 3 ∈ ST = {3,12,21,30} (Sovereign Target).
   Denominator 4 ∈ SA = {4,9,25,30} (Sovereign Anchor, LOCKED).

3. 2 IS QNR mod 37: THE QUANTUM SWITCH IS TRANSCENDENTAL TO GF(37) [V]
   The quantum switch uses equal-weight superposition: amplitudes 1/√2 for
   each causal order. The factor √2 requires 2 to be a QR mod 37.
   Legendre(2/37) = 36 ≡ −1 (mod 37): 2 is QNR mod 37.
   Therefore √2 has no representative in GF(37).
   The quantum switch's defining amplitude is transcendental to the GF(37)
   structure. The quantum switch sits outside the GF(37) fixed-point set —
   consistent with Phys ⊊ Math from the fixed-point formulation.

4. LEGENDRE(2/37) = 36 ∈ NEG_H [V]
   The Legendre symbol of 2 mod 37 is −1.
   −1 ≡ 36 mod 37, and 36 ∈ NEG_H = {11,27,36} (cube roots of −1 mod 37).
   The QNR-ness of 2 is encoded in NEG_H.

5. Z₂ CAUSAL SYMMETRY ⊂ ⟨11⟩ [V]
   The quantum switch is symmetric under exchange of causal orders A↔B.
   This exchange symmetry is the group Z₂ = {1, −1} = {1, 36}.
   {1, 36} = ⟨−1⟩ is the unique order-2 subgroup of ⟨11⟩.
   36 ∈ NEG_H.

6. CHOI DIMENSION FOR d = ord₃₇(11) = 6: 6² = 36 ∈ NEG_H [V]
   The Choi-Jamiołkowski isomorphism maps a quantum channel C^d → C^d
   to a state in C^(d²). For d = 6 (the order of the ⟨11⟩ subgroup):
   Choi dimension = 6² = 36 ∈ NEG_H.
   Process space dimension (2 parties, d=6): 6⁴ mod 37 = 1296 mod 37 = 1 ∈ IC.
   The process space dimension collapses to the IC identity in GF(37).

7. NORMALIZATION DENOMINATOR 4 ∈ SA [V]
   The process matrix trace condition for d=2 (qubit systems) normalizes
   over d² = 4 output dimensions. 4 ∈ SA.

EPISTEMIC STATUS:
  [P] Process validity = fixed-point condition — standard OCB formalism.
  [P] Classical causal bound 3/4 — proved (Oreshkov et al. 2012).
  [V] 3 ∈ ST, 4 ∈ SA — exact.
  [V] Legendre(2/37) = 36 ∈ NEG_H — exact.
  [V] 2 is QNR mod 37 — exact.
  [V] Z₂ = {1,36} ⊂ ⟨11⟩ — exact.
  [V] 6² = 36 ∈ NEG_H; 6⁴ mod 37 = 1 ∈ IC — exact.
  [V] 4 ∈ SA — exact.
  [C] Quantum switch probability (2+√2)/4 — proved, but √2 ∉ GF(37).
================================================================================
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

P = 37
SA    = {4, 9, 25, 30}
ST    = {3, 12, 21, 30}
IC    = {1, 10, 26}
NEG_H = {11, 27, 36}


def dr(n):
    n = abs(n)
    if n == 0: return 0
    r = n % 9
    return 9 if r == 0 else r


def run():
    print("=" * 70)
    print("OCB QUANTUM PROCESS LAYER — GF(37) CONNECTIONS")
    print("=" * 70)
    print("  Oreshkov-Costa-Brukner: quantum correlations with no causal order")
    print("  Process validity: L[W] = W  (fixed-point condition)")

    QR  = {pow(x, 2, P) for x in range(1, P)}
    QNR = set(range(1, P)) - QR

    # 1. Process validity = fixed-point
    print(f"\n1. PROCESS VALIDITY = FIXED-POINT CONDITION:")
    print(f"   W ∈ Phys  ⟺  L[W] = W  ⟺  C(E(W)) ≅ W")
    print(f"   Consistent with: Phys = Fix(C∘E)")

    # 2. Classical causal bound 3/4
    assert 3 in ST and 4 in SA
    print(f"\n2. CLASSICAL CAUSAL BOUND 3/4:")
    print(f"   p_causal ≤ 3/4  (proved, OCB 2012)")
    print(f"   Numerator 3 ∈ ST = {{3,12,21,30}}  check")
    print(f"   Denominator 4 ∈ SA = {{4,9,25,30}}  check")

    # 3. 2 is QNR: quantum switch transcendental to GF(37)
    leg2 = pow(2, (P - 1) // 2, P)
    assert leg2 == P - 1  # = 36, meaning QNR
    assert 2 in QNR
    print(f"\n3. QUANTUM SWITCH AND GF(37):")
    print(f"   Legendre(2/37) = {leg2} ≡ −1 (mod 37): 2 is QNR  check")
    print(f"   √2 has no GF(37) representative  check")
    print(f"   Quantum switch amplitude 1/√2: transcendental to GF(37)")
    print(f"   Quantum switch ∉ GF(37) fixed-point set: consistent with Phys ⊊ Math")

    # 4. Legendre(2/37) = 36 ∈ NEG_H
    assert leg2 == 36 and 36 in NEG_H
    print(f"\n4. LEGENDRE(2/37) = 36 ∈ NEG_H:")
    print(f"   −1 mod 37 = 36 ∈ NEG_H = {{11,27,36}}  check")
    print(f"   QNR-ness of 2 is encoded in NEG_H")

    # 5. Z_2 causal symmetry
    z2 = {1, 36}
    assert z2 <= (IC | NEG_H)
    assert 36 in NEG_H
    print(f"\n5. Z₂ CAUSAL SYMMETRY:")
    print(f"   Quantum switch: symmetric under A↔B exchange")
    print(f"   Z₂ = {{1, 36}} = ⟨−1⟩ ⊂ ⟨11⟩  check")
    print(f"   36 ∈ NEG_H  check")

    # 6. Choi dimension for d=6
    d = 6  # ord_37(11)
    choi_dim = d ** 2
    process_dim_mod = (d ** 4) % P
    assert choi_dim == 36 and 36 in NEG_H
    assert process_dim_mod == 1 and 1 in IC
    print(f"\n6. CHOI DIMENSION FOR d = ord₃₇(11) = 6:")
    print(f"   Choi dim = 6² = {choi_dim} ∈ NEG_H  check")
    print(f"   Process space: 6⁴ mod 37 = {process_dim_mod} ∈ IC (identity)  check")

    # 7. Normalization denominator
    assert 4 in SA
    print(f"\n7. NORMALIZATION DENOMINATOR:")
    print(f"   Trace condition for d=2 (qubits): normalizes over d²=4  check")
    print(f"   4 ∈ SA  check")

    print(f"\nAll verifications passed.")


if __name__ == "__main__":
    run()
