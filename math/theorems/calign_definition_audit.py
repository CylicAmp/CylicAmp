# math/theorems/calign_definition_audit.py
"""
C_Align Definition Audit
========================
The candidate definition conflates three separate things:

  (1) C_Align as a NUMBER: 2φ−1−1/13 ≈ 2.1591449
      — established in parabolic_spear_audit.py

  (2) C_Align as a MATRIX PROPERTY: orbit under ⟨ρ,σ_p,σ_a⟩ inside
      Fix(φ) ∩ (Law-of-12 filter)
      — a predicate on matrices, different kind of object from (1)

  (3) "ρ" naming conflict: ρ = plastic number (1.3247) elsewhere in
      this codebase; reusing ρ for the cyclic row-shift is ambiguous.

This file:
  A. Checks P(n) DR values against the Law-of-12 filter
  B. Identifies the space conflict (binary vs integer)
  C. Computes the group G = ⟨row_cycle, σ_p, σ_a⟩ on Mat_3(F_2)
  D. Computes Fix(φ) ∩ (mod-3 survivor set) in the integer DR context
  E. Reports what the number 2φ−1−1/13 connects to, if anything
"""

import math
from itertools import product as iproduct


# ── helpers ───────────────────────────────────────────────────────────────────

def dr(n: int) -> int:
    return 0 if n == 0 else 1 + (n - 1) % 9


PHI = (1 + math.sqrt(5)) / 2


def sigma_p(M):
    n = len(M)
    return [[M[n-1-i][n-1-j] for j in range(n)] for i in range(n)]


def sigma_a(M):
    n = len(M)
    return [[M[i][n-1-j] for j in range(n)] for i in range(n)]


def row_cycle(M):
    """ρ_row: cyclic row-shift M[i][j] → M[(i+1)%3][j], order 3."""
    n = len(M)
    return [[M[(i + 1) % n][j] for j in range(n)] for i in range(n)]


def mat_key(M):
    return tuple(tuple(r) for r in M)


def all_3x3_f2():
    for bits in range(512):
        yield [[(bits >> (3*i + j)) & 1 for j in range(3)] for i in range(3)]


def apply_seq(M, ops):
    for op in ops:
        M = op(M)
    return M


# ── A. P(n) DR values vs Law-of-12 filter ────────────────────────────────────

