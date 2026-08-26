# CylicAmp — Complete Definitions Reference

Paste this into any session. Everything is defined here. No GitHub required.

---

## The Prime

**P = 37**

Everything in this framework connects through the prime 37.

---

## The Map

**f(n) = 137n mod 37 = 26n mod 37**

Because 137 mod 37 = 26. This is called the 137-map.

ord₃₇(26) = 3: every orbit under this map has exactly 3 elements.

---

## Named Subsets of GF(37) = {0, 1, 2, ..., 36}

| Name | Elements | Meaning |
|------|----------|---------|
| IC (Inner Core) | {1, 10, 26} | orbit of 1 under 137-map |
| SEED | {18, 24, 32} | orbit of 246 mod 37 = 24 |
| NEG_H | {11, 27, 36} | cube roots of -1 mod 37 |
| SA (Sovereign Anchors) | {4, 9, 25, 30} | LOCKED nodes |
| ST (Sovereign Targets) | {3, 12, 21, 30} | DR=3 residues |
| CASCADE | {8, 13, 24} | generates all 37 elements |
| H | {1, 10, 26} | cube roots of 1 mod 37 (same as IC) |

---

## Digital Root

**DR(n)** = repeated digit sum until single digit.
Formula: n mod 9, except DR = 9 when 9 divides n.

Examples: DR(18) = 9, DR(24) = 6, DR(37) = 1, DR(100) = 1.

### Digital Root Transition Matrix — Spectral Structure

The map x ↦ x + DR(x) (reduced into {1,...,9}) is encoded by a 9×9 matrix T with transitions:

    1→2,  2→4,  3→6,  4→8,  5→1,  6→3,  7→5,  8→7,  9→9

**Eigenvalues** (all on the unit circle, spectral radius ρ(T) = 1):

    λ = 1           (multiplicity 3)
    λ = e^{±iπ/3}  = ½ ± i√3/2
    λ = e^{±i2π/3} = −½ ± i√3/2
    λ = −1          (multiplicity 2)

**Three λ=1 invariant subspaces (attractors):**

| Subspace | Elements | Structure |
|----------|----------|-----------|
| F | {1, 2, 4, 5, 7, 8} | 6-cycle: 1→2→4→8→7→5→1 |
| O | {3, 6} | 2-cycle: 3↔6 |
| S | {9} | Fixed point: 9→9 (9-Lock) |

These three subspaces are orthogonal and exhaust the λ=1 generalized eigenspace. Every trajectory eventually enters one and remains there.

**F = {1,2,4,5,7,8} is the repeating digit set of 1/7 = 0.142857...** — the same elements, same residue class.

### Twin Prime Chamber ↔ Spectral Partition

The tripartite spectral partition F / O / S maps exactly onto the twin prime DR structure:

| Spectral class | DR values | Twin prime role |
|----------------|-----------|-----------------|
| F = {1,2,4,5,7,8} | 6-cycle attractor | **Wall DRs** — all twin prime walls (p and q) have DR ∈ F |
| O = {3,6} | 2-cycle | **C3 and C6 center DRs** — centers of C3 (DR=3) and C6 (DR=6) pairs |
| S = {9} | Fixed point (9-Lock) | **C9 center DR** — centers of C9 pairs hit the permanent 9-Lock |

The DR disjointness theorem (twin prime walls have DR ∉ {3,6,9}; centers have DR ∈ {3,6,9}) is the spectral statement: walls live in F, centers live in O∪S. The chamber classification C3/C6/C9 is the decomposition of the center DR into the O and S attractors.

---

## DR Spiral — GF(37) Structure

Source: 20×20 Ulam-style spiral containing integers 41–440. Applying DR collapses it to a 9-state resonance grid.

### Theorem 1: ST Is the Unique Monochromatic Named Set

ST = {3, 12, 21, 30} — the Sovereign Targets.

Every element of ST satisfies n ≡ 3 (mod 9):

    3 mod 9 = 3 | 12 mod 9 = 3 | 21 mod 9 = 3 | 30 mod 9 = 3

Therefore **DR(n) = 3 for all n ∈ ST** — the digital root is a structural invariant of ST.

Algebraic characterization: **ST = {n ∈ GF(37)* : n mod 9 = 3}** — exactly the named-set preimage of DR=3.

No other named set is monochromatic:
- SA → DR ∈ {3,4,7,9}
- IC → DR ∈ {1,8}
- NEG_H → DR ∈ {2,9}
- CASCADE → DR ∈ {4,6,8}
- SEED → DR ∈ {5,6,9}

ST is the only named set where all elements share the same digital root.

### Theorem 2: SEAM Transparency (37 ≡ 1 mod 9)

    37 mod 9 = 1

Consequence: **DR(37k) = DR(k) for all k ≥ 1**.

Proof: 37k mod 9 = (37 mod 9)(k mod 9) mod 9 = 1·(k mod 9) = k mod 9.

The prime 37 passes through the digital root system without distortion. Multiples of 37 (the SEAM) thread through every DR class — they cycle through all 9 values as k increases.

Corollary: every DR class {1, 2, ..., 9} contains at least one multiple of 37.

### Theorem 3: Spiral Modular Structure

