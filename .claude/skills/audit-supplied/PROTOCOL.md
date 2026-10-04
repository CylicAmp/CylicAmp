# Mathematical Audit Protocol (owner-supplied, 2026-10-04)

Filed verbatim in substance from the owner's message of 2026-10-04. Checked claims inside it:
`math/theorems/audit_protocol_cycle_drift_check_2026_10_04.py`.

## 1. Record Structure

### Required fields
Every substantive record must independently specify:
- OBJECT CLASSIFICATION — what the record is.
- AUDIT LEVEL — how thoroughly it was checked.
- VERIFICATION MODE — how evidence was obtained.
- PROOF STATUS — what the evidence establishes.

Every substantive record must contain:
ID, STATEMENT, OBJECT CLASSIFICATION, AUDIT LEVEL, VERIFICATION MODE, PROOF STATUS, EVIDENCE,
SCOPE, DEPENDENCIES, COMPUTATION, PRECISION, CONCLUSION.

Use NONE, NOT APPLICABLE, or UNVERIFIED where necessary. Separate claims with different scopes,
dependencies, evidence bases, or proof statuses. If a record contains multiple conclusions, split
it into separately auditable records or explicitly assign a status to each conclusion.

### Additional fields
Where applicable: SOURCE, PROVENANCE, ASSUMPTIONS, CONTRADICTIONS, CORRECTIONS, STATUS HISTORY,
REPRODUCTION INSTRUCTIONS.

## 2. Classification and Scope

### Object classification (exactly one)
- DEFINITION — introduces terminology, notation, or an object.
- IDENTITY — asserts equality over a stated domain.
- PROPOSITION — states a claim requiring justification.
- THEOREM — a proposition established by valid proof.
- LEMMA — a proved auxiliary result.
- COROLLARY — a result following from established results.
- CONJECTURE — an unproved proposed statement.
- COUNTEREXAMPLE — a verified object disproving a universal claim.
- COMPUTATIONAL RESULT — a specified computational output.
- ARTIFACT — an object, dataset, proof, program, or document being audited.

Do not classify a record as THEOREM, LEMMA, or COROLLARY merely because it is labeled that way in a
source. Classification must agree with the evidence and proof status.

### Scope
State the claim and scope: domain, assumptions, quantifiers, limitations, boundary conditions,
exclusions, and whether the claim is general or restricted. Evaluate the claim at the scope
actually stated, not at a stronger scope inferred from context. Restricted-domain evidence cannot
establish an unrestricted claim without separate proof.

## 3. Dependencies and Contradictions

### Dependency inventory
Identify all material inputs, definitions, conventions, assumptions, and dependencies. A
conclusion is only as strong as its weakest material dependency. A material unresolved dependency
prevents PROVED, CONDITIONALLY PROVED, or DISPROVED unless the conclusion is demonstrably
independent of it. If assumptions are necessary, record them and use CONDITIONALLY PROVED.

Distinguish: a false claim, an unsupported claim, an unverified claim, an invalid proof attempt, a
failed computation, an unavailable computation, and a contradiction between records.

### Contradiction handling
Preserve conflicting results; never select one silently. Create:
CONTRADICTION ID, CLAIM A, CLAIM B, COMMON INPUTS, DIVERGENT OPERATION, DIVERGENT ASSUMPTION,
INDEPENDENT RECOMPUTATION, SOURCE AND PROVENANCE COMPARISON, RESOLUTION, REMAINING UNCERTAINTY,
FINAL STATUS.
Until resolved, dependent claims cannot be marked fully established. If the conflict is immaterial,
state why and document the independence argument.

## 4. Verification

