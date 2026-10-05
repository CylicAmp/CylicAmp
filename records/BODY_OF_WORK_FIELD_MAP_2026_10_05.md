# Body of work: field map, 2026-10-05

This map shows which outside fields the repo's work connects to, where it can
contribute most, and what work would establish each contribution. It was put
together from two surveys and some direct checks.

## What stands

The eight sections below are fields, not results. Each one holds many results.

- **Graded results:** 161 files are graded THEOREM and 267 COMPUTATION in
  CLASSIFICATION_INDEX, and about 500 more files are not yet graded.
- **New to the published record:** 577 terms of OEIS A185584 beyond its
  published range (9.3·10¹⁸), and the m-sequence 60, 286650, …, which is not in
  OEIS. Both come with a proved lemma, proofs that k = 2, 3 and 6 are
  impossible, and a search to 10²² that a second program confirms.
- **Independent rediscoveries of standard theory:** cosets (Lagrange),
  Zsigmondy, Euler's criterion, Kummer, and CM curves.
- **Errors caught in outside material:** a Miller–Rabin prime test that
  accepted a composite, a false "Leyland record" claim (the number is divisible
  by 113 and 5101), and a refuted "kernel dim 5" claim.
- **Formal proofs:** four Lean 4 theorems, written with no unfinished proof
  steps but not yet compiled.

## How this was made, and its limits

- **Mathematics survey.** Covered SYNTHESIS, WORK_SYNTHESIS, INDEX, LITERATURE_MAP
  and CLASSIFICATION_INDEX, plus samples across math/theorems, math/lemmas,
  math/primes, math/exhaustion, divisor-square-sums, lean/, paper/ and papers/.
- **Checked directly** (2026-10-05):
  - Φ₃(137) = 18907 = 7·37·73.
  - `divisor-square-sums/verify.py` passes: 4 small solutions, and 587 family
    members with m ≤ 10²².
  - Fixed `verify.py` so it no longer fails when run from outside its own folder.
- **Not surveyed.** The survey of the non-math areas (forensic/, security/,
  ai-safety/, algorithms/, llm_eval/, baserate/) stopped early. Its rows below
  come only from top-level READMEs and directory listings.
- **Grades are the repo's own.** Statuses (THEOREM, CONJECTURE, REFUTED, Tier
  A/B/C) are quoted from the files. This pass did not re-check them, except where
  marked.
- **Corpus size.** CLASSIFICATION_INDEX grades 467 files: 161 THEOREM,
  267 COMPUTATION, 16 METHOD, 9 CONJECTURE, 14 NOTE. math/theorems holds 985
  files, so about half the tree is ungraded.

## Ranked by contribution to an outside field

### 1. Number theory: divisor-square sums (OEIS A185584)
**What exists**
- Proved lemma: n = m·p with p = σ₂(m)/m − m prime, p > m/2 and p ∤ m.
- Proved impossibility for k = 2, 3 and 6.
- Proof that at most one prime of n lies above the prefix.
- Exactly 4 solutions below 10⁹, by exhaustive sieve.
- 587 family members with m ≤ 10²², complete by bounded search. The search was
  cross-checked against an independent implementation at 10¹², 10¹⁴, 10¹⁶ and
  10¹⁸.
- 577 of those members lie beyond the published OEIS range.
- The m-sequence 60, 286650, … is recorded as not in OEIS.
- A draft submission is in `divisor-square-sums/OEIS_SUBMISSION.md`.

**Why it ranks first:** this is the one result that is new to the outside
literature, sits on a standing OEIS entry, and comes with a runnable check.

**To establish it**
1. Submit the new m-sequence to OEIS (this needs an OEIS account in the owner's
   name).
2. Add the 577 new terms, or a b-file, to A185584 as an extension.
3. Write a short note (arXiv math.NT) with the lemma, the k = 2, 3, 6 proofs,
   the completeness method (prime-by-prime build plus the supply-cycle loops)
   and the cross-check.
4. Open questions, which would raise it from data to theorem:
   - Is the family finite?
   - Close the m = 108·s² sub-case.

### 2. Research method: auditing pattern claims
**What exists:** 28 skills in `.claude/skills/`. Each encodes a check, and each
has a recorded case where the check caught a real error:
- **forced-check, tier-test, miss-test, null-control:** whether a pattern is
  forced, holds at other primes, can fail, or also passes a do-nothing input.
