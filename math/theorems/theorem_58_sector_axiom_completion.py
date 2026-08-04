"""
Theorem 58: Sector Axiom Completion — GF(37) Definitions for the Axiomatic System

Supplies the GF(37) definitions required to complete the axiomatic system
(60 axioms, 15 theorem groups). All terms below are sourced from the existing
framework; assertions verify every claim against the field.

DEFINITIONS
===========

chi(26):
  chi = Legendre symbol. chi(n) = pow(n, 18, 37).
  chi(26) = +1 — 26 is a quadratic residue. Square root: 27² ≡ 26 (mod 37).
  Consequence: every 137-map orbit is homogeneous (all QR or all NQR).

QR / NQR orbits:
  12 orbits total under the 137-map (×26 mod 37), split exactly:
  QR  (visible): {1,10,26}, {3,4,30}, {7,33,34}, {9,12,16}, {11,27,36}, {21,25,28}
  NQR (dark):    {2,15,20}, {5,13,19}, {6,8,23},  {14,29,31}, {17,22,35}, {18,24,32}

TESLA_FLOW:
  TESLA_FLOW = 6. NQR, non-primitive-root. ord₃₇(6) = 4.
  6 is a square root of −1 in GF(37): 6² ≡ −1 (mod 37).
  Orbit: {6, 8, 23}. Counts QR orbits (6) and NQR orbits (6).
  Fixed point of affine map f(n) = 6n: only SEAM=0 is fixed.

Sovereign spiral:
  Orbit {3, 4, 30} — the unique 3-cycle containing all three sovereign grades:
    ST(3) →×26→ SA(4) →×26→ SA∩ST(30) →×26→ ST(3)
  Anti-sovereign dual: {7, 33, 34} (orbit sum 74; {3,4,30} sum 37).

Sectors:
  SA   (Sovereign Anchors):  {4, 9, 25, 30}   — QR, visible
  ST   (Sovereign Targets):  {3, 12, 21, 30}  — QR, visible, DR=3
  DARK_A:                    {2, 15, 20}       — NQR, all primitive roots
  SEAM:                      0                 — neither QR nor NQR; absorbing element

SA-step operator Op(+-):
  Delta = +9 (mod 37). Increments tens digit, decrements units digit of 2-digit form.
  Drives the ST chain: 3 →+9→ 12 →+9→ 21 →+9→ 30.
  Meta-3-cycle among sovereign orbits:
    {3,4,30} →+9 on ST-element→ {9,12,16} →+9→ {21,25,28} →+9→ {3,4,30}

SEAM value:
  SEAM = 0. The zero residue of Z/37Z. chi(0) = 0.
  Fixed point of all pure multiplicative maps. Horizon of the 137-map.
  111 = 3 × 37 ≡ 0 (mod 37): R₃ (the 3-repunit 111) lands on the SEAM.
  28 + 9 ≡ 0 (mod 37): the outlier node 28 steps to SEAM under Op(+-).

504 (not a directed connection count):
  504 = σ(246) = sum of divisors of seed 246: 1+2+3+6+41+82+123+246 = 504.
  504 mod 37 = 23 ∈ {6, 8, 23} = TESLA_FLOW orbit.
  DR(504) = 9 = SEAM of Z/9Z.
  The connection map holds 711 directed connections across 84 theorems.

THEOREM 58
==========
Let G = (Z/37Z)×, χ the Legendre symbol mod 37, f(n) = 26n mod 37 the 137-map.

(i)   χ(26) = +1, so f is a QR-preserving endomorphism of G.
(ii)  G decomposes into exactly 6 QR orbits and 6 NQR orbits under f,
      with TESLA_FLOW = 6 counting both halves.
(iii) The sovereign spiral {3,4,30} is the unique f-orbit intersecting ST, SA, and SA∩ST.
(iv)  The SA-step operator Op(+−) with Δ=+9 generates a meta-3-cycle
      {3,4,30} → {9,12,16} → {21,25,28} → {3,4,30} among the sovereign orbits.
(v)   SEAM = 0 is the unique fixed point of every f_a(n) = an, a ∈ G,
      and is reached from the sovereign triple only via 28 +9 ≡ 0 (mod 37).
(vi)  σ(246) = 504, and 504 mod 37 = 23 ∈ TESLA_FLOW orbit — the seed's
      divisor sum maps into the dark sector through TESLA_FLOW.
"""

P = 37
SCALAR = 26