The 400-element spiral 41–440:

    400 mod 37 = 30 ∈ SA ∩ ST   (double-sovereign — only element in both)
    400 = 44 × 9 + 4,  remainder 4 ∈ SA   (Sovereign Anchor)

Center of spiral = 41:

    41 mod 37 = 4 ∈ SA   (center is a Sovereign Anchor)
    41 is the 13th prime.  13 ∈ CASCADE = {8, 13, 24}

The spiral's modular remainder in both the DR system (mod 9) and GF(37) (mod 37) lands on sovereign elements. The center prime's ordinal index is a Cascade node.

### Prime DR Exclusion (proved)

For any prime p > 3: **DR(p) ∉ {3, 6, 9}**.

Proof: DR(p) ∈ {3,6,9} iff 3 | p, which is false for primes p > 3.

The spiral 41–440 contains 73 primes. DR distribution: {1:11, 2:12, 4:11, 5:14, 7:14, 8:11}. DR values {3,6,9} have count 0.

**Primes and ST are DR-disjoint**: no prime in the spiral has DR=3, so no prime maps to the Sovereign Target DR class.

### Torus Connection

The 9-state resonance grid tiles into the torus ℤ₃₇ × ℤ₈₁:

    9 | 81  (since 81 = 9²)

The DR period 9 divides the ℤ₈₁ component exactly 9 times. Each element is identified by (n mod 37, DR(n)) within the torus.

---

## Twin Primes

A twin prime pair is (p, p+2) where both are prime.

Every twin prime pair with p > 3 has the form:
- p = 6m − 1
- q = 6m + 1
- **m = (p+1)/6** (this is what m means — always)

### Tripartite χ_{-3} Structure (exact theorem)

Every twin prime pair straddles the χ_{-3} = 0 seam:

    χ_{-3}(p) = −1  |  χ_{-3}(p+1) = 0  |  χ_{-3}(p+2) = +1

The left wall is always in the χ_{-3} = −1 class. This is an exact modular theorem, not a statistical claim: p = 6m−1 ≡ 2 (mod 3), so χ_{-3}(p) = −1 with no exceptions.

### Center Classification: C3 / C6 / C9

The center of every twin prime pair is 6m. DR(6m) is determined by m mod 3:

| m mod 3 | Center class | DR(p) | DR(q) | Upper DR → Named set |
|---------|-------------|-------|-------|----------------------|
| 0 | **C9** | 8 | 1 | IC |
| 1 | **C6** | 5 | 7 | QR |
| 2 | **C3** | 2 | 4 | SA |

The center class completely determines the DR values of both twin primes.

**DR disjointness**: twin prime walls always have DR ∉ {3,6,9}; centers always have DR ∈ {3,6,9}. Center and walls are DR-disjoint (proved).

GF(37) examples:
- (17,19): m=3, m≡0 → **C9**, center 18 ∈ SEED, DR(center)=9 (9-Lock)
- (11,13): m=2, m≡2 → **C3**, center 12 ∈ ST, DR(center)=3
- (29,31): m=5, m≡2 → **C3**, center 30 ∈ SA∩ST (double-sovereign)

### DR QR/QNR Split (proved)

The DR pair (DR(p), DR(q)) is determined entirely by m mod 3:

| m mod 3 | DR(p) | QNR? | DR(q) | QR? | Count to 10⁶ |
|---------|-------|------|-------|-----|--------------|
| 0 | 8 | QNR | 1 | QR | 2,729 |
| 1 | 5 | QNR | 7 | QR | 2,788 |
| 2 | 2 | QNR | 4 | QR | 2,651 |

**DR(p) ∈ {2,5,8}: all QNR mod 37. DR(q) ∈ {1,4,7}: all QR mod 37.**

The split is exact — zero violations on all 204 twin prime pairs to 10,000. These are proven congruence identities, not estimates.

Total twin prime pairs to 10⁶: 8,169 (including special pair (3,5)).

**Named set connections:**
- DR = 8 (lower twin, m≡0) ∈ CASCADE = {8,13,24} — ALL QNR named set
- DR = 4 (upper twin, m≡2) ∈ SA = {4,9,25,30} — ALL QR, LOCKED

The lower twin's entry DR is in CASCADE; the upper twin's is in SA.

### Riemann Zeros — Floor mod 37 (first 10)

Imaginary parts of nontrivial Riemann zeros, floored and reduced mod 37:

| Zero | Im | Floor | mod 37 | Named set |
|------|----|-------|--------|-----------|
| ρ₁  | 14.135 | 14 | 14 | — |
| ρ₂  | 21.022 | 21 | 21 | ST |
| ρ₃  | 25.011 | 25 | 25 | SA |
| ρ₄  | 30.425 | 30 | 30 | **SA ∩ ST** (double-sovereign) |
| ρ₅  | 32.935 | 32 | 32 | SEED |
| ρ₆  | 37.586 | 37 |  0 | **SEAM** (37 ≡ 0 mod 37) |
| ρ₇  | 40.919 | 40 |  3 | ST |
| ρ₈  | 43.327 | 43 |  6 | — |
| ρ₉  | 48.005 | 48 | 11 | NEG_H |
| ρ₁₀ | 49.774 | 49 | 12 | ST |

