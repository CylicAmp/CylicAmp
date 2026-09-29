# Catalog of math/theorems and math/lemmas by kind of result

Every one of the 889 Python files, sorted into the kinds of mathematical object listed on 2026-09-29
(axioms, definitions, primitive notions, theorems, propositions, lemmas, corollaries, claims,
identities, formulas, counterexamples, paradoxes, algorithms, heuristics), plus Conjecture, Audit
(checks a claim from elsewhere) and Other. Files were not moved; this is a label layer.

How: eight reviewers read every file's docstring and assertions against fixed definitions.
Checked by machine: every Corollary names a parent result that exists in the repo; every
Counterexample names the statement it refutes. `CATALOG.json` has the full record per file
(primary, secondary, statement, evidence).

| Kind | Files |
|---|---|
| Axiom | 2 |
| PrimitiveNotion | 0 |
| Definition | 34 |
| Theorem | 106 |
| Proposition | 180 |
| Lemma | 3 |
| Corollary | 4 |
| Claim | 2 |
| Identity | 14 |
| Formula | 8 |
| Counterexample | 5 |
| Paradox | 0 |
| Conjecture | 1 |
| Algorithm | 297 |
| Heuristic | 5 |
| Audit | 183 |
| Other | 45 |

Total: 889. A file's old `# CLASS:` label is not used: many files labelled THEOREM
only compute, and are catalogued as Algorithm.

## Worth knowing

- **T149 contains a counterexample to the Jacobian Conjecture in dimension 3.** Verified here: the
  map's Jacobian determinant is the constant -2 for all x, y, z (symbolic, sympy), and three distinct
  points map to (-1/4, 0, 0). The file's own check now computes the determinant instead of
  hard-coding it. The attribution in the file (Alpöge, July 2026) is not verified.
- **Lemmas:** reviewers call 3 files Lemma as their primary kind (`heartbeat_3cycle`,
  `theorem_313`, `mod9_midpoint`). `math/lemmas/` holds 7 by a different, citation-based rule
  (see `math/lemmas/CLASSIFICATIONS.md`). The two rules are recorded, not merged.

## Axiom (2)

| File | Secondary | Statement | Evidence |
|---|---|---|---|
| `math/theorems/bio_bridge_scaling_invariance.py` | Algorithm | Posits scaling invariance ψ·φ=ρ with ψ=1, 37-filter, ODE, gate 18; asserts numerics | ψ=1 and ψ·φ=ρ are assumed, not proved; rest is arithmetic checks |
| `math/theorems/principle_1_substrate_principle.py` | Other | Substrate principle: substrate prior to biology and Newton. | Asserted without proof as foundational starting point. |

## Definition (34)

| File | Secondary | Statement | Evidence |
|---|---|---|---|
| `math/theorems/ahl_17_grid_structure.py` | Proposition | Names AHL=8=DR(17) and lists digital-root facts about 17 and its sums | Main content names AHL and records DR arithmetic observations |
| `math/theorems/decimal_trade_extraction.py` | Algorithm | Defines trade operator T preserving 10 when digit sum is 10; tabulates | Main content defines named operator T(n) |
| `math/theorems/digit_extension_operator_gf37.py` | Proposition | Defines digit-extension operator d->dd->ddd; mod 37 path has period 3. | Main content names a new operator; period follows from ord_37(10)=3. |
| `math/theorems/dr_grid_orbit.py` | Algorithm | Defines pair-sum DR orbit types on the 3x3 grid and tabulates column pairings | Main content names orbit types and column groups |
| `math/theorems/e8_framework_glossary.py` |  | Glossary defining E8 Adjoint Mirror Ledger terms | Main content defines named terms |
| `math/theorems/eleven_123_family.py` |  | Defines the '123 family' and lists facts about 11 in GF(37) | Opens with explicit definition of a named family |
| `math/theorems/eml_operator.py` | Identity | Defines eml(x,y)=exp(x)-ln(y); eml(x,1)=exp(x), non-commutative. | Main content defines a named binary operator. |
| `math/theorems/f26_anchor_target_architecture.py` | Algorithm | Defines anchors {4,9,25,30}, targets {3,12,21,30}, LOCKED/GATED/PURGE tiers. | Names sets and a three-tier classification. |
| `math/theorems/f26_binary_classifier.py` | Algorithm | Two-state classifier: singularity {30}, anchors {4,9,25}, purge. | Names a partition of {1..36}; implements it. |
| `math/theorems/f26_pillar_verification.py` | Audit | Defines F26 pillars {4,9,25,30} and SECURE/WARNING/ALERT tiers. | Main content names a set and classification; corrects earlier pillar set. |
| `math/theorems/fixed_point_physics_math.py` |  | Defines selection operator S and Phys=Fix(C o E) as fixed-point formulation. | Main content introduces named operators and sets. |
| `math/theorems/formal_definitions_gf37.py` | Theorem | Formal definitions of 137-map, orbit, heartbeat; Theorem H1 all periods 3. | Main content is numbered definitions, each followed by a result. |
| `math/theorems/gf37_classes.py` |  | Canonical definitions of the 12 named orbits and sets of GF(37) | Single source of truth defining named sets |
| `math/theorems/heartbeat_6step_chambers.py` | Proposition | Names two prime chambers mod 6 {1,5} labelled by DR fixed points | Main content labels chambers of primes |
| `math/theorems/holographic_manifold_gf37.py` | Proposition | Defines holographic memory operations (bind, superpose, retrieve) on GF(37). | Main content names operations and the 12 basins. |
| `math/theorems/medusa_v3_sovereign.py` | Algorithm | Defines anchor/target sets and LOCKED/GATED/PURGE classification of nodes. | Main content names sets and a classification procedure. |
| `math/theorems/morowah_condition.py` | Algorithm | Defines the Morowah condition S_d=a^r, S_p=r^a and scans for it. | Main content defines a named condition. |
| `math/theorems/nk_naturals_with_presence.py` |  | Defines N-kappa naturals with provenance | Defines named object |
| `math/theorems/permutation_132_bipartite_gf37.py` | Identity | Defines 132-occurrences and bipartite graph G(T); handshaking sum 3r(T). | Main content Definitions M1-M4 from Mansour-Vainshtein. |
| `math/theorems/string_duality_37phi_bridge.py` | Identity | Defines T-duality D(x)=37^2/x on 37phi bridge; D(D(x))=x. | Main content defines an operator; involution is D(D(x))=x. |
| `math/theorems/theorem_170_qho_operator_separation.py` |  | Classifies QHO features into six named layers with operators | Main content defines six layers |
| `math/theorems/theorem_190_mws_framework_integrity.py` | Axiom | Framework integrity constants labelled axioms, each checked mod 37 | Lists named constants; 'axioms' are verified, not assumed |
| `math/theorems/theorem_219_annotated_map_observables.py` | Algorithm | Three-layer falsification protocol with status vocabulary and thresholds. | Main content defines a protocol and status terms. |
| `math/theorems/theorem_223_orbit_partition_riemann_gf37.py` | Algorithm | Names 12 orbits of 137-map; classifies zero floors | Main content names orbits |
| `math/theorems/theorem_224_d7_envelope_stability_gf37.py` | Algorithm | Defines D7 envelope E(h) and admissible region; residues of period points. | Main content defines envelope and region. |
| `math/theorems/theorem_225_manifold_m_d7_consistency.py` | Proposition | Defines stability manifold M and D7-consistency; areas equal 12. | Main content defines objects; one integral computed. |
| `math/theorems/theorem_229_m9_terminal_singularity.py` | Algorithm | Defines M_3 and M_9 basis-collapse operators on C^9 and checks structure. | Main content defines operators. |
| `math/theorems/theorem_282_admissibility_gf37.py` | Heuristic | Defines the miss-test admissibility criterion and classifies case register | Main content defines criterion |
| `math/theorems/theorem_305_claim_strength_cuts.py` | Audit | Defines four orthogonal cuts for grading correspondence claims; Rule 30 worked. | Main content defines grading terms. |
| `math/theorems/theorem_424_rewrite_certificate_ledger_gf37.py` | Audit | Constructs a subgroup filtration for the ledger and grades a supplied claim. | File says it is a construction supplying undefined names. |
| `math/theorems/theorem_58_sector_axiom_completion.py` |  | Supplies GF(37) definitions (chi, QR/NQR orbits) for axiomatic system | Main content defines terms |
| `math/theorems/zero_comma_label_system.py` | Algorithm | Labeling system for zero-strings via commas and DR | Defines named labeling rules |
| `math/theorems/zero_comma_label_v2.py` | Algorithm | Zero-comma label formula and its all-same cases | Defines label system |
| `math/theorems/zero_fill_bridge_audit.py` | Proposition | Defines fill/bridge operation; reaches repunit in T(n-1) steps. | Main content defines an operation and its rules. |

## Theorem (106)

| File | Secondary | Statement | Evidence |
|---|---|---|---|
| `math/lemmas/sigma3_eisenstein_gf37.py` | Audit | 37 divides sigma3(p) iff p = 11,27,36 mod 37; Eisenstein splitting 37=N(7+3w) | Proof chain via cube roots of -1; also corrects source N(4+3w)=37 |
| `math/theorems/ababab_convergence.py` | Corollary | ABABAB ≡ 0 mod 37 for all digit pairs; A+B=10 gives digit sum 30 | Two proved parts plus corollary; proof via 10101 ≡ 0 mod 37 |
| `math/theorems/affine_causal_processes_gf37.py` |  | Four conditions necessary and sufficient for affine three-party process validity over GF(p) | Proved iff characterization with determinant argument |
| `math/theorems/affine_fixed_point_gf37.py` | Algorithm | Affine maps ax+b on Z/37: census 1332 unique fixed point, 36 none, 1 identity. | Full three-case classification proved via invertibility of a-1, with census. |
| `math/theorems/all_prime_grids_coset.py` |  | 3x3 all-prime digit grid rows have residues forming full coset (b-s)*H, summing to 0 mod 37. | General proof via N_i=111s+(b-s)e_i with {100,10,1}=H mod 37. |
| `math/theorems/basin_sum_wraparound_gf37.py` | Identity | Basin sum S(a)=37(a-k1-k2); all 12 basin sums are 37 or 74, 6/6 split. | General statement with proof, several parts, cited downstream by T331/T332. |
| `math/theorems/collatz_v2_equidistribution.py` | Conjecture | Exact distribution of v2(3n+1), expected log ratio, MGF, Cramér bound; equidistribution left open | Several proved sections plus an explicitly open conjecture |
| `math/theorems/connection_7518.py` | Formula | Links 7518 in 103/137 decimal and QR sum mod 179 via 103×73=7519; class-number closed form | Multi-part proved chain with closed-form formula |
| `math/theorems/cubic_residue_cycle_structure.py` |  | 137-map 3-cycles are cosets of <26>; cube fingerprint bijection; order reduction law | Four proved results about cycle structure |
| `math/theorems/cycle_partition_37.py` |  | Twelve 3-cycles of 26n mod 37 have node-sum 37 or 74, six each | Proved general result with complete proof |
| `math/theorems/cycle_symmetry_maps.py` |  | Negation, squaring, inversion induce maps on the 12 cosets; four numbered theorems proved. | Several proved results on coset maps with algebraic proofs. |
| `math/theorems/decimal_trinity.py` | Corollary | ord_37(10)=3, so <10>={1,10,26}=H_3 | Stated with proof and corollaries |
| `math/theorems/dr_algebra.py` | Algorithm | DR classes under addition ≅ Z/9Z; subgroup lattice; doubling cycles | Multi-part group-theoretic result |
| `math/theorems/dr_modular_foundation.py` | Corollary | dr(n)≡n mod 9 and mod 3, with 2n−1 rule; proof given | Central proved foundation for all DR claims |
| `math/theorems/dr_ring_homomorphism_emirp_palindrome.py` | Identity | DR is ring homomorphism; emirp DR invariance; palindromic prime exclusion. | Several-part proved result with derived consequences. |
| `math/theorems/ds_congruence_mod9.py` | Identity | DS(n) = n mod 9; bounds on DS; tier sum T(k) = 5 mod 9 | Proved; identity DS(n) = n (mod 9) |
| `math/theorems/emirp_dr_c0_eisenstein.py` | Identity | Emirp pairs share DR and chi_{-3}; rev(p)≡(−1)^(L−1)p mod 11; no mod-37 analogue | Several-part proved result on reversal |
| `math/theorems/erdos_primitive_set_bound.py` |  | States Lichtman's theorem on Erdős primitive sets and checks examples numerically | Central proved external result, restated and checked |
| `math/theorems/f26_order3_cycles_mod37.py` |  | ord37(26)=3 so f(n)=26n mod 37 splits 36 residues into 12 3-cycles | Proved central result of the 137-map |
| `math/theorems/fixed_line_3cycle_gf37.py` | Formula | 3-cycle affine process on GF(37) has fixed line iff uvw≡rst; kernel direction given | Numbered theorem with determinant condition and kernel proof |
| `math/theorems/gaussian_integers_gf37.py` | Definition | Z[i]/(6+i) ≅ GF(37); i ≡ 31; norms of lifts. | Multi-part proved result on Gaussian integer structure. |
| `math/theorems/group_G54_structure.py` |  | Full structure of G = C9 x\| C6 order 54: center, classes, irreps | Multi-part proved group classification |
| `math/theorems/lob_26_collatz_f37.py` |  | Collatz-like T on F_37 has exactly 3 cycles (1,3,9) by exhaustive enumeration. | Complete classification of a finite map's cycles; includes corollary. |
| `math/theorems/mersenne_dr9_period6_theorem.py` | Audit | DR(M_n) period 6; DR=9 iff 6\|n; Mersenne primes DR∈{1,4} | Three proved parts; refutes 33.3% claim |
| `math/theorems/monomial_universe.py` | Algorithm | Order ideals of N^n characterised by lower covers; verifies universe counts | Proposition 1 proved plus verification scaffold |
| `math/theorems/orbit_negation_duality_gf37.py` |  | Negation maps orbits to orbits, none self-dual; 6 pairs each summing to 111. | Proved structural result with several parts. |
| `math/theorems/palindrome_gf37.py` | Formula | Palindrome pair coefficients mod 37 lie in ORBIT_11 or DARK_A by power class | General coefficient rule for all lengths |
| `math/theorems/pascal_repunit_gf37.py` | Identity | Pascal row n read in base 10 equals 11^n iff all coefficients <10. | Binomial theorem at x=10; general proved statement. |
| `math/theorems/phi12_cut_and_t33_gf37.py` |  | Φ12 splits over F37 as (x−8)(x−14)(x−23)(x−29); C3=μ12; T33 collapse | Several proved theorems |
| `math/theorems/power_tower_collapse_gf37.py` |  | Power towers mod 37 and mod 9 collapse; 9-tower hits 1 from height 2 | Numbered multi-part proved result |
| `math/theorems/primitive_root_test.py` | Algorithm | g primitive root mod p iff g^((p−1)/q)≢1 for prime q\|p−1 | Standard proved theorem with test |
| `math/theorems/prisoners_permutation_gf37.py` |  | 100 prisoners: survival iff no cycle >50; cycle structure linked to GF(37) | Proved survival criterion with several parts |
| `math/theorems/rank_elevation_audit.py` |  | rank(C-Delta)=rank(C)+1 for arithmetic grid with anchor exemption | Proved general rank statement |
| `math/theorems/reciprocal_quadrinomial_pp_criterion.py` |  | Quadrinomial restricted to mu_{q+1} reduces to h(x^2); PP criterion for b=-1. | Derived criterion with factorization of h(t). |
| `math/theorems/repunit_square_998001.py` | Identity | 1/998001 expands as concatenated 000..997 with period 2997. | Series-identity proof plus period derivation. |
| `math/theorems/sovereign_matrix_charpoly.py` |  | Sovereign DR matrix has rank 4 and char poly λ⁶·p₃(λ) | Proved structural result on one matrix |
| `math/theorems/sovereign_qr_closure.py` | Corollary | Sovereign anchors and targets all lie in QR37; 26 is QR so map preserves QR. | Proved containment plus structural corollary. |
| `math/theorems/stark_heegner_theorem.py` |  | Stark-Heegner nine discriminants; Rabinowitsch primes finite list. | Restates and checks a known theorem. |
| `math/theorems/t33_orbit_invariance_and_transversal_gf37.py` |  | x³+33 constant on μ_3 cosets; its 6-cycle is a transversal of six orbits | Two proved statements |
| `math/theorems/theorem_110_mirror_reversal_gf37.py` | Identity | ABC−CBA=99(A−C); 99≡25 mod 37; five consequences | Central result with several parts |
| `math/theorems/theorem_118_coset_structure_gf37.py` |  | (Z/37)* cyclic; cosets of H_3 are the 12 137-map orbits | Multi-part proved structure theorem |
| `math/theorems/theorem_130_pohlig_hellman_sylow_gf37.py` |  | Sylow decomposition of F_37*; Sylow-3 = IC∪SA_ORB∪D7 | Proved group-structure result |
| `math/theorems/theorem_138_dr_law_orbit_multiplication.py` | Identity | DR(a×₃₇b)=DR(ab)−DR(⌊ab/37⌋); 12 orbits form Z/12Z | Two linked proved results |
| `math/theorems/theorem_142_subgroup_tower_gf37.py` |  | Subgroup tower μ3<H9<QR<F37× and its two quotient partitions | Multi-part proved structure |
| `math/theorems/theorem_150_phi3_forcing_lucas_gf37.py` |  | Proves 137-map orbit is X³−1 roots; Φ3 forcing; Lucas link | Three proofs forming main result |
| `math/theorems/theorem_163_gf37_c6_decomposition.py` |  | x->27x on GF(37)* is intertwined with 60-degree rotation on 6 shells x 6 sectors. | Exact intertwiner identity, several parts. |
| `math/theorems/theorem_193_process_functions_zp.py` | Algorithm | Affine 3-party process functions over Z_p are causally ordered. | Proved main result with exhaustive scans. |
| `math/theorems/theorem_200_quotient_z12z_gf37.py` | Proposition | GF(37)*/<26> is Z/12Z with coset arithmetic of named sets. | Central quotient structure with several parts verified. |
| `math/theorems/theorem_201_additive_coset_gf37.py` | Definition | Coset positions add under multiplication; doubling shifts coset by +1. | Multi-part proved structural result. |
| `math/theorems/theorem_203_diagonal_coset_sum_gf37.py` | Definition | Defines diagonal coset sum; proves well-defined; tabulates sovereign sums. | Definition plus proof of well-definedness and results. |
| `math/theorems/theorem_228_affine_doubling_topology.py` |  | Doubling map on Z_(B-1): cycles/transients determined by v2(B-1) | General proved result with cases |
| `math/theorems/theorem_242_rule30_left_vs_right_boundary_gf37.py` |  | Rule 30 left vs right boundary periods; left depth-0 constant 1 proved | Proved boundary results |
| `math/theorems/theorem_245_n130_divisor_square_sum_gf37.py` | Algorithm | n=130 is the unique divisor-square-sum solution at k=4; cross-k uniqueness corrected. | Several proved per-k cases; searches reported separately as evidence. |
| `math/theorems/theorem_250_n250_twin_prime_engine_gf37.py` |  | Twin prime k_m mod 3 determines DR(6k_m) as 6,3,9 cycle | Proved modular result |
| `math/theorems/theorem_275_inverse_orbit_map_gf37.py` |  | Inversion induces involution on 12 orbits; three structural classes. | Complete classification with parts. |
| `math/theorems/theorem_278_twin_prime_structure_gf37.py` | Audit | Proved structural conditions on twin primes; corrects 2025 translation | Proved conditions plus corrections |
| `math/theorems/theorem_284_operator_group_gf37.py` |  | <11>=IC u NEG_H; three-level coset partition of GF(37)*. | Proved subgroup chain and partition. |
| `math/theorems/theorem_285_quotient_group_z12_gf37.py` |  | GF(37)*/IC = Z/12Z; antipodal map is +6; inverse pairing | Main quotient structure result (prior art T138) |
| `math/theorems/theorem_287_anomalous_curve_orbit_partition.py` |  | x³+5 constant on 137-orbits; orbits split 6+6 by QR | Proved mechanism and count |
| `math/theorems/theorem_288_j0_isomorphism_classes_gf37.py` |  | Six j=0 curve isomorphism classes over F_37 match antipodal orbit pairs | Proved bijection with point counts |
| `math/theorems/theorem_289_quadratic_twist_h4_cosets_gf37.py` | Corollary | Quadratic twist pairs of j=0 curves over F_37 are the three H_4 cosets. | Main multi-part result building on T288. |
| `math/theorems/theorem_291_iterated_squaring_sylow3_gf37.py` | Corollary | k squarings on Z/12Z collapse to Sylow-3 H_3 after 2 steps | Extends T290; proved chain |
| `math/theorems/theorem_292_forced_extension_limits_gf37.py` |  | Primes with ord_p(137)=3 are exactly {7,37,73}; three extensions forced negative. | Complete finite classification by factorization. |
| `math/theorems/theorem_293_anomalous_uniqueness_p37.py` |  | p=37 unique among {7,37,73} satisfying both anomalous-curve conditions | Proved uniqueness with two conditions |
| `math/theorems/theorem_295_glv_generalization_secp256k1.py` |  | μ3 structure generalizes to every p≡1 mod 3; GLV on secp256k1 | General proved result |
| `math/theorems/theorem_296_36gon_rotation_model.py` | Definition | F_37* as 36-gon; multiplicative maps as rotations | Proved isomorphism with geometric dictionary |
| `math/theorems/theorem_298_j1728_gaussian_cm.py` | Algorithm | j=1728 curves over F_37: four twist classes, traces, Gaussian CM. | Multi-part result verified by enumeration. |
| `math/theorems/theorem_299_two_maps_from_phi3.py` |  | Evaluating vs quotienting Φ_3 give different objects meeting at μ_3 at p=37 | Proved separation result |
| `math/theorems/theorem_300_what_is_special_about_37.py` |  | Classifies properties of 37 into tiers A (p=1 mod 3), B ({7,37,73}), C. | Complete classification with verification. |
| `math/theorems/theorem_302_137map_is_decimal_shift.py` | Identity | 137-map is decimal shift since 26 = 10^2 mod 37; reciprocal-pair rule. | Several proved parts; a*b=10^n-1 gives 1/a = b/(10^n-1). |
| `math/theorems/theorem_303_block_map_is_27.py` | Identity | block(k)=27k exactly; block map cycles are antipodal pairs | Main proved result, several parts |
| `math/theorems/theorem_304_three_lists_meet_at_37.py` |  | 37 unique prime with ord_p(10)=3; three lists meet at 37 | Proved list intersections |
| `math/theorems/theorem_306_discrete_rope_circle_gf37.py` | Counterexample | Norm-1 circle S(37) ≅ F_37*, order 36; order-3 subgroup is IC. | Proved isomorphism; refutes 'max cycle length 3'. |
| `math/theorems/theorem_314_twelve_double_closure_gf37.py` | Corollary | 12 unique n closed under both readings of n+9 | Proved; builds on T313 |
| `math/theorems/theorem_316_t120_seed_class_mod_333_gf37.py` | Audit | T120/121 gate passes exactly seeds ≡246 mod 333; 8 reference values constant. | Proved by CRT plus seed sweep. |
| `math/theorems/theorem_317_cubic_quotient_mu3_gf37.py` |  | x³+33 fibres are μ_3 cosets; induced map on 12 shelves described | Proved result with several parts |
| `math/theorems/theorem_320_ag23_lift_geometry_gf37.py` | Proposition | The lift machine is AG(2,3); columns are a parallel class, rows lines for 3 grids. | Several proved parts placing a construction in an affine plane. |
| `math/theorems/theorem_321_latin_phase_criterion_gf37.py` |  | Phase-Latin iff all row sums equal iff row sums 15 | Proved equivalence of three conditions |
| `math/theorems/theorem_322_lift_criterion_theorem_gf37.py` |  | Lift criterion: equivalences for Latin phase array | Multi-part proved theorem |
| `math/theorems/theorem_324_general_lift_magic_gf37.py` |  | Lift is row-magic at n(n^2+1)/2 for all n, magic for none. | Proved general result generalising T322, T323. |
| `math/theorems/theorem_325_rotation_walk_shapes_gf37.py` |  | Rotation stack of 123 is cyclic Latin square; reversal swaps rotation classes | Proved result, several parts |
| `math/theorems/theorem_326_all_roads_ap_triples_gf37.py` | Identity | AP digit triple a,a+d,a+2d has residue 12d mod 37. | General law n=111a+12d proved. |
| `math/theorems/theorem_334_base_inversion_negates_slope_orbit_gf37.py` |  | Slope orbits of bases 10 and 26 are negation duals, via Vieta. | General proof for p=1 mod 3. |
| `math/theorems/theorem_337_sophie_germain_map_gf37.py` |  | Sophie Germain map is ×2 in shifted coordinates; primes show no orbit bias | Main proved result |
| `math/theorems/theorem_338_sg_137_generate_agl_gf37.py` |  | Sophie Germain and 137-maps generate AGL(1,37); no joint taxonomy | Proved central group result |
| `math/theorems/theorem_341_koopman_spectra_gf37.py` |  | Koopman spectra of 26x and 2x+1 on F_37 from cycle types | Proved spectral result |
| `math/theorems/theorem_345_twin_midpoint_forbidden_gf37.py` | Audit | Twin midpoints avoid exactly ±1 mod 37; settles T167 | Proved forcing plus measured check |
| `math/theorems/theorem_346_collatz_137_proper_subgroup_gf37.py` |  | Collatz and 137-maps generate index-2 subgroup preserving QR of differences | Proved group result |
| `math/theorems/theorem_356_T_functional_graph_gf37.py` | Proposition | T descends to quotient; graph is 6-cycle with two length-3 chains. | Complete proved characterisation of a map. |
| `math/theorems/theorem_357_two_quotients_separated_gf37.py` | Audit | 13-state cubic quotient and 9-state doubling system differ in kind | Proved comparison; corrects terminology |
| `math/theorems/theorem_358_no_semiconjugacy_gf37.py` |  | No surjective semiconjugacy from cubic quotient onto mod-9 doubling. | Lemmas, propositions, corollary leading to impossibility result. |
| `math/theorems/theorem_364_complement_involution_3663.py` |  | 9s-complement on Z_3663 is global involution; F_37 invariant fibre; 18 two-cycles. | Multi-part proved result. |
| `math/theorems/theorem_365_37_first_irregular_prime.py` |  | 37 is the first irregular prime (divides B_32 numerator) | Known result verified over all smaller primes |
| `math/theorems/theorem_366_cyclotomic_membership_is_vacuous.py` | Counterexample | Every prime except 2,5 divides some Phi_m(10); the sieve filter is vacuous. | Proof via m=ord_p(10); refutes the supplied filter. |
| `math/theorems/theorem_381_napkin_ring_volume_invariance.py` |  | Napkin-ring volume πh³/6 independent of R; surface area is not | Proved result by two routes |
| `math/theorems/theorem_425_collatz_lob26_dynamics_descent_gf37.py` |  | Collatz T on {0..36}: not induced, 9-cycle artifact, no semiconjugacy | Complete finite-dynamics result, several parts |
| `math/theorems/theorem_426_5n_plus_1_map_gf37.py` |  | 5x+1 mod 37 gives full AGL; parity map 7-cycle | Multi-part proved result |
| `math/theorems/theorem_427_7n_plus_1_map_gf37.py` | Algorithm | \|<A_m, mu>\| = 37 lcm(ord_37(m),3); 7x+1 map cycle structure. | General order formula subsuming T338, T346, T426. |
| `math/theorems/theorem_428_parity_word_determinant_sieve.py` | Audit | Parity-word determinant sieve closes band of positive cycles; repairs two verdicts. | Proved identity/sign argument plus corrections. |
| `math/theorems/theorem_429_transversal_triple_partitions_gf37.py` |  | 3x3 digit grid is transversality of two triple-partitions; permutation orbits | Proved characterisation plus census |
| `math/theorems/theorem_430_rank_one_trace_law_all_ones_gf37.py` |  | Rank-one A satisfies A^2=tr(A)A; all-ones J^k=n^(k-1)J over GF(37). | General law proved, nilpotent case at 37\|n. |
| `math/theorems/theorem_431_factorial_square_residue_handoff_gf37.py` | Audit | n! is never a square for n>1; residue oracles fail | Proof via Bertrand's postulate |
| `math/theorems/theorem_432_carry_map_digital_root_rings_gf37.py` | Identity | Carry map and digital-root ring Z/(b-1); Kummer identity; boundary carries. | Multiple proved parts; C_b(x,y)=(s_b(x)+s_b(y)-s_b(x+y))/(b-1). |
| `math/theorems/tripling_map_gf37.py` |  | ×3 generates QR subgroup; 3^6=26 so 137-map is its 6th power; 6-orbit cycle | Proved multi-part result |
| `math/theorems/twin_prime_18x_framework.py` | Identity | (18x±1) orbit-pair sequence has period 37; orbit sum ≡0 | Proved periodic structure |
| `math/theorems/twin_prime_structure.py` |  | Primes >3 are 6n±1; twin pairs are (6n−1,6n+1); midpoint divisible by 6 | Several proved parts |

