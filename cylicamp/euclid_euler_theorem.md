# Euclid–Euler Theorem — Detailed Proof

© 2026 Michael Warren Song. All Rights Reserved.

---

## Theorem

A positive integer N is **even and perfect** if and only if

```
N = 2^(p−1) · (2^p − 1)
```

for some prime p such that 2^p − 1 is also prime (a **Mersenne prime**).

---

## Part 1 — Euclid's Direction

**Claim:** If p is prime and M_p = 2^p − 1 is prime, then N = 2^(p−1) · M_p is perfect.

**Proof.**

Let σ be the sum-of-divisors function. Since N is a product of two coprime
factors (2^(p−1) and the odd prime M_p), σ is multiplicative:

```
σ(N) = σ(2^(p−1)) · σ(M_p)
```

The geometric series gives:

```
σ(2^(p−1)) = 1 + 2 + 2² + … + 2^(p−1) = 2^p − 1
```

Since M_p is prime:

```
σ(M_p) = 1 + M_p
```

Therefore:

```
σ(N) = (2^p − 1)(1 + M_p)
      = (2^p − 1)(1 + 2^p − 1)
      = (2^p − 1) · 2^p
      = 2 · 2^(p−1) · (2^p − 1)
      = 2N
```

Since σ(N) = 2N, N is perfect by definition. **QED (Euclid)**

---

## Part 2 — Euler's Converse

**Claim:** If N is even and perfect, then N = 2^(p−1)(2^p − 1) for some prime p
with M_p = 2^p − 1 prime.

**Proof.**

Since N is even and perfect, write N = 2^a · m where m is odd and a ≥ 1.

Since N is perfect, σ(N) = 2N. Since 2^a and m are coprime:

```
σ(N) = σ(2^a) · σ(m) = 2N = 2^(a+1) · m
```

We know:

```
σ(2^a) = 2^(a+1) − 1
```

Thus:

```
(2^(a+1) − 1) · σ(m) = 2^(a+1) · m
```

Solving for σ(m):

```
σ(m) = 2^(a+1) · m / (2^(a+1) − 1)
```

**Step 1 — The divisibility constraint.**

The right-hand side must be an integer, so (2^(a+1) − 1) divides 2^(a+1) · m.
But 2^(a+1) − 1 is odd, and m is odd, so gcd(2^(a+1) − 1, 2^(a+1)) = 1.
Therefore 2^(a+1) − 1 must divide m.

Write m = (2^(a+1) − 1) · k for some positive integer k. Substituting:

```
σ(m) = 2^(a+1) · k
```

**Step 2 — m must be prime.**

We have σ(m) = m + (something) ≥ m + 1 for any m > 1 (since 1 and m are both
divisors). If m is composite, σ(m) ≥ m + d + 1 where d is a non-trivial divisor.

From m = (2^(a+1) − 1) · k and σ(m) = 2^(a+1) · k:

```
σ(m) = 2^(a+1) · k = m + k
```

This means the sum of all divisors of m equals m + k. But the divisors of m
include at least 1, k, m (if k > 1 and k < m). For σ(m) = m + k to hold with
no other divisors, we need k = 1. Hence:

```
m = 2^(a+1) − 1       (a Mersenne number)
σ(m) = m + 1          (exactly two divisors: 1 and m)
```

σ(m) = m + 1 means m is **prime**.

**Step 3 — p must be prime.**

Set p = a + 1. Then M_p = 2^p − 1 = m is prime.

For M_p = 2^p − 1 to be prime, p itself must be prime (standard result: if p is
composite, 2^p − 1 is composite).

Therefore:

```
N = 2^(p−1) · (2^p − 1)
```

with p prime and 2^p − 1 prime. **QED (Euler)**

---

## Conclusion

Together, Euclid's construction and Euler's classification give the **complete
characterization of all even perfect numbers**.

```
Even perfect numbers ←→ Mersenne primes
```

Each Mersenne prime 2^p − 1 yields exactly one even perfect number:

| p  | M_p = 2^p − 1 | N = 2^(p−1) · M_p     |
|----|----------------|------------------------|
| 2  | 3              | 6                      |
| 3  | 7              | 28                     |
| 5  | 31             | 496                    |
| 7  | 127            | 8128                   |
| 13 | 8191           | 33550336               |
| 17 | 131071         | 8589869056             |
| 19 | 524287         | 137438691328           |

**No odd perfect numbers are known.** None can exist below extremely large
bounds (currently > 10^1500).

---

## Connection to the Lucas-Lehmer Test

This theorem is why the Lucas-Lehmer test matters practically:

1. To find a new perfect number, find a new Mersenne prime.
2. To confirm a Mersenne prime M_p, run the Lucas-Lehmer sequence to step p−2.
3. If s_{p−2} ≡ 0 (mod M_p), then M_p is prime → N = 2^(p−1) · M_p is perfect.

The algebraic structure α = 2 + √2 in Z[√2]/M (proven in `ll_sequence_sympy.py`
and `lucas_lehmer_verify.py`) underpins why the sequence detects primality
with certainty.
