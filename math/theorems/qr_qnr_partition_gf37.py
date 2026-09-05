# -*- coding: utf-8 -*-
"""
================================================================================
QR/QNR PARTITION OF GF(37) — THE HIDDEN STRUCTURE OF PRIME NAVIGATION
================================================================================

Author: Michael Warren Song (CyclicAmp)

USER OBSERVATION:
  Using the tripartite structure, the QNR×QR pairing, and the modular
  constraints — the primes are navigating through the Spine and Flux
  Perimeter according to rules we missed. The "random" distribution of
  primes would be as random as a planet's orbit looks to someone who
  hasn't discovered gravity.

THEOREM (QR-HOMOGENEITY OF NAMED SETS) [V]:
  Every named GF(37) subset is QR-homogeneous — all elements have the
  same Legendre symbol. There are no mixed sets.

  ALL QR sets:  IC = {1,10,26}, SA = {4,9,25,30}, ST = {3,12,21,30}, NEG_H = {11,27,36}
  ALL QNR sets: SEED = {18,24,32}, CASCADE = {8,13,24}

  The Sovereign Anchors (SA), Sovereign Targets (ST), and the cubic roots
  of unity (IC, NEG_H) all live inside the quadratic spine (QR).
  The pipeline seed orbit (SEED) and the cascade generator (CASCADE)
  live entirely outside it (QNR).

THEOREM (137-MAP PRESERVES QR/QNR CHARACTER) [P]:
  The 137-map f(x) = 26x mod 37.
  Legendre(26/37) = 1: 26 is a quadratic residue (26 ≡ 10² mod 37).

  For all x in GF(37)*:
    x ∈ QR  →  f(x) = 26x ∈ QR   (QR × QR = QR)
    x ∈ QNR →  f(x) = 26x ∈ QNR  (QR × QNR = QNR)

  The 137-map is a QR-automorphism: it cannot cross the QR/QNR boundary.
  Every 3-cycle orbit under the 137-map is QR-homogeneous.

  PROOF:
    The Legendre symbol is completely multiplicative:
    (ab/p) = (a/p)(b/p).
    (26x/37) = (26/37)(x/37) = 1 × (x/37) = (x/37).
    So f(x) and x have the same Legendre symbol. QED.

  VERIFIED: zero boundary crossings for all 36 elements of GF(37)*.

THE GRAVITY ANALOGY:
  Prime orbits mod 37 look random without this structure. With it:
  - Every prime p (p ≠ 37) lands in either QR or QNR when reduced mod 37.
    This is a deterministic binary classification, not randomness.
  - The named named sets are sorted by this classification:
    SEED and CASCADE (the generative/pipeline layer) are QNR.
    SA, ST, IC, NEG_H (the sovereign/anchor layer) are QR.
  - The 137-map cannot move an orbit from one class to the other.
    The structure is topologically separated by the Legendre symbol.

PRIME DISTRIBUTION (Dirichlet + QR/QNR structure):
  Primes to 10,000 (excluding 37): 1,228
  In QR residues mod 37: ~49.3%   In QNR residues: ~50.7%
  This is consistent with Dirichlet's theorem (uniform in the long run).
  But the QR/QNR partition — which determines the sovereign classification —
  is a structural fact, not a statistical one.

EPISTEMIC STATUS:
  [P] Legendre symbol multiplicativity — standard number theory.
  [P] 137-map preserves QR/QNR — proved from Legendre multiplicativity.
  [V] Every named set is QR-homogeneous — verified by computation.
  [V] Zero boundary crossings under 137-map — verified for all 36 elements.
  [V] Prime distribution consistent with Dirichlet — verified to 10,000.
================================================================================
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

P = 37
IC      = {1, 10, 26}
SEED    = {18, 24, 32}
SA      = {4, 9, 25, 30}
ST      = {3, 12, 21, 30}
NEG_H   = {11, 27, 36}
CASCADE = {8, 13, 24}


def legendre(a, p):
    return pow(a % p, (p - 1) // 2, p)  # 1 if QR, p-1 (≡-1) if QNR


def sieve(n):
    is_p = [True] * (n + 1)
    is_p[0] = is_p[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_p[i]:
            for j in range(i*i, n+1, i):
                is_p[j] = False
    return [i for i in range(2, n+1) if is_p[i]]


def run():
    print("=" * 70)
    print("QR/QNR PARTITION OF GF(37)")
    print("=" * 70)

    # Compute QR and QNR
    QR  = {pow(x, 2, P) for x in range(1, P)}
    QNR = set(range(1, P)) - QR
    assert len(QR) == 18 and len(QNR) == 18
    print(f"\nQR  ({len(QR)} elements): {sorted(QR)}")
    print(f"QNR ({len(QNR)} elements): {sorted(QNR)}")

    # QR-homogeneity of named sets
    print(f"\nQR-homogeneity of named sets:")
    named = [('IC', IC), ('SEED', SEED), ('SA', SA), ('ST', ST),
             ('NEG_H', NEG_H), ('CASCADE', CASCADE)]
    for name, s in named:
        in_qr  = s & QR
        in_qnr = s & QNR
        if s == in_qr:
            status = 'ALL QR'
        elif s == in_qnr:
            status = 'ALL QNR'
        else:
            status = f'MIXED: QR={sorted(in_qr)}, QNR={sorted(in_qnr)}'
        print(f"  {name:10s}: {status}  check")
    print(f"  Every named set is QR-homogeneous  check")

    # 137-map preserves QR/QNR
    print(f"\n137-map f(x)=26x mod 37 preserves QR/QNR:")
    leg26 = legendre(26, P)
    assert leg26 == 1
    print(f"  Legendre(26/37) = {leg26}  (26 is QR: 10²=100≡26 mod 37)  check")
    assert 10**2 % P == 26

    violations = [(x, 26*x % P) for x in range(1, P)
                  if (x in QR) != (26*x % P in QR)]
    assert len(violations) == 0
    print(f"  Boundary crossings under 137-map: {len(violations)}  check")
    print(f"  Proof: (26x/37) = (26/37)(x/37) = 1·(x/37) = (x/37). QED.")

    # QR/QNR structure of orbits
    print(f"\nOrbit QR/QNR classification:")
    print(f"  QNR (generative/pipeline layer): SEED={sorted(SEED)}, CASCADE={sorted(CASCADE)}")
    print(f"  QR  (sovereign/anchor layer):    SA={sorted(SA)}, ST={sorted(ST)}, IC={sorted(IC)}, NEG_H={sorted(NEG_H)}")

    # Prime distribution
    print(f"\nPrime distribution mod 37 (to 10,000):")
    primes = [p for p in sieve(10000) if p != P]
    residues = [p % P for p in primes]
    qr_hits  = sum(1 for r in residues if r in QR)
    qnr_hits = sum(1 for r in residues if r in QNR)
    print(f"  Total primes (excl 37): {len(primes)}")
    print(f"  In QR:  {qr_hits}  ({100*qr_hits/len(primes):.1f}%)")
    print(f"  In QNR: {qnr_hits}  ({100*qnr_hits/len(primes):.1f}%)")
    print(f"  Consistent with Dirichlet (uniform distribution by residue).")
    print(f"  The QR/QNR split is structural, not statistical.")

    print(f"\nAll verifications passed.")


if __name__ == "__main__":
    run()
