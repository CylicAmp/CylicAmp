# Three CKKS bootstrapping approaches vs the HEIR Lattigo emit path

Verification of a three-way comparison (Owner A / B / C) against the actual
repositories and against HEIR's Lattigo backend. Companions:
`notes/lcr_aks_scope.md` (Owner A internals) and
`notes/heir_ilp_placement_scope.md` (HEIR's placement ILP).

Pins:

```
Owner A  Fainabi/Lattigo-LCR-AKS   branch lcr   3fbe5c8eeeea...   2025-10-23
Owner B  aqua4689jh/OverModRaise                ad9bdcad5281...   2025-10-07
Owner C  se-tim/PaCo-Implementation             84a91afbd855...   2026-08-31
HEIR     google/heir                            c61bcc4d3c32...   2026-09-11
```

---

## 1. The three, as verified

| | Owner A LCR-AKS | Owner B OverModRaise | Owner C PaCo |
|---|---|---|---|
| paper | (fork, no paper linked) | Kim, Cheon, Yeo — IACR CiC 2(3) | Coron, Seuré — ASIACRYPT 2025 |
| kernel | Go, Lattigo fork | C++, HEAAN (built on CryptoLab EvalRound) | SageMath PoC |
| build | `go build` w/ directory replace | `g++ proposal_main.cpp -I.`, `ulimit -s unlimited` | SageMath >= 10.0 |
| object | first C2S factor M0 | **ModRaise, upstream of M0** | partial CtS + blind-rotate |

**Correction to the original table.** Owner B's object was listed as "first CtS
factor M0", same as A. It is not — the over-lift happens at ModRaise, before
CoeffToSlot runs:

```cpp
const int LogQ_new = LOGQ + LogDelS;              // Q_over = Q_max + LogDelS
mod_raise<LOGq, LogQ_new, N>(ct, ct_modraise);    // lift ABOVE Q_max
RS<LogQ_new, LOGQ, N>(ct_modraise, ct_RS);        // rescale straight back
CoeffToSlot<LOGQ, ...>(ct_RS, s, ct_cts);         // C2S starts at LOGQ
```

Owner B's object is one step earlier in the pipeline than Owner A's.

---

## 2. A and B reclaim the same budget by opposite routes

Both land their saving in the **post-C2S** budget, neither enlarges the total.

**Owner A** keeps `Q_L <= Q_max` and folds the divide-by-`q_L` into the
GHS/AKS key. Verified in `notes/lcr_aks_scope.md` §3: `btpMax` is identical
within each stock/LCR parameter pair, bootstrapping depth drops by exactly 1,
and the level appears in `residualMax`. **+1 residual level at constant total
budget.**

**Owner B** lifts to `Q_over = Q_max + LogDelS`, rescales straight back, and the
over-raised bits survive the C2S chain:

```cpp
const int LOGQ_after_cts = LOGQ - (LOGN)/G * LOGDELTA_cts + LogDelS;
//                                                          ^^^^^^^^^
```

That trailing `+ LogDelS` is the entire saving, and it is the direct analogue of
Owner A's `residualMax` increment.

Same goal, opposite mechanism: A never exceeds `Q_max` and pays in key material
(2.17x Galois keys, verified); B exceeds it briefly and pays in an extra prime
during ModRaise.

**Not verified:** the original table's "pt-mul + rescale before KS" for Owner B.
The variant read here rescales with no plaintext multiply. The README lists
eight test entry points (`evalroundplus_test_S2C_first_adaptive_S2C`,
`erpluspar_12/23/all_together_*`); the pt-mul may appear in the adaptive ones.
Recorded as unchecked, not as wrong.

---

## 3. The HEIR emit path blocks all three, by three different mechanisms

### Owner A — replace is necessary but NOT sufficient

Two independent failure points, and the second is silent:

1. **Module resolution.** Only a local *directory* replace works; a remote
   replace is impossible in both directions (`notes/lcr_aks_scope.md` §1).
2. **Emitter fields.** `LattigoEmitter::printOperation(
   CKKSNewBootstrappingParametersFromLiteralOp)` writes exactly ONE field:

```cpp
os << "bootstrapping.ParametersLiteral{\n";
os << "LogN: utils.Pointy(" << btParams.getLogN() << "),\n";
os << "})\n";
```

`LogSlots` is deliberately omitted (with a justifying comment). `LevelConserved`
and `AggregatedFlags` are never written, so they default to `false` / `nil`.

**Consequence:** with the replace correct, the emitted program compiles against
the fork, links the fork, and runs **stock Bossuat** — no error, no diagnostic.
This is the same silent fallback recorded for the `go.mod`, reached from the
emitter instead, so fixing the module path does not fix it.

Requirement for Owner A is therefore *replace Lattigo path* **and** *extend the
emitter to write both fields*.

### Owner B — there is no target, not a replace problem

HEIR's backends:

```
Jaxite  JaxiteWord  Lattigo  OpenFhePke  Poulpy
SCIFRBool  SimFHE  TfheRust{,Bool,HL}  Verilog  Metadata  CompilationTarget
```

`grep -rliE 'heaan|evalround'` over `lib/` and `tools/` returns **nothing**.
OverModRaise is C++/HEAAN, so no Go module mechanism applies at all. The
prerequisite is writing a HEAAN emitter, not adjusting a directive.

### Owner C — the op has no seam

`Lattigo_CKKSBootstrapOp` is a `Lattigo_CKKSUnaryOp`: in `(evaluator,
ciphertext)`, out `(ciphertext)`. It emits one monolithic call:

```go
result, err := evaluator.Bootstrap(input.CopyNew())
```

There is no point at which "partial CtS, then blind-rotate" could be inserted.
Its own docstring pins the contract it cannot escape — *"takes a ciphertext at
level 0 … returns a ciphertext with the max level of
`evaluator.ResidualParameters.MaxLevel`"* — which is precisely the EvalMod-based
round trip PaCo replaces.

Worth noting a seam does exist one op over: `Lattigo_CKKSLinearTransformOp` is
separate, and `NewBootstrappingEvaluator` / `GenEvaluationKeysBootstrapping` are
distinct ops. Owner C is not blocked by dialect granularity in general — only by
`bootstrap` specifically being atomic.

---

## 4. The cross-row result

All three approaches modify the **early bootstrapping stages** — A and B at or
just before the first C2S factor, C by replacing the DFT chain outright.

HEIR's `lattigo.ckks.bootstrap` is the one op in the Lattigo dialect with **no
internal structure at all**. Every approach here targets exactly the region the
Lattigo backend treats as a black box. That is why three unrelated designs are
blocked by three unrelated mechanisms: it is one structural gap seen from three
directions.

This compounds with the ILP finding in
`notes/heir_ilp_placement_scope.md` §4-5. The placement pass prices rotations
with one OLS line fitted on stock 64k Lattigo, so it cannot see BSGS-vs-flat;
the emitter cannot express any of the three alternatives. HEIR can neither
*model* nor *emit* the design space these three occupy.

---

## 5. Status

| claim | status |
|---|---|
| A: +1 residual level at constant btpMax | verified (companion note) |
| A: 2.17x Galois key blowup, structurally fixed | verified (companion note) |
| A: HEIR emit needs replace AND emitter change | **verified here** |
| B: lift to Q_over > Q_max, saving survives C2S | **verified here** |
| B: object is ModRaise, not first C2S factor | **verified — corrects the table** |
| B: "pt-mul + rescale before KS" | **unchecked** (8 variants; one read) |
| B: no HEIR target exists at all | **verified here** |
| C: real paper, Sage PoC, partial CtS present | **verified here** |
| C: blocked by atomic bootstrap op | **verified here** |
| C: depth O(log C), EvalMod-replacement | **unchecked** |
| relative wall-clock of any of the three | unmeasured (host RAM ceiling) |

---

## Reproduction

```bash
GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 --branch lcr \
  https://github.com/Fainabi/lattigo-lcr-aks /tmp/a          # 3fbe5c8eeeea
GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 \
  https://github.com/aqua4689jh/overmodraise /tmp/b          # ad9bdcad5281
GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 --recurse-submodules \
  https://github.com/se-tim/paco-implementation /tmp/c       # 84a91afbd855
GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 \
  https://github.com/google/heir /tmp/heir                   # c61bcc4d3c32
```

`--recurse-submodules` is load-bearing for C: `paco_package/ckks_in_sagemath`
points at `se-tim/CKKS-in-SageMath` and a plain shallow clone leaves it empty,
so the PoC will not run.

```bash
# B's over-lift and the surviving LogDelS
sed -n '195,225p' /tmp/b/OverModRaise/proposal_main.cpp

# HEIR emits only LogN
sed -n '2411,2436p' /tmp/heir/lib/Target/Lattigo/LattigoEmitter.cpp

# the bootstrap op is unary / atomic
sed -n '339,360p' /tmp/heir/lib/Dialect/Lattigo/IR/LattigoCKKSOps.td

# no HEAAN or Sage backend
ls /tmp/heir/lib/Target/
grep -rliE 'heaan|evalround|sagemath|paco' /tmp/heir/lib /tmp/heir/tools   # expect none
```
