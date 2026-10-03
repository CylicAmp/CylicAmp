# LCR/AKS CKKS bootstrapping fork — scope findings

Audit of `github.com/Fainabi/Lattigo-LCR-AKS`, branch `lcr`, pinned at
**`3fbe5c8eeeea9ee127d074915d909a18c2a0f9d4`** (2025-10-23, subject "benches"),
against stock `github.com/tuneinsight/lattigo/v6 v6.1.0`.

Every number below was measured on the pinned checkout, not taken from the
repository's claims. Reproduction steps are at the end.

---

## 1. The fork cannot be consumed as a remote Go module

`go.mod` on `lcr` declares `module github.com/tuneinsight/lattigo/v6` — the
**upstream** path — with **no replace directive**. `master` carries an
identical `go.mod`.

Both remote-replace forms are rejected, verified by building:

```
replace ... => github.com/Fainabi/Lattigo-LCR-AKS v6.0.0-...
  -> "invalid version: should be v0 or v1, not v6"      (repo path lacks /v6)

replace ... => github.com/Fainabi/Lattigo-LCR-AKS v0.0.0-...
  -> "go.mod has post-v0 module path
      github.com/tuneinsight/lattigo/v6 at revision 3fbe5c8eeeea"
```

The fork is caught between its path (which forces v0/v1) and its go.mod
(which declares v6). No pseudo-version satisfies both.

**The only working path is a local directory replace**, verified building
clean:

```
require github.com/tuneinsight/lattigo/v6 v6.1.0
replace github.com/tuneinsight/lattigo/v6 => /path/to/clone
```

This works *because* the fork kept the upstream module path — a directory
replace requires the target's go.mod to declare the left-hand path. What
looks like an oversight is load-bearing.

**Verification consequence.** A directory replace has no `go.sum` entry and
no version to pin, so a published benchmark from this fork **cannot be
reproduced from its go.mod**; the commit SHA must travel out of band. Two
people with a correct replace and different checkouts get different code
with no diagnostic. Separately, omitting the replace entirely resolves
silently to stock upstream from the module proxy — no error, wrong
algorithm.

---

## 2. What the fork adds

```
LCR  Level-Conserved Rotation
     NewLevelConservedEvaluator, dftLevelConserved,
     NewMatrixFromLiteralLevelConserved, EvaluateLevelConserved,
     MultiplyByDiagMatrixLevelConserved

AKS  Aggregated Key Switching
     MultiplyByDiagMatrixWithAKS, checkKeysWithAKSFlags,
     EvaluateAggregatedLT, GaloisElementsRemovingAggregatedFlags
```

plus a packing layer (`packingContext`, `pack`/`unpack`, ring-degree
switching) absent upstream. ~1000 changed lines across the bootstrapping
path — a substantive fork, not a rename.

### LCR is C2S-only and applies to one stage

Every guard is `i == 0 && d.LevelConserved`; `dftLevelConserved` takes the
level-conserved branch only at `matrixIdx == 0`. Stages 1..n-1 use AKS where
an aggregated key exists at that level, else stock `Evaluate` + `Rescale`.
`NewMatrixFromLiteralLevelConserved` is wired only into `C2SDFTMatrix` —
SlotsToCoeffs never gets it.

**A cost model treating LCR as a per-stage saving is wrong by the stage
count. It is one level off the head, total.**

Two preconditions are hard errors, not degradations:

```
nbModuliPerRescale != 1   ->  "LevelConserved is not implemented"
d.Levels[i] != 1          ->  "LevelConserved is not implemented for d.Levels[i]"
```

### AKS is not a BSGS variant

`MultiplyByDiagMatrixWithAKS` is a fork of upstream's **flat**
`MultiplyByDiagMatrix`, not of `MultiplyByDiagMatrixBSGS`:

| | lines | substantive diff vs fork AKS |
|---|---|---|
| upstream flat | 120 | **24** |
| upstream BSGS | 178 | 159 |
| fork AKS | 131 | — |

Loop bounds confirm it:

