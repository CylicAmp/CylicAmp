# FRAMEWORK FILE MAP
# How All 13 Files Connect

© 2026 Michael Warren Song. All Rights Reserved.

---

## THE THREE PILLARS

```
                    [FOUNDATION]
                        |
        +---------------+---------------+
        |               |               |
    [DIGITAL]      [PATTERNS]      [GEOMETRY]
     ROOT           ANALYSIS        (DIFFERENTIAL)
    SYSTEM
        |               |               |
        +---------------+---------------+
                        |
                   [SYNTHESIS]
```

---

## PILLAR 1: DIGITAL ROOT SYSTEM (Core)
*The base layer — everything builds on this*

### 1. `dr_algebra.py`
**Purpose:** Mathematical foundation
**Contains:**
- DR(n) = (n−1) mod 9 + 1 definition
- Addition table (Cayley table)
- Doubling cycles
- Group structure (Z/9Z isomorphism)

**Outputs to:** All other files
**Key insight:** DR forms a closed algebra

---

### 2. `pairs_81_analysis.py`
**Purpose:** The 9×9 grid structure
**Contains:**
- All 81 digit pairs (1–9 × 1–9)
- Uniform distribution proof (each DR 1–9 appears exactly 9 times)
- Trinity pairs (3, 6, 9) = 27/81 = 33.3%
- Total sum = 405 → 9

**Depends on:** `dr_algebra.py`
**Outputs to:** `vibration_grid_9x9.py`, `nine_constant_system.py`
**Key insight:** The grid is a Latin square with perfect symmetry

---

### 3. `vibration_grid_9x9.py`
**Purpose:** 3-6-9 anchor distribution
**Contains:**
- 3-6-9 anchor positions in the grid
- Growth chains (doubling sequences)
- 162-chain verification

**Depends on:** `dr_algebra.py`, `pairs_81_analysis.py`
**Outputs to:** `nine_constant_system.py`
**Key insight:** 3-6-9 forms the "gears" of the system (33.3% of all pairs)

---

### 4. `dr_preserving_doubling.py`
**Purpose:** The 162/324/648 chain
**Contains:**
- Proof: DR preserved under doubling IFF n ≡ 0 (mod 9)
- 162 → 324 → 648 → … all have DR = 9
- General form: 81 × 2^n

**Depends on:** `dr_algebra.py`
**Outputs to:** `nine_constant_system.py`, `vibration_grid_9x9.py`
**Key insight:** Multiples of 9 are "fixed points" under doubling

---

### 5. `repunit_sequence.py`
**Purpose:** The 2n−1 pattern
**Contains:**
- Repunit sequences R_n = (10^n − 1)/9
- Skip-2 pattern: 0→3→5→7→9→2→4→6→8→1
- Formula: 2n − 1

**Depends on:** `dr_algebra.py`
**Outputs to:** Pattern analysis layer
**Key insight:** The 2n−1 pattern is omnipresent across all systems

---

### 6. `nine_constant_system.py`
**Purpose:** The 9-constant as unifying container
**Contains:**
- Triad consolidation: 27×3=81→9, 27×6=162→9, 27×9=243→9
- Matrix power convergence to 9
- 37-field resonance

**Depends on:** All core DR files above
**Outputs to:** Synthesis layer
**Key insight:** 9 is the attractor — all paths lead to 9

---

## PILLAR 2: PATTERN ANALYSIS

### 7. `pattern_transform.py`
**Purpose:** Digit pattern transformations
**Contains:**
- Left column: n=X=Y
- Right column: a+b=XY
- Middle: a+b=X+Y=Z=W transformations

**Depends on:** `dr_algebra.py`
**Outputs to:** Synthesis layer
**Key insight:** Patterns that map to the core framework

---

## PILLAR 3: DIFFERENTIAL GEOMETRY

### 8. `differential_geometry.py`
**Purpose:** Curves, surfaces, geodesics
**Contains:**
- Curve class (parametric curves, curvature)
- Surface class (first/second fundamental forms)
- Geodesic class (shortest paths on surfaces)

**Depends on:** None (standalone mathematical foundation)
**Outputs to:** `tensors_curvature.py`, `jacobi_fields.py`
**Key insight:** Classical differential geometry as a potential embedding space

