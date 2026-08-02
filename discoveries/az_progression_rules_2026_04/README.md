# Alpha Zero (AZ) Progression Rules

Complete formalization of the Alpha Zero progression system (AZ1–AZ4).

## Core Progression Rules

1. **AZ Level Assignment (Outer Pair Rule)**
   - Outer pair (1,9) or (9,1) → AZ1
   - Outer pair (2,8) or (8,2) → AZ2
   - Outer pair (3,7) or (7,3) → AZ3
   - Outer pair (4,6) or (6,4) → AZ4

2. **Zero Completion Rule**
   AZ1 completes at 10, AZ2 at 20, AZ3 at 30, AZ4 at 50. Cycle repeats at next decade.

3. **Digit Label Sequence (Fixed Order)**
   1→ALO 2→ALE 3→AHO 4→AHE 5→A51 6→BLE 7→BLO 8→BHE 9→BHO

4. **A/B Pattern & OEEO Parity Preservation**
   Every valid structure maintains AABB, BABA, ABAB, or BBAA pattern with OEEO parity.

5. **Global Cycle Rule**
   AZ1 (10) → AZ2 (20) → AZ3 (30) → AZ4 (50) → AZ1 (60) → AZ2 (70) → …

See statement.tex and verification.py.
