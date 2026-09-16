---
name: prior-art
description: Search the CylicAmp corpus for an existing result BEFORE writing a new theorem. Use at the start of every theorem, every time a pattern looks new, and before reporting anything as a discovery. The corpus is 568 files with no one able to hold it in memory, and results have been independently re-derived three and four times — the Z/12 orbit quotient exists in T138, T200 and T339; the 37/74 orbit-sum split and negation duality exist in orbit_negation_duality_gf37 and again in T331 and T332; the Pisano period 76 exists in T141 and again in T344. Run this before theorem-build, not after.
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

## What it cannot do

It searches text. It will miss a result stated in different vocabulary,
and it will flag coincidental word matches. It reduces the failure rate; it
does not eliminate it. When a result feels important, also read the
`CLASS: CONJECTURE` files and `INDEX.md` by hand.
