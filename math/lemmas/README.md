# Lemmas

A lemma here is a file that states **one small supporting fact** used as a step
toward other results. This wording was written by Claude as one of three
options offered on 2026-09-29; the owner selected it. Everything else stays in
`math/theorems/`.

How these were chosen: all 237 files labelled `# CLASS: THEOREM` were read
against that rule; when unsure, a file stayed a theorem. A mention in an index or
list did not count as use. `primitive_root_test.py` was proposed and held back
for that reason (its only mention elsewhere is a listing).

| File | The fact | Used by |
|---|---|---|
| `heartbeat_3cycle.py` | ord_37(26)=3, so every nonzero residue lies in a 3-cycle of the 137-map | engine_integration.py step 12, T316 |
| `sigma3_eisenstein_gf37.py` | For prime p, 37 | sigma_3(p) iff p = 11, 27, 36 mod 37 | T262 (theorem_262_e8_theta_mod37.py) |
| `abcabc_mod37_orbit.py` | ABCABC = 1001*ABC ≡ 2*ABC (mod 37); orbit walks all of (Z/37)* since 2 primitive | cylicamp/engine_integration.py (step 9); compact_generation.py |
| `theorem_310_digit_chain_seam_gf37.py` | aba with a=b is 111a ≡ 0 mod 37 for every digit a | T311, T312, T315 |
| `twin_prime_dr_pair.py` | Twin pair (6m-1,6m+1): DR pair is (8,1),(5,7),(2,4) as m = 0,1,2 mod 3 | T336 |
| `theorem_283_negation_antipodal_gf37.py` | The six antipodal orbit pairs are exactly the negation pairs x -> -x mod 37 | T284, T285, T303 |
| `theorem_313_add_nine_reversal_diagonal_gf37.py` | For two-digit n, n+9=rev(n) iff b=a+1: exactly 12,23,...,89 | T314 |

Moving these files did not change any output: the 13 files and every Python file
that refers to them (22 in all) gave identical output before and after.

**Revised 2026-09-29:** only files that another result names by filename or
T-number stay here (7). Six more read as small facts but no other file cites
them; they are back in `math/theorems/`. See CLASSIFICATIONS.md.
