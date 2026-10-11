---
name: tier-test
description: Decide whether a result is actually about the parameter it is named for by re-running the construction elsewhere. Identify the axis the construction is built on first — primes and bases are this corpus's usual two, but a supplied construction carries its own (for a discrete torus (Z/nZ)^2 it is n). Use on every result before calling it a finding, and always before presenting one as evidence for 37. Complements forced-check, which classifies by mechanism; this classifies by experiment. Four results in one session were presented as discoveries and turned out to hold for every prime congruent to 1 mod 3, carrying no information about 37 at all.
---

# tier-test

A tier assigned by inspection is a label. A tier assigned by re-running is
a fact.

```
python3 .claude/skills/tier-test/tier.py order 10 3    # which primes?
python3 .claude/skills/tier-test/tier.py base          # which bases?
python3 .claude/skills/tier-test/tier.py prime         # the whole table
```

## The test

**Re-run the construction somewhere else.**

### First identify the axis

Primes and bases are this corpus's usual axes because most results here are
built on `p = 37` or on base-10 numerals. They are not the method. The
method is: **find the parameter the construction is actually built on, and
vary that one.**

A supplied construction often carries its own axis, and it is usually named
in the title. Worked case, the pointed MTC on `(Z/8Z)^2` — equivalently the
Weil representation of `SL(2,Z/8Z)`: the axis is `n`, the modulus of the
discrete torus `(Z/nZ)^2`. Re-running the whole thing for
n = 3..12 showed every structural claim — `S'S = I`, `S^2 = C`,
`(ST)^3 = C`, `S_00 = 1/n` — holding in all ten, so none of them says
anything about 8. The specific integers (|SL2| = 384, dim A' = 44, the
twist histogram 20/12, the block type) are that general construction
evaluated at n = 8.

Even the parts that look like they might be special usually resolve into a
rule once the axis is swept: the count of modular twist refinements is 1,
3 or 4 according to whether n is odd, 2 mod 4, or 0 mod 4 — the 2-adic
valuation, not the 8.

Worked case, a drawn graph (2026-10-11,
`resonant_lattice_c12_supplied_audit_2026_10_11.py`): crossing counts were
reported for C_12(1,2,3,6) "on integer coordinates". A graph fixes which
vertices are joined, not where edges cross, so the axis is the **embedding**.
Re-placing the same 12 vertices in the same cyclic order:

    supplied two-row grid        43 crossing pairs, 25 points, 15 pairs at one point
    any strictly convex position 111 pairs (chords cross iff endpoints interleave)
    regular 12-gon               111 pairs, 73 points, 15 pairs at the centre
    integer parabola (k,k^2)     111 pairs, 111 points, no concurrency

Only 12 vertices, 42 edges and 7-regularity survive, so those are the graph
facts; 111 is a fact of the graph with its cyclic order; 43/25 belong to one
placement. The 15-pair concurrency survives exactly when the placement is
centrally symmetric with the offset-6 matching — that is its mechanism,
found by the sweep rather than by looking.

Watch the qualifier when you state the sweep's rule. The first write-up
said "any convex position" gives 111; the supplied grid is itself convex
(its points run in order round a rectangle) and gives 43, because it is only
WEAKLY convex — collinear rows turn interleaving chords into overlaps and
vertex contacts. The rule needs "strictly convex". A counterexample to your
own stated rule can be the very object under test.

If you cannot name the axis, you cannot tier the result. Say "not assessed"
rather than assigning a tier by inspection.

- Survives every prime p = 1 mod 3 → **Tier A**. It says nothing about 37.
- Survives only {7, 37, 73} → **Tier B**.
- Survives only at 37 → **Tier C**. This is the only tier that is evidence.

For a construction using base-10 digits, the second axis is the base: re-run
it in base b and see where it breaks. **The break point is the stated
expiry**, and it belongs in the result.

## The Tier C facts in this corpus

```
ord_p(10) = 3  requires  p | 10^3 - 1 = 999 = 3^3 x 37
prime divisors of 999 are 3 and 37; at p = 3 the base collapses to 1
=>  37 is the ONLY prime for which base 10 generates mu_3
```

Everything else structural — the twelve orbits, the 37/74 split, negation
duality, the CRT independence, the Koopman spectrum — holds for every
p = 1 mod 3. **No result is evidence FOR 37 unless it uses ord_37(10) = 3.**

### A SECOND one, unrelated to the first (T365)

37 is the FIRST IRREGULAR PRIME: it divides the numerator of B_32, and
equivalently divides the class number of Q(zeta_37). No prime below 37
does. That is the first exponent Kummer's proof of FLT does not reach.

**The two do not touch.** `ord_37(10) = 3` is about the multiplicative
order of a particular base; irregularity is about Bernoulli numerators and
cyclotomic class numbers. Neither implies the other and neither
strengthens the other. Cite whichever one a result actually uses, and
never both as if they were one distinction.

## The reverse error

Tier A does not mean "numerology". At this prime the positional shift IS
the group action — rotation of a 3-digit word equals multiplication by 26,
verified on all 900 words. That is a theorem. The digit results are real;
they are simply consequences of the one Tier C fact rather than independent
evidence for it.

## Recording

State the tier in the theorem, with the primes or bases tested:

> TIER A. Verified for p = 7, 13, 19, 31, 37, 43, 61, 67, 73, 79, 97, 103,
> 109 — the property holds in every one, so it carries no information about
> 37. Checked before claiming rather than after.
