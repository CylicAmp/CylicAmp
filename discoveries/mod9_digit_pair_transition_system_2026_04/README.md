# Mod-9 Digit-Pair Transition System

Original formalization of the three-layer mod-9 digit-pair transition system governing the adjacency lattice from 11 to 99.

## Three Layers
1. **Adjacency Lattice** — transitions by +1 (linear) or digit swap (mirror) from 11 through 55
2. **Swap Symmetry** — every pair (d1,d2) has mirror (d2,d1); both share the same DR
3. **Mod-9 Collapse** — all transitions preserve digital root under mod-9 reduction

## Core Constants
- Completion Constant 20: 7+4=11+9=20 and 9+1+1+9=20
- Global invariant: DR is preserved across all adjacency and swap transitions

This system is the foundation for the 9×9 State Matrix [11,99] and the deterministic recurrence in the G'5 Sovereign Kernel.

See statement.tex, analysis.tex, and verification.py for the formal definition and automated checks.
