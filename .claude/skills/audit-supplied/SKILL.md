---
name: audit-supplied
description: Audit an analysis someone hands you — a document, another model's output, a collaborator's write-up, a posted claim. Use whenever a block of results arrives to be checked, accepted or built on. Reproduce every number first, then separate what is forced from what is contingent, then check that each comparison uses the right null, then report what is correct before what is wrong. Wrong baselines are the commonest defect and they invert the sign of an effect rather than shrinking it.
---

# audit-supplied

Reproduce, then classify, then check the null, then report.

## 1. Reproduce every number

Recompute independently before commenting on anything. Say so plainly when
they all match — that is information, and it earns the corrections that
follow. A supplied prime-gap analysis reproduced to the digit: 664,579
primes, 664,566 gaps, mean 15.047, QR 290,196 against NR 374,150. All of it
correct. Two of its three conclusions still used the wrong null.

## 2. Separate forced from contingent

For each claim ask whether it could have come out otherwise.

- **forced** — true by definition, or by a one-line identity. Report as
  such: "the collapse is the subgroup, not a finding."
- **contingent** — could have failed. This is the only kind that can be
  evidence, and it gets a grade (selectivity, n, pre-registered or not).

A claim can be arithmetically correct and carry no information. Both halves
need saying.

## 3. Check the null, not just the arithmetic

**This is where most real errors are.** A statistic compared against the
wrong baseline reads backwards.

> "orbit self-transitions 0.0577, under the uniform 1/12 = 0.0833 — a
> prime's successor prefers a different orbit."

The baseline is not 1/12. orbit(p) = orbit(p+g) requires 1 + g/p in the
order-3 subgroup, which for fixed g pins p to exactly 2 of 36 residues. The
null is **1/18 = 0.0556**, and the observed 0.0577 is a **3% excess**, not
a 31% deficit. The sign of the effect inverts.

Derive the baseline from the structure. Never assume uniform because the
categories look symmetric.

## 4. Check whether the statistic is a restatement

If a quantity is a deterministic function of another already reported, it
carries no new information. χ(g) over prime gaps is the gap histogram
re-weighted by a fixed sign — gap 6 alone contributed 119% of the excess,
because the commonest gap happens to be a non-residue. That is one sentence
about 6, not a fact about consecutive primes.

## 4a. Reconstruct unlabeled lines

When a line of supplied output has no stated origin, find the sequence that
produces it exactly before judging it. Try the obvious variants (wrap a digit,
hold a digit, reduce mod 10 / 9 / 7) and assert the one that reproduces every
entry. Say if more than one reading fits.

Example (2026-10-02, `math/theorems/ap_147_step20_audit.py`): output for the
progression 147, 167, 187, 207 included "alt diffs [20, 20, -80, 20, 20]"
with no definition. It is the difference list of 147, 167, 187, 107, 127, 147
-- hundreds digit held at 1, tens digit taken mod 10; the -80 is the wrap
8 -> 0 (+20 - 100). Asserted, not described.

## 5. Report in this order

1. what reproduces — all of it, explicitly
2. what is forced — with the one-line reason
3. what the wrong null was — with the right one and the corrected sign
4. what stands as a genuine result — with its grade

Never lead with the correction. Leading with what is right is both accurate
and what makes the correction land.

## Wording

State the defect and the repair in the same breath, with no verdict on the
author. "The pair (12, 33) mixes levels — 12 is a road residue, 33 a stack
sum" is a correction. "This is wrong" is not.

## Audit the mathematics only (owner, 2026-10-03)

"Do you think I listen to algorithms when they ramble on about anything but math?"
Supplied text from other assistants comes with openers ("You are completely right"),
flourishes ("the DNA of the universe") and closing questions. The owner takes only the
mathematics from it. Check every mathematical claim; do not grade or report the rhetoric.
Example that exposed it: prime_digital_root_supplied_audit_2026_10_03.py item D6 audited
the opener instead of the math.
