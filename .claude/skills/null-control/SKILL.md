---
name: null-control
description: Run a do-nothing implementation through your own check before believing the check. Use whenever a test, screen, assertion or conformance rule reports a pass, and always before recording that pass as evidence. Generalises forced-check's STANDARD OBJECT mechanism from claims to checks — a numerical check that a null implementation also passes confirms the harness, not the mathematics. It diagnosed a specification whose sensitivity rule included the input's own value hash, so every mutation changed the compared projection and a constant-returning implementation passed every test at 0.0 bits.
---

# null-control

`forced-check` asks whether a CLAIM is forced by the construction.
`miss-test` asks whether a TEST can come back negative.
This asks the sharper version: **does your check pass a program that does
nothing?**

```
python3 .claude/skills/null-control/nullctl.py --demo
```

## The mechanism

    real_passes = check(real_implementation)
    null_passes = check(lambda _: CONSTANT)

    null_passes  ->  FORCED, 0 bits, not evidence
    not null_passes ->  CONTINGENT, the check discriminates

## What it caught

A sensitivity contract defined projection equality to include "input-field
references and value hashes". The mutated input's own hash sits inside the
compared projection, so baseline and mutated projections differ for EVERY
mutation, of every dimension, relevant or not. A constant-returning
implementation passed every sensitivity check.

    equality as written (includes value_hash)  null passes  FORCED      0.0 bits
    hashes moved to provenance comparison      null fails   CONTINGENT  1.0 bits

No reasoning about hashes was required to find it. The null control found it
mechanically.

## Why it beats reading the check

A check is read by the person who wrote it, who knows what it is supposed to
test and supplies that meaning while reading. The null implementation
supplies nothing. It is the only reader with no theory of what the check
means.

## Procedure

1. Write the null: same signature, returns a constant, computes nothing.
2. Run the identical check against it.
3. Null passes -> the check is FORCED. Report 0 bits. Fix the check before
   fixing anything else; every result it produced is uninformative.
4. Null fails -> CONTINGENT. Record the classification alongside the result.
5. Apply to assertions too, not only test harnesses. An assertion that holds
   for any input is a comment.

## Companion failure: the accidental null

A check can also be forced by the ENVIRONMENT rather than by its own logic.
theorem_423 asserted exactly one file defines the four-tier ledger. True,
passing, and empty — three other files defining it were on branches the
check could not see. Run the null control after any change to what the check
can observe, not just after changing the check.
