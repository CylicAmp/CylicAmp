---
name: audit-chain
description: The standing order of work for every result in this project — Find, Check prior art, Reproduce, Test mechanism, Classify dynamics, Test baseline, Prove, Interpret. Use at the start of any new observation, pattern, claim or incoming analysis, and use it to decide which of the other skills to invoke and in what order. Interpretation is the last step, never the first. This chain exists because pattern accumulation and auditable investigation look identical at step one and diverge completely by step three.
---

# audit-chain

The order is the method. Interpretation is last.

> **Auditing tests claims against specified failure conditions. It does not
> assume that a failure exists. A successful audit may leave the claim
> unchanged; a non-applicable test is an outcome, not an omission.**

An audit is a decision procedure, not a defect-finding ritual. A correct
document must have a path through this chain ending in *confirmed*, *not
applicable*, or a bounded assessment. If the chain admits no such path, the
chain itself generates pressure to manufacture a problem, and the output
stops being information.

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

### The same rule pointing the other way

> **"Coincidence" is a claim. It needs the work that "structure" needs.**

Grading a pattern down is not the safe default, and a dismissal is not
automatically the conservative reading. Both directions assert something
about every n you did not check.

The concrete case is T361. Two sequences agree for three terms and then
part. Asymptotics (`d_n ~ -n log n`) prove they separate eventually — and
prove nothing about any particular n, since a sequence tending to minus
infinity may still return to zero finitely often first. Calling the
agreement "a three-term coincidence" on the strength of the asymptotics
alone would have been numerology with the sign reversed.

What licensed the word was a separate finite argument: composite gaps are
at most 2, prime gaps at least 2, so the difference sequence never
increases, so the three zeros are the complete zero set. That is the claim
doing the work, and it is a theorem rather than an impression.

Before writing "just a coincidence", ask which statement rules out
recovery at every later index, and whether it is proved or merely
suggestive. If nothing does, the honest label is "not assessed".

## Audit the summaries too

> **Run the audit chain on summaries, inventories and conclusions with the
> same severity as on the underlying computations.**

An unaudited premise can migrate upward through a record until repetition
makes it look established. It cannot acquire evidentiary status that way,
but it can acquire the appearance of it, and the appearance is enough to
get it cited.

**Worked case.** `T_C(N) << N` entered this record four times. Every single
time:

- it appeared in a **summary paragraph**, never in a computational section
- it appeared inside a **list of things already checked** -- "the framework
  is officially purged", "everything that remains has survived hostile
  auditing"
- it was never accompanied by a definition, at any of the four appearances

Grepping 568 files, the only occurrences of `T_C` are in T357 and T358,
both recording it as undefined and excluded. The 11-compressor that
travelled with it appears nowhere at all.

**The diagnostic signature** of a premise laundering itself upward:

1. it is named rather than stated -- a label, not a formula
2. it appears in conclusions and never in working
3. its status verb escalates -- "proposed", then "retained", then
   "verified", then "survived auditing"
4. it travels in a list with genuinely verified items, borrowing their
   status

**Three statuses, not two.**

```
not assessed  !=  survived  !=  failed
```

Something with no definition cannot survive an audit and cannot fail one --
an audit tests a definition against a computation, and there is nothing to
test. The correct status is *not assessed*, and it must be written that way
rather than folded into either of the others.

When closing a record, list what was verified and what was never eligible,
separately and by name. A shorter list that holds beats a longer one that
does not.

## When nothing fires

Every step above is written as something that kills a claim, which builds
in an expectation that each audit produces a correction. Sometimes none of
them fires. A supplied audit of the pointed MTC on (Z/8Z)^2 — the Weil
representation of SL(2,Z/8Z) and its commutant — went through all eight
steps and came out
with nothing to fix: 13/13 reproduced, no prior art, the structural claims
correctly identified by the document itself as construction rather than
discovery, the analogies explicitly refused in its own text.

**A clean pass is a result. Report it as one.** The failure mode here is
manufacturing a criticism to justify the time spent — reaching for a
quibble, or downgrading something accurate so the audit has an output.
That is the same error as inflating a finding, pointed the other way, and
the rule from the previous section applies: a dismissal is a claim.

What a clean pass should still produce:

- the **tier**, stated — a document can be entirely correct and still carry
  no information about the parameter it is named for
- what was checked that the document did **not** check, if anything. On
  that one it was Burnside pinning the trivial isotypic block, and the
  64-dimensional multiplicities cross-checking the 44-dimensional ones
- the **grade**, which is usually Level 1 for a correct instance of a
  classified family, and Level 1 is not a criticism

## Maintaining this chain

The four rules added on 2026-09-17 — the construction axis in `tier-test`,
the standard-object mechanism in `forced-check`, the clean-pass section
above, and "not applicable" in `miss-test` — were all found by auditing
material that PASSED. None of them had surfaced in months of auditing
things that failed.

That is not a coincidence, and it is the maintenance instruction: **a
failure-oriented corpus hides its own assumptions, and only a successful
case exposes them.** Every rule here was written against a defect, so the
gaps were all in the shape of "what does this say when there is nothing
wrong" — invisible until something with nothing wrong came through.

So: run the chain on material you expect to pass, deliberately and
periodically. Not to find something, but to test whether the chain can
say "nothing to find" in the vocabulary it has. If it cannot say that
cleanly, fix the chain.

## The one Tier C fact, and its limit

```
ord_p(10) = 3  =>  10^3 == 1 (mod p)  =>  p | 999 = 3^3 x 37
```

so among primes, 37 is the only nontrivial modulus with order 3 for 10 (at
p = 3 the base collapses to 1). That is a genuine arithmetic statement.

**It does not transfer.** It does not establish significance for any other
pattern subsequently observed at 37. Every such pattern needs its own pass
through step 4. Keeping those apart is the whole job of `tier-test`.
