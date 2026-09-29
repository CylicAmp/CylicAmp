# Lemmas

A lemma here is a file that states **one small supporting fact** used as a step
toward other results. This wording was written by Claude as one of three
options offered on 2026-09-29; the owner selected it. Everything else stays in
`math/theorems/`.

How these were chosen: all 237 files labelled `# CLASS: THEOREM` were read
against that rule; when unsure, a file stayed a theorem. A mention in an index or
list did not count as use. `primitive_root_test.py` was proposed and held back
for that reason (its only mention elsewhere is a listing).

| File | The fact | Cited by (checked in the repo) |
|---|---|---|
| `heartbeat_3cycle.py` | ord_37(26)=3, so every nonzero residue lies in a 3-cycle of the 137-map | engine_integration.py, theorem_316_t120_seed_class_mod_333_gf37.py |
| `sigma3_eisenstein_gf37.py` | For prime p, 37 | sigma_3(p) iff p = 11, 27, 36 mod 37 | theorem_424_rewrite_certificate_ledger_gf37.py |
| `abcabc_mod37_orbit.py` | ABCABC = 1001*ABC ≡ 2*ABC (mod 37); orbit walks all of (Z/37)* since 2 primitive | engine_integration.py |
| `theorem_310_digit_chain_seam_gf37.py` | aba with a=b is 111a ≡ 0 mod 37 for every digit a | theorem_311_triad_lock_and_subgrid_map_gf37.py, theorem_312_repdigit_chain_complete_gf37.py, theorem_315_base_ten_block_and_cofactor_gf37.py, thread_session_connections.py |
| `twin_prime_dr_pair.py` | Twin pair (6m-1,6m+1): DR pair is (8,1),(5,7),(2,4) as m = 0,1,2 mod 3 | test_prime_engine.py, twin_prime_tripartite_audit.py |
| `theorem_283_negation_antipodal_gf37.py` | The six antipodal orbit pairs are exactly the negation pairs x -> -x mod 37 | theorem_284_operator_group_gf37.py, theorem_285_quotient_group_z12_gf37.py, theorem_286_subgroup_lattice_z12_gf37.py, theorem_287_anomalous_curve_orbit_partition.py, theorem_288_j0_isomorphism_classes_gf37.py, theorem_291_iterated_squaring_sylow3_gf37.py, theorem_296_36gon_rotation_model.py, theorem_297_block_separation.py, theorem_301_cyclotomic_slot_table.py, theorem_303_block_map_is_27.py, theorem_304_three_lists_meet_at_37.py, theorem_331_orbit_sum_37_74_negation_gf37.py, theorem_332_six_six_forced_inversion_closed_gf37.py |
| `theorem_313_add_nine_reversal_diagonal_gf37.py` | For two-digit n, n+9=rev(n) iff b=a+1: exactly 12,23,...,89 | theorem_314_twelve_double_closure_gf37.py, theorem_315_base_ten_block_and_cofactor_gf37.py |

Moving files in and out of this folder did not change any output: every Python
file involved gave identical output before and after each move.

**Revised 2026-09-29:** only files that another result names by filename or
T-number stay here (7). Six more read as small facts but no other file cites
them; they are back in `math/theorems/`. See CLASSIFICATIONS.md.