```
BSGS  keys := GetSortedKeys(matrix.BSGSIndex())   giant steps, ~sqrt(d)
      nested giant x baby; GadgetProductLazy per giant step

AKS   keys := GetSortedKeys(matrix.Vec)           EVERY diagonal, d of them
      flat loop; GadgetProductHoistedLazy per diagonal
```

**AKS performs d key-switches where BSGS performs ~sqrt(d).** It does not
reduce rotations; it abandons the BSGS decomposition. Any reading of "AKS"
as a rotation-count optimisation over BSGS has the sign backwards.

What is eliminated is not a rotation. The per-diagonal plaintext multiply
over the **full QP ring** (four `ringQP.MulCoeffsMontgomery*` calls)
collapses to a single **Q-only** `ringQ.MulCoeffsMontgomeryThenAdd`. The
mechanism is in `genAggregatedGaloisKeys`, which calls
`GenAggregatedGaloisKeysNew(galEl, &skDense.Value, &rotatedSkDense, &matVec,
qModuli[level])` — `matVec` is the automorphed **matrix diagonal**. The
plaintext is baked into the key.

That is also why the keys cannot be shared: each is specific to
(level, rotation, diagonal value).

---

## 3. The payoff: +1 usable level at constant total budget — VERIFIED

Every LCR parameter set carries one more residual modulus than its stock
twin, and this is **not** paid for with a larger parameter set:

```
          residualMax   btpMax   C2S.LevelQ   S2C.LevelQ   btpDepth
stock[0]        9         24         24           12          15
LCR[0]         10         24         24           13          14
stock[1]        5         23         23            8          18
LCR[1]          6         23         23            9          17
stock[2]        7         21         21            9          14
LCR[2]          8         21         21           10          13
```

`btpMax` is **identical within each pair**. Bootstrapping depth falls by
exactly 1 and that level appears in `residualMax`. `S2C.LevelQ` shifts +1,
confirming the saved level propagates rather than being reabsorbed.

**This is the one claim of the fork that is fully verified here.**

---

## 4. The cost: a fixed 2.17x key blowup

C2S diagonal structure, identical at LCR[1] and LCR[2]:

```
  matrix[0]  32 diagonals   LCR stage (VectorQP keys)
  matrix[1]  15 diagonals   AKS
  matrix[2]  15 diagonals   AKS
  matrix[3]  31 diagonals   AKS
```

```
                       LCR[1]            LCR[2]
stock Galois keys        46                46
reduced (AKS flags)      39                39
aggregated generated     61                61
net total               100               100     = 2.17x
one GaloisKey         22.00 MB          28.00 MB
stock set              0.99 GB           1.26 GB
LCR/AKS set            2.15 GB           2.73 GB  = 2.39x / 2.17x
uncounted VectorQP       32                32
```

The ratio is **invariant** — it is fixed by the DFT factorisation geometry
(32/15/15/31), not the modulus chain, so it does not improve at other
parameters. Storage runs worse than the count ratio because LCR keys sit at
higher levels. Both storage figures **exclude** the 32 `VectorQP` objects of
the LCR stage, so they are lower bounds.

`aksFlags` is a free parameter: hardcoded `{21,20,19}` in `BenchmarkLCR`,
otherwise derived in `evaluator.go` from whatever levels happen to have
entries in `EvkAggregatedGaloisKeys`. It is not reported alongside any
result.

---

## 5. Wall-clock is unmeasured, and the repo cannot measure it

### The fork ships no like-for-like benchmark

- `BenchmarkLCR` — ScaleDown + ModUp + CoeffsToSlots on `SparseLCR[2]`.
- `BenchmarkBootstrap` — a **full bootstrap** on the **stock**
  `DefaultParametersSparse`/`Dense`.

Different parameter families, different scopes. No benchmark compares stock
C2S against LCR C2S. Any speedup claim citing this file compares two things
that were never run against each other.

`BenchmarkBootstrap` also calls `GenEvaluationKeys` **outside** `b.Run`,
inside a `2 param types x 3 sets` loop, so `-bench` filtering does not
prevent key generation for all six sets.

### The memory wall is upstream's, not the fork's

