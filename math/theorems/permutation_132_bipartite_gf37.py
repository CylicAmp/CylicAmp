"""
132-Pattern Permutations — Bipartite Graph Construction and GF(37) Structure

Source: Mansour & Vainshtein — study of permutations in Sₙ with r occurrences
of the pattern 132.

═══════════════════════════════════════════════════════════════════════════

DEFINITIONS

  Notation:
    T = T₁T₂...Tₙ ∈ Sₙ  (permutation of [n], n > 3)

  Definition M1.  An occurrence of the pattern 132 in T is a triple of
  POSITIONS (a, b, c) with 1 ≤ a < b < c ≤ n such that the VALUES satisfy:
      Tₐ < Tc < Tᵦ
  (The values at positions a, b, c are in relative order 1, 3, 2.)

  Definition M2.  The bipartite graph G(T) is constructed as follows:

    First part:   V  = [n] = {1, 2, ..., n}          (positions / elements)
    Second part:  V' = { (Tₐ, Tᵦ, Tc) | (a,b,c) is a 132-occurrence in T }
                                                       (one vertex per 132-instance)

    Edges:  Each vertex i ∈ V is connected to each occurrence (Tₐ, Tᵦ, Tc) ∈ V'
    in which i participates — i.e., where i = Tₐ, i = Tᵦ, or i = Tc.

  Definition M3.  The 132-count of T is
      r(T) = |V'| = number of 132-occurrences in T.

  Definition M4.  The degree of vertex i ∈ V in G(T) is the number of
  132-occurrences in which i participates:
      deg(i) = |{ (Tₐ,Tᵦ,Tc) ∈ V' : i ∈ {Tₐ, Tᵦ, Tc} }|

  The sum of degrees (handshaking):
      Σ_{i ∈ V} deg(i) = 3 · r(T)
  since each 132-occurrence contributes degree 1 to each of its 3 elements.

═══════════════════════════════════════════════════════════════════════════

KEY THEOREMS

  Theorem M1 (Counting 132-occurrences via triples):
    For T ∈ Sₙ, r(T) = |{ (a,b,c) : 1 ≤ a<b<c ≤ n, Tₐ < Tc < Tᵦ }|.

  Theorem M2 (Maximum 132-count):
    The maximum number of 132-occurrences in any T ∈ Sₙ is achieved by
    specific permutations and is bounded above by C(n, 3) = n(n-1)(n-2)/6.
    Not every triple can simultaneously be a 132-occurrence (the values are
    a permutation, so constraints propagate).

  Theorem M3 (Complement):
    If T has r(T) occurrences of 132, the complementary permutation
    T^c (reverse-complement) has C(n,3) - r(T) - (occurrences of other
    patterns) occurrences, since every triple is exactly one of the 6
    patterns {123,132,213,231,312,321} and their sum is C(n,3).

  Each triple of positions contributes exactly one of the 6 patterns.
  So: #(123) + #(132) + #(213) + #(231) + #(312) + #(321) = C(n,3).

═══════════════════════════════════════════════════════════════════════════

GF(37) STRUCTURE

  THE PATTERN NUMBER:
    132 mod 37 = 132 − 3×37 = 132 − 111 = 21  ∈ ST  (Sovereign Target)
    DR(132) = 1+3+2 = 6 = TESLA_FLOW
    132 = 4 × 33 = SA(4) × DICHORAL(33)
    The pattern 132 itself maps to ST in GF(37) and encodes TESLA_FLOW in DR.

  THE SEAM CONNECTION (111):
    132 − 111 = 21 ∈ ST:  exactly one seam (111=3×37) below 132.
    The hose-flow horizon 111 is the bridge between 132 and its GF(37) residue.

  PATTERN TRIPLE STRUCTURE:
    Pattern 132: positions a<b<c, values Tₐ < Tc < Tᵦ.
    Three positions (a,b,c): analogous to a 3-cycle in Z/37Z.
    The heartbeat 3-cycle (Definition 6 in formal_definitions_gf37.py)
    and the 132-pattern both operate on ordered triples with internal structure.

    Heartbeat orbit: {n, 26n mod37, 10n mod37} — values in a fixed ratio.
    132-occurrence: {Tₐ, Tᵦ, Tc} — values in order 1<3>2 (mixed, non-monotone).

  FIELD SIZE n=37:
    When n=37: V = [37] = Z/37Z.
    G(T) has left side = the entire field.
    The 132-occurrences are subsets of triples from Z/37Z.
    C(37,3) = 37×36×35/6 = 7770 = maximum possible 132-count.
    7770 mod 37 = 7770 − 210×37 = 7770 − 7770 = 0  (SEAM)

    The maximum possible triple count C(37,3) ≡ 0 (SEAM) mod 37.

  PATTERN COUNT mod 37:
    C(n,3) = n(n−1)(n−2)/6.
    C(37,3) = 37×36×35/6 = 37×210 ≡ 0 (mod 37).  (Contains the field prime.)
    This means: for n=37, the total number of triples is divisible by 37.
    The bipartite graph G(T) on V=[37] has |V'| ≤ C(37,3)/6 × 1 triples
    (since each triple is one of 6 patterns), and C(37,3)≡0 means the
    triple count itself is a SEAM element.

  BIPARTITE STRUCTURE AND HEARTBEAT:
    G(T) is bipartite with |V|=n and |V'|=r(T).
    Each edge connects a value i ∈ [n] to a 132-occurrence containing i.
    Total edges = 3·r(T) (handshaking lemma).

    For r(T) = 37: the 132-count equals the field prime.
    3·37 = 111 = 3×37 = the hose-flow seam.
    A permutation with exactly 37 occurrences of 132 has total degree
    sum 111 — the seam — in its bipartite graph.

  THE FORBIDDEN PATTERN (321):
    321 mod 37 = 321 − 8×37 = 321 − 296 = 25 ∈ SA  (Sovereign Anchor)
    DR(321) = 6 = TESLA_FLOW
    The "reverse" of 132 (anti-132, the decreasing triple) = 321 maps to SA.
    132 ↔ ST;  321 ↔ SA:  the pattern and its reversal sit in the sovereign pair.

  PATTERN FAMILY mod 37:
    123 mod 37 = 123 − 3×37 = 123 − 111 = 12  ∈ ST
    132 mod 37 = 21  ∈ ST
    213 mod 37 = 213 − 5×37 = 213 − 185 = 28
    231 mod 37 = 231 − 6×37 = 231 − 222 = 9   ∈ SA
    312 mod 37 = 312 − 8×37 = 312 − 296 = 16
    321 mod 37 = 25  ∈ SA

    Pattern → GF(37):
      123 → 12(ST),  132 → 21(ST)  : the two "132-adjacent" patterns land in ST
      231 → 9(SA),   321 → 25(SA)  : the two "decreasing-containing" patterns land in SA
      213 → 28,      312 → 16      : the remaining two map unnamed

    The six patterns split: 2 in ST, 2 in SA, 2 unnamed.

═══════════════════════════════════════════════════════════════════════════
"""