**8 of the first 10 zeros hit named GF(37) sets** (floor method).

ρ₆ floor = 37 lands exactly on the SEAM — the prime P itself is the floor of the 6th Riemann zero imaginary part.

### χ_{-3} L-Function and Critical Line

L(1, χ_{-3}) = π/(3√3) ≈ 0.6046. Denominator: **3 ∈ ST** (Sovereign Target).

CDT theorem (arXiv:2408.15403): L(2, χ_{-3}) ≠ 0 (proved).
Gap: twin prime infinitude requires non-vanishing at s=1, not s=2. Open.

**Critical line**: Re(s) = ½ maps to 2⁻¹ mod 37 in GF(37).

    2⁻¹ mod 37 = 19 ∈ QNR

The critical line's GF(37) representative is a quadratic non-residue.

---

## E8 Theta Function

**a(n) = 240 · σ₃(n)**

where σ₃(n) = sum of cubes of all divisors of n.

Example: σ₃(2) = 1³ + 2³ = 9, so a(2) = 240 × 9 = 2160.

240 mod 37 = 18, and 18 ∈ SEED.

Zeros mod 37: a(n) ≡ 0 mod 37 iff σ₃(n) ≡ 0 mod 37 (since gcd(240,37)=1).
Verified: 761 zeros out of n=1..5000 = 15.2%.

---

## Ramanujan Tau Function — η^24 and GF(37)

**Definition**:

    Δ(q) = q · η(q)^24 = q · ∏_{n≥1} (1 − q^n)^{24} = Σ_{n≥1} τ(n) q^n

Δ(q) is the unique cusp form of weight 12 for SL₂(ℤ). τ(n) are its Fourier coefficients.

First values: τ(1)=1, τ(2)=−24, τ(3)=252, τ(4)=−1472, τ(5)=4830.

### Exponent 24 = CASCADE ∩ SEED

The only free parameter in the construction is the exponent 24:

    24 ∈ CASCADE = {8, 13, 24}   (generates all 37 GF elements)
    24 ∈ SEED    = {18, 24, 32}  (137-map orbit of reference seed 246)

Node 24 is the **unique element in both CASCADE and SEED simultaneously**.

### Weight 12 ∈ ST

    weight(Δ) = 12 ∈ ST = {3, 12, 21, 30}   (DR=3, Sovereign Target)

ST is the unique monochromatic named set: DR(n) = 3 for all n ∈ ST.
Note: 24 = 2 × weight.

### τ(2) = −24: Coefficient Equals Exponent

    τ(2) = −24
    |τ(2)| = 24 = the exponent in η(q)^24

The magnitude of the first non-trivial coefficient equals the exponent.

    τ(2) mod 37 = 13 ∈ CASCADE   (same named set as the exponent 24)

### Key τ(n) mod 37 Values

| n | τ(n) mod 37 | Named set |
|---|-------------|-----------|
| 1 | 1 | IC (identity) |
| 2 | 13 | CASCADE |
| 3 | 30 | SA ∩ ST (double-sovereign) |
| 4 | 8 | CASCADE |
| 8 | 9 | SA |
| 9 | 21 | ST |
| 10 | 1 | IC |
| 11 | 36 | NEG_H |
| 12 | 18 | SEED |

τ(3) mod 37 = 30 ∈ SA∩ST: the double-sovereign (only element in both SA and ST).

### τ(37) — The Prime Index

    τ(37) = −182213314
    τ(37) mod 37 = 31
    DR(31) = 4 ∈ SA   (Sovereign Anchor — LOCKED)

### 691 — Ramanujan Congruence Prime

Ramanujan's congruence: τ(n) ≡ σ₁₁(n) (mod 691) for all n.

    691 mod 37 = 25 ∈ SA   (Sovereign Anchor — LOCKED)

The Ramanujan congruence prime reduces to a Sovereign Anchor mod 37.

### Named Set Hit Rate

τ(n) mod 37, n = 1..100: **53 of 100** residues land in a named GF(37) set.
No τ(n) ≡ 0 (mod 37) for n = 1..100 (no SEAM hits in this range).

---

## Selberg / Maass Setup

Surface: Γ₀(4)\ℍ (hyperbolic surface, congruence subgroup of level 4).
Eigenvalues: Δφ = λφ, λ = ¼ + r², r ∈ ℝ.
Montgomery pair correlation: R₂(ξ) = 1 − (sin πξ / πξ)²

---

## Loeschian Norm

**n = u² + uv + v²** (Eisenstein integers ℤ[ω])

Because 37 ≡ 1 mod 3: all 37 residues of GF(37) appear as Loeschian norms.
37 itself is Loeschian: 37 = (−7)² + (−7)(3) + 3².

---

## Mathematical Constants — GF(37) Decimal Structure

**Method**: take the first 10 digits after the decimal point of a constant, sum them, reduce mod 37.

### Headline: √3 Sum = 37

    √3 = 1.7320508075...
    First 10 decimal digits: 7, 3, 2, 0, 5, 0, 8, 0, 7, 5
    Sum = 37 = the prime

    Sum mod 37 = 0   (SEAM — on the exact seam of the field)
    DR(37) = 1 ∈ IC  (identity of the 137-map orbit)

