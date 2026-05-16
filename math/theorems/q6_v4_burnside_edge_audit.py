# math/theorems/q6_v4_burnside_edge_audit.py
"""
Q6 / V4 Edge Count: Burnside Lemma Audit
==========================================
Disputed claim resolved: |E(Q6 / V4)| = 48, NOT 56.

The "56" claim arose from a wrong fixed-edge count of 32 for the reversal
element β. This audit proves that count is zero by two independent methods:

  (A) Direct enumeration: no edge in Q6 is fixed by any non-identity element.
  (B) Algebraic proof: hamming(u, rev(u)) is always even for any u ∈ {0,1}^6;
      therefore no u and rev(u) can be adjacent (differ in exactly 1 bit).

Burnside result:  (192 + 0 + 0 + 0) / 4 = 48.
"""

from itertools import product


# ── group action ─────────────────────────────────────────────────────────────

def identity(v): return v
def alpha(v):    return tuple(1 - x for x in v)      # complement
def beta(v):     return v[::-1]                        # reversal
def gamma(v):    return beta(alpha(v))                 # complement ∘ reverse


def apply_to_edge(g, edge):
    u, v = edge
    return tuple(sorted([g(u), g(v)]))


# ── hypercube construction ────────────────────────────────────────────────────

def build_q6():
    V = list(product([0, 1], repeat=6))
    E = set()
    for v in V:
        for i in range(6):
            w = list(v)
            w[i] ^= 1
            E.add(tuple(sorted([v, tuple(w)])))
    return V, list(E)


# ── algebraic lemmas ──────────────────────────────────────────────────────────

def hamming(u, v):
    return sum(a != b for a, b in zip(u, v))


