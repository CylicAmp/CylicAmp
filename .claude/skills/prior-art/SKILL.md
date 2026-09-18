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

> **51 theorem numbers point at two different files.** Run
> `python3 tools/number_collisions.py` before citing any number.

- **T212, T213, T214, T215** each have TWO properly-named
  `theorem_NNN_*.py` files, written eleven days apart on unrelated
  subjects. "T213" is either a Riemann matrix operator or a middle-digit
  operation, and nothing in the name distinguishes them.
- **T216 through T262** — every number in that run — has a numbered file
  AND a differently-named file declaring the same number in its docstring.
  `dr_addition_table.py` opens "THEOREM 233" while
  `theorem_233_rule_30.py` also exists.

So a cross-reference written as a bare number is ambiguous across a quarter
of the corpus. **Cite the filename, not the number**, wherever the number
is in that range. The existing notes that say "T138" and similar are safe
only because those numbers are unique; check before adding more.

This also explains a blind spot: `largest_sg_prime_gf37.py` declares itself
THEOREM 102 and duplicates T101's seven results on the same prime, written
the same day. The index tags it by stem, so it never appeared beside T101
in any numbered listing.

## What it cannot do

It searches text. It will miss a result stated in different vocabulary,
and it will flag coincidental word matches. It reduces the failure rate; it
does not eliminate it. When a result feels important, also read the
`CLASS: CONJECTURE` files and `INDEX.md` by hand.