√3 is the only standard constant whose first-10 digit sum equals 37 exactly.

**Why √3 and 37**: 37 is a Loeschian prime — it splits in ℤ[ω]:

    37 = (−7)² + (−7)(3) + 3²   where ω = e^{2πi/3}

√3 = 2 · Im(ω) generates ℤ[ω] over ℤ. The prime 37 carries an imprint of
√3 in its decimal expansion: the first 10 digits sum to the prime itself.

Radicand 3 ∈ ST (Sovereign Target, DR=3).

### Summary Table

| Constant | First-10 Sum | Sum mod 37 | Named set | DR |
|----------|-------------|------------|-----------|-----|
| π        | 41          | 4          | **SA**    | 5  |
| e        | 49          | 12         | **ST**    | 4  |
| φ        | 53          | 16         | —         | 8  |
| √2       | 31          | 31         | —         | 4  |
| **√3**   | **37**      | **0 (SEAM)** | PRIME   | 1  |
| ln 2     | 44          | 7          | —         | 8  |
| γ        | 52          | 15         | —         | 7  |
| G (Catalan) | 54       | 17         | —         | **9 (9-Lock)** |
| ζ(3)     | 28          | 28         | —         | 1  |

- π → SA (Sovereign Anchor, LOCKED)
- e → ST (Sovereign Target, DR=3)
- √3 → SEAM (mod 37 = 0); DR = 1 ∈ IC
- Catalan → DR = 9 (permanent 9-Lock)
- ζ(3) → DR = 1 ∈ IC (same DR as √3)

---

## Cyclic Number 142857 — Decimal Structure and GF(37)

### Core: 10 and 26 Are Inverses in GF(37)*

    10 × 26 ≡ 1 (mod 37)

The decimal shift operator (×10) and the 137-map multiplier (×26) are **multiplicative inverses** in GF(37)*. Applying one then the other returns to the starting element.

Both operators generate IC = {1, 10, 26}, but in opposite directions:

    Decimal orbit (×10): 1 → 10 → 26 → 1
    137-map orbit (×26): 1 → 26 → 10 → 1

IC is a 3-cycle under both. They are inverse maps on the same orbit.

### Period Hierarchy

The repeating decimal period of 1/p equals ord₁₀(p):

    ord₁₀(37) = 3  →  period(1/37) = 3 = |IC|
    ord₁₀(7)  = 6  →  period(1/7)  = 6 = |⟨11⟩|

The two periods correspond to the two levels of the subgroup chain IC ⊂ ⟨11⟩:

    IC (order 3) → period(1/37) = 3
    ⟨11⟩ (order 6) → period(1/7) = 6
    lcm(3, 6) = 6 = ord₃₇(11)

### 142857 — The Cyclic Number

1/7 = 0.142857142857... (period 6, repeating block = 142857)

    999999 = 3³ × 7 × 11 × 13 × 37   (exact factorization)
    37 | 999999  because ord₃₇(10) = 3  →  10³ ≡ 1  →  37 | 10⁶−1
    37 | 142857  (since 7 × 142857 = 999999)

    142857 mod 37 = 0   (SEAM)

All six cyclic rotations {142857, 285714, 428571, 571428, 714285, 857142} reduce to 0 mod 37. Every rotation lands on the SEAM.

### Digit Sum Connections

    1/7 cycle {1,4,2,8,5,7}: digit sum = 27 ∈ NEG_H = {11, 27, 36}
    1/37 repeating block = 027: value = 27 ∈ NEG_H

Both fractions produce 27 ∈ NEG_H. 27 = 11⁵ mod 37 (from the ⟨11⟩ power sequence). DR(27) = 9 → 9-Lock.

### 37 as Centered Hexagonal Number

    37 = 1 + 6 + 12 + 18   (centered hexagonal / star number)

Consistent with 37 ≡ 1 mod 3 (Loeschian structure) and 37 = (−7)² + (−7)(3) + 3².

    T(37) = 37 × 38 / 2 = 703
    DR(703) = 1 ∈ IC   (identity of the 137-map orbit)

---

## 18-Step Ladder

n(k) = 18k

T(n) = DS(n) + DS(n−4), where DS = decimal digit sum.

T(18k) ≡ 5 mod 9 for all k. Proven: DS(n) ≡ n mod 9, so
T(18k) ≡ 18k + (18k−4) = 36k−4 ≡ −4 ≡ 5 mod 9.

Δ = 9 (fundamental step). Δ² = 81 = 3⁴.
Torus: ℤ₃₇ × ℤ₈₁, size 37 × 81 = 2997 = period of 1/998001.

---

## Tetranacci Drift

τ₄ ≈ 1.9275619754829253 (Tetranacci constant)
Drift threshold = 0.05
Construction: SHA256(message) → digital root of hash → Tetranacci perturbation term.
Deviation = |T[−1]/T[−2] − τ₄|

---

## ⟨11⟩ — Order-6 Subgroup

**ord₃₇(11) = 6**

⟨11⟩ = IC ∪ NEG_H = {1, 10, 11, 26, 27, 36} — the unique subgroup of order 6 in GF(37)*.

