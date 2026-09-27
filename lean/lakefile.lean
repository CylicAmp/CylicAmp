import Lake
open Lake DSL

package «CylicAmp» where
  name := "CylicAmp"

require mathlib from git
  "https://github.com/leanprover-community/mathlib4" @ "v4.14.0"

lean_lib «CylicAmp» where
  roots := #[`CylicAmp]
