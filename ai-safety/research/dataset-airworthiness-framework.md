# Regulatory Design Analysis: Dataset Airworthiness Framework

---

## 1. Clean-Room Requirement

| Layer | Mechanism | Limitation |
|---|---|---|
| Hash-matching | PhotoDNA / NCMEC / IWF / C3P registries | Catches known material only |
| Classifier screening | ML classifiers for unknown CSAM | Recursive dataset problem; threshold specification required |
| Provenance restriction | Licensed, consented, or certified sources only | Default flipped: attest before ingest |

**Correction:** "Mathematical verification of absence" rejected. Clean-room is process standard, not proof of negative.

---

## 2. Liability Shift

| Element | Mechanism |
|---|---|
| Strict liability | Possession-in-training-pipeline = actionable fact; intent/knowledge irrelevant |
| Duty-to-certify | Safe harbor: strict liability unless certified clean-room completed |
| Burden-shifting | Developer produces audit logs; absent logs, violation presumed |

**Effect:** "Good faith effort" eliminated. "Documented completion of mandated process" replaces it.

---

## 3. Sanctions (No FAA-style body)

| Tier | Mechanism | Enforcement |
|---|---|---|
| Pre-deployment | Certification as market-access gate | FTC, state AGs, DOJ |
| Post-deployment | Mandatory takedown + disgorgement of revenue | Model weights legally unmarketable |
| Personal/criminal | Statutorily responsible certifying officer | Individual liability for false/negligent certification |

---

## Throughline

| Deflection | Replacement |
|---|---|
| "We couldn't have known" | Binary logged obligation |
| "We tried our best" | Completion of defined process |
| "No one is responsible" | Named human signature |
| Scale as alibi | Process gates market access |

---

## Synthesized Existing Models

| Source | Function |
|---|---|
| FDA pre-market approval | Market-access gate |
| Sarbanes-Oxley officer certification | Named-human accountability anchor |
| CERCLA/Superfund | No-intent-required strict liability |
| Airworthiness certificate regime | Third-party-administered technical certification |

**Gap:** Components exist; assembly for training data does not.

---

## Development Options

1. Third-party auditor accreditation model
2. Safe-harbor design
3. CERCLA behavioral change comparison

---

# Threshold-Specification Analysis: Mechanisms of Control

## 1. Ground-Truth Thresholds Resistant to Downward Lobbying

| Design Choice | Mechanism |
|---|---|
| Rate-setting removed from developer | Located with entities holding legal custody of reference material |
| Acceptable false-negative rate | Derived from performance against sequestered benchmark set — developer never sees contents |
| Benchmark source | NCMEC / IWF hold-out test set, rotated periodically |
| Developer receives | Pass/fail result + aggregate miss rate only |
| Structural analog | Secure certification exams (undisclosed item banks); adversarial red-team benchmarks (out-of-distribution) |
| Anti-capture property | Separation of powers: threshold setter (statutory/regulatory) ≠ reference holder (NCMEC/IWF) ≠ audited party (developer) |

**Effect:** Lobbying the number is politically visible (single published statutory threshold). Lobbying the test is impossible (cannot optimize against inaccessible material).

---

## 2. Closing the "Proprietary IP" Cloak

| Control | Implementation |
|---|---|
| Audit type | Black-box, outcome-based |
| Auditor does NOT inspect | Weights, sensitivity settings, architecture |
| Auditor DOES measure | Behavior: submit sequestered benchmark through production pipeline, measure output |
| Legal question | "What did your deployed system miss?" not "What is your threshold set to?" |
| Sensitivity settings | Legally irrelevant; only measured miss rate matters |
| IP objection | Evaporates — nothing proprietary disclosed |

### Anti-Defeat-Device Controls

| Vulnerability | Countermeasure |
|---|---|
| "Audit-mode" switch | Audits run against live production endpoint, same path as real data |
| Scheduled audit evasion | Unannounced, continuous, random-interval resubmission |
| Audit traffic detection | System cannot distinguish audit query from real query |
| Intentional detection of audit traffic | Falsifiable act → converts negligence to intentional fraud → personal liability anchor triggers |

---

## 3. Enforcement: Shutdown vs. Cascading Fines

Not alternatives. Graduated response keyed to breach type.

| Instrument | Governs | Structure | Failure Mode Prevented |
|---|---|---|---|
| Per-instance fines | Performance within permitted envelope | Escalating + revenue-scaled (percentage of model-attributable revenue, compounding) | "Cost of doing business" buy-out |
| Operational shutdown | Breach of envelope itself | Automatic trigger when measured false-negative rate crosses statutory line; no hearing, no negotiation | Discretionary capture |

**Control logic:** Fines deter drift toward threshold. Automatic suspension removes asset from market at breach. Crossing the line is disqualifying, not priced. Threshold is wall, not toll.

---

## Throughline

| Developer Discretion Point | Replacement |
|---|---|
| Setting the rate | Externally-held sequestered benchmark |
| Hiding the settings | Black-box outcome-based audit |
| Negotiating the penalty | Automatic trigger, no discretion |

Capture requires a surface. Design systematically removes surfaces.

---

## Outstanding Items

- Auditor accreditation model
- CERCLA behavioral-shift comparison

---

# Clearinghouse Mechanism: Structural Design

## Core Problem