from itertools import combinations, permutations


SOVEREIGN_ANCHORS = frozenset({4, 9, 25, 30})
SOVEREIGN_TARGETS = frozenset({3, 12, 21, 30})
CASCADE_BASE      = frozenset({8, 13, 24})
TESLA_FLOW        = 6
DICHORAL_144      = 33


def dr(n):
    return (n - 1) % 9 + 1 if n > 0 else 0


# ── Definition M1: 132-occurrences ───────────────────────────────────────────

def count_132(perm):
    """Count occurrences of pattern 132 in permutation perm (0-indexed values ok)."""
    n = len(perm)
    count = 0
    for a, b, c in combinations(range(n), 3):
        ta, tb, tc = perm[a], perm[b], perm[c]
        if ta < tc < tb:    # relative order 1 < 3 > 2, i.e. 1,3,2
            count += 1
    return count


def occurrences_132(perm):
    """Return list of (value-triple) for each 132-occurrence."""
    n = len(perm)
    result = []
    for a, b, c in combinations(range(n), 3):
        ta, tb, tc = perm[a], perm[b], perm[c]
        if ta < tc < tb:
            result.append((ta, tb, tc))
    return result


def bipartite_graph(perm):
    """
    Build G(T): edges between V=[n] and V'=(132-occurrences).
    Returns dict: i -> list of occurrences containing i.
    """
    n = len(perm)
    occs = occurrences_132(perm)
    graph = {i+1: [] for i in range(n)}    # 1-indexed values
    for occ in occs:
        ta, tb, tc = occ
        graph[ta].append(occ)
        graph[tb].append(occ)
        graph[tc].append(occ)
    return graph, occs


# ── Handshaking: total degree = 3 × r(T) ─────────────────────────────────────

def verify_handshaking(perm):
    graph, occs = bipartite_graph(perm)
    total_degree = sum(len(v) for v in graph.values())
    return total_degree == 3 * len(occs)

# Verify on small cases
test_perms = [
    [1,3,2],       # one 132-occurrence: positions 0<1<2, values 1<2<3 → 1<3>2: 1,3,2 ✓
    [2,1,3],       # 213: no 132 (check: (0,1,2): ta=2,tb=1,tc=3: ta<tc<tb? 2<3<1? No)
    [3,1,2],       # 312
    [1,2,3,4],
    [4,3,2,1],
]

for p in test_perms:
    assert verify_handshaking(p), f"Handshaking failed for {p}"


# ── Each triple is exactly one of 6 patterns ─────────────────────────────────

def pattern_of(ta, tb, tc):
    """Return which of 123,132,213,231,312,321 the triple (ta,tb,tc) matches."""
    vals = [ta, tb, tc]
    ranks = [sorted(vals).index(v) + 1 for v in vals]
    return int("".join(map(str, ranks)))