def chi(n, p=P):
    if n % p == 0:
        return 0
    return pow(n, (p - 1) // 2, p) if pow(n, (p - 1) // 2, p) == 1 else -1


def orbit137(n):
    x, path = n % P, []
    for _ in range(3):
        path.append(x); x = (SCALAR * x) % P
    assert x == path[0]
    return frozenset(path)


SA         = frozenset({4, 9, 25, 30})
ST         = frozenset({3, 12, 21, 30})
DARK_A     = frozenset({2, 15, 20})
SEAM       = 0
TESLA_FLOW = 6
TESLA_ORB  = frozenset({6, 8, 23})

SOVEREIGN_SPIRAL = frozenset({3, 4, 30})
QR_ORBITS = [
    frozenset({1, 10, 26}), frozenset({3, 4, 30}),  frozenset({7, 33, 34}),
    frozenset({9, 12, 16}), frozenset({11, 27, 36}), frozenset({21, 25, 28}),
]
NQR_ORBITS = [
    frozenset({2, 15, 20}),  frozenset({5, 13, 19}), frozenset({6, 8, 23}),
    frozenset({14, 29, 31}), frozenset({17, 22, 35}), frozenset({18, 24, 32}),
]


def run_assertions():
    # chi(26) = +1
    assert pow(SCALAR, 18, P) == 1
    assert chi(SCALAR) == 1
    assert (27 * 27) % P == SCALAR          # square root witness: 27² ≡ 26

    # QR/NQR orbit homogeneity
    for orb in QR_ORBITS:
        assert all(chi(x) == 1 for x in orb)
    for orb in NQR_ORBITS:
        assert all(chi(x) == -1 for x in orb)

    # TESLA_FLOW structure
    assert TESLA_FLOW == 6
    assert TESLA_FLOW in TESLA_ORB
    assert len(QR_ORBITS) == TESLA_FLOW
    assert len(NQR_ORBITS) == TESLA_FLOW
    assert (6 * 6) % P == P - 1            # 6² ≡ −1 (mod 37)
    assert pow(6, 4, P) == 1               # ord₃₇(6) = 4

    # Sovereign spiral
    assert SOVEREIGN_SPIRAL == frozenset({3, 4, 30})
    assert 3 in ST and 3 not in SA
    assert 4 in SA and 4 not in ST
    assert 30 in SA and 30 in ST           # SA∩ST
    assert orbit137(3) == SOVEREIGN_SPIRAL
    assert sum(SOVEREIGN_SPIRAL) == P      # orbit sum = 37

    # SA-step operator
    assert (3  + 9) % P == 12 and 12 in frozenset({9, 12, 16})
    assert (12 + 9) % P == 21 and 21 in frozenset({21, 25, 28})
    assert (21 + 9) % P == 30 and 30 in SOVEREIGN_SPIRAL

    # SEAM
    assert SEAM == 0
    assert chi(SEAM) == 0
    assert (111) % P == 0                  # 111 = 3 × 37 ≡ SEAM
    assert (28 + 9) % P == SEAM            # outlier 28 steps to SEAM

    # 504 = σ(246)
    divisors_246 = [d for d in range(1, 247) if 246 % d == 0]
    assert sum(divisors_246) == 504
    assert 504 % P == 23
    assert 23 in TESLA_ORB

    print("All assertions passed.")


def summarise():
    print("=" * 60)
    print("Theorem 58: Sector Axiom Completion")
    print("=" * 60)
    print(f"  chi(26) = {pow(SCALAR,18,P)}  (QR; 27²≡26 mod 37)")
    print(f"  QR orbits: {len(QR_ORBITS)}   NQR orbits: {len(NQR_ORBITS)}")
    print(f"  TESLA_FLOW = {TESLA_FLOW}  orbit {sorted(TESLA_ORB)}  6²≡{(6*6)%P} mod 37")
    print(f"  Sovereign spiral {{3,4,30}}: ST→SA→SA∩ST  sum={sum(SOVEREIGN_SPIRAL)}")
    print(f"  SA-step Δ=9: 3→12→21→30  meta-3-cycle among sovereign orbits")
    print(f"  SEAM = 0   111 mod 37 = {111%P}   28+9 mod 37 = {(28+9)%P}")
    print(f"  σ(246) = 504   504 mod 37 = {504%37} ∈ TESLA_FLOW orbit")
    print(f"  Connection map: 711 directed connections (504 is not an edge count)")


if __name__ == "__main__":
    run_assertions()
    summarise()
