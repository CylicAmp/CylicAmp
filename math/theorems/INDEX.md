# Theorem Index — CylicAmp Math Library

280 files. This index maps every file to what it does and groups related work together.

---

## CORE FOUNDATIONS

| File | What it does |
|------|-------------|
| dr_fixed_point_mod9.py | DR(n) = 1+(n-1)%9; DR(0)=0; all {1..9} are fixed points; DR=9 iff 9\|n |
| dr_algebra.py | Closed algebra on DR classes — addition and multiplication tables mod 9 |
| dr_modular_foundation.py | Foundational DR modular arithmetic |
| dr_number_theory_module.py | DR number theory module — reusable functions |
| dr_pattern_suite.py | DR in base 10: dr(n) = 1+(n-1)%9 |
| ds_congruence_mod9.py | DS(n) ≡ n (mod 9) — digit sum congruence proof |
| master_record_dr_audit.py | Master record of DR identities |

---

## PRIME STRUCTURE

| File | What it does |
|------|-------------|
| twin_prime_tripartite_audit.py | DR pairs (2,4)(5,7)(8,1) — proven exhaustive for p>3 |
| twin_prime_hl_audit.py | Hardy-Littlewood C₂=0.6601618; π₂(10⁶)=8169 verified |
| twin_prime_markov_audit.py | 3×3 transition matrix; MI=0.003820 bits; tracks near-independent |
| prime_dr_append_audit.py | p→p\|\|DR(p): two layers, all factorizations verified; fold-back 437=19×23, 731=17×43 |
| mersenne_dr_audit.py | DR(2^p-1) determined by p%6; DR∈{1,3,4,7} only; 5 DRs excluded |
| mersenne_dr9_period6_theorem.py | Mersenne DR period-6 theorem |
| mersenne_digit_boundary_analysis.py | Mersenne digit boundary analysis |
| mersenne_dr_boundary_53_54.py | Mersenne DR boundary at exponents 53-54 |
| carmichael_wheel_tier_audit.py | W₃₇ eliminates 41/43 Carmichaels; survivors 252601, 410041 both T=68 |
| prime_dr_unification.py | Prime DR unification |
| prime_gap_dr_audit.py | Prime gap DR analysis |
| prime_gap_fold_audit.py | Prime gap fold structure |
| prime_delta23_audit.py | Prime delta-23 audit |
| plus2_chain_theorem.py | +2 chain theorem: consecutive pair collapse to twin primes |
| primes_23_extended_audit.py | {2,3}-digit prime extended audit |
| primes_digits_23_audit.py | Primes using only digits {2,3} — lengths 1 to 7 |
| primes_751_palindromes.py | Primes 751 and palindromes |
| primality_10343_audit.py | Primality investigation — 10343 |
| linear_form_11n_37m_primes.py | Frobenius(11,37)=359; first primes in linear form |
| crt_emirp_null_model_audit.py | Emirp null model audit |
| emirp_digit_aware_baseline.py | Emirp digit-aware baseline |
| emirp_five_moduli_zscores.py | Emirp five moduli z-scores |
| emirp_gap_spectral_dr.py | Emirp gap spectral DR |
| emirp_k_mod37.py | Emirp k mod37 |
| emirp_mod37_spectral_audit.py | Emirp mod37 spectral audit |
| emirp_moduli_comparison.py | Emirp moduli comparison |
| emirp_moduli_comparison_audit.py | Emirp moduli comparison audit |
| liouville_parity_audit.py | Liouville parity domain n=1..37 |
| explicit_formula.py | Explicit formula (prime counting) |
| erdos_primitive_set_bound.py | Erdős primitive set bound |

---

## TIER FUNCTION T(k) = DS(18k) + DS(18k-4)

| File | What it does |
|------|-------------|
| tier_ds_18k_distribution.py | T(k)≡5(mod 9) for all k≥1; proven |
| layer30_dr_matrix_entropy.py | Layer 30: 9×9 DR multiplication matrix and DR orbit entropy |

---

## MOD-37 / F₃₇ FIELD STRUCTURE

