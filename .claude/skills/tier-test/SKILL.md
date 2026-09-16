---
name: tier-test
description: Decide whether a GF(37) result is actually about 37 by re-running the construction elsewhere — at other primes, or in other bases. Use on every result before calling it a finding, and always before presenting one as evidence for 37. Complements forced-check, which classifies by mechanism; this classifies by experiment. Four results in one session were presented as discoveries and turned out to hold for every prime congruent to 1 mod 3, carrying no information about 37 at all.
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
