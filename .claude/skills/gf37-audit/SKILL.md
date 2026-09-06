---
name: gf37-audit
description: Run METHOD.md's fixed 10-step sequence and CLAUDE.md's standing analysis on any number or list of numbers. Use whenever a new number enters the work — a constant, a date, a seed, a factor, a decimal block — before drawing any conclusion about it. Reports residue, named sets, orbit and position, Z/12Z class, antipode, decimal block, digital root and basin, modular structure, primality profile including twin/cousin/sexy/Sophie-Germain, plus the RH, 1/137 and Rule-30 checks. Also prints the forced facts that carry no information so they are not mistaken for findings.
---

# gf37-audit

Runs the fixed sequence. No step skipped, no conclusion before the sequence finishes.

```
python3 .claude/skills/gf37-audit/audit.py 246
python3 .claude/skills/gf37-audit/audit.py 819 1221 137
```

## What it reports

Steps 1–6 of METHOD.md, then the standing analysis from CLAUDE.md, then a
list of facts about the number that are **forced** and therefore carry no
information — orbit membership, 137-map preservation, factorization
agreement on class and digital root, and the decimal block.

## Reading the output

The residue, orbit, class and DR are the content. Everything under
"forced facts" would be true of any number in that residue class and must
not be reported as a discovery.

If the number is SEAM (37 | n) there is no orbit and no class. SEAM is the
rotation axis, not a gap in the structure (T302).

## After the audit

Run `forced-check tier` on any property you intend to claim, and
`miss-test declare` before testing it.
