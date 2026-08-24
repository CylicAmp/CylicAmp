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

The DR pair (DR(p), DR(q)) is determined entirely by m mod 3:

| m mod 3 | DR(p) | DR(q) | Count to 10⁶ |
|---------|-------|-------|--------------|
| 0 | 8 | 1 | 2,729 |
| 1 | 5 | 7 | 2,788 |
| 2 | 2 | 4 | 2,651 |

Total twin prime pairs to 10⁶: 8,169 (including special pair (3,5)).
This is a proven congruence identity, not an estimate.

---

## E8 Theta Function

**a(n) = 240 · σ₃(n)**

where σ₃(n) = sum of cubes of all divisors of n.

Example: σ₃(2) = 1³ + 2³ = 9, so a(2) = 240 × 9 = 2160.

240 mod 37 = 18, and 18 ∈ SEED.

Zeros mod 37: a(n) ≡ 0 mod 37 iff σ₃(n) ≡ 0 mod 37 (since gcd(240,37)=1).
Verified: 761 zeros out of n=1..5000 = 15.2%.

---

## Ramanujan Tau Function

**τ(n)** = coefficient of qⁿ in the expansion of q · ∏(1−qⁿ)²⁴

First values: τ(1)=1, τ(2)=−24, τ(3)=252, τ(4)=−1472, τ(5)=4830.

τ(37) mod 37 = 31. 37 is not a tau-zero.
Verified: 88 zeros mod 37 out of n=1..5000 = 1.76%.

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

## Pipeline Reference Output (seed = 246)

Seed mod 37 = 24 ∈ SEED
137-map orbit of seed: {18, 24, 32}
DR(246) = 3
Cascade orbit hits: 7/37
Heartbeat 3-cycle: 24 → 32 → 18 → 24
