---
name: miss-test
description: Apply the T282 admissibility screen before evaluating any GF(37) claim. Use when about to test whether some number, sequence, constant or construction lands somewhere meaningful in GF(37). Forces a miss condition to be declared in advance, then measures whether that condition could actually fire — sweeping a predicate over F_37* to get its selectivity in bits, or chi-squaring a distribution over the 12 orbits to see whether any orbit is genuinely distinguished. A test that cannot come back negative is not a test.
---

# miss-test

The screen from T282. State the miss condition first, then compute.

```
python3 .claude/skills/miss-test/misstest.py declare "<claim>" "<miss condition>"
python3 .claude/skills/miss-test/misstest.py sweep "pow(x,3,37)+5" qr
python3 .claude/skills/miss-test/misstest.py orbit-uniform '{"IC":3,"SEED":2}'
```

## declare

Prints the five questions that must be answered yes, and the known vacuous
patterns. Run this **before** the computation, not after.

## sweep

Takes a predicate over `x` in F_37* and reports what fraction passes, the
bits a hit would carry, and whether the hit set is a union of whole orbits
(which is real structure, cf. T287).

Domains: `qr`, `nqr`, `seam`, `prime`.

## orbit-uniform

Chi-squares a distribution over the 12 orbits. `chi^2/df` near or below 1
means no orbit is distinguished and naming one is post-hoc selection.
This is what settled the CAS_EXT question in T302 Part 4.

## When a test fails

Record it. T290 and T302 keep their falsified hypotheses in the theorem
file with the numbers that killed them. Dropping a miss is how a body of claims
stops being testable.

## Grammar searches: coverage is not expression count

When a "finding" is an expression over given inputs that equals a target,
`|G|` — how many expressions were searched — measures nothing. The evidential
quantity is how much of the output universe the grammar's image covers.

    c = |im(G; inputs)| / |U|        s_image = -log2 c

This is the **uniform-image model**: it assigns equal probability to every
distinct reachable value. Name it that way, because it is not the only
option. If the grammar carries a prior over expressions, multiplicity matters
and the right meter is

    s_syntax(t) = -log2 sum{ P(e) : e(inputs) = t }

Neither substitutes for the other. Report which one you used.

`misstest.py grammar` computes the uniform-image version.

### MDL: the length bound

`L(e) >= log2|G|` holds only for a fixed-length code. Under a general prefix
code, Kraft's inequality `sum 2^-L(e) <= 1` permits simple expressions to be
shorter — lengths [1,3,4,4,4,4,4,4] over |G|=8 sum to exactly 1, and the
shortest is 1 < log2(8) = 3. The rigorous form is

    L(e) = -log2 P(e)     for the chosen coding prior

which strengthens rather than weakens the discipline: a short expression earns
evidential privilege only if the prior that made it short was fixed BEFORE the
target was seen. Choosing the code after seeing the answer is the same error
as choosing the expression after seeing the answer.

### Look-elsewhere, and why the union bound is the wrong tool here

For T independent pre-named targets at coverage c, `P(>=1 hit) = 1-(1-c)^T`.
But post-hoc targets are usually algebraically dependent — in the worked case
444 = 183+261 and 78 = 261-183, so four "hits" carry two degrees of freedom.
Do not pretend independence, and do not settle for the union bound
`P(union) <= sum P(E_i)`, which here returns a vacuous 0.80.

Compute the joint event directly: draw random targets from the null and count
how often the whole fit exists. In the worked case that is 0.34 (1.55 bits)
against a union bound of 0.80 — the exact rate is lower because the two
expressions must additionally share parity for the derived halves to be
integral. The constraint structure is part of the null.

### A closed-grammar MISS is stronger than its self-information

The asymmetry matters. If the grammar and evaluation are frozen and the
enumeration is exhaustive, and the target is not in the image, then

    P(target | "the rule lies in G") = 0        the hypothesis is FALSIFIED

regardless of how unsurprising a generic miss would have been. So a negative
result should be reported as `C not in im(G; A,B)` for a named frozen G — a
theorem about that finite hypothesis class — not as "N expressions searched."
The count is the weakest part of the claim; the closure is the strong part.

### The chain that is not implication

    correct arithmetic  =/=>  selective evidence  =/=>  mechanism

An identity can be exact, verified, and worth nothing evidentially, if the
expression was chosen after the target was exposed. The only repair is a
frozen out-of-sample test: fix the exact formula — no alternative constant,
sign, modulus, permutation or replacement target permitted afterwards — then
evaluate it on a new tuple. Failure rejects it; success is real evidence.