## Proposition (180)

| File | Secondary | Statement | Evidence |
|---|---|---|---|
| `math/lemmas/abcabc_mod37_orbit.py` | Identity | ABCABC = 1001*ABC and 1001≡2 mod 37, so the map acts as ×2, a primitive root | Identity ABCABC ≡ 2·ABC (mod 37) for all 3-digit ABC |
| `math/lemmas/theorem_283_negation_antipodal_gf37.py` | Lemma | The six antipodal orbit pairs equal the six negation pairs; 0 is negation's unique fixed point. | Proved finite statement; file itself says Parts 1-4,6 restate orbit_negation_duality_gf37. |
| `math/lemmas/twin_prime_dr_pair.py` | Algorithm | Twin pair (6m-1,6m+1) DR pair fixed by m mod 3: (8,1),(5,7),(2,4). | Narrow congruence fact proved mod 9; counts to 10^6 computed. |
| `math/theorems/all_prime_grids_full.py` |  | All-prime grids: DR constant per grid, row product = (b-s)^3 mod 37 | Proved facts limited to three specific grids; extends T401/T403 |
| `math/theorems/alpha_137_dr_extension.py` |  | DR(137)=DR(137036)=2 because appended 036 has digit sum 9 | Single narrow proved digit-root fact about one number |
| `math/theorems/arithmetic_progression_37field.py` | Identity | 37-term AP with step 18 sums to 0 mod 37 and preserves a mod 9. | Proved closed-form sum 37(a+324); narrow result. |
| `math/theorems/arithmetic_sequence_1111.py` |  | AP with difference -1111: digital root rises by 5 mod 9 each term | Small proved fact: -1111 = 5 mod 9 |
| `math/theorems/bfs_attractor_mod9.py` | Algorithm | Under moves {+2,+3} mod 9 every residue reaches S={0,2,3,6,8} in at most one step. | Narrow finite statement verified exhaustively by BFS. |
| `math/theorems/chi2_cancellation_proof.py` | Audit | Gives valid proof chi_2(φ^-3)=π²/24−(3/4)ln²φ via ln2 cancellation | Proved closed-form value at one point; replaces invalid route |
| `math/theorems/chi3_twin_prime_character.py` | Definition | chi_{-3}(n)=0 iff 3\|n iff DR in {3,6,9}; twin walls carry chi -1,+1. | Short proved equivalence linking T409/T410 chambers to character classes. |
| `math/theorems/cipher_123_1234.py` | Definition | Z/9Z splits into {3,6,9} and doubling orbit; 1234 mod 37 = 13 | Small verified partition fact with named sets |
| `math/theorems/collatz_mod37_basin.py` | Algorithm | Basin sizes 1/23/13 of mod-37 Collatz map; integer cycles project onto T-cycles. | Proved finite facts extending lob_26; narrower than a theorem. |
| `math/theorems/column_cross_pairing.py` | Algorithm | Column cross-pairing totals and DR facts for 3x3 digit grid | Several small verified DR facts, mostly computed |
| `math/theorems/coset_step_alignment.py` |  | Torus steps −2 and 54 land in same coset of H={1,10,26} mod 37 | Narrow proved residue fact |
| `math/theorems/cubic_shift_33_gf37.py` | Algorithm | x^3+33 mod 37 has one 6-cycle attracting all 37 points within 4 steps. | Exhaustively verified finite dynamics statement about one map. |
| `math/theorems/cyclic_142857.py` | Algorithm | 142857 = 3^3*37*11*13 and its multiples 1..6 are cyclic rotations. | Specific verified facts about one number. |
| `math/theorems/cyclic_142857_decimal_gf37.py` |  | 10·26≡1 mod 37: decimal shift and 137-map are inverse on IC; period hierarchy | Narrow proved facts about orders mod 37 and 7 |
| `math/theorems/cyclic_permutation_coset.py` | Identity | Cyclic permutations of 3-digit N form a coset N*H of <10> mod 37 | Proved via 999=27*37; narrower result |
| `math/theorems/dark_sector_algebra.py` | Definition | QR/NQR partition aligns with named sets; primitive roots are all NQR. | Proves PR subset NQR by order argument; narrow scope, names sectors. |
| `math/theorems/delta27_heisenberg_neutrino.py` | Definition | Generators x,y generate Delta(27)=H(F_3) with xy=omega yx; TBM link. | Verifies known group facts; narrower than a central theorem. |
| `math/theorems/digit_seq_dr_coverage_gf37.py` |  | Fibonacci-triple digit sums with single digits miss DR=2; zero or two-digit term fills it. | Proved small result by mod 9 reasoning. |
| `math/theorems/digits_137_and_7.py` | Identity | Arithmetic on digits 1,3,7 gives k/7 decimals; block halves of 1/7 and 1/137 sum to 10^(k/2)-1. | Verifies specific facts for p=7,137; general split claim not proved in file. |
| `math/theorems/digits_137_running_sum.py` |  | Running digit sums of 137 read '411' = 3×137; 3↔6 DR pair | Narrow verified numerical fact |
| `math/theorems/dr_369_closure_mirror_audit.py` | Audit | {3,6,9} DR class closed under doubling/halving; mirror pairs sum to 9 | Small proved closure facts |
| `math/theorems/dr_fixed_point_mod9.py` | Audit | Every 1..9 is a dr fixed point; dr idempotent; corrects 'unique fixed point' claim. | Short proved facts about dr map with correction. |
| `math/theorems/dr_matrix_v3_snf_audit.py` | Audit | DR multiplication matrix V3 has SNF [1,9,...,9], trivial kernel over Z/26Z. | Computed statement about one matrix; notes Theorem 9 not realised. |
| `math/theorems/dr_pattern_suite.py` | Algorithm | Suite of ten-plus DR pattern findings, D4 group algebra, Cardano roots. | Many verified narrow facts (105 asserts); none central. |
| `math/theorems/dr_spiral_gf37.py` | Algorithm | ST={3,12,21,30} is the unique named set with constant digital root | Narrow proved fact on the DR-collapsed spiral |
| `math/theorems/drift_loeschian_delta2.py` | Algorithm | Loeschian norm form surjects onto GF(37); drift and Delta^2 threads computed. | Standard fact (37=1 mod 3) plus verified counts. |
| `math/theorems/eisenstein_chi_m3_connection.py` | Definition | Sovereign set {3,6,9} equals kernel of chi_{-3} on DR values; 37 Loeschian. | Short proved correspondences; CDT theorem cited externally. |
| `math/theorems/emirp_product_col1_theorem.py` | Theorem | For emirp pair p>3, DR(p·rev(p))∈{1,4,7}; two proofs | Single narrow proved statement |
| `math/theorems/f26_dr3_anchors_mod37.py` |  | Under 26n mod 37, exactly nodes {4,9,25,30} give DR=3 residues | Narrow verified fact by exhaustive scan |
| `math/theorems/f26_fixed_point_mod37.py` |  | Two branches of check_f26_logic are dead since 26n mod 37 is a bijection. | Proves unreachability of branches from bijectivity. |
| `math/theorems/f26_qr_closure_mod37.py` |  | Anchors {4,9,25,30} and targets {3,12,21,30} lie in QR mod 37 | Proved narrow membership statement |
| `math/theorems/f37_hexagonal_decomposition_audit.py` | Audit | F_37* hexagonal structure: <10>={1,10,26}, C3 union -C3 = <27>, 27^3=-1. | Verified narrow group-structure facts. |
| `math/theorems/five_six_orbit.py` | Algorithm | 5,6 flank 11/2; products/sums land in named sets; small 'theorems'. | Narrow computed facts about specific residues. |
| `math/theorems/gamma_22_inverse_seed_gf37.py` | Definition | {17,22,35} is the element-wise inverse orbit of {18,24,32} in GF(37). | Narrow proved inverse-pairing fact with class checks. |
| `math/theorems/goldilocks_prime.py` |  | Goldilocks prime 2^64-2^32+1 is prime; p-1 factors with 2^32 and Fermat primes | Verified facts about one specific prime |
| `math/theorems/group_framework_primitives.py` | Algorithm | 20 and 17 are primitive roots mod 37; payload X = 8 mod 37, 11, 407. | Specific verified facts about named numbers. |
| `math/theorems/hanlon_decomposition_gf37.py` | Identity | Hanlon D4/D5 decomposition of chromatic polynomials for 3x3 grid and C5 | Polynomial identities verified for two specific graphs |
| `math/theorems/identity_cycle_sum_structure.py` | Identity | Pairwise sums of {1,10,26} are {11,27,36}; triple sum 0 mod 37 | Small proved facts about subgroup sums |
| `math/theorems/intersection_cycle_theorem.py` |  | (3,4,30) is the unique 3-cycle of 26n mod 37 wholly in SA∪ST | Narrow fact proved by exhaustive check of 12 cycles |
| `math/theorems/k5_shape_c_q3.py` | Lemma | Shape C 3\|n branch of k=5 ledger is empty | Proves one branch closed; step in larger case tree |
| `math/theorems/kaprekar_2481_1572_3693.py` | Algorithm | Kaprekar sibling pairs, 2481+3693=6174, mod-73 and mod-37 facts. | Narrow verified numerical facts. |
| `math/theorems/largest_sg_prime_gf37.py` | Algorithm | Largest known Sophie Germain prime is 26 mod 37 and DR 8. | Narrow residue fact proved by modular arithmetic. |
| `math/theorems/layer54_lucas_period24.py` | Algorithm | Lucas numbers mod 9 have minimal period 24. | Proved narrow fact via recurrence state repeat and divisor check. |
| `math/theorems/layer56_period_minimality_audit.py` | Audit | Lucas numbers mod 9 have minimal DR period exactly 24 | Narrow proved minimality by exhaustive divisor check |
| `math/theorems/layer58_pisano_period9.py` |  | Pisano period pi(9)=24 with minimality proof | Proved narrow statement |
| `math/theorems/layer62_lucas_period_mod9.py` | Audit | Lucas sequence mod 9 has minimal period exactly 24. | Single proved fact checked by divisor minimality. |
| `math/theorems/lcm_convergence_dr_cycle.py` |  | LCM(1,2,3)=6, LCM(1,2,3,9)=18; DR of 6n cycles {6,3,9} | Small proved arithmetic facts |
| `math/theorems/lob_25_legendre_applications.py` |  | Legendre-symbol results: x²-x-1 irreducible over F_37; tier QR classification | Several narrow verified Legendre facts |
| `math/theorems/lob_88_g_ord18_cycle.py` | Audit | Six TLA+ invariants of powers of 3 mod 37; <3>=QR_37. | Verified finite facts; narrower result. |
| `math/theorems/lucas_abbc_chain.py` | Conjecture | Chain 4,7,11,...,123 is Lucas L(3..10); lists zeta-zero approximations as conjecture. | Verified identification; Riemann-zero table explicitly labelled conjecture. |
| `math/theorems/matrix_config_ab_gf37.py` | Algorithm | Kernel, det, permanent of two 3x3 matrices and residues mod 37 | Computed facts about specific matrices |
| `math/theorems/mersenne_dr_boundary_53_54.py` | Algorithm | DR(2^n-1) period-6 cycle; boundary n=53/54 digit length; 56 digit-sum-6 counts. | Narrow proved counting and periodicity facts. |
| `math/theorems/mersenne_seam_kervaire_gf37.py` | Algorithm | S_k≡0 mod odd p iff p \| 2^k−1; Kervaire table. | One-line proved statement plus table. |
| `math/theorems/mirror_table_mod37_audit.py` | Audit | ABAB = T mod 37 iff AB = 11T; doubling acts as negation on <27>. | Short proved derivation about one subgroup. |
| `math/theorems/mod37_qr_analysis.py` |  | <3> equals QR_37; 3^9=-1; DR=5 values excluded from QR. | Narrow proved subgroup facts. |
| `math/theorems/mult_by_2_orbit_audit.py` | Audit | 2^6≡27 mod 37; ABAB≡27·AB, ABCABC≡2·ABC mod 37 | Narrow proved orbit facts |
| `math/theorems/nine_tower_dr_invariant.py` | Definition | Defines 9-tetration tower; proves DR(9^^k)=9 for all k. | Narrow proved statement with accompanying definitions. |
| `math/theorems/nines_complement_sa_h.py` |  | For k=1..3, 10^k−1 is in SA or 0 mod 37 and 10^k in H | Narrow verified statement for three k |
| `math/theorems/odd_perfect_zero_system.py` |  | Zero-string comma grouping is ECO iff n=2 mod 3, otherwise OCO. | Proved small classification by residue mod 3. |
| `math/theorems/orbit_order_structure_gf37.py` |  | Orbits are homogeneous in order except the 4 containing 4th roots of unity | Proved classification from order table |
| `math/theorems/orbit_sector_geometry_gf37.py` | Definition | chi(26)=+1 so every 137-orbit is QR- or NQR-homogeneous; 6+6 orbits. | One-line proved fact plus named geometric labels. |
| `math/theorems/order6_subgroup_gf37.py` | Definition | 11 has order 6 mod 37; ⟨11⟩ = IC ∪ NEG_H | Narrow proved subgroup fact |
| `math/theorems/pair_addition_dr_switch.py` |  | DR(2n) even for n<=4, odd for n>=5 due to 9-wraparound. | Narrow proved parity fact. |
| `math/theorems/palindrome_cipher_37R.py` | Algorithm | 8-digit palindrome pair sums always divisible by 11; seeds' residues listed. | Proves narrow divisibility fact; rest is computed. |
| `math/theorems/perfect_496_dr_structure.py` | Formula | Factors of 496 have DRs in {1,2,4,5,7,8}; DR(2^k-1)=DR(2^k)-1 rule. | Narrow proved facts plus a DR computation rule. |
| `math/theorems/perfect_numbers_137.py` | Algorithm | Even perfect numbers ≥28 have DR 1; QR mod 37 table | Narrow proved mod-9 fact |
| `math/theorems/period_999_2997.py` |  | period(1/999^2)=2997=999*period(1/999) | Proved via multiplicative orders |
| `math/theorems/permutation_cycle_notation_gf37.py` |  | ×3 permutes the 12 orbits as two 6-cycles; index sums computed | Narrow verified fact about orbit permutation |
| `math/theorems/phi12_order_and_cut_string_link_gf37.py` |  | Prime factors of Phi_12(137) are 1 mod 12; 13 shared with cut string | Proved general fact plus checks |
| `math/theorems/pisano_period_333.py` |  | pi(333)=lcm(pi(9),pi(37))=456 via CRT. | Applies standard CRT Pisano lemma to one modulus. |
| `math/theorems/prime_dr_unification.py` | Algorithm | DR framework gives track structure for prime pairs of even gap <=246. | Proved DR/mod-18 track facts; external results cited not proved. |
| `math/theorems/prime_streams_z9_gf37.py` |  | Prime streams are (Z/9Z)* generated by 2 | Proved narrow group facts |
| `math/theorems/primitive_root_invariants_gf37.py` | Algorithm | The 12 primitive roots mod 37 form 4 NQR orbits; g^9, g^6, g^12 invariants. | Verified finite group facts. |
| `math/theorems/primitive_roots_mod37.py` |  | Twelve primitive roots mod 37, all QNR | Proved facts about primitive roots |
| `math/theorems/qr_qnr_partition_gf37.py` |  | Named GF(37) sets are QR-homogeneous; 137-map preserves QR/QNR. | Narrow proved facts via Legendre symbol. |
| `math/theorems/repdigit_framework_lattice.py` | Algorithm | ddd = 0 mod 37 since ord37(10)=3; repdigit residue map | Proved period-3 law plus tables |
| `math/theorems/repdigit_self_similarity_gf37.py` | Algorithm | Repunits mod 37 have period 3 with residues {1,11,0}. | Proved from ord_37(10)=3. |
| `math/theorems/repunit_sq_euler_phi_gf37.py` |  | R_n and R_n² mod 37 are period-3; φ(38..42) residues listed | Narrow verified facts from ord_37(10)=3 |
| `math/theorems/reversal_differences.py` | Algorithm | Digit-block reversal differences 198 and {594,396} | ABC−CBA=99(A−C) instances; narrow |
| `math/theorems/reversal_sovereign_collapse.py` | Lemma | DR(\|n-rev(n)\|)=9 and DR(6n) in {3,6,9}, both proved mod 9. | Short proved congruence facts. |
| `math/theorems/root_grid_dr6_dr7.py` | Formula | 2-digit DR-6/DR-7 grids split by digit sum; span 81 | Small verified facts |
| `math/theorems/sa_self_cycle_st_chain.py` | Definition | ST 12,21,30 step by 9 and digit chain; SA 9 self-cycle | Narrow verified arithmetic facts |
| `math/theorems/scalar_triad_137_248_359.py` |  | 137, 248, 359 all = 26 mod 37 since AP step 111=3*37. | Narrow proved fact plus assorted checks. |
| `math/theorems/sector_invariance_137map.py` | Corollary | chi(26n)=chi(n): 137-map preserves Legendre symbol; 2x2 cycle classification follows. | One-line proof; in-file corollary derived from it. |
| `math/theorems/self_square_divisor_130.py` | Conjecture | 130 = 1+4+25+100 unique; proved for n=pqr, sieve elsewhere | Partial proof; general uniqueness only searched |
| `math/theorems/shell_opacity.py` | Corollary | No purge node maps into sovereign range under 137n mod 37 | Bijection consequence; parent not named by file/T-number |
| `math/theorems/sieve_rank_audit.py` | Audit | Exact epsilon_2, rank-2 proof for Type-II matrix, wheel sieve mod 90. | Proved narrow matrix-rank and sieve facts. |
| `math/theorems/sliding_window_9cycle_gf37.py` | Algorithm | Windows 123..789 all ≡12 mod 37 via step 111; wrap breaks it | Narrow verified fact |
| `math/theorems/sovereign_fixed_point.py` | Lemma | Two classifier branches unreachable since 26n mod 37 is a bijection. | Short proved fact about the code's logic. |
| `math/theorems/sovereign_triple_plus9_gf37.py` | Definition | +9 action on sovereign triple orbits; 26 is QR | Computed facts about named sets |
| `math/theorems/sylow_subgroup_gf37.py` |  | Sylow-2 and Sylow-3 subgroups of GF(37)* | Proved narrow group facts |
| `math/theorems/theorem_101_sophie_germain_gf37.py` | Lemma | Largest known Sophie Germain prime ≡26 mod 37; safe prime ≡16 | Narrow facts via lemma chain |
| `math/theorems/theorem_106_mohr_mascheroni_gf37.py` | Audit | Mohr–Mascheroni via Fermat primes; F_n mod 37 periodic with period 6 for n≥2 | Narrow proved periodicity plus residue table |
| `math/theorems/theorem_108_serpentine_twin_gf37.py` | Definition | Serpentine 3x3 path is Hamiltonian; n=35 mod 37 pair never twin | Small proved facts |
| `math/theorems/theorem_109_137_twin_prime_gf37.py` | Algorithm | 137 = 26 mod 37, 26 a cube root of unity; twin 139 orbit facts. | Verified specific finite-field facts. |
| `math/theorems/theorem_111_ascending_descending_gf37.py` |  | 987654321≡1, 123456789≡-1 mod 37 | Proved narrow congruences |
| `math/theorems/theorem_116_multiplicative_orders_gf37.py` | Algorithm | Order table mod 37; phi(d) elements of each order d\|36 | Computed table instantiating standard count |
| `math/theorems/theorem_134_mirror_concatenation_gf37.py` | Algorithm | 246642 = 2·3·11·37·101; quotient 6666 | Narrow factorization fact |
| `math/theorems/theorem_135_triangular_numbers_gf37.py` |  | T(n) mod 37 hits exactly 19 residues iff 1+8k QR | Proved coverage criterion |
| `math/theorems/theorem_137_369_digital_roots_gf37.py` | Algorithm | DR classes partition (Z/37)* into 4-element classes; 12 multiples of 3. | Proved counting facts, narrow. |
| `math/theorems/theorem_139_gf7_gf37_structural_parallel.py` |  | GF(7) and GF(37) compared: phi factors, mu_3, quotients C2 vs C12. | Proved narrow structural comparison. |
| `math/theorems/theorem_141_pisano_period_76_gf37.py` | Algorithm | Pisano period mod 37 is 76; zeros at 0,19,38,57; F_{38+k} = -F_k. | Verified known facts about one modulus. |
| `math/theorems/theorem_144_loop_cipher_negation_gf37.py` | Corollary | 9-complement cipher is negation mod 37 on strings of length divisible by 3. | Proved via 10^n-1 = 0 mod 37 iff 3\|n. |
| `math/theorems/theorem_145_six_seven_triangles_gf37.py` | Algorithm | 3-digit {6,7} strings' residue determined by popcount via weights {1,10,26}. | Proved via positional weights; narrow. |
| `math/theorems/theorem_148_single_digit_orbit_coverage_gf37.py` | Algorithm | Digits 1..9 cover exactly 7 of 12 orbits | Finite verified fact |
| `math/theorems/theorem_154_dr_fibonacci_trinity_period8.py` |  | DR-Fibonacci on {3,6,9} has period 8; {3,6,9}≅Z/3Z under DR-addition | Narrow proved periodicity |
| `math/theorems/theorem_157_repdigit_triple_seam.py` | Identity | Every repdigit ddd is divisible by 37, DRs cycle 3,6,9. | ddd = 111d = 3d*37. |
| `math/theorems/theorem_158_counting_palindrome_seam.py` |  | 11213141514131211 ≡ 0 mod 37 | Single narrow verified fact |
| `math/theorems/theorem_164_hmod_operator_algebra.py` | Definition | T3 = T6^2 on C[GF(37)*]; Fourier decomposition into 36 lines | Proved operator identity and decomposition |
| `math/theorems/theorem_167_twin_prime_chi_gf37.py` | Conjecture | Twin primes forced chi_-3 pattern; forbidden midpoint residues | Proved 6n±1 facts; file labelled conjecture |
| `math/theorems/theorem_172_triangular_seam_squaring_map.py` |  | ORBIT_11 = -IC; squaring maps both into IC; T(n)=0 mod 37 iff n=0,36 | Three small proved facts |
| `math/theorems/theorem_173_hexagonal_homothety_orbit_products.py` | Algorithm | Three orbit-coset products (DARK_A x SS = TESLA_ORB, etc.) from hexagon dimensions. | Verified coset multiplication facts. |
| `math/theorems/theorem_183_boundary_principle_gf37.py` |  | n-ball boundary equals interior measure at r=n | Derivation then tagging |
| `math/theorems/theorem_197_coset_3cycle_gf37.py` | Identity | Every 137-map 3-cycle sums to 0 mod 37; coset partition classified. | Proved via g(1+26+10)=37g. |
| `math/theorems/theorem_198_trinity_sequence_gf37.py` | Definition | {3,6,9} closed under DR addition; ST = DR-3 residues exactly | Narrow proved facts |
| `math/theorems/theorem_202_harmonic_pairs_gf37.py` | Definition | 18 harmonic pairs a+b≡ab mod 37 enumerated; (4,26) unique to 30 | Defines harmonic pairs and proves narrow facts |
| `math/theorems/theorem_206_pell_sqrt_gf37.py` | Algorithm | √37=[6;12̄]; Pell fundamental solution (73,12); y mod 37 | Narrow verified facts |
| `math/theorems/theorem_208_cubing_map_gf37.py` | Identity | Each coset of <26> satisfies pure cubic x^3 = 8^k mod 37. | Proved via vanishing symmetric functions of {r,10r,26r}. |
| `math/theorems/theorem_210_trinity_dr_arithmetic_gf37.py` |  | {3,6,9} ≅ Z/3Z under DR-addition; DR-products collapse to 9 | Narrow proved facts |
| `math/theorems/theorem_212_twin_prime_rh_gf37.py` | Algorithm | Twin primes p>3 have DR pairs (2,4),(5,7),(8,1) only | Proved mod 9 case analysis |
| `math/theorems/theorem_216_buckingham_pi_gf37.py` | Algorithm | Buckingham Pi null space rank 3, nullity 2 preserved mod 37. | Narrow fact; scope note says holds mod any suitable prime. |
| `math/theorems/theorem_217_torus_z37_z81.py` | Algorithm | Torus map on Z_37×Z_81 has period 111 via gcd/CRT. | Short proved period fact. |
| `math/theorems/theorem_220_barrier_c_mod3.py` |  | c = 1 mod 3 so c not in orbit of 3-map from multiples of 3 | One-line proved fact |
| `math/theorems/theorem_222_seed_times2_negh.py` |  | Multiplication by 2 maps SEED {18,24,32} onto NEG_H | Narrow verified fact |
| `math/theorems/theorem_232_f_hexad_mirror_differences.py` | Identity | F-hexad mirror differences are divisible by 137 and generate full orbits. | Proved narrow facts about \|abababab - babababa\|. |
| `math/theorems/theorem_240_rule30_path_to_problem2_gf37.py` | Conjecture | Proves P2 (orbit bias vanishing) implies Rule 30 Problem 2. | Implication proved; Problem 2 itself remains open. |
| `math/theorems/theorem_241_rule30_right_boundary_2adic_gf37.py` | Algorithm | Rule 30 left-permutive; right boundary runs backward; 2-adic periods. | Proved properties with computation. |
| `math/theorems/theorem_251_n251_parity_architecture_gf37.py` |  | Orbit parity split: {5,13,19} unique all-odd, {18,24,32} unique all-even. | Exhaustive check of a finite statement. |
| `math/theorems/theorem_252_cyclic_cubic_gf37.py` | Algorithm | Cube roots of 27 mod 37 are {3,4,30}; 4 solutions of cyclic system | Small proved facts |
| `math/theorems/theorem_264_a078358_oblong_gf37.py` | Algorithm | n(n+1) = r mod 37 solvable iff 1+4r is QR; orbit oblong partition. | Narrow proved criterion plus orbit classification. |
| `math/theorems/theorem_266_n123_multiples_dr369_gf37.py` |  | 123k DR cycle 6,3,9; 123k mod 37 permutes residues, each orbit thrice | Narrow proved facts |
| `math/theorems/theorem_269_sophie_map_gf37.py` | Definition | S(x)=2x+1 is a bijection mod 37; unique fixed point 36; seam preimage 18. | Short proved facts about one affine map. |
| `math/theorems/theorem_271_collatz_map_gf37.py` |  | 3x+1 mod 37 has fixed point 18, seam preimage 12 | Proved narrow map facts |
| `math/theorems/theorem_274_seed_nqr17_inverse_gf37.py` |  | SEED and NQR17 are inverse orbits; products land in IC | Narrow proved fact |
| `math/theorems/theorem_276_kolakoski_gf37.py` | Algorithm | Kolakoski A078649 gap set is exactly {2,3,4}; residues mod 37 | Proved gap bound plus computations |
| `math/theorems/theorem_290_squaring_map_exact_sequence_gf37.py` | Corollary | Squaring induces ×2 on Z/12Z; kernel H_2, image H_6. | Proved via T285 discrete-log fact; two tests failed. |
| `math/theorems/theorem_297_block_separation.py` | Audit | Separates group-derivable results from curve results; falsification test. | Proved boundary between Block 1 and Block 2. |
| `math/theorems/theorem_301_cyclotomic_slot_table.py` | Algorithm | Primes with ord_p(137)=d are factors of Phi_d(137); table d=1..12 | Standard mechanism verified and tabulated |
| `math/theorems/theorem_309_alternating_digit_swap_chain_gf37.py` | Audit | Alternating-digit-swap chain has period 6 mod 37 for all 81 pairs | Exhaustive finite check, forced by rendering |
| `math/theorems/theorem_311_triad_lock_and_subgrid_map_gf37.py` | Audit | dr(2A)=dr(T_A) exactly when 3\|A; sub-grid map; three claims corrected. | Proved via A(A-3)=0 mod 9. |
| `math/theorems/theorem_312_repdigit_chain_complete_gf37.py` | Corollary | Repdigit chain a..aaaa for all digits; all columns forced | Aaa column follows from T310 named |
| `math/theorems/theorem_315_base_ten_block_and_cofactor_gf37.py` | Algorithm | 10+11 unique reversal-preserving split of 21; 10 -> 27 cofactor chain. | Narrow facts derived and checked by brute force. |
| `math/theorems/theorem_318_permutation_vs_functional_gf37.py` |  | 26x cycles are mu_3 cosets; T(x)=x^3+33 is not a permutation on them. | Proved distinction; narrow. |
| `math/theorems/theorem_319_lift_machine_gf37.py` | Definition | Lift grid partitions 1..9 iff seed meets each +3 orbit once | Proved iff over finite set |
| `math/theorems/theorem_327_counting_stack_123_246_369_gf37.py` | Definition | Counting stack 123/246/369 = 123k; differs from rotation stack | Small proved facts |
| `math/theorems/theorem_331_orbit_sum_37_74_negation_gf37.py` | Audit | Every 137-orbit sums to 37 or 74; negation swaps halves. | Proved narrow fact; corrected by T340, prior art noted. |
| `math/theorems/theorem_339_orbit_index_safe_semiprimes_gf37.py` | Definition | Orbit index F_37*/<10> = Z/12 explains safe prime and semiprime hits. | Proved facts; quotient itself credited to T138/T285. |
| `math/theorems/theorem_342_sandwich_numbers_sigma_gf37.py` |  | n+(n+1)=sigma(n); 26 and 8,9 are classical uniqueness numbers. | Narrow identification; GF(37) reading null. |
| `math/theorems/theorem_343_eisenstein_reconciliation_gf37.py` | Audit | Six results equivalent to 37 = 1 mod 3 (Tier A) | Proved equivalences reconciling prior files |
| `math/theorems/theorem_344_no_golden_ratio_gf37.py` |  | x^2-x-1 has no root mod 37 since 5 is a non-residue. | Narrow proved fact via quadratic reciprocity plus exhaustion. |
| `math/theorems/theorem_350_kaprekar_rotation_decomposition_gf37.py` | Identity | Kaprekar step equals 99(a-c); 495 unique fixed point. | Closed form proved, narrow. |
| `math/theorems/theorem_351_anchor_gap5_pairing_gf37.py` | Identity | SA has gap-5 and equal-sum pairings that cross | Identity 4+30 = 9+25 |
| `math/theorems/theorem_352_why_37_uniqueness_gf37.py` |  | 37 is the only prime with ord_p(10)=3; notes T304 prior art. | Proved via Phi_3(10)=111=3*37. |
| `math/theorems/theorem_355_conjugate_orbit_and_layer3_gf37.py` | Audit | Conjugate CTC^-1 orbit has preperiod 1 into a 6-cycle; Layer III d=7 forced. | Proved narrow dynamics facts plus assessment. |
| `math/theorems/theorem_359_length_vs_digital_root.py` | Identity | DS(R_k) = 9k; DR(R_k) constant; DS(R_k)+k = 10k | Identity digitsum(10^k-1)+k = 10k |
| `math/theorems/theorem_361_index_shift_primes_composites.py` | Audit | a_n+n on primes and composites overlap three terms; break forced | Narrow proved statement on supplied lists |
| `math/theorems/theorem_362_prime_pair_baseline_2_over_35.py` | Audit | Orbit self-transition baseline for prime pairs is 2/35 | Proved; corrects T347 baseline |
| `math/theorems/theorem_367_1311_rotation_areas.py` | Definition | Rotations of 1113: run-length sum 9; three areas by spread | Small verified facts |
| `math/theorems/theorem_371_12321_rotation_reversal_d5.py` | Algorithm | Rotation cycle of 12321 carries a D_5 action; rotation is not the 137-map. | Narrow proved group-action fact. |
| `math/theorems/theorem_379_shell_riemann_exact_error.py` | Identity | Shell Riemann sum error is exactly pi r^2/n; midpoint exact at n=1. | Proved narrow exact-error result on supplied derivation. |
| `math/theorems/theorem_infinite_666_resonances.py` |  | Each 666-track has infinitely many scaled-triangle resonances | Proved via gcd(17,666)=1 |
| `math/theorems/tier_ds_18k_distribution.py` | Algorithm | T(k)=DS(18k)+DS(18k-4) = 5 mod 9; tier distribution k<=1369 | Proved congruence plus counts |
| `math/theorems/triple_coupling_666_gf37.py` | Algorithm | 666 = 2*3^2*37 = T(36); 37 unique prime with T(p-1)=666. | Specific proved facts about one number. |
| `math/theorems/tripling_6cycle_gf37.py` | Algorithm | 3^6≡26 so ×3 permutes 12 orbits in two 6-cycles. | Short proved fact with witnesses. |
| `math/theorems/twelve_tone_crt_gf37.py` | Algorithm | CRT Z12 x Z37 = Z444; orbits mapped to pitch classes. | Standard CRT plus residue tabulation. |
| `math/theorems/twin_midpoint_dr_axis.py` |  | For twin pairs p>3 the midpoint has DR in {3,6,9}. | Short proof from p = 5 mod 6. |
| `math/theorems/twin_prime_chamber_gf37.py` |  | Twin prime centers classify C3/C6/C9 by m mod 3 | Proved narrow modular facts |
| `math/theorems/twin_prime_consolidation.py` |  | (6n-1)(6n+1) divisible by 37 iff n = +-6 mod 37. | Proved narrow congruence fact among collected twin-prime facts. |
| `math/theorems/twin_prime_dr_sum_audit.py` | Audit | Twin prime pair p>3 has DR(2p+2)∈{3,6,9} | Narrow proved necessary condition |
| `math/theorems/twin_prime_gf37.py` | Algorithm | No twin prime pair starts at residue 35 mod 37; +2 staircase through named residues. | Narrow proved forbidden-residue fact plus data. |
| `math/theorems/twin_prime_pipe.py` |  | Twin prime centers are multiples of 6 with DR in {3,6,9} | Proved narrow fact |
| `math/theorems/twin_prime_rh_qr_gf37.py` | Algorithm | DR of lower twin is QNR mod 37, upper twin QR. | Narrow proved fact via m mod 3 cases. |
| `math/theorems/twin_prime_riemann_framework.py` |  | Twin primes (6n−1,6n+1) have chi_{-3} pattern (−1,0,+1); forbidden midpoint residues. | Proved forced fact from 6n±1. |
| `math/theorems/two_digit_transition_gf37.py` | Definition | Four digit-transition deltas +-11,+-9 and their residue pairings | Small proved facts |
| `math/theorems/two_group_split.py` | Algorithm | The 12 137-map cycles split 6/6 into sums 37 and 74. | Proved: sum = 0 mod 37 and bounded in [3,108]. |
| `math/theorems/unit_scalar_init_gf37.py` |  | Basin-preserving scalars are exactly IC={1,10,26}; C=1 fixes every element. | Narrow coset proof. |
| `math/theorems/zero_comma_complete_theorem.py` | Definition | Zero-comma label formula; all-same labels occur only for K<=3. | Short proved statement about a defined label. |

