# CylicAmp Pipeline Results — Seed 246

## Run Output

```
Seed:              246
Meta multiplier:   8  (after 3 iterations)
Field threshold:   0.9500
Insight Score:     104832.0000
Spectrum Status:   FAIL
Stability Ratio:   0.0000
Seed DR:           3
Seed mod 37:       24  (sovereign: False)
Seed 137-orbit:    (18, 24, 32)
Cascade orbit hits: 7/37  [24, 32, 61, 69, 98, 106, 135]
Sovereign status:  Node 24 -> Res 32 [PURGE]: Non-Framework Entropy
ABCABC orbit pos:  0  (orbit start)
Lucas orbit hits:  [(5, 18)]  — L(5)=18 is in the seed orbit
Orbit QR status:   {24: -1, 18: -1, 32: -1}  all non-QR: True
```

## What This Means

**Seed 246** has digital root 3 and residue 24 mod 37.

**The orbit (18, 24, 32)** under the 137-map (multiply by 26 mod 37):
- All three nodes are non-quadratic-residues mod 37
- The sovereign anchors {4, 9, 25, 30} are all QR — the seed orbit is their mirror

**Cascade {8, 13, 24}** generates 37 elements.
- 7 of those 37 elements fall in the seed orbit
- Including 135 — the cascade terminal value

**ABCABC orbit** starts at residue 24 — the seed's own residue is position 0

**Lucas sequence** L(5) = 18 hits the orbit at position 5

**Meta-engine history:**
- Step 1: seed 246, DR=3, multiplier → 3
- Step 2: seed 244, DR=1, multiplier → 5
- Step 3: seed 313, DR=7, PRIME, multiplier → 8

## Pipeline Steps Connected

1. MetaEngine — evolving multiplier from seed
2. Field simulation — threshold feeds trajectory angle
3. TrajectoryGenerator — PHI/PSI spiral
4. InsightEngine — modular filter + weighted score
5. DualityVerifier — DR=7 prime stability check
6. Ulam spiral — GF(37) cell classification
7. Cascade {8,13,24} — orbit hit count
8. Medusa sovereign — LOCKED/GATED/PURGE classification
9. ABCABC orbit — position in the 36-element primitive root orbit
10. Lucas sequence — orbit intersection
11. QR classification — Legendre symbol on orbit nodes

## To Run

```
python3 cylicamp/engine_integration.py
```