| File | What it does |
|------|-------------|
| f26_fixed_point_mod37.py | Fixed point theorem for f(n)=(26n)%37 |
| f26_order3_cycles_mod37.py | 3-cycles under the 137/37 map: universal order-3 theorem |
| f26_anchor_target_architecture.py | F26 anchor/target architecture under f(n)=(26n)%37 |
| f26_binary_classifier.py | F26 binary classifier |
| f26_dr3_anchors_mod37.py | DR=3 anchor scan under f(n)=(26n)%37 |
| f26_pillar_verification.py | F26 pillar verification — 137/37 packet verification |
| f26_pillars_jacobian.py | F26 pillar verification v2.5 + Jacobian wobble test |
| f26_qr_closure_mod37.py | F26 QR closure theorem |
| f37_hexagonal_decomposition_audit.py | F₃₇× hexagonal decomposition — full algebraic structure |
| f37_subgroup_audit.py | F₃₇× subgroup theory: ⟨27⟩ and the 37-family law |
| f37_subgroup_structure_audit.py | F₃₇ subgroup structure audit |
| primitive_roots_mod37.py | Primitive roots mod 37 — structural audit |
| mirror_table_mod37_audit.py | Mirror table audit — subgroup ⟨27⟩ ⊂ ℤ/37ℤ |
| arithmetic_progression_37field.py | Arithmetic progression on Z/37Z — field collapse and 1/9 attractor |
| circulant_avg_37.py | Circulant average mod 37 |
| cycle_partition_37.py | Cycle partition mod 37 |
| dr5_mod37_ap_audit.py | DR=5 arithmetic progression in mod-37 |
| freq_37field_555_2220.py | Frequency 37-field 555/2220 |
| collision_node_20979.py | 20979=3⁴×7×37; DS=27; DR=9; DR(37k)=DR(k) identity |
| z2701_37x73_qed.py | 2701=37×73 — triangle number, DR identity, QED α connections |
| lob_26_collatz_f37.py | LoB 26 — Collatz map T in F₃₇ |
| mult_by_2_orbit_audit.py | Multiplication-by-2 orbit audit — ⟨27⟩ ⊂ F₃₇ |
| spoke_enumeration_ab_audit.py | Spoke enumeration audit — valid AB pairs per spoke in ⟨27⟩ ⊂ F₃₇ |
| toroidal_projection.py | Theorem 28: toroidal projection of F26 anchors |
| fps37_scanner.py | FPS-37 scanner — LoB 23/23b |
| emirp_k_mod37.py | Emirp k mod37 |
| collatz_mod37_basin.py | Collatz mod37 basin |
| dimensional_bridge.py | 37φ dimensional bridge — computational verification |
| string_duality_37phi_bridge.py | String duality audit — 37φ bridge under T-duality |

---

## DIGITAL ROOT CHAINS & SEQUENCES

| File | What it does |
|------|-------------|
| fibonacci_dr_chain_audit.py | Fibonacci–DR–Cunningham–AP chain |
| layer54_lucas_period24.py | Lucas period-24 mod 9 |
| layer56_period_minimality_audit.py | Period minimality audit |
| layer58_pisano_period9.py | Pisano period mod 9 |
| layer59_fib_oscillation_mtheory.py | Fibonacci DR-oscillation + M-theory extension |
| layer62_lucas_period_mod9.py | Lucas period minimality mod 9 proof |
| layer64_fib_lucas_comparison.py | Lucas vs Fibonacci period comparison |
| fib_mod90_audit.py | Fibonacci mod 90 audit |
| pisano_period_333.py | Pisano period 333 |
| lucas_abbc_chain.py | Lucas ABBC chain |
| lcm_convergence_dr_cycle.py | LCM convergence and DR cycle |
| digit_cycles_1_9.py | Digit cycles 1 through 9 |
| multiplication_dr_chains_audit.py | Multiplication DR chains — seeds 2,3,4,5 |
| hybrid_recurrence_16_96_audit.py | Hybrid recurrence audit — 16,32,48,64,96 |
| sequence_1111_cycle_1210.py | Sequence 1111 cycle 1210 |
| sequence_30303_doubling.py | Sequence 30303 doubling |
| arithmetic_sequence_1111.py | Arithmetic sequence with common difference -1111 |
| ladder_11_111.py | Ladder 11→111 |
| pair_addition_dr_switch.py | Pair addition: even sum → odd DR switch at n=5 |

