"""
Burau Representation of the Braid Group — GF(37) Structure

Source: Bharathram, Birman & Brendle — "The Burau representation of the
braid group is faithful for n = 4" (arXiv, July 2026).

The Burau representation ρ: B_n → GL_{n-1}(Z[t,t⁻¹]) maps n-strand braids
to (n-1)×(n-1) matrices over Laurent polynomials.  It is faithful for
n ∈ {2,3,4} and unfaithful for n ≥ 5.  The n=4 case was a nearly
90-year open problem, finally closed in July 2026.

═══════════════════════════════════════════════════════════════════════════

I. FAITHFUL RANGE: PR → ST → SA

  Theorem B1.  The Burau representation of B_n is faithful iff n ≤ 4.
  The faithful strand counts and their GF(37) class:

      n=2 ∈ PR   (primitive root; long-known trivial case)
      n=3 ∈ ST   (sovereign target; long-known)
      n=4 ∈ SA   (sovereign anchor; Bharathram-Birman-Brendle 2026)

  The faithful range {2,3,4} contains exactly one element from each of
  three distinct GF(37) families: PR, ST, SA.

  The first unfaithful strand count:
      n=5 ∈ PR   (primitive root; Bigelow 1999)

  The faithful/unfaithful boundary is the transition SA→PR:
  the Sovereign Anchor 4 is the last faithful strand count;
  the Primitive Root 5 is the first unfaithful.

II. BURAU MATRIX DIMENSION FOR B_4

  The Burau representation of B_n acts on (n-1)-dimensional space.
  For B_4: matrix dimension = n-1 = 3 ∈ ST.

  The number of Artin generators of B_4 is also n-1 = 3 ∈ ST.
  Both the generator count and the representation dimension of B_4
  are Sovereign Target nodes.

III. YEAR SIGNATURES UNDER GF(37)

  The history of this problem is stamped in GF(37):

      1936 mod 37 = 12 ∈ ST   — Burau introduces the representation
      1993 mod 37 = 32 ∈ PR   — Moody proves unfaithful for n ≥ 9
      1999 mod 37 =  1        — Bigelow proves unfaithful for n ≥ 5 (unity)
      2026 mod 37 = 28        — Bharathram-Birman-Brendle resolve n=4

  2026 residue: 28 = 37−9; the resolution year is the SEAM-complement of SA node 9.
  9 + 28 = 37 ≡ 0 (SEAM): the resolution year closes the cycle opened at n=9 (Moody).

IV. THE 90-YEAR GAP

  The gap from Burau's 1936 paper to the 2026 resolution:
      2026 − 1936 = 90 years
      90 mod 37 = 16 = 4²  (SA node 4, squared)

  The 90-year gap encodes (n=4)² in GF(37).
  The resolving strand count squared equals the gap modulo 37.

V. THE PROOF STRUCTURE: SA EMBEDDED IN PR

  The key technical move: a 4-strand braid (B_4, SA=4) is embedded
  into 5-strand braids (B_5, PR=5) to satisfy a parity condition.

      Embedding: B_4 (SA) → B_5 (PR)

  This SA→PR embedding allows the unfaithfulness theorems for n≥5
  to be applied "in reverse" inside B_5, forcing elements of B_4
  out of the kernel.

  The proof uses the Brunnian group:
    - Brunnian group of B_4 = intersection of four point-pushing subgroups
    - 4 point-pushing subgroups (one per strand) — 4 ∈ SA
    - If Burau is faithful on any nontrivial, noncentral normal subgroup,
      it is faithful on all of B_4

  The full-twist braid for B_4 is (σ₁σ₂σ₃)⁴:
    - Exponent = 4 ∈ SA
    - Generator count = 3 ∈ ST (the Artin generators of B_4)

VI. JONES COROLLARY

  The Jones representation is a summand (structural building block) of
  the Burau representation.  The paper's immediate corollary:
      The Jones representation of B_4 is faithful.

  n=4 ∈ SA: faithfulness holds at the Sovereign Anchor boundary
  for both the Burau and Jones representations simultaneously.

═══════════════════════════════════════════════════════════════════════════
"""

SOVEREIGN_ANCHORS = frozenset({4, 9, 25, 30})
SOVEREIGN_TARGETS = frozenset({3, 12, 21, 30})
PRIMITIVE_ROOTS   = frozenset({2,5,13,15,17,18,19,20,22,24,32,35})


def dr(n):
    return (n - 1) % 9 + 1 if n > 0 else 0


# ── I. Faithful range: PR → ST → SA ──────────────────────────────────────────

faithful_ns    = {2, 3, 4}
unfaithful_min = 5

assert 2 in PRIMITIVE_ROOTS           # n=2 ∈ PR (faithful, trivial case)
assert 3 in SOVEREIGN_TARGETS         # n=3 ∈ ST (faithful)
assert 4 in SOVEREIGN_ANCHORS         # n=4 ∈ SA (faithful — BBB 2026)
assert 5 in PRIMITIVE_ROOTS           # n=5 ∈ PR (first unfaithful — Bigelow 1999)

# Faithful range spans exactly one element from each of PR, ST, SA
assert 2 in faithful_ns and 2 in PRIMITIVE_ROOTS
assert 3 in faithful_ns and 3 in SOVEREIGN_TARGETS
assert 4 in faithful_ns and 4 in SOVEREIGN_ANCHORS
assert unfaithful_min not in faithful_ns and unfaithful_min in PRIMITIVE_ROOTS