### Modes (record only modes actually performed)
- SYMBOLIC: transformations, identities, derivations shown and checked.
- DIRECT-CALCULATION: stated inputs directly evaluated by a specified operation.
- INDEPENDENT-CROSS-CHECK: a materially different route reaches the same result.
- EXHAUSTIVE-FINITE: finite domain completely specified and every element checked.
- NUMERICAL: evaluation, precision, tolerance and rounding recorded.
- COMPUTATIONAL: algorithm, implementation, inputs, outputs and scope recorded.
- LITERATURE-CROSS-CHECK: search record, sources, comparison and relevance recorded.
- STRUCTURAL: follows from independently checked structural properties.
- DEPENDENCY-AUDIT: upstream and downstream dependencies inventoried and assessed.
- REPRODUCIBLE: complete materials, environment, instructions and expected outputs available.

### Dependency-chain audit
definitions -> inputs -> arithmetic -> derivation -> exact result -> numerical result -> conclusion.
Check domain validity, type compatibility, units, indexing, boundary conditions, quantifiers,
hidden assumptions, duplicated endpoints, omitted cases, invalid transformations, unverified
external claims, and accidental numerical agreement.

## 5. Audit Level (highest level whose requirements are met)
- A0 SUPPLIED — supplied record and source; no independent verification.
- A1 DIRECT — inputs identified, calculation reproduced, compared with supplied result.
- A2 DERIVATION — A1 plus reconstructed derivation and consistency check.
- A3 INDEPENDENT CROSS-CHECK — A2 plus a materially different verification route.
- A4 EXHAUSTIVE FINITE — every element of a completely defined finite domain checked.
- A5 DEPENDENCY — all material upstream/downstream dependencies audited, including the effect of
  changing or invalidating them.
- A6 REPRODUCIBLE — the complete audit reproducible from available materials.

An audit level describes the extent of verification, not the truth of the claim.
- A4 records DOMAIN, DOMAIN SIZE, CHECKED, MISSED, EXCLUDED CASES and requires CHECKED = DOMAIN SIZE,
  MISSED = 0; never for infinite, unspecified, sampled or incompletely enumerated domains.
- A5 records DEPENDENCY INVENTORY, UPSTREAM VERIFICATION, DOWNSTREAM CONSEQUENCES, SENSITIVITY TO
  DEPENDENCY CHANGES, UNRESOLVED DEPENDENCIES.
- A6 records SOURCES, DATA, SOFTWARE OR ENVIRONMENT, FORMULAS OR ALGORITHMS, INPUTS, PARAMETERS,
  PRECISION, ROUNDING RULES, EXPECTED OUTPUTS, REPRODUCTION INSTRUCTIONS, LIMITATIONS.
Audit level and proof status are independent (A2 + PROVED, A4 + COMPUTATIONALLY VERIFIED,
A5 + OPEN, A6 + DISPROVED, ...).

## 6. Computation and Numerical Verification
For every numerical result record EXACT VALUE, NUMERICAL VALUE, PRECISION, ERROR OR TOLERANCE,
ROUNDING RULE, VERIFICATION METHOD, UNITS. Keep the exact expression primary; never replace it with
a decimal; never infer equality from numerical closeness without a bound or exact argument.
Verify every material operation (arithmetic, factorization, modular arithmetic, powers, roots,
determinants, matrix operations, trace, characteristic polynomial, eigenvalues/vectors, rank,
sign, ordering, comparison, rounding, precision, set membership, permutation enumeration,
counting, indexing, domain restrictions, unit conversion). Record stability, overflow/underflow,
cancellation, convergence and stopping criteria, and whether displayed digits are justified.

### Closed sequences and wrap transitions
- An N-cycle has N distinct vertices and N directed edges.
- A repeated initial node shown only to display closure is not a second state.
- Aggregates (sums, moments, parity counts, coordinate totals, drift) count each distinct state once.
- Nonzero drift caused solely by repeating the initial node is a closure-counting error.
- State indexing conventions explicitly (vertices, edges, or displayed entries).
- For the 2-digit cycle 12 23 ... 89 91: 9 nodes; eight steps of -1 and one wrap of +8; total 0.
  Appending 12 again adds a spurious -1.
- For any cycle whose nodes are (x, sigma(x)) for x running over one cycle of a permutation sigma of
  the digits, the drift sum is 0 (the left and right columns hold the same digits).
