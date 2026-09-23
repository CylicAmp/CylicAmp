---
name: dangling-cite
description: Find citations in the corpus that point at theorems which were never written. Use before filing any result that cites a T-number, and periodically across the whole corpus. prior-art guards one direction — re-deriving something that already exists; this guards the other — citing something that never entered the corpus. 46 of the 248 T-numbers cited in CylicAmp file text (19%) refer to theorems with no file anywhere in any branch, mostly the contiguous block T382-T421, and INDEX.md jumps straight from 381 to 422.
---

# dangling-cite

The complement of `prior-art`. That skill stops you re-deriving T138 for the
fourth time. This one stops you citing T397, which does not exist.

```
python3 .claude/skills/dangling-cite/dangling.py
python3 .claude/skills/dangling-cite/dangling.py --file math/theorems/theorem_500_x.py
```

## What it found

Run across the consolidated corpus, 2026-09-22:

    numbered theorem files present : 291  (range 58-430)
    distinct T-numbers cited       : 248
    cited with no file             : 46   (19% of citations)

    isolated : 73 79 81 82 83 84
    block    : 382-421   (forty consecutive)

Worst offenders: theorem_237_universal_scope_81_149.py (8 dangling),
ratio_177_133_identity.py (6), twin_gap_dr_chain.py (6).

These were never written, not lost. `git log --all --diff-filter=A` over all
eleven branch histories returns ZERO additions for any of those paths.

## Why it matters more than it looks

A dangling citation is locally invisible. The citing file runs, its
assertions pass, and the reference reads as support. Nothing fails. The
corpus acquires apparent depth that does not exist, and a later reader
following the chain finds nothing at the end of it.

## Procedure

1. Collect every `T<number>` appearing in file text across the corpus.
2. Collect every theorem number that has a file.
3. Report cited-minus-present, with the citing file for each.
4. For each dangling number, choose one: write it, renumber the citation to
   the theorem actually meant, or strike the citation.
5. Never leave it pending. A citation with no referent is a claim with no
   evidence, which is the defect `forced-check` and `miss-test` exist to stop
   one level down.

## What it cannot do

It matches `T<digits>`. A citation written as "theorem 397" or "the orbit
result" is invisible to it, and a number appearing in prose for another
reason ("T382 was never assigned") registers as a citation.
