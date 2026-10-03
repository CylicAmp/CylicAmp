---
name: case-tree
description: Branch a problem into cases and prove the branching is COMPLETE before killing anything. Use whenever a proof splits on the shape of an object — which divisor is third smallest, which parameter is even, which prime divides. Census the shapes that actually occur first, by machine, then branch; a hand-built tree missed three of twelve shapes in the k=5 layer of T245 and the reduction it claimed was not established. The census is the whole skill: killing branches is easy, enumerating them is where trees fail.
---

# case-tree

Enumerate the branches by machine before you kill any of them.

## Why this exists

A supplied nine-branch tree for the k=5 divisor-square-sum layer reduced the
problem to "two live families". A census of the shapes that actually occur
found **twelve**, not nine. The three unlisted ones were not rare:

| shape | occurrences, n <= 300000 |
|---|---|
| (1, p, q, pq, q^2) | 9972 |
| (1, p, q, r, s) | 1848 |
| (1, p, q, r, p^2) | 1044 |

Every kill in that tree was correct. The conclusion survived, because the
three missing branches turned out empty when searched. But the *reduction*
did not: "two branches survive" was false, five did. A tree is only as good
as its enumeration, and enumeration is the step that gets eyeballed.

## Run it

```
python3 .claude/skills/case-tree/census.py --divisor-shapes 5 300000
python3 .claude/skills/case-tree/census.py --divisor-shapes 6 200000
```

## Procedure

1. **Define the shape function.** One map from an object to a finite label:
   the cycle type, the symbolic form of the first k divisors, the parity
   vector. It must be computable and total.
2. **Census it by machine** over a range wide enough that rare shapes appear.
   Print the count per shape. A shape with one occurrence in your range is a
   warning that the range is too small, not that the shape is negligible.
3. **Diff the census against your hand-drawn tree.** Name every shape in the
   census that your tree does not list. This step is the skill.
4. **Only now kill branches**, one argument each, and say which of parity,
   mod 4, mod 8, ordering or size does the work.
5. **Report live branches with their own bounds.** Different branches get
   searched to different depths — see `search-bounds`. One global coverage
   figure across branches with different bounds overstates the weakest.

## What a kill must contain

A branch is closed when a contradiction is exhibited, not when it looks
unlikely. Three kills that hold up, from T245:

- **ordering**: 8 | n puts a divisor at 8, so d4, d5, d6 < 8, but (4,8)
  holds only 5 and 7 — two slots, three divisors.
- **divisibility**: d3 | n and d3 | 5 + d3^2 give d3 | 5, so d3 = 5, so
  n = 30 — whose divisors are 1,2,3,5, making d3 = 3, not 5.
- **size**: n >= pqr > pq^2 while n = 1+p^2+q^2 < 3q^2 forces p < 3.

A kill that ends "no solutions found" is not a kill. That is a search, and
it belongs in the live column with its bound attached.

## What it cannot do

The census proves your tree is incomplete; it cannot prove it is complete.
Shapes that first occur above your range are invisible. Say the range with
the result, and prefer a shape function whose image is provably finite —
then a census that stabilises is an argument, not just evidence.

## Closing a branch from a superset (added 2026-10-02)

When the census cannot certify the shape list, enumerate a PROVABLE SUPERSET
(order ideals + log-space LP with non-strict inequalities, in-box ghosts
only), then run cheap filters in sequence and hand-kill what is left:
shape-level congruence -> size LP (lcm <= n < k d_k^2) -> strictness (LP
solutions that sit on a tie between an odd and an even monomial) -> finite
check where the LP bounds every prime. Negative control: every shape a
census realizes must be inside the superset.

Example: T245 k=8 case B, `math/theorems/k8_case_b_complete.py` with
`tools/k8_caseb_shape_enumerator.py`: 304 -> 122 (labels) -> 38 (mod 8) ->
12 (size) -> 0. Census below 4e5 realizes 33 shapes, all inside. This
closed k=8.

Lower bounds are per branch, and a wrong one is a silent kill. The first k=8
version forced q >= 7, r >= 11 in every shape; in the p = 3 branch the right
bounds are q >= 5, r >= 7, and with them three more shapes survived the size
LP (they then died by 10 | n). Found while reusing the code for k=7, which
closed the same way: `math/theorems/k7_even_complete.py`, 22 -> 5 -> 0.
Derive each bound from the branch's own ordering, and assert the LP's upper
bounds below the brute-force limit instead of quoting them.
