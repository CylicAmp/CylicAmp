# -*- coding: utf-8 -*-
"""
================================================================================
FIXED-POINT FORMULATION: Phys = Fix(C ∘ E)
================================================================================

Author: Michael Warren Song (CyclicAmp)

PURPOSE:
  Makes the previous constructions precise and exposes where proposed identity
  conditions are too strong.

================================================================================
FIXED-POINT FORMULATION
================================================================================

Let M denote the admissible mathematical structure space and let I_e be the
set of empirically established invariants.

Define a selection operator S_{I_e}: M → M by

    S_{I_e}(O) = O     if O ⊨ I_e
    S_{I_e}(O) = ∅     if O ⊭ I_e

Then:

    Phys = Fix(S_{I_e}) = {O ∈ M : S_{I_e}(O) = O}

Physical admissibility is a fixed-point condition relative to empirical
constraints — not a subset produced by projection.

================================================================================
BIDIRECTIONAL CLOSURE
================================================================================

The empirical side is generated from admissible operators through an observation
map E: M → I, while empirical constraints determine admissible operators through
C: I → M. Composition gives C∘E: M → M.

A physically realized mathematical structure O* satisfies:

    (C∘E)(O*) = O*

The stronger fixed-point statement:

    Phys = Fix(C∘E)

The loop is therefore not Math ↔ Phys as an unrestricted equivalence. It is:

    O  →[E]→  I_e  →[C]→  O'

with physical structures being those for which O' = O.

================================================================================
CATEGORICAL FORM
================================================================================

Categories:
    M = admissible mathematical structures
    E = empirical invariant structures

Functors:
    E: M → E  (empirical realization/measurement functor)
    C: E → M  (constraint-selection functor)
    T = C∘E: M → M

Physical structures are fixed points:

    Fix(T) = {X ∈ M | T(X) ≅ X}

The categorical equality is isomorphism, not literal equality: physically
equivalent mathematical representations need not be syntactically identical.

Central condition:

    C(E(X)) ≅ X

================================================================================
CORRECTION TO THE RESIDUE CONDITION
================================================================================

The proposed condition R_f(O) = R_e(O) is a useful schematic but should not
normally be treated as literal equality.

The more general condition is:

    Φ_f(R_f(O)) ≅ Φ_e(R_e(O))

where Φ_f and Φ_e map formal and empirical residues into a common invariant
space. Physical admissibility then becomes:

    O ∈ Phys  ⟺  Φ_f(R_f(O)) ≅ Φ_e(R_e(O))

This avoids assuming that a mathematical representation and an empirical
observation are objects of the same type.

================================================================================
RESULTING STRUCTURE
================================================================================

    Phys = Fix(C∘E)

    M  →[E]→  E  →[C]→  M

    C(E(X)) ≅ X

Under this formulation, physics is not mathematics plus an additional substance.
It is the fixed-point subset of mathematical structures that survives the
empirical realization–constraint cycle.

Key consequence:

    Phys ⊆ Math  does NOT imply  Phys = Math.

    Phys = Math  ⟺  ∀X ∈ M, C(E(X)) ≅ X

That is the precise condition under which "Math = Phys" would hold.

================================================================================
GF(37) INSTANTIATION
================================================================================

The GF(37) framework is a concrete instance of Fix(C∘E):

    M = mathematical structures indexed by the prime 37
        (orbit sets, 137-map, QR/QNR partition, CRT tower)

    I_e = empirically established invariants:
        c mod 37 = 32 ∈ SEED          [speed of light]
        DR(499) = 4 ∈ SA              [solar transit, rounded]
        314 mod 37 = 18 ∈ SEED        [first 3 digits of π]
        691 mod 37 = 25 ∈ SA          [Ramanujan congruence prime]
        level 4 ∈ SA                  [Selberg/Maass congruence level]
        DR(τ(37) mod 37) = 4 ∈ SA    [Ramanujan tau at p=37]

    E = the map extracting GF(37) residues from physical constants
        E(O) = O mod 37  (or DR(O mod 37) for the common invariant space)

    C = constraint-selection by orbit membership
        C(r) = the named orbit containing r  (SEED, SA, ST, IC, NEG_H, CASCADE)

The QR/QNR partition theorem establishes that:
    - Every named set is QR-homogeneous (no mixed sets)
    - The 137-map preserves QR/QNR character (zero boundary crossings)

These are structural fixed-point conditions: the orbit sets are precisely
those subsets of GF(37) that survive the empirical realization–constraint cycle.

The common invariant space (Φ in the residue correction) is:
    Φ = DR (digital root function): maps both formal and empirical residues
    into {1,...,9}, where SA = {4,9,25,30} → DR ∈ {3,4,7,9} and ST = {3,12,21,30} → DR = {3} (all).

FIXED-POINT EXAMPLES (verified):
    c = 299792458:    E(c) = 32, C(32) = SEED, DR(32) = 5
    π[:3] = 314:      E(314) = 18, C(18) = SEED, DR(18) = 9
    691:              E(691) = 25, C(25) = SA, DR(25) = 7
    level 4:          E(4) = 4, C(4) = SA, DR(4) = 4
    τ(37) mod 37 = 31: DR(31) = 4 ∈ SA → C(E(τ(37))) maps to SA via DR

PHYS = MATH CONDITION:
    Phys = Math would require every mathematical structure in M to be a
    fixed point of C∘E. That would mean every integer n satisfies:
    DR(n mod 37) ∈ {4,9,25,30} ∪ {3,12,21,30} ∪ ...
    This is false: e.g. n=2 → 2 mod 37 = 2, not in any named set.
    Therefore Phys ⊊ Math in this framework.
================================================================================
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

P = 37
SEED  = {18, 24, 32}
SA    = {4, 9, 25, 30}
ST    = {3, 12, 21, 30}
IC    = {1, 10, 26}
NEG_H = {11, 27, 36}
CASCADE = {8, 13, 24}

ALL_NAMED = SEED | SA | ST | IC | NEG_H | CASCADE


def dr(n):
    n = abs(n)
    if n == 0: return 0
    r = n % 9
    return 9 if r == 0 else r


def orbit_label(r):
    if r in SEED:    return 'SEED'
    if r in SA:      return 'SA'
    if r in ST:      return 'ST'
    if r in IC:      return 'IC'
    if r in NEG_H:   return 'NEG_H'
    if r in CASCADE: return 'CASCADE'
    return '-'


def compute_tau_37():
    N = 37
    coeffs = [0] * (N + 1)
    coeffs[0] = 1
    for k in range(1, N + 1):
        for _ in range(24):
            for m in range(N, k - 1, -1):
                coeffs[m] -= coeffs[m - k]
    return coeffs[N - 1]


def run():
    print("=" * 70)
    print("FIXED-POINT FORMULATION: Phys = Fix(C ∘ E)")
    print("=" * 70)
    print("  M  →[E]→  E  →[C]→  M")
    print("  Physical structures: C(E(X)) ≅ X")

    # QR structure
    QR  = {pow(x, 2, P) for x in range(1, P)}
    QNR = set(range(1, P)) - QR

    # Verify 137-map preserves QR/QNR (the fixed-point structure of the map)
    violations = [(x, 26*x%P) for x in range(1, P) if (x in QR) != (26*x%P in QR)]
    assert len(violations) == 0
    print(f"\n137-map QR-automorphism: {len(violations)} boundary crossings  check")

    # GF(37) instantiation: empirical fixed points
    print(f"\nGF(37) fixed-point examples  [C(E(O)) ≅ O]:")

    # c mod 37
    c = 299792458
    r = c % P
    assert r == 32 and r in SEED
    print(f"  c={c}:  E(c)={r} → C={orbit_label(r)}, DR={dr(r)}  check")

    # pi[:3]
    pi3 = 314
    r = pi3 % P
    assert r == 18 and r in SEED
    print(f"  π[:3]={pi3}:  E={r} → C={orbit_label(r)}, DR={dr(r)}  check")

    # 691
    r = 691 % P
    assert r == 25 and r in SA
    print(f"  691:  E={r} → C={orbit_label(r)}, DR={dr(r)}  check")

    # level 4
    assert 4 in SA
    print(f"  Level 4:  E=4 → C={orbit_label(4)}, DR={dr(4)}  check")

    # tau(37) mod 37
    t37 = compute_tau_37()
    r = t37 % P
    assert r == 31 and dr(r) == 4 and 4 in SA
    print(f"  τ(37) mod 37={r}:  DR({r})={dr(r)} → SA  check")

    # Named set count vs total GF(37)
    named_count = len(ALL_NAMED)
    total = P - 1  # nonzero elements
    print(f"\nPhys ⊊ Math verification:")
    print(f"  Named (fixed-point) elements: {named_count} / {total} of GF(37)*")
    print(f"  Non-named elements: {total - named_count}")
    print(f"  Example non-fixed-point: 2 mod 37 = 2 → not in any named set")
    assert 2 not in ALL_NAMED
    print(f"  Phys = Math would require all 36 elements to be named. False.  check")
    print(f"  Therefore: Phys ⊊ Math in this framework  check")

    # Residue condition correction via DR
    print(f"\nCorrected residue condition  Φ_f(R_f(O)) ≅ Φ_e(R_e(O)):")
    print(f"  Common invariant space Φ = DR (digital root, range {{1..9}})")
    print(f"  SA → DR ∈ {{4,9}}: {sorted({dr(x) for x in SA})}")
    print(f"  ST → DR ∈ {{3,3,3,3}}: {sorted({dr(x) for x in ST})}")
    print(f"  SEED → DR ∈ {{9,6,5}}: {sorted({dr(x) for x in SEED})}")
    print(f"  IC → DR ∈ {{1,1,8}}: {sorted({dr(x) for x in IC})}")

    print(f"\nAll verifications passed.")


if __name__ == "__main__":
    run()