On a 15 GB host, LogN=16 key generation is OOM-killed for **both**:

```
LCR[2]     peak 13.95 GB   killed in GenEvaluationKeys (dmesg-confirmed)
stock[1]   peak 12.08 GB   killed in GenEvaluationKeys
```

Stock has 46 keys and a 0.90 GB table and dies at the same ceiling. The
~5x transient overhead is intrinsic to lattigo's LogN=16 bootstrapping
keygen, **not** an artifact of `genAggregatedGaloisKeys`.

### There is no smaller fallback

`DefaultParametersSparseLCR` contains only LogN=16 sets. The one LogN=15
set, `DefaultParametersSparse[3]`, fails to construct:

```
cannot NewParametersFromLiteral: Q[0]=8589475841 != 1 mod NthRoot=131072
```

**and fails identically on upstream v6.1.0** — a pre-existing lattigo defect
the fork inherited, not a fork regression.

Wall-clock comparison requires a host with >= 24-32 GB RAM.

---

## 6. Net position

| | status |
|---|---|
| +1 usable level at constant budget | **verified** |
| 2.17x key count, 2.39x storage | **verified, structurally fixed** |
| ~5x transient keygen memory | **verified, upstream's not the fork's** |
| Q-only multiply beats QP | **unmeasured** |
| flat d automorphisms beat BSGS sqrt(d) | **unmeasured** |
| net wall-clock speedup | **unmeasured, and unmeasurable with the shipped harness** |

The costs are measured and fixed. The benefit is unquantified. On what has
actually been demonstrated, this trades a known 2.17x key blowup for a known
+1 level, with the arithmetic saving still to be shown.

---

## Reproduction

```bash
GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 --branch lcr \
  https://github.com/Fainabi/lattigo-lcr-aks /tmp/lcr
git -C /tmp/lcr rev-parse HEAD   # must be 3fbe5c8eeeea9ee127d074915d909a18c2a0f9d4
```

Level table (section 3) — drop this in
`circuits/ckks/bootstrapping/zz_lvl_test.go` and run
`go test ./circuits/ckks/bootstrapping/ -run TestZZLevels -v`:

```go
package bootstrapping

import (
	"fmt"
	"testing"

	"github.com/tuneinsight/lattigo/v6/schemes/ckks"
)

func TestZZLevels(t *testing.T) {
	row := func(tag string, ps defaultParametersLiteral, lc bool) {
		if lc {
			ps.BootstrappingParams.LevelConserved = true
			ps.BootstrappingParams.AggregatedFlags = []int{}
		}
		params, err := ckks.NewParametersFromLiteral(ps.SchemeParams)
		if err != nil {
			t.Fatalf("%s: %v", tag, err)
		}
		btp, err := NewParametersFromLiteral(params, ps.BootstrappingParams)
		if err != nil {
			t.Fatalf("%s: %v", tag, err)
		}
		t.Logf("%-9s residualMax=%2d btpMax=%2d C2S.LevelQ=%2d S2C.LevelQ=%2d btpDepth=%2d",
			tag, btp.ResidualParameters.MaxLevel(),
			btp.BootstrappingParameters.MaxLevel(),
			btp.CoeffsToSlotsParameters.LevelQ,
			btp.SlotsToCoeffsParameters.LevelQ,
			btp.BootstrappingParameters.MaxLevel()-btp.ResidualParameters.MaxLevel())
	}
	for i := 0; i < 3; i++ {
		row(fmt.Sprintf("stock[%d]", i), DefaultParametersSparse[i], false)
		row(fmt.Sprintf("LCR[%d]", i), DefaultParametersSparseLCR[i], true)
	}
}
```

Key counts (section 4) need `initializeWithoutEvk`, so the probe must live
inside package `bootstrapping`. Count `len(m.Vec)` over
`ev.C2SDFTMatrix.Matrices`, compare `btp.GaloisElements(params)` against
`btp.GaloisElementsRemoveAggregatedFlags(params, flags)`, and size one key
with `kgen.GenGaloisKeyNew(galEl, sk).BinarySize()`.
