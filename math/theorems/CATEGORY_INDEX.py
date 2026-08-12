"""
Mathematical Category Index — CylicAmp Framework

Categories used in this framework:
  Axiom       — accepted without proof, foundational
  Postulate   — assumed truth specific to this system
  Definition  — establishes precise meaning of a term
  Theorem     — proven from axioms and definitions
  Lemma       — helper result supporting a larger theorem
  Corollary   — follows directly from a theorem
  Conjecture  — believed true, not yet proven
  Proposition — proven, smaller scope than theorem
  Algorithm   — step-by-step procedure
  Law         — universal rule, no exceptions
  Observation — noticed pattern, not yet formalized
  Formula     — equation expressing a relationship
  Identity    — equation true for all variable values
  Principle   — foundational governing rule

INDEX (250 files)
"""

CATEGORIES = {
    "Algorithm": [
        "abbc_manifold_grid",
        "ahl_17_grid_structure",
        "alpha_grid_growth_pattern_connection",
        "errata_prevention_protocol",
        "fps37_scanner",
        "growth_pattern_full_333",
        "kimi_session_protocol",
        "lob_25_legendre_applications",
        "lob_26_collatz_f37",
        "lob_591_592_595",
        "meta_algorithm_gf37",
        "pattern_1234_5_1234_gf37",
        "pie_sieve_gf37",
        "scaling_sequences_gf37",
        "sieve_eratosthenes_gf37",
    ],
    "Conjecture": [
        "goldbach_proof_attempt_gf37",
        "twin_prime_gf37",
        "twin_prime_structure",
    ],
    "Definition": [
        "formal_definitions_gf37",
        "nk_naturals_with_presence",
        "two_group_split",
    ],
    "Identity": [
        "basin_sum_wraparound_gf37",
        "concatenation_123_repunit",
        "repunit_sq_euler_phi_gf37",
        "triple_coupling_666_gf37",
    ],
    "Law": [
        "dr_algebra",
        "theorem_138_dr_law_orbit_multiplication",
        "wallis_product_gf37",
    ],
    "Observation": [
        "cipher_123_1234",
        "connection_map",
        "digit_circle_5_center",
        "digit_rotation_patterns",
        "dr_chain_52_25_41",
        "dr_grid_orbit",
        "eleven_thirtyseven_ops",
        "errata_analogy_corrections",
        "fibonacci_grid_four_readings",
        "gamma_22_inverse_seed_gf37",
        "goldbach_gf37",
        "mersenne_seam_kervaire_gf37",
        "palindrome_gf37",
        "prime_quartet_chains_palindromes",
        "repdigit_self_similarity_gf37",
        "root_grid_dr6_dr7",
        "seed_window_241_252_gf37",
        "sliding_window_9cycle_gf37",
        "theorem_175_riemann_gf37_trinity",
        "triplet_partition_3x3",
    ],
    "Principle": [
        "errata_prevention_protocol",
    ],
}

COUNTS = {cat: len(files) for cat, files in CATEGORIES.items()}
COUNTS["Theorem"] = 201  # remainder

if __name__ == "__main__":
    print("CylicAmp — Mathematical Category Index")
    print("=" * 45)
    total = 0
    for cat in sorted(COUNTS):
        n = COUNTS[cat]
        total += n
        print(f"  {cat:<14} {n:>4}")
    print(f"  {'TOTAL':<14} {total:>4}")
