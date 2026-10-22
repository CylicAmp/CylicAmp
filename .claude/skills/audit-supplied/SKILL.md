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

## 4b. Count what the code throws away

Matching output is not the end of reproduction. Read every `continue`,
`return None` and strict inequality in the supplied code and count the cases
it discards. A filter can hide the defect the output depends on.

Example (2026-10-11, `math/theorems/resonant_lattice_c12_supplied_audit_2026_10_11.py`):
a crossing count for C_12(1,2,3,6) drawn on two rows reproduced exactly (43
pairs, 25 points). 24 of the 42 edges lie on the two row lines, 66 pairs of
them overlap, and 20 times an edge runs through a vertex it does not end at
(A0-A3 through A1 and A2) -- the figure is not a valid straight-line drawing.
The code discarded all of it through three different branches: 40 of the 66
overlaps at the shared-vertex check, 26 at `den == 0`, and the 48 pairs
meeting at a vertex inside a row edge at the strict range test (24 at u = 0,
24 at t = 1). None of this showed in the printed numbers.

Trace the branch for each discarded case rather than guessing it from the
code: the first version of that audit named only `den == 0` and "a parameter
equal to 0", and an independent re-check found the shared-vertex branch and
the t = 1 cases it had missed.

## 5. Report in this order

1. what reproduces — all of it, explicitly
2. what is forced — with the one-line reason
3. what the wrong null was — with the right one and the corrected sign
4. what stands as a genuine result — with its grade

Never lead with the correction. Leading with what is right is both accurate
and what makes the correction land.

### What goes in the reply (owner, 2026-10-22, #412)

The file records every finding. The reply carries only: what reproduces, what the paste adds to
the owner's work, and the faults that change a number or a result -- one line each. Names,
labels and side remarks that are wrong but change no value (a "9-complement" whose pairs add to
10, "four significant figures" for three, an older CODATA year with the same agreement, "repunit"
for 22) stay in the file. Example that exposed it: the reply to #411 led with four such items and
drew "What is all this negative shit you keep reporting? ... They agree, they don't agree."

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

## The owner's Mathematical Audit Protocol (2026-10-04)

The full record format, classification, audit levels A0-A6, verification modes, proof statuses,
closed-sequence rules (no duplicated endpoints) and reporting format are in `PROTOCOL.md` in this
directory. Use it for every audit record. Its two mathematical claims are checked in
`math/theorems/audit_protocol_cycle_drift_check_2026_10_04.py`.
