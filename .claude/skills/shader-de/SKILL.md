---
name: shader-de
description: Analyse a golfed raymarching shader and check whether its distance estimate is valid. Use when reading or writing compact GLSL raymarchers — twigl/Shadertoy one-liners, KIFS and Mandelbox folds, glow-accumulated marchers — or when one renders wrong, marches too slowly, or breaks after a port. Recovers the loop structure and fold operations from source, computes the Lipschitz bound the folds imply, compares it against the DE divisor, and independently verifies by sampling that no point inside the claimed clearance sphere is on the far side of the surface. Also flags unnormalised ray directions, non-unit rotation axes, uninitialised loop variables, and numeric literals standing in for named constants.
---

# shader-de

A folded raymarcher is only correct if its distance estimate never overstates
clearance. This checks that two ways — from the source text, and by sampling.

```
python3 .claude/skills/shader-de/de_check.py scan   shader.glsl
python3 .claude/skills/shader-de/de_check.py scan   -          # stdin
python3 .claude/skills/shader-de/de_check.py ray    1.7778
python3 .claude/skills/shader-de/de_check.py template > de_module.py
python3 .claude/skills/shader-de/de_check.py verify de_module.py
```

## scan — static, fully automatic

Recovers loops, fold operations and their scale factors, then computes the
Lipschitz constant and compares it to the divisor applied to the DE.

```
7 folds x scale 2.0  ->  L = 2^7 = 128
DE divisor found: 800
safety factor = 800/128 = 6.25x   -> covers the fold scaling (conservative)
```

A fold `p = abs(p+p) - c` scales by 2; `abs(p*s) - c` scales by s. Rotations
are isometries and contribute nothing. **The divisor must be at least the
product of the scale factors** or the march can step through the surface.

## verify — numerical, needs the DE transcribed

`template` prints a Python skeleton. Fill in the DE, then `verify` samples
points, and for each one checks that nothing within the claimed distance is
already inside the surface. Catches errors `scan` cannot see: a wrong
primitive, a sign slip, a fold that is not what it looks like.

The two agree. Sabotaging the divisor from 800 to 40:

```
scan    safety factor 40/128 = 0.31x   DIVISOR TOO SMALL
verify  386 points tested, 219 sign flips inside the DE sphere
```

## What else it reports

**Unnormalised rays.** `p = vec3(uv*g, g-c)` is not `ro + rd*g` with unit rd,
so `g` understates distance travelled. `ray <aspect>` gives the factor —
1.43x at 16:9, 1.62x at 21:9. A DE with tight margin renders correctly at one
aspect and breaks at another.

**Non-unit rotation axes.** `rotate3D(a, vec3(1, f(t), 0))` has length between
1 and sqrt(2). Twigl's builtin normalises; a hand-rolled one may not, and then
the matrix is not orthogonal, the Lipschitz bound fails, and the margin stops
being enough. This is the usual cause of a shader that works in twigl and
breaks elsewhere.

**Uninitialised loop variables.** `for(float i,e,g;...)` is undefined in GLSL
and zero on every driver anyone golfs against. Standard idiom, first thing to
break on an unusual compiler.

**Constants written as literals.** Reports any literal within 1% of pi, pi/2,
tau, phi, sqrt2 or e — `1.57` is pi/2 to 0.051%, which is deliberate and
invisible after seven folds, but worth knowing is an approximation.

## Reading the result

A large safety factor is not a mistake. It costs march steps and buys
robustness across aspect ratios and animated parameters. A factor below 1 is
a bug regardless of how the render looks — it means some ray, somewhere,
steps through geometry.

## Constant proximity is a diagnostic, not a bound

`constant_literals()` flags numeric literals within 1% of pi, pi/2, pi/3, pi/4,
tau, phi, sqrt2, e. It reports line numbers and does not deduplicate, so
`vec2(3.14159, 3.14159)` is two occurrences.

    constant proximity  =/=>  Lipschitz multiplier

These flags are never fatal and contribute nothing to the DE certificate. A
1%-off constant may be deliberate golf, or it may rotate an axis, shift a
boundary, move a phase, or flip a branch — the check makes no claim either
way. Do not write that such an error "becomes invisible after several folds";
depending on where the constant sits its error can stay fixed, accumulate, or
change the geometry outright.

Two implementation rules, both found by breaking the earlier version:

**The literal pattern is unsigned.** Folding `[-+]?` into the match does NOT
break `x-3.14159` — the engine advances past the operator and matches at the
digit, and the lookbehind then sees `-`, which is not `\w` or `.`. What it
does break is the standalone negative: `x * -6.2832` captures `-6.2832`, and
|(-6.2832) - tau| / tau = 2.0, so the tau approximation is silently missed.
A false negative on exactly the constant the check exists to catch. Unary
minus is an operator, not part of the literal.

**Strip both comment forms before scanning.** `line.split("//")[0]` leaves
`/* pi = 3.14159 */` intact and reports it as code. `strip_comments()`
replaces comment bytes with spaces rather than deleting them, so line numbers
and columns still refer to the original source. The pipeline is

    source preprocessing  ->  token extraction  ->  constant audit

and the audit stage must never see comment text.
