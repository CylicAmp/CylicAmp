# HEIR ILP bootstrap placement — scope findings

Audit of `github.com/google/heir` pinned at
**`c61bcc4d3c327c100eff4b3b1e31229994564625`** (2026-09-11, "Integrate LLVM at
llvm/llvm-project@7024b9e1b423").

Companion to `notes/lcr_aks_scope.md`. That note audits a CKKS bootstrapping
backend; this one audits the compiler pass that decides *where* bootstraps go.
Section 5 is where the two meet.

Primary sources:

```
lib/Analysis/ILPBootstrapPlacementAnalysis/ILPBootstrapPlacementAnalysis.{cpp,h}   631 + 125 lines
lib/Transforms/ILPBootstrapPlacement/{ILPBootstrapPlacement.cpp,.td,README.md}
lib/Utils/RotationUtils.h
```

---

## 1. Solver

OR-Tools **MathOpt**, `SolverType::kGscip` — i.e. **SCIP**. Not CBC, not HiGHS,
not Z3. The BUILD dependency set is exactly two targets:

```
@com_google_ortools//ortools/math_opt/cpp:math_opt
@com_google_ortools//ortools/math_opt/solvers:gscip_solver
```

`MODULE.bazel` pins `or-tools 9.12`, with `soplex 7.1.4` as SCIP's LP backend.

It is solved to a **1% relative MIP gap**, not to proven optimality:

```cpp
constexpr double kRelativeMipGap = 0.01;
solveArgs.parameters.relative_gap_tolerance = kRelativeMipGap;
```

The rationale in the source is candid and matters for section 4:

> "matching Orbit's solver configuration (Gurobi MIPGap / CBC gapRel = 0.01).
> Proving full optimality often dominates solve time on large instances while
> improving the objective by less than measurement noise in the profiled cost
> models."

The model is deliberately not solved more precisely than its own cost data
justifies.

Only three solver bindings exist in the whole tree:

| site | solver |
|---|---|
| `ILPBootstrapPlacementAnalysis` | SCIP via `kGscip`, 1% gap |
| `OptimizeRelinearizationAnalysis` | SCIP via `kGscip`, no gap tolerance set |
| `Dialect/Polynomial/Transforms/NTTSolver` | OR-Tools **CP-SAT** (not MIP) |

---

## 2. Variables and objective

Decision variables are exclusively level/scale state and management placement:

```
level[value], scale[value]           per secret SSA value  (scale in bits)
input_level[op], input_scale[op]     per tracked op
bootstrap[op], node_rescale[op]      management AFTER an op
edge_rescale[use], edge_scale[use]   management BEFORE a consuming op
```

`bootstrap[op]` is the only binary. Levels/scales are integer; `edge_scale` is
introduced only for CKKS multiplication operands.

Objective:

```
  bootstrapCost · SUM bootstrap[op]
+ rescaleCost   · ( SUM node_rescale[op] + SUM edge_rescale[use] )
+ SUM_op ( slope_op · input_level[op] + intercept_op )     <- level-dependent latency
- 0.001 · SUM level[value]                                 <- tie-break toward high levels
```

The `-0.001` term exists because level constraints are one-sided; without it the
solver could pick gratuitously low levels that decode into spurious
`level_reduce` ops. Op *input* levels are separate variables and take real
downward pressure from the latency terms, so the two do not fight.

Boundary conditions are ordinary linear constraints, not a separate injection
mechanism: `secret.generic` block args initialise from `mgmt.mgmt` attrs when
present (else `(bootstrapWaterline, Sw)`), and yielded values are **pinned by
equality** to the level annotated on the generic's result.

### There are no rotation-key variables

Neither per-level nor global. There is no Galois-key variable, no key-switch
count, no key-table size term anywhere in the model. Rotation enters **only as a
priced op**: `OpCostModel.rotate` is a `LinearCost`, and
`isa<tensor_ext::RotateOp>(op)` maps to it.

So key-switch density is **not** weighted against multiplicative depth. The only
coupling is that a rotation costs `slope · input_level + intercept`, which pushes
rotations toward low levels. Depth enters through the level variables and
bootstrap placement, never through key cost.

---

## 3. The Orbit cost model

`OpCostModel` is populated by `loadOrbitCostModel(path)` from a JSON
`latencyTable`. Per the pass README: **units are microseconds**, every key maps
to a per-level latency array where index `i` holds the latency at level `i+1`,
and **all keys are required** — loading fails if any is missing.

Six op classes get a `LinearCost{slope, intercept}` obtained by ordinary least
squares against level:

```cpp
slope     = (n*sumXY - sumX*sumY) / (n*sumXX - sumX*sumX);
intercept = (sumY - slope*sumX) / n;
```

```
addCtCt  addCtPt  mulCtCt  mulCtPt  rotate  negate
```

`bootstrap` and `rescale` are **not** fitted — they enter as constants:

```
bootstrapCost = average of POSITIVE latency samples
                (levels below the bootstrap range are recorded as zero)
rescaleCost   = per-level MAXIMUM
```

### Two hazards worth recording

**Mismatched aggregation.** `bootstrapCost` is a mean and `rescaleCost` is a
max. Their ratio in the objective is therefore partly an artifact of the
sampling distribution rather than a measured relationship. Since the objective
trades these two against each other directly, that ratio is load-bearing.

**Overridable free parameters.** `bootstrap-cost` and `rescale-cost` are pass
options (`ILPBootstrapPlacement.td`), as is `orbit-cost-model` itself. A
reported placement is reproducible only if those values are reported with it —
the same free-parameter problem as `aksFlags` in `notes/lcr_aks_scope.md`.

Defaults come from "Orbit's profiled 64k Lattigo base cost model" — i.e. the
profile is measured against **stock Lattigo at N=65536**.

---

## 4. BSGS: known to HEIR, invisible to the ILP

An earlier reading of this session concluded HEIR "cannot distinguish BSGS from
flat". **That was too broad and is corrected here.** HEIR knows BSGS well —
`lib/Utils/RotationUtils.h`:

```
/// Returns the best baby-step size N1 for BSGS
/// Mirrors Lattigo's lintrans.FindBestBSGSRatio.
inline int64_t findBestBSGSRatio(...)
```

plus `implementBabyStepGiantStep`, and ~60 files in `lib/` mention
BSGS/hoisting.

The real finding is a **layering boundary**:

```
BSGS IS used in      Kernel/EvalVisitor, Kernel/KernelImplementation,
                     Dialect/{Lattigo,Cheddar,TensorExt},
                     Lattigo/Transforms/ConfigureCryptoContext,
                     Analysis/RotationAnalysis/RotationEvalVisitor

BSGS is ABSENT from  Kernel/RotationCountVisitor              (0 hits)
                     Transforms/LayoutOptimization/LayoutConversionCost
                                    (0 hits; uses a separate shift network)
                     OpCostModel and the entire ILP           (0 hits)
```

BSGS is chosen during **kernel lowering**, which runs *after* the ILP has
already placed bootstraps using a per-op `rotate(level)` profile.

And the gap is structural, not an oversight that could be patched in place: a
`LinearCost{slope, intercept}` has no room to express amortisation. One
rotation's price cannot depend on how many other rotations share its
decomposition. A hoisted rotation inside a 32-diagonal linear transform and an
isolated rotation receive the identical fitted line.

**Consequence.** The ILP over-prices rotation-dense regions, and the error scales
with how much the backend amortises — not because HEIR is unaware of BSGS, but
because the placement decision is made one layer above where BSGS is chosen,
against a profile that averages over both cases.

This also explains the 1% gap. A `rotate` profile that cannot separate hoisted
from unhoisted carries noise well above 1%, so solving tighter would be
precision the data does not support. The comment quoted in section 1 says
exactly this.

---

## 5. Where this meets the LCR/AKS backend

From `notes/lcr_aks_scope.md`: the Fainabi fork replaces BSGS's ~sqrt(d)
giant-step key-switches with **flat d** hoisted automorphisms, buying a Q-only
plaintext multiply (the plaintext is baked into the key by
`GenAggregatedGaloisKeysNew`) at a fixed **2.17x** Galois key blowup, plus an
upstream-inherited ~5x transient keygen spike.

Both strategies emit the **same `RotateOp` count** into the IR. Orbit fits one
line to `rotate`. The ILP charges them identically.

**The architectural decision the LCR/AKS fork exists to make is invisible to the
placement pass sitting above it.** And because Orbit's default profile is
measured on stock 64k Lattigo, it is fitted to **BSGS** behaviour specifically —
so a flat-hoisted backend is priced by a model calibrated on its alternative.

Neither project is wrong on its own terms. The gap is between them, and neither
side's benchmarks would reveal it:

| | measured | unmeasured |
|---|---|---|
| LCR/AKS fork | +1 level, 2.17x keys | wall-clock; no like-for-like harness ships |
| HEIR ILP | placement optimal *given* the profile | whether the profile holds under amortisation |

---

## 6. Net position

| claim | status |
|---|---|
| solver is SCIP via OR-Tools MathOpt, 1% MIP gap | verified |
| no rotation-key variables, per-level or global | verified |
| key-switch density not weighted vs multiplicative depth | verified |
| cost model is OLS `slope*level + intercept`, 6 op classes | verified |
| bootstrap = mean of positives, rescale = max | verified |
| HEIR knows BSGS (RotationUtils mirrors Lattigo) | verified — **corrects an earlier reading** |
| ILP cost model cannot express amortisation | verified (structural: `LinearCost` shape) |
| magnitude of the resulting mispricing | **unmeasured** |

The last row is the open question. Quantifying it needs a rotation-dense program
profiled both ways against the same backend, which the LCR/AKS host-RAM ceiling
in the companion note currently blocks.

---

## Reproduction

```bash
GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 https://github.com/google/heir /tmp/heir
git -C /tmp/heir rev-parse HEAD   # c61bcc4d3c327c100eff4b3b1e31229994564625

H=/tmp/heir

# solver binding and gap
grep -nE 'SolverType::|relative_gap' \
  $H/lib/Analysis/ILPBootstrapPlacementAnalysis/ILPBootstrapPlacementAnalysis.cpp

# variables, objective, constraint families
grep -nE 'AddBinaryVariable|AddIntegerVariable|AddContinuousVariable|Minimize|AddLinearConstraint' \
  $H/lib/Analysis/ILPBootstrapPlacementAnalysis/ILPBootstrapPlacementAnalysis.cpp

# no rotation-key modelling (expect only the two RotateOp/costModel.rotate hits)
grep -cniE 'rotate|galois|keyswitch|bsgs|baby|giant|hoist|diagonal' \
  $H/lib/Analysis/ILPBootstrapPlacementAnalysis/ILPBootstrapPlacementAnalysis.{cpp,h}

# OLS fit and the mean-vs-max asymmetry
sed -n '80,145p' $H/lib/Transforms/ILPBootstrapPlacement/ILPBootstrapPlacement.cpp

# BSGS exists, but not in the cost path
grep -rln 'RotationUtils.h\|findBestBSGSRatio\|implementBabyStepGiantStep' $H/lib
grep -nE 'bsgs|baby|giant|hoist' $H/lib/Kernel/RotationCountVisitor.cpp   # expect none
```
