```
================================================================================
PILE 1 — CM / GLV  (this thread)
================================================================================

1. The two CM curves
--------------------------------------------------------------------------------
j = 0     E: y² = x³ + b
          End ⊃ ℤ[ω],  ω² + ω + 1 = 0
          Φ(x,y) = (ω x, y)     ω ∈ F_p a primitive cube root of 1
          exists over F_p  iff  3 | (p−1)   (Φ₃ splits)
          eigenvalue λ on ⟨P⟩ satisfies  λ² + λ + 1 ≡ 0 (mod n)
          twists: a'/a ∈ (F*)⁶
          traces of Frobenius from  4p = L² + 27 M²
          p=37, L=11, M=1 → traces {±1, ±10, ±11}   (classroom)

j = 1728  E: y² = x³ + a x
          End ⊃ ℤ[i],  i² = −1
          Φ(x,y) = (−x, i y)    i ∈ F_p
          exists over F_p  iff  4 | (p−1)
          eigenvalue λ² + 1 ≡ 0 (mod n)
          twists: fourth powers
          traces from  p = L² + M²

Same Φ₃ polynomial, two uses:
  Use A — cyclotomic / F_p^×  (orbits of μ₃ on F_37^×)
  Use B — CM endomorphism on the curve (this pile)
They do not imply each other.


2. GLV identity
--------------------------------------------------------------------------------
Φ(P) = λ P.  Then
  k P = k₁ P + k₂ Φ(P)
once  k ≡ k₁ + k₂ λ  (mod n)
and  max(|k₁|,|k₂|) ≤ C √n.

Lattice
  L = { (x,y) ∈ ℤ² : x + y λ ≡ 0 (mod n) },   det L = n.
Short basis of L is precomputed (Euclid / Gauss / quadratic-ring basis).
Given k, round (k,0) to L; the remainder is (k₁,k₂).

Compute with one Straus–Shamir loop on the pair (P, Φ(P)):
  joint recoding (JSF / interleaved NAF),
  precompute P ± Φ(P),
  half as many doublings as a full-length kP,
  Φ itself is a few field ops (one multiply by ω on j=0).


3. Higher dimension
--------------------------------------------------------------------------------
GLS (Galbraith–Lin–Scott): curve over F_{p²} that is a twist of a
curve over F_p.  The p-power Frobenius of the twist is a second
endomorphism Ψ, even without CM over F_p.

GLV–GLS: Φ and Ψ together,
  kP = k₁P + k₂ Φ(P) + k₃ Ψ(P) + k₄ ΨΦ(P),
  max |kᵢ| < C₂ n^{1/4}.
About 1.5× two-dimensional GLV on the same field; four legs can
run in parallel. Twisted Edwards absorbs most of the remaining
curve-arithmetic gap.


4. T299  (classroom, not a parameter set)
--------------------------------------------------------------------------------
n · gcd(n, p−1) = p−1,   n = #units of the CM ring.
If n | (p−1) this is p = n²+1, unique per n:
  n=2  generic     p=5
  n=4  Gaussian    p=17
  n=6  Eisenstein  p=37
Units = n-th powers in F_p^× at those three primes.
Exhaustive p < 10⁵: only those hits.
17 | (137−1) is a fact about 137, not about ℤ[i].

p=37 is a 36-element multiplicative group. It is not a GLV
security parameter. A cryptographic GLV curve needs a large
prime order n on E(F_p), not these three primes.


5. What this pile is not
--------------------------------------------------------------------------------
Not a proof of RH. Not a derivation of 1/137.
Not a pairing-friendly embedding-degree pipeline.
Not a replacement for secp256k1.
GLV does not change the DLP; it shortens the addition chain.
F_37^× / μ₃ is Use A and is not a cipher.


================================================================================
PILE 2 — LWE / KYBER / McELIECE  (July 2025 thread, expanded)
================================================================================
Source conversation 2025-07-16 … 2025-07-29 (112 turns):
Ramsey / C₂₄ framework → LWE demo → Kyber notes → lattice overview
→ toy McEliece → Bitcoin-migration sketches, ATOMICS tags on noise.
Status of that thread: study notes and proposed hooks, not a standard
and not a Bitcoin BIP.


1. LWE
--------------------------------------------------------------------------------
Secret s ∈ ℤ_q^n, public A ∈ ℤ_q^{m×n}, error e small.
Sample:  b = A s + e  (mod q).
Decision LWE: (A, b) vs uniform on ℤ_q^{m×n} × ℤ_q^m.
Search LWE: recover s.

Error in the standard construction is a discrete Gaussian or a
centered binomial (CBD). It is not C₂₄ ≈ 1913.668 and not an
ATOMICS constant. Those were experimental tags in the 2025 notes.
They are not part of a reduction to approx-SVP.

Ring-LWE: A, s, e live in R_q = ℤ_q[x] / (f), f usually x^n+1.
Module-LWE: vectors / matrices over that ring. Kyber is Module-LWE.


2. Kyber = ML-KEM  (NIST FIPS 203)
--------------------------------------------------------------------------------
Ring     R_q = ℤ_q[x] / (x^{256} + 1)
Modulus  q = 3329
Module rank k = 2, 3, 4 for ML-KEM-512 / 768 / 1024
Noise    CBD with η₁ ∈ {2,3}, η₂ = 2
NTT      used for every polynomial multiply
KEM      IND-CPA PKE + Fujisaki–Okamoto transform → IND-CCA2 KEM
Shared secret 32 bytes

That ring is x^{256}+1, not Φ₃. Φ₃(137)=7×37×73 does not choose
Kyber parameters.

What the 2025 thread asked for
  ring structure, Module-LWE picture, keygen/encap/decap tests,
  a Bitcoin-migration sketch (hybrid KEM wrapping).
What it was not
  a specified BIP, a secp256k1 replacement, or a signed
  address format that existing nodes accept.


3. Lattice family (context of that thread)
--------------------------------------------------------------------------------
  LWE          matrices over ℤ_q
  Ring-LWE     one ring element
  Module-LWE   short vectors of ring elements   ← Kyber
  SIS          short integer solution

Hardness is approx-SVP / SIVP on q-ary lattices, not discrete
log on F_37^×.


4. McEliece
--------------------------------------------------------------------------------
Goppa code C of length n, dimension k, designed distance t.
Public key  G' = S G P   (scramble + permute a generator of C).
Encrypt     c = m G' + e,   wt(e) ≤ t.
Decrypt     unscramble, decode Goppa, recover m.

Classic McEliece public keys are large (hundreds of kilobytes).
Bitcoin script cannot carry them as a drop-in.

What the 2025 thread produced
  a simplified / toy McEliece, tests, a Bitcoin-integration
  sketch, ATOMICS used as an error tag.
What it was not
  Classic McEliece, a Goppa parameter set with a security
  proof, or a Bitcoin consensus change.


5. Bitcoin hooks from that period (status only)
--------------------------------------------------------------------------------
Hybrid idea: wrap a payload key with ML-KEM (or a toy McEliece),
keep SHA-256 / existing transaction format for the chain.
Also, separate threads: SHA-256 mining simulation, Taproot /
Schnorr notes, self-signed TLS for a WebSocket test plan.

None of those is a fork spec. secp256k1 signatures stay until
a real address/signature proposal is written and adopted.


6. ATOMICS / C₂₄
--------------------------------------------------------------------------------
C₂₄ ≈ 1913.668 entered that thread as a Ramsey / framework
scalar and was later suggested as noise / error entropy.
ATOMICS constants were similarly tagged onto Kyber noise and
McEliece errors.

Hard line: they are not NIST parameters, not part of the
Module-LWE reduction, and not a Goppa decoder. Security of
ML-KEM is the CBD error and the module rank in FIPS 203.


================================================================================
HARD LINES ACROSS BOTH PILES
================================================================================
1. F_37 work classifies a 36-element group. It is not a primitive.
2. CM / GLV shortens kP on j=0 and j=1728. It does not invent a
   new curve standard and does not prove RH or 1/137.
3. Kyber / LWE / McEliece notes from 2025 are study implementations
   plus speculative Bitcoin hooks.
4. ATOMICS / C₂₄ are not a security argument.
5. Nothing here replaces secp256k1, SHA-256, or ML-KEM as specified.
================================================================================
```