- **prior-art, outside-prior-art, dangling-cite:** rediscovery and citation gaps.
  - T245 was OEIS A185584 for weeks before anyone noticed.
  - T382–T421 are cited but were never written.
- **try-to-disprove:** caught a Miller–Rabin bug. Witnesses 2..37 accept the
  composite 318665857834031151167461.
- **Baseline audits:**
  - 0.0577 reads as a 31% deficit against 1/12, but a 3% excess against the
    correct 1/18.
  - The prime-pair baseline is 2/35, not 1/18 (T362).

**Fields:** meta-science and reproducibility; verification of computer- and
AI-assisted mathematics.

**To establish it:** write the method up as a paper or a practitioner guide
built on these cases, each with the defect, the check that caught it, and the
file. The record already exists in the commits; what is missing is the write-up
and a comparison with existing practice (pre-registration, null models,
look-elsewhere corrections).

### 3. Formal verification (Lean 4)
**What exists:** `lean/CylicAmp.lean`, 161 lines, with four theorems:
DR_ADDITIVITY, DR_PRIME_FILTER, TWIN_TRIPARTITE and TWIN_CENTER_DIV6. It
contains no `sorry`.

**Gap:** no build log or lake manifest, and Lean is not installed here, so it
has never been shown to compile.

**To establish it**
1. Compile it against Mathlib in CI.
2. Formalize the divisor-square lemma and the k = 2, 3 impossibilities. Those
   proofs are short and fully elementary.

### 4. Computational number theory: twin-prime coset saturation
**What exists:** `cylicamp/twin_prime_saturation.py`. Exact first-fill point
N* = 43,068,437 for all 6561 cosets mod 3¹⁰, for each twin type.

**To establish it:** compare it against the Hardy–Littlewood / Bateman–Horn
prediction for when the last coset fills. That comparison has not been done, so
the figure is data without a reference distribution yet.

### 5. Cellular automata (Rule 30)
**What exists**
- T236: block coverage up to k = 10.
- T241: left-permutivity.
- T244: the right-boundary period formula, exact for j ≤ 9 and failing for
  j ≥ 10.
- `rule30_scope.py`: statistical tests.
- T240 is recorded as proving "P2 ⇒ P3".

**Not checked in this pass:** T240. An implication between two open prize
problems would matter, so it needs a full audit before it is cited anywhere.

**To establish it:** audit T240, then put the boundary-period result (T244)
alongside OEIS A094605/A094606.

### 6. Finite fields, modular forms and elliptic curves over F₃₇
**What exists**
- The 12-orbit / μ₃-coset structure (T118).
- {7, 37, 73} = all primes with ord_p(137) = 3 (T292, re-checked above).
- The j = 0 / CM results (T288, T293).
- The order-12 cyclotomic classes (T433).

**Status:** LITERATURE_MAP records most of this as classical ("Rediscovered, not
discovered"): Lagrange, Zsigmondy, Euler's criterion, CM theory.

**Contribution:** worked, executable examples of classical theory, which is
teaching value.
- New per the files: the named transversals SA/ST and the {8, 13, 24} cascade.
- To establish those: run tier-test, to see whether they hold at other primes.

### 7. Physics crossover (`papers/nuclear_stability_gf37.tex`)
**What exists:** maps the nuclear magic numbers mod 37. The repo's own T373 calls
these "observed numerical correspondences, not causal derivations".

**To establish it:** a miss-test against random 7-element sets of the same size
range, before any physics claim. Nothing in the file is a nuclear-physics
mechanism.

### 8. AI behaviour documentation (`ai-safety/`, `README.md`, `evidence/`)
**What exists**
- A 20-category taxonomy of LLM failure modes, in README.md.
- About 40 research notes.
- Signing and attribution reports.
- Audits of other models' supplied code.

**Not surveyed** in this pass, so no assessment of its contents is made here.

**Fields:** AI evaluation; human–AI interaction.

**To establish it** in those fields:
- Coding rules for each category.
- Inter-rater agreement.
- The transcripts as a dataset.
- A comparison with published work on sycophancy and refusal behaviour.

## Not yet assessed
- forensic/, security/, algorithms/, llm_eval/, baserate/ and api/: not surveyed.
- `discoveries/` (2026-04) and the two LaTeX papers: no tier grading.
- About 518 theorem files: outside CLASSIFICATION_INDEX.
