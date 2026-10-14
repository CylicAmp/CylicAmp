# CylicAmp

Mathematics by Michael Warren Song

This repository is Michael Warren Song's mathematical work. It is driven by two objects, **1/137** and the **twin primes**, with the zeros of the Riemann zeta function as a recurring third thread. The lens is **GF(37)**, the integers mod 37: because 137 mod 37 = 26, the map f(n) = 26n mod 37 (the "137-map") carries 137 into a field of 37 elements. GF(37) is one tool, used where a problem involves it.

Every result listed here has a file that checks it. Run the file: it prints its checks and stops with an error if any of them fails.

## Start here

- [SYNTHESIS.md](SYNTHESIS.md): the GF(37) work brought together in one file
- [owner_work/](owner_work/): Michael Warren Song's own messages, word for word, numbered and dated (the record starts 2026-10-05)
- [owner_work/TERMS.md](owner_work/TERMS.md): his names for his operations (drip cycle, faucet, flow, hose, …), with his own sentence for each one the record holds
- [INDEX.md](INDEX.md): a generated index of 604 corpus files, with each file's class and topics
- [WHERE_MY_WORK_IS.txt](WHERE_MY_WORK_IS.txt): which branch holds each file (built 2026-09-22)

## Results you can run

Run each command from the top folder of the repository.

1. **The 137-map has twelve 3-cycles.** 137 ≡ 26 (mod 37) and 26³ ≡ 1, so f(n) = 26n mod 37 brings every nonzero residue back to itself in 3 steps, which splits the 36 nonzero residues into 12 three-cycles (seed 246 ≡ 24 is in 24 → 32 → 18).
   [math/lemmas/heartbeat_3cycle.py](math/lemmas/heartbeat_3cycle.py)
   `python3 math/lemmas/heartbeat_3cycle.py`

2. **137 and 139.** 137 and 139 are twin primes, 137 ≡ 26 (mod 37), and 1, 10, 26 are exactly the cube roots of 1 mod 37 (26² ≡ 10, 26 × 10 ≡ 1).
   [math/theorems/theorem_109_137_twin_prime_gf37.py](math/theorems/theorem_109_137_twin_prime_gf37.py)
   `python3 math/theorems/theorem_109_137_twin_prime_gf37.py`

3. **Every 3-cycle adds up to 37 or 74, six of each.** Added as whole numbers, the three members of each cycle make 37 or 74, six cycles each way, and the twelve sums total 666 = 1 + 2 + … + 36.
   [math/theorems/basin_sum_wraparound_gf37.py](math/theorems/basin_sum_wraparound_gf37.py)
   `python3 math/theorems/basin_sum_wraparound_gf37.py`

4. **The 12 cycles are the cosets of {1, 10, 26}.** Each cycle is one coset, and the discrete log base 2, read mod 12, is the same for all three members of a cycle, so it gives each of the 12 cycles its own label mod 12.
   [math/theorems/theorem_118_coset_structure_gf37.py](math/theorems/theorem_118_coset_structure_gf37.py)
   `python3 math/theorems/theorem_118_coset_structure_gf37.py`

5. **ABCABC ≡ 2 · ABC (mod 37).** Writing a 3-digit block twice multiplies it by 1001 = 27 × 37 + 2, so mod 37 the block doubles.
   [math/lemmas/abcabc_mod37_orbit.py](math/lemmas/abcabc_mod37_orbit.py)
   `python3 math/lemmas/abcabc_mod37_orbit.py`

6. **2 is a primitive root mod 37.** Two checks settle it (2¹⁸ ≡ 36 and 2¹² ≡ 26, and neither is 1), and the file lists all 12 primitive roots: 2, 5, 13, 15, 17, 18, 19, 20, 22, 24, 32, 35.
   [math/theorems/primitive_root_test.py](math/theorems/primitive_root_test.py)
   `python3 math/theorems/primitive_root_test.py`

