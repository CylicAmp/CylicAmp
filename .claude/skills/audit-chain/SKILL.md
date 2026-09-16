---
name: audit-chain
description: The standing order of work for every result in this project — Find, Check prior art, Reproduce, Test mechanism, Classify dynamics, Test baseline, Prove, Interpret. Use at the start of any new observation, pattern, claim or incoming analysis, and use it to decide which of the other skills to invoke and in what order. Interpretation is the last step, never the first. This chain exists because pattern accumulation and auditable investigation look identical at step one and diverge completely by step three.
---

# audit-chain

The order is the method. Interpretation is last.

```
Find
  -> Check prior art      prior-art
  -> Reproduce            audit-supplied      (if it came from elsewhere)
  -> Test mechanism       forced-check, tier-test
  -> Classify dynamics    finite-dynamics     (if a map is involved)
  -> Test baseline/null   miss-test, audit-supplied
  -> Prove                theorem-build
  -> Interpret            claim-grade
```

## The steps, and what each one kills

**1. Find.** A pattern, a coincidence, a supplied claim. Write it in one
sentence. If you cannot, you do not have one yet.

**2. Check prior art** — `prior-art`. The corpus is 568 files. The Z/12
orbit quotient exists in at least five of them (T118, T138, T200, T285,
T339); the 37/74 split and negation duality exist in
`orbit_negation_duality_gf37` before T331 and T332; Pisano 76 exists in
T141 before T344. Rediscovery is not a failure — **link the existing result
and state precisely what, if anything, is new beyond it.**

**3. Reproduce** — `audit-supplied`. For anything arriving from elsewhere,
recompute every number independently before commenting on the
interpretation. Say plainly when they all match; that earns the corrections
that follow.

**4. Test mechanism** — `forced-check` then `tier-test`. Forced or
contingent, and then: re-run it at other primes and in other bases. A tier
assigned by inspection is a label; a tier assigned by re-running is a fact.

**5. Classify dynamics** — `finite-dynamics`. If a map is involved,
characterise it completely — cycles, transients, sources, in-degrees,
image, permutation status, quotient descent, semiconjugacy — *before*
using any word like attractor, collapse, lock or terminal.

**6. Test baseline/null** — `miss-test`. Derive the reference distribution
from the structure. Declare the miss condition before computing.

**7. Prove** — `theorem-build`. A surviving observation becomes a statement
with hypotheses, a proof, a runnable check, and a falsification criterion.

**8. Interpret** — `claim-grade`. Last. Level 1, 2 or 3, with the grade
written into the record.

## The standing rule

> **Never interpret a deviation until the reference distribution has been
> independently established.**

Otherwise the *direction* of an effect can be wrong, not merely its size.
The concrete case: orbit self-transitions at 0.0577 read as a 31% deficit
against an assumed 1/12, and as a **3% excess** against the correct 1/18.
The baseline is 1/18 because orbit(p) = orbit(p+g) requires 1 + g/p in the
order-3 subgroup, which for fixed g pins p to exactly 2 of 36 residues.
Same data, opposite conclusion.

## The one Tier C fact, and its limit

```
ord_p(10) = 3  =>  10^3 == 1 (mod p)  =>  p | 999 = 3^3 x 37
```

so among primes, 37 is the only nontrivial modulus with order 3 for 10 (at
p = 3 the base collapses to 1). That is a genuine arithmetic statement.

**It does not transfer.** It does not establish significance for any other
pattern subsequently observed at 37. Every such pattern needs its own pass
through step 4. Keeping those apart is the whole job of `tier-test`.
