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
in the title. Worked case, Dragon-64 / D(Z/8Z): the axis is `n`, the
modulus of the discrete torus `(Z/nZ)^2`. Re-running the whole thing for
n = 3..12 showed every structural claim — `S'S = I`, `S^2 = C`,
`(ST)^3 = C`, `S_00 = 1/n` — holding in all ten, so none of them says
anything about 8. The specific integers (|SL2| = 384, dim A' = 44, the
twist histogram 20/12, the block type) are that general construction
evaluated at n = 8.

Even the parts that look like they might be special usually resolve into a
rule once the axis is swept: the count of modular twist refinements is 1,
3 or 4 according to whether n is odd, 2 mod 4, or 0 mod 4 — the 2-adic
valuation, not the 8.

If you cannot name the axis, you cannot tier the result. Say "not assessed"
rather than assigning a tier by inspection.

- Survives every prime p = 1 mod 3 → **Tier A**. It says nothing about 37.
- Survives only {7, 37, 73} → **Tier B**.
- Survives only at 37 → **Tier C**. This is the only tier that is evidence.

For a construction using base-10 digits, the second axis is the base: re-run
it in base b and see where it breaks. **The break point is the stated
expiry**, and it belongs in the result.

## The one Tier C fact in this corpus

```
ord_p(10) = 3  requires  p | 10^3 - 1 = 999 = 3^3 x 37
prime divisors of 999 are 3 and 37; at p = 3 the base collapses to 1
=>  37 is the ONLY prime for which base 10 generates mu_3
```

Everything else structural — the twelve orbits, the 37/74 split, negation
duality, the CRT independence, the Koopman spectrum — holds for every
p = 1 mod 3. **No result is evidence FOR 37 unless it uses ord_37(10) = 3.**

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
