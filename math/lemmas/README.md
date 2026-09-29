# Lemmas

A lemma here is a file that states **one small supporting fact** used as a step
toward other results (the owner's rule, 2026-09-29). Everything else stays in
`math/theorems/`.

How the 13 were chosen: all 237 files labelled `# CLASS: THEOREM` were read
against that rule; when unsure, a file stayed a theorem. A mention in an index or
list did not count as use. `primitive_root_test.py` was proposed and held back
for that reason (its only mention elsewhere is a listing).

| File | The fact | Used by |
|---|---|---|
| `decimal_trinity.py` | ord_37(10)=3, so <10>={1,10,26}=H_3 | twin_gap_dr_chain.py, nines_complement_sa_h.py (T389) |
| `heartbeat_3cycle.py` | ord_37(26)=3, so every nonzero residue lies in a 3-cycle of the 137-map | engine_integration.py step 12, T316 |
| `verify_local_confluence.py` | Diamond property holds on 144-state lattice, zero counterexamples | one_over_137_framework.md layer 38 (Newman's Lemma) |
| `sigma3_eisenstein_gf37.py` | For prime p, 37 | sigma_3(p) iff p = 11, 27, 36 mod 37 | T262 (theorem_262_e8_theta_mod37.py) |
| `abcabc_mod37_orbit.py` | ABCABC = 1001*ABC ≡ 2*ABC (mod 37); orbit walks all of (Z/37)* since 2 primitive | cylicamp/engine_integration.py (step 9); compact_generation.py |
| `cycle_partition_37.py` | Every 137-map 3-cycle sums to 37 or 74, six of each | orbit sum results (orbit_negation_duality, T331/T332) |
| `intersection_cycle_theorem.py` | (3,4,30) is the only 137-map 3-cycle with all elements in SA∪ST | sovereign classification (medusa_v3_sovereign) |
| `sovereign_fixed_point.py` | Two classification branches unreachable because 26n mod 37 is a bijection | medusa_v3_sovereign.py |
| `theorem_310_digit_chain_seam_gf37.py` | aba with a=b is 111a ≡ 0 mod 37 for every digit a | T311, T312, T315 |
| `twin_prime_dr_pair.py` | Twin pair (6m-1,6m+1): DR pair is (8,1),(5,7),(2,4) as m = 0,1,2 mod 3 | T336 |
| `two_group_split.py` | Each 137-map 3-cycle sums to 37 or 74; six cycles each | cycle_symmetry_maps.py |
| `theorem_283_negation_antipodal_gf37.py` | The six antipodal orbit pairs are exactly the negation pairs x -> -x mod 37 | T284, T285, T303 |
| `theorem_313_add_nine_reversal_diagonal_gf37.py` | For two-digit n, n+9=rev(n) iff b=a+1: exactly 12,23,...,89 | T314 |

Note: `cycle_partition_37.py` and `two_group_split.py` state the same fact
(every 3-cycle of x -> 26x sums to 37 or 74, six of each).

Moving these files did not change any output: the 13 files and every Python file
that refers to them (22 in all) gave identical output before and after.
