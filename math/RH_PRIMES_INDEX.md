# Riemann Hypothesis & Primes — File Index

All work listed here is connected through the same underlying system:
digital roots, mod 37 structure, and the URI framework.

---

## Riemann Hypothesis / Zeta Function

### Core files

| File | Location |
|---|---|
| `riemann_zeta_zeros.py` | math/primes/ |
| `riemann_first_zero_141.py` | math/theorems/ |
| `rh_reverse_audit.py` | math/theorems/ |
| `gue_riemann_zeros_audit.py` | math/theorems/ |
| `berry_keating_gue_audit.py` | math/theorems/ |
| `odlyzko_schonhage_audit.py` | math/theorems/ |
| `explicit_formula.py` | math/theorems/ |
| `t_phi_zeta_determinant.py` | math/theorems/ |
| `t_phi_spectral_audit.py` | math/theorems/ |
| `paper_spectral_audit.py` | math/theorems/ |
| `infinity_proof_roadmap.py` | math/theorems/ |
| `layered_framework_zeta_prime.tex` | math/papers/ |

### MWS framework (sections 16–21)

| File | Location | Sections |
|---|---|---|
| `mws_framework_verified.py` | math/theorems/ | Zeta zeros, off-line gap, chiasm proof, 2-factor symmetry |
| `mws_pure_math_extract.py` | math/theorems/ | Same, interpretation removed |

### Liouville / prime parity (bridge between primes and zeta)

| File | Location |
|---|---|
| `liouville_parity_audit.py` | math/theorems/ |
| `chi2_cancellation_proof.py` | math/theorems/ |
| `chi2_phi3_proof_audit.py` | math/theorems/ |

---

## Primes

### Core engine (math/primes/)

| File | Purpose |
|---|---|
| `prime_engine.py` | Main prime computation engine |
| `core.py` | Core routines |
| `main.py` | Entry point |
| `alpha_grid.py` | Alpha grid structure |
| `dgm_hyperagent_37field.py` | 37-field hyperagent |
| `modal_crossing_orbit.py` | Modal crossing |
| `repunit_sequence.py` | Repunit sequences |
| `verify_dr9_termination.py` | DR9 termination verification |
| `verify_local_confluence.py` | Local confluence |

### Emirp / 37×73 structure (math/theorems/)

| File |
|---|
| `emirp_digit_aware_baseline.py` |
| `emirp_five_moduli_zscores.py` |
| `emirp_gap_spectral_dr.py` |
| `emirp_k_mod37.py` |
| `emirp_mod37_spectral_audit.py` |
| `emirp_moduli_comparison.py` |
| `emirp_moduli_comparison_audit.py` |
| `crt_emirp_null_model_audit.py` |
| `z2701_37x73_qed.py` |

### Twin primes (math/theorems/)

| File |
|---|
| `twin_prime_hl_audit.py` |
| `twin_prime_markov_audit.py` |
| `twin_prime_tripartite_audit.py` |
| `euler_quadratic_twin_audit.py` |

### Prime distribution / gaps (math/theorems/)

| File |
|---|
| `prime_delta23_audit.py` |
| `prime_gap_dr_audit.py` |
| `prime_gap_fold_audit.py` |
| `prime_dr_append_audit.py` |
| `prime_dr_append_layer3_audit.py` |
| `prime_dr_unification.py` |
| `prime_sieve_dr_audit.py` |
| `prime_insertion_sequence_audit.py` |
| `sieve_rank_audit.py` |
| `fixed_point_sieve_audit.py` |
| `linear_form_11n_37m_primes.py` |
| `arithmetic_progression_37field.py` |

### Primality / special primes (math/theorems/)

| File |
|---|
| `primality_10343_audit.py` |
| `primorial_mirror_audit.py` |
| `repunit_prime_entry.py` |
| `pseudoprime_audit.py` |
| `carmichael_dr_audit.py` |
| `carmichael_wheel_tier_audit.py` |
| `korselt_proof_audit.py` |
| `erdos_primitive_set_bound.py` |
| `eisenstein_primes.py` |
| `sphenic_191919919191_audit.py` |
| `sphenic_happy_371113.py` |
| `primes_751_palindromes.py` |
| `primes_23_extended_audit.py` |
| `primes_digits_23_audit.py` |

### Ulam / quadratic forms (math/theorems/)

| File |
|---|
| `ulam_quadratic_k5000_audit.py` |
| `leveling_ulam_audit.py` |
| `quadratic_classnum_audit.py` |

---

## Connection Points

The following files explicitly bridge primes and the Riemann hypothesis
through the same modular and digital root framework:

| File | Bridge |
|---|---|
| `explicit_formula.py` | Explicit formula connecting zeros to prime counting |
| `liouville_parity_audit.py` | L(x) parity connects prime factorization to zeta |
| `harmonic_prime_matrix_audit.py` | Harmonic structure over primes |
| `dr_modular_foundation.py` | Digital root foundation used across both |
| `uri_framework_audit.py` | Universal Reduction Invariant — the spine |
| `mws_pure_math_extract.py` | L(T(37)), L(T(73)), zeta zeros, 2-factor symmetry |

---

## Papers

| File | Location |
|---|---|
| `layered_framework_zeta_prime.tex` | math/papers/ |
| `Audit_Synthesis_Report.pdf` | math/theorems/ |
| `theorem28_forensic_analysis.md` | math/theorems/ |
| `one_over_137_framework.md` | math/primes/ |
| `euler_totient_verified.md` | math/primes/ |
