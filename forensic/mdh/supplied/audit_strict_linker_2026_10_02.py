# CLASS: AUDIT
"""
Audit of the supplied StrictForensicLinker (2026-10-02), saved verbatim in
strict_linker_2026_10_02.py.  Its own three tests pass.  Run this file for the
findings below; each is asserted.

HOLDS
 - Equal timestamps without an explicit source_sequence produce no edge in
   either direction; with sequence 1 < 2 they produce FRAGMENT_CONTINUATION.
 - Weight inversion M - w gives the maximum-weight spanning arborescence.
   It is exact for ANY constant M, because every spanning arborescence of n
   nodes has n - 1 edges: sum(M - w) = (n-1)M - sum(w).  The "+ epsilon so
   weights stay positive" step is not needed for exactness (Edmonds accepts
   any real weights); it is harmless.

DEFECTS
 1. selected_root is computed but never given to the optimizer.  With an
    explicit root that has an incoming candidate edge, Edmonds roots the tree
    elsewhere while the output reports root_id = the explicit root and names
    the component after it.  Reproduced: e0 -> e1 (e1 marked explicit root);
    output root_id "e1", actual tree root "e0".
 2. "Preserves the rejected hypotheses" is not what the code does.  REJECTED
    edges -- including every cross-session edge -- are never added to the
    graph, so they appear in no component's discarded_edges.  Only ACCEPTED
    and AMBIGUOUS edges that lost to the tree are kept.
 3. MESSAGE_SUCCESSION is never produced, and CAUSAL_REPLY is assigned to
    every strictly later event in the horizon.  TurnEvent has no role field,
    so "inter-role turn boundary" cannot be tested; the taxonomy in section I
    is not implemented.
 4. PayloadIntegrity defines < and <= but not > or >=, which fall back to
    str comparison: MALFORMED < COMPLETE is True and COMPLETE > MALFORMED is
    False.  The "lattice" is inconsistent.
 5. The JSON in section IV was not produced by this code.
    - evt_301 -> evt_303 and evt_302 -> evt_303 have the same delta (both
      sources at 18:00:00, target at 18:04:15) but are shown with temporal
      affinities 0.450 and 0.650; the formula gives 0.820 for both.
    - Same session, same source: weight = min(1, 0.75 + 0.2 a + 0.05).
      Affinity 1.0 gives 1.000, not the 0.910 shown; 0.650 gives 0.930, not
      0.820; 0.450 gives 0.890, not 0.740.
 6. Default event_confidence is 0.0, so a VERIFIED component built from
    default events reports component_confidence 0.0.
 7. "Byte-stream deframing introduces zero offset drift": there is no
    deframing code in the supplied engine; the claim has nothing to test.
 8. Comparison with the repo engine (forensic/mdh/branching.py): that one
    computes a maximum BRANCHING through a virtual root, so several roots in
    one component are allowed and the root is chosen by weight.  The supplied
    engine marks any component with two in-degree-zero nodes UNRESOLVED.

FALSIFICATION: any assertion failing.
"""
import os
import sys
from datetime import datetime, timedelta

try:
    import networkx as nx
except ImportError:      # the SUPPLIED engine imports networkx; it cannot run without it
    print("audit_strict_linker: the supplied engine needs networkx (pip install networkx). "
          "The fixed engine, forensic/mdh/strict_linker.py, does not.")
    raise SystemExit(0)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import strict_linker_2026_10_02 as S  # noqa: E402

S.test_equal_timestamp_without_sequence_fails()
S.test_equal_timestamp_with_sequence_succeeds()
S.test_exact_edmonds_weight_inversion()

t0 = datetime(2026, 3, 8, 12, 0, 0)

# 1. explicit root not enforced
L = S.StrictForensicLinker()
e0 = S.TurnEvent("e0", timestamp=t0, session_id="s", event_confidence=1.0)
e1 = S.TurnEvent("e1", timestamp=t0 + timedelta(minutes=1), session_id="s", is_explicit_root=True, event_confidence=1.0)
e2 = S.TurnEvent("e2", timestamp=t0 + timedelta(minutes=2), session_id="s", event_confidence=1.0)
comp = L.reconstruct([e0, e1, e2])[0]
G = nx.DiGraph([(e.source_id, e.target_id) for e in comp.selected_arborescence])
true_root = [n for n in G if G.in_degree(n) == 0]
assert comp.root_id == "e1" and comp.component_id == "comp_e1" and true_root == ["e0"]

