---
name: search-bounds
description: Turn an enumeration into a COMPLETE search by bounding the object instead of the loop, and report coverage per branch rather than globally. Use whenever a search is about to be reported as evidence — before writing "no solutions found to B". Bounding the cycle minimum took the T428 parity-word sieve from L<=16 by brute force to L<=24 complete; quoting one coverage figure across five branches with five different bounds overstated the weakest by four orders of magnitude in the k=5 layer. A search is never a proof, and the ledger row must say which it is.
---

# search-bounds

Bound the object, not the loop. Then state the bound per branch.

## The move

Brute force enumerates the search space and stops when it runs out of time,
so the result is "nothing below B". Bounding the object instead gives a
theorem of the form *any solution must satisfy X <= B*, and then checking
every candidate below B is **complete** — no case is skipped, and the phrase
"searched to B" changes meaning entirely.

Worked case, T428. Enumerating parity words dies around L = 17, since 2^24
words per multiplier is out of reach. But for each (L, a) with
D = 2^L - m^a > 0, a two-line DP gives the exact maximum of B_sigma over
placements, so any positive cycle has `x = B/D <= Bmax/D`. Maximising over
all (L, a) with L <= 24 gives one number:

    m = 3   x <= 3018      m = 5   x <= 18510     m = 7   x <= 14398

and testing every odd x below that is complete for **all** words of length
<= 24, because every cycle has a minimum element. 16.7M words per multiplier
became a few thousand direct tests.

## Run it

```
python3 .claude/skills/search-bounds/ledger.py --new "k=5 odd, shape C1" 5000 6e14
python3 .claude/skills/search-bounds/ledger.py --show
```

## Procedure

1. **Name the invariant** every solution must carry: a minimum element, a
   smallest prime factor, a least index. It must exist for every solution.
2. **Bound it** from the equation. Usually one side is maximised by a DP or
   a crude inequality; crude is fine, the point is a finite number.
3. **Test every candidate below the bound.** Now the search is complete for
   the stated range of the *parameter*, not of the loop.
4. **Record the bound per branch.** Different branches have different
   bounds; there is no single coverage figure.
5. **Write the ledger row as SEARCH or PROOF, never in between.**

## The coverage trap

The k=5 layer has five live shapes. Their bounds were q <= 5000 (two of
them), p < 4000, p < 400, and (p,q,r < 200, k <= 200). In terms of n those
are roughly 6e14, 1e14, **2.6e10**, and 1e18. Quoting "n <~ 6e14 for the
layer" — one branch's figure — overstated the weakest branch by four orders
of magnitude.

> State the bound of the WEAKEST branch, or state all of them. Never the
> best one.

## Vocabulary, kept straight

- **"no solutions found to B"** — a search. Belongs in the open column.
- **"complete for L <= 24"** — a bounded proof. Every case below the bound
  is checked, and the bound is derived, not chosen.
- **"impossible"** — a proof with no bound at all.

T245's ledger uses all three and labels each row. A row that reads
"IMPOSSIBLE by proof" next to a row that reads "no solutions found up to
5e8" is doing its job; a table that lets one bound cover seven rows is not.

## What it cannot do

It cannot bound an object that is not bounded — the non-periodic branch of
a Collatz-like map has no cycle equation, so no minimum to bound, and no
amount of searching touches it. When the invariant does not exist, say so
and leave the row open rather than reporting the largest B you reached.
