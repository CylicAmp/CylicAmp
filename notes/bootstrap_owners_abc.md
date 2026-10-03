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

### The pt-mul IS there, in the erpluspar variants — verified

The simple variant read first has no plaintext multiply at the over-raise. The
`erpluspar_*_adaptive_S2C` variants (the ones the README uses to reproduce the
paper's Table 4) do, and they lift more to pay for it:

```cpp
// simple (proposal_main.cpp ~200)
const int LogQ_new    = LOGQ + LogDelS;
RS<LogQ_new, LOGQ, N>(...)                       // drops LogDelS, back to LOGQ

// erpluspar_12_S2C_first_adaptive_S2C (3692)
const int LogQ_new    = LOGQ + LogDelS + LOGDELTA_cts;   // bigger lift
const int LogQ_new_rs = LOGQ + LOGDELTA_cts;             // rescale KEEPS LOGDELTA_cts
RS<LogQ_new, LogQ_new_rs, N>(...)                        // drops only LogDelS
```

One extra `LOGDELTA_cts` — a full C2S rescale step — survives into CoeffToSlot.
It is consumed in the first factor, via `CoeffToSlot_sw_adaptive` ->
`grouped_serial_linear_transform_sw_adaptive` -> `linear_transform_sw`
(`HEAAN/linear_transform.h`):

```cpp
rot<LOGQ, N>(pt, pt_rot, N/2 - Ar.off[s]);       // rotate the PLAINTEXT
ct_rot = ct;
ct_rot *= pt_rot;                                 // 1. pt-MUL
RS<LOGQ, LOGQ - LOGDELTA, N>(ct_rot, ct_rs);      // 2. RESCALE
swkgen(skey_rot, skey, rkey);
rot_ct<LOGQ - LOGDELTA, N>(ct_rs, Ar.off[s], rkey, ct_block);   // 3. KEY-SWITCH
```

**pt-mul -> rescale -> key-switch**, confirming the original table row exactly.

The plain `linear_transform` does the reverse — pt-mul, accumulate, then
`rot_ct` on the CIPHERTEXT at full `LOGQ`, with no rescale in between. The
mechanism in `_sw` is that it **rotates the plaintext instead of the
ciphertext**, by the complementary offset `N/2 - Ar.off[s]`. That lets the
rescale precede the key-switch, so the key-switch — the expensive operation —
runs at `LOGQ - LOGDELTA` rather than `LOGQ`. The extra `LOGDELTA_cts` carried
through ModRaise is exactly what buys that.

### Which makes the A/B parallel exact

```
A   fold divide-by-q_L into the GHS/AKS key      -> the key-switch performs the rescale
B   rotate plaintext, pt-mul, rescale, then switch -> the rescale precedes the key-switch
```

Both lower the modulus at which the **first factor's key-switch** runs. A
rewrites the key; B reorders the operations. And both keep the same shape for
the rest of the chain: `serial_linear_transform_sw_adaptive` uses
`linear_transform_sw` for factor 0 and
`linear_transform_adaptive_sparse_babystep_giantstep` for factors 1..D-1,
mirroring `dftLevelConserved`'s LCR-at-i=0 / AKS-or-BSGS-after split.

Incidental: the dense (`double[][]`) overload of plain `linear_transform`
carries a literal `// BUG` comment on its `rot_ct` line. Not on any path used
by these variants, but recorded.

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
| B: "pt-mul + rescale before KS" | **verified** in the erpluspar variants |
| B: first factor special, later factors BSGS (as in A) | **verified here** |
| B: no HEIR target exists at all | **verified here** |
| C: real paper, Sage PoC, partial CtS present | **verified here** |
| C: blocked by atomic bootstrap op | **verified here** |
| C: EvalMod genuinely replaced, not reduced | **verified** — zero EvalMod in the package |
| C: depth is O(log C) | **verified** — but see below, it is not *lower* depth |
| C: "not a full DFT chain" | **not what the benchmark tests** (baseline runs at matched C) |
| relative wall-clock of any of the three | unmeasured (host RAM ceiling) |

---

## 3b. Owner C's O(log C) claim, verified and qualified

`benchmarks.py` states both depth formulas outright:

```python
# PaCo
L = ceil((log_C + 1)/g) + ceil((log_C - 1)/g) + log_h + 3
# Original
L = 2 * ceil(max(log_C - 1, 1)/g) + log_d + r + 1
```

**O(log C): verified.** The C-dependent term is
`ceil((log2 C + 1)/g) + ceil((log2 C - 1)/g)`, from the two matrix chains built
in `config_PaCo` — `log2(C)+1` partial-CtS factors and `log2(C)-1` StC factors,
with `C` a power of two, `C >= 2`, and `4*C*h <= N`.

**EvalMod replaced, not reduced: verified.** `grep -rnE
'eval_mod|EvalMod|sine|taylor|squaring'` over `paco_package/` returns nothing.
`seq_PaCo` runs blind-rotate (`coeff_encoding_list[t] @ bsk[t]`), trace, the
partial-CtS chain, mu/eta plaintext multiplies, then the StC chain. The `d`
and `r` prompts in `benchmarks.py` belong to the BASELINE it compares against.

**"Not a full DFT chain": not what is tested.** The baseline is configured at
matched slot count — `CKKS.config(N, 2**(log_C - 1), L, q, p, delta)` — so both
sides carry O(log C / g) transform depth. The benchmark is PaCo vs
baseline-at-C-slots, not PaCo vs a full `log2(N/2)` chain.

**And PaCo is not cheaper in depth at the repo's own defaults**
(N=2^16, h=64, g=3, d=63, r=2):

```
    C   CtS  StC   PaCo L   Orig L   diff
    2     1    0      10       11      -1
    4     1    1      11       11       0
    8     2    1      12       11      +1
   16     2    1      12       11      +1
   32     2    2      13       13       0
   64     3    2      14       13      +1
  128     3    2      14       13      +1
  256     3    3      15       15       0

CtS = ceil((log2 C + 1)/g)   StC = ceil((log2 C - 1)/g)   g = 3
PaCo constant:  log2(h) + 3           = 9
Orig constant:  ceil(log2 d) + r + 1  = 9
```

PaCo is **never below** the baseline except at C=2, and is strictly **above** it
at C = 8, 16, 64, 128. The two constants coincide, so the whole difference is
the ceiling behaviour of the two transform chains.

Consequence for parameters, since FHE parameters are dictated by L: a scheme
with equal or higher depth cannot run on smaller parameters. At C = 8, 16, 64
and 128, PaCo needs one MORE level, which pushes Q up, not down. Any claim that
sparse bootstrapping yields "smaller and faster parameters" is not supported by
these numbers and is contradicted at half the admissible values of C.

**Arithmetic warning.** These ceilings are easy to get wrong, and getting them
wrong biases in one direction — every error found in a drifted copy of this
table understated PaCo's depth (`ceil(4/3)` read as 1, `ceil(7/3)` as 2,
`ceil(8/3)` as 2). Recompute with true division, not integer division.