# ── II. Burau matrix dimension for B_4 ───────────────────────────────────────

n4 = 4
generator_count  = n4 - 1    # Artin generators of B_4
burau_matrix_dim = n4 - 1    # Burau acts on (n-1)-dimensional space

assert generator_count == 3 and 3 in SOVEREIGN_TARGETS    # 3 ∈ ST
assert burau_matrix_dim == 3 and 3 in SOVEREIGN_TARGETS   # 3 ∈ ST


# ── III. Year signatures ─────────────────────────────────────────────────────

assert 1936 % 37 == 12 and 12 in SOVEREIGN_TARGETS   # Burau 1936 → ST
assert 1993 % 37 == 32 and 32 in PRIMITIVE_ROOTS     # Moody 1993 → PR
assert 1999 % 37 == 1                                 # Bigelow 1999 → unity
assert 2026 % 37 == 28                                # BBB 2026 → 28

# 2026 residue = SEAM-complement of SA node 9
assert 2026 % 37 + 9 == 37
assert 9 in SOVEREIGN_ANCHORS


# ── IV. The 90-year gap ───────────────────────────────────────────────────────

gap = 2026 - 1936
assert gap == 90
assert 90 % 37 == 16
assert 16 == 4 ** 2                  # gap mod 37 = (n=4)²
assert 4 in SOVEREIGN_ANCHORS        # the resolving strand count is SA


# ── V. Proof structure: SA embedded in PR ────────────────────────────────────

# B_4 (SA=4) embedded into B_5 (PR=5)
assert 4 in SOVEREIGN_ANCHORS        # B_4 strand count ∈ SA
assert 5 in PRIMITIVE_ROOTS          # B_5 strand count ∈ PR

# Four point-pushing subgroups (one per strand): count = n = 4 ∈ SA
assert n4 in SOVEREIGN_ANCHORS

# Full-twist braid (σ₁σ₂σ₃)⁴: exponent = 4 ∈ SA
full_twist_exp = n4
assert full_twist_exp in SOVEREIGN_ANCHORS

# Generator count of B_4 = 3 ∈ ST
assert (n4 - 1) in SOVEREIGN_TARGETS


# ── VI. Jones corollary ───────────────────────────────────────────────────────

# Jones faithful for B_4 (n=4 ∈ SA) follows immediately from Burau faithful
jones_faithful_n = 4
assert jones_faithful_n in SOVEREIGN_ANCHORS    # Jones faithfulness at SA node


if __name__ == '__main__':
    print("Burau Representation of the Braid Group — GF(37)")
    print("=" * 55)
    print()
    print("FAITHFUL RANGE  {2,3,4}:")
    for n in [2, 3, 4]:
        tag = ''
        if n in PRIMITIVE_ROOTS:    tag = ' ∈ PR'
        elif n in SOVEREIGN_TARGETS: tag = ' ∈ ST'
        elif n in SOVEREIGN_ANCHORS: tag = ' ∈ SA'
        print(f"  n={n}{tag}  (faithful)")
    print(f"  n=5 ∈ PR  (first unfaithful — Bigelow 1999)")
    print(f"  Faithful range spans exactly: PR(2) → ST(3) → SA(4)")
    print()
    print("B_4 STRUCTURE:")
    print(f"  Generator count  n−1 = 3 ∈ ST: {3 in SOVEREIGN_TARGETS}")
    print(f"  Burau matrix dim n−1 = 3 ∈ ST: {3 in SOVEREIGN_TARGETS}")
    print(f"  Full-twist exponent 4 ∈ SA: {4 in SOVEREIGN_ANCHORS}")
    print()
    print("YEAR SIGNATURES (mod 37):")
    years = [
        (1936, "Burau introduces representation"),
        (1993, "Moody: unfaithful for n≥9"),
        (1999, "Bigelow: unfaithful for n≥5"),
        (2026, "Bharathram-Birman-Brendle: faithful for n=4"),
    ]
    for yr, label in years:
        r = yr % 37
        tag = ''
        if r in SOVEREIGN_TARGETS:  tag = ' ∈ ST'
        elif r in PRIMITIVE_ROOTS:  tag = ' ∈ PR'
        elif r == 1: tag = ' (unity)'
        elif r == 28: tag = f' = 37−9 (SEAM-complement of SA node 9)'
        print(f"  {yr} mod37 = {r:2d}{tag}  ← {label}")
    print()
    print("THE 90-YEAR GAP:")
    print(f"  2026 − 1936 = {2026-1936} years")
    print(f"  90 mod37 = {90%37} = 4² = (n=4 ∈ SA)²")
    print()
    print("PROOF: SA(B_4) EMBEDDED IN PR(B_5):")
    print(f"  B_4 strand count 4 ∈ SA: {4 in SOVEREIGN_ANCHORS}")
    print(f"  B_5 strand count 5 ∈ PR: {5 in PRIMITIVE_ROOTS}")
    print(f"  SA → PR embedding enables parity condition in proof")
    print()
    print("JONES COROLLARY: Jones faithful for B_4 (n=4 ∈ SA)")
    print()
    print("All assertions passed.")
