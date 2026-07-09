# CylicAmp Framework: Complete Mathematical Synthesis

Everything in this framework connects through one prime: **37**.

---

## The Core: Z/37Z and the 137-Map

The central map is `f(n) = (137 × n) mod 37`. Since 137 mod 37 = 26, this is multiplication by 26 in the field GF(37).

The multiplier 26 has **multiplicative order 3** in (Z/37Z)*:
- 26¹ mod 37 = 26
- 26² mod 37 = 10
- 26³ mod 37 = 1

This means every non-zero element of Z/37Z returns to itself in exactly 3 steps under the 137-map. The 36 non-zero residues decompose into **12 disjoint 3-cycles**.

---

## The Orbit Structure

The full multiplicative group (Z/37Z)* has order φ(37) = 36 = 4 × 9.

**2 is a primitive root mod 37** with order 36 — verified by the primitive root test theorem (`math/theorems/primitive_root_test.py`): g is a primitive root mod p iff g^((p-1)/q) ≢ 1 (mod p) for every prime q dividing p-1. For p=37, p-1=36, prime factors {2,3}: checking 2^18 ≡ 36 ≠ 1 and 2^12 ≡ 26 ≠ 1 confirms ord₃₇(2) = 36.

The ×2 mod 37 orbit (`math/theorems/abcabc_mod37_orbit.py`) cycles through all 36 non-zero residues. This is the **algebraic certificate** that the orbit is complete.

The 12 three-cycles under the 137-map split into two groups of 6:
- Group A: cycle sums ≡ 37 (DR = 1)
- Group B: cycle sums ≡ 74 (DR = 2)

This is provable: within any 3-cycle {n, 26n, 10n} mod 37, the sum is n(1+26+10) = 37n ≡ 0 mod 37, so the sum is always a multiple of 37.

---

## Quadratic Residues: The Sovereign QR Closure

The quadratic residues mod 37 form a subgroup of index 2 with 18 elements. Since 26 is itself a QR (10² ≡ 26 mod 37), the 137-map **preserves QR membership**: every orbit lives entirely within QR or entirely within non-QR.

The **sovereign anchors** {4, 9, 25, 30} are all QR. Their images under f:
- 4 → 30
- 9 → 12
- 25 → 21
- 30 → 3

Node **30** is simultaneously an anchor and a target — the self-referential fixed structure.

The pivot prime 5 is explicitly **non-QR** mod 37 (Legendre(5|37) = −1), which means the golden ratio φ (satisfying x²−x−1=0 with discriminant 5) does not exist in GF(37). It requires the degree-2 extension GF(37²) with 1369 elements.

---

## The {8, 13, 24} Cascade

Starting from base set B = {8, 13, 24}, the cascade construction (`math/theorems/cascade_8_13_24.py`) generates all k-element subset sums iteratively:

- S₁ = {8, 13, 21, 24, 32, 37} (all 1- and 2-element subset sums)
- Continuing through all k-subset sums...
- Total elements generated: **exactly 37**
- Terminal value: 135 = 8+13+24+37+53 (ratio 135/24 = 45/8)
- Elements ≡ 0 mod 37: {37, 74, 111}
- 135 mod 37 = 24 (the cascade feeds back to its own generator)

The cascade count of 37 is not coincidental — it is the same prime that governs the field. The base {8, 13, 24} has digital roots {8, 4, 6}; their sum 45 has DR = 9, the identity of the DR algebra.

---

## The ABCABC ≡ 2·ABC (mod 37) Theorem

Any 3-digit number ABC forms ABCABC = ABC × 1001. Since 1001 = 27 × 37 + 2, we have:

**ABCABC ≡ 2 · ABC (mod 37)**

This means every 6-digit repunit of a 3-digit block lands in the orbit of 2 × the original value. Since 2 is a primitive root of 37, this connects every 3-digit number to the full 36-element orbit (`math/theorems/abcabc_mod37_orbit.py`).

The inverse operation: given a residue r in the orbit, recover ABC via `ABC = r × 19 mod 37` (since 2⁻¹ ≡ 19 mod 37).

---

## The Digital Root Algebra

The doubling map x → DR(2x) on {1,...,9} produces:
- **6-cycle**: 1 → 2 → 4 → 8 → 7 → 5 → 1
- **Fixed point**: 9

The number 8 is the bridge between 4 and 7 in this cycle. The values 8, 13, 24 in the cascade correspond to DR values 8, 4, 6 — three distinct positions in the DR structure.

The DR algebra operates mod 9, and 9 divides φ(37) = 36, making DR and field arithmetic compatible throughout.

---

## The Lucas Sequence Connection

The ABBC manifold chain starting at (4,7) is the Lucas sequence L(3)...L(10):
**4, 7, 11, 18, 29, 47, 76, 123**