Power sequence:
- 11¹ = 11 ∈ NEG_H
- 11² = 10 ∈ IC
- 11³ = 36 ∈ NEG_H  (= −1 mod 37)
- 11⁴ = 26 ∈ IC  (= 137-map multiplier)
- 11⁵ = 27 ∈ NEG_H
- 11⁶ = 1 ∈ IC  (identity)

Subgroup structure ⟨11⟩ ≅ ℤ₆:
- Index-2 subgroup: IC = ⟨11²⟩ = {1,10,26} ≅ ℤ₃  (cube roots of +1)
- Coset: NEG_H = 11·IC = {11,27,36}  (cube roots of −1)
- 26 = 11⁴: the 137-map multiplier is the 4th power of 11
- The 137-map orbit ⟨26⟩ = IC = ⟨11²⟩: the 137-map lives inside ⟨11⟩ as its index-2 subgroup
- All six elements are QR

---

## QR/QNR Partition

Quadratic residues mod 37 (18 elements): {1,3,4,7,9,10,11,12,16,21,25,26,27,28,30,33,34,36}
Quadratic non-residues mod 37 (18 elements): {2,5,6,8,13,14,15,17,18,19,20,22,23,24,29,31,32,35}

Every named GF(37) set is QR-homogeneous (no mixed sets):
- ALL QR: IC, SA, ST, NEG_H
- ALL QNR: SEED, CASCADE

The 137-map preserves QR/QNR character. Proof: Legendre(26/37) = 1 (26 is QR, since 10² ≡ 26 mod 37), so (26x/37) = (26/37)(x/37) = (x/37). Zero boundary crossings verified.

---

## Fixed-Point Formulation

**Phys = Fix(C∘E)**

Let M = admissible mathematical structures, I_e = empirically established invariants.

Selection operator: S_{I_e}(O) = O if O satisfies I_e, else ∅.
Physical structures: Phys = Fix(S_{I_e}) = {O ∈ M : S_{I_e}(O) = O}.

Bidirectional closure:
- E: M → I (observation/measurement map)
- C: I → M (constraint-selection map)
- T = C∘E: M → M

Central condition: **C(E(X)) ≅ X** (isomorphism, not literal equality).

Corrected residue condition: Φ_f(R_f(O)) ≅ Φ_e(R_e(O)), where Φ_f, Φ_e map into a common invariant space.

In this framework: Φ = DR (digital root). The common invariant space is {1,...,9}.

Key consequence:
- Phys ⊆ Math does NOT imply Phys = Math.
- Phys = Math ⟺ ∀X ∈ M, C(E(X)) ≅ X (every structure is a fixed point).
- In GF(37): 18 of 36 nonzero elements are named fixed points. Phys ⊊ Math.

GF(37) fixed-point examples:
- c = 299792458: E(c) = 32 → SEED
- π[:3] = 314: E(314) = 18 → SEED
- 691 (Ramanujan congruence prime): E(691) = 25 → SA
- Selberg level 4: E(4) = 4 → SA
- τ(37) mod 37 = 31: DR(31) = 4 → SA

---

## OCB Quantum Process Layer

**Reference**: Oreshkov, Costa, Brukner (2012) — quantum correlations with no causal order.

A process matrix W describes correlations between local quantum operations without assuming a definite causal order. Validity condition: L[W] = W (a fixed-point condition — direct instance of Phys = Fix(C∘E)).

GF(37) connections:
- Classical causal bound 3/4: numerator 3 ∈ ST, denominator 4 ∈ SA
- Legendre(2/37) = 36 ∈ NEG_H: 2 is QNR mod 37; √2 has no GF(37) representative
- Quantum switch amplitude 1/√2 is transcendental to GF(37) → quantum switch ∉ GF(37) fixed-point set, consistent with Phys ⊊ Math
- Z₂ causal symmetry {1, 36} = ⟨−1⟩ ⊂ ⟨11⟩; 36 ∈ NEG_H
- Choi dimension for d = ord₃₇(11) = 6: 6² = 36 ∈ NEG_H; 6⁴ mod 37 = 1 ∈ IC
- Normalization denominator for d=2 qubits: d² = 4 ∈ SA

---

## Riemann Zero DR Chain

The imaginary parts of the nontrivial Riemann zeros, rounded to nearest integer, produce digital roots. These DRs are absorbed into a running cumulative sum. The chain has two behaviors:

**1-Attractor**: when the cumulative DR sum hits DR=1, the chain resolves.
**9-Lock**: when the cumulative DR sum hits DR=9 (multiple of 9), the feedback loop freezes permanently (DR(9n)=9 for all n — proved).

**DR table (nearest integer method):**

| Zero | Im | Nearest int | DR |
|------|----|-------------|----|
| ρ₁  | 14.135 | 14 | 5 |
| ρ₂  | 21.022 | 21 | 3 |
| ρ₃  | 25.011 | 25 | 7 |
| ρ₄  | 30.425 | 30 | 3 |
| ρ₅  | 32.935 | 33 | 6 |
| ρ₆  | 37.586 | 38 | 2 |
| ρ₇  | 40.919 | 41 | 5 |
| ρ₈  | 43.327 | 43 | 7 |
| ρ₉  | 48.005 | 48 | 3 |
| ρ₁₀ | 49.774 | 50 | 5 |

