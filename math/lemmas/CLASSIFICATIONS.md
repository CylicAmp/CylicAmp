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

Current folder layout follows the reading method (13 files in `math/lemmas/`).

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
