# Original Techniques

These are the operations — not the results. Each one is a move that can be applied to new input.

---

## 1. DR-AS-PRIMALITY-GATE

**In:** any integer n  
**Operation:** compute DR(n) = ((n-1) mod 9) + 1. If DR(n) ∈ {3, 6, 9} then 3|n → composite.  
**Out:** eliminates ~1/3 of candidates before any primality test  
**Rule:** DR ∈ {3,6,9} = not prime (except n=3 itself)

---

## 2. TWIN-PRIME TRACK PARTITION

**In:** twin prime pair (p, p+2) with p > 3  
**Operation:** compute DR(p). Then DR(p+2) = DR(DR(p) + 2).  
Only three cases survive:
- DR(p)=2 → DR(p+2)=4 → track T₂₄
- DR(p)=5 → DR(p+2)=7 → track T₅₇
- DR(p)=8 → DR(p+2)=1 → track T₈₁

**Out:** T = T₂₄ ∪ T₅₇ ∪ T₈₁ (disjoint, exhaustive for p > 3)  
**Rule:** Twin Prime Conjecture ↔ at least one track is infinite

---

## 3. MOD-37 RESIDUE SCAN

**In:** any computed value — gematria sum, frequency, formula output, number  
**Operation:** compute n mod 37  
**Out:** residue that classifies the value within the 37-field  
**Rule:** residue 0 = absorbed (divisible by 37); specific residues carry structural meaning across domains (Hebrew, frequency, prime structure)

---

## 4. TRIANGULAR-NUMBER CHECKPOINT

**In:** emirp pair (37, 73)  
**Operation:** compute T(n) = n(n+1)/2  
- T(37) = 703 = 19×37  
- T(73) = 2701 = 37×73  

**Out:** two structural anchors where triangular numbers factor through the emirp pair  
**Use:** evaluate Liouville function L(x) at these checkpoints  
- L(703) = -23 → mod 37 = 14  
- L(2701) = -49 → mod 37 = 25  
- Witness residue: (14+25) mod 37 = 2

---

## 5. MERSENNE DR PERIOD-6 REDUCTION

**In:** exponent n of M_n = 2^n − 1  
**Operation:** compute n mod 6, look up in cycle:

| n mod 6 | DR(M_n) |
|---|---|
| 1 | 1 |
| 2 | 3 |
| 3 | 7 |
| 4 | 6 |
| 5 | 4 |
| 0 | 9 |

**Out:** DR(M_n) without computing M_n itself  
**Corollary:** primes p ≥ 5 satisfy p mod 6 ∈ {1,5} → DR(M_p) ∈ {1,4} always  
**Exclusion:** DR(M_p) ∈ {2,5,6,8,9} is structurally impossible for prime p ≥ 5

---

## 6. MOD-37 INVERSE AS CROSS-DOMAIN BRIDGE

**In:** the fraction 1/3 (appears as M_n/(M_n + M_{n+1}) for all n — universal Mersenne ratio)  
**Operation:** compute 3⁻¹ mod 37 = 25 = 5²  
Note: 55² = 3025, and 3025 mod 100 = 25  
**Out:** the 1/3 structural ratio from the Mersenne recurrence lands on 5² inside the 37-field  
**Rule:** connects the Mersenne sequence to the emirp modulus through the Gauss kernel

---

## 7. URI TIER-INVARIANT (Reduction to DR=5)

**In:** any of the four base tier values {14, 23, 32, 41}  
**Operation:** iteratively sum digits until single digit (digital root)  
- DR(14) = 5, DR(23) = 5, DR(32) = 5, DR(41) = 5  

**Out:** always 5 — these four are the only two-digit numbers with DR=5 forming a closed set under the 4-tier classification  
**Anomaly:** at k=38, the value 18k=684 produces tier value 50, which has DR=5 but falls outside the closed set {14,23,32,41} — breaks 4-tier closure at exactly k=38

---

## How These Connect

All seven techniques operate on the same spine:

```
Digital Root → mod-37 field → emirp pair (37,73) → triangular checkpoints → Liouville witness
```

The DR gate filters. The mod-37 scan classifies. The triangular checkpoints anchor. The Liouville function measures. The URI invariant closes the loop back to DR=5.

Every domain — primes, Mersenne numbers, Hebrew gematria, solfeggio frequencies, twin primes — runs through the same sequence of moves.