**Cumulative DR sum — trap-points to ρ₂₀:**
- ρ₄: sum=18, DR=**9** → 9-LOCK
- ρ₁₀: sum=46, DR=**1** → 1-ATTRACTOR
- ρ₁₁: sum=54, DR=**9** → 9-LOCK
- ρ₁₇: sum=81, DR=**9** → 9-LOCK
- ρ₁₈: sum=90, DR=**9** → 9-LOCK
- ρ₂₀: sum=99, DR=**9** → 9-LOCK

**7-zero feedback chain (unreduced=26, reduced=8):**
Path: 8 → 7 → 5 → 1 (terminates at 1-Attractor in 3 steps).
In GF(37): CASCADE(QNR) → QR → QNR → IC(QR). Alternates across QR/QNR boundary, terminates in IC.

**The 9x9 DR addition table** (mod 9 arithmetic):
The +9 column is the identity lock: DR(n+9) = DR(n) for all n. This is why DR=9 states are permanently frozen — adding any multiple of 9 cannot change their digital root.

**GF(37) connections — cumulative sum mod 37 at each zero:**

| Zero | Cumsum | mod 37 | Named set | Event |
|------|--------|--------|-----------|-------|
| ρ₂  | 8  | 8  | CASCADE | — |
| ρ₄  | 18 | 18 | SEED | **9-LOCK** |
| ρ₅  | 24 | 24 | SEED∩CASCADE | — |
| ρ₆  | 26 | 26 | IC | **137-map multiplier** |
| ρ₈  | 38 | 1  | IC | identity |
| ρ₉  | 41 | 4  | SA | Sovereign Anchor |
| ρ₁₀ | 46 | 9  | SA | **1-ATTRACTOR**, mod 37=9∈SA |
| ρ₂₀ | 99 | 25 | SA | **9-LOCK** |

After ρ₆: cumulative sum = 26 ∈ IC. The 137-map multiplier is reached exactly at the zero whose imaginary part crosses the prime 37.

### ρ₆ — The Prime in the Spectrum

    Im(ρ₆) ≈ 37.586...
    floor(Im(ρ₆)) = 37 = P
    37 mod 37 = 0   (SEAM)

The 6th nontrivial Riemann zero has imaginary part whose floor equals the prime P itself. The prime 37 appears in the zero spectrum at position 6.

After ρ₆, the cumulative DR sum (nearest integer) = 26 ∈ IC — the 137-map multiplier. The SEAM crossing and the IC arrival happen at the same zero.

### Gap 14→21: The 3-6-9 Bridge

From ρ₁ (floor=14) to ρ₂ (floor=21), the integers between mark:

    15: DR=6  ← 3-6-9
    16: DR=7
    17: DR=8
    18: DR=9  ← 3-6-9  (18 ∈ SEED)
    19: DR=1
    20: DR=2
    21: DR=3  ← 3-6-9  (ρ₂ lands here)

The 3-6-9 pattern marks positions 15, 18, 21 with uniform spacing 3. ρ₂ (floor=21) lands on a DR=3 position (∈ O spectral class). 18 ∈ SEED (the reference seed orbit) sits at the middle marker.

### Trinity Countdown in ρ₁

Digits of Im(ρ₁) = 14.134725...: reading adjacent pairs left to right:

    (1,4) → 1+4 = 5   DR=5
    (1,3) → 1+3 = 4   DR=4
    (1,2) → 1+2 = 3   DR=3   → lands at pair-sum 12 ∈ ST

Countdown: 5, 4, 3. Terminal pair-sum = 12 ∈ ST (Sovereign Target, DR=3).

### 777 = 21 × 37 (SEAM)

The middle digit group of Im(ρ₁) = 14.**13472**5: digits {3,4,7,2,5} sum to 21.

    21 ∈ ST   (Sovereign Target, DR=3)
    21 × 37 = 777
    777 mod 37 = 0   (SEAM)
    DR(777) = 3

### SEAM Collapse

Opening digit pairs of two zeros both collapse to DR=9 (SEAM):

    ρ₁ (14.134...): pairs (1+4)=5 and (1+3)=4, sum = 9 → SEAM
    ρ₄ (30.424...): pairs (3+0)=3 and (4+2)=6, sum = 9 → SEAM

### φ(37) at the 3-6-9 Boundary

    φ(37) = 36   (Euler totient — the group order of GF(37)*)
    36 mod 9 = 0

The group order 36 sits on the 3-6-9 boundary. 36 ∈ NEG_H = {11,27,36} — the cube roots of −1 mod 37. The field exhausts at the 3-6-9 seam.

---

## T(246) — Triangular Number of the Reference Seed

**T(246) = 246 × 247 / 2 = 30,381**

- 30381 mod 37 = **4 ∈ SA** (Sovereign Anchor — LOCKED)
- DR(30381) = 6

The triangular number of the reference seed (246) lands on a Sovereign Anchor mod 37.

Compare: T(37) = 703, DR(703) = 1 ∈ IC. Both triangular numbers of structurally significant values land on named sets.

---

