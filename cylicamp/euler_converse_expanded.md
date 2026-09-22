# Expanded Proof of Euler's Converse

© 2026 Michael Warren Song. All Rights Reserved.

---

## Theorem (Euler's Converse)

If N is an even perfect number, then there exists a prime p such that

```
N = 2^(p−1) · (2^p − 1)
```

and 2^p − 1 is also prime (a Mersenne prime).

---

## Proof — Step by Step

### Step 1 — Canonical Form

Since N is even and perfect (σ(N) = 2N), write:

```
N = 2^a · m,    a ≥ 1,    m odd.
```

### Step 2 — Apply Multiplicativity of σ

Because 2^a and m are coprime:

```
σ(N) = σ(2^a) · σ(m)
```

The geometric series gives:

```
σ(2^a) = 1 + 2 + … + 2^a = 2^(a+1) − 1
```

Since N is perfect, σ(N) = 2N = 2^(a+1) · m. Therefore:

```
(2^(a+1) − 1) · σ(m) = 2^(a+1) · m
```

Rearranging:

```
σ(m) = 2^(a+1) · m / (2^(a+1) − 1)
```

---

### Step 3 — Divisibility Constraint

The left side is an integer, so (2^(a+1) − 1) divides 2^(a+1) · m.

Since m is odd: gcd(2^(a+1) − 1, 2^(a+1)) = 1
(any common prime divisor would divide both an odd number and a power of 2 —
impossible).

Therefore **(2^(a+1) − 1) must divide m**.

---

### Step 4 — The Quotient Forces a Specific Form

Let d = 2^(a+1) − 1. Since d divides m, write m = d · k for some positive
integer k. Substituting back:

```
σ(m) = 2^(a+1) · k
```

But we also know σ(m) ≥ m + 1 = dk + 1 for any m > 1 (since 1 and m are
always divisors). So:

```
2^(a+1) · k ≥ dk + 1
k(2^(a+1) − d) ≥ 1
k · 1 ≥ 1       (since 2^(a+1) − d = 2^(a+1) − (2^(a+1) − 1) = 1)
```

This holds for all k ≥ 1. Equality σ(m) = m + k holds iff the **only**
divisors of m are 1 and m itself — i.e. **m is prime** — and k = 1.

Therefore **k = 1** and **m = 2^(a+1) − 1** is prime.

---

### Step 5 — Verification When m is Prime

Set m = q prime. Then σ(m) = 1 + q. The equation becomes:

```
1 + q = 2^(a+1) · q / (2^(a+1) − 1)
```

Cross-multiplying:

```
(1 + q)(2^(a+1) − 1) = 2^(a+1) · q
2^(a+1) − 1 + q · 2^(a+1) − q = 2^(a+1) · q
2^(a+1) − 1 − q = 0
q = 2^(a+1) − 1
```

So **m = 2^(a+1) − 1** and it must be prime. Set **p = a + 1**.

For 2^p − 1 to be prime, p itself must be prime (standard: if p = rs with
r, s > 1, then 2^r − 1 divides 2^p − 1, making it composite).

---

### Step 6 — Ruling Out All Other Cases

**Case m = 1:**
N = 2^a, σ(2^a) = 2^(a+1) − 1 ≠ 2^(a+1) for any a ≥ 1. Not perfect.

**Case m composite:**
If m has distinct prime factors q₁, q₂ then:
```
σ(m) ≥ 1 + q₁ + q₂ + m > m + 1
```
This forces σ(m) > 2^(a+1) · k, contradicting the equality. No composite m
can satisfy the equation.

Therefore the only possibility is m = 2^(a+1) − 1 prime, giving:

```
N = 2^(p−1) · (2^p − 1)
```

with p prime and 2^p − 1 prime. **QED**

---

## Key Insight

The proof turns on a single strict inequality: for composite m, σ(m) is always
too large. The divisibility chain:

```
(2^(a+1) − 1) | m  →  m = (2^(a+1) − 1) · k  →  k = 1  →  m prime
```

is forced by the arithmetic of σ combined with the coprimality of m and 2^a.

---

## Why p Must Be Prime

If p = r · s (r, s > 1), then:

```
2^r − 1  divides  2^(rs) − 1 = 2^p − 1
```

since (x − 1) | (x^s − 1) for x = 2^r. So 2^p − 1 would be composite.
Contrapositive: 2^p − 1 prime ⟹ p prime.

---

## Connection to Lucas-Lehmer

This theorem is the bridge between perfect numbers and the Lucas-Lehmer test:

```
New even perfect number  ←→  New Mersenne prime  ←→  s_{p−2} ≡ 0 (mod M_p)
```

The algebraic proof in `lucas_lehmer_verify.py` (α = 2+√2 in Z[√2]/M)
provides the mechanism by which the sequence detects exactly which M_p are
prime — and therefore which N are perfect.

---

## Summary of Logic Chain

```
N even + perfect
    ↓
N = 2^a · m,  m odd
    ↓
σ multiplicative → (2^(a+1)−1)·σ(m) = 2^(a+1)·m
    ↓
(2^(a+1)−1) | m  →  m = (2^(a+1)−1)·k
    ↓
σ(m) = 2^(a+1)·k  and  σ(m) = m+k  →  k = 1
    ↓
m = 2^(a+1)−1 is prime  (p = a+1 prime)
    ↓
N = 2^(p−1)·(2^p−1),  Mersenne prime
```