- Any discrepancy is a contradiction or unresolved dependency until resolved; record whether it
  comes from arithmetic, indexing, endpoint duplication, a wrong transition rule, or a domain
  mismatch.

## 7. Proof Status (exactly one)
DEFINED, PROVED, CONDITIONALLY PROVED, DISPROVED, COMPUTATIONALLY VERIFIED, COMPUTATIONALLY
SUPPORTED, NUMERICALLY VERIFIED, OPEN, UNVERIFIED. Apply scope before status; use the weakest
applicable status when uncertainty remains.
- AUDIT LEVEL = how much verification was performed; VERIFICATION MODE = how evidence was obtained;
  PROOF STATUS = what the mathematics establishes; OBJECT CLASSIFICATION = what kind of record it is.
- A6 does not imply PROVED; COMPUTATIONALLY VERIFIED does not imply THEOREM; THEOREM implies PROVED.
- Restricted evidence does not imply an unrestricted claim; failed verification does not imply
  DISPROVED; an unresolved material dependency blocks a fully established status unless
  independence is shown. DISPROVED requires an established valid disproof.

## 8. Search and External Work
Keep search separate from verification. A source report is evidence of what the source states,
not proof that it is correct. No match is not evidence of novelty, originality, truth or
nonexistence. Record SEARCH QUERY, DATE, SEARCH SCOPE, SOURCES, RELEVANT RESULT, MATCH TYPE
(EXACT MATCH / EQUIVALENT / RELATED / NO MATCH), SOURCE RELIABILITY, INDEPENDENT CHECK,
IMPLICATION FOR CURRENT WORK. If not performed: SEARCH STATUS: NOT PERFORMED, with the reason.
Downgrade conclusions that depend on inaccessible or incomplete sources.

## 9. Automated Agent Rules
- Compute before declaring a decidable claim incorrect; if computation is impossible, UNVERIFIED
  with the reason. Missing evidence is not DISPROVED; computation is not proof.
- Preserve exact mathematics over decimals. Track dependencies, assumptions, conventions, domains.
- A4 / EXHAUSTIVE-FINITE only with CHECKED = N and MISSED = 0.
- Do not manufacture, simulate, or repeat work without stating reason, method and scope.
- Report contradictions explicitly; never overwrite earlier results.
- Do not infer causation from coincidence, correlation, numerical proximity or temporal order.
- Separate mathematics from commentary, interpretation, speculation and source claims.
- Apply scope before status; use the weakest sufficient claim; preserve provenance.
- Exclude duplicated endpoints from closed-sequence aggregates; recheck every wrap transition.
- Distinguish a proof of an algorithm's output from a proof of the claim it investigates.
- Do not claim reproducibility without the materials; do not claim independence for a cross-check
  that reuses the same input, code path, assumption or source.
- Record failed checks, omitted cases and limitations. Expose unstated conventions and test whether
  alternatives change the conclusion. Rewrite conclusions at the weaker scope the evidence supports.
- Consistency pass before finalizing; never use a stronger label because it is rhetorically
  convenient.

## 10. Reporting
Final consistency check: the summary must agree with the record, else use the weaker status and
record the conflict. End each audit with ID, STATEMENT, OBJECT CLASSIFICATION, AUDIT LEVEL,
VERIFICATION MODE, PROOF STATUS, SCOPE, EXACT RESULT, COMPUTATIONAL RESULT, DEPENDENCIES, EVIDENCE,
REPRODUCIBILITY, LIMITATIONS. Canonical one-line summary:

    [ID] [OBJECT CLASSIFICATION] | [A-LEVEL] | [VERIFICATION MODE] | [PROOF STATUS] | [RESULT] | [EVIDENCE]

Worked example (EX-001): "For the integers 2 and 3, 2 + 3 = 5" -- IDENTITY | A3 | DIRECT-CALCULATION,
INDEPENDENT-CROSS-CHECK, REPRODUCIBLE | PROVED.

Rule order: specific over general; scoped over unscoped; prohibitions over permissions; explicit
evidence over unsupported inference.
