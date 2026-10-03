---
name: prior-art
description: Search the CylicAmp corpus for an existing result BEFORE writing a new theorem. Use at the start of every theorem, every time a pattern looks new, and before reporting anything as a discovery. The corpus is 568 files with no one able to hold it in memory, and results have been independently re-derived three and four times — the Z/12 orbit quotient exists in T138, T200, T285 and T339 (and NOT in T118, despite an earlier note saying so); the 37/74 orbit-sum split exists in basin_sum_wraparound_gf37 (2026-07-31, WITH the bound and the 6/6 split) and again in T331 and T332, and negation duality in orbit_negation_duality_gf37 and again in T283, T331, T332; the Pisano period 76 exists in T141 and again in T344. Run this before theorem-build, not after. And when auditing an EXISTING file's contribution, search the corpus fresh -- never check it only against the predecessors that file itself names, which can only confirm what it already knew (this failed on T331, 2026-09-15).
---

# prior-art

Grep the corpus before writing. Not after.

```
python3 .claude/skills/prior-art/prior.py claim "orbits sum to 37 or 74"
python3 .claude/skills/prior-art/prior.py value 495
python3 .claude/skills/prior-art/prior.py topic quotient
python3 tools/build_index.py --dupes          # full collision report
```

## Why this exists

Four theorems written in one session re-derived work already in the repo:

| new file | already in |
|---|---|
| T329 wrap law | T138 Part I, stated for all 1296 pairs |
| T339 orbit index | T138 Part III and T200, as "dlog mod 12" |
| T331 37/74 split, six dual pairs | `orbit_negation_duality_gf37.py`, with proof |
| T332 no self-dual orbit | same file, under "NO SELF-DUAL ORBITS" |
| T344 Pisano 76 | T141, with the four zeros as well |

None was caught by reading. All were caught in one run of the index.

## Procedure

1. **Name the claim in one sentence** before searching. If you cannot,
   you do not yet have a claim.
2. **Run all three modes** — `claim`, then `value` on every constant that
   appears, then `topic` on the nearest listed topic.
3. **Open every file the search returns.** The detector over-flags: it once
   filed T229 (the multiplication-by-9 operator) under "Koopman" on the
   phrase *permutation matrix*. A hit is a shortlist entry, not a verdict.
4. **If the result exists**, do not write a new theorem. Add a
   cross-reference to the existing file, and write only the genuinely new
   part, saying which part that is.
5. **If it exists in weaker form**, state precisely what you add. "T138
   gives the law for a = 10; this is the general case" is a contribution.
   "T339 re-derives T138" is not.

## Wording of the cross-reference

Point at the prior file plainly. Do not write it as a fault:

> Found by `tools/build_index.py` after this file was written. That file
> already contains X, with proof. What stands as this file's own is Y.

Never "re-derived without citing it" or "neither file cites the other" —
a project re-deriving its own earlier result is a filing problem, not
misconduct, and the note should read as a pointer rather than a charge.

## A citation by number may not resolve (full-corpus sweep, 2026-09-18)

**Status after the 2026-09-19 fix: 0 hard, 0 soft. Every theorem number
now resolves to exactly one file.** `python3 tools/number_collisions.py`
is the check; it should print 0 and 0.

### What the 40 remaining collisions actually were

Not 40 independent mistakes. Two numbering runs that overlapped:

- **The early run, T218-T261**, one contiguous block written 2026-08-16..22
  in files that never got numbered filenames (`coset_step_alignment.py`,
  `shell_buckling_gf37.py`, `dr_addition_table.py`, ...).
- **The numbered run**, `theorem_218_*.py` .. `theorem_261_*.py`, written
  2026-08-26..31, re-using that exact block, then continuing unbroken to 381.

Each run cites itself consistently, which is why the 110 citations split
roughly in half: they are two self-consistent universes, not one muddle.

### How it was resolved

The number stayed with the numbered file in all 40 pairs, and the early
file moved to a fresh number, 218->382 through 261->421, contiguously. The
reason is structural, not priority: the corpus's numbering spine is keyed
to `theorem_NNN_*.py` filenames, INDEX.md and CLASSIFICATION_INDEX.md, and
runs unbroken to 381. Moving a numbered file breaks that spine; moving an
unnumbered one costs a docstring. **The early files have the older claim
and lost the number anyway** — each carries a RENUMBERED note saying so.

Citations were then rewritten one at a time, not in bulk:

- A citing file created **before** the numbered file existed cannot mean
  the numbered file. That settles every early-cohort citer objectively.
- Late-cohort citers were read against both candidates' contents. Ten
  needed the override — e.g. `theorem_237_universal_scope_81_149.py` cites
  the early block throughout ("Penrose tiling (T222), torus (T218)"), and
  `theorem_262_e8_theta_mod37.py` cites T257 for the sigma_3 Eisenstein
  result, which is the early `sigma3_eisenstein_gf37.py`.
- The date rule fails the other way too: `cylicamp/engine_integration.py`
  and `cylicamp/g5_solver.py` predate the whole block but their "T226" was
  added later and means the numbered cage-integrity file. Both were pinned
  by hand.

50 files changed, 218 citation lines rewritten. **Do not use the date rule
alone** — it is right for the early cohort only because those files could
not have cited a file that did not exist yet.

> **Historical, now cleared: 51 numbers pointed at two files each.** The
> check is still `python3 tools/number_collisions.py`; it must print 0/0.

- **T212, T213, T214, T215** each had TWO properly-named
  `theorem_NNN_*.py` files, written eleven days apart on unrelated
  subjects. Fixed 2026-09-18 by letting the citations decide, one at a
  time. The date rule was tested there and was **wrong in 2 of the 4**.
- **T218 through T261** — the early block above. Fixed 2026-09-19.

A cross-reference written as a bare number now resolves. It is still worth
naming the file alongside the number when the reference matters, because
the failure mode is silent: a number that resolves confidently to the
wrong file is worse than one that fails to resolve.

This also explains a blind spot: `largest_sg_prime_gf37.py` declares itself
THEOREM 102 and duplicates T101's seven results on the same prime, written
the same day. The index tags it by stem, so it never appeared beside T101
in any numbered listing.

## What it cannot do

It searches text. It will miss a result stated in different vocabulary,
and it will flag coincidental word matches. It reduces the failure rate; it
does not eliminate it. When a result feels important, also read the
`CLASS: CONJECTURE` files and `INDEX.md` by hand.