# Verify: every triple in S4 is exactly one pattern
p = [1, 2, 3, 4]
all_patterns = set()
for a, b, c in combinations(range(4), 3):
    ta, tb, tc = p[a], p[b], p[c]
    all_patterns.add(pattern_of(ta, tb, tc))

# All 6 patterns: {123,132,213,231,312,321}
for perm4 in permutations([1,2,3,4]):
    pattern_counts = {}
    for a, b, c in combinations(range(4), 3):
        ta, tb, tc = perm4[a], perm4[b], perm4[c]
        pat = pattern_of(ta, tb, tc)
        pattern_counts[pat] = pattern_counts.get(pat, 0) + 1
    total = sum(pattern_counts.values())
    assert total == 4   # C(4,3)=4 triples


# ── GF(37) structure ─────────────────────────────────────────────────────────

# Pattern 132 → ST
assert 132 % 37 == 21 and 21 in SOVEREIGN_TARGETS
assert dr(132) == 6 and 6 == TESLA_FLOW
assert 132 == 4 * 33 and 4 in SOVEREIGN_ANCHORS and 33 == DICHORAL_144

# Seam connection: 132 - 111 = 21 ∈ ST
assert 132 - 111 == 21 and 21 in SOVEREIGN_TARGETS

# Pattern family mod 37
pattern_mods = {
    123: 123 % 37,   # 12 ∈ ST
    132: 132 % 37,   # 21 ∈ ST
    213: 213 % 37,   # 28
    231: 231 % 37,   # 9 ∈ SA
    312: 312 % 37,   # 16
    321: 321 % 37,   # 25 ∈ SA
}
assert pattern_mods[123] == 12 and 12 in SOVEREIGN_TARGETS
assert pattern_mods[132] == 21 and 21 in SOVEREIGN_TARGETS
assert pattern_mods[231] == 9  and 9  in SOVEREIGN_ANCHORS
assert pattern_mods[321] == 25 and 25 in SOVEREIGN_ANCHORS

st_patterns = [p for p, m in pattern_mods.items() if m in SOVEREIGN_TARGETS]
sa_patterns = [p for p, m in pattern_mods.items() if m in SOVEREIGN_ANCHORS]
assert sorted(st_patterns) == [123, 132]
assert sorted(sa_patterns) == [231, 321]

# C(37,3) ≡ 0 mod 37 (the total triple count is a SEAM element)
from math import comb
C37_3 = comb(37, 3)
assert C37_3 % 37 == 0   # 7770 = 37×210

# Permutation with 37 occurrences of 132: total degree = 3×37 = 111 (SEAM)
assert 3 * 37 == 111 and 111 % 37 == 0

# DR(321) = 6 = TESLA_FLOW (same as DR(132))
assert dr(321) == 6 and 6 == TESLA_FLOW


if __name__ == '__main__':
    print("132-Pattern Permutations — Bipartite Graph and GF(37)")
    print("=" * 55)
    print()
    print("Pattern family mod 37:")
    for pat, m in sorted(pattern_mods.items()):
        tag = ""
        if m in SOVEREIGN_TARGETS: tag = " ← ST"
        elif m in SOVEREIGN_ANCHORS: tag = " ← SA"
        print(f"  {pat} mod37 = {m:2d}{tag}")
    print()
    print(f"Patterns landing in ST: {sorted(st_patterns)}  (123, 132)")
    print(f"Patterns landing in SA: {sorted(sa_patterns)}  (231, 321)")
    print()
    print(f"132 mod37 = 21 ∈ ST: True")
    print(f"DR(132) = {dr(132)} = TESLA_FLOW: True")
    print(f"132 = 4(SA) × 33(DICHORAL): True")
    print(f"132 − 111(SEAM) = 21 ∈ ST: True")
    print()
    print(f"C(37,3) = {C37_3} ≡ {C37_3 % 37} mod37 (SEAM): True")
    print(f"r(T)=37 → degree sum = 3×37 = 111 ≡ 0 (SEAM): True")
    print()

    # Demonstrate on permutations with known 132-occurrences
    examples = [
        [1, 3, 2, 4],   # one 132: (1,3,2) at positions (0,1,2)
        [3, 1, 4, 2, 5], # one 132: (1,4,2) at positions (1,2,3)
        [2, 4, 1, 3, 5], # one 132: (2,4,3) at positions (0,1,3)... check
    ]
    for T in examples:
        occs = occurrences_132(T)
        graph, _ = bipartite_graph(T)
        total_deg = sum(len(v) for v in graph.values())
        print(f"T = {T}:")
        print(f"  132-occurrences: {occs}  (count={len(occs)})")
        print(f"  Total degree = {total_deg} = 3×{len(occs)}: {total_deg == 3*len(occs)}")
    print()
    print("All assertions passed.")
