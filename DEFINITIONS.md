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

| m mod 3 | DR(p) | DR(q) | Count to 10⁶ |
|---------|-------|-------|--------------|
| 0 | 8 | 1 | 2,729 |
| 1 | 5 | 7 | 2,788 |
| 2 | 2 | 4 | 2,651 |

DR(p) ∈ {2,5,8}: all QNR mod 37. DR(q) ∈ {1,4,7}: all QR mod 37.

Total twin prime pairs to 10⁶: 8,169 (including special pair (3,5)).
These are proven congruence identities, not estimates.

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

**GF(37) connections of the 7-zero chain:**
- After zero 6: cumulative sum = 26 ∈ IC (the 137-map multiplier)
- After zero 9: cumulative sum = 41, mod 37 = 4 ∈ SA
- ρ₄ floor=30: double-sovereign SA∩ST
- ρ₅ floor=32: SEED (pipeline reference orbit)
- ρ₆ floor=37: SEAM

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

## Pipeline Reference Output (seed = 246)

Seed mod 37 = 24 ∈ SEED
137-map orbit of seed: {18, 24, 32}
DR(246) = 3
Cascade orbit hits: 7/37
Heartbeat 3-cycle: 24 → 32 → 18 → 24
