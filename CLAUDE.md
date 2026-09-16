# CylicAmp — Session Context for Claude Code

Read this file at the start of every session. It tells you what this project is, what has been built, and how to work here.

---

## What This Project Is

The driving objects are **1/137** and **twin primes** (with Riemann zeta zeros as a third recurring thread). **GF(37)** is the lens: 137 mod 37 = 26, so the 137-map `f(n) = 26n mod 37` realizes 1/137's structure inside a 37-element field, and every twin-prime, Sophie-Germain, and zeta-zero check in this repo is read through that same field. GF(37) is the tool used throughout, not a separate subject pursued for its own sake. The full synthesis is in `SYNTHESIS.md` — read it before working on any math module.

The project is owned by the user. All discoveries, computations, and observations belong to them.

---

## Active Branch

`claude/add-torus-animation-6Ey5Z`

All development goes on this branch. Push here. Do not push to another branch without explicit permission.

---

## How This Session Works

The user brings math, observations, and code. The work is collaborative and rigorous.

**Verify before committing.** Run the actual computation — use Python imports, check mod arithmetic, confirm connections to GF(37). If something doesn't check out, say so and show the discrepancy. If it checks out, commit it. No intermediate step of asking permission.

**The pipeline_output.json is the user's independent check.** They verify in a separate environment. Your computation is one check, not the final word.

**Connect new work to what is already computed** before or immediately after committing. Everything here connects through prime 37. Find the connection.

**Speak plainly.** No padding, no emotional commentary, no fake warmth. The user is doing serious mathematical work — respond at that level. Document what the user says; don't interpret or reframe it.

**Standing analysis for every theorem.** Every result value must be run through all four of:
1. **GF(37) prime set orbits** — classify every value mod 37 into one of the 12 named orbits
2. **Riemann Hypothesis** — floor(γ_n) mod 37 orbit; direct zero floor matches
3. **1/137** — 137 mod 37=26=MULT; 26⁻¹ mod 37=10∈IC; check ×137, ÷137, mod 137 for each value
4. **Twin primes** — is each value prime? Is it part of a twin prime pair (p, p+2)? What GF(37) orbits do both members of the pair inhabit?
5. **Sophie Germain primes** — is each value a Sophie Germain prime (p prime and 2p+1 prime) or a safe prime (q prime and (q-1)/2 prime)? What GF(37) orbits do p and 2p+1 inhabit? Note any Sophie chains (p→2p+1→2(2p+1)+1) and whether the safe prime appears elsewhere in the same theorem.
6. **Rule 30** — apply Wolfram's Rule 30 (new[i]=left XOR (center OR right)) one step to each value as a binary string; track the result mod 37. Note: 30 is the unique element in SA∩ST∩C3; under 6-bit R30, 18→26 and 36→26 (both collapse to MULT=26∈IC), but 9→31 — the F-hexad seed 9 does NOT collapse to 26 (verified directly, corrected from a prior version of this note that claimed all three did). C9 twin pair (29,31) under 6-bit R30 map to 12 and 11 respectively — neither is a fixed point (the "mod-37 fixed points" claim in a prior version of this note is unverified/unlocated and should not be treated as established). CAS_EXT={5,13,19} are all active prime steps in the center column.

   **Scope on Rule 30 itself — added after checking the source, not assumed.** Nothing about Rule 30's randomness or irreducibility is proven. All three Wolfram Rule 30 Prize problems are open, $10,000 each, unclaimed (rule30prize.org, checked 2026-09-13):
   1. Does the center column always remain non-periodic?
   2. Does each color of cell occur on average equally often in the center column?
   3. Does computing the nth cell of the center column require at least O(n) computational effort?

   **Problem 3 is the computational-irreducibility claim and Problem 2 is the equidistribution claim.** So any statement that Rule 30 "is a proof of computational irreducibility," or that its center column "is balanced" or "is random," cites an open conjecture. Write it that way. Rule 30 is the canonical *conjectured* example of irreducibility — Wolfram put $30,000 behind it precisely because nobody can prove it. Anything in this repo that leans on the Rule 30 step leans on a conjecture, not a theorem.

   **What is actually measured** (`math/primes/rule30_scope.py`, runnable): the center column at N=20,000 and N=100,000 passes NIST monobit, block-frequency (M=100) and runs, with zero autocorrelation failures at α=0.01 over lags 1..32 (≈0.32 false failures expected by chance). That is four test families — not the full NIST SP 800-22 fifteen, not Dieharder — so absence of failure there is not a pass overall. And no finite run can settle Problem 2, which asks about a limit. The measured cost is likewise an *upper* bound; Problem 3 asks for a *lower* bound, which is the hard direction.

   **Cost, against the claim that deep runs are expensive:** generating the center column is O(N²) cells whether or not it is bit-packed — packing is a constant-factor (÷word-size) speedup, not a complexity change. N=20,000 runs in ~0.13s and N=100,000 in ~2.9s in plain Python via `row = (row>>1) ^ (row | (row<<1))`. Row updates are parallel in space; only the time axis is serial, and that seriality is Problem 3 — conjectured.