---

## ZERO-COMMA LABEL SYSTEM

| File | What it does |
|------|-------------|
| zero_comma_complete_theorem.py | Complete zero-comma theorem |
| zero_comma_label_system.py | Zero-comma label system |
| zero_comma_label_v2.py | Zero-comma label system v2: uniform suffix |
| one_zeros_nine_pattern.py | One-zeros-nine pattern |
| odd_perfect_zero_system.py | Odd perfect zero-decimal system: comma group parity analysis |

---

## COLLATZ

| File | What it does |
|------|-------------|
| collatz_v2_equidistribution.py | Collatz v2 equidistribution |
| collatz_mod37_basin.py | Collatz mod37 basin |
| lob_26_collatz_f37.py | Collatz map T in F₃₇ |
| infinity_proof_roadmap.py | Infinity proof roadmap |

---

## GROUP THEORY & ALGEBRA

| File | What it does |
|------|-------------|
| group_G54_structure.py | Group G=⟨x,y|x⁹=y⁶=1, yxy⁻¹=x⁴⟩ — complete structural theorem |
| g54_character_theory_audit.py | G54 character theory audit |
| klein4_z2_orbit_audit.py | Klein four-group action on Mat₃(F₂) — corrected orbit count |
| parity_proof_z2_audit.py | Refined parity proof — σ_p vs σ_a on Mat₃(Z₂) |
| todd_coxeter_c2c3_audit.py | Todd-Coxeter coset enumeration: G=⟨a,b|a²,b³⟩ |
| smith_normal_form_z26.py | Smith normal form over Z/nZ — modular kernel verifier |
| dr_matrix_9x9_audit.py | DR 9×9 multiplication matrix; period-24 Fibonacci/Lucas DRs |
| dr_matrix_v2_snf_audit.py | DR matrix v2 SNF audit |
| dr_matrix_v3_snf_audit.py | F26 matrix v3 SNF audit |
| block_cayley_spectral_audit.py | Block Cayley spectral audit |
| ramsey_survey_audit.py | Ramsey survey audit |
| steiner_systems_framework.py | Steiner systems — five-section framework |

---

## E8 / LATTICE / HIGH-DIMENSIONAL

| File | What it does |
|------|-------------|
| e8_cartan_audit.py | E8 Cartan audit |
| e8_coset_incidence.py | E8 coset incidence |
| e8_framework_glossary.py | E8 framework glossary |
| h4_e8_spectral_audit.py | H4/E8 spectral audit |
| cosmogram_e8_audit.py | Cosmogram E8 audit |
| v600_programme.py | V600 programme — binary icosahedral group, E8, cosmological tension |
| hexacosichoron_600cell.py | Hexacosichoron (600-cell) — 4D regular polytope vertex generator |
| clifford_fibration_audit.py | Clifford parallelism and Hopf fibration audit — 600-cell |
| d4_600cell_latin_square_audit.py | D4/600-cell Latin square audit |
| chiral_manifold_c4d4_audit.py | Chiral manifold C4/D4 audit |
| abbc_manifold_grid.py | ABBC manifold grid structure |

---

## MODULAR & NUMBER THEORY

