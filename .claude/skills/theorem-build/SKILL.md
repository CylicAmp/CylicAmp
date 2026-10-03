---
name: theorem-build
description: Build and commit a new numbered theorem in the CylicAmp repository end to end. Use when a verified result is ready to become a theorem file. Runs the audit, applies the miss-test and forced-check screens, writes the theorem with assertions that fail loudly, runs it, and commits with the repository's message format. Enforces METHOD.md's rule that a theorem must carry a runnable computation, a failing-loud assertion, a connection through 37, and a stated falsification criterion.
---

# theorem-build

The pipeline from a verified result to a pushed theorem.

## Before writing anything

1. `gf37-audit` every number involved.
2. `miss-test declare` the claim and its miss condition. If no outcome
   counts as a miss, stop — there is nothing to record but the vacuity.
3. `forced-check` for partition, homomorphism, tie, definition.
4. `forced-check tier` — Tier A, B, or C.
5. Name the block: Use 1 (evaluate Phi_3) or Use 2 (quotient to Z[omega]).

## File requirements

`math/theorems/theorem_NNN_<slug>.py`, and it must have all four:

- a computation that runs independently
- assertions that fail loudly on a wrong claim
- a connection through 37, stated as arithmetic
- a falsification criterion written in the docstring

Assert the numbers, not just return them. A count quoted in prose but not
asserted will drift — that is how "160 factor pairs" reached a commit
message when the true figure was 32.

## Structure

Docstring states the result, the mechanism, and what would falsify it.
Then verification functions, each asserting. Then `run()` printing the
table. Then `if __name__ == '__main__': run()`.

Every claimed count, ratio and chi-square goes inside an `assert`.

## Negatives

A falsified hypothesis stays in the file with the numbers that killed it,
as in T290 and T302 Part 4. State the miss condition, the result, and
`VERDICT: FALSIFIED`. Do not delete it.

## Corrections

When a committed theorem turns out wrong, add a correction section naming
what was withdrawn and why, and tighten the assertions so it cannot recur.
Do not rewrite history. T237, T300 and T301 carry their corrections in place.

## Commit

Run the file. All assertions must pass. Then commit — no asking — with the
finding in the message, not the process, and end with:

```
Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01Km28W4mnsqabQahvMZU2Wz
```

Push to `claude/add-torus-animation-6Ey5Z`.