## Lemma (3)

| File | Secondary | Statement | Evidence |
|---|---|---|---|
| `math/lemmas/heartbeat_3cycle.py` | Theorem | ord37(26)=3, so every nonzero residue lies in a 3-cycle; 12 disjoint cycles. | Short proof of one order fact, used as step for orbit structure. |
| `math/lemmas/theorem_313_add_nine_reversal_diagonal_gf37.py` | Proposition | n+9=rev(n) on two digits iff b=a+1; eight solutions | Small forced derivation used as step toward T314 |
| `math/theorems/mod9_midpoint.py` | Audit | 5 is the mean of {1..9}; tier values T(k)=5 mod 9. | Small fact used as a step for the tier constraint; corrects a sketch. |

## Corollary (4)

| File | Secondary | Statement | Evidence |
|---|---|---|---|
| `math/theorems/mirror_set_generator.py` | Proposition | Digit permutations of n = 0 mod 9 also = 0 mod 9 | Follows from dr_modular_foundation.py Theorem 1 (DR(n)=n mod 9) |
| `math/theorems/theorem_286_subgroup_lattice_z12_gf37.py` | Algorithm | Subgroup lattice of Z/12Z lifted to GF(37)* via the orbit quotient. | Parent named: T285 (GF(37)*/IC = Z/12Z). |
| `math/theorems/theorem_332_six_six_forced_inversion_closed_gf37.py` | Proposition | 6/6 split of orbit sums forced by total 666; two inversion-closed orbits. | Names T331 (orbit sums 37 or 74). |
| `math/theorems/theorem_354_fb_trajectory_gf37.py` |  | f_b orbit of 18 equals C applied to f_a orbit | Follows from T353 conjugacy |