| File | What it does |
|------|-------------|
| cyclic142857_audit.py | Cyclic 142857 audit |
| cyclic_142857.py | 142857 cyclic number |
| kaprekar_6174.py | Kaprekar's routine — 6174 |
| kaprekar_2481_1572_3693.py | Kaprekar 2481/1572/3693 |
| pell_10101_audit.py | Pell equation x²-10101y²=1: fundamental unit |
| eisenstein_primes.py | Norm of a+bω — Eisenstein primes |
| cunningham_modulus_audit.py | Cunningham chain investigation + modulus field invariance |
| repunit_prime_entry.py | Repunit prime entry |
| palindrome_1888081808881.py | Palindrome analysis: 1888081808881 |
| palindrome_cipher_37R.py | Palindrome cipher 37R |
| palindrome_diamond_audit.py | Palindrome diamond audit |
| palindrome_divisors_ord10_audit.py | Palindrome divisors ord-10 audit |
| perfect_numbers_137.py | Perfect numbers and 137 |
| sphenic_191919919191_audit.py | Structural audit — 191919919191 |
| sphenic_happy_371113.py | Structural audit — 371113 (sphenic + happy) |
| digital_root_table_audit.py | Digital root table audit |
| mirror_set_generator.py | Mirror set generator — 9-invariant permutation theorem |
| mirror_triplet_cascade.py | Mirror triplet cascade |
| mod12_collision_audit.py | Mod-12 collision audit |
| mod9_11k_44k_audit.py | Mod-9 analysis of 11k and 44k |
| mod9_midpoint.py | Mod-9 midpoint |
| bfs_attractor_mod9.py | BFS attractor mod 9 |
| dr_369_closure_mirror_audit.py | DR 3-6-9 closure mirror audit |
| digits_137_and_7.py | Digits 137 and 7 |
| digits_137_running_sum.py | Digits 137 running sum |
| fraction_103_137.py | Fraction 103/137 |
| fraction_1111_12800_audit.py | Binary/fraction audit — 0.086796875 = 1111/12800 |
| continued_fraction_R3252.py | Continued fraction evaluation: R=0.3252=813/2500 |
| continued_fractions_audit.py | Continued fractions audit |
| log2_sqrt5_audit.py | log₂(√5) audit |
| parabolic_spear_audit.py | Parabolic spear: P(n)=n(10-n) — verified properties |
| permutation_dr_99.py | Permutation DR mod 99 |
| sequence_permutation_audit.py | Sequence permutation audit |
| parity_diamond_9x9.py | Layer 21 — 9×9 parity grid: O/E diamond |
| origami_fold_1_to_9.py | Origami fold 1 to 9 |
| triangular_partition_audit.py | Triangular partition audit |
| cumsum_correction_audit.py | Cumsum correction audit |
| cumsum_triangle_audit.py | Cumsum triangle audit |
| scalar_triad_137_248_359.py | Scalar triad 137/248/359 |

---

## CIPHER / KYBER / CRYPTOGRAPHIC

| File | What it does |
|------|-------------|
| cipher_42128_audit.py | Cipher 42128 audit |
| kyber_ntt_coset_audit.py | Kyber/ML-KEM NTT parameter audit |
| kyber_ring_mlkem_audit.py | Kyber ring R_q and ML-KEM pipeline audit |
| v4_orbit_kyber_audit.py | V4 orbit automaton vs ML-KEM cyclic subgroup ⟨17⟩ ⊆ (Z/3329Z)× |
| index13_resonance_audit.py | Index-13 resonance: F₃₇ (Pisot) vs (Z/3329Z)× (ML-KEM) |

---

## RIEMANN / SPECTRAL / GUE

| File | What it does |
|------|-------------|
| riemann_first_zero_141.py | Riemann first zero 141 |
| rh_reverse_audit.py | Riemann hypothesis reverse audit |
| gue_r3_audit.py | GUE R3 audit |
| gue_riemann_zeros_audit.py | GUE statistics audit — Riemann zeros vs Z/26Z kernel |
| berry_keating_gue_audit.py | Berry-Keating GUE audit |
| odlyzko_schonhage_audit.py | Odlyzko-Schönhage audit |
| paper_spectral_audit.py | Paper spectral audit |
| ramanujan_modular_audit.py | Ramanujan modular equations — claim audit + CF of ψ |
| agm_theta_elliptic_audit.py | AGM theta elliptic audit |
| jacobi_theta_cascade_audit.py | Jacobi theta cascade audit |
| adelic_valuation_audit.py | Adelic valuation audit |
| explicit_formula.py | Explicit formula (prime counting) |

---

## GEOMETRIC / SPIRAL / LATTICE

