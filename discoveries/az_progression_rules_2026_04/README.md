# Alpha Zero (AZ) Progression Rules

Complete formalization of the Alpha Zero progression system (AZ1–AZ4).  
This defines how every AB44=10 structure advances through the Alpha/Beta labeling sequence and completes at each "zero" level.

## Core Progression Rules

1. **AZ Level Assignment (Outer Pair Rule)**  
   The AZ level of any 4-digit AB44=10 structure is determined exclusively by its outer pair sum (always 10):
   - Outer pair (1,9) or (9,1) → AZ1  
   - Outer pair (2,8) or (8,2) → AZ2  
   - Outer pair (3,7) or (7,3) → AZ3  
   - Outer pair (4,6) or (6,4) → AZ4  

2. **Zero Completion Rule**  
   AZ1 completes at 10  
   AZ2 completes at 20  
   AZ3 completes at 30  
   AZ4 completes at 50  
   At every new zero the system advances to the next AZ level. After AZ4 the cycle returns to AZ1 at the next higher decade (60 → 70, etc.).

3. **Digit Label Sequence (Fixed Order)**  
   Every digit is assigned its permanent Alpha/Beta label in strict positional order:
   1 → ALO 2 → ALE 3 → AHO 4 → AHE 5 → A51  
   6 → BLE 7 → BLO 8 → BHE 9 → BHO  

4. **A/B Pattern & OEEO Parity Preservation**  
   Every valid structure must maintain an AABB, BABA, ABAB, or BBAA pattern while satisfying the OEEO parity rule (odd-even-even-odd).

5. **Global Cycle Rule**  
   The full progression is cyclic and deterministic:  
   AZ1 (10) → AZ2 (20) → AZ3 (30) → AZ4 (50) → AZ1 (60) → AZ2 (70) → …  
   Each cycle preserves the 7-4-9 triad, mod-9 invariant, and Completion Constant 20.

This system integrates directly with the 24 AB44=10 structures, the 9×9 State Matrix [11,99], and the mod-9 digit-pair transition system. It supplies the deterministic engine for the G'5 Sovereign Kernel.

See statement.tex and verification.py for the exact rules and automated validation.