---

### 9. `tensors_curvature.py`
**Purpose:** Riemannian geometry
**Contains:**
- Riemann curvature tensor
- Ricci tensor, scalar curvature
- Parallel transport and holonomy

**Depends on:** `differential_geometry.py`
**Outputs to:** `jacobi_fields.py`
**Key insight:** Curvature measures deviation from flatness

---

### 10. `jacobi_fields.py`
**Purpose:** Geodesic deviation
**Contains:**
- Jacobi field equations
- Convergence/divergence analysis
- Connection to curvature

**Depends on:** `differential_geometry.py`, `tensors_curvature.py`
**Outputs to:** Synthesis layer
**Key insight:** How nearby geodesics separate (gravitational tidal forces)

---

## PILLAR 4: LATTICE SYSTEMS

### 11. `lattice_digital_root.py`
**Purpose:** 2D cellular automaton
**Contains:**
- 2D lattice with DR rules
- 3-6-9 resonance conditions
- Evolution rules for grid states

**Depends on:** `dr_algebra.py`, `pairs_81_analysis.py`
**Outputs to:** Synthesis layer
**Key insight:** Discrete spatial evolution of DR patterns

---

## SYNTHESIS LAYER

### 12. `FRAMEWORK_MASTER_REFERENCE.md`
**Purpose:** Single document with all axioms and rules
**Contains:**
- Core definitions
- All theorems
- Quick reference for key numbers
- Z = 0.023 analysis example

**Depends on:** All files above
**Key insight:** One place to find everything

---

### 13. `PROJECT_KNOWLEDGE.md`
**Purpose:** Session memory and context
**Contains:**
- Conversation history
- Work patterns

---

## DEPENDENCY GRAPH

```
dr_algebra.py  (FOUNDATION)
    |
    +--> pairs_81_analysis.py
    |       |
    |       +--> vibration_grid_9x9.py
    |               |
    |               +--> nine_constant_system.py
    |
    +--> dr_preserving_doubling.py
    |       |
    |       +--> nine_constant_system.py
    |
    +--> repunit_sequence.py
    |       |
    |       +--> pattern_transform.py
    |
    +--> pattern_transform.py
    |
    +--> lattice_digital_root.py
            |
            +--> nine_constant_system.py

nine_constant_system.py  (SYNTHESIS POINT)
    |
    +--> FRAMEWORK_MASTER_REFERENCE.md

DIFFERENTIAL GEOMETRY BRANCH (separate but parallel):
differential_geometry.py
    |
    +--> tensors_curvature.py
            |
            +--> jacobi_fields.py
                    |
                    +--> [potential connection to nine_constant_system.py]
```

---

## THE MISSING LINKS

**Gap 1: Differential geometry → Digital root system**
- No formal connection established yet
- Potential: Embed 81-grid on a curved surface?
- Potential: Geodesics as paths through DR space?

**Gap 2: Pattern transforms → Core framework**
- Patterns in `pattern_transform.py` need mapping to DR algebra
- Are they equivalent? Extensions? Something else?

**Gap 3: Physical interpretation**
- What does Z = 0.023 actually represent in the framework?
- Is it a coupling constant? A coordinate? A threshold?

---

## WORKFLOW RECOMMENDATION

| Task | Use |
|---|---|
| Computation | `dr_algebra.py` + `nine_constant_system.py` |
| Reference | `FRAMEWORK_MASTER_REFERENCE.md` |
| New patterns | Extend `pattern_transform.py` |
| Geometry connections | Build bridge from `jacobi_fields.py` to DR system |

---

## FILES BY FUNCTION

| Function | Files |
|---|---|
| Core math | `dr_algebra.py`, `pairs_81_analysis.py` |
| 9-constant | `nine_constant_system.py`, `dr_preserving_doubling.py` |
| Grid analysis | `vibration_grid_9x9.py`, `lattice_digital_root.py` |
| Sequences | `repunit_sequence.py` |
| User patterns | `pattern_transform.py` |
| Geometry | `differential_geometry.py`, `tensors_curvature.py`, `jacobi_fields.py` |
| Reference | `FRAMEWORK_MASTER_REFERENCE.md`, `FRAMEWORK_MAP.md` |

---

*The connections exist — they just weren't documented until now.*
