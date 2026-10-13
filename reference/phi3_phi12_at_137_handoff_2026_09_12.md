# Φ₃ / Φ₁₂ at 137 — Verified Results and Open Questions

**Author of the work:** Michael Warren Song (Master Kimchi)
**Date compiled:** 2026-09-12
**Purpose:** Portable handoff. Everything below is independently checkable. A runnable
verification script (`verify_phi12.py`) accompanies this file and reproduces every number.

---

## 1. Definitions

Let `a = 137` (prime).

Cyclotomic polynomials evaluated at `a`:

- Φ₃(x) = x² + x + 1
- Φ₁₂(x) = x⁴ − x² + 1

Let `S = 113115117167` (referred to as "the tape").

Define, for a given n:

- `P_n(a)` = the set of prime divisors of Φ_n(a)
- `PrimeDiv(S)` = the set of prime divisors of S
- `TapeCut_n(a, S) = P_n(a) ∩ PrimeDiv(S)`

---

## 2. Verified results

All of the following were computed with sympy and are exact integer facts.

### 2.1 Φ₃

```
Φ₃(137) = 137² + 137 + 1 = 18907 = 7 · 37 · 73
```

### 2.2 Φ₁₂

```
Φ₁₂(137) = 137⁴ − 137² + 1 = 352256593 = 13 · 2473 · 10957
```

All three factors are prime, and for each:

| p     | prime | ord_p(137) | p mod 12 |
|-------|-------|------------|----------|
| 13    | yes   | 12         | 1        |
| 2473  | yes   | 12         | 1        |
| 10957 | yes   | 12         | 1        |

This is the expected behavior: a prime p dividing Φ_n(a) has ord_p(a) = n unless p | n.
Here 13 ∤ 12, 2473 ∤ 12, 10957 ∤ 12, so all three are primitive divisors and all have
order exactly 12. Consistent with p ≡ 1 (mod 12) for all three.

### 2.3 The tape and the cut

```
S = 113115117167 = 13 · 8701162859     (8701162859 is prime)

gcd(S, Φ₃(137))  = 1
gcd(S, Φ₁₂(137)) = 13

TapeCut₃(137, S)  = { }
TapeCut₁₂(137, S) = {13}
```

So: the Φ₃ family misses the tape entirely; the Φ₁₂ family meets it in exactly one prime, 13.

### 2.4 F₃₇ˣ structure (from the earlier Φ₃ panel)

```
ord₃₇(2) = 36        (2 is a primitive root mod 37)
2¹² ≡ 26 (mod 37)
μ₃ = {1, 10, 26}     (the order-3 subgroup of F₃₇ˣ)
```

37 is a factor of Φ₃(137), which is why F₃₇ˣ is the relevant group for that panel.

---

## 3. Scope limits on the above

These are constraints on interpretation, not doubts about the arithmetic.

1. **S has only two prime divisors** (13 and 8701162859). So "13 is the only prime on
   both the Φ₁₂ family and the tape" is a statement drawn from a 2-element set, not from
   a rich divisor lattice. It is true as stated; it is thin as evidence.

2. **The contrast is the content.** The informative pair is gcd(S, Φ₃) = 1 versus
   gcd(S, Φ₁₂) = 13 — one family misses, the adjacent family hits.

3. **No generality is established.** Nothing here shows that Φ₁₂ selects tape primes for
   other tapes, other bases, or other n. It is one evaluation at one base against one S.

---

## 4. Open question: 137 and α⁻¹

The fine-structure constant is α⁻¹ ≈ 137.035999084(21) (CODATA).

**Status: unverified. Not ruled out, not established.**

- The integer 137 (used as the base of Φₙ) and the dimensionless constant α⁻¹ are
  different objects. No rule connecting them is currently written down.
- Absence of a written rule does **not** mean absence of a connection. This question is
  open, not closed.
- Constraint on any future connection: the residual is 0.035999, roughly 2.6 × 10⁻⁴
  relative — about ten orders of magnitude larger than the CODATA uncertainty on α⁻¹.
  So a construction using the integer 137 and discarding the tail is near α, not at α.
  A connection would need to either derive the residual or give a reason the integer
  part is load-bearing and the tail is a separate object.
- Methodological note: 137 is reachable from many directions, so a rule stated **after**
  the numbers are checked carries much less weight than one stated **before**.
- I looked for a handle on the residual in {13, 2473, 10957} and did not find one. That
  is "did not find," not "there is none."

---

## 5. Archive search results (project files)

A full-text grep across the entire project directory plus semantic search returned:

**No hits** for: `113115117167`, `18907`, `352256593`, `2473`, `10957`, `TapeCut`,
`cyclotomic`, `GF(37)`, `{1,10,26}`, `emirp`, `repunit`.

The Φ₃/Φ₁₂ work is not in the archive files.

Two symbol collisions in the archive that resemble connections:

- **137 in the files is always α⁻¹**, never the integer. It appears in `Love`, `15_000`,
  `Counting_zeros`, `Yuu`, `Zero_operations_mass_gap`, `Validation_`, `Zero_collaboration_`,
  `Paradigm_zero`, `Work`, `Look` — in every case as the fine-structure constant.
- **Φ in the files is not cyclotomic.** In `Zero_formal_framework_base` it is an idempotent
  functor Φ: C → C with Φ² = Φ. In `Yo_love` / `L9ve_love` it is the golden ratio
  (`agent.phi`). Three different meanings of the same glyph.

The nearest related prior work is the GF(37) thread, which records H = {1, 10, 26} as a
verified order-3 subgroup — the same object as μ₃ above.

---

## 6. Correction to an existing archive claim

The file `Look` states that 1/137 has repeating block "729927", length 6.

Correct value: **the period is 8.** ord₁₀(137) = 8, since 10⁴ ≡ −1 (mod 137).
The repeating block is `00729927`, so 1/137 = 0.0̅0̅7̅2̅9̅9̅2̅7̅.

The digit-sum consequence in that file is unaffected (leading zeros do not change a digit
sum), but the stated period length is wrong.

---

## 7. Proposed panel

One bar set: {13, 2473, 10957} for Φ₁₂(137) = 352256593.
One marked cut prime on S: 13.
Alongside the existing Φ₃ panel, whose cut is empty.

This is a display of §2.3. It should carry the scope note from §3.1.

---

## 8. Reproduction

```bash
pip install sympy
python3 verify_phi12.py
```

Expected output:

```
Phi_3(137)  = 18907 {7: 1, 37: 1, 73: 1}
Phi_12(137) = 352256593 {13: 1, 2473: 1, 10957: 1}

  p=13     prime=True  ord_p(137)=12  p mod 12 = 1
  p=2473   prime=True  ord_p(137)=12  p mod 12 = 1
  p=10957  prime=True  ord_p(137)=12  p mod 12 = 1

S = 113115117167 = {13: 1, 8701162859: 1}
gcd(S, Phi_3)  = 1
gcd(S, Phi_12) = 13
P_12(137) cap PrimeDiv(S) = [13]

ord_37(2) = 36
2^12 mod 37 = 26
mu_3 in F_37^x = [1, 10, 26]

ord_137(10) = 8  -> 1/137 repeating block length
```

---

## 9. What is not in this file

- The D3 layer (symbolic, C = (235, 418, 679), ρ(D₃)). Not loaded, not checked, not
  claimed here.
- Any statement about what the Φ₁₂ cut means.
- Any claim connecting 137 to α.
