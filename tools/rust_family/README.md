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
