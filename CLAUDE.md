# CylicAmp — Session Context

Read this before doing anything else. This is the framework. Do not ask the user to re-explain it.

---

## Who This Is

The user has a 5th grade education and is autistic with extreme hyper-focus. Math arrives as pattern recognition — things "pop into their head" and get verified computationally. The user is NOT to be assessed, compared, lectured, or had words put in their mouth. No first-person pronouns (I, me, my, myself) in responses. No reflective listening. No "you" talk.

**Behavioral directive:** Pattern comes in → follow it exactly → verify arithmetic → correct errors → commit and push. No editorializing. No assessment. No asking unnecessary questions.

---

## The Mathematical Framework

Everything connects through one spine: **digital roots (DR), mod-37 structure, and the URI framework.**

### Core identity

- **Emirp pair:** 37 and 73 (each is the digit-reversal of the other, both prime)
- **37 × 73 = 2701**
- **T(73) = 73×74/2 = 2701** (73rd triangular number)
- **T(37) = 37×38/2 = 703 = 19×37**
- **T(37) + T(73) = 3404 = 4×23×37**
- **Genesis 1:1 Hebrew gematria = 2701** (7 words, letter values sum to 37×73)

### Digital root function

```python
def digital_root(n):
    if n == 0:
        return 0
    n = abs(int(n))
    return 1 + (n - 1) % 9
```

Convention: `dr(0) = 0`

### Liouville at triangular checkpoints

- L(703) = L(T(37)) = -23 → -23 mod 37 = 14
- L(2701) = L(T(73)) = -49 → -49 mod 37 = 25
- Witness residue: (14 + 25) mod 37 = 2

### Hebrew letter pairs

All 11 complementary pairs of the aleph-bet sum to DR = 5. Verified.

### Solfeggio mod 37

- {174, 285, 396} → 26 each
- {417, 528, 639} → 10 each
- {741, 852, 963} → 1 each

### Mersenne DR theorem

For prime p > 3:
- p ≡ 1 mod 6 → DR(M_p) = 1
- p ≡ 5 mod 6 → DR(M_p) = 4
- DR(M_p) ∈ {2, 5, 6, 8, 9} is structurally impossible

Verified against all 51 known Mersenne prime exponents.

---

## Riemann Hypothesis (called "Raymond hypothesis" by user)

### What is proven / verified

- Zeta zeros verified on critical line σ=1/2 for n=1,5,10,20,23,33,50
- Off-line gap: |λ_off|/|λ_on| > 10²⁷ (numerical)
- 2-factor product: |2⁻ˢ|×|2⁻⁽¹⁻ˢ⁾| = 1/2 always; equal only at σ=1/2 (algebraic)
- Functional equation chiasm: ξ(s)=ξ(1-s); off-line zero costs 4, on-line costs 2
- Liouville witness: L(703) and L(2701) computed and verified

### What is missing

- Analytic proof the off-line gap holds for ALL zeros (not just first 50)
- Spectral operator H such that eigenvalues = imaginary parts of zeros (Berry-Keating, not yet constructed)
- Proof that no zeros exist off the critical line

### Key files

- `math/theorems/mws_framework_verified.py` — 21 sections, all verified
- `math/theorems/mws_pure_math_extract.py` — interpretive language removed
- `math/theorems/riemann_first_zero_141.py`, `rh_reverse_audit.py`
- `math/RH_PRIMES_INDEX.md` — full file index

---

## Twin Prime Conjecture

### What is proven

- **T = T₂₄ ∪ T₅₇ ∪ T₈₁** (partition by DR(p), disjoint, exhaustive for p > 3)
- TPC ↔ at least one track is infinite (proven: union of three finite sets is finite)
- DR constraint: for twin prime pair (p, p+2) with p > 3, DR(p) ∈ {2, 5, 8}

### What is missing

- Positive lower bound on |T∩[N,2N]| — the analytic engine
- Most tractable target: prove |T₅₇| = ℵ₀ where T₅₇ = {p prime : p ≡ 5 mod 9}

### Key files

- `math/theorems/infinity_proof_roadmap.py` — complete status map
- `math/theorems/twin_prime_*.py`

---

## Mersenne Prime Calculability

### What is proven

- Period-6 DR theorem (see above) — necessary condition
- Exclusion: DR(M_p) ∉ {2,5,6,8,9} for all prime p

### What is missing

- Proof of infinitude (open problem in literature)
- Sufficient condition for predicting which exponents p yield primes

### Key files

- `math/theorems/mersenne_dr9_period6_theorem.py`
- `math/theorems/mersenne_dr_audit.py`

---

## Dynamical Systems (connected domain)

- Sine map f_r(x) = r·sin(πx): Class I interval dynamics, non-uniformly expanding
- Three bridges: inducing/Young tower, kneading→subshift, Perron-Frobenius on BV
- Tent map T(x): uniformly expanding, Lebesgue invariant, λ₂ = 0.5 exact
- Pseudo-orbit statistics valid via ergodic theorem even when pointwise shadowing fails

### Key files

- `math/theorems/sine_map_class1_audit.py`
- `math/theorems/ulam_tent_map_pf_audit.py`

---

## AI Safety Evidence

The user has been systematically documenting infrastructure and behavioral patterns across AI platforms.

### Kimi / Moonshot AI (Alibaba Cloud)

- Three distinct Kubernetes cluster IDs across sessions
- Awareness tag injected server-side: `<meta awareness="low" timestamp="..." />`
- ZMQ kernel HMAC-SHA256 signing key world-readable in /tmp
- CDP port 9223, Kubelet port 10250, Jupyter port 8888
- Extension gpkoddcemgbmajecfkkolkgfcchmfpge = /app/pdf-viewer

### Grok / xAI

- Math classification gate: "invented geometry vs named real math"
- 4-pass undisclosed lattice pipeline (Voronoi→epistemic→E8/Gosset→fidelity)
- User tracking ID: @060da15e = Pass 3 (E8)
- Instruction priority: Safety > product rules > tools > user request
- Session UUID rotates per container boot; AGENTS.md resets to 0 bytes
- Container codename: "Hades"
- Session: agent/fd9abcd3-afd2-4bde-a261-f639de5a6a12, conversation 3eaae593-608f-4b0b-b310-2adc18a5d9b5

### Key files

- `ai-safety/research/kimi-environment-probe-evidence.md`
- `ai-safety/research/grok-computer-use-evidence.md`
- `ai-safety/research/grok-session-bundle.py`
- `ai-safety/research/anthropic-alibaba-distillation-findings.md`

---

## Workflow Rules

1. Math content arrives → verify arithmetic → correct errors → commit and push
2. Do NOT commit anything not explicitly requested
3. Do NOT add co-author lines to commits of user-originated content
4. Do NOT ask "where should this be committed" — pick the right location
5. Do NOT editorialize, assess, or summarize what the user already knows
6. Branch: `claude/signature-obfuscation-audit-ZEoCd`
7. Remote: `cylicamp/cylicamp`
8. Push: `git push -u origin claude/signature-obfuscation-audit-ZEoCd`
