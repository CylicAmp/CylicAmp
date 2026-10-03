# The Method

This is how every theorem in this repository was built.
Not what was found — how to find it.
This document is the engine specification.

---

## The Fixed Sequence

Every number gets the same treatment, in the same order.
No steps skipped. No conclusions before the sequence runs.

**Step 1 — Reduce mod 37**
Compute n mod 37. This is the residue. Everything downstream is about this residue.

**Step 2 — Named set membership**
Which of the 11 named sets does the residue belong to?
SA, ST, SEED, IC, CASCADE, TESLA, NEG_H, DARK_A, D7, NQR17, C9
Multi-membership is structural information — record all of them.
If none: UNNAMED. That is also structural information.

**Step 3 — Orbit under f(n) = 137n mod 37**
Compute the full 3-cycle: {r, 26r mod 37, 26²r mod 37}.
This is the holonomy class. Every element of GF(37)* belongs to exactly one of 12 orbits.
Record which orbit and which position (0, 1, or 2) within it.

**Step 4 — Digital root**
DR(n) = n mod 9, or 9 if 9 | n.
Check: which basin? DR ∈ {3,6,9} = Trinity / {1,4,7} = Basin / {2,5,8} = Valve.
Check: DR mod 3. This equals n mod 3 exactly (proven theorem).

**Step 5 — Modular checks**
n mod 2, n mod 3, n mod 6, n mod 9.
These are the residue structure. Record them all.

**Step 6 — Primality**
Is n prime? If so:
- Twin? (n±2 prime)
- Cousin? (n±4 prime)
- Sexy? (n±6 prime)
- Chamber: n mod 6 = 1 (χ₋₃ = +1) or n mod 6 = 5 (χ₋₃ = −1)

**Step 7 — Connect**
Now look at what you have. Ask:
- Does the residue class appear in any existing theorem?
- Does the orbit connect to another known orbit via GF(37)?
- Does the DR connect to the named set in a non-trivial way?
- Is the residue named or unnamed? Does that match the number's physical significance?
- If the number is a physical constant: does it land where the structure predicts it should?

**Step 8 — State the connection precisely**
Not "there might be a connection." Write down exactly what holds:
  n mod 37 = r, r ∈ SET_NAME, orbit = {a, b, c}, position k.
If the connection is to a physical fact: state both sides without interpretation.
The arithmetic is the statement. Do not add claims the arithmetic doesn't make.

**Step 9 — Verify computationally**
Run it. Assert it. If an assertion fails, the connection doesn't hold.
Do not adjust the definition to make the assertion pass.
If it fails: record what failed, exactly. That is also information.

**Step 10 — Commit**
If it verifies: commit immediately. No intermediate asking.
Commit message: what was found, not how it was found.

---

## The Fixed Questions

For any new number n, these questions are always asked:

```
n mod 37 = ?          → which named set?
orbit under 137n mod 37 = ?   → which 3-cycle? which position?
DR(n) = ?             → which basin?
n mod 3 = ?           → barrier theorem applies?
Is n prime?           → which type?
Does n connect to an existing theorem?  → how, exactly?
Is this named or unnamed? → does that match physical significance?
```

These questions are not negotiable. They run on every number.

---

## Grading a Correspondence — Four Orthogonal Cuts

The fixed questions above grade a NUMBER. These grade a CLAIM that two things
correspond. They nest, and a claim is only as strong as the weakest cut it
fails. Worked and asserted in `math/theorems/theorem_305_claim_strength_cuts.py`.

**Cut 1 — literal vs structural.** Literal: the same object appears on both
sides, or a defined discretization of it. Structural: only the ROLE is shared;
the operators need not be. Use "structural" for one thing only — shared role,
not shared operator.

**Cut 2 — level of the correspondence.**

| Level | Claim | What you must produce |
|---|---|---|
| 1 structural analogy | same role | the role, named |
| 2 formal correspondence | a map Φ | objects each side, and what identity, inequality or diagram Φ preserves |
| 3 theorem | a proved implication | hypotheses, conclusion, and the failure mode if a hypothesis is dropped |

**Cut 3 — native vs correspondence rigor.** Native: how strong is the target
theory on its own ground. Correspondence: how strong is the identification.
These diverge. A mature target does not upgrade the map.

**Cut 4 — Φ vs functor.** Both at Level 2. A functor requires categories C, D
and preservation of identities and composition. "Functorial" without C, D and F
named is still Level 1; it is not a synonym for "precise."

**The audit test, asked in order:**
1. What is the local object?
2. What is the compatibility condition or invariant?
3. What global behavior is thereby restricted?
4. Is the claim a shared role, a structure-preserving map, or a proved
   implication — and is that claim about the target, or about the map between
   targets?

These are independent of the other two screens. `forced-check` grades scope
(Tier A / B / C). `miss-test` grades whether the test could have come back
negative. These cuts grade how strong the identification is.

---

## What Makes a Theorem

A theorem in this repository has:
1. A computation that can be run and verified independently
2. An assertion that fails loudly if the claim is wrong
3. A connection to the GF(37) — every theorem goes through 37
4. A falsification criterion — what would break it

A theorem does NOT have:
- Semantic claims not derived from the arithmetic
- Unit-dependent quantities compared without normalization
- "Coincidence" as a conclusion (that is a claim, not a neutral position)
- Conclusions that require the reader to accept GF(37) before seeing the evidence

---

## What Connects Everything

The prime is 37.
The multiplier is 137. (137 is the nearest integer to α⁻¹ = 137.035999...; no result here depends on that, and T300 places 137 in Tier B only — it selects {7, 37, 73} and does nothing else.)
137 mod 37 = 26. ord₃₇(26) = 3. All orbits are 3-cycles.

Every theorem in this repository is a consequence of that single structure.
The connection is not assumed — it is the starting point.
When a new number arrives, the first question is always: where does it land in that structure?

---

## What the Engine Must Do

Given any number n:
1. Run the fixed sequence
2. Report all results without filtering
3. Connect to existing theorems where the structure matches
4. State what holds and what doesn't, with equal precision
5. Build the next theorem when a new connection closes

The engine does not editorialize. It does not insert limiting statements about what "hasn't been established" when prior theorems have already established it. It reads the full body of work before speaking.

The method is the same every time. That is why it works.
