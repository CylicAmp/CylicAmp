# AB44=10 Full Tagging – A/B, Odd/Even Parity, and Label Mapping

Complete, exhaustive tagging of all 24 AB44=10 structures with:
- A/B classification
- Odd/Even parity (O/E)
- Full label mapping (ALO, ALE, AHO, AHE, BLE, BLO, BHE, BHO)

A-side digits: 1,2,3,4  
B-side digits: 6,7,8,9  
Odd → O, Even → E

This tagging confirms perfect AABB ↔ BBAA mirror symmetry and consistent OEEO parity cycles across the closed 24-pattern system.

## Full Tagged List

**Forward Set (12)**

1. 1289 → ALO–ALE–BHE–BHO → AABB / OEEO  
2. 1379 → ALO–AHO–BLO–BHO → AABB / OOOO  
3. 1469 → ALO–AHE–BLE–BHO → AABB / OEEO  

4. 2198 → ALE–ALO–BHO–BHE → AABB / EOOE  
5. 2378 → ALE–AHO–BLO–BHE → AABB / EOOE  
6. 2468 → ALE–AHE–BLE–BHE → AABB / EEEE  

7. 3197 → AHO–ALO–BHO–BLO → AABB / OOOO  
8. 3287 → AHO–ALE–BHE–BLO → AABB / OEEO  
9. 3467 → AHO–AHE–BLE–BLO → AABB / OEEO  

10. 4196 → AHE–ALO–BHO–BLE → AABB / EOOE  
11. 4286 → AHE–ALE–BHE–BLE → AABB / EEEE  
12. 4376 → AHE–AHO–BLO–BLE → AABB / EOOE  

**Mirror Set (12)**

13. 9821 → BHO–BHE–ALE–ALO → BBAA / OEEO  
14. 9731 → BHO–BLO–AHO–ALO → BBAA / OOOO  
15. 9641 → BHO–BLE–AHE–ALO → BBAA / OEEO  

16. 8912 → BHE–BHO–ALO–ALE → BBAA / EOOE  
17. 8732 → BHE–BLO–AHO–ALE → BBAA / EOOE  
18. 8642 → BHE–BLE–AHE–ALE → BBAA / EEEE  

19. 7913 → BLO–BHO–ALO–AHO → BBAA / OOOO  
20. 7823 → BLO–BHE–ALE–AHO → BBAA / OEEO  
21. 7643 → BLO–BLE–AHE–AHO → BBAA / OEEO  

22. 6914 → BLE–BHO–ALO–AHE → BBAA / EOOE  
23. 6824 → BLE–BHE–ALE–AHE → BBAA / EEEE  
24. 6734 → BLE–BLO–AHO–AHE → BBAA / EOOE  

## Key Observations
- Perfect symmetry: AABB ↔ BBAA (mirror)  
- Parity cycles repeat in groups: OEEO (dominant), EOOE (mirror), OOOO, EEEE  
- ALO/ALE/AHO/AHE and BLE/BLO/BHE/BHO labels stay strictly ordered on their respective sides  
- The entire set is structurally consistent with the mod-9 digit-pair transition system, 9×9 State Matrix, and 7-4-9 triad

This full tagging completes the base layer for Alpha Zero progression and deterministic recurrence.

See statement.tex and verification.py for formal definition and automated reproduction.