## Claim (2)

| File | Secondary | Statement | Evidence |
|---|---|---|---|
| `math/theorems/lob_691_695.py` | Algorithm | 3+8=11, 5+8=13; 695 mod 37=29, digit sum 11. | Minor arithmetic statements within the LoB series. |
| `math/theorems/theorem_256_mahalanobis_gf37_orbits.py` | Algorithm | Reads 137-map as covariance, x10 as precision; orbits as Mahalanobis classes. | Correspondence statement inside argument; not a proof. |

## Identity (14)

| File | Secondary | Statement | Evidence |
|---|---|---|---|
| `math/lemmas/theorem_310_digit_chain_seam_gf37.py` | Lemma | aba=111a is 0 mod 37 for every digit a; DR pattern 3,6,9 forced | 111a ≡ 0 (mod 37) for all a, since 111=3·37 |
| `math/theorems/concatenation_123_repunit.py` |  | N_n (n 1s, n 2s, n 3s) block sum equals 6*R_n for all n. | Identity: R_n + 2R_n + 3R_n = 6R_n for all n>=1. |
| `math/theorems/digit_repetition_dr_audit.py` |  | DR(11k)=DR(2k), DR(111k)=DR(3k) for digits k=1..9. | DR(11k)=DR(2k) and DR(111k)=DR(3k) since 11≡2, 111≡3 mod 9. |
| `math/theorems/equivalence_24_coupling.py` | Proposition | For all a+b=24, DR(a)+DR(b) reduces to 6. | DR(a)+DR(24-a) ≡ 24 ≡ 6 (mod 9) for all a. |
| `math/theorems/mirror_cycle_audit.py` | Audit | Mirror subtraction grid; A−B = 9(10001d − 11111 next(d)) so DR=9 | A−B = 9·(10001·d − 11111·next(d)) |
| `math/theorems/mirror_triplet_cascade.py` | Algorithm | Consecutive-digit mirror sums abc+cba=2b·111 form series step 666 | abc+cba = 2b×111 for consecutive digits |
| `math/theorems/permutation_dr_99.py` |  | For 3-digit N and reverse R, N-R=99(a-c). | N-R=99(a-c) for all digits a,b,c. |
| `math/theorems/repunit_37_identity.py` |  | nnn/(n+n+n)=37 for every digit n | nnn/(3n) = 37 since nnn = 3·37·n |
| `math/theorems/repunit_sequence_audit.py` | Proposition | digit_sum(R_n^2)=n^2 and digit_sum(R_n R_{n+1})=n(n+1); period mod 37. | digit_sum(R_n^2)=n^2 (n≤9), digit_sum(R_nR_{n+1})=n(n+1). |
| `math/theorems/sequence_30303_doubling.py` | Algorithm | 30303*2^k patterns; xy*10101=xyxyxy | Identity xy*10101=xyxyxy for two-digit xy |
| `math/theorems/shell_octave_identity_gf37.py` | Proposition | (2k+1)^2-(2k-1)^2 = 8k and 1+sum 8j = (2k+1)^2. | (2k+1)^2 - (2k-1)^2 = 8k for all k. |
| `math/theorems/theorem_214_dr_symmetric_pair_duality.py` |  | DR(n+k)+DR(n−k) ≡ DR(2n) mod 9 for all k | DR(n+k)+DR(n−k) ≡ DR(2n) (mod 9) |
| `math/theorems/three_block_ladder.py` | Algorithm | 3·(3…3)_k + 1 = 10^k for each k; rows reduced mod 37 | 3·(10^k−1)/3 + 1 = 10^k |
| `math/theorems/z2701_37x73_qed.py` |  | 2701 = 37×73 = T(73); DR 1; QED α notes | T(73) = 73·74/2 = 37·73 |

## Formula (8)

| File | Secondary | Statement | Evidence |
|---|---|---|---|
| `math/theorems/circulant_avg_37.py` | Proposition | Closed-form eigenvalues and spectral gap of circulant averaging operator on Z/37 | Symbolic eigenvalue formula, numerically checked |
| `math/theorems/explicit_formula.py` | Algorithm | Truncated Riemann explicit formula approximating pi(x) | Computes pi(x) from zeros via standard formula |
| `math/theorems/meromorphic_trajectory_map.py` | Heuristic | Poles of 0.3/(4cos(i/21)) and adaptive-step sampling prescription | Symbolic pole formula and step rule |
| `math/theorems/one_zeros_nine_pattern.py` | Proposition | 1[0^n]9: comma count floor((n+1)/3), DR 1, mod-37 period 3 | Rule for computing comma count and residue |
| `math/theorems/psi_operator_audit.py` | Definition | Defines Psi(a,b,c) and gap formula for its first difference | Symbolic rule dPsi = 2(g_n+g_{n+1}) - g_{n+2} |
| `math/theorems/theorem_213_middle_digit_operation.py` | Algorithm | Middle-digit operation op_sum = 2(a+3b+c); digit-sum-10 case 20+4b. | Symbolic rule used to compute results. |
| `math/theorems/triadic_seed_mu3_gf37.py` | Definition | P_k(t)=r(t)(cos 2πk/3, sin 2πk/3,0) indexed by mu_3={1,10,26}. | Fills in an undefined formula for vertex positions. |
| `math/theorems/zeno_spatial_scaling.py` | Other | f(n)=100(0.5)^(n-1); sum 200; crossover and residue readings | Geometric series formula |

## Counterexample (5)

