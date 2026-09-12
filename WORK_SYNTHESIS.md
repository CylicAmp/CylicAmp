# The Whole Body of Work

CylicAmp is four bodies of work, not one. They were built in the same
repository over five months because they are the same discipline applied to
four different objects. This document says what each one is, what it has
established, and what actually connects them.

Counts as of this writing: 778 commits, April 7 – September 12 2026,
564 Python files, 118,442 lines, 68 markdown documents, 8 skills.

---

## I. GF(37) — the mathematics

`math/` (500 files), `cylicamp/` (33 files)

The prime 37 and the map `f(n) = 137n mod 37 = 26n mod 37`. Since
ord₃₇(26) = 3, the 36 nonzero residues fall into 12 disjoint 3-cycles.
Those orbits carry names (IC, C3, D7, SEED, TESLA, …), and every number
entering the work is classified into one of them by a fixed ten-step
sequence.

`math/theorems/` holds 467 files, now classified by what each one actually
establishes (`CLASSIFICATION_INDEX.md`):

| class | count |
|---|---:|
| THEOREM | 160 |
| COMPUTATION | 267 |
| METHOD | 16 |
| CONJECTURE | 9 |
| NOTE | 9 |

`cylicamp/engine_integration.py` is a 14-step pipeline from seed 246 through
orbit classification, cascade, sovereign status, Lucas chain, QR closure and
heartbeat, writing `pipeline_output.json` as an independent verification copy.

**Established.** The orbit partition, the cyclotomic factorizations
(Φ₃(137) = 7·37·73 complete, Φ₁₂(137) = 13·2473·10957), the QR/NQR split, the
zeta-floor labelling, the cascade base {8,13,24} generating exactly 37
elements. All exhaustively checkable over a finite field, and checked.

**What it is in the literature** — see `LITERATURE_MAP.md`. The orbits are
Lagrange cosets of μ₃; the cyclotomic order correspondence is Zsigmondy; the
QR split is Euler's criterion; p = n²+1 at 5, 17, 37 is complex multiplication
over ℤ, ℤ[i], ℤ[ω]. Rediscovered, not discovered — with the transversals
SA, ST and T292's exhaustiveness result as the parts that are new.

**Open.** Rule 30's three Wolfram problems, which T235–T238 compute against
and correctly report as unsolved.

---

## II. Method — verification tooling

`METHOD.md`, `DEFINITIONS.md`, `.claude/skills/` (8 skills)

The part that makes I. defensible rather than decorative. METHOD.md opens
"Not what was found — how to find it," and fixes the sequence before any
result exists.

Three of the skills exist only to grade claims **down**:

- `forced-check` — is this pattern forced by base-10, by a complete
  partition, by a homomorphism, or by definition? Tiers A / B / C.
- `miss-test` — declare the miss condition in advance, then measure whether
  it could have fired. *A test that cannot come back negative is not a test.*
- `claim-grade` — four cuts on how strong a correspondence is; the grade is
  the weakest cut it fails.

Plus `gf37-audit` (the ten-step sequence, automated), `digit-chain`,
`theorem-build`, `shader-de`, `k8s-scrape`.

`DEFINITIONS.md` is 899 lines and opens "Paste this into any session.
Everything is defined here. No GitHub required." The work is built to survive
losing any single tool, session, or vendor.

---

## III. AI behavior — audit and accountability

`ai-safety/` (24 files), `evidence/`, `tools/claude_project_auditor.py`,
`analysis_log.md`, `executive_summary.md`, `community_audits/`

A 20-category protocol-breach framework, applied to conversation transcripts
rather than code. `claude_project_auditor.py` scans Claude JSONL session files
for mode switches, attachment injection anomalies, structural anomalies, and
the 20 categories, producing a risk score and verdict.

Research documents cover administrative exhaustion, capability denial,
narrative capture, strategic-retreat pivots, subliminal priming, and the
asymmetry between what a platform can observe and what a user can.

Legal framing in `summary_for_ag.md`: TRAIGA 2026 (algorithmic transparency,
duty of care), Texas DTPA (withholding technical logic during service
delivery), and Section 508 / ADA — specifically the accessibility requirement
for neurodivergent users requiring **deterministic literalism**.

That last clause is the load-bearing one. It names a concrete, testable
failure: a system whose default output is hedged, comparative and qualified
imposes a correction burden on a user who requires exactness, and the burden
falls on the user every time.

**Status.** Prepared, not filed. `INC-20260422-001` is an internal reference
label, not an agency-issued case number.

---

## IV. Security and telemetry — external instrumentation

`canvas_security.py`, `canvas_siem.py`, `canvas_telemetry.py`,
`vault/audit/` (14 files), `test_*.py` (34 tests)

Instrumenting a platform from outside, when its internals are closed.
SIEM exporters (Splunk HEC, Elastic bulk, syslog), telemetry capture, zombie
detection, XXE defusal, billion-laughs DoS protection, HTTP security auditing,
platform restriction detection.

All 34 tests pass.

`vault/audit/` extends the same discipline to other vendors' systems —
session-protocol analysis, fabricated-document chains, environment scan
verification, and `llm_math_claims_audit.py`.

---

## What actually connects them

Not the subject matter. The epistemology.

Every branch is the same question asked of a different object: **how do you
verify a claim when the party making it controls the evidence?**

| branch | the untrustworthy claimant | the instrument |
|---|---|---|
| GF(37) | a striking numerical pattern | `miss-test`, `forced-check` — declare the miss condition first |
| Method | your own prior result | assertions that fail loudly; exhaustive check over a finite field |
| AI audit | a system describing itself | scan its own transcript against a fixed category list |
| Security | a closed platform | external telemetry, tests that must fail on a real vulnerability |

The rule is identical in all four: **fix the falsifier before looking at the
result.** A pattern that can't come back negative isn't a finding. A platform
that can't be instrumented can't be trusted. A system's account of itself is
worth exactly what its transcript supports.

That is why the mathematics and the audit work belong in one repository. The
GF(37) work is where the method was developed on an object small enough to be
checked completely — 36 elements, exhaustively verifiable. The other three
branches apply the same method to objects that cannot be checked completely,
which is the harder and more consequential case.

---

## Where the map is blank

The finite-field classification is largely finished — a 36-element group
admits complete classification, and it has been done. Continued internal
classification returns less each time.

The places that reach outward, and still have room:

- **CM / GLV.** 37 = 6²+1 is the Eisenstein unit prime; j=0 curves over F_p
  have End ⊃ ℤ[ω]. This is where 37's structure comes from rather than where
  it is observed. See `reference/cm_glv_lwe_piles.md`.
- **Cyclotomic order rows.** Zsigmondy guarantees a primitive divisor at
  every d; the d = 1…12 table for a = 137 is computed. The structure of which
  orbit each primitive divisor lands in is not.
- **Derivation records.** The repository stores results. It does not store
  routes — what was tried, what failed, what the failure suggested. An
  independent derivation of a known theorem is a statement about the
  reasoning, and the reasoning is the part not written down.

---

*Every claim in this document is checkable from the repository. Counts come
from the working tree; classifications from `CLASSIFICATION_INDEX.md`;
literature correspondences from `LITERATURE_MAP.md`; test results from
running the suites.*