**The real structural change is which parameter the depth depends on.**
Original CKKS bootstrapping depth carries no `h` term — it is `log2(d) + r + 1`,
purely EvalMod. PaCo's is `log2(h) + 3`, purely the secret's Hamming weight.
PaCo does not remove a cost; it **relocates the dependence** from EvalMod
parameters onto the sparse secret. It wins when `log2(h) + 3 < log2(d) + r + 1`
— sparse secret, expensive EvalMod — and loses on a dense one. The constraint
`4*C*h <= N` couples them: raising `h` both raises the constant and caps `C`.

The other half of the trade, from the `seq_PaCo` docstring: *"Only the
coefficients indexed by multiples of N / C are bootstrapped."* The O(log C) is
bought by refreshing C of N coefficients; `parallel_PaCo(kappa)` recovers
coverage with kappa independent instances at multiples of `N/(kappa*C)`.

**On precision.** A claim that PaCo "removes the precision/error tradeoff
inherent in EvalMod" is NOT supported by anything in this repository. The
tradeoff is relocated, not eliminated: PaCo swaps EvalMod's analytical
approximation error for the noise growth of its blind-rotate and accumulator
steps. `benchmarks.py` computes and prints both `precision_paco` and
`precision_orig`, which is what one does for a quantity expected to vary — the
authors treat it as an empirical comparison, not a structural guarantee.

**The sound form of the argument**, narrower than the usual framing:
PaCo does structurally compress the TRANSFORM depth from O(log N) to O(log C)
— real, and large: a full DFT at N=2^16, g=3 costs 2*ceil(15/3) = 10 levels
against PaCo's 6 at C=256. But it spends that saving on a heavier evaluation
constant, `log2(h) + 3` in place of `log2(d) + r + 1`. The benefit is therefore
strictly conditional on the regime: it wins only where the N-to-C gap is large
enough to outpace the constant h imposes, and `4*C*h <= N` works against that
by capping C as h grows.

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