| File | Secondary | Statement | Evidence |
|---|---|---|---|
| `math/theorems/parity_proof_z2_audit.py` | Proposition | Shows point reflection and axial flip differ on Mat_3(Z2) via generic matrix | Refutes σ_p = σ_a (supplied parity proof's collapse claim) |
| `math/theorems/theorem_149_kakeya_jacobian_dimension_gf37.py` | Other | Records a 3D polynomial map with det J = -2 that is not injective. | Refutes the Jacobian Conjecture (dimension 3). Verified 2026-09-29: det(JF) = -2 identically (sympy); 3 distinct points share image (-1/4,0,0). Attribution not verified. |
| `math/theorems/theorem_244_rule30_right_boundary_period_formula_gf37.py` | Algorithm | Rule 30 right-boundary period exponents from simulation | Refutes e_R(j)=floor((2j+1)/3) for j>=10 |
| `math/theorems/theorem_329_dr_orbit_invariance_refuted_gf37.py` | Audit | DR not invariant on 137-orbits; wrap-count law replaces it | Refutes 'all orbit elements share the same DR mod 9' |
| `math/theorems/theorem_363_ac_lead_oscillates_quadratic_census.py` | Algorithm | A and C quadratic prime counts swap lead 90 times below 300000. | Refutes census ordering 'A > C' as fact about the forms. |

## Conjecture (1)

| File | Secondary | Statement | Evidence |
|---|---|---|---|
| `math/theorems/theorem_308_reversal_build_mod37_period_gf37.py` | Algorithm | Reversal-build recurrence mod 37 eventually periodic, period 3 or 6, seeds 0..399. | Result only checked in tested range; mechanism not proved. |

## Algorithm (297)

| File | Secondary | Statement | Evidence |
|---|---|---|---|
| `math/theorems/abbc_manifold_grid.py` | Conjecture | Enumerates digit-pair sum grid by sum blocks; records DR chains; 13/14 zeta crossing marked conjecture. | Verified tabulation of specific sums; one item explicitly labelled CONJECTURE. |
| `math/theorems/abc_row_sequence.py` | Audit | Generates ABC rows n=0..10 and their tuple sums mod 37; flags source-image errors | Row generation procedure; output is a table, with error flags |
| `math/theorems/agm_theta_elliptic_audit.py` | Identity | Numerically implements AGM, Gauss-Legendre pi, theta inversion, Landen transform, K(k). | Computes standard pipeline numerically; no asserts, no new proof. |
| `math/theorems/allpaths_module2_seed.py` | Audit | Computes digit reversal, mod-3^k phase vector and outer-product matrix for seed 123296682. | Step-by-step computation producing data; notes source dr(0) convention discrepancy. |
| `math/theorems/alpha_grid_growth_pattern_connection.py` | Definition | Maps n,2n,3n growth table rows onto alpha grid positions | Tabulates and tags values; no proved general statement |
| `math/theorems/alternating_12_structures.py` | Proposition | Computes mod-37 orbits of alternating 1-2 digit sequences, palindromes, tables. | Enumerates and prints residues; asserts check computed values. |
| `math/theorems/bivariate_grid_audit.py` | Definition | Describes 3x3 matrix with row step 90, singular step 80, checks residues. | Computes and checks stated relations of a given matrix; proves nothing general. |
| `math/theorems/board_row_col_numbers_mod37.py` |  | Reads 3x3 board rows/columns as numbers, reports residues mod 37 and DR patterns. | Computes and labels residues of specific numbers; no general proof. |
| `math/theorems/burau_braid_gf37.py` | Other | Classifies Burau faithful strand counts and history years into GF(37) sets | Only computes residues of cited numbers; proves nothing new |
| `math/theorems/carmichael_37_structure.py` | Proposition | Searches cyclotomic-type Carmichael numbers to k=20000; explains 37 divisibility | Search output with side derivations of residue conditions |
| `math/theorems/cascade_8_13_24.py` | Proposition | Subset-sum closure of {8,13,24} yields exactly 37 integers; lists properties | Construction procedure whose output is a set; properties verified by computation |
| `math/theorems/closing_threads.py` | Conjecture | Closes two threads: ord_p(10) lift search; checks predicted floor(gamma_11) mod 37=15. | Computes search and pre-registered prediction check; no proof. |
| `math/theorems/collision_node_20979.py` |  | Factorization and DR properties of 20979=3^4*7*37 and its reversal. | Computes facts about one number; notes non-uniqueness. |
| `math/theorems/compact_generation.py` | Definition | Computes compression ratios for several structures under a 'compact generation' notion. | Computes and prints ratios; no proved statement. |
| `math/theorems/comprehensive_structures.py` |  | Implements Reed-Solomon, BCH, narcissistic checks, meta-evolve engine | Collection of computational implementations |
| `math/theorems/consecutive_digit_triples.py` | Proposition | Digit-grouping sums of consecutive triples reduce to DR 6 or 3; residues mod 37 | Computes groupings/residues of user observations |
| `math/theorems/constants_gf37_decimal.py` | Proposition | Computes decimal digit sums of constants; sqrt(3) first 10 digits sum to 37. | Digit-sum computation outputs data about specific expansions. |
| `math/theorems/continued_fraction_R3252.py` | Proposition | Continued fraction [0;3,13,3,19,1] of 813/2500 with convergents and residues. | Computes an expansion and residues; labelled Theorem but only computes. |
| `math/theorems/cooley_tukey_ntt_audit.py` | Audit | Cooley-Tukey NTT over F5 checked against naive NTT | Implements procedure and cross-checks output |
| `math/theorems/coset_orbit_137_audit.py` | Audit | Computes coset coordinates and multiples of 37 along orbit 137+4k. | Computation and printing only; no asserts. |
| `math/theorems/criss_cross_17_81_audit.py` | Identity | DR structure of {17,71,18,81}: sums, products, repetitions, alternating strings. | Tabulates digital roots; uses DR multiplicativity. |
| `math/theorems/cunningham_modulus_audit.py` | Audit | Computes Cunningham chains of factors of 191919919191 and parity-field facts. | Enumerates chains and verifies properties; output is data. |
| `math/theorems/cyclo_ntt_sl2_gf37.py` | Identity | Implements cyclotomic prime families, length-8 NTT mod 17, SL2(F_37) generators. | Operator implementations verified by asserts; 10*137-37^2=1 checked. |
| `math/theorems/dhananjaya_prana_engine.py` |  | Maps engine quantities (4c, 499 s, 3c) to named GF(37) sets. | Residue lookups of supplied values; nothing general proved. |
| `math/theorems/diamond_core_gap_chain_audit.py` | Audit | Gap chain of Diamond Core read order and residues of 26095/8 | Computes gaps and matches; no proof |
| `math/theorems/digit_circle_5_center.py` | Other | Computes pair sums and complement pairs on digit line centered at 5 | Only computes and asserts digit arithmetic; no general statement |
| `math/theorems/digit_cycles_1_9.py` |  | Chains digit pairs into three cycles partitioning 1..9 | Enumerates constructed cycles; no proof |
| `math/theorems/digit_rotation_patterns.py` |  | Enumerates 3-digit rotation numbers, partition trios, and D4 grid orientations | Enumeration and tabulation; no general proved result |
| `math/theorems/dimensional_bridge.py` |  | Finds smallest N with sum of first N primes >37*phi and divisible by 7. | Search procedure; output N=8, sum 77. |
| `math/theorems/discrete_cue_discretization.py` |  | Discrete Vandermonde weights and spacing variance on Z/9, Z/37, Z/333. | Computes weights and statistics; output is data. |
| `math/theorems/displacement_sync_13699631.py` | Definition | Sliding cursor over palindrome 13699631; primality and mod-37 of each split | Computes properties of one number; labelled Theorem but proves nothing general |
| `math/theorems/divisor_prefix_ledger.py` | Proposition | Mechanized ledger/oracles for n = sum of squares of k smallest divisors | Enumeration machinery with proved oracle levels |
| `math/theorems/divisor_strings.py` | Counterexample | Enumerates palindromic proper-divisor strings for n in 11..99. | Enumeration; also refutes claim all multiples of 11 contain '111'. |
| `math/theorems/doubling_dr_cycle_audit.py` | Identity | Tabulates doubling in DR space; notes DR(repunit_n)=n for n=1..9. | Computes and prints sequences with checks; no general proof. |
| `math/theorems/dr_addition_table.py` | Definition | Builds a self-feeding (1)+n digital-root addition table. | Computes a table from user notation; no proof. |
| `math/theorems/dr_chain_52_25_41.py` |  | Computes digit roots and residues for 52, 25, 41 | Tabulates arithmetic; nothing proved |
| `math/theorems/dr_number_theory_module.py` | Identity | Module of digital-root, perfect number, DR-Fibonacci functions | Utility functions; dr(37k)=dr(k) since 37≡1 mod 9 |
| `math/theorems/e8_coset_incidence.py` | Audit | Builds E8 248×30 height incidence matrix; notes sympy root convention bug | Construction/computation output is data |
| `math/theorems/eleven_thirtyseven_ops.py` |  | Arithmetic of 11 and 37 (sum, difference, product, quotient) mapped to orbit labels. | Lists computed values; no general statement. |
| `math/theorems/emirp_digit_aware_baseline.py` | Audit | Digit-permutation null model for emirp mod-m bias, comparing m=37 and m=31. | Monte Carlo baseline computation producing Z-scores. |
| `math/theorems/emirp_five_moduli_zscores.py` |  | Computes emirp reversal-residue Z-scores for five moduli | Statistical computation; output is data |
| `math/theorems/emirp_gap_spectral_dr.py` |  | Gap-conditioned Markov spectral analysis and chi-square test on emirp DR transitions. | Statistical computation; outputs data, proves nothing. |
| `math/theorems/emirp_k_mod37.py` | Proposition | Histogram of emirp K-statistic mod 37; symmetry and zero bins. | Enumerates emirps below 10^5 and tabulates. |
| `math/theorems/emirp_mod37_nonuniformity.py` | Heuristic | Chi-square test finds emirps nonuniform mod 37 (Z≈2.93) not mod 31,41,43 | Statistical measurement over data; not proved |
| `math/theorems/emirp_mod37_spectral_audit.py` |  | Emirp mod-37 frequency vector, chi-square test, Markov matrix eigenstructure to 10^6. | Statistical computation; output is data. |
| `math/theorems/emirp_moduli_comparison.py` |  | Chi-squared of emirp residues mod 31,37,41,43 up to 1e6 | Statistical computation; outputs data |
| `math/theorems/eta24_ramanujan_tau_gf37.py` | Other | Computes Ramanujan tau mod 37 and labels exponent 24 and weight 12 by named sets. | Computation and set-membership labelling; nothing proved about tau. |
| `math/theorems/euler_quadratic_twin_audit.py` | Audit | Compares prime/twin output of three quadratic polynomials; parity and mod-3 filters | Counts and comparisons; output data |
| `math/theorems/fibonacci_dr_audit.py` | Audit | Fibonacci DR period 24 and orbit of 133+4k mod 37 | Computes periods/distributions; no asserts |
| `math/theorems/fibonacci_grid_four_readings.py` |  | Reads 4×5 Fibonacci-seed digit grid four ways; computes mod 37 and DR | Only computes readings |
| `math/theorems/fibonacci_mathieu_gf37.py` |  | Fibonacci mod 37 seam, Mathieu orders mod 37, radical anchors | Residue tabulations of observations |
| `math/theorems/field_55_mirror_structure.py` |  | Pair-sum and zero-migration arithmetic of seven 8-digit palindromic seeds. | Computes and asserts observations on specific numbers. |
| `math/theorems/fold_audit.py` | Audit | Computes four fold vectors of 18-digit sequences for linear and mirrored cases | Enumerates fold outputs as data |
| `math/theorems/fold_mirror_transform_gf37.py` |  | Fold+mirror transform on 1234(0)6789 and residues mod 37 | Computes transformed values and residues |
| `math/theorems/fps37_scanner.py` | Audit | 37-field feature-vector scanner; fixes has_sqrt to use true QRs mod 37 | Tooling procedure computing features; includes bug fix |
| `math/theorems/fraction_103_137.py` |  | Decimal expansion of 103/137 period 8 and related residues | Computes expansion and residues |
| `math/theorems/frequency_888_audit.py` |  | Factors 888 and lists residues | Computational tagging of one number |
| `math/theorems/fvk_gamma_extension.py` | Claim | Computes gamma=1/eps^2 mod 37 for three eps values from T387. | Residue computation; 'GF(37) selects them' is unproved claim. |
| `math/theorems/g4_parameter_sweep.py` | Formula | Derives spectral-center formula and sweeps K(alpha,beta) spectra over a grid. | Parameter sweep output is data; one formula derived. |
| `math/theorems/g4_spectral_decomposition.py` | Audit | Builds G4 regular representation, projectors, block-diagonalizes Cayley operator | Implements spectral computation |
| `math/theorems/g5_engine.py` |  | G'5 engine simulation validating psi=1 across stages | Simulation; self-label Theorem not supported |
| `math/theorems/gf37_error_correction.py` | Audit | Reed-Solomon (10,6) and BCH over GF(37); fixes syndrome bug. | Encoding/decoding procedure implementation. |
| `math/theorems/ghost_kervaire_chain_gf37.py` | Corollary | Partial sums 6,13,30,62,80 mod 37 labelled; K(p)=2^p-2 = 0 mod p. | Chain computation; Fermat-SEAM part follows from named Fermat's little theorem. |
| `math/theorems/goldbach_gf37.py` | Proposition | Tabulates Goldbach decompositions by mod-37 class; 37-component rule q≡n | Mostly tabulation; rule is trivial |
| `math/theorems/goldbach_proof_attempt_gf37.py` | Conjecture | Residue-level Goldbach decomposition coverage mod 37 | Computation; states no classical proof results |
| `math/theorems/golden_mean_fibonacci_audit.py` | Claim | Lists Fibonacci/golden-mean facts (Pisano mod 9, 37\|F(19)) linked to framework. | Computes connections; no supplied claim audited, no proof. |
| `math/theorems/golden_path_sequence.py` |  | Generates digit for any t>=9 from three 8-row color cycles. | Lookup procedure producing output values. |
| `math/theorems/group_g54_representation.py` | Theorem | Computes conjugacy classes and irreps of Z9⋊C6 (order 54) | No asserts; computes and prints the table |
| `math/theorems/growth_pattern_full_333.py` |  | Prints full 333-row growth table with tags | Table generation |
| `math/theorems/growth_pattern_n_2n_3n.py` | Definition | Tabulates rows n,2n,3n with DR and mod-37 periods 9, 37, 333. | Table generation with checks. |
| `math/theorems/hejhal_maass_level1.py` |  | Hejhal's algorithm finds Maass eigenvalues on SL2(Z) | Numerical procedure, data output |
| `math/theorems/hexacosichoron_600cell.py` |  | Generates the 120 vertices of the 600-cell and element counts mod 37. | Vertex generator; output is data despite 'Classification: Theorem'. |
| `math/theorems/hose_flow_transient.py` |  | Digit strings 000->111 and 000->100->010->101 tracked mod 37. | Computes residues of two strings; analogy narrative, nothing general. |
| `math/theorems/hybrid_recurrence_16_96_audit.py` | Audit | Two-phase recurrence 16,32,48,64,96 with span-3 continuation | Defines and generates a sequence |
| `math/theorems/hydrogen_orbital_gf37.py` | Other | Maps hydrogen orbital counts n^2 mod 37 into named sets. | Computes residues and labels; nothing proved. |
| `math/theorems/k5_odd_shapes.py` | Lemma | Reduces three open k=5 divisor shapes to bounded searches; runs them | Searches complete per parameter; shapes not closed |
| `math/theorems/kalman_f26_closed_loop.py` | Other | Closed-loop Kalman estimator with R=1/137, P0=37 on Z/37. | Step-by-step control procedure; label 'Theorem' not applied. |
| `math/theorems/kaprekar_6174.py` | Theorem | Exhaustively runs Kaprekar's routine on 4-digit numbers, reaching 6174 | Exhaustive computation of known result; outputs step distribution |
| `math/theorems/kervaire_addend_chain_gf37.py` | Audit | Tabulates partial sums of chain 2,4,8,16,32,12,4,2 vs Kervaire dimensions | Computes chain residues; notes ghost step |
| `math/theorems/kervaire_ghost_gf37.py` |  | Kervaire dimensions reduced mod 37 and classified | Residue tabulation |
| `math/theorems/ladder_11_111.py` | Other | Records +11 and +111 ladders from 26 and 30 (137, 136, 141). | Arithmetic observations asserted; tagged OBSERVED, nothing proved. |
| `math/theorems/lane_generator_246_gf37.py` |  | Divisors of 246 mapped to residues mod 37 | Tabulation of residues |
| `math/theorems/layer30_dr_matrix_entropy.py` |  | Builds 9x9 DR multiplication matrix and computes DR orbit entropy. | Computation producing a matrix and entropy value. |
| `math/theorems/layer30_sovereign_matrix_entropy.py` | Definition | Builds 9x9 DR matrix and computes its DR entropy | Construction plus computed entropy |
| `math/theorems/layer_trinity_factor_lattice.py` |  | Factor lattice of N=2244220 and residues of labels mod 37. | Computes divisors and residues of one number. |
| `math/theorems/lights_out_gf2_gf37.py` | Other | Lights Out as GF(2) linear system: light chasing and null space | Solution procedures; GF(37) notes |
| `math/theorems/linear_form_11n_37m_primes.py` | Theorem | Enumerates primes of form 11n+37m; cites Dirichlet | Search output; cited external theorem |
| `math/theorems/lob_44_9_bilateral_369_lock.py` | Audit | Computes block DRs, residues and /3 quotient of a 24-digit number | Computes properties of one number |
| `math/theorems/lob_591_592_595.py` | Other | Computes nodes n=4 mod 5 with DR=1 and 595 mod 74 = 3. | Computation with a placeholder; nothing proved. |
| `math/theorems/lob_601_602_605.py` |  | DR computations on time values 21:42, 04:50, 605 | Arithmetic tabulation |
| `math/theorems/m14_scraper_engine.py` |  | Enumerates permutations of 14-digit multiset; DR fingerprints | Enumeration engine |
| `math/theorems/mc_sensitivity_analyzer.py` | Other | Monte Carlo sensitivity validation engine code as provided | Tooling code; audit is in separate file |
| `math/theorems/medusa_137_resonance.py` | Definition | Scans nodes n where (137n mod 37) has DR 3; finds {4,9,25,30}. | Scan procedure; output is data. |
| `math/theorems/medusa_guard.py` | Definition | Classifies nodes SECURE/WARNING/ALERT by DR of 137-map residue. | Classification procedure; corrects pillar set. |
| `math/theorems/mersenne_digit_boundary_analysis.py` | Audit | Analyses digit-length boundaries of 2^n-1 and tests mod-9 and mod-6 coincidences. | Counting against baselines; refutes a mod-9 pattern. |
| `math/theorems/mirror_seam_antipode.py` |  | 33+4, 33+3, 66+7 DR palindrome and 37/73 reversal residues. | Records arithmetic of specific numbers; nothing general proved. |
| `math/theorems/mod37_slot_audit.py` | Audit | Slot table of framework constants mod 37 and descent 191→100. | Tabulates residues; output is data. |
| `math/theorems/mod4_1_sequence_audit.py` | Audit | Enumerates 4n+1 up to 1001: primes, mod-37 residues, framework values | Enumeration output of data |
| `math/theorems/mod9_grid_audit.py` | Proposition | Grid (xA+yB) mod 9: Latin-square sweep; gcd(A,9),gcd(B,9) decide Latin | Construction and parameter sweep; no asserts |
| `math/theorems/monte_carlo_pi_gf37.py` |  | pi digits 314, 355, pi[:18] residues mod 37 mapped to named sets. | Residue lookups on specific numbers. |
| `math/theorems/monte_carlo_prime_streams.py` |  | Monte Carlo prime stream distribution, Chebyshev bias, chi-squared | Simulation outputting statistics |
| `math/theorems/multi_layer_obstruction_gf37.py` |  | Maps obstruction families to GF(37) named sets | Analogy with residue tabulations |
| `math/theorems/multiplication_dr_chains_audit.py` | Audit | Computes DR chains for seeds 2-5 under multiplier sequences. | Runs chains and verifies terminal DRs. |
| `math/theorems/mws_framework_verified.py` | Audit | Verified computations: emirp mirror, gematria, word values, corrections. | Mostly prints computations; notes some earlier claims false. |
| `math/theorems/one_two_three_generator.py` | Other | Lists aggregates of {1,2,3} and labels them with named sets. | Arithmetic facts computed and labelled; nothing proved. |
| `math/theorems/open_closed_grid_theorem.py` |  | Open/closed grid digit sums giving 37 | Arithmetic of a drawn grid |
| `math/theorems/orbit11_triple_convergence_458689_gf37.py` | Claim | Three arithmetic paths from {18,24,32} reach 11; 458689 cross-pair residues. | Computes specific residues; proves nothing general. |
| `math/theorems/orbit_137_period333_audit.py` |  | Nine-step orbit of 137 under a→a+4 tracking dr, mod 37, fib-index. | Computes an orbit table. |
| `math/theorems/origami_fold_1_to_9.py` |  | Fold pairs of 1..9 sum to 10 with residues | Arithmetic tabulation |
| `math/theorems/palindrome_1234_audit.py` | Proposition | Permutation palindromes of {1,2,3,4}: DRs, residues mod 37, factorization. | Enumerates and reports computed findings. |
| `math/theorems/palindrome_1888081808881.py` |  | Digit, factor and mod-37 analysis of palindrome 1888081808881 | Computes properties of one number |
| `math/theorems/parity_diamond_9x9.py` | Definition | Defines 9x9 Manhattan diamond grid and counts E/O cells. | Constructs grid and counts; labelled Theorem but computes. |
| `math/theorems/pascal_row8_mod37.py` | Other | Pascal row 8 coefficients: DRs, residues mod 37, partial sums | Computes and labels residues |
| `math/theorems/pattern_1234_5_1234_gf37.py` |  | Classifies 16 numbers (1-4)5(1-4) by parity and residue mod 37. | Enumeration and labelling. |
| `math/theorems/pattern_verification.py` | Other | Raw verification of user digit patterns; prints results | CLASS: NOTE; only computes and prints |
| `math/theorems/pattern_verification_audit.py` |  | Verifies five digit patterns and tags residues | Computes arithmetic of patterns |
| `math/theorems/payload_digit_structure.py` |  | Mirror-pair sums and residues of the digits of 23572481523. | Computes observations on one number. |
| `math/theorems/penrose_tiktok_gf37.py` | Proposition | Reduces Penrose-patch and TikTok numbers mod 37 into cosets of H | Computes residues of supplied numbers; coset facts are standard |
| `math/theorems/permutation_347_137.py` |  | Digit sums of permutations of {3,4,7} and {1,3,7}. | Enumeration only. |
| `math/theorems/phase_gap_correlation_audit.py` |  | Pearson correlation of prime-gap DR phases with raw gaps | Numerical statistic |
| `math/theorems/pie_sieve_gf37.py` |  | PIE sieve counts for pi(100) reduced mod 37 and DR. | Computes sieve steps and residues. |
| `math/theorems/pisot_sieve_audit.py` | Audit | Rounded plastic-constant powers, DRs, root 13 mod 37; corrects exponent | Computes sequence data |
| `math/theorems/plus2_chain_theorem.py` | Other | Arithmetic chains from consecutive pairs to 11 and 13; DR notes | Records computed chains; no general proof |
| `math/theorems/plus9_scatter_map_gf37.py` |  | Images of orbits under +9, +18, +27 shifts | Tabulation of shifted residues |
| `math/theorems/polyhedral_orbit_duality.py` | Claim | Orbit {8,23,6} sums to 37; links cube/octahedron counts to cascade base. | Computes residues and associations; no general proof. |
| `math/theorems/polymath8_maynard_gf37.py` | Conjecture | Reduces prime-gap bounds 70M, 4680, 246 mod 37. | Only computes residues; labelled Conjecture. |
| `math/theorems/prime_ap_imaginary_unit.py` | Proposition | Consecutive prime pair sums 12..36 form AP of step 6; residues | Finite computation on small primes |
| `math/theorems/prime_dr_append_audit.py` | Audit | Appends DR to two-digit primes, two layers; factorizes results | Computation producing data |
| `math/theorems/prime_gap_fold_audit.py` | Heuristic | Reconstructs prime-gap column fold rule by sliding windows | Search for an unknown rule; outputs data |
| `math/theorems/prime_power_sovereign_collapse.py` |  | Evaluates two expressions and 1468919^998 mod 37 | Computes residues |
| `math/theorems/prime_quartet_chains_palindromes.py` |  | Records arithmetic chains of {2,3,5,7}, 11x{1,4,7}, 144, palindrome table. | Computed arithmetic labelled; nothing proved. |
| `math/theorems/prime_sum_137_gf37.py` |  | Computes sum of primes up to 137 and residues mod 37. | Computation of sums; output is data. |
| `math/theorems/prime_sum_coset_sequence.py` |  | Consecutive prime sums mapped to GF(37) cosets. | Computes a sequence and classifies. |
| `math/theorems/primes_751_palindromes.py` |  | Table of primes/palindromes 751, 353, 373, 787 and cross-product digit sums. | Verified table entries; no general statement. |
| `math/theorems/primes_digits_23_audit.py` |  | Exhaustive enumeration of primes with digits {2,3}, lengths 1-7 | Search output is data |
| `math/theorems/qed_alpha_zα_structure.py` |  | Numerical checks of QED alpha values | Computation of physical constants |
| `math/theorems/ramanujan_pi_gf37.py` |  | Residues mod 37 of Ramanujan 1/pi constants | Computes residues |
| `math/theorems/ramanujan_tau_gf37.py` | Other | Counts n with tau(n)=0 mod 37 and residue distribution; printed, not asserted. | File states its only assertion tests nothing; output is data. |
| `math/theorems/ratio_177_133_identity.py` |  | Decodes user notation for 177/133: sums, differences, digit folds mod 37. | Computes and reports values. |
| `math/theorems/repunit_prime_entry.py` |  | Computes ord_p(10) entry points: 37 at k=3, 137 at k=8. | Computation of multiplicative orders. |
| `math/theorems/repunit_valuation_orbit_audit.py` | Formula | 37-adic valuation of repunits at orbit multiples via LTE | Applies known formula to table |
| `math/theorems/resonance_row_1335.py` | Proposition | 17-point resonance row DRs; any additive split of '1335' has DR 3. | Computation; DR additivity cited as reason. |
| `math/theorems/reversal_ladder_2357.py` |  | Reversal ladder of 2357 and 99^2 lock | Arithmetic tabulation |
| `math/theorems/riemann_first_zero_141.py` |  | Digits of γ₁ split into blocks reduced mod 37; digit-sum comparisons | Computes residues of digit blocks; observed layers |
| `math/theorems/riemann_gf37_coverage.py` |  | Classifies floor(gamma_n) mod 37 of Riemann zeros into 12 orbits or SEAM. | Computes zero floors; coverage is vacuous since orbits partition residues. |
| `math/theorems/rotational_spiral_analyzer.py` | Proposition | Circulant 3×3 matrix analyzer with five invariants and B↔C duality | Analyzer tool computing invariants |
| `math/theorems/rubiks_cube_gf37.py` |  | 137-map orbits related to Rubik's cube numbers | Residue tagging |
| `math/theorems/rule30_gf37_boundary.py` |  | Reduces Rule 30 record-run values (OEIS A094605) mod 37 to named sets. | Residue computation; proves nothing. |
| `math/theorems/seed_orbit_convergence.py` |  | Values from several domains reduced into {18,24,32} | Residue collection |
| `math/theorems/seed_orbit_dr_chain_458689_gf37.py` | Claim | DR profile and differences of {18,24,32}; 458689 = 37 x 12397. | Computes specific residues and DRs. |
| `math/theorems/seed_window_241_252_gf37.py` |  | DR countdown and residues across integers 241–252. | Tabulates computed properties of a window. |
| `math/theorems/selberg_maass_montgomery_gf37.py` |  | Maps Selberg, Maass, Montgomery constants (1/2, level 4, 3/16, tau(37)) to residues. | Residue lookups of known constants. |
| `math/theorems/seq_146_257_368_gf37.py` |  | Residue, digit and DR labelling of 146, 257, 368 (step 111). | Computation and labelling. |
| `math/theorems/sequence_1111_cycle_1210.py` |  | 1111-series and 1210 cycle sequences; n+DR(n) chains | Computes sequences |
| `math/theorems/sequential_morph_transform.py` | Definition | Defines transform T(S)_i=DR(s_i+i); computes its 9-orbit on base sequence. | Iterates a defined transform and prints data. |
| `math/theorems/sg_exponent_doubling_gf37.py` |  | Perfect-number exponents vs Sophie Germain p=2,3,5; residues of chain tops. | Tabulates specific cases; no general proof. |
| `math/theorems/shell_buckling_gf37.py` | Heuristic | FvK energy minimization of cup/saddle shells by boundary condition | Numerical minimization |
| `math/theorems/sieve_eratosthenes_gf37.py` |  | Sieve of Eratosthenes counts tagged mod 37 | Tabulation of sieve numbers |
| `math/theorems/sine_map_class1_audit.py` | Definition | Sine map taxonomy; computes Lyapunov and bridge statistics. | Numerical computation with class definitions; no asserts. |
| `math/theorems/smith_normal_form_z26.py` | Audit | SNF over Z/nZ kernel verifier; flags claimed Theorem 9 as unverified. | Computational tool; audit of one claim secondary. |
| `math/theorems/sofia_germain_prime_gf37.py` |  | Residue mod 37 of largest known Sophie Germain prime and its safe prime | Computes residues |
| `math/theorems/sophie_germain_perfect_gf37.py` | Proposition | Perfect numbers mod 37 for Mersenne exponents; Sophie Germain triad p=2,3,5. | Computes residues for specific cases. |
| `math/theorems/sovereign_binary_engine.py` | Definition | Two-state classifier of residues 1..36 | Implements classification |
| `math/theorems/sovereign_bridge_30.py` | Claim | Arithmetic facts about 30: sovereign sums, gap 11-13 to 41-43, Euler polynomial. | Computes observations; no general proof. |
| `math/theorems/spectral_embedding_gf37.py` | Audit | Spectrum of Cayley graph Cay(Z37, H u -H); flags source-document errors. | Computes eigenvalues and eigengap; source errors noted. |
| `math/theorems/speed_of_light_gf37.py` |  | c mod 37 = 32 and DR(AU/c) residues computed | Computes residues of constants |
| `math/theorems/sphenic_191919919191_audit.py` |  | Factorization and digit structure of 191919919191 | Tabulation of one number |
| `math/theorems/stacked_zeros_gf37.py` |  | Two zero-counting readings of the 1–9 grid; rows reduced mod 37 | Computes and tabulates readings |
| `math/theorems/steiner_systems_framework.py` |  | Steiner system admissibility and parameter checks for five sections | Computes parameters of known results |
| `math/theorems/t33_node_level_coordinates_gf37.py` | Definition | Per-node (X,Y,Z) layout coordinates via transient of T_33. | Computes coordinate table. |
| `math/theorems/t_phi_zeta_determinant.py` | Audit | Tests whether gamma_MWS appears in spectral observables of T_phi | Numerical search |
| `math/theorems/theorem_100_milestone_gf37.py` |  | 100 mod 37 = 26 reached by five computational paths. | Residue computations; nothing beyond arithmetic. |
| `math/theorems/theorem_103_easter_cycle_gf37.py` |  | Easter computus constants reduced mod 37 | Residue tagging despite THEOREM label |
| `math/theorems/theorem_104_lo_shu_gf37.py` | Claim | Classifies Lo Shu cells, sums and product mod 37. | Residue computation on a fixed square. |
| `math/theorems/theorem_105_platonic_solids_gf37.py` | Proposition | Platonic solid V,E,F counts reduced mod 37 and classified. | Computes residues of known counts. |
| `math/theorems/theorem_107_convergences_gf37.py` |  | Metonic orbit sum, DR chain and twin prime count at seed 246. | Collects computed coincidences at one seed. |
| `math/theorems/theorem_112_five_split_gf37.py` | Claim | Digit sums 1+2+3+4=10 and 6+7+8+9=30 classified mod 37. | Computation of two sums' residues. |
| `math/theorems/theorem_113_dual_focal_triads_gf37.py` | Definition | Focal triads {2,5,8},{3,5,7}; product 6 and its 137-orbit. | Computes arithmetic and residues. |
| `math/theorems/theorem_114_heegner_rabinowitsch_differences_gf37.py` |  | Pairwise differences of Heegner and Rabinowitsch sets classified mod 37 | Enumeration and hit counts |
| `math/theorems/theorem_115_primitive_roots_difference_structure.py` |  | Differences of Heegner/Rabinowitsch numbers that are primitive roots mod 37. | Enumeration of set differences. |
| `math/theorems/theorem_117_discrete_log_base2_gf37.py` | Proposition | Full discrete-log base 2 table mod 37 and 137-map in logs. | Table computation. |
| `math/theorems/theorem_119_rabinowitsch_class_numbers_gf37.py` |  | Class numbers h(1-4q) computed and tagged mod 37 | Computes class numbers; residue tagging |
| `math/theorems/theorem_120_digit_algebra_007_008.py` | Claim | Digits 7,8: DR(15)+1=7; DR(15)=6 lies in orbit of 8. | Computes a specific pair's residues. |
| `math/theorems/theorem_121_scientific_notation_007_008.py` |  | Arithmetic of mantissas 7,8 with shift 3 classified mod 37. | Computes and classifies values. |
| `math/theorems/theorem_123_cayley_dickson_gf37.py` |  | Cayley-Dickson dimensions 2^k mod 37 labelled by class. | Residue table of powers of 2. |
| `math/theorems/theorem_124_ic_string_dimensions.py` | Other | IC orbit {1,10,26} matches string-theory dimensions | Computes orbit; coincidence claim |
| `math/theorems/theorem_125_exceptional_lie_gf37.py` |  | Exceptional Lie algebra dims, ranks, roots mod 37 labelled by sets. | Residue computation and labelling. |
| `math/theorems/theorem_126_jfunction_gf37.py` |  | j-function coefficients and CM values reduced mod 37 | Computes residues of constants |
| `math/theorems/theorem_127_emirp_genesis_gf37.py` |  | Emirp pair 37/73, gematria, residues | Residue tabulation |
| `math/theorems/theorem_128_loeschian_speed_of_light.py` | Formula | Classifies Loeschian norms <=25 mod 37; speed of light mod 37. | Residue classification; r(n)=6*sum chi checked. |
| `math/theorems/theorem_129_digit_rotation_orbit.py` | Proposition | Digit rotations of 246 trace seed orbit forward, mirror orbit reverse. | Computes residues of six permutations. |
| `math/theorems/theorem_132_dlp_algorithms_gf37.py` |  | Brute force, BSGS, Pollard rho, Pohlig-Hellman DLP in GF(37)* | Procedures cross-checked |
| `math/theorems/theorem_136_cycle_sum_1332.py` | Claim | 246+624+462 = 1332 = 36 x 37; residues and factors. | Arithmetic computation on three numbers. |
| `math/theorems/theorem_140_fibonacci_e8_solfeggio_gf37.py` | Audit | Fibonacci/E8/Solfeggio values mod 37; Pisano period 76; table correction | Computes residues |
| `math/theorems/theorem_143_rsa_totient_twin_primes.py` |  | Totient, RSA over F_37, twin prime checks | Computational verification |
| `math/theorems/theorem_146_look_and_say_142241_gf37.py` |  | Look-and-say orbit of 142241 reduced mod 37 | Iterates a procedure and classifies outputs |
| `math/theorems/theorem_147_414_palindrome_gf37.py` |  | Palindrome tower residues mod 37 via positional weights {1,10,26}. | Computes residues of specific nested palindromes. |
| `math/theorems/theorem_151_digit_arrangement_seam_observable.py` |  | Residues of five 4-digit patterns | Tabulation |
| `math/theorems/theorem_153_seed_nqr5_complement_collapse.py` | Proposition | Seed orbit and NQR_5 pair to 37; worked 20,12 example. | Computes sums and residues. |
| `math/theorems/theorem_155_first_primes_ic_collapse.py` |  | 2,3,5,23 concatenation and DR collapse to IC. | Computes facts about specific small primes. |
| `math/theorems/theorem_156_prime_pair_seed_orb_bridge.py` |  | Consecutive primes 7,11,13 pair sums land in {18,24,32} | Observation checked over first 50 primes |
| `math/theorems/theorem_159_layered_pair_sums.py` |  | Layered pair sums of five numbers mod 37 | Tabulation |
| `math/theorems/theorem_160_aba_portal_palindromes.py` | Definition | Enumerates A0A..A9A palindromes with DR and mod-37 sums. | Enumeration; output is data. |
| `math/theorems/theorem_161_atomics_gf37_embedding.py` |  | ATOMICS constants reduced mod 37 and classified. | Computes residues of supplied constants. |
| `math/theorems/theorem_162_atomics_field_equations_gf37.py` |  | Reduces ATOMICS frequency ladder values mod 37 | Computes residues of model outputs |
| `math/theorems/theorem_165_session_numbers_gf37.py` |  | Scans session numbers through residues, DR, primality. | Scan output is data. |
| `math/theorems/theorem_166_goldbach_gf37.py` | Proposition | Goldbach 37-component rule and residue tables | Mostly tabulation; rule is trivial |
| `math/theorems/theorem_168_signed_digits_gf37.py` |  | Maps signed digits +-1..+-9 to GF(37) orbits. | Classification table computation. |
| `math/theorems/theorem_169_7666667_palindrome_chain.py` |  | 7666667 palindrome residue, primality; 0.00048 chain mod 37. | Computes and classifies values. |
| `math/theorems/theorem_171_digit_grid_raabe_gf37.py` |  | Digit grid 000->565->000 residues; Raabe boundary constant placement. | Residue computations on specific grid entries. |
| `math/theorems/theorem_175_riemann_gf37_trinity.py` |  | Digit sums of Riemann zero expansions | Digit tabulation |
| `math/theorems/theorem_176_birthday_biblical_gf37.py` |  | Encodes birthday, biblical dates and names numerically mod 37. | Numeric encoding computations; proves nothing. |
| `math/theorems/theorem_177_123_expansion_algorithm.py` |  | 123 expansion grid and repetition patterns mod 37. | Labelled algorithm; computes residues. |
| `math/theorems/theorem_181_otolith_gf37.py` | Other | Otolith CaCO3 masses reduced mod 37 and labelled. | Residue labelling; nothing proved. |
| `math/theorems/theorem_182_spin_gf37.py` | Other | Decomposes 137 = 3·37+26 into framework components | Arithmetic readings; no proof |
| `math/theorems/theorem_185_data_science_gf37.py` | Other | Regression/statistics terms mapped into 137-map and residues. | Computes values; analogy-level content. |
| `math/theorems/theorem_187_twelve_sequence_sphere_gf37.py` |  | Twelve-sum digit triples and their residues mod 37. | Tabulates specific numbers. |
| `math/theorems/theorem_189_three_zero_kdf_gf37.py` | Definition | Designs a KDF with length 59, target 22, 4x4 matrix, PBKDF2 parameters. | Specifies a procedure; design invariants are residue checks. |
| `math/theorems/theorem_191_lagrange_cf_gf37.py` |  | Periodic continued fractions and Lagrange constants mod 37 | Tabulation |
| `math/theorems/theorem_195_factorial_orbit_gf37.py` |  | n! mod 37 tallied by sector; derangement and partition residues. | Enumeration producing counts. |
| `math/theorems/theorem_199_squaring_generation_gf37.py` | Proposition | Squaring map generation of SA and ST; 6-cycle | Computes squaring dynamics |
| `math/theorems/theorem_204_lucas_sovereign_gf37.py` |  | Lucas and Fibonacci terms landing in named residue sets | Lists computed hits |
| `math/theorems/theorem_205_framework_algebra_gf37.py` | Proposition | Enumerates products within SA u ST u SEED and inverse pairs. | Exhaustive enumeration of pairs. |
| `math/theorems/theorem_207_binomial_sovereign_gf37.py` |  | Binomial coefficients mod 37 in selected rows | Tabulation |
| `math/theorems/theorem_209_sum_qr_structure_gf37.py` | Proposition | Sums of seed, SA, ST sets mod 37 and QR partition. | Computes set sums and Legendre symbols. |
| `math/theorems/theorem_211_permutation_diamond_gf37.py` |  | Permutations of {1,3,7} residues and primality; 11-ladder. | Discovery-engine output on specific numbers. |
| `math/theorems/theorem_215_246_equals_2x123_gf37.py` |  | Coset sums for decompositions of 246 | Residue arithmetic |
| `math/theorems/theorem_218_nuclear_falsification.py` | Conjecture | Maps nuclear observables mod 37 and states falsification criteria | Computes residues and lists predictions |
| `math/theorems/theorem_221_prime_index_137.py` |  | 137 is the 33rd prime; 33 labelled and compared to gamma_5. | Computation and labelling. |
| `math/theorems/theorem_226_cage_integrity_check.py` | Definition | Gate: floor(aggregate) mod 37 ≥ 14 against D7 envelope threshold | Pipeline gate procedure |
| `math/theorems/theorem_227_s_old_d7_crossing.py` | Definition | Defines S_old floor and D7 envelope, solves transcendental crossing numerically. | Numerical root finding; output is data. |
| `math/theorems/theorem_230_six_manifold.py` | Other | Repeated-digit sums equal to 6 and backward doubling pattern | Records arithmetic pattern |
| `math/theorems/theorem_231_236_permutations.py` |  | Arithmetic on splits of permutations of {2,3,6} | Enumeration |
| `math/theorems/theorem_233_rule_30.py` |  | Rule 30 one-step applied to values; results mod 37. | Computes CA steps and residues. |
| `math/theorems/theorem_234_1137_decimal_shift.py` |  | Decimal-shift sequence of 1137 and reversal pairs reduced mod 37 | Computes and tabulates |
| `math/theorems/theorem_235_rule30_open_problems_gf37.py` |  | Rule 30 center-column bit density by GF(37) orbit class of step index. | Measured frequencies over 5000 steps. |
| `math/theorems/theorem_236_rule30_block_universality_gf37.py` |  | Rule 30 center column k-bit block coverage steps and residues | Computes coverage data |
| `math/theorems/theorem_238_rule30_complexity_gf37.py` | Conjecture | Rule 30 center bit naive O(n²) cost, entropy, autocorrelation measured | Measurements; complexity question open |
| `math/theorems/theorem_239_rule30_autocorrelation_gf37.py` |  | Rule 30 center column autocorrelation by orbit class | Statistical computation |
| `math/theorems/theorem_243_rule30_boundary_2adic_unified_gf37.py` |  | Detects periods of Rule 30 left/right boundary columns by depth. | Computational period detection. |
| `math/theorems/theorem_246_n167_cas_ext_prime_gf37.py` | Proposition | Profile of 167: prime, safe prime, residues, 167=137+30 | Numerical profile of one number |
| `math/theorems/theorem_247_n247_mult26_portrait_gf37.py` | Identity | Portrait of n=247; f(x)f^2(x)≡x^2 | Tabulation; identity f(x)·f²(x)≡x² mod 37 |
| `math/theorems/theorem_248_n248_e8_resonance_gf37.py` | Claim | E8 invariants 8, 30, 240, 248 reduced mod 37. | Residue computation of known constants. |
| `math/theorems/theorem_254_elliptic_curves_gf37.py` | Proposition | Counts points on three elliptic curves over F37 | Computed group orders |
| `math/theorems/theorem_255_n255_d7_binary_gf37.py` |  | n=255 residues and Rule 30 image | Tabulation |
| `math/theorems/theorem_257_fermat_prime_f3_gf37.py` |  | 257 as Fermat prime F3: residues, R30 step, orbit tower. | Computes residues and classifications. |
| `math/theorems/theorem_258_rule30_mersenne_gf37.py` | Conjecture | Rule 30 right-edge run records at t=2^k−1, verified to T=4096 | Observed pattern from simulation |
| `math/theorems/theorem_260_n260_ic_casext_square_gf37.py` |  | Factorization and orbit residues of 260 | Computes residues |
| `math/theorems/theorem_261_n261_dark_a_sa_st_a_c9_gf37.py` | Proposition | 261 residues, orbit of 2, SA_ST_A x C9 = DARK_A, Sophie values. | Computation and labelling of one number. |
| `math/theorems/theorem_262_e8_theta_mod37.py` | Proposition | E8 theta coefficients mod 37: zero rates for n≤5000 | Empirical distribution computed |
| `math/theorems/theorem_263_n263_c3_prime_gf37.py` |  | n=263 residues and properties | Tabulation |
| `math/theorems/theorem_265_decimal_antipodal_gf37.py` | Proposition | 1/37 decimal period, IC trinity, antipodal orbit pairing. | Computes decimal and residue facts. |
| `math/theorems/theorem_267_n369_trio_gf37.py` |  | 369 = -1 mod 37 and {3,6,9} products and sums mapped to orbits. | Residue lookups of specific numbers. |
| `math/theorems/theorem_268_cubic_k3_33_gf37.py` | Proposition | Cubic trajectory k^3+33 mod 37 for k=1..5 and orbits | Computes sequence |
| `math/theorems/theorem_270_birthday_march3_gf37.py` | Other | Encodes birthday/astronomical dates as residues mod 37 | Computes residues of dates |
| `math/theorems/theorem_272_easter_dates_gf37.py` |  | Computes Easter dates 2016-2036 and their MMDD residues mod 37. | Computus procedure; output is data. |
| `math/theorems/theorem_273_easter_37year_gf37.py` |  | Easter dates 2016–2052 classified by GF(37) orbits. | Runs computus and tallies. |
| `math/theorems/theorem_277_planck_gf37.py` | Other | Planck constant digit strings reduced mod 37 and labelled. | Residue computation; nothing proved. |
| `math/theorems/theorem_279_twin_antipodal_gate_gf37.py` | Proposition | Twin prime orbit statistics; TESLA/C9 +2 pairs | Mixed counts and small facts |
| `math/theorems/theorem_280_matrix_dimension_gf37.py` | Formula | Alternating {1,2} matrix totals and palindromic block residues mod 37. | Computation; total-sum formula by parity of n. |
| `math/theorems/theorem_281_147_258_369_gf37.py` | Identity | 147,258,369 all ≡ −1 mod 37; grid orbit map. | Computes residues of grid rows. |
| `math/theorems/theorem_294_complete_cross_prime_table.py` | Proposition | Full dump of computed structure for primes 7, 37, 73. | Data table; file class METHOD. |
| `math/theorems/theorem_307_seed_orbit_residue_breakdown_gf37.py` |  | Per-residue breakdown of Riemann zero floors in SEED, first 500 zeros | Counting computation |
| `math/theorems/theorem_323_order4_split_gf37.py` | Proposition | Enumerates Latin squares of order 4: 576, two isotopy classes, transversals. | Enumeration counts; output is data. |
| `math/theorems/theorem_328_splits_percent_repunit_gf37.py` | Proposition | Four readings of the 123/246/369 stack: percentage, splits, prefix residue, 37^2. | Checkable arithmetic readings; forced reasons given. |
| `math/theorems/theorem_336_twin_prime_orbit_alignment_null_gf37.py` | Audit | Pre-registered test: twin primes do not align with 137-orbit structure. | Statistical test against declared baselines; output is null data. |
| `math/theorems/theorem_348_cycle_495_c9_gf37.py` | Proposition | Cycling digits 4,9,5 gives 495,549,954 → C9 orbit. | Computes rotations and residues. |
| `math/theorems/theorem_368_matrix_operator_rh_digits_gf37.py` |  | Verifies rows of T(n)=DS(n)+DS(n-4) = 5 mod 9 and zeta-zero digit structure. | Row-by-row computation. |
| `math/theorems/theorem_369_2468145_sovereign_collapse_gf37.py` | Other | 2,468,145 mod 37 and digit-sum collapse to 30 then DR 3 | Computes residues of one number |
| `math/theorems/theorem_370_gauge_holonomy_gf37.py` |  | Gauge covariance checks and discrete bundle analogy | Numerical verification plus analogy |
| `math/theorems/theorem_373_nuclear_stability_gf37.py` | Definition | Reduces nuclear magic numbers and Z,N values mod 37 into named sets | Computes residues; observations not derivations |
| `math/theorems/theorem_374_rule30_normality_gf37.py` |  | Measures Rule 30 k-block chi-square convergence and GF(37) extremes. | Statistical measurement; normality unproved. |
| `math/theorems/theorem_375_n23456789_pandigital_prime_gf37.py` |  | Prefix residues of 23456789 mod 37 and orbits | Computes residues |
| `math/theorems/theorem_376_n258_negh_gf37.py` |  | 258 factorization, residue 36, orbit and Sophie values labelled. | Computation and labelling. |
| `math/theorems/theorem_377_seam_fibonacci_gf37.py` | Proposition | 259=7·37; Fibonacci mod 37 entry point 19, Pisano 76 | Computes known values |
| `math/theorems/theorem_378_n262_c3_dark_a_square_gf37.py` |  | n=262 residues and DARK_A products | Tabulation |
| `math/theorems/three_tier_phase_engine.py` |  | Three 137-map orbits presented as tier gears; 648/12=54 residue. | Residue lookups on supplied observation. |
| `math/theorems/toroidal_projection.py` | Proposition | Maps sovereign anchors onto torus coordinates; tube-position split | Computes torus positions |
| `math/theorems/triad_33_137_139_audit.py` | Claim | 33 DR-8 numbers to 300, 33rd prime 137, twin 139, residues. | Computes chain of facts; no proof. |
| `math/theorems/triangular_sovereign_structure.py` |  | Repunit triangle sums 369, 123, 492 factor by 41; palindrome DR pairs. | Arithmetic on specific numbers. |
| `math/theorems/triple_grid.py` |  | CLI tool: odd/even digit grid, complements, mirror, gap structure | Tooling procedure |
| `math/theorems/triplet_84_feature_table.py` |  | Feature table of all 84 triplets on 3x3 board | Enumeration |
| `math/theorems/triplet_partition_3x3.py` |  | Enumerates 280 partitions of 1..9 into triples; 14 with named-set sums. | Enumeration; output is data. |
| `math/theorems/twin_gap_dr_chain.py` | Other | DR chain from twin primes 17,19 back to gap 2 | Computes DR steps |
| `math/theorems/twin_prime_dr_convergence.py` |  | Decodes notation for twin pair (17,19): DR chains to 6, then 7. | Computes digit/DR steps. |
| `math/theorems/twin_prime_lattice_patches.py` |  | 3x3 patches of base sequence; column-sum DR signatures and extensions. | Computation of patch data. |
| `math/theorems/ulam_diagonal_b4k2_gf37.py` | Proposition | Counts primes on 4k²+1; residues mod 37 period 37 | Computation output data |
| `math/theorems/ulam_quadratic_k5000_audit.py` | Audit | Ulam diagonal prime counts to k=5000 | Counting search |
| `math/theorems/ulam_tent_map_pf_audit.py` | Audit | Ulam matrix approximations of tent-map transfer operator eigenvalues. | Numerical procedure; output is eigenvalue data. |
| `math/theorems/unified_field_architecture.py` | Other | Unified field architecture: residues of configuration counts, generators, folds. | Computes and narrates connections. |
| `math/theorems/v600_programme.py` | Conjecture | Enumerates 2I, 600-cell, E8 roots; cosmological ratios; pending items. | Verified enumerations; pending parts unproved. |
| `math/theorems/verify_dr9_termination.py` |  | 9x9 cyclic grid row DRs all 9; finite state count 48 | Computational verification of listed checks |
| `math/theorems/verify_local_confluence.py` |  | Exhaustive check of diamond property on 144-state transition system. | Exhaustive search; output a boolean. |
| `math/theorems/wallis_product_gf37.py` |  | Wallis product fractions and partial products reduced mod 37 | Computes residues only |
| `math/theorems/xdiamond_100x100_audit.py` |  | Builds and verifies 100x100 X-diamond matrix | Construction check, no docstring |
| `math/theorems/xx_collapse_matrix.py` |  | Digit sums and 119/911 substring counts in a 1/9 matrix. | Counts and tabulates. |
| `math/theorems/zero_ground_decimal.py` | Other | Zero-ground decimal: 45+81=126 and digit-pair sums. | Computes values from user notation. |

## Heuristic (5)

| File | Secondary | Statement | Evidence |
|---|---|---|---|
| `math/theorems/errata_prevention_protocol.py` | Other | Error-prevention protocol: compute QR/incidence instead of recalling; Legendre oracle | Practical rules to avoid errata, not a proof |
| `math/theorems/mollified_orbit_engine.py` | Algorithm | Snaps noisy data to nearest rotation frame within 0.37 threshold. | Practical smoothing rule, no correctness guarantee. |
| `math/theorems/scaling_sequences_gf37.py` | Algorithm | Extrapolates next terms of two scaling sequences; residues mod 37 | Pattern-guessed next terms not guaranteed |
| `math/theorems/theorem_179_three_geometries_gf37.py` |  | Maps flat/spherical/hyperbolic geometry to SEAM/QR/NQR. | Analogy correspondence, not a proof. |
| `math/theorems/theorem_333_tier_test_base_dependence_gf37.py` | Algorithm | Tier assignment by re-running construction in other bases | Proposed practical test procedure |

## Audit (183)

| File | Secondary | Statement | Evidence |
|---|---|---|---|
| `math/theorems/adelic_valuation_audit.py` | Algorithm | Checks factorizations, valuations, product formula and height for x=3^2*11*19*103/(2^10*5^10). | Main job is verifying a supplied list of claims; no asserts. |
| `math/theorems/adjacent_pair_sum_audit.py` | Algorithm | Checks supplied adjacent-pair-sum cases for 3-digit numbers and corrects two | Verifies user cases; corrects 235→234 and 724→824 |
| `math/theorems/apple_energy_audit.py` |  | Checks apple atom count, kinetic energy chain and vaporization arithmetic against framework claims | Main job is checking supplied physics claims |
| `math/theorems/audit_e8_special_primes_twin_centers.py` | Proposition | Audits 'special primes predict E8 zeros'; shows it is forced by sigma_3 definition. | Checks supplied Datasets 39-45 and gives verdict: forced by definition, not predictive. |
| `math/theorems/audit_leibniz_row37.py` | Proposition | Audits supplied Leibniz triangle row 37 claims; verifies spectrum, corrects carry reasoning | Main job: check/correct supplied Thread 5 analysis |
| `math/theorems/audit_mixture_total_correlation.py` | Identity | Reproduces supplied total-correlation computation for Bernoulli mixture; derives asymptotics | Checks a supplied computation; TC equals KL divergence identity |
| `math/theorems/automorphic_orbit_ntt_audit.py` | Algorithm | Verifies five components: (Z/9)* orbit, CRT cover, 3-6-9 kernel, Mobius, NTT. | Main job is checking a supplied five-part loop structure. |
| `math/theorems/base7_palindrome_22800_audit.py` |  | Checks base-7 palindrome 123321_7=22800; finds 12 is QR, not QNR as claimed. | Main job is correcting a supplied document claim. |
| `math/theorems/base_recurrence_audit.py` | Formula | Checks two recurrences for middle and index sequences as functions of base N | Named audit of supplied base-recurrence claims; no asserts |
| `math/theorems/berry_keating_gue_audit.py` |  | Audits Berry-Keating, GUE, explicit-formula claims; labels each proven/numerical/open | Main job is checking supplied claims' status |
| `math/theorems/block_cayley_spectral_audit.py` | Proposition | Audits spectrum and Fourier block claims for 8x8 coupled-4-cycle adjacency matrix. | Checks supplied spectral claims item by item. |
| `math/theorems/blue_shifted_recursive_mapping_audit.py` | Counterexample | Tests exponential decay claim against W_n data; finds two-segment structure instead | Checks supplied claim f(t)=7e^{-λt}; fails from n=2 |
| `math/theorems/calign_definition_audit.py` | Definition | Audits a C_Align definition that conflates a number, a matrix property and a symbol clash. | Main job is checking a supplied candidate definition. |
| `math/theorems/calign_derivation_audit.py` |  | Tests whether √5−1/13 correction is derivable from existing roles of 13 | Checks a supplied constant's claimed derivation; verdict section |
| `math/theorems/carmichael_dr_audit.py` | Proposition | Verifies DR table of 11 Carmichael numbers and DR multiplicativity. | Checks user's supplied code output table. |
| `math/theorems/carmichael_wheel_tier_audit.py` |  | Tests three claims on Carmichael numbers, W_37 wheel, tier function concentration. | Grades supplied proposition: trivial / confirmed / inconclusive. |
| `math/theorems/cascade_constants_audit.py` |  | Checks first-digit/DR readings of phi, e, pi and products against cascade framework. | Named audit file checking supplied claims; check() calls, no asserts. |
| `math/theorems/cascade_dr_audit.py` |  | Corrects DR table of a 3x3 matrix; finds user DR labels wrong | Checks and corrects supplied labels |
| `math/theorems/chi2_phi3_proof_audit.py` |  | Tests five-step derivation of chi_2(phi^-3) closed form; finds canceling errors | Checks and refutes steps of a supplied proof |
| `math/theorems/chiral_manifold_c4d4_audit.py` |  | Audits C4/D4 chiral manifold assembly claims, polyomino count, stabilizer. | Verifies externally supplied group/geometry claims. |
| `math/theorems/cipher_42128_audit.py` |  | Forensic check of cipher table 42128: digit sums, overrides, lock properties. | Verifies a supplied cipher's claimed steps and flags overrides. |
| `math/theorems/claim_verification_audit.py` |  | Verifies claims from a 2026-05-15 JSON package and fixes three bugs. | Main job is checking and correcting supplied claims. |
| `math/theorems/clifford_fibration_audit.py` | Algorithm | Audits Hopf fibration/Clifford parallelism claims on 600-cell's 120 vertices | Checklist verification of supplied geometric claims |
| `math/theorems/closed_form_audit.py` | Formula | Checks closed form for seven-row matrix with single-cell correction | Verifies supplied matrix closed form |
| `math/theorems/complement_cascade_31_audit.py` | Proposition | Checks complement-cascade digit groups; proves cascade=31 under constraints; corrects user arithmetic | Corrects '2+11=14' and '7+5=13'; verifies supplied chain |
| `math/theorems/conic_lame_audit.py` |  | Audits five-column conic table: discriminant, eccentricity, Lame exponents. | Checks a supplied table's claims. |
| `math/theorems/constellation_mirror_audit.py` | Proposition | Audits mirror constellation claims; proves six-prime constellation covers all three DR tracks | Investigates listed claims; contains DR 3-cycle proof |
| `math/theorems/continued_fraction_3_4_8_audit.py` | Algorithm | Verifies convergents of continued fraction [3;4,8,6,...] | Checks supplied convergent arithmetic |
| `math/theorems/continued_fraction_3_7_11_audit.py` | Counterexample | Recomputes convergents of [3;7,11,...]; claimed 249/82 and sqrt(10) limit wrong. | Checks and refutes supplied convergents and claimed sqrt(10) limit. |
| `math/theorems/continued_fraction_mod37_audit.py` |  | Verifies continued-fraction convergent residues mod 37; corrects n=9 residue 32→22 | Checks and corrects a supplied residue sequence |
| `math/theorems/continued_fractions_audit.py` |  | Audits plastic-constant identities, 19/10101 CF, and a structural claim. | Point-by-point check of supplied claims. |
| `math/theorems/cosmogram_e8_audit.py` |  | Audits cosmogram E8 descent claim 248->7->6 | Checks externally supplied claim |
| `math/theorems/coupled_oscillator_audit.py` | Algorithm | Checks physics and analogy claims about metronome synchronization via simulation. | Main job is checking supplied physical/analogy claims. |
| `math/theorems/crt_emirp_null_model_audit.py` |  | Audits CRT-filtered prime claims; finds null model drawn from S_X collapses variance | Main job is checking supplied statistical claims C1–C6 |
| `math/theorems/cryo_em_hopf_lift_audit.py` |  | Numerically verifies Hopf fibration / SU(2)/SO(3) / Vaisman claims for cryo-EM lift. | Checks a supplied framework claim numerically. |
| `math/theorems/cumsum_correction_audit.py` | Algorithm | Audits cumulative-sum triangle claims: DR period, 314≈100π, correction factor | Checks supplied structural claims |
| `math/theorems/cumsum_triangle_audit.py` | Formula | Audits cumulative-sum triangle from [1,2,3,2,1] and closed-form sums | Checks supplied triangle; derives sum formula |
| `math/theorems/cycle_parity_audit.py` |  | Audits base-9 cycle parity claims about DR classes and twin-pair counts. | Checks five supplied claims. |
| `math/theorems/cyclic142857_audit.py` |  | Verifies claims about 1/7, 142857, 248% and 3844/4375 decimal | Checks a supplied list of claims |
| `math/theorems/d4_600cell_latin_square_audit.py` |  | Arithmetic audit of D4 / 600-cell / Latin square document; flags undefined symbols | Checks a supplied document's claims |
| `math/theorems/data_ledger_audit.py` |  | Audits four Data Ledger claims on doubling circuit and Mersenne backbone | Checks supplied claims |
| `math/theorems/dds_ca_digit_audit.py` | Algorithm | Audits {1,11,111} representation, a cascade chain, and a DDS/CA reinterpretation. | Main job is checking three supplied claims. |
| `math/theorems/decomposition_audit.py` | Proposition | Verifies M = C - Delta decomposition and ranks of a 3x3 matrix. | Checks a stated claim M=C-Delta at all cells. |
| `math/theorems/descent_191_100_audit.py` | Algorithm | Factors and DRs of descent 191..100; checks claims S1–S4 | Checks listed claims about a supplied sequence |
| `math/theorems/diff_interleave_audit.py` | Counterexample | Recomputes difference-interleave sequence; corrects submitted S4 and false convergence claim. | Checks supplied iterations; refutes 'sequence reaches (0,...,0)' via invariants. |
| `math/theorems/digital_root_table_audit.py` | Formula | Determines formula behind n-A-B DR table and checks every entry | Checks supplied table |
| `math/theorems/dim6_kernel_role_audit.py` | Proposition | Checks Fix(phi) in Mat_3(F_2) is maximal subspace where sigma_p=sigma_a | Audits supplied claim; proves parts, flags others |
| `math/theorems/division_582739_937285_audit.py` |  | Audits division 937285/582739: factorizations, residues, decimal DR collapse. | Named audit; check() of supplied numeric claims. |
| `math/theorems/doubling_cycle_loop_audit.py` | Proposition | Checks seven-row mirror-subtraction doubling loop; DR(L−R)=9 for all rows | Verifies supplied matrix; mirror-subtraction fact proved |
| `math/theorems/doubling_cycle_matrix_audit.py` |  | Audits doubling-cycle matrix strings and digit-sum structure | Checks supplied matrix facts |
| `math/theorems/doubling_mirror_audit.py` |  | Doubling-mirror engine: finds row labels off by one between two seedings. | Checks user's code/row citations; reports arithmetic correct, labels off. |
| `math/theorems/dr5_mod37_ap_audit.py` | Proposition | DR=5 residues mod 37 are {5,14,23,32}; checks AP and distribution claims | Verifies supplied DR=5 AP claim and corrects coset remark |
| `math/theorems/dr6_tensor_audit.py` | Proposition | Audits DR-6 family matrices; cross-products collapse since 6^2=0 mod 9. | Checks supplied claims; explains via nilpotency of 6 mod 9. |
| `math/theorems/dr_matrix_9x9_audit.py` | Algorithm | Checks 9x9 DR matrix, Fibonacci/Lucas period-24 DRs, Law of 12, checkerboard. | Section-by-section verification of supplied tables. |
| `math/theorems/dr_matrix_v2_snf_audit.py` |  | SNF audit of F26 matrix V2: rank 7, kernel dim 2, not 5 as claimed | Refutes supplied kernel-dimension claim |
| `math/theorems/e8_cartan_audit.py` | Proposition | Verifies E8 Cartan matrix: Dynkin arms, det=1, eigenvalues from exponents. | Checks a standard object against its known properties. |
| `math/theorems/eisenstein_primes.py` |  | Eisenstein norms: 6+omega has norm 31 not 37; 7+3omega is 37. | Corrects a table typo in supplied material. |
| `math/theorems/embedding_phase_orbit_audit.py` | Definition | Verifies embedding rule, DS law and DR oscillation for S-space grids | Verifies three supplied claims built on definitions |
| `math/theorems/emirp_moduli_comparison_audit.py` | Algorithm | Interprets emirp mod-m chi-square results across moduli 31,37,41,43. | Evaluates a supplied result set against null; no asserts. |
| `math/theorems/eml_branch_cut_audit.py` | Identity | Audits log branch cut and eml(x,y) identity claims | Checks supplied claims; log(z)=eml(1,eml(eml(1,z),1)) |
| `math/theorems/errata_analogy_corrections.py` |  | Records and corrects four analogy claims (Banach-Tarski, Buffon, ord37(10), anchor 4). | Main job is correcting earlier claims. |
| `math/theorems/f26_pillars_jacobian.py` |  | Corrects anchor set (node 3 wrongly included) and checks Jacobian of 137n mod 37 | Corrects supplied v2.5 claim |
| `math/theorems/f37_subgroup_audit.py` | Proposition | Verifies <27> subgroup facts; corrects representative count 16 to 14. | Checks listed claims and corrects one. |
| `math/theorems/f37_subgroup_structure_audit.py` | Proposition | Verifies C3=<10>, C6=<27> subgroups of F_37* and quotient relations | Checks claims in a supplied audit JSON |
| `math/theorems/fib_mod90_audit.py` |  | Checks 120-term Fibonacci mod 90 table and Pisano period 120. | Verifies a supplied table. |
| `math/theorems/fibonacci_dr_chain_audit.py` | Algorithm | Checks arithmetic steps of a Fibonacci-DR-Cunningham-AP chain read from a sketch. | Verifies supplied sketch statements. |
| `math/theorems/fixed_point_sieve_audit.py` |  | Audits Banach fixed-point proof, sieve context, functor claim on N=12 lattice | Checks supplied claims |
| `math/theorems/flanking_palindrome_audit.py` | Algorithm | Checks flanking-digit palindrome constructions over digits {1,5,6}. | Verifies supplied constructions; no asserts. |
| `math/theorems/four_value_signature_audit.py` |  | Audits (144.24,137.33,1.41,14.13) identification; corrects 137.33 as Ba mass. | Checks and corrects supplied identifications. |
| `math/theorems/fractal_grid_parity_audit.py` |  | 9x9 block circulant, prime parity break, parity centrosymmetry; corrects exposition. | Verifies claims and issues a correction. |
| `math/theorems/fraction_1111_12800_audit.py` | Proposition | Checks 0.086796875 = 1111/12800 and its residue -1/2 = 18 mod 37. | Verifies a supplied numeric claim; single values, not a variable identity. |
| `math/theorems/freq_37field_555_2220.py` | Algorithm | Checks frequency ratios mod 37 and flags 10^14 shielding claim as overstated | Corrects supplied physical claim |
| `math/theorems/g4_construction_audit.py` | Proposition | Audits G4=Z_4^2 ⋊ D_4 group axioms, center, commutator, subgroups. | Verifies a supplied construction from first principles. |
| `math/theorems/g4_mackey_fourier_audit.py` | Theorem | Mackey/Fourier decomposition of Z_4^2⋊D_4: unitarity, orbits, spectra, 20 irreps | Verifies a list of supplied claims |
| `math/theorems/g4_stabilizer_geometry_audit.py` | Proposition | Audits G4 stabilizer geometry: D4 stabilizer, orbits, spectrum multiplicities, absent even values. | Addresses four rigour steps for a supplied audit. |
| `math/theorems/g54_character_theory_audit.py` |  | Audits G_54 character-theory code: what is real math vs decoration | Checks supplied source code claims |
| `math/theorems/grid_column_sum_audit.py` | Formula | Six-row grid column sums = 6j+57, DR cycle 9,6,3. | Named audit checking supplied grid; derives column-sum formula. |
| `math/theorems/gue_r3_audit.py` |  | Refutes fabricated GUE R3 table and 3-9-6 level repulsion claim. | Recomputes and refutes supplied table. |
| `math/theorems/gue_riemann_zeros_audit.py` |  | Unfolds Riemann zeros, KS vs GUE; refutes 5-dim Z/26Z kernel premise | Checks and corrects supplied premise; kernel dim is 0 |
| `math/theorems/h4_e8_spectral_audit.py` |  | Audits H4/E8 root norms, Weyl order, and spectral table vs G4 eigenvalues. | Checks claims in supplied code snippet. |
| `math/theorems/harmonic_prime_matrix_audit.py` |  | Audits Harmonic Prime Matrix dashboard claims; corrects '13-Separation' label to 25-step. | Checks supplied dashboard claims. |
| `math/theorems/ib_vib_derivation_audit.py` |  | Audits IB/VIB claims: sufficient statistics, Blahut-Arimoto, VIB bounds | Checks supplied theory block |
| `math/theorems/index13_resonance_audit.py` | Proposition | Tests whether index-13 match between F_37 and ML-KEM is structural; finds coincidence. | Checks a supplied coincidence claim. |
| `math/theorems/jacobi_theta_cascade_audit.py` |  | Audits Jacobi theta identity, cascade classification, random-walk chi-square claims. | Named audit of three supplied image claims. |
| `math/theorems/joy_framework_v25_2_audit.py` |  | Audits JOY FRAMEWORK v25.2 axioms/theorems arithmetic-first, lists errors | Checks supplied document |
| `math/theorems/joy_lob_45_6_correction_audit.py` |  | Audits JOY v25.2 LoB 45.6 table corrections, divisions and zero-count reinterpretation. | Checks a supplied document. |
| `math/theorems/kepler_symplectic_audit.py` | Algorithm | Checks symplectic integrator energy errors and convergence orders for Kepler. | Numerically reproduces supplied claims. |
| `math/theorems/kernel5_construction_audit.py` | Proposition | Kernel-dim-5 {0,13} matrix: rank over Q is 8 not 4; table vs code mismatch | Corrects supplied code comment and table |
| `math/theorems/kernel5_generators_audit.py` | Algorithm | Corrects premise, then computes kernel generators of {0,13} matrix over Z/26Z. | Main job is checking a supplied request's premise and claims. |
| `math/theorems/klein4_z2_orbit_audit.py` | Proposition | Burnside count of Klein-4 on Mat_3(F_2) is 168, correcting 176. | Corrects an exposition's fixed-point count. |
| `math/theorems/korselt_proof_audit.py` | Theorem | Computationally audits each step of Korselt's criterion proof | Main job is checking a supplied proof |
| `math/theorems/kyber_ntt_coset_audit.py` |  | Verifies Kyber NTT parameters; corrects 3328 factorization and zeta-zero indexing. | Checks supplied claims and flags errors. |
| `math/theorems/kyber_ring_mlkem_audit.py` |  | Kyber ring/ML-KEM: coset bug, primitive-root mislabel, noise artifacts | Checks and corrects supplied code/claims |
| `math/theorems/lame_projective_audit.py` |  | Audits Lamé/Fermat curve genus, curvature, symmetry and PGL(3) claims | Checks supplied architecture claims |
| `math/theorems/law_of_12_period_audit.py` |  | dr(12k) period 3 vs dr(3 L_n) period 8; claim 3 fails. | Grades supplied claims PASS/FAIL. |
| `math/theorems/layer24_error_corrections_audit.py` |  | Verifies 9 manifest errors and 3 self-corrections in Layer 24.XX | Checks and corrects supplied claims |
| `math/theorems/layer64_fib_lucas_comparison.py` | Proposition | Fibonacci and Lucas mod 9 both period 24; compares DR sequences; errata | Compares sequences and corrects Grok doc density claim |
| `math/theorems/leveling_ulam_audit.py` | Algorithm | Verifies leveling phenomena and Ulam diagonal prime counts. | Checks supplied list of claims; no asserts. |
| `math/theorems/liouville_parity_audit.py` | Algorithm | Verifies Liouville lambda counts on 1..37: 17 positive, 20 negative. | Checks listed claims by direct computation. |
| `math/theorems/lob_24c_errata.py` |  | Errata record: 3 cells per edge; 5 is non-residue mod 37. | Corrects two falsified claims and checks dependencies. |
| `math/theorems/lob_file_audit_recheck.py` |  | Independent recheck of flagged claims in a file audit summary | Recomputes supplied claims; PASS/FAIL per claim |
| `math/theorems/log2_sqrt5_audit.py` |  | Verifies 10 claims about log2(2+sqrt5) and DR(2+8+2+7). | Claim-by-claim audit. |
| `math/theorems/lsystem_fractal_audit.py` |  | L-system claims: eigenvalues, growth, wrong Hausdorff dimension, collapse() bug | Checks and corrects supplied claims |
| `math/theorems/magic_1_palindrome_audit.py` | Identity | Audits 1B1 palindrome pair sums equal 11(2A+B) | Checks supplied pattern |
| `math/theorems/master_framework_audit.py` |  | Pass/fail audit of 'Complete Master Framework' document claims. | Explicitly audits supplied document. |
| `math/theorems/master_matrix_audit.py` | Algorithm | Digit sums, reversals and DRs of master-matrix number strings | Checks supplied string claims; no asserts |
| `math/theorems/master_record_dr_audit.py` |  | DR fingerprints of Master Record address, nodes, rows, bridges. | Named audit establishing supplied DR values. |
| `math/theorems/matrix_m_mod37_audit.py` |  | Shows 'Matrix M mod 37' is the earlier PROVIDED_M; analyses parity claims. | Checks a resubmitted matrix and accompanying claims. |
| `math/theorems/mc_sensitivity_audit.py` | Counterexample | Shows Monte Carlo sensitivity analyzer claims C1-C3 false | Refutes claims of mc_sensitivity_analyzer.py |
| `math/theorems/medusa_shield_jacobian.py` |  | Removes node 3 from pillar set; checks Jacobian of 137n mod 37 | Corrects a prior version's error |
| `math/theorems/mersenne_dr_audit.py` | Proposition | Tests DR of Mersenne primes determined by p mod 6 | Tests claims D1-D5 with proof of D2 |
| `math/theorems/mod12_collision_audit.py` |  | Audits mod-12 collision and categorical lattice claims | Checks supplied framework claims |
| `math/theorems/mod9_11k_44k_audit.py` | Proposition | Audits when DR(11^k g)=DR(44^k g); confirms conditions, flags period and labels. | Checks supplied claims, flags errors. |
| `math/theorems/modular_data_processor_audit.py` |  | Audits ModularDataProcessor's derived constants; removal test | Checks whether supplied justifications govern output |
| `math/theorems/modular_doubling_37_audit.py` | Proposition | Structure of (g*2^k mod 37) mod 9 | Checks claims M1-M7 about sequence |
| `math/theorems/modular_framework_audit.py` |  | Checks numerically specific claims of 'Modular Arithmetic Properties' document. | Main job is auditing a supplied document. |
| `math/theorems/narcissistic_audit.py` |  | Narcissistic numbers; corrects bound claim at n=60 to n=61. | Corrects supplied bound and description. |
| `math/theorems/node_verification_matrix_audit.py` | Counterexample | Checks DR, parity, QR mod 13 claims for five nodes; no DR-parity correlation. | Checks supplied per-node claims. |
| `math/theorems/numpy_rank_audit.py` | Proposition | Audits NumPy rank-elevation experiment against the Rank Elevation Theorem. | Checks user's code against a theorem. |
| `math/theorems/odlyzko_schonhage_audit.py` |  | Audits log substitution, Riemann-Siegel cutoff, Odlyzko-Schonhage claims | Checks supplied document |
| `math/theorems/palindrome_diamond_audit.py` |  | Audits VIREON matrix, seed extrapolation, repunit diamonds, 'axioms 0-5', polar conic | Checks supplied constructions |
| `math/theorems/palindrome_divisors_ord10_audit.py` | Algorithm | Checks palindromes, divisors of 191919919191, and ord_m(10) table. | Three-section audit of supplied tables. |
| `math/theorems/paper_spectral_audit.py` |  | Arithmetic audit of spectral paper claims | Checks explicit claims in external paper |
| `math/theorems/parabolic_spear_audit.py` | Identity | Verifies properties of P(n)=n(10-n) incl. P(n)=P(10-n), sum 165. | Checks listed claims; P(n)=P(10-n) holds for all n. |
| `math/theorems/pell_10101_audit.py` | Proposition | Pell x^2−10101y^2=1: CF period 6, fundamental unit verified. | Verifies listed claims. |
| `math/theorems/percentage_matrix_node_progression_audit.py` |  | Audits percentage matrix, 10-beat node progression, 13.x sequence. | Named audit file with check() calls. |
| `math/theorems/phenomenological_effective_model_audit.py` |  | Audits factorization and DR claims about 191919919191. | Checks supplied structural claims. |
| `math/theorems/phi_power_operator_precedence_audit.py` |  | Finds operator-precedence bug in submitted phi^3 script; checks others. | Main job checks supplied scripts. |
| `math/theorems/planc_audit.py` | Algorithm | Audits PLANC nanocluster model: hook effect, geometry, entropy, diffusion, epistemic labels. | Checks a supplied paper's claims. |
| `math/theorems/primality_10343_audit.py` |  | Proves 10343 prime by trial division up to 101. | Checks a supplied primality claim. |
| `math/theorems/prime_delta23_audit.py` | Proposition | Audits delta DR(p+23)-DR(p) counts for primes <= 5000. | Checks supplied counts; proves underlying +5/-4 law. |
| `math/theorems/prime_dr_append_layer3_audit.py` | Algorithm | Layer-3 of DR-append n->10n+DR(n) on prime chain | Factorizes and counts primes |
| `math/theorems/prime_gap_dr_audit.py` | Identity | Checks gap→DR transition sequence via DR(p+g)=DR(DR(p)+DR(g)). | Audits a submitted sequence. |
| `math/theorems/prime_insertion_sequence_audit.py` | Algorithm | Digit insertion sequence 167..111: primality, DR, factorizations. | Named audit verifying listed values. |
| `math/theorems/prime_sieve_dr_audit.py` | Proposition | Verifies five sieve/DR results; corrects n=0 case typo in supplied proof | Checks and corrects supplied proof |
| `math/theorems/primes_23_extended_audit.py` | Algorithm | Extends {2,3}-digit prime list, corrects omissions, length-8 enumeration | Cross-check and correction of supplied list |
| `math/theorems/primorial_mirror_audit.py` |  | Audits 'symmetrical folding of twin primes' around 30. | Checks five supplied claims. |
| `math/theorems/pseudoprime_audit.py` |  | Verifies pseudoprime 341, Korselt criterion, Carmichael 561 examples. | Named audit checking known results computationally. |
| `math/theorems/q6_v4_burnside_edge_audit.py` | Counterexample | Burnside count gives \|E(Q6/V4)\| = 48; refutes claimed 56. | Checks disputed claim; names '56' and its wrong fixed-edge count. |
| `math/theorems/q6_v4_spectral_audit.py` | Theorem | Q6/V4 quotient graph spectrum computed; three supplied claims refuted | Verifies and refutes supplied claims |
| `math/theorems/quadratic_classnum_audit.py` |  | Corrects prime counts of E, A, C polynomials; verifies discriminants, class numbers. | Checks document's counts against computation. |
| `math/theorems/ramanujan_modular_audit.py` |  | Audits five Ramanujan modular claims; computes CF of psi. | Point-by-point claim audit. |
| `math/theorems/ramsey_survey_audit.py` |  | Audits corrected Ramsey survey: R values, Schur, VdW, Erdős–Szekeres | Checks a supplied document |
| `math/theorems/ratchet_walk_audit.py` | Formula | Audits ratchet walk on 38-digit string; closed form X=1368+330*sqrt(5). | Checks a supplied walk and computes closed form. |
| `math/theorems/reciprocal_quadrinomial_gfq2_pp.py` | Theorem | Correct PP classification of reciprocal quadrinomial on μ_6⊂GF(25) | Corrects a prior erroneous count |
| `math/theorems/repunit_paired_sequence_audit.py` |  | Audits 24 repunit/reversal paired entries | Checks supplied sequence |
| `math/theorems/rh_reverse_audit.py` |  | Audits claim that a structural prime law proves RH; identifies missing density bound. | Checks logic of a supplied claim. |
| `math/theorems/rossler_attractor_audit.py` |  | Rossler trajectory statistics authentic; framework mapping layer fabricated. | Checks a supplied mapping claim. |
| `math/theorems/sequence_permutation_audit.py` |  | Checks supplied rotation/reversal sequences for mistakes, sections 1-6. | Main job checks supplied sequences. |
| `math/theorems/sphenic_happy_371113.py` | Algorithm | Verifies 371113 = 29 x 67 x 191 is sphenic and happy. | Structural audit of listed properties. |
| `math/theorems/spoke_enumeration_ab_audit.py` |  | Two AB-pair enumerations (14 vs 16) differ by multiplier 27 vs 5. | Reconciles competing enumerations from supplied tables. |
| `math/theorems/structural_semantic_d_audit.py` | Definition | Compares structural vs semantic D(n) for 6-row grid | Checks supplied row-6 anomaly claim |
| `math/theorems/symmetry_correction_audit.py` | Counterexample | Restricts sigma_point=sigma_axial to constant matrices; retracts trace=det; reclassifies 9x9 claim. | Corrects prior claims; circulant [1,2,3] refutes collapse for cyclic grids. |
| `math/theorems/t_phi_spectral_audit.py` |  | Audits T_phi spectral tables, phi^-3 identity, dilogarithm claim; corrects E sector. | Named audit with correction. |
| `math/theorems/theorem_131_zeta_zero_bridge_gf37.py` |  | Grades four zeta-zero bridges: three sound, one broken; GF(37) placement. | Main job is checking supplied bridge claims. |
| `math/theorems/theorem_192_hilbert_polya_delta_critique.py` |  | Critiques proposed delta-function Hilbert-Polya RH construction. | Main job checks a supplied proof attempt. |
| `math/theorems/theorem_249_audit_corrections.py` | Algorithm | Corrects earlier audits: 666, calendar dates, solar transit mod 37. | Main job is correcting earlier audit items. |
| `math/theorems/theorem_259_jc3_falsification.py` |  | Stress-tests announced JC(3) counterexample map: det JF constant, 3-to-1. | Attempts to refute a supplied claim; checks it. |
| `math/theorems/theorem_330_row5_closure_residue_gf37.py` |  | Row 5 residue match graded as post hoc, not established | Grades its own residue match claim |
| `math/theorems/theorem_335_transfer_gate_audit_falsified_gf37.py` |  | Audits T333 transfer gate: row 5 falsified for parameter-free rules | Checks supplied procedure |
| `math/theorems/theorem_340_phi3_seam_interference_gf37.py` | Identity | Checks quantum-interference post; T331 seam is Phi_3 identity. | Main job checks post's algebra and corrects T331. |
| `math/theorems/theorem_347_prime_gap_chi_baselines_gf37.py` |  | Reproduces prime-gap chi analysis; shows two conclusions use wrong null. | Main job checks a supplied analysis. |
| `math/theorems/theorem_349_cubic_map_conjugacy_gf37.py` | Theorem | Confirms supplied conjugacy analysis of x³+33 in full, adds two facts | Main job checks supplied analysis |
| `math/theorems/theorem_353_fa_trajectory_correction_gf37.py` | Counterexample | Corrects f_a orbit of 18: preperiod 5 into 3-cycle | Corrects supplied record f_a(6)=10 not 19 |
| `math/theorems/theorem_360_count_sum_operator_base_generic.py` | Theorem | Audits count-sum operator T_C; shows it is base-generic. | Checks a supplied theorem and re-files its scope. |
| `math/theorems/theorem_380_birthday_253_over_365_vs_ln2.py` | Proposition | Verifies birthday derivation; 253/365≈ln2 gives estimate, not answer. | Checks supplied derivation exactly. |
| `math/theorems/theorem_422_lo_shu_dr9_antidiagonal_cycle_gf37.py` | Theorem | DR-9 family has 72 members; calibration 24=4!; anti-diagonal graph is Hamiltonian. | Audit of supplied run, three corrections. |
| `math/theorems/theorem_423_data_pipeline_correspondence_grade_gf37.py` |  | Grades five data-pipeline correspondence claims by four cuts | Checks supplied mapping |
| `math/theorems/thirtyseven_squared_audit.py` | Identity | Checks 37^2+1 = 10 x 137, sqrt(-1) chain, repunit valuations. | Checks listed properties of 37^2. |
| `math/theorems/todd_coxeter_c2c3_audit.py` | Algorithm | Todd-Coxeter on C2*C3 with H=<ab>: infinite index, exponential coset growth. | Verifies a supplied list of claims. |
| `math/theorems/triangular_partition_audit.py` | Formula | Triangular diagram read as 6 ordered 2-compositions of 5 | Interprets and checks a supplied diagram |
| `math/theorems/trinity_137_matrix_audit.py` |  | Arithmetic audit of five claimed matrix constructions | Checks supplied claims |
| `math/theorems/twin_prime_hl_audit.py` |  | Hardy-Littlewood twin prime count at N=1000; corrects 35.4 | Checks and corrects supplied figures |
| `math/theorems/twin_prime_markov_audit.py` | Algorithm | Tests Markov claims on successive twin-prime DR tracks | Checks claims M1–M3 |
| `math/theorems/twin_prime_tripartite_audit.py` |  | Audits tripartite DR distribution twin prime claims and 1:1:1 density. | Checks supplied document claims. |
| `math/theorems/uniform_grid_audit.py` | Identity | Six uniform arithmetic grids: DR completeness and row/col sums | Checks supplied grid claims |
| `math/theorems/uri_framework_audit.py` |  | Verifies Mersenne recurrence, tiers, grids, 37-field claims | Checks supplied framework |
| `math/theorems/uri_skip_gate_cascade_audit.py` | Algorithm | Checks palindrome/gap structure, symmetric sum and a skip-gate cascade. | Verifies supplied user constructions; no asserts. |
| `math/theorems/v4_orbit_kyber_audit.py` |  | Audits V4 orbit vs Kyber ⟨17⟩ alignment; finds cardinality coincidence | Checks supplied claim |
| `math/theorems/v600_extract_audit.py` |  | Audits V600 programme extract | Checks supplied extract |
| `math/theorems/verify_325_326_327_portable.py` |  | Portable re-derivation of every numeric claim in T325–T327. | Explicitly a check of other theorem files. |
| `math/theorems/xp_weyl_audit.py` |  | Checks semiclassical xp phase-space count vs Riemann-von Mangoldt. | Main job checks supplied claims. |
| `math/theorems/z9z_correspondence_audit.py` |  | Audits Z/9Z correspondence claims: ideal, idempotents, non-split sequence. | Checks supplied document claims. |

## Other (45)

| File | Secondary | Statement | Evidence |
|---|---|---|---|
| `math/theorems/CATEGORY_INDEX.py` | Definition | Index assigning 250 theorem files to named categories. | Tooling/catalogue; no mathematical statement or proof. |
| `math/theorems/alpha_prime_inference_layer.py` | Conjecture | Neural gate using first d primes scaled by 137.036; bug-fixed module. | Labelled hypothesis; ML tooling code, no mathematical result proved. |
| `math/theorems/bio_harmonic_desync.py` | Heuristic | Proposed biological model of neural bandwidth saturation from undefined residue | Self-labelled hypothesis; speculative non-mathematical model |
| `math/theorems/celestial_stages8_10.py` | Algorithm | Maps physical scale stages 8-10 (stellar to cosmological) onto framework numbers. | Asserts arithmetic on scale labels; no mathematical statement proved. |
| `math/theorems/connection_map.py` |  | Cross-reference map linking every theorem in repo via named residues. | Index/connection tooling; its many asserts recheck other files' facts. |
| `math/theorems/cylicamp_master.py` | Definition | Master file collecting DR, repunit, orbit equations and constants with asserts. | Compendium of many independent sections, not one result. |
| `math/theorems/dr_fingerprint_scraper.py` | Algorithm | Generates DR-permutation fingerprints and scans text for copied tags. | Tooling for attribution detection, with source bugs fixed. |
| `math/theorems/gf37_toolkit.py` |  | GF(37) classification toolkit for integers | Tooling library |
| `math/theorems/hopf_stage6_human_scale.py` | Formula | Maps Hopf normal form limit-cycle amplitude sqrt(mu)≈1/φ to a 'human scale' stage | Speculative physical narrative; asserts only arithmetic and Hopf normal-form facts |
| `math/theorems/infinity_proof_roadmap.py` | Conjecture | Evaluates four approaches to twin prime infinitude; identifies missing lower bound. | Survey/roadmap notes; proves nothing, TPC is open. |
| `math/theorems/kinematic_focal_zoom.py` | Algorithm | Renders zoom animation of orbit 2^k mod 333 toward residue 167. | Plotting/video tooling. |
| `math/theorems/layer59_fib_oscillation_mtheory.py` |  | Plotting extension: Fibonacci DR overlay and M-theory subplots. | Plotting code. |
| `math/theorems/lob_596_600.py` | Algorithm | LoB notes on 3900 and 600 residues and DR | Notes of residue computations; no statement proved |
| `math/theorems/master_137.py` | Proposition | Compendium of 137 facts labelled PROVEN/OBSERVED/OPEN. | Collection of notes across layers, not one result. |
| `math/theorems/mws_pure_math_extract.py` | Algorithm | Extracts pure arithmetic content from mws framework file | Extraction/notes file of arithmetic checks |
| `math/theorems/neural_ode_stage5_cells.py` | Algorithm | Narrative Neural ODE stage mapped to residues/Eisenstein norms | Framework narrative; asserts only residues |
| `math/theorems/ocb_quantum_process_gf37.py` |  | Maps OCB process-matrix/quantum switch notions to GF(37) readings | Correspondence notes; no proved statement |
| `math/theorems/orbit_connection_map.py` | Algorithm | Scans theorem files for which GF(37) orbits each touches | Corpus tooling |
| `math/theorems/perceptual_hydrodynamics_v7.py` | Formula | Hyperbolic color space narrative with residue labels | Framework narrative; no proved result |
| `math/theorems/pinn_rt_phase_field.py` |  | Correspondence table between PINN two-phase flow and GF(37) 137-map | Analogy mapping; asserts arithmetic only |
| `math/theorems/quantum_bio_bridge_stage4.py` |  | Plastic-golden 'fusion axiom', THz mapping and Eisenstein norm for stage 4 bio bridge | Speculative physical narrative; asserts arithmetic only |
| `math/theorems/run_all_math_tests.py` |  | Runs every theorem file as subprocess and reports pass/fail. | Test runner tooling. |
| `math/theorems/seed_246_polymath_gap_gf37.py` | Algorithm | Notes 246 as Polymath8b gap bound; factorization and twin-midpoint checks | External cited fact plus arithmetic; nothing proved |
| `math/theorems/selberg_maass_montgomery.py` | Conjecture | Research record on Selberg trace formula, Maass forms, Montgomery; flags unverified claims | Notes with epistemic tags, not a single result |
| `math/theorems/session_log_verified.py` | Audit | Session log of verified arithmetic facts with inline corrections | Log file of assertions |
| `math/theorems/source_mirror_manifold_396.py` | Algorithm | Source-mirror-channel manifold: k-values DR and residues | Framework notes with residue arithmetic |
| `math/theorems/theorem_122_coin_banach_tarski_kakeya.py` | Theorem | Coin paradox, Banach–Tarski, Kakeya presented as one free-group engine | Expository linkage of known theorems |
| `math/theorems/theorem_133_quaternion_rope_gf37.py` | Algorithm | Compares quaternions, RoPE and GF(37) orbit rotation frameworks. | Expository comparison with incidental computation. |
| `math/theorems/theorem_152_x_space_observable_frame.py` | Conjecture | Philosophical notes on exterior frame x, 0 and big bang. | Interpretive notes; no mathematics proved. |
| `math/theorems/theorem_174_ehrhart_connes_bridge.py` | Algorithm | Analogy between Connes rigidity and Ehrhart h*-vector; residues | Analogy/notes, nothing proved |
| `math/theorems/theorem_178_3sat_lyapunov_gf37.py` | Heuristic | Argues 137-map has zero Lyapunov exponent so escapes 3-SAT barrier | Argument; only permutation fact verified, conclusion unsupported |
| `math/theorems/theorem_180_periodic_table_gf37.py` | Algorithm | Maps element numbers of periodic table to GF(37) sets | Narrative labels; no proof |
| `math/theorems/theorem_184_skin_boundary_gf37.py` | Claim | Skin as boundary organ: 26-day renewal, three layers mapped to GF(37). | Interpretive notes on biology, not mathematics. |
| `math/theorems/theorem_186_fractal_uncertainty_gf37.py` |  | Relates fractal uncertainty principle and Cantor set to GF(37) numbers | Expository correspondence notes |
| `math/theorems/theorem_188_consolidated_framework.py` | Algorithm | Session compilation of Tetranacci, Pentanacci, and residue readings | Compilation notes |
| `math/theorems/theorem_194_mtls_ingestion_gf37.py` |  | mTLS ingestion pipeline spec with mod-37 readings of parameters | Software specification notes |
| `math/theorems/theorem_196_applied_framework_gf37.py` |  | Reads residues of document page numbers, dates, parameters | Narrative residue readings |
| `math/theorems/theorem_237_universal_scope_81_149.py` | Algorithm | Scope statement of 22 fields; 81+68=149 residues labelled. | Notes on scope with incidental arithmetic. |
| `math/theorems/theorem_253_gf37_motive_framework.py` | Definition | Correspondence table between motive concepts and GF(37) orbit objects. | Analogy; file labels main part structural alignment, not a proof. |
| `math/theorems/theorem_372_cot_serial_gf37.py` | Algorithm | Analogy between chain-of-thought serialization and 137-map orbits. | Analogy/narrative; no proved mathematical statement. |
| `math/theorems/thread_session_connections.py` | Algorithm | Asserts cross-links between pieces built in one session. | Connection ledger; tooling. |
| `math/theorems/torus_animation_137map.py` | Algorithm | Torus animation of three 137-map orbits | Plotting/animation tooling |
| `math/theorems/vireon_stage7_planetary.py` |  | Narrative VIREON planetary stage with residue labels | Framework narrative |
| `math/theorems/visualize_gf37.py` |  | Plots Eisenstein lattice, Loeschian norm distribution and random walk. | Plotting tool. |
| `math/theorems/zero_space_stages1_3.py` |  | Planck-to-atomic stage narrative with Eisenstein norm and mod-37 filter | Speculative physical narrative; asserts arithmetic only |