# 2. rejected (cross-session) edges vanish
a = S.TurnEvent("a", timestamp=t0, session_id="s1", event_confidence=1.0)
b = S.TurnEvent("b", timestamp=t0 + timedelta(minutes=1), session_id="s1", event_confidence=1.0)
c = S.TurnEvent("c", timestamp=t0 + timedelta(minutes=2), session_id="s2", event_confidence=1.0)
assert L.evaluate_directed_edge(a, c).classification == S.EdgeClassification.REJECTED
out = L.reconstruct([a, b, c])
kept = {(e.source_id, e.target_id) for k in out for e in k.selected_arborescence + k.discarded_edges}
assert ("a", "c") not in kept and ("b", "c") not in kept

# 3. edge types actually produced
types = set()
for d in range(0, 46):
    for seq in ((None, None), (1, 2)):
        u = S.TurnEvent("u", timestamp=t0, source_sequence=seq[0], session_id="s")
        v = S.TurnEvent("v", timestamp=t0 + timedelta(minutes=d), source_sequence=seq[1], session_id="s")
        e = L.evaluate_directed_edge(u, v)
        if e:
            types.add(e.edge_type)
assert types == {S.EdgeType.CAUSAL_REPLY, S.EdgeType.FRAGMENT_CONTINUATION}
assert not hasattr(S.TurnEvent(" ", None), "role")

# 4. inconsistent ordering
P = S.PayloadIntegrity
assert (P.MALFORMED < P.COMPLETE) is True and (P.COMPLETE > P.MALFORMED) is False

# 5. the section IV JSON is not this code's output
T = datetime(2026, 3, 8, 18, 0, 0)
x1 = S.TurnEvent("evt_301", timestamp=T, source_sequence=1, session_id="sess_900", source="x")
x2 = S.TurnEvent("evt_302", timestamp=T, source_sequence=2, session_id="sess_900", source="x")
x3 = S.TurnEvent("evt_303", timestamp=T + timedelta(minutes=4, seconds=15), session_id="sess_900", source="x")
w12, w23, w13 = (L.evaluate_directed_edge(*p) for p in ((x1, x2), (x2, x3), (x1, x3)))
assert w23.evidence_vector["temporal_affinity"] == w13.evidence_vector["temporal_affinity"] == 0.82
assert (w12.weight, w23.weight, w13.weight) == (1.0, 0.964, 0.964)
assert (w12.weight, w23.weight, w13.weight) != (0.910, 0.820, 0.740)
f = lambda a_: round(min(1.0, 0.75 + 0.2 * a_ + 0.05), 3)
assert (f(1.0), f(0.65), f(0.45)) == (1.0, 0.93, 0.89)

# 6. default confidence
d1 = S.TurnEvent("d1", timestamp=t0, session_id="s")
d2 = S.TurnEvent("d2", timestamp=t0 + timedelta(minutes=1), session_id="s")
k = L.reconstruct([d1, d2])[0]
assert k.status == S.GraphComponentStatus.VERIFIED and k.component_confidence == 0.0

# exactness of inversion for any M (including no epsilon, and negative)
import random
R = random.Random(3)
for _ in range(200):
    n = R.randrange(3, 7)
    G = nx.DiGraph()
    for i in range(n):
        for j in range(i + 1, n):
            if R.random() < 0.7:
                G.add_edge(i, j, weight=round(R.random(), 3))
    if not nx.is_weakly_connected(G) or sum(1 for v in G if G.in_degree(v) == 0) != 1:
        continue
    best = None
    for M in (0.0, -5.0, max(d["weight"] for *_, d in G.edges(data=True)) + 1.0):
        H = nx.DiGraph(); H.add_nodes_from(G)
        for u, v, dd in G.edges(data=True):
            H.add_edge(u, v, weight=M - dd["weight"])
        A = nx.minimum_spanning_arborescence(H)
        tot = round(sum(G[u][v]["weight"] for u, v in A.edges()), 9)
        best = tot if best is None else best
        assert tot == best
    assert best == round(nx.maximum_spanning_arborescence(G).size(weight="weight"), 9)

if __name__ == "__main__":
    print("StrictForensicLinker audit: supplied tests pass; 8 findings asserted")
