# family_search (Rust port of the T245 proper-divisor family search)

Line-for-line port of the Python search (read-off of large primes, surplus-is-final
prune, primorial-gcd read-off below R = 1e6). Validated against Python by
IDENTICAL node counts and member sets:

| M    | depth | items  | nodes        | members |
|------|-------|--------|--------------|---------|
| 1e12 | 5     | 38 391 | 1 832 796    | 26      |
| 1e14 | 5     | 59 720 | 37 450 482   | 55      |
| 1e16 | 5     | 90 118 | 300 318 563  | 95      |

Build: `cargo build --release`. Table: `python3 make_table.py 1e22` (prime factors
>= 250 of sigma_2(p^e), p < 250). Run: `family_search <M> <depth> <state> [seed]`,
seed = supply cycle as `[[p,e],...]`. Resumable: rerun with the same state file.
Depth must satisfy 60 * 250^(depth+1) > M (depth 7 for 1e20, 8 for 1e22), and
completeness also needs the supply-cycle seeds (T245, "cycles").

## Build-flag note (verified 2026-09-28 on this environment's CPU: avx512f/dq/bw/vl/vnni, 4 cores, gcc 13.3)
gcc `-O3 -march=native -ffast-math` emits **no zmm** for a simple reduction (default
`-mprefer-vector-width=256`); `-mprefer-vector-width=512` enables zmm. For rustc the
analogous knob is `-C target-cpu=native` plus `-C target-feature=+avx512f`; this crate's
hot loop is big-integer and branchy, so it has not been tuned for SIMD width.
