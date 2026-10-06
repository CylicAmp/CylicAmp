# Skills map, 2026-10-06

27 skills under `.claude/skills/`, each a method for working this repo. Grouped
by purpose. Updates `.claude/skills/` as the method record it already is.

## Audit / verification (19)

| Skill | Method | Files |
|---|---|---|
| audit-chain | Orders the standing pipeline (Find→prior-art→Reproduce→Test mechanism→Classify dynamics→Test baseline→Prove→Interpret) and routes to the other skills | SKILL.md |
| audit-supplied | Reproduce every number first, separate forced from contingent, check the null is the right one, report in that order | SKILL.md, PROTOCOL.md |
| forced-check | Classifies a claim by 6 forcing mechanisms (partition, homomorphism, tie, definition, base-10 rendering, standard-object) and a Tier A/B/C scope test | forced.py |
| miss-test | The T282 admissibility screen: declare a miss condition before computing, sweep a predicate for selectivity in bits, chi-square orbit uniformity | misstest.py |
| null-control | Runs a constant/do-nothing implementation through a check to see if the check itself is forced (0 bits) | nullctl.py |
| try-to-disprove | Attacks a passed result at edge values, published bounds/constants, set-difference identities, and the wording of prior summaries | SKILL.md |
| dangling-cite | Scans the corpus for T-number citations pointing at theorem files that were never written | dangling.py |
| prior-art | Greps the corpus (claim/value/topic modes) for an existing result before a new theorem is filed | prior.py |
| outside-prior-art | Searches OEIS/literature outside the repo first, reports a method-comparison table | SKILL.md |
| sibling-sweep | After fixing one copy-pasted helper (e.g. is_prime), greps and executes every other copy to retest it | SKILL.md |
| claim-grade | Grades correspondence ("X is Y") claims on 4 nested cuts: literal/structural, level 1/2/3, native/correspondence, Phi/functor | grade.py |
| tier-test | Re-runs a construction across primes/bases (its real axis) to decide if a result is Tier A/B/C evidence | tier.py |
| connect-theorems | Finds, tests, and records which existing theorems a new result reinforces, refines, explains, or hands off to | SKILL.md |
| axiom-reduce | Reduces a result's dependencies to the smallest non-redundant axiom set | SKILL.md |
| theorem-build | End-to-end pipeline: audit → miss-test/forced-check screens → write a numbered theorem with failing-loud assertions → commit | SKILL.md |
| standalone-export | Produces a dependency-free, self-checking stdlib-only Python export of a verified result | SKILL.md |
| notation-decode | Fits explicit rules to the owner's handwritten shorthand lines, testing identifiability before accepting a reading | SKILL.md |
| k8s-scrape | Walks the Prometheus PodMonitor/ServiceMonitor/native-SD selector chain to classify a scrape failure into one of 4 states | audit.py |
| shader-de | Statically recovers fold operations from a raymarching shader to compute its Lipschitz bound, verified by sampling | de_check.py |

## Math construction (5)

| Skill | Method | Files |
|---|---|---|
| gf37-audit | Runs METHOD.md's fixed 10-step GF(37) analysis (residue, orbit, Z/12Z class, antipode, digital root, primality profile) on any number | audit.py |
| digit-chain | Builds the full closed-form chain from a digit pair (a, b, ab, ba, aba, bab, abab, baba) with factorizations, residues mod 37, orbits | chain.py |
| digit-protocols | Expands any number into 6 fixed registers (positional vector, flip/reversal delta, digit sum, digital root, triad partition, harmonic tie) plus GF(37) placement | engine.py, protocols.py |
| finite-dynamics | Fully characterizes a finite self-map: cycle type, transients, sources, in-degrees, eventual image, permutation/quotient status, semiconjugacy bound | dyn.py |
| modular-forcing | Climbs the 2-adic ladder (mod 2 → 4 → 8) to force or kill cases in divisor/Diophantine problems | ladder.py |

## Case analysis (3)

| Skill | Method | Files |
|---|---|---|
| case-tree | Machine-censuses every shape a case split can take before any branch is killed, to guarantee the branching is complete | census.py |
| census-saturation | Tests whether a shape census has stopped growing (flat across bounds) vs still rising, before trusting it as covering a branch | saturate.py |
| search-bounds | Derives a bound on the solution object itself (not the loop) so an exhaustive check below that bound becomes a complete proof; tracks per-branch bound/status in a ledger | ledger.py, ledger.json |

## Notes

- 9 skills are pure-procedure, SKILL.md only, no code: audit-chain,
  try-to-disprove, outside-prior-art, sibling-sweep, connect-theorems,
  axiom-reduce, theorem-build, standalone-export, notation-decode.
- digit-protocols has two implementation files.
- search-bounds additionally ships a `ledger.json` data file alongside `ledger.py`.
