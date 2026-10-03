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

## The labels are names, not concepts

The twelve orbit names are labels for the twelve cosets of
`<10> = {1,10,26}` in `F_37*`. Each has an exact mathematical designation
— its element set, and its index `j` in the quotient `F_37*/<10> = Z/12`
(T339), where `j` is the power of the primitive root 2 landing in it:

```
j   0   1      2   3     4       5    6     7     8  9  10     11
  IC DARK_A  C3 TESLA SA_ST_A SEED NEG_H NQR17 D7 C9 SA_ST_B CAS_EXT
```

SEAM is the class `{0}`, outside `F_37*` entirely.

Use the label for indexing and the designation when the claim depends on
what the set actually is. A name carries no mathematical content — where a
result turns on structure, cite the set or the index, not the label. Names
like SOVEREIGN, HEARTBEAT and SCALAR_137 elsewhere in the corpus are the
same kind of thing, and the branch `signature-obfuscation-audit` renames
them to `f26`, `order-3 cycle under f(n) = 26n mod 37`, and `26`.

## After the audit

Run `forced-check tier` on any property you intend to claim, and
`miss-test declare` before testing it.