def verify():
    print("Q6 / V4 Edge Count: Burnside Lemma Audit\n")

    V, E = build_q6()
    assert len(V) == 64
    assert len(E) == 192
    print(f"|V(Q6)| = {len(V)}  ✓")
    print(f"|E(Q6)| = {len(E)}  ✓  (6 × 2^5 = 192)\n")

    # ── Algebraic proof: Fix(β) = 0 ──────────────────────────────────────────
    print("=" * 60)
    print("ALGEBRAIC PROOF: β has no fixed edges")
    print("=" * 60)
    print("""
  An edge {u, v} is fixed by β iff {β(u), β(v)} = {u, v}, i.e.:
    Case A: β(u)=u AND β(v)=v  (both palindromes, Hamming-adjacent)
    Case B: β(u)=v AND β(v)=u  (u and rev(u) are Hamming-adjacent)

  CASE A:
    Palindromes in Q6 have the form (a,b,c,c,b,a).
    Flipping any single bit i breaks the constraint bit[i]=bit[5-i]
    at BOTH position i and position 5-i simultaneously (since 6 is even,
    no bit occupies the centre). So no two palindromes are adjacent.

  CASE B:
    hamming(u, rev(u)) counts positions i where u[i] ≠ u[5-i].
    This count equals twice the number of mismatched pairs (i, 5-i)
    because each mismatch appears at both i and 5-i.
    Therefore hamming(u, rev(u)) ∈ {0, 2, 4, 6} — always even — never 1.
    """)

    # Verify Case A: no palindrome-palindrome edges
    pals = [v for v in V if v == v[::-1]]
    assert len(pals) == 8               # 2^3 palindromes in Q6
    pal_adj = [(u, v) for u in pals for v in pals if hamming(u, v) == 1]
    assert len(pal_adj) == 0
    print(f"  Palindromes in Q6: {len(pals)}  (form (a,b,c,c,b,a))")
    print(f"  Adjacent palindrome pairs: {len(pal_adj)}  ✓  (Case A: 0 fixed edges)")

    # Verify Case B: hamming(u, rev(u)) always even
    assert all(hamming(u, u[::-1]) % 2 == 0 for u in V)
    assert all(hamming(u, u[::-1]) != 1    for u in V)
    print(f"  hamming(u, rev(u)) is even for all 64 vertices  ✓  (Case B: 0 fixed edges)\n")

    # ── Fixed-edge counts for all four group elements ─────────────────────────
    print("=" * 60)
    print("BURNSIDE: fixed-edge counts")
    print("=" * 60)

    group = [("id", identity), ("α", alpha), ("β", beta), ("αβ", gamma)]
    fixed_counts = {}
    for name, g in group:
        count = sum(1 for e in E if apply_to_edge(g, e) == e)
        fixed_counts[name] = count

    assert fixed_counts["id"] == 192
    assert fixed_counts["α"]  == 0
    assert fixed_counts["β"]  == 0
    assert fixed_counts["αβ"] == 0

    print()
    for name, count in fixed_counts.items():
        note = ""
        if name == "id":  note = "  (all edges)"
        if name == "α":   note = "  (complement maps u↦1-u; no binary solution to 1-u=u)"
        if name == "β":   note = "  (proved above)"
        if name == "αβ":  note = "  (hamming(u, 1-rev(u)) always even — same parity argument)"
        print(f"  Fix({name}) = {count}{note}")

    burnside_sum = sum(fixed_counts.values())
    quotient_edges = burnside_sum // 4
    assert quotient_edges == 48

    print(f"\n  Burnside sum: {burnside_sum}")
    print(f"  |E(Q6/V4)| = {burnside_sum} / 4 = {quotient_edges}  ✓\n")

    # ── Verify by direct orbit counting ──────────────────────────────────────
    print("=" * 60)
    print("VERIFICATION: direct orbit enumeration")
    print("=" * 60)

    seen_orbits: set = set()
    edge_orbits = 0
    for e in E:
        orbit = frozenset(apply_to_edge(g, e) for _, g in group)
        if orbit not in seen_orbits:
            seen_orbits.add(orbit)
            edge_orbits += 1

    assert edge_orbits == 48
    print(f"\n  Distinct edge orbits: {edge_orbits}  ✓")
    print(f"  All orbit sizes: {sorted(set(len(frozenset(apply_to_edge(g,e) for _,g in group)) for e in E))}")

    # ── Refutation of the "56" claim ──────────────────────────────────────────
    print()
    print("=" * 60)
    print("REFUTATION: the 56-edge claim")
    print("=" * 60)
    print(f"""
  The "56" claim requires Fix(β) = 32.
  Source of the error: the erroneous code reported 32 fixed edges
  under β, likely from a bug where the lambda identity function in the
  group list [lambda x: x, alpha, beta, gamma] incorrectly captured
  the wrong reference, or from confusing vertex palindromes (8 vertices)
  with edge palindromes (0 edges).

  Checking: does ANY edge satisfy apply_to_edge(beta, e) == e?
    → {sum(1 for e in E if apply_to_edge(beta, e) == e)} edges  ✓  (zero, confirmed)

  Burnside with wrong Fix(β)=32 would give (192+0+32+0)/4 = 56 — this is false.
  Correct result: (192+0+0+0)/4 = 48.
    """)

    # ── Summary ───────────────────────────────────────────────────────────────
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"""
  VERIFIED:
    |V(Q6)| = 64,  |E(Q6)| = 192                         ✓
    Fix(id)  = 192                                         ✓
    Fix(α)   = 0   (complement has no binary fixed point)  ✓
    Fix(β)   = 0   (hamming(u, rev(u)) always even)        ✓
    Fix(αβ)  = 0   (same parity argument)                  ✓
    |E(Q6/V4)| = 192/4 = 48  (Burnside)                   ✓
    |E(Q6/V4)| = 48  (direct orbit enumeration)            ✓

  REFUTED:
    Fix(β) = 32  →  FALSE
    |E(Q6/V4)| = 56  →  FALSE

  ACTION IS FREE ON EDGES:
    All edge orbits have size exactly 4 (no edge stabilizer).
    This is equivalent to: the V4 action is free on E(Q6).
    Confirmed: orbit sizes = {{4}} only.
    """)

    print("All assertions passed.")


if __name__ == "__main__":
    verify()
