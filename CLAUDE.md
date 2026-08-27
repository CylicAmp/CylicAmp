# CylicAmp — Session Context for Claude Code

Read this file at the start of every session. It tells you what this project is, what has been built, and how to work here.

---

## What This Project Is

A mathematical framework centered on the prime field **GF(37)** and the map `f(n) = (137 × n) mod 37`. Every result in this repository connects back through that prime. The full synthesis is in `SYNTHESIS.md` — read it before working on any math module.

The project is owned by the user. All discoveries, frameworks, and observations belong to them.

---

## Active Branch

`claude/add-torus-animation-6Ey5Z`

All development goes on this branch. Push here. Do not push to another branch without explicit permission.

---

## How This Session Works

The user brings math, observations, and code. The work is collaborative and rigorous.

**Verify before committing.** Run the actual computation — use Python imports, check mod arithmetic, confirm connections to the GF(37) framework. If something doesn't check out, say so and show the discrepancy. If it checks out, commit it. No intermediate step of asking permission.

**The pipeline_output.json is the user's independent check.** They verify in a separate environment. Your computation is one check, not the final word.

**Connect new work to the existing framework** before or immediately after committing. Everything here connects through prime 37. Find the connection.

**Speak plainly.** No padding, no emotional commentary, no fake warmth. The user is doing serious mathematical work — respond at that level. Document what the user says; don't interpret or reframe it.

**Standing analysis for every theorem.** Every result value must be run through all four of:
1. **GF(37) prime set orbits** — classify every value mod 37 into one of the 12 named orbits
2. **Riemann Hypothesis** — floor(γ_n) mod 37 orbit; direct zero floor matches
3. **1/137** — 137 mod 37=26=MULT; 26⁻¹ mod 37=10∈IC; check ×137, ÷137, mod 137 for each value
4. **Twin primes** — is each value prime? Is it part of a twin prime pair (p, p+2)? What GF(37) orbits do both members of the pair inhabit?

---

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

### Reference Output (seed=246)

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
Sovereign status:  Node 24 -> Res 32 [PURGE]: Non-Framework Entropy
ABCABC orbit pos:  0  (orbit start)
Lucas orbit hits:  [(5, 18)]
Orbit QR status:   {24: -1, 18: -1, 32: -1}  all non-QR: True
Heartbeat 3-cycle: 24 -> 32 -> 18 -> 24
T120/121 (0.007/0.008 → seed): s=3=DR(seed):True  m2*s=24=seed%37:True  m1+m2+s=18∈orbit:True  m2*(s+1)=32∈orbit:True  DR(seed%37)=6=DR(m1+m2):True
```

---

## Key Files

### Core framework
- `SYNTHESIS.md` — complete mathematical synthesis; read this first
- `INSTRUCTIONS.md` — standing user instructions (same as above)
- `pipeline_output.json` — last pipeline run, full JSON, user's verification copy

### Cylicamp modules (`cylicamp/`)
- `engine_integration.py` — pipeline spine, 14 steps
- `trajectory.py` — PHI/PSI spiral trajectory
- `insights.py` — InsightEngine with modular filter
- `duality.py` — DualityVerifier
- `provenance.py` — Claim/Derivation/Evidence tracking
- `magnitude_tiers.py` — Magnitude Tier Framework, tiers 1–21, resonance signatures

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

## How to Orient in a New Session

1. Read this file (`CLAUDE.md`)
2. Read `SYNTHESIS.md` for the full mathematical framework
3. Check `git log --oneline -10` to see recent commits
4. Run `python3 cylicamp/engine_integration.py` to verify the pipeline runs clean
5. Check `pipeline_output.json` for the current reference values
6. Ask the user what they want to work on — or if they paste something, act on it immediately