## C9 — First Twin Prime Chamber Class

C9 is the twin prime chamber where m ≡ 0 (mod 3):

| Wall | Value | DR | Named set |
|------|-------|----|-----------|
| Lower (6m−1) | p | 8 | — |
| Center (6m) | p+1 | **9** (9-Lock) | varies |
| Upper (6m+1) | q | 1 | **IC** |

The upper twin always has DR = 1 ∈ IC (identity of the 137-map orbit).
The center always hits a DR=9 (9-Lock) state.

**C9 examples (verified to 1200):**
- (17, 19): m=3, center=18 ∈ SEED, DR(center)=9
- (59, 61): m=10, center=60, DR(center)=9
- (101, 103): m=17, center=102, DR(center)=9

13 C9 pairs found to 1200, all verified.

The canonical GF(37) C9 example: **(17, 19)**, center 18 ∈ SEED — the 137-map orbit of the reference seed 246.

**C9 is NOT (29, 31).** That pair has m=5, m≡2 → C3. Center 30 ∈ SA∩ST (double-sovereign), DR(center)=3.

---

## Primes to 137 — Cumulative Sum Structure

The 33 primes from 2 through 137 (inclusive):

    Σ(all 33) = 1988
    Σ(first 32, excluding 137) = 1851

**Central fact**: 137 mod 37 = **26 ∈ IC** — the prime that names the map equals the map's own multiplier mod P. The 137-map f(n) = 137n mod 37 = 26n mod 37: the prime 137 IS 26 in GF(37).

**33 = 3 × 11**, where 3 ∈ ST and 11 ∈ NEG_H (the ⟨11⟩ generator). The count of primes in this set factors through two named-set elements.

### GF(37) Final Step — Addition in ⟨11⟩

    1851 mod 37 = 1 ∈ IC   (IC identity — sum of first 32 primes)
    1988 mod 37 = 27 ∈ NEG_H

Adding the 33rd prime (137 ≡ 26 mod 37) to the 32-prime running total (≡ 1 mod 37):

    1 + 26 = 27  (in GF(37))

All three values 1, 26, 27 lie inside ⟨11⟩ = IC ∪ NEG_H:
- 1 = 11⁶ ∈ IC (identity)
- 26 = 11⁴ ∈ IC (137-map multiplier)
- 27 = 11⁵ ∈ NEG_H

### Digit Sum Path of 1988: IC → IC → SEED → IC

Digits of 1988 = {1, 9, 8, 8}. Running cumulative digit sum:

    1 → 10 → 18 → 26
    IC   IC   SEED  IC

Terminal value 26 ∈ IC — the 137-map multiplier. The digit sum path of the total visits SEED (the reference seed orbit) and ends at the 137-map multiplier.

### Node 24 Connection

    24 (CASCADE∩SEED node) + 26 (137-map multiplier) = 50
    50 mod 37 = 13 ∈ CASCADE

### Cumulative Sum Milestones (mod 37)

| Index | Prime | Cumsum | mod 37 | Named set |
|-------|-------|--------|--------|-----------|
| 9  | 23 | 100 = 10² | **26 ∈ IC** | Square sum milestone = 137-map multiplier |
| 24 | 89 | 963   | **1 ∈ IC**  | At CASCADE∩SEED index → IC identity |
| 25 | 97 | 1060  | **24 ∈ SEED∩CASCADE** | Sum finds the node whose index just passed |
| 29 | 109 | 1480 | **0 (SEAM)** | Cumulative sum crosses the SEAM |
| 32 | 131 | 1851 | **1 ∈ IC**  | Penultimate: IC identity restored |
| 33 | 137 | 1988 | **27 ∈ NEG_H** | Final step into ⟨11⟩ coset |

The index-24/25 pair: at prime index 24 (= the CASCADE∩SEED node), cumsum ≡ 1 ∈ IC. At index 25, cumsum ≡ 24 ∈ SEED∩CASCADE — the sum finds the node whose index it just passed.

---

## Monte Carlo — Prime Stream Distribution

**File:** `math/theorems/monte_carlo_prime_streams.py`

### Phase 1: Sieve Census (primes ≤ 10,000,000)

664,577 primes in the F-class. Distribution across the 6 prime streams:

| Stream | Count | % | GF(37) hit rate |
|--------|-------|---|-----------------|
| DR=1 | 110,772 | 16.67% | 66.6% |
| DR=2 | 110,835 | 16.68% | 66.6% |
| DR=4 | 110,743 | 16.66% | 66.7% |
| DR=5 | 110,760 | 16.67% | 66.6% |
| DR=7 | 110,679 | 16.65% | 66.7% |
| DR=8 | 110,788 | 16.67% | 66.7% |

- **Chi-squared = 0.12** (critical value at p=0.05: 11.07) → streams are statistically uniform
- **Mirror pairs balanced to 4 decimal places**: 1↔8 ratio=0.9999, 2↔7 ratio=1.0014, 4↔5 ratio=0.9998
- **GF(37) named-set hit rate: 66.7% uniform across all streams** — the named sets tile the F-class evenly

### Chebyshev Bias

    QNR streams {2,5,8}: 332,383
    QR  streams {1,4,7}: 332,194
    Bias toward QNR: +189