| File | What it does |
|------|-------------|
| rotational_spiral_analyzer.py | Rotational spiral analyzer — 3×3 circulant topology |
| fractal_grid_parity_audit.py | Fractal grid and parity invariance audit |
| lsystem_fractal_audit.py | L-system fractal audit |
| constellation_mirror_audit.py | Constellation mirror audit |
| embedding_phase_orbit_audit.py | Embedding rule, phase law, and modular orbit analysis |
| golden_path_sequence.py | Golden path sequence — eternal rule |
| layer_trinity_factor_lattice.py | Layer trinity factor lattice |
| source_mirror_manifold_396.py | SOURCE-MIRROR-CHANNEL manifold — 3-9-6 metronome framework |
| root_grid_dr6_dr7.py | Root grid theorem — DR classes 6 and 7 |

---

## PHYSICS / SCALING / DIMENSIONAL

| File | What it does |
|------|-------------|
| zero_space_stages1_3.py | Stages 1–3: zero-space foundation (10⁻³⁵ to 10⁻¹¹ m) |
| quantum_bio_bridge_stage4.py | Quantum-to-bio bridge stage 4 |
| hopf_stage6_human_scale.py | Stage 6: human scale / organisms (10⁻² to 10¹ m) |
| vireon_stage7_planetary.py | Stage 7: planetary scale |
| celestial_stages8_10.py | Stages 8–10: celestial / gate 18 singularity (10⁷ to 10²⁶ m) |
| bio_bridge_scaling_invariance.py | Quantum-to-bio bridge — scaling invariance, 37-filter, neural ODE, gate 18 |
| bio_harmonic_desync.py | Bio harmonic desync |
| neural_ode_stage5_cells.py | Neural ODE stage 5 — cells |
| delta27_heisenberg_neutrino.py | Delta-27 Heisenberg neutrino |
| phenomenological_effective_model_audit.py | Phenomenological effective model — digit-boundary mismatch drive |
| kepler_symplectic_audit.py | Kepler symplectic audit |
| coupled_oscillator_audit.py | Coupled oscillator audit |
| rossler_attractor_audit.py | Rössler attractor audit |
| planc_audit.py | Planck constant audit |
| qed_alpha_zα_structure.py | QED alpha Zα structure |
| apple_energy_audit.py | Apple energy audit |
| dim6_kernel_role_audit.py | Dimension-six kernel role — rigorous audit |
| cryo_em_hopf_lift_audit.py | Cryo-EM Hopf lift audit |
| g5_engine.py | G'5 engine — v∞ neural ODE full-spectrum simulation |

---

## FRAMEWORK / MASTER / LOB RECORDS