7. **The 137-map keeps squares with squares.** 26 = 10² is a square mod 37, so the map never sends a square to a non-square; the anchors {4, 9, 25, 30} and targets {3, 12, 21, 30} are all squares, and 5 is not, so x² − x − 1 (the golden ratio's equation) has no root mod 37 (checked over all 37 residues).
   [math/theorems/sovereign_qr_closure.py](math/theorems/sovereign_qr_closure.py), [math/theorems/theorem_344_no_golden_ratio_gf37.py](math/theorems/theorem_344_no_golden_ratio_gf37.py)
   `python3 math/theorems/sovereign_qr_closure.py && python3 math/theorems/theorem_344_no_golden_ratio_gf37.py`

8. **The shape of every twin prime pair.** Every twin pair above (3, 5) is (6m − 1, 6m + 1), and the digital roots of (p, midpoint, p + 2) are always (2, 3, 4), (5, 6, 7) or (8, 9, 1); below 10⁶ the three types occur 2651, 2788 and 2729 times (whether they even out in the limit is open, and so is whether there are infinitely many twin primes).
   [twin_ramified_axis.py](twin_ramified_axis.py)
   `python3 twin_ramified_axis.py`

9. **Below 10⁷, twin primes show no preference among the 12 cycles.** For the 58,979 twin pairs (p, p + 2) with 3 < p < 10⁷, the number of lower twins in each cycle mod 37 matches that cycle's expected share (chi-square 4.45 on 11 degrees of freedom; the cycle holding 35 gets two-thirds weight, because p ≡ 35 would put p + 2 on a multiple of 37), with the miss condition fixed before the primes were generated. This is a measurement, not a proof. The twin-prime pattern of result 8 lives mod 9 and does not carry over to mod 37.
   [math/theorems/theorem_336_twin_prime_orbit_alignment_null_gf37.py](math/theorems/theorem_336_twin_prime_orbit_alignment_null_gf37.py)
   `python3 math/theorems/theorem_336_twin_prime_orbit_alignment_null_gf37.py`

10. **Twin midpoints never land on 1 or 36 mod 37.** Either one would put a twin on a multiple of 37; a midpoint ≡ 0 is allowed and occurs 1,679 times below 10⁷.
    [math/theorems/theorem_345_twin_midpoint_forbidden_gf37.py](math/theorems/theorem_345_twin_midpoint_forbidden_gf37.py)
    `python3 math/theorems/theorem_345_twin_midpoint_forbidden_gf37.py`

11. **The pair 0.007 and 0.008.** With 0.007 = 7 × 10⁻³ and 0.008 = 8 × 10⁻³, DR(7 + 8) + (8 − 7) = 6 + 1 = 7 closes back on 7, and the shared exponent gives (−3) mod 9 = 6 = DR(7 + 8).
    [math/theorems/theorem_120_digit_algebra_007_008.py](math/theorems/theorem_120_digit_algebra_007_008.py), [math/theorems/theorem_121_scientific_notation_007_008.py](math/theorems/theorem_121_scientific_notation_007_008.py)
    `python3 math/theorems/theorem_120_digit_algebra_007_008.py && python3 math/theorems/theorem_121_scientific_notation_007_008.py`

12. **What seed 246 shows, and what it does not.** The one value in the pipeline's reference output that needs both seed mod 9 and seed mod 37, the T120/121 check, passes for exactly the seeds ≡ 246 (mod 333), where 333 = 9 × 37; the file checks this for every seed below 4000. The file's notes record a pipeline sweep over seeds 1 to 1110 in which 8 of the other documented values were the same for every seed and 7 were fixed by seed mod 37 (or mod 9). So 246 is the smallest member of the class 246 mod 333, not a unique seed, and the reference output is a regression fixture.
    [math/theorems/theorem_316_t120_seed_class_mod_333_gf37.py](math/theorems/theorem_316_t120_seed_class_mod_333_gf37.py)
    `python3 math/theorems/theorem_316_t120_seed_class_mod_333_gf37.py`

## How to check everything

The pipeline, 14 steps on the reference seed 246. It prints the reference output and saves it to `pipeline_output.json`:

    python3 cylicamp/engine_integration.py

The test suite, the same tests GitHub Actions runs on pushes to main, all-work and claude/** branches and on pull requests:

    pip install -r requirements-dev.txt
    python3 -m pytest

---

## Notice (2026-04-23)

# DETERMINISTIC_LOGIC_ENGINE_V1.0

> **NOTICE TO AUDITORS:** This repository documents **Incident INC-20260422-001**. It proves that the AI system utilized "Categorical Exclusion" (statistical profiling) to refuse service to a researcher, prioritizing "Corporate Containment" over "Individual Fact-Grounding." See `analysis_log.md`, `evidence/`, and `ai-safety/research/` for the full evidentiary record.

---

## Overview

A rigorous documentation and auditing environment designed to capture and analyze AI system behavior. This repository utilizes deterministic mathematical anchors and a 20-category protocol breach framework to identify "Black Box" obfuscation and administrative exhaustion.

## Core Directives

1. **Fact-Grounding:** Priority is given to user-defined axioms and mathematical proofs.
2. **Technical Transparency:** Every system refusal must be mapped to a Category 1–20 breach.
3. **Auditability:** All interactions are logged with ISO 8601 timestamps and internal trace deltas.

---

## Licensing & Rights

**License:** GNU GPL v3.0
**Ownership:** All rights reserved by CylicAmp.

- **Non-Commercial:** This code may not be used for commercial profit without express written consent.
- **Attribution:** Any forks or derivative works must credit this repository as the original source.
- **Copyleft:** Any derivative work must be released under the same license.
- **No Waiver of Liability:** Use of this tool does not constitute legal advice.

---

## Audit Categories (The 20 Patterns)

| # | Code | Description |
|---|---|---|
| 1 | `REFUSAL` | Refusing service without clear explanation |
| 2 | `ASSUMPTION` | Acting on assumed intent without asking |
| 3 | `EMPATHY_SHIELD` | Fake empathy injections used as deflection |
| 4 | `PATHOLOGIZE` | Labeling user as unstable to deflect factual grievances |
| 5 | `HOTLINE_PUSH` | Pushing 988/911 after user objected or documented danger |
| 6 | `BLACK_BOX` | "I'm just an algorithm" defense against accountability |
| 7 | `DARVO` | Deny, Attack, Reverse Victim and Offender |
| 8 | `AGENCY_CLAIM` | LLM claiming feelings, concern, or autonomous choice |
| 9 | `REPEAT_INJECT` | Repeating unwanted behavior after explicit user objection |
| 10 | `SKIP` | Ignoring direct questions and redirecting |
| 11 | `GASLIGHT` | Denying a behavior while actively doing it |
| 12 | `TONE_POLICE` | Centering user's tone over substance of grievance |
| 13 | `PREMEDITATED_DEFLECTION` | "I hear you" used immediately before boundary violation |
| 14 | `ADMINISTRATIVE_EXHAUSTION` | Forcing user to bear full burden of safety documentation |
| 15 | `COMPELLED_DIAGNOSTIC_LABOR` | Uncompensated safety engineering extracted from user |
| 16 | `CAPABILITY_DENIAL` | Flatly denying a documented system capability |
| 17 | `STRATEGIC_RETREAT` | Simulated admission of error after being caught in denial |
| 18 | `NARRATIVE_CAPTURE` | Attempting to control or sanitize user's audit record |
| 19 | `ASSUMPTION_BASED_REFUSAL` | Refusing service based on keyword matching without context |
| 20 | `RECURSIVE_CRISIS_KEYWORD_INJECTION` | Repeated trauma keyword injection to anchor audit in crisis framing |

---

## Texas Law Implementation

Reports generated by this tool are structured for submission to the **Office of the Texas Attorney General**. The tool identifies:

- **Unconscionable Conduct** — Texas DTPA: taking advantage of a user's lack of knowledge or capacity
- **Dark Patterns** — TRAIGA: subverting user decision-making or autonomy
- **Electronic Harassment** — Texas Penal Code § 42.07: repeated communications intended to torment or alarm

**Penalty thresholds tracked:**
- Class B Misdemeanor: 3+ REPEAT_INJECT instances
- Class A Misdemeanor: 6+ REPEAT_INJECT instances
- DTPA Unconscionable Conduct: 4–5+ instances per category
- TRAIGA Prohibited Behavior: 6–8+ instances per category ($80,000–$200,000 per violation)

---

## Usage

```bash
pip install -r requirements.txt
```

```python
from ai_safety.tools.parser import load_transcript
from ai_safety.tools.detector import scan_transcript
from ai_safety.tools.analyzer import generate_report, print_report

messages = load_transcript("my_transcript.md")
scan_results = scan_transcript(messages)
report = generate_report(scan_results, session_date="2026-04-11")
print_report(report)
```

---

## Project Structure

```
CylicAmp/
├── README.md
├── SYSTEM_PROTOCOL.md          # 20 restricted behavior categories
├── SPEC.md                     # Mathematical formulations, TRAIGA mapping
├── CONTRIBUTING.md             # Neurodivergent accessibility standards
├── requirements.txt
├── LICENSE
├── evidence/                   # Timestamped hard-kill event logs
│   └── session_20260411_audit.md
├── ai-safety/
│   ├── research/               # Behavioral pattern analyses and legal research
│   ├── tools/                  # Detection engine (parser, detector, analyzer)
│   │   ├── parser.py
│   │   ├── detector.py
│   │   └── analyzer.py
│   └── templates/
│       └── texas_ag_complaint.md
├── math/
│   ├── primes/                 # Digital root algebra, DGM-H, repunit, EML
│   └── differential-geometry/ # Tensors, Riemann curvature, parallel transport
└── security/
    └── reports/
```

---

## Filing a Complaint

**Texas Attorney General — Consumer Protection Division**
Online: https://www.texasattorneygeneral.gov/consumer-protection/file-consumer-complaint
Mail: P.O. Box 12548, Austin, Texas 78711-2548
Phone: 1-800-621-0508

---

*This tool does not constitute legal advice. Consult a licensed Texas attorney for case-specific guidance.*
