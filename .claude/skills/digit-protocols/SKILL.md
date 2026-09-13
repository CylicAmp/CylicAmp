---
name: digit-protocols
description: Expand every number into all six registers automatically — positional vector, commutative flip and reversal delta, internal digit sum, digital root, triad/circuit partition, and harmonic tie to the triangular cycle — plus P/C/1 digit classification and GF(37) placement. Use on EVERY number that appears, without waiting to be asked: any digit pattern, reversal or flip pair, repdigit, palindrome, zero-structure or place-value tally, triangular number, Collatz or other trajectory, two-number pair, 3x3 or 9x9 grid, digit-sum ladder, comma group, or cumulative partial-sum chain. Nothing gets dropped or passed over as background math.
---

# digit-protocols

Two entry points. Neither needs the numbers flagged by hand first.

```
python3 .claude/skills/digit-protocols/engine.py     <mode> <args>
python3 .claude/skills/digit-protocols/protocols.py  <mode> <args>
```

## engine.py — the Multi-Register State Engine

Every number expands into all six registers automatically.

| mode | what it does |
|---|---|
| `n 34` | one number, all 6 registers |
| `trace 27 82 41` | a sequence, engine on each, with step index |
| `collatz 27` | full trajectory + triad-state audit |
| `pair 14 41` | the complete two-number expansion |
| `pairs 14 41 25 52` | many pairs in one call |
| `block 28 14 41 82` | flanked block, both flank rules, mirror checks |
| `classify 2288 5145` | P/C/1 and parity rendering, tally, symmetry breaks |
| `matrix` | the 9x9 R-matrix, concentric shells, borders, diagonals |
| `blocks 1` | the 1B family for B=1..9 |
| `verify` | every encoded claim asserted, fails loudly |

## protocols.py — the digit protocols

| mode | what it does |
|---|---|
| `246` | runs protocols 1-6 on a number |
| `board a b` | the two-number 3x3 board |
| `stream 121212` | chunk-counting by unit size |
| `revbuild 9 4` | additive-reversal recurrence, with the digit-swap variant |
| `nines 5` | the zero-count / all-nines progression |
| `zerostruct N` / `zerostruct-all` | terminal and incrementing zero structure |
| `triangular 9` | cumulative zero structure, T_n with DR reduction |

## The six registers

1. **POSITIONAL VECTOR** — string form, digits, length, comma groups, period tier
2. **COMMUTATIVE FLIP** — reverse, `|N - N_rev|` and its dr
3. **INTERNAL SUM** — explicit sum of constituent digits
4. **MODULAR REDUCTION** — digital root
5. **PARTITION FILTER** — triad attractor {3,6,9} vs dynamic circuit {1,2,4,5,7,8}
6. **HARMONIC TIE** — alignment with the triangular cycle 1,3,6,1,6,3,1,9,9

Plus a labelled 7th line for GF(37) residue and orbit, per CLAUDE.md's
standing analysis, and P/C/1 digit classification (P prime, C composite,
**1 unit** — the unit keeps its own symbol; calling it composite is the
error found in `reference/cut_table_113115117167.py`).

## Laws the tools already know

Do not rediscover these by hand — they are asserted in `verify()`.

```
ab + ba = aa + bb = 11(a+b)      flip pair and repdigit pair share a sum
|ab - ba| = 9|a-b|               but the spreads differ, 9:11
|aa - bb| = 11|a-b|
aba = 111a  -> SEAM always       111 = 3 x 37            (T310)
dr(2A) = dr(T_A)  iff  A = 0 mod 3                       (T311)
T_(n+9) - T_n = 9n+45            root stream has period 9
T_(8-n) - T_n = 36-9n            mirror axis is n=4, not n=5
3n+1 never outputs a triad root  {1,4,7}->4 {2,5,8}->7 {3,6,9}->1
n/2 is x5 mod 9                  1,5,7,8,4,2 cycle; 3<->6; 9 fixed
```

## Standing rule

Run the engine before drawing any conclusion about a number, and report
what it finds — including when a register has nothing to say. A register
that cannot return anything but one value is reporting a tautology, not a
measurement; `harmonic_tie` flags that case explicitly rather than
printing a zero that looks like a result.