| File | What it does |
|------|-------------|
| cylicamp_master.py | CylicAmp master framework |
| master_137.py | Master 137 |
| master_framework_audit.py | Audit: complete master framework document — December 2025 |
| joy_framework_v25_2_audit.py | Joy framework v25.2 audit |
| joy_lob_45_6_correction_audit.py | Joy LoB 45.6 correction audit |
| lob_24c_errata.py | LoB 24c — errata correction record (MWS v37.20 → v37.21) |
| lob_25_legendre_applications.py | LoB 25 Legendre applications |
| lob_44_9_bilateral_369_lock.py | LoB 44.9 bilateral 3-6-9 lock |
| lob_591_592_595.py | LoB 591/592/595 |
| lob_596_600.py | LoB 596/600 — 3900 frequency check and F26 seal |
| lob_601_602_605.py | LoB 601/602/605 — inversion, trinity invariant, quiescence |
| lob_691_695.py | LoB 691/695 — AHL-8 vault and observer gap lock |
| lob_88_g_ord18_cycle.py | LoB 88 g ord18 cycle |
| lob_file_audit_recheck.py | LoB file audit recheck |
| closing_threads.py | Closing threads |
| errata_prevention_protocol.py | Errata prevention protocol |
| pattern_verification_audit.py | Pattern verification audit |
| claim_verification_audit.py | Claim verification audit |
| data_ledger_audit.py | Data ledger audit |
| modular_data_processor_audit.py | Modular data processor audit |
| modular_framework_audit.py | Modular framework audit |
| symmetry_correction_audit.py | Symmetry correction audit — scope restriction and sealed core |
| verify_dr9_termination.py | Layer 38: computational verification of DR=9 termination |
| verify_local_confluence.py | Layer 38 (cont.): computational verification of local confluence |
| allpaths_module2_seed.py | All paths module 2 seed |
| alpha_137_dr_extension.py | Alpha-137 DR extension |
| alpha_prime_inference_layer.py | Alpha prime inference layer |
| connection_7518.py | Connection 7518 |
| displacement_sync_13699631.py | Displacement sync 13699631 |
| dr_fingerprint_scraper.py | Digital root fingerprint scraper |
| m14_scraper_engine.py | M₁₄ multiset fingerprint engine |
| mc_sensitivity_analyzer.py | MC sensitivity analyzer |
| mc_sensitivity_audit.py | MC sensitivity audit |
| meromorphic_trajectory_map.py | Meromorphic trajectory map |
| mollified_orbit_engine.py | Mollified orbit engine |
| morowah_condition.py | Morowah condition — Chahine's S_d/S_p symmetry |
| node_verification_matrix_audit.py | Node verification matrix — DR, QR(13), sphenic, happy |
| structural_semantic_d_audit.py | Structural semantic D audit |
| fixed_point_sieve_audit.py | Fixed point sieve audit |
| ratchet_walk_audit.py | Ratchet walk audit |
| cycle_parity_audit.py | Cycle parity audit |
| eml_branch_cut_audit.py | EML branch cut audit |
| g4_construction_audit.py | G4 construction audit |
| g4_mackey_fourier_audit.py | G4 Mackey-Fourier audit |
| g4_parameter_sweep.py | G4 parameter sweep |
| g4_spectral_decomposition.py | G4 spectral decomposition |
| g4_stabilizer_geometry_audit.py | G4 stabilizer geometry audit |
| ib_vib_derivation_audit.py | IB/VIB derivation audit |
| t_phi_spectral_audit.py | T-phi spectral audit |
| t_phi_zeta_determinant.py | T-phi zeta determinant |
| conic_lame_audit.py | Conic Lamé audit |
| lame_projective_audit.py | Lamé projective audit |
| chi2_cancellation_proof.py | Chi-squared cancellation proof |
| chi2_phi3_proof_audit.py | Chi-squared phi³ proof audit |
| calign_definition_audit.py | C_Align definition audit |
| calign_derivation_audit.py | C_Align derivation audit — is √5−1/13 derivable from existing structure? |
| kernel5_construction_audit.py | Kernel-5 construction audit |
| kernel5_generators_audit.py | Kernel-5 generators audit |
| layer24_error_corrections_audit.py | Layer 24 error corrections audit |
| matrix_m_mod37_audit.py | Matrix M mod37 audit |
| field_55_mirror_structure.py | Field-55 mirror structure |
| q6_v4_burnside_edge_audit.py | Q6/V4 edge count: Burnside lemma audit |
| q6_v4_spectral_audit.py | Q6/V4 quotient graph: spectral and structural audit |
| pisot_sieve_audit.py | Pisot-powered integer sieve |
| phi_power_operator_precedence_audit.py | Phi power operator precedence audit |
| decimal_trade_extraction.py | Decimal trade extraction |
| resonance_row_1335.py | 17-point resonance row and 1335 partition invariant |
| theorem_infinite_666_resonances.py | Theorem: infinite resonances on every 666-track |
| equivalence_24_coupling.py | 24 equivalence pattern — coupling signature audit |
| law_of_12_period_audit.py | Law of 12 — two distinct phenomena |
| lob_88_g_ord18_cycle.py | LoB 88 g ord18 cycle |
| dds_ca_digit_audit.py | DDS CA digit audit |
| primorial_mirror_audit.py | Primorial mirror audit |
| dr_matrix_9x9_audit.py | DR 9×9 matrix; period-24 Fibonacci/Lucas; law of 12; checkerboard |
| percentage_matrix_node_progression_audit.py | Percentage matrix node progression audit |
| perceptual_hydrodynamics_v7.py | Perceptual hydrodynamics v7 — layer 24: hyperbolic color space |
| kalman_f26_closed_loop.py | Kalman F26 estimator — closed-loop Kalman control |
| shell_opacity.py | Shell opacity theorem: 100% inviolate |
| lob_file_audit_recheck.py | LoB file audit recheck |
