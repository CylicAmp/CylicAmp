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
