---
name: forced-check
description: Decide whether a GF(37) claim is forced or contingent before recording it. Use when a pattern looks striking — factorizations agreeing on coset position or digital root, an extreme block mapping to a named orbit, a property that seems special to 37. Detects the four forcing mechanisms found across T237, T285, T297 and T299 — complete partition, homomorphism, unbroken tie, and definition — and classifies any property into Tier A (true for every p = 1 mod 3), Tier B (the set {7,37,73}), or Tier C (unique to 37).
---

# forced-check

Four ways a GF(37) "finding" turns out to have been guaranteed.

```
python3 .claude/skills/forced-check/forced.py factorization 246
python3 .claude/skills/forced-check/forced.py tie '{"IC":7,"SEED":7,"C3":4}'
python3 .claude/skills/forced-check/forced.py tier "traces lie in <11>"
python3 .claude/skills/forced-check/forced.py orbit-claim 246 SEED
```

## The four mechanisms

**partition** — every residue lands in exactly one orbit, so "n has an
orbit" is never news. Only a *predicted* orbit carries the 3.58 bits.

**homomorphism** — class positions always add (T285) and digital roots
always multiply. Any check that factorizations agree is guaranteed. This is
what emptied T215's three-factorization list.

**tie** — an extreme that is not unique. Reading an orbit off one member of
a tie is the T237 failure; the tie can span both ends of the scale being
tested.

**definition** — the 137-map preserves every orbit because that is what an
orbit is. "The map fixes orbit X" is a restatement.

## Tier classification (T300)

Ask whether the property still holds at p=73, and at p=101.

- holds at both → **Tier A**, a fact about p = 1 mod 3, not about 37
- holds at 7 and 73 → **Tier B**, a fact about 137
- fails at both → candidate **Tier C**, verify against all primes

Tier B `{7,37,73}` and Tier C `{5,17,37}` are independent lists that meet
only at 37. Neither refines the other.

## Block separation (T297/T299)

Before recording, name which use of Phi_3 the claim belongs to:

- **Use 1** — evaluate Phi_3 in Z[x]. Factors 18907, gives mu_3, orbits,
  Z/12Z, the lattice. Computes no traces.
- **Use 2** — quotient by Phi_3 to get Z[omega]. Gives CM, twists, traces.
  Never factors 18907.

They share a root and nothing else. A Use-2 result must never be presented
as a corollary of a Use-1 result.
