```
================================================================================
CRYPTOGRAPHIC WORK — COMPILED
================================================================================
A. This thread: crypto-adjacent number theory (no protocol).
B. Earlier conversations: Kyber / LWE / McEliece / Bitcoin notes.
C. What is not a cryptosystem.
================================================================================


A. THIS THREAD — MATH THAT SHOWS UP IN CRYPTO
--------------------------------------------------------------------------------

A1. Finite field  F_37^×
  Cyclic of order 36. Primitive root 2 (discrete log base 2 exists).
  μ₃ = {1, 10, 26} = ⟨10⟩ = ⟨26⟩.  Order 3.
  137 ≡ 26 (mod 37).   26⁻¹ ≡ 10 (mod 37).
  Action: x ↦ 26x ↦ 10x ↦ x.
  12 orbits of F_37^× / μ₃, plus SEAM = 0.

  Crypto reading (standard, not a new primitive):
    F_p^× discrete log is the setting of classical DH / DSA-style groups,
    here only as a 36-element toy. Order 36 is not a security parameter.
    Cube roots of unity in F_p exist iff 3 | (p−1). That is the splitting
    law of Φ₃, used in pairing-friendly constructions and in GLV on
    j=0 curves. It is not a key-exchange.

A2. Cyclotomic  Φ₃
  Φ₃(x) = x²+x+1.
  Φ₃(137) = 18907 = 7 × 37 × 73. Complete.
  Theorem: p | Φ_d(a) ⇒ ord_p(a)=d unless p|d.

  Crypto reading:
    Cyclotomic polynomials index the order of a in F_p.
    Cyclotomic *rings* ℤ[x]/(Φ_n) are the ambient rings of NTRU / Kyber
    (different n, different use). Φ₃ itself is not a Kyber modulus.

  Two uses of Φ₃ stay separate:
    Use A — field / order of a cube root of unity.
    Use B — CM by ℤ[ω] on j=0 curves (endomorphism ω²+ω+1=0).

A3. CM curves  (the part that is actually used in ECC)
  j=0:   E: y² = x³+a,  End ⊃ ℤ[ω],  6 units,  disc −3.
         Twists: a'/a ∈ (F*)⁶.
         Traces from 4p = L² + 27M².
         p=37, L=11, M=1 → traces {±1, ±10, ±11}.

  j=1728: E: y² = x³+ax, End ⊃ ℤ[i], 4 units, disc −4.
         Twists: fourth powers. Traces from p = L²+M².

  T299: n · gcd(n, p−1) = p−1, n = #units of the CM ring.
        If n|(p−1) this is p = n²+1, unique per n:
          n=2  generic   p=5
          n=4  Gaussian  p=17
          n=6  Eisenstein p=37
        Units equal the n-th powers in F_p^× at those three primes.
        Exhaustive below 10⁵: only those three hits.

  Crypto reading:
    j=0 and j=1728 are the GLV curves (Gallant–Lambert–Vanstone).
    The endomorphism ω (or i) splits scalar multiplication.
    Sixth-power / fourth-power twists are the isomorphism criterion
    used when choosing a curve model. T299 is a unit-vs-powers test
    at tiny primes; it is not a pairing parameter or a curve-gen
    pipeline. 17 | (137−1) is unrelated to Gaussian CM.

A4. What this thread did not produce
  No DH/ECDH parameters, no pairing-friendly embedding degree,
  no secure curve (p=37 is a classroom field), no hash, no AEAD,
  no signature scheme, no hardness reduction.


B. EARLIER CONVERSATIONS — EXPLICIT CRYPTO NOTES
--------------------------------------------------------------------------------
Source conversation (Jul 2025): Kyber / LWE / McEliece / Bitcoin
plus a separate SHA-256 mining simulation thread.

B1. Learning With Errors (LWE)
  Hardness: distinguish (A, A s + e) from uniform, e small error.
  You asked for an LWE demo, then an expansion with “ATOMICS”
  constants and a C₂₄ scalar (~1913.668) injected into noise.
  Status: pedagogical / experimental. Injecting a fixed named
  constant into error is not a standard LWE parameter set and
  does not give a security proof. NIST Kyber does not use C₂₄.

B2. Kyber (ML-KEM)
  Module-LWE over a cyclotomic ring (not Φ₃; Kyber uses
  ℤ_q[x]/(x²⁵⁶+1)).
  You asked for: ring structure, Module-LWE, key generation tests,
  a Bitcoin-migration sketch.
  Status: study notes and a proposed extension of the LWE demo.
  Not a drop-in replacement for Bitcoin’s secp256k1 signatures
  and not a specified hybrid KEM-inside-Bitcoin BIP.

B3. Lattice-based overview
  SIS / LWE / Module-LWE / Ring-LWE as the post-quantum
  family. Security claim is worst-case lattice problems
  (approx-SVP / SIVP), not discrete log on F_37.

B4. McEliece (code-based)
  Public key = scrambled generator matrix of a Goppa code.
  You asked for a simplified implementation, tests, and a
  Bitcoin-integration sketch with ATOMICS used in error
  generation.
  Status: toy McEliece is not Classic McEliece. Classic
  McEliece public keys are large; Bitcoin script cannot
  carry them as-is. ATOMICS-as-error is not a Goppa decoder.

B5. Bitcoin-adjacent
  - SHA-256 mining simulation (nonce search, 3.125 BTC reward
    bookkeeping, GPU notes). That is a hash-iteration demo,
    not a wallet or a consensus change.
  - Proposed Kyber / McEliece “migration.” No fork spec,
    no address format, no signature replacement that
    existing nodes would accept.
  - WebSocket test plan with self-signed certificates
    (TLS hygiene, not a cryptosystem).


C. MAP: THIS THREAD → THOSE SCHEMES
--------------------------------------------------------------------------------
  F_37^× discrete log          toy DH group, not Kyber
  Φ₃ splitting / μ₃            cube roots of unity; GLV auxiliary
  j=0 / ℤ[ω] / sixth powers    GLV on BN/BLS-style curves (real ECC)
  j=1728 / ℤ[i] / fourth powers GLV on secp-style endomorphism
  T299 units = n-th powers     classroom check at p=5,17,37
  Maynard–Tao / M_k            sieve for prime gaps, not crypto
  Bunch–Kaufman / SMW / BFGS   numerical linear algebra, not crypto

  Kyber ring                   x^256+1, not Φ₃
  LWE error                    random discrete Gaussian, not C₂₄
  McEliece                     Goppa / irreducible polynomial, not F_37 orbits


D. HARD LINES  (so the copy does not overclaim)
--------------------------------------------------------------------------------
  1. F_37 work is classification of a 36-element group. It is not
     a primitive and not a parameter set.
  2. CM / T299 explains why p=5,17,37 are the unit-index primes
     for n=2,4,6. It does not generate a pairing-friendly curve
     and does not prove anything about 1/137 or RH.
  3. Kyber / LWE / McEliece notes from 2025 are study implementations
     plus speculative Bitcoin hooks. They are not standards and
     ATOMICS / C₂₄ are not part of the security argument.
  4. Nothing in either pile replaces secp256k1, SHA-256, or
     ML-KEM as specified by NIST.

================================================================================
END COPY
================================================================================
```
