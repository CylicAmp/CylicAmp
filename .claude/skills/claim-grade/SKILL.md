---
name: claim-grade
description: Grade how strong a correspondence claim actually is, before it gets written down as a result. Use whenever a claim says one thing "is" another — an orbit is a curl, a CA rule is a Laplacian, a protocol is Stokes, a residue pattern is a divergence, a map is functorial — or whenever the word "structural" is about to carry weight. Applies the four cuts of T305 in order (literal vs structural, correspondence level 1/2/3, native vs correspondence rigor, Phi vs functor) and reports the weakest cut, which is the grade. Separate from forced-check (which grades scope) and miss-test (which grades falsifiability); those three axes are independent and this one must not be substituted for either.
---

# claim-grade

A claim that two things correspond is graded by four cuts. They nest. The
weakest one you fail is the grade.

    literal / structural       identity of objects vs identity of roles
            |
    level 1 / 2 / 3            strength of the map between domains
            |
    native / correspondence    where that strength is being claimed
            |
    Phi / functor              which kind of Level-2 map, if you are at Level 2

## Run it

```
python3 claim-grade/grade.py                  # the checklist, blank
python3 claim-grade/grade.py --examples       # the graded claims from T305
python3 claim-grade/grade.py --check-eca 30   # is rule N the GF(2) Laplacian?
python3 claim-grade/grade.py --axes           # show the three axes are independent
```

`--check-eca` is the worked case and the pattern to copy: it does not argue
about roles, it decides. Over GF(2), `u[i-1] - 2u[i] + u[i+1] = u[i-1] + u[i+1]`
because `-2 = 0`, and exhaustive search over all 256 elementary rules finds
exactly one match, rule 90. Rule 30 is not it and is not even linear.

## Cut 1 — literal or structural

**Literal**: the same object appears on both sides, or a defined
discretization of it. **Structural**: only the *role* is shared.

Use "structural" for one thing only — shared role, not shared operator. If it
is being used for "not literal", or "Level 1", or "has structure", the word is
carrying four jobs and the sentence is unreadable.

Before grading a claim as structural, look for the literal object. If it
exists and is a *different* object, the claim is decided, not a matter of
taste. That is what rule 90 does to "rule 30 is the discrete Laplacian".

## Cut 2 — what level

| Level | Claim | You must produce |
|---|---|---|
| 1 structural analogy | same role | the role, named |
| 2 formal correspondence | a map Φ | objects each side, and what identity, inequality or diagram Φ preserves |
| 3 theorem | a proved implication | hypotheses, conclusion, and the failure mode when a hypothesis is dropped |

Level 2 means only: Φ is specified and a named relation survives it. It does
not yet mean functor.

## Cut 3 — native or correspondence

**Native**: how strong is the target theory on its own ground.
**Correspondence**: how strong is the identification.

These diverge, and a mature target does not upgrade the map. "Cryptography is
rigorous, therefore the Stokes analogy is a theorem" is what this cut blocks.
State which one a strength claim is about, every time.

## Cut 4 — Φ or functor

A functor needs categories C and D named, and preservation of identities and
composition. A graph cut is a Level-2 Φ and not a functor. A Galois connection
is a Level-2 Φ and not a functor. "Functorial" without C, D and F written is
still Level 1; it is not a synonym for "precise".

## State the scope

A decision inside a scope licenses nothing outside it. Rule 90 is Δ over GF(2)
for nearest-neighbour ECA on a line or cycle — not the Hodge Laplacian
dδ + δd, and not Δ over ℝ. Write the scope down with the grade.

## Do not collapse the axes

    axis                    grades                              lives in
    Tier A/B/C              scope of a number or property       forced-check
    correspondence L1/2/3   strength of a map between domains   this skill
    test can fail           whether a measurement is operational miss-test

A Tier C property can still be a Level 1 correspondence. A test that can come
back negative can still be measuring a role rather than an operator. Never let
a Tier stamp upgrade a level, and never report a level in place of a scope.
`--axes` asserts this on the recorded claims and fails if any axis becomes a
function of another.

## The audit test, asked in order

1. What is the local object?
2. What is the compatibility condition or invariant?
3. What global behavior is thereby restricted?
4. Is the claim a shared role, a structure-preserving map, or a proved
   implication — and is that claim about the target, or about the map between
   targets?