def verify():
    print("C_Align Definition Audit\n")

    print("=" * 60)
    print("A. P(n) = n(10-n) DR values vs Law-of-12 filter {3,6,9}")
    print("=" * 60)

    P = [n * (10 - n) for n in range(11)]
    P_drs = [dr(v) if v > 0 else 0 for v in P]
    law12_set = {3, 6, 9}

    print(f"\n  n:    {list(range(11))}")
    print(f"  P(n): {P}")
    print(f"  DR:   {P_drs}")
    print()

    fails = [(n, P[n], P_drs[n]) for n in range(11)
             if P_drs[n] not in law12_set and P_drs[n] != 0]
    passes = [(n, P[n], P_drs[n]) for n in range(11)
              if P_drs[n] in law12_set]

    print(f"  DR ∈ {{3,6,9}}:  positions {[t[0] for t in passes]}")
    print(f"                  values    {[t[1] for t in passes]}")
    print(f"  DR ∉ {{3,6,9}}:  positions {[t[0] for t in fails]}")
    print(f"                  values    {[t[1] for t in fails]}")
    print()

    # P(2)=16 DR=7, P(5)=25 DR=7, P(8)=16 DR=7 — three failures
    assert len(fails) == 3
    assert all(t[2] == 7 for t in fails)
    print(f"  RESULT: P(n) does NOT satisfy Law-of-12 filter.")
    print(f"  3 positions with DR=7: n = {[t[0] for t in fails]}")
    print(f"  P(2)=P(8)=16 (DR=7), P(5)=25 (DR=7).")
    print(f"  The candidate definition's claim that P(n) matches the")
    print(f"  Law-of-12 filter is FALSE.")

    # ── B. Space conflict ─────────────────────────────────────────────────────
    print()
    print("=" * 60)
    print("B. Space conflict")
    print("=" * 60)
    print("""
  Fix(φ) is a subspace of Mat_3(F_2): entries are 0 or 1.
  DR(0) = 0,  DR(1) = 1.  Neither is in {3,6,9}.

  Therefore the Law-of-12 filter (DR ∈ {3,6,9}) applied to elements
  of Mat_3(F_2) is EMPTY — no binary matrix satisfies it entry-wise.

  The candidate definition combines:
    Fix(φ) ⊂ Mat_3(F_2)  [binary space]
    Law-of-12 filter      [integer DR condition]
  These two conditions cannot simultaneously constrain the same object
  without specifying an embedding from F_2 into Z.
    """)

    # ── C. Group G = ⟨row_cycle, σ_p, σ_a⟩ on Mat_3(F_2) ──────────────────
    print("=" * 60)
    print("C. Group G = ⟨row_cycle, σ_p, σ_a⟩ on Mat_3(F_2)")
    print("=" * 60)

    generators = [row_cycle, sigma_p, sigma_a]

    # Build group by closure: collect all distinct transformations
    # Represent each as a permutation of {0..511}
    all_mats = list(all_3x3_f2())
    mat_to_idx = {mat_key(M): i for i, M in enumerate(all_mats)}

    def perm_of(op):
        return [mat_to_idx[mat_key(op(M))] for M in all_mats]

    identity_perm = list(range(512))
    group_perms = {tuple(identity_perm)}
    frontier = [perm_of(g) for g in generators]
    for p in frontier:
        group_perms.add(tuple(p))

    def compose(p, q):
        return tuple(p[q[i]] for i in range(512))

    changed = True
    while changed:
        changed = False
        new_elements = set()
        for p in list(group_perms):
            for g in [perm_of(g) for g in generators]:
                c = compose(p, tuple(g))
                if c not in group_perms:
                    new_elements.add(c)
                    changed = True
        group_perms |= new_elements

    group_order = len(group_perms)
    print(f"\n  |G| = |⟨row_cycle, σ_p, σ_a⟩| = {group_order}")

    # Klein four-group K = ⟨σ_p, σ_a⟩ has order 4
    K_perms = {tuple(identity_perm)}
    for g in [sigma_p, sigma_a]:
        K_perms.add(tuple(perm_of(g)))
    changed = True
    while changed:
        changed = False
        for p in list(K_perms):
            for g in [perm_of(sigma_p), perm_of(sigma_a)]:
                c = compose(p, tuple(g))
                if c not in K_perms:
                    K_perms.add(c)
                    changed = True
    assert len(K_perms) == 4
    print(f"  |K| = |⟨σ_p, σ_a⟩| = {len(K_perms)}  (Klein four-group, as expected)  ✓")

    # row_cycle has order 3; K has order 4; gcd(3,4)=1 → |G| divides 12
    assert group_order == 12
    print(f"  order(row_cycle) = 3, |K| = 4, gcd(3,4) = 1 → |G| = 12  ✓")
    print(f"  G ≅ Z_3 ⋊ K ≅ A_4  (alternating group on 4 elements, order 12)")

    # Orbits under G on Mat_3(F_2)
    seen = set()
    orbits_G = 0
    for M in all_mats:
        k = mat_key(M)
        if k not in seen:
            orbits_G += 1
            # compute orbit
            orbit_frontier = [M]
            orbit_set = {k}
            while orbit_frontier:
                cur = orbit_frontier.pop()
                for g in generators:
                    img = g(cur)
                    ik = mat_key(img)
                    if ik not in orbit_set:
                        orbit_set.add(ik)
                        orbit_frontier.append(img)
                    # also apply inverses / compositions via closure
                    for g2 in generators:
                        img2 = g2(img)
                        ik2 = mat_key(img2)
                        if ik2 not in orbit_set:
                            orbit_set.add(ik2)
                            orbit_frontier.append(img2)
            seen |= orbit_set
    print(f"  Orbits of G on Mat_3(F_2): {orbits_G}  (out of 512 matrices)")

    # Fix(φ) under G: which collapse matrices are G-stable?
    phi_collapse = [M for M in all_mats if sigma_p(M) == sigma_a(M)]
    assert len(phi_collapse) == 64
    G_stable_collapse = [M for M in phi_collapse
                         if all(mat_key(g(M)) in {mat_key(X) for X in phi_collapse}
                                for g in generators)]
    print(f"  Fix(φ) matrices stable under all G generators: {len(G_stable_collapse)} / 64")

    # ── D. C_Align number: what it actually connects to ───────────────────────
    print()
    print("=" * 60)
    print("D. The number 2φ−1−1/13 — what it connects to")
    print("=" * 60)

    C_align = 2 * PHI - 1 - 1/13
    sqrt5 = math.sqrt(5)

    print(f"\n  C_Align = 2φ−1−1/13 = {C_align:.10f}")
    print(f"  2φ−1    = √5        = {sqrt5:.10f}  (exact: 2φ−1 = √5)")
    print(f"  So C_Align = √5 − 1/13")

    assert abs(2*PHI - 1 - sqrt5) < 1e-12
    assert abs(C_align - (sqrt5 - 1/13)) < 1e-12
    print(f"  C_Align = √5 − 1/13  ✓  (exact closed form)")

    # 1/13 connection: 13 is one of the 7 prime factors of 191919919191
    # 191919919191 = 3×7×11×13×37×167×10343
    assert 191919919191 % 13 == 0
    print(f"  1/13: 13 | 191919919191  ✓  (13 is a sphenic factor)")
    print(f"  No demonstrated connection between √5−1/13 and the")
    print(f"  proposed group action or Fix(φ).")

    # Does C_Align appear as an eigenvalue, trace, or orbit ratio? No obvious link.
    print()

    # ── E. Summary ────────────────────────────────────────────────────────────
    print("=" * 60)
    print("E. Verdict on candidate definition")
    print("=" * 60)
    print(f"""
  ISSUES:
  1. Type mismatch: C_Align = 2φ−1−1/13 is a number (≈{C_align:.4f}).
     The candidate definition defines a PREDICATE on matrices.
     These are different objects; one definition cannot serve both.

  2. P(n) fails the Law-of-12 filter:
     DR(P(2)) = DR(16) = 7,  DR(P(5)) = DR(25) = 7,  DR(P(8)) = 7.
     The claim "matches P(n)" is false.

  3. Space conflict: Fix(φ) ⊂ Mat_3(F_2); Law-of-12 requires integers.
     No binary matrix has DR ∈ {{3,6,9}} entry-wise.

  4. ρ naming conflict: ρ = plastic number (1.3247) is already defined.
     The cyclic row-shift should be written ρ_row or σ_row.

  WHAT IS VERIFIED:
  — G = ⟨row_cycle, σ_p, σ_a⟩ has order {group_order}, acts on Mat_3(F_2)  ✓
  — C_Align = √5 − 1/13  (exact closed form)  ✓
  — G-stable elements of Fix(φ): {len(G_stable_collapse)} out of 64  ✓

  RECOMMENDATION:
  Keep the numerical constant as:
    C_Align = √5 − 1/13  ≈ {C_align:.7f}
  Do not use "C_Align" for the matrix predicate — name it separately,
  e.g. "G-alignment condition" or "collapse-stable set", and state it
  in the integer sovereign DR context, not the binary F_2 context.
    """)

    print("All assertions passed.")


if __name__ == "__main__":
    verify()
