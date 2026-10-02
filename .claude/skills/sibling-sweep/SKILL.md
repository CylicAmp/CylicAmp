---
name: sibling-sweep
description: After fixing a defect in one function, find and test every other copy of that function in the repo. Use whenever a bug is fixed in a helper (is_prime, dr, orbit_of, legendre...) that has been copy-pasted across modules.
---

# sibling-sweep

A fix to one copy is not a fix. This repo has many hand-copied helpers.

## Procedure

1. **Name the defect as a test input.** A concrete value that the broken
   version gets wrong (psi_12 = 318665857834031151167461 for 12-witness
   Miller-Rabin; n = 2..41 for witness = n).
2. **Grep by the defect's signature, then by the function's name.** The
   signature grep (the literal witness tuple) finds exact copies; the name
   grep (`def .*(is_prime|miller|rabin)`) finds variants with different
   constants. Run both: the name grep found `rsa_dr_engine` (witnesses 2..11),
   which the tuple grep missed.
3. **Test every hit by running it,** not by reading it: extract top-level
   functions with `ast`, exec them with a per-file timeout, compare against a
   reference (sympy) on a small range plus the defect inputs.
4. **Account for every file the run skipped** (nested functions, methods,
   name-only matches) by reading them, and list them.
5. **Check whether recorded results move:** run each patched module before and
   after; identical output means no recorded result touched the defect.
   Unseeded randomness makes a diff meaningless -- say so.
6. Record all of it in one asserted audit file.

## Harness pitfalls (seen 2026-10-02)

- `pkill -f name` kills your own shell if the command line contains `name`.
- Exec only top-level Assign/FunctionDef and a module's sieve `for` loop is
  skipped: `crt_emirp_null_model_audit.is_prime(4)` read as wrong. A failure
  that implicates module state is a harness artifact until reproduced by
  running the module itself.
- Trial-division functions time out on 24-digit inputs; send the large
  pseudoprimes only to functions that call `pow(`.

Example: `math/theorems/mr_witness_audit_2026_10_02.py`.