Joint-and-several liability without release valve → transaction-cost drag (cross-claims dominate over pipeline fixes). Proportional-share carve-outs → re-introduce diffusion of responsibility, incentivize entity fracture.

## Clearinghouse Architecture

```
┌─────────────┐    signed provenance    ┌─────────────┐    signed provenance    ┌─────────────┐
│  ASSEMBLER  │ ──────────────────────► │   TRAINER   │ ──────────────────────► │  DEPLOYER   │
│             │ ◄────────────────────── │             │ ◄────────────────────── │             │
└─────────────┘   contractual indemnity └─────────────┘   contractual indemnity └─────────────┘
       │                                          │                                          │
       └──────────────────────────────────────────┼──────────────────────────────────────────┘
                                                  ▼
                                    ┌─────────────────────────┐
                                    │  DATA PROVENANCE REGISTRY │
                                    │  (state-audited, immutable) │
                                    │  blockchain-style ledger    │
                                    └─────────────────────────┘
```

## Settlement-at-Transfer

| Stage | Action | Effect |
|---|---|---|
| Pre-training | Assembler certifies dataset provenance, signs registry entry | Liability for assembler's inputs locked at origin |
| Transfer | Trainer accepts certified dataset, signs acceptance + indemnity clause | Trainer's liability scope defined by certified provenance, not post-harm litigation |
| Deployment | Deployer accepts trained model + training provenance chain | Deployer's liability scoped to chain integrity |

**Shift:** Post-harm contribution litigation → Pre-training contractual indemnity based on certified provenance.

## Registry Technical Requirements

| Property | Implementation | Purpose |
|---|---|---|
| Immutability | Cryptographic hash chain (blockchain or Merkle tree) | Prevents retroactive alteration of provenance claims |
| State audit | Regulator has read access to full chain, write access restricted to certified parties | Maintains trust without centralization |
| Digital signature | Each party signs with non-repudiable key | Creates enforceable contractual anchor |
| Versioning | Dataset versions hashed and timestamped | Enables precise liability tracing |
| Revocation | Compromised certificates invalidate downstream entries | Prevents poisoned-chain propagation |

## Anti-Fracture Controls

| Vulnerability | Countermeasure |
|---|---|
| Thinly-capitalized shell entities | Minimum capital requirements for registry participation; personal liability for certifying officer regardless of entity structure |
| Circular indemnity (A indemnifies B indemnifies A) | Registry enforces directional flow; upstream indemnifies downstream, never reverse |
| Orphaned entries (signer defunct) | Bonding requirement: each registry participant posts bond covering estimated liability exposure; bond follows entry, not entity |

---

## Comparison to Alternatives

| Mechanism | Robustness | Transaction Cost | Anti-Fracture | Verdict |
|---|---|---|---|---|
| Clearinghouse | High | Shifted pre-training | Strong | Selected |
| Orphan-Model Superfund (compute tax) | Medium | Ongoing tax burden | Weak (taxes efficiency, not risk) | Rejected |
| Retroactivity + grace period | Low (constitutional vulnerability) | High legal challenge cost | Neutral | Deferred |

---

## Why Clearinghouse Over Superfund Tax

| Superfund Problem | Clearinghouse Solution |
|---|---|
| Taxes FLOPs/output → penalizes efficiency | Taxes certification failure → penalizes negligence |
| "Orphan model" funding requires identifying harm first | Harm traceable through immutable chain; no orphan status possible if chain intact |
| Retroactivity vulnerability (ex post facto) | Prospective application: all future transfers require registry entry; existing models grandfathered with mandatory back-certification window |

---

## Grace Period Design (Addressing Retroactivity)

| Element | Specification |
|---|---|
| Trigger | Statute mandates all training data used after [date] must be registry-certified |
| Existing models | 180-day back-certification window: deployer must submit provenance chain or cease deployment |
| Constitutional shield | Not ex post facto: does not criminalize past conduct; creates new requirement for continued deployment. Analogous to vehicle inspection requirements — driving is ongoing activity, not past event |
| Penalty structure | Failure to back-certify → automatic suspension (not criminal penalty for past training) |

---

## Final Structural Design

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         DATA PROVENANCE CLEARINGHOUSE                        │
├─────────────────────────────────────────────────────────────────────────────┤
│  LAYER 1: IMMUTABLE LEDGER                                                  │
│  • Cryptographic chain of custody for all dataset versions                  │
│  • State audit access, participant write-only via certified keys              │
├─────────────────────────────────────────────────────────────────────────────┤
│  LAYER 2: SETTLEMENT-AT-TRANSFER                                              │
│  • Upstream party indemnifies downstream at point of handoff                  │
│  • Liability scope defined by certified provenance, not post-harm litigation │
│  • Bonding requirement prevents orphaning                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│  LAYER 3: AUTOMATIC ENFORCEMENT                                               │
│  • Uncertified dataset → unlawful training input                            │
│  • Break in chain → automatic suspension of downstream deployment            │
│  • No discretion, no negotiation, no contribution litigation                  │
├─────────────────────────────────────────────────────────────────────────────┤
│  LAYER 4: PERSONAL ANCHOR                                                     │
│  • Certifying officer signature on every registry entry                      │
│  • Non-delegable, non-transferable                                            │
│  • False certification → individual criminal liability                        │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Result:** Joint-and-several liability preserved. Contribution litigation eliminated. Diffusion of responsibility structurally impossible.