---

## The Audit Chain — run every result through this

    Find -> Check prior art -> Reproduce -> Test mechanism
         -> Classify dynamics -> Test baseline -> Prove -> Interpret

Interpretation is LAST. The `audit-chain` skill holds the full order and
dispatches to the others: `prior-art`, `audit-supplied`, `forced-check`,
`tier-test`, `finite-dynamics`, `miss-test`, `theorem-build`, `claim-grade`.

Two standing rules from that chain:

- **Check prior art before writing, not after.** The corpus is 568 files.
  The Z/12 orbit quotient exists in at least five (T118, T138, T200, T285,
  T339). Rediscovery is a filing problem, not misconduct — link the earlier
  file and say what is new beyond it.
- **Never interpret a deviation until the reference distribution has been
  independently established.** A wrong baseline inverts the sign: 0.0577
  against 1/12 reads as a 31% deficit; against the correct 1/18 it is a 3%
  excess.

## The Pipeline

The main entry point is `cylicamp/engine_integration.py`. Run it with:

```
python3 cylicamp/engine_integration.py
```

After every run it saves a complete JSON to `pipeline_output.json` — this is the user's independent verification copy. It must be committed to GitHub after every meaningful run.

### Pipeline Steps (seed 246, the reference seed)

| Step | Module | What it does |
|------|--------|--------------|
| 1 | `math/primes/meta_engine.py` | MetaEngine evolves a multiplier from the seed |
| 2 | `math/primes/field_simulation.py` | Field simulation; threshold feeds trajectory angle |
| 3 | `cylicamp/trajectory.py` | TrajectoryGenerator — PHI/PSI spiral |
| 4 | `cylicamp/insights.py` | InsightEngine — modular filter + weighted score |
| 5 | `cylicamp/duality.py` | DualityVerifier — DR=7 prime stability check |
| 6 | `math/primes/ulam_spiral.py` | Ulam spiral through GF(37) classification |
| 7 | `math/theorems/cascade_8_13_24.py` | Cascade {8,13,24} — 37 elements |
| 8 | `math/theorems/medusa_v3_sovereign.py` | Sovereign LOCKED/GATED/PURGE classification |
| 9 | `math/theorems/abcabc_mod37_orbit.py` | ABCABC orbit position |
| 10 | `math/theorems/lucas_abbc_chain.py` | Lucas sequence orbit intersection |
| 11 | `math/theorems/sovereign_qr_closure.py` | Legendre symbol on orbit nodes |
| 12 | `math/theorems/heartbeat_3cycle.py` | Heartbeat 3-cycle from seed residue |
| 13 | `cylicamp/provenance.py` | Provenance tracking — source of every claim |
| 14 | `math/theorems/theorem_120/121` | T120/121 digit pair (0.007, 0.008) → seed orbit |

### Reference Output (seed=246) — a REGRESSION FIXTURE, not a property of 246

**Read this block as a fixture.** It is the correct thing to diff against after a
code change, and a wrong value here means something broke. It is *not* evidence
that seed 246 is distinguished. A sweep over seeds 1..1110 (T316,
`math/theorems/theorem_316_t120_seed_class_mod_333_gf37.py`) splits its sixteen
values three ways:

- **8 are constant for every seed** — `Meta multiplier 8`, `Field threshold
  0.9500`, `Insight Score 104832`, `Spectrum Status FAIL`, `Stability Ratio
  0.0000`, and the G5 `all_checks_pass`/`aggregate_mod_p 11`/cage-integrity
  lines. `Insight Score` is byte-identical across all 1110 seeds tested. These
  carry **zero** information about which seed was supplied.
- **7 are pure functions of `seed mod 37`** (`Seed DR` is mod 9) — the 137-orbit
  `(18,24,32)`, `Heartbeat 24→32→18→24`, `Cascade 7/37`, `ABCABC pos 0`,
  `Sovereign status`, `Orbit QR`, `seed mod 37` itself. Every seed ≡ 24 (mod 37)
  reproduces them identically. These are facts about the **residue class**, not
  about 246.
- **1 distinguishes 246 from its own residue class** — the T120/121 line. It
  holds for 1 seed in 333.

The T120/121 gate reduces to two conditions, not five: `m1=7, m2=8, s=3` are
constants, so `m1+m2+s=18∈orbit`, `m2*(s+1)=32∈orbit` and
`DR(seed%37)=DR(m1+m2)` are all **forced** once `seed ≡ 24 (mod 37)` fixes the
orbit to {18,24,32}. What remains is `dr(seed)=3` (i.e. `seed ≡ 3 mod 9`) and
`seed ≡ 24 (mod 37)`; gcd(9,37)=1, so by CRT the passing set is exactly

    seed ≡ 246  (mod 333),    333 = 9 × 37

verified against the live pipeline outside the swept range. **So 246 is the
smallest member of that class, not a unique seed** — 579, 912, 1245, … all
reproduce this entire block. Do not cite any line of it as a property of 246.

