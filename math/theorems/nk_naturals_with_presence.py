"""
Nκ — Naturals with Presence

LABEL
=====
Nκ  (spoken: "N-kappa")

Label established: Nκ.

DEFINITION
===========
N  = standard natural numbers. No provenance. Each element carries no record
     of how it was produced.

Nκ = naturals with presence. Each element n_i carries κ: its genealogy,
     its subscript history, its origin chain.

     N ⊂ Nκ  but  Nκ ⊄ N

Every ordinary natural embeds into Nκ with trivial κ (no history).
Elements of Nκ with nontrivial genealogy have no image in N.

PROPERTIES
===========
- N is the math of exchange. Provenance is erased at each step.
- Nκ is the math of existence. Provenance is carried forward.
- ds(13) = 4: in N, 13 and 4 are unrelated. In Nκ, 4 is in the genealogy
  of 13 — digit sum is a form of κ-recovery.

CONNECTION TO GF(37)
=====================
- The SEAM (elements ≡ 0 mod 37) is where N collapses provenance.
  Nκ preserves it: 37₁, 74₂, and 111₃ remain distinct even though
  all map to 0 mod 37.
- The 7-bag Tetris randomizer ≅ Nκ: each piece carries its bag-position
  genealogy. Classic RNG Tetris ≅ N: no memory, no provenance.
- The orbit structure of GF(37) is a partial Nκ: orbit membership
  (e.g. 7 ∈ D7) survives the 137-map, but the path taken to reach
  an element does not.
"""

LABEL = "Nκ"
DESCRIPTION = "Naturals with presence — each element carries its genealogy (κ)"