Key anchors:
- L(3) = 4: sovereign anchor node
- L(5) = 11: twin prime, DR = 2
- L(6) = 18: half of 36 = φ(37)
- L(7) = 29, L(8) = 47: both prime with DR = 2

The DR period of Lucas numbers mod 9 is **24** — the same 24 that appears in the cascade base {8, 13, 24}.

---

## The 11 ↔ 37 Arithmetic Encoding

All verified (`math/theorems/eleven_thirtyseven_ops.py`):

| Operation | Value | Meaning |
|---|---|---|
| 11 − 37 = −26 → DR(26) | 8 | cascade base element |
| 11 + 37 = 48 → DR(DS(48)) | 3 | \|B\| = 3 base elements |
| 11 × 37 = 407 → DR(DS(407)) | 2 | orbit generator |
| 297 mod 37 | 1 | orbit identity (1/37 = 0.027027...) |
| 37 ÷ 11 = 3.363636... | repeating "36" | φ(37) = 36 |
| 3689 = 7 × 17 × 31 | all in ×2 orbit | 0.11 − 37 = −36.89 |

---

## The EML Operator

`eml(x, y) = exp(x) − ln(y)` (`math/theorems/eml_operator.py`)

Key identities:
- eml(x, 1) = exp(x)
- eml(1, 1) = e
- Non-commutative: eml(x,y) ≠ eml(y,x)
- Domain: y > 0 (branch cut at y ≤ 0)

eml naturally generates exp, ln, and multiplication. Addition requires external input — defining the boundary of what the operator can produce from within itself.

---

## The Primitive Root Test Theorem

**Theorem** (`math/theorems/primitive_root_test.py`): g is a primitive root mod p if and only if g^((p−1)/q) ≢ 1 (mod p) for every prime q dividing p−1.

For p = 37: only 2 checks needed (prime factors of 36 are {2, 3}) instead of 8 (all proper divisors of 36). This is the certificate of orbit completeness.

All 12 primitive roots mod 37: {2, 5, 13, 15, 17, 18, 19, 20, 22, 24, 32, 35}

**13 is a primitive root mod 37** — the cascade mediator (in B = {8,13,24}) and a generator of the full orbit are in the same algebraic class.

---

## The Divisor String Palindromes

Proper divisor string of n = concatenation of all proper divisors of n in sorted order (`math/theorems/divisor_strings.py`).

In [11, 99]: exactly **22 of 89 integers** have palindromic proper divisor strings:
- 21 are primes (proper divisors = {1}, string = "1")
- 1 composite: n = 93 = 3 × 31, string = "1331" = 11³

37 is one of the 22 palindromes (prime).
93 mod 37 = 19 ∈ non-QR₃₇.

---

## The Goldilocks Prime

p = 2⁶⁴ − 2³² + 1 (`math/theorems/goldilocks_prime.py`)

p − 1 = 2³² × 3 × 5 × 17 × 257 × 65537 = 2³² × F₁ × F₂ × F₃ × F₄

The Fermat factors {F₁,...,F₄} enable NTT up to length 2³². Only 6 primality checks needed for primitive root verification. Smallest primitive root: 7.

The primitive root test theorem reduces verification from exponential to logarithmic in the number of prime factors.

---

## The Lattice Transform Engine

Encodes D4 symmetry (4 rotations × 2 mirror states) combined with cyclic shifts (h horizontal, v vertical) into a single integer token ID (`pipeline/lattice_transform_engine.py`).

Encoding: `ID = r × 2N² + m × N² + h × N + v`

For N=4: max ID = 127. For N=8: max ID = 511.

The canonical base sequence [1,2,3,4] transforms as:
1. Cyclic right-shift by r
2. Cyclic right-shift by h (mod 4)
3. Reverse if m = 1
4. Tile to width N

All 7 spec cases verified.

---

## The Unifying Structure

Every result connects back through the prime 37:

- **37 is prime** → (Z/37Z)* is cyclic of order 36
- **36 = 4 × 9** → compatible with digital root algebra (mod 9) and D4 symmetry (order 4)
- **ord₃₇(26) = 3** → 12 three-cycles, the heartbeat of the 137-map
- **ord₃₇(2) = 36** → 2 is primitive root, the ×2 orbit is complete
- **|QR₃₇| = 18** → sovereign closure, QR subgroup at index 2
- **{8,13,24} cascade → 37 elements** → the count equals the modulus
- **ABCABC ≡ 2·ABC (mod 37)** → the orbit generator appears in every 6-digit repunit
- **13 ∈ primitive roots mod 37** → cascade mediator and orbit generator are algebraically equivalent
- **DR period of Lucas mod 9 = 24** → connects to cascade base {8,13,24}
- **1001 = 27×37 + 2** → the bridge between decimal representation and the orbit

The framework is not a collection of separate observations. It is one algebraic object — the prime field GF(37), its multiplicative structure, and the specific map f(n) = 137n mod 37 — seen from multiple angles simultaneously.
