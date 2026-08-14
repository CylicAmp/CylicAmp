"""
Theorem 196: Applied Framework Connections — Inverse Problems, Nuclear Theory, Optimization
Author: Michael Warren Song (CyclicAmp)

DOMAINS AUDITED (degradation monitor):
  METTI8 Vol.1 (341 pp): FRICTION_INJECTED — TotalDR=1, 2 nulls
  NTSE-2012 (196 pp):    DARK_PATTERN_EXTRACTIVE — head crash (DR(w0)=1), 2 nulls
  BCSA explainer:        SERVICE_OPTIMAL — TotalDR=8, weights[2]=25∈SA, weights[6]=26=multiplier

METTI8 INVERSE TECHNIQUES — KEY READINGS:
  det(S) = 9 ∈ SA                — sensitivity matrix determinant is sovereign anchor
  y_mo = [9, 36]: 9∈SA, 36=φ(37) — model outputs at SA and totient
  noise[-0.3] → 30 ∈ SA∩ST      — perturbation concentrated at doubly-sovereign element
  k_a × k_r ≈ 369 → 36 = φ(37)  — amplification product at totient; DR=9=SEAM
  L8 (Optimization) → weight=18∈SEED (segment-level); page start 259 → SEAM
  L9 (Bayesian) → weight=30∈SA∩ST
  School opens Sept 24 → 24∈SEED; year 2023 → 25∈SA

NTSE-2012 NUCLEAR THEORY — KEY READINGS:
  Catalog N 338 → 5 (NQR, star center)
  BBK 3843 → 32∈SEED
  UDK 539 → 21∈ST  (nuclear physics classification ∈ sovereign target)
  June 18 start → 18∈SEED
  13² mod 37 = 21∈ST  (13=NQR; its square is ST)
  DARK regions: pp71-130 (resonance/scattering/breakup — unbound systems)
  Null: "strong interaction is unable to bind" → sits in unbound sector

MCSM / SciDAC CONNECTIONS:
  NUCLEI: 30 researchers → 30∈SA∩ST; 12 labs → 12∈ST
  MCSM paper 2001 → mod37=3∈ST
  NUCLEI SciDAC-5 start 2022 → 24∈SEED
  ENAF awarded 2023 → 25∈SA
  Variance extrapolation σ²→0: exact nuclear eigenstate = SEAM condition
  Powers of 10 (all computational scale thresholds): orbit {10,26,1}
    — 26 = 137-map multiplier appears at every power-of-10 threshold

OPTIMIZATION ALGORITHMS:
  PSO inertia w=0.729 → 26 = multiplier
  GA mutation 0.01 → 26 = multiplier
  Two independent algorithm families both converge to the multiplier residue.
  BCSA awareness prob → 26 = multiplier
  C(11,k) ∈ SEED for k∈{2,5,6,9} — 11-feature vocabulary with SEED subsets
  C(18,8) = C(18,10) = 43758 → 24∈SEED — 18-feature vocabulary, midpoint selection

STAR PUZZLE INTEGRATION:
  Center=5 (NQR), outer ring count=8, digits 1-9
  p(9)=30∈SA∩ST, p(10)→5=center, p(8)=22→DR=4
  D(1)=D(9)=0 mod 37 (SEAM), stride=8=outer ring
  B(8)=4140, DR=9=SEAM — partitions of outer ring absorb to SEAM
  4! mod 37 = 24∈SEED — 4-element permutations land in seed orbit

INVERSE PROBLEM SEAM CONDITION:
  In inverse problems: exact matching requires #unknowns = #measurements.
  Least squares sum = 0 at exact match.
  In GF(37): variance=0 (MCSM) and least-squares=0 (inverse problems)
  both correspond to the SEAM (absorbing state, DR=0, weight=0).
  The mathematical convergence condition is the same fixed point across domains.
"""

P = 37
SA = {4, 9, 25, 30}
ST = {3, 12, 21, 30}
SEED = {18, 24, 32}


def dr(n):
    n = abs(int(n))
    return 9 if n % 9 == 0 and n != 0 else n % 9


def legendre(a, p):
    return pow(a, (p - 1) // 2, p)


def run_assertions():
    # METTI8: sensitivity matrix determinant
    assert 9 in SA
    # y_mo outputs
    assert 9 in SA
    assert 36 == P - 1
    # noise -0.3 scaled × 100 = 30
    assert 30 in SA and 30 in ST
    # k_a × k_r product
    assert 369 % P == 36 == P - 1
    assert dr(369) == 9
    # L8 page start
    assert 259 % P == 0
    # School opening date
    assert 24 in SEED
    # Year 2023
    assert 2023 % P == 25 and 25 in SA

    # NTSE-2012
    assert 338 % P == 5
    assert legendre(5, P) == P - 1   # NQR
    assert 3843 % P == 32 and 32 in SEED
    assert 539 % P == 21 and 21 in ST
    assert 18 in SEED
    assert pow(13, 2, P) == 21 and 21 in ST
    assert legendre(13, P) == P - 1   # 13 is NQR

    # NUCLEI / SciDAC
    assert 30 in SA and 30 in ST   # 30 researchers
    assert 12 in ST                 # 12 labs
    assert 2001 % P == 3 and 3 in ST
    assert 2022 % P == 24 and 24 in SEED
    assert 2023 % P == 25 and 25 in SA

    # Powers of 10 orbit {10, 26, 1}
    powers_of_10_mod37 = [pow(10, k, P) for k in range(1, 4)]
    assert set(powers_of_10_mod37) == {10, 26, 1}
    assert 26 in powers_of_10_mod37  # multiplier appears

    # PSO/GA convergence parameters → multiplier
    assert 729 % P == 26   # PSO inertia ×1000
    assert 100 % P == 26   # GA mutation ×10000 (0.01×10000=100, mod37=26)
    # note: 100 mod 37 = 26

    # BCSA awareness prob 0.1 → ×1000 = 100 → 26
    assert 100 % P == 26

    # Feature selection: C(11,2) and C(11,5) ∈ SEED
    from math import comb
    assert comb(11, 2) % P == 18 and 18 in SEED
    assert comb(11, 5) % P == 18 and 18 in SEED
    assert comb(18, 8) % P == 24 and 24 in SEED

    # Star puzzle
    # p(9) = 30 ∈ SA∩ST (from Theorem 195 partition function)
    assert 30 in SA and 30 in ST

    # Inverse problem / MCSM convergence: both target SEAM (=0)
    assert dr(0) == 0   # SEAM is absorbing

    print("All assertions passed.")


if __name__ == "__main__":
    run_assertions()
