# Mod-9 Digit-Pair Transition System

Formalization of the complete mod-9 / digit-transition system derived from the 7-4-9 triad, 360 Milestone Overlay, and Completion Constant 20.

## System Overview
The full structure consists of three interacting layers:
- Layer 1: Nearest-neighbor adjacency lattice on digit pairs (11 → 55)
- Layer 2: Involutive swap symmetry (a,b) ↔ (b,a) with fixed points aa
- Layer 3: Mod-9 equivalence collapse (n ∼ n + 9k) with 9 → 9

Global invariants:
- Fixed diagonal: 11, 22, 33, 44, 55, 66, 77, 88, 99
- Swap orbits: {67,76}, {78,87}, {89,98}
- Modular collapse classes: {1,10,19,…}, {2,11,20,…}, …

Final formal result:
A bidirectional digit-pair lattice with involutive symmetry and mod-9 equivalence collapse.

This system directly extends the Digital Root Compression discovery and supplies the explicit, checkable transition rules that power the D7 Dual Harmonic layer in the G'5 Sovereign Kernel.

See statement.tex, analysis.tex, and verification.py for the complete formal specification and automated checks.
