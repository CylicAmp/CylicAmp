# Literature Map

What each core construction in this repository corresponds to in the
classical literature. Written because an independent derivation that lands
on a known theorem is a statement about the reasoning, and the repository
had no record of which theorems it was landing on.

Each row is stated as: the construction here, the classical result it is,
and what is checkably true about the correspondence. Nothing below is a
claim of novelty; several rows are the opposite.

---

## 1. The 12 orbits under f(n) = 26n mod 37

**Classical name:** coset decomposition of a cyclic group by a subgroup —
Lagrange's theorem (1771).

μ₃ = {1, 10, 26} is the order-3 subgroup of F₃₇ˣ (it is the kernel of the
cubing map, and the group of cube roots of unity). The "12 orbits" are
exactly the 12 left cosets of μ₃ in F₃₇ˣ.

Verified: 12 cosets, each of size 3, index [F₃₇ˣ : μ₃] = 36/3 = 12.

The orbit partition is therefore forced the moment 3 | (p−1). It is a
theorem, and it is Lagrange's. Choosing 137 as the multiplier does not
produce it; 137 ≡ 26 and 26 happens to generate μ₃.

---

## 2. Cyclotomic prime families — p | Φ_d(a) ⟹ ord_p(a) = d

**Classical name:** the order/cyclotomic correspondence, and **Zsigmondy's
theorem** (1892) for the existence half.

The statement used throughout this repo — that every prime factor of Φ_d(a)
has multiplicative order exactly d unless p | d — is standard. Zsigmondy
supplies the harder direction: a^n − b^n has a *primitive* prime divisor
(one of order exactly n) for every n, with a short finite list of exceptions.

Verified for a = 137:

| d | Φ_d(137) | primes | primitive (ord = d) |
|---|---|---|---|
| 1 | 136 | 2, 17 | 2, 17 |
| 2 | 138 | 2, 3, 23 | 3, 23 |
| 3 | 18907 | 7, 37, 73 | 7, 37, 73 |
| 4 | 18770 | 2, 5, 1877 | 5, 1877 |
| 6 | 18633 | 3, 6211 | 6211 |
| 12 | 352256593 | 13, 2473, 10957 | 13, 2473, 10957 |

Every row has a primitive divisor, as Zsigmondy guarantees. The d = 3 row
is the one this framework is built on, and 37 appears inside it.

**T292's exhaustiveness result** — that {7, 37, 73} is the complete factor
set of Φ₃(137) — is a finite computation, not covered by Zsigmondy, and
stands on its own.

---

## 3. The QR / NQR split, and 19 as the critical-line element

**Classical name:** Euler's criterion (1748) and the Legendre symbol; the
quadratic residues are the image of the squaring map, of index 2.

Verified: |QR| = 18 = (p−1)/2. ⟨4⟩ = QR as sets, since 4 = 2² and 2 is a
primitive root.

19 = 2⁻¹ mod 37 is the modular inverse of 2, and 1 − 19 ≡ 19, so it is the
fixed point of s ↦ 1 − s over F₃₇. That is a genuine structural analogue of
Re(s) = ½ being fixed by the functional equation's reflection — but it is an
analogy between a finite field and the complex plane, not a theorem relating
them.

---

## 4. p = n² + 1 at n = 2, 4, 6 giving 5, 17, 37

**Classical name:** complex multiplication; the unit groups of ℤ, ℤ[i], ℤ[ω],
of orders 2, 4, 6 — a classical fact going back to Gauss (ℤ[i], 1832) and
Eisenstein (ℤ[ω], 1844).

The three rings of integers with extra units are exactly ℚ, ℚ(i), ℚ(√−3), and
their unit counts are 2, 4, 6. The condition n·gcd(n, p−1) = p−1 with n | p−1
collapses to p = n² + 1, and those three n give three primes.

37 = 6² + 1 is the Eisenstein case. This is why 37 carries the structure it
does, and it is a known reason, not a coincidence.

---

## 5. Digital roots

**Classical name:** casting out nines — reduction mod 9, known since at least
the 12th century (al-Khwarizmi's transmitters), formalised by congruence.

DR(n) = 1 + (n−1) mod 9 is n mod 9 with 0 mapped to 9. Every digital-root
identity in this repo is a statement about ℤ/9ℤ, and the base-10 digit sum is
a homomorphism onto it because 10 ≡ 1 (mod 9).

---

## 6. Zeta-zero floors mod 37

**Classical name:** equidistribution — Weyl's criterion (1916); the
underlying spacing statistics are Montgomery's pair correlation (1973) and
the GUE conjecture.

floor(γ_n) mod 37 landing uniformly across the 12 orbits is what
equidistribution of γ_n predicts. T223 reports this correctly and says so.

The labelling is exact and verifiable; the distribution carries no signal
beyond what equidistribution already implies, which T223 states.

---

## 7. Rule 30 center column

**Classical name:** Wolfram's Rule 30 problems (1985; prize announced 2019).
Problem 1 (non-periodicity), Problem 2 (equal density), Problem 3 (block
universality) are all open.

T235–T238 compute GF(37) structure alongside these and state plainly that
the problems are open. The implication chain recorded there — block
universality ⟹ non-periodicity — is correct and elementary.

---

## What is not in the literature

The cross-orbit transversals defined here — SA = {4,9,25,30}, ST = {3,12,21,30},
the cascade base {8,13,24} generating exactly 37 elements — are constructions
specific to this repository. They are definitions plus verified consequences,
not rediscoveries. Whether they are useful is a separate question from
whether they are new; they are new.

T292's exhaustiveness result on Φ₃(137) is likewise a finite fact belonging
to this work.

---

## How to read this map

A row that names a classical theorem is not a demotion. Arriving at
Lagrange's coset decomposition from digit patterns and modular arithmetic,
without being handed it, means the reasoning was sound enough to reproduce a
theorem that took a century to state properly the first time.

What the map buys is direction: the rows with classical names are finished
territory, and the effort is better spent where the map is blank.
