---
name: census-saturation
description: Test whether a shape census has stopped growing before quoting it as covering a branch. Use after any machine census of divisor prefixes, orbit shapes, parity patterns or case trees, and ALWAYS before writing that a shape list covers its branch. A census to 600000 gave 83 shapes in the k=9 odd branch of T245; 95 existed by 800000 and 101 by 1.2e6, still climbing, so the sweep covered the shapes seen below the bound and not the branch. The complement of case-tree: that skill says census by machine, this one says check the census is finished.
---

# census-saturation

`case-tree` says enumerate the shapes by machine before branching. It does
not say verify the enumeration stopped. This is that step.

```
python3 .claude/skills/census-saturation/saturate.py <census_script> B1 B2 B3 ...
```

## The failure it catches

T245, k=9, n odd. Shapes first realised at or below B:

    57 @150k   69 @300k   76 @450k   83 @600k   95 @800k   98 @1M   101 @1.2M

The list was quoted at 83 as covering the branch. It was still climbing.
Every shape swept came back EMPTY, so nothing looked wrong — the defect was
in coverage, not in results, and no amount of further sweeping would have
revealed it.

## Why odd branches leak and even ones do not

An odd n has no small even divisors padding the prefix, so the k smallest
divisors can carry many distinct primes — and a shape with t distinct primes
is not realisable below roughly their product. `1 3 p q r s t 3*p 3*q` first
occurs at 969969 = 3*7*11*13*17*19. Even branches cap t and saturate fast.

Measured across T245: k=7 flat at 209; k=8 4|n flat at 85 from 400k to 2M;
k=8 n odd 197 -> 272 and rising; k=9 odd 83 -> 101 and rising.

## Procedure

1. Run the census at several increasing bounds, not one.
2. Plot count against bound. Flat over at least a 3x range = saturated.
3. Still rising = the list is a sample. Say so in the ledger row, and do
   NOT write that the shapes cover the branch.
4. If it does not saturate, build the shape list from a structural bound
   instead of a census (see tools/k9_odd_shape_enumerator.py, which uses
   t <= 9 - c from the count lemma to make the set finite).
5. Record the bounds tested and the counts, not just the verdict.

## What it cannot do

Flat over the range tested is evidence, not proof. A shape needing six
distinct primes first appears near their product; if that product exceeds
every bound you tried, the census looks saturated and is not. Prefer a
structural bound on the number of primes whenever one is available.