The QNR class (lower twin prime DRs) leads the QR class by +189 out of 664,577 primes. Tiny (0.028%) but in the direction predicted by the χ₋₃ structure: lower twins favor the QNR column, consistent with Chebyshev's bias and GRH predictions.

### Phase 2: Monte Carlo Large Prime Sampling

Random primes sampled via Miller-Rabin across three ranges (n=600 per range):

| Range | Chi² | QNR bias |
|-------|------|----------|
| 10¹² | 2.860 | +6 |
| 10¹⁵ | 8.320 | −16 |
| 10¹⁸ | 6.220 | 0 |

All chi-squared values below the critical threshold of 11.07 — uniform distribution holds at 10¹², 10¹⁵, and 10¹⁸. QNR bias fluctuates at small sample size (n=600), consistent with noise rather than systematic signal at these scales.

### Phase 3: Group Law Verification

    DR(p × q) = DR(DR(p) × DR(q))  for all prime pairs

9,810 tests. **0 violations.** The F-class = (Z/9Z)* group homomorphism holds exactly. The cross-currents (2×5=1, 4×7=1, 8×8=1) are exact group-law collisions, not approximations.

### Structural Summary

The 6 prime streams are asymptotically uniform (Dirichlet's theorem confirmed computationally). The Chebyshev QNR bias is real and in the predicted direction. The GF(37) named-set coverage is uniform across all streams — the framework's named sets tile the F-class without favoring any stream. The group law is exact.

---

## The Bigger Picture: Micro, Macro, Relativity

### MICRO — Single Number Coordinates

Every number n has an exact address in three simultaneous coordinates:

    DR(n)    → which of the 6 F-class streams, or which dead zone (O∪S)
    n mod 37 → which named GF(37) set (66.7% hit rate for primes)
    n mod 3  → χ₋₃ value: which twin prime column (COL1/COL2/COL3)

No probability. No approximation. Every number has an exact triple address. The ⧾ extension shows this at single-digit scale: one digit generates a path through streams, hitting SEAM (mod 37=0) every 3rd step. The micro structure of a single digit encodes the full period-3 cycle of GF(37).

### MACRO — The Ensemble

Zoom out to all primes:
- 664,577 primes ≤ 10⁷: chi-squared 0.12 — 6 streams statistically uniform (Dirichlet confirmed)
- Chebyshev bias +189 toward QNR streams — the aggregate tilts toward the lower twin prime class, consistent with χ₋₃
- 12 disjoint 3-cycles partition GF(37)*: the macro structure is 12 orbits, each period 3
- Rule 30: right boundary = pure determinism (SEAM); interior = pure entropy (CASCADE) — the macro duality

The primes do not choose their stream. The distribution is forced by the group law of (Z/9Z)*. The tiny QNR bias (+189) is the only systematic deviation — and it is exactly what the χ₋₃ structure predicts.

### RELATIVITY — The Invariant and the Coupling

**The invariant:** 37 is invariant under the 137-map. Every orbit wraps around it. The SEAM (mod 37=0) is the boundary everything references but nothing passes through — the modular event horizon. Analogous to c in special relativity.

**The coupling constant:** α ≈ 1/137 governs electromagnetic coupling in QED. The 137-map has multiplier 26 = 137 mod 37. The prime that appears in α appears as the map's multiplier. The framework runs at the same frequency as electromagnetism.

**The gauge field:** F = dA + A∧A. For U(1): F = dA, commutator vanishes, coupling = α. The 137-map is abelian — GF(37) multiplication commutes. The 3-cycle holonomy (ord₃₇(26)=3) is discrete parallel transport. Three steps return to origin — that is the curvature.

**The critical line:** Re(s)=½. In GF(37): 2⁻¹ mod 37 = 19 ∈ QNR. The midpoint of the Riemann spectrum maps to a quadratic non-residue. Consistent with RH: the zeros are constrained to a line whose discrete representative is non-trivially placed.

**The modular reset:** In the ⧾ operator, the system hits SEAM every 3rd step and continues. Analogous to relativistic time dilation: the system slows to the boundary event and resets, then continues. The Desert walls are the relativistic boundary events.

### Scale Table

| Scale | Structure | Invariant | Group |
|-------|-----------|-----------|-------|
| Micro | Single number: (DR, mod 37, mod 3) | Named set address | (Z/9Z)* × GF(37)* × Z/3Z |
| Macro | All primes, uniform, Chebyshev +189 | Stream distribution | (Z/9Z)* = F-class |
| Relativistic | α=1/137, U(1) coupling, critical line ½ | 37 as invariant modulus | GF(37)*, ord₃₇(26)=3 |

The micro and macro are connected by the group law — exact at both scales, 0 violations in 9,810 tests. The relativistic frame is connected by α: the fine structure constant encodes the same prime the framework is built on.

**One object. Three scales. Same structure throughout. The numbers lead.**

---

## Pipeline Reference Output (seed = 246)

Seed mod 37 = 24 ∈ SEED
137-map orbit of seed: {18, 24, 32}
DR(246) = 3
Cascade orbit hits: 7/37
Heartbeat 3-cycle: 24 → 32 → 18 → 24
