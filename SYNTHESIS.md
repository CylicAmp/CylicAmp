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

## The (0.007, 0.008) Pair: Digit Algebra and Scientific Notation

Theorems 120–121 (`math/theorems/theorem_120_digit_algebra_007_008.py`, `theorem_121_scientific_notation_007_008.py`).

**Scientific notation decomposition** (Theorem 121):

```
0.007 = 7 × 10^{-3}    mantissa m1 = 7,  shift s = 3
0.008 = 8 × 10^{-3}    mantissa m2 = 8,  shift s = 3
```

The six arithmetic combinations of each mantissa with the shared shift count each land in a distinct named GF(37) class:

| Expression | Value | Class |
|---|---|---|
| m1 + s | 10 | IC = {1, 10, 26} |
| m1 − s | 4 | SA = {4, 9, 25, 30} |
| m1 × s | 21 | ST = {3, 12, 21} |
| m2 + s | 11 | ORBIT_11 = {11, 27, 36} |
| m2 − s | 5 | PR₃₇ (primitive root) |
| m2 × s | 24 | CB = {8, 13, 24} |

The shift count s = 3 has orbit (3, 4, 30) under the 137-map — the only orbit that spans both a Sovereign Target (3) and Sovereign Anchors (4, 30).

**Digit algebra** (Theorem 120): operating on the significant digits directly:

```
Sum:        7 + 8 = 15,   DR(15) = 6
Difference: 8 − 7 = 1
Synthesis:  6 + 1 = 7     ← closes back to m1
```

The closure `DR(m1+m2) + (m2−m1) = m1` is specific to the pair (7, 8); it fails for (6,8), (7,9), (8,9), (3,5).

**Bridge between the two theorems:** the negated exponent −3 encodes both results simultaneously:

- (−3) mod 9 = **6** = DR(7+8)  — the exponent residue equals the digital root of the mantissa sum
- (−3) mod 37 = **34** ∈ orbit(7) = (7, 34, 33) = D7  — the negated shift lies inside the 137-orbit of m1

The digit algebra (Theorem 120) and the scientific notation decomposition (Theorem 121) are the same object seen from two angles: one operates on the mantissa pair, the other on mantissa × shift. Their connection is encoded in the shared exponent −3.

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
- **m1×s = 24 ∈ CB, m2−s = 5 ∈ PR₃₇** → the (7,8) mantissa pair with shift s=3 reaches both the cascade base and the primitive root class in one arithmetic step
- **(−3) mod 9 = DR(7+8) = 6, (−3) mod 37 = 34 ∈ orbit(7)** → the shared exponent of 0.007 and 0.008 encodes their digit algebra residue and their D7 orbit simultaneously

The framework is not a collection of separate observations. It is one algebraic object — the prime field GF(37), its multiplicative structure, and the specific map f(n) = 137n mod 37 — seen from multiple angles simultaneously.
