---
name: forced-check
description: Decide whether a GF(37) claim is forced or contingent before recording it. Use when a pattern looks striking — factorizations agreeing on coset position or digital root, an extreme block mapping to a named orbit, a property that seems special to 37. Also use for any digit observation — mirror sums, repdigit digit sums, palindrome swaps, comma groups, checkerboard grids, digit-vector spectra, splitting a decimal expansion — since those are almost always fixed by the numeral rather than the number. Detects the five forcing mechanisms — complete partition, homomorphism, unbroken tie, definition, and base-10 rendering — and classifies any property into Tier A (true for every p = 1 mod 3), Tier B (the set {7,37,73}), or Tier C (unique to 37).
---

# forced-check

Five ways a "finding" turns out to have been guaranteed.

```
python3 .claude/skills/forced-check/forced.py factorization 246
python3 .claude/skills/forced-check/forced.py tie '{"IC":7,"SEED":7,"C3":4}'
python3 .claude/skills/forced-check/forced.py tier "traces lie in <11>"
python3 .claude/skills/forced-check/forced.py orbit-claim 246 SEED
python3 .claude/skills/forced-check/forced.py digits 70767137183112
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

**rendering** — the result is fixed by the base-10 numeral, not by the number.
A digit operation that would give the same answer for any digits in the same
shape carries nothing about the specific value. This is the mechanism behind
every digit-game result: mirror sums, repdigit digit sums, comma groups,
checkerboard determinants. Run `forced.py digits <n>` before recording any
digit observation.

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

## The rendering catalogue

Each of these is forced. If a claim reduces to one, it carries zero bits.

| observation | forced because | value |
|---|---|---|
| `(10a+b) + (10b+a)` | mirror sum | `11(a+b)`, always |
| `DR` of that | `11 = 2 mod 9` | `DR(2(a+b))` |
| `aba - bab` | 3-digit palindrome swap | `91(a-b)`, and `91 = Phi_6(10) = 7 x 13` |
| digit sum of k copies of d | construction | `k*d = N`, so `DR = DR(N)` |
| "n splits as k copies of d" | divisor pair | every `(k,d)` with `kd = N`, `d <= 9` |
| a 3-digit substring at a comma | grouping | position artifact; test divisibility instead |
| checkerboard matrix, odd height | row 1 = row 3 | `det = 0`, any two digits |
| period-2 digit vector, even length | sub-period | DFT is DC + Nyquist only, all else exactly 0 |
| same vector, odd length | 2 does not divide N | spectrum is full; no structure lost or gained |
| Nyquist DFT bin, even length | `10 = -1 mod 11` | equals the alternating digit sum, equals the mod-11 test |
| splitting a decimal expansion | chosen cut + rounding | result moves with the cut; not a property of the constant |

Two rules that follow:

**A digit fact must survive a digit substitution.** If replacing the digits
with any other pair in the same arrangement gives the same conclusion, the
conclusion is about the arrangement.

**Divisibility is not substring occurrence.** `137` appearing in a numeral
is a rendering fact. `137 | n` is arithmetic. Check the second; the first is
free at roughly 1 in 1000 per 3-digit window.
