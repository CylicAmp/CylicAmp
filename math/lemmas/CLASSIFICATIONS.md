# Three classifications of the 237 THEOREM-labelled files, side by side

None of the three is treated as the answer. The folder layout can hold only one
arrangement; the three verdicts for every file are in `classifications.json`.

| Method | How | Lemmas |
|---|---|---|
| **Import graph** | a file is a lemma if another file imports it (machine, from the code) | 2 |
| **Named by the owner** | a file is a lemma if the owner names it | 0 (none named) |
| **Reading** | a file is a lemma if it states one small fact used as a step toward other results (six reviewers read every file; held back when unsure or when the only mention is a listing) | 13 |

Agreement: every import-graph lemma is also a reading lemma (abcabc_mod37_orbit.py, heartbeat_3cycle.py).
The reading method finds 11 more; the import graph misses them because
files in this repo build on each other by citing results in their text, not by
importing code.

Folder layout follows the fourth method below (7 files in `math/lemmas/`).

## Every file any method calls a lemma

| File | Import graph | Reading | Folder |
|---|---|---|---|
| `abcabc_mod37_orbit.py` | LEMMA | LEMMA | math/lemmas |
| `heartbeat_3cycle.py` | LEMMA | LEMMA | math/lemmas |
| `cycle_partition_37.py` | THEOREM | LEMMA | math/lemmas |
| `decimal_trinity.py` | THEOREM | LEMMA | math/lemmas |
| `intersection_cycle_theorem.py` | THEOREM | LEMMA | math/lemmas |
| `sigma3_eisenstein_gf37.py` | THEOREM | LEMMA | math/lemmas |
| `sovereign_fixed_point.py` | THEOREM | LEMMA | math/lemmas |
| `theorem_283_negation_antipodal_gf37.py` | THEOREM | LEMMA | math/lemmas |
| `theorem_310_digit_chain_seam_gf37.py` | THEOREM | LEMMA | math/lemmas |
| `theorem_313_add_nine_reversal_diagonal_gf37.py` | THEOREM | LEMMA | math/lemmas |
| `twin_prime_dr_pair.py` | THEOREM | LEMMA | math/lemmas |
| `two_group_split.py` | THEOREM | LEMMA | math/lemmas |
| `verify_local_confluence.py` | THEOREM | LEMMA | math/lemmas |

The other 224 files are THEOREM under all three methods.

## Fourth method, from comparing the three (added 2026-09-29)

**Reading + cited:** a lemma is a file the reading method calls a small single
fact AND that another result file names (by filename or T-number; index and map
files do not count). This joins the reading method's judgement with a check a
machine can repeat. 7 lemmas:

| File | Cited by |
|---|---|
| `abcabc_mod37_orbit.py` | 1: engine_integration.py |
| `heartbeat_3cycle.py` | 2: engine_integration.py, theorem_316_t120_seed_class_mod_333_gf37.py |
| `sigma3_eisenstein_gf37.py` | 1: theorem_424_rewrite_certificate_ledger_gf37.py |
| `theorem_283_negation_antipodal_gf37.py` | 13: theorem_284_operator_group_gf37.py, theorem_285_quotient_group_z12_gf37.py, theorem_286_subgroup_lattice_z12_gf37.py, theorem_287_anomalous_curve_orbit_partition.py |
| `theorem_310_digit_chain_seam_gf37.py` | 4: theorem_311_triad_lock_and_subgrid_map_gf37.py, theorem_312_repdigit_chain_complete_gf37.py, theorem_315_base_ten_block_and_cofactor_gf37.py, thread_session_connections.py |
| `theorem_313_add_nine_reversal_diagonal_gf37.py` | 2: theorem_314_twelve_double_closure_gf37.py, theorem_315_base_ten_block_and_cofactor_gf37.py |
| `twin_prime_dr_pair.py` | 2: test_prime_engine.py, twin_prime_tripartite_audit.py |

The other 6 reading lemmas (`cycle_partition_37`, `two_group_split`,
`decimal_trinity`, `intersection_cycle_theorem`, `sovereign_fixed_point`,
`verify_local_confluence`) are named by no other result file, so "used as a
step" is not shown for them. They were moved back to `math/theorems/` on
2026-09-29; the 22 files that refer to them produced identical output before and after.
