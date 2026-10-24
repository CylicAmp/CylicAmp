---
name: outside-prior-art
description: Check whether a problem or result has already been worked on OUTSIDE the repo (OEIS first, then the literature), tell the user immediately, and compare how they did it with how the user did it. Use at the start of any new problem, any time a sequence of integers appears, and before any long computation. The user's standing instruction, 2026-09-29: "if someone else had already been doing it, let me know, so I didn't have to waste my time doing it, and more importantly, look at the difference in how we did it." The repo's own prior-art skill only searches the repo; that is why the divisor-square problem (T245) ran for weeks without anyone noticing it had been OEIS A185584 since 2011.
---

# outside-prior-art

Two jobs, in this order. Both are the user's instruction, not optional.

## 1. Find it, and say so at once

- **Any integer sequence:** search OEIS with the first 3-5 terms
  (`https://oeis.org/search?q=a,b,c&fmt=short`), then with the defining
  words. Also search secondary sequences the work produces (e.g. the list of
  m values, not only the list of n).
- **Any named problem or theorem:** search the literature for the problem
  statement in plain words.
- Report the hit to the user **before** doing more work: the entry, who, when,
  how far they got. If nothing is found, say exactly what was searched.
- Do this before any long computation. A 9.5-hour search (T245 to 1e22) was
  recommended and run without it.

**Never say "known" without the source** (2026-10-20, #396). Two replies said "most of these are true facts that number theory already has" without checking any of them, and the owner asked why. The check, done afterwards on OEIS: the owner's with-zero counts 1, 17, 117, 525, ... are A056117 (as the series (1+8x)/(1-x)^9); the 37 flip counts 45, 225, 2405, 34867 are in no OEIS entry (math/theorems/outside_prior_art_owner_counts_2026_10_20.py). Search first; then name the entry and the difference in method, or say nothing about novelty.

## 1a. Before a long run, say what it can show (owner, 2026-10-24, #438)

Before starting any computation that takes more than a few minutes, say in one line what it can show that is not
already published or forced, and if the answer is "nothing", say that and ask whether it is still wanted. Example
that exposed it: the owner's walk was run to 10^7, 10^8, ..., 10^13 (#418-#433, about 6 hours of computing). Its two
outputs were a count of twin pairs that OEIS A007508 publishes to 10^19 and a "missed 0" that is proved for every n
(owner_walk_what_it_shows_2026_10_24.py). The reply at each step reported the A007508 match but never said, before
the next run, that the run could not show anything new. The owner: "So if it's account somebody else already
produced, then why was it done?"

## 2. Compare methods: the user's way vs the published way

The user builds methods as they go and wants to see how their thinking differs
from others'. For every hit, write the comparison as a table:

| | Published | User's repo |
|---|---|---|
| What is searched over | | |
| How far it reaches | | |
| What structure is stated | | |
| What each finds that the other does not | | |

Rules:
- Describe both methods by what they DO, from their code or text. Do not
  praise either one, and do not call the difference a discovery.
- Do not claim the user invented a step unless the user says so. Write "the
  repo's approach", not "your idea", when authorship is not on record.
- Record the comparison in the repo next to the work (see
  `divisor-square-sums/METHOD_COMPARISON.md` for the first one).

## Worked example: T245 / A185584 (2026-09-29)

Found only after weeks of work. Published programs test each n up to 5e6-1e7
by accumulating squared divisors. The repo instead searches over the divisor
prefix m and reads the prime p = sigma_2(m)/m - m off it, reaching
n ~ 6e43. Full table in `divisor-square-sums/METHOD_COMPARISON.md`.