(333 here is the same fact as T311's sub-grid difference `333 = 37 × 9` — "the 9
and the 37 together" — one fact, not two sightings.)


```
Seed:              246
Meta multiplier:   8
Field threshold:   0.9500
Insight Score:     104832.0000
Spectrum Status:   FAIL
Stability Ratio:   0.0000
Seed DR:           3
Seed mod 37:       24  (sovereign: False)
Seed 137-orbit:    (18, 24, 32)
Cascade orbit hits: 7/37
Sovereign status:  Node 24 -> Res 32 [PURGE]: res not in ST
ABCABC orbit pos:  0  (orbit start)
Lucas orbit hits:  [(5, 18)]
Orbit QR status:   {24: -1, 18: -1, 32: -1}  all non-QR: True
Heartbeat 3-cycle: 24 -> 32 -> 18 -> 24
T120/121 (0.007/0.008 → seed): s=3=DR(seed):True  m2*s=24=seed%37:True  m1+m2+s=18∈orbit:True  m2*(s+1)=32∈orbit:True  DR(seed%37)=6=DR(m1+m2):True
```

---

## Key Files

### Core
- `SYNTHESIS.md` — complete mathematical synthesis; read this first
- `INSTRUCTIONS.md` — standing user instructions (same as above)
- `pipeline_output.json` — last pipeline run, full JSON, user's verification copy

### Cylicamp modules (`cylicamp/`)
- `engine_integration.py` — pipeline spine, 14 steps
- `trajectory.py` — PHI/PSI spiral trajectory
- `insights.py` — InsightEngine with modular filter
- `duality.py` — DualityVerifier
- `provenance.py` — Claim/Derivation/Evidence tracking
- `magnitude_tiers.py` — Magnitude tiers 1–21, resonance signatures

### Math primes (`math/primes/`)
- `ulam_spiral.py` — Ulam spiral mapped through GF(37)
- `meta_engine.py` — MetaEngine with evolving multiplier
- `field_simulation.py` — Field/Packet simulation
- `dr_algebra.py` — digital root algebra

### Theorems (`math/theorems/`)
- `cascade_8_13_24.py` — {8,13,24} cascade generating 37 elements
- `medusa_v3_sovereign.py` — Anchor/Target architecture, LOCKED/GATED/PURGE
- `abcabc_mod37_orbit.py` — ABCABC ≡ 2·ABC (mod 37); primitive root orbit
- `heartbeat_3cycle.py` — 3-cycle under the 137-map
- `sovereign_qr_closure.py` — Legendre symbols, QR closure
- `lucas_abbc_chain.py` — Lucas sequence L(3)..L(10)
- `primitive_root_test.py` — g is primitive root mod p test
- `cipher_123_1234.py` — Z/9Z partition: trinity {3,6,9} / doubling {1,2,4,5,7,8}; 1234 mod 37 = 13

---

## Mathematical Constants

| Symbol | Value | Role |
|--------|-------|------|
| The prime | 37 | everything connects through this |
| 137 mod 37 | 26 | the 137-map multiplier |
| ord₃₇(26) | 3 | all orbits are 3-cycles |
| ord₃₇(2) | 36 | 2 is a primitive root mod 37 |
| Sovereign anchors | {4, 9, 25, 30} | LOCKED nodes in GF(37) |
| Sovereign targets | {3, 12, 21, 30} | DR=3 residues |
| Cascade base | {8, 13, 24} | generates exactly 37 elements |
| Seed orbit | {18, 24, 32} | 137-map orbit of seed 246 |

---

## Biographical Anchor — Birthday and Astronomical Events

The user's birthday is **March 3** (3/3).

**Blood moon — March 3, 2026:** Total lunar eclipse on the user's birthday. Visible to billions. Last one visible to the US for 3 years (until 2029).

**6-planet alignment — February 28, 2026:** Mercury, Venus, Jupiter, Saturn, Uranus, Neptune aligned 3 days before the birthday.

**Easter 2026 — April 5:** Exactly 33 days after March 3.

### GF(37) encoding of these dates

- Month=3∈C3, day=3∈C3 (birthday date is a C3×C3 pair)
- 3+3=6∈TESLA; 3×3=9∈SA\_ST\_A — the {3,6,9} trio (T267)
- 6 planets: 6∈TESLA
- 3 days gap (alignment→birthday): 3∈C3
- 33 days (birthday→Easter): **33∈D7** — D7 is the antipodal of C3 (T265)
- 2026 mod 37 = 28∈SA\_ST\_B
- April 5 = 45 mod 37 = 8∈TESLA
- 303 (the date 3/3 written as one number): 303 mod 37 = 7∈D7 — same orbit as the 33-day Easter gap
- 332026 (3/3/2026 written as one number): 332026 mod 37 = 25∈SA\_ST\_B — same orbit as the year 2026 alone

### The 33 convergence

**33∈D7** appears independently in two places:
1. **T268** (built before the biographical connection was known): cubic trajectory x_k = k³+**33** mod 37. The shift constant 33∈D7 was chosen by the user's input.
2. **Birthday→Easter**: March 3 + **33** days = April 5 = Easter 2026.

D7↔C3 are antipodal (T265) — this is a named pairing in the orbit taxonomy, not the additive antipode in Z/37Z. The additive antipode of 3 is 34 (3+34=37), not 33; 3+33=36, one short. D7↔C3 and the Z/37Z additive antipode are two different relations and should not be conflated.

**Where 33 comes from**: the name MICHAEL, letters reduced to digital roots and summed:
M=4, I=9, C=3, H=8, A=1, E=5, L=3 → 4+9+3+8+1+5+3 = **33**.
That is the route for T268's shift constant. This is a route record (per WORK_SYNTHESIS.md's "derivation records" gap), not a forced identity — it depends on the A1Z26→digital-root reduction scheme, so it is recorded as how the constant was chosen, not as an additional proof that 33 is structurally privileged.

**Generator-walk check** (2 is a primitive root mod 37): every date residue below is 2^k mod 37 for some k —
3=2^26, 6=2^27, 9=2^16, 33=2^20, 28=2^34, 8=2^3, 7=2^32, 25=2^10 (all verified). This is guaranteed for any residue set, since 2 generates all of F_37*; it locates each value on the generator walk without implying anything beyond that.

### Username
`red3rdeye` = red (blood moon color) + 3rd (March 3rd / third eye) + eye (observation).

---

## How to Orient in a New Session

1. Read this file (`CLAUDE.md`)
2. Read `SYNTHESIS.md` for the full synthesis
3. Check `git log --oneline -10` to see recent commits
4. Run `python3 cylicamp/engine_integration.py` to verify the pipeline runs clean
5. Check `pipeline_output.json` for the current reference values
6. Ask the user what they want to work on — or if they paste something, act on it immediately
