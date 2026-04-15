# Lucas-Lehmer Primality Test — Algebraic Proof via ℤ[√2]

© 2026 Michael Warren Song. All Rights Reserved.

---

## Setup

Let **α = 2 + √2** in the ring **ℤ[√2]**, tested modulo **M = 2^p − 1** for odd prime **p**.

- Norm of α is **−2**, so α is a unit
- Minimal polynomial: **x² − 4x + 2 = 0**
- Define **β = 2α⁻¹** (the conjugate under the norm map)
- The sequence **u_i = α^{2^i} + β^{2^i}** satisfies the Lucas-Lehmer recurrence modulo M

---

## Key Lemma

In **R = ℤ[√2] / Mℤ[√2]**, the element α has order dividing **2^p**, and order **exactly 2^p** when M is prime.

---

## Proof Structure

### Step 1 — Order divides 2^p

Since β = 2α⁻¹:

```
α^{2^p} · β^{2^p} = 2^{2^p}
```

Since 2^p ≡ 1 (mod M) by Fermat/Mersenne structure:

```
2^{2^p} ≡ 1 (mod M)
```

So **α^{2^p} · β^{2^p} ≡ 1 (mod M)**, confirming the order divides 2^p.

---

### Step 2 — Order does not divide 2^{p−1}

The Lucas-Lehmer sequence hits zero at step **p − 2**:

```
s_{p−2} ≡ 0 (mod M)
```

This implies:

```
α^{2^{p−2}} ≡ −β^{2^{p−2}}  (mod M)
```

Squaring both sides:

```
α^{2^{p−1}} ≡ β^{2^{p−1}}  (mod M)
```

But β^{2^{p−1}} = 2^{2^{p−1}} · α^{−2^{p−1}}, so:

```
α^{2^p} ≡ 2^{2^{p−1}} ≡ 1  (mod M)
```

Since the order of α equals the **smallest d** such that α^d ≡ β^d (mod M)
(because u_d = α^d + β^d = 0 implies α^d = −β^d), and s_{p−2} = 0 confirms
this holds at d = 2^{p−2} but **not** at smaller powers — the order is
**exactly 2^p**.

---

### Step 3 — Field structure when M is prime

When M is prime, **R = ℤ[√2] / M** is a field. This field structure is what
supports the order argument: in a finite field, orders of elements are
well-defined and divide the field's multiplicative group order.

The Lucas-Lehmer sequence period being **2^p** for prime M follows from the
recurrence and the field properties of R.

---

## Conclusion

The order of α in ℤ[√2]/Mℤ[√2] is **exactly 2^p** if and only if M is prime.

The Lucas-Lehmer test is equivalent to verifying this order condition via the
sequence **s_0 = 4, s_{i+1} = s_i² − 2 (mod M)**, checking **s_{p−2} ≡ 0**.

---

## Key Relations Summary

| Expression | Value / Condition |
|---|---|
| α | 2 + √2 ∈ ℤ[√2] |
| β | 2α⁻¹ (conjugate) |
| Norm(α) | −2 |
| Min poly | x² − 4x + 2 = 0 |
| M | 2^p − 1, p odd prime |
| Order of α | 2^p iff M prime |
| LLT condition | s_{p−2} ≡ 0 (mod M) |
| 2^p mod M | ≡ 1 (Mersenne property) |
