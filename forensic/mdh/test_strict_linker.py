"""Tests for strict_linker.py: the five audited defects (D1-D5), axioms A1-A7,
and the derivative of the edge score.  Defect references:
forensic/mdh/supplied/audit_strict_linker_2026_10_02.py."""
import json
import os
import random
from datetime import datetime, timedelta

import networkx as nx
import pytest

from forensic.mdh import strict_linker as S

T0 = datetime(2026, 3, 8, 12, 0, 0)
HERE = os.path.dirname(os.path.abspath(__file__))


def ev(i, minutes=0.0, **kw):
    kw.setdefault("session_id", "s")
    kw.setdefault("role", "user")
    kw.setdefault("event_confidence", 1.0)
    return S.TurnEvent(i, T0 + timedelta(minutes=minutes), **kw)


# ---- the supplied tests, kept (roles added where strict order needs them) ----
def test_equal_timestamp_without_sequence_no_edge():
    L = S.StrictForensicLinker()
    a, b = ev("e1"), ev("e2")
    assert L.evaluate_directed_edge(a, b) is None and L.evaluate_directed_edge(b, a) is None
    out = L.reconstruct([a, b])
    assert [c.status for c in out] == [S.GraphComponentStatus.SINGLETON] * 2


def test_equal_timestamp_with_sequence_fragment():
    L = S.StrictForensicLinker()
    a, b = ev("e1", source_sequence=1), ev("e2", source_sequence=2)
    e = L.evaluate_directed_edge(a, b)
    assert e.edge_type == S.EdgeType.FRAGMENT_CONTINUATION
    out = L.reconstruct([a, b])
    assert len(out) == 1 and out[0].status == S.GraphComponentStatus.VERIFIED and out[0].root_id == "e1"


def test_max_weight_tree_selected():
    L = S.StrictForensicLinker()
    W = {("e1", "e2"): 0.9, ("e1", "e3"): 0.7, ("e2", "e4"): 0.4, ("e3", "e4"): 0.8}
    L.evaluate_directed_edge = lambda u, v: (S.EdgeEvidence(u.event_id, v.event_id, W[(u.event_id, v.event_id)],
                                             S.EdgeType.CAUSAL_REPLY, S.EdgeClassification.ACCEPTED, {}, "t")
                                             if (u.event_id, v.event_id) in W else None)
    es = [ev("e1", 0, is_explicit_root=True), ev("e2", 1), ev("e3", 2), ev("e4", 3)]
    c = L.reconstruct(es)[0]
    assert {(e.source_id, e.target_id) for e in c.selected_arborescence} == {("e1", "e2"), ("e1", "e3"), ("e3", "e4")}
    assert [(e.source_id, e.target_id) for e in c.discarded_edges] == [("e2", "e4")]


# ---- D1 explicit root ----
def test_D1_explicit_root_with_earlier_event_is_conflict_not_mislabel():
    L = S.StrictForensicLinker()
    c = L.reconstruct([ev("e0", 0), ev("e1", 1, is_explicit_root=True), ev("e2", 2)])[0]
    assert c.status == S.GraphComponentStatus.UNRESOLVED and c.root_id is None
    assert c.diagnostics[0].startswith("EXPLICIT_ROOT_CONFLICT")


def test_D1_explicit_root_is_tree_root():
    L = S.StrictForensicLinker()
    c = L.reconstruct([ev("e0", 0, is_explicit_root=True), ev("e1", 1, role="model"), ev("e2", 2)])[0]
    G = nx.DiGraph([(e.source_id, e.target_id) for e in c.selected_arborescence])
    assert [n for n in G if G.in_degree(n) == 0] == [c.root_id] == ["e0"]


# ---- D2 rejected edges kept ----
def test_D2_rejected_edges_recorded():
    L = S.StrictForensicLinker()
    out = L.reconstruct([ev("a", 0, session_id="s1"), ev("b", 1, session_id="s1"), ev("c", 2, session_id="s2")])
    rej = {(e.source_id, e.target_id) for c in out for e in c.rejected_edges}
    assert rej == {("a", "c"), ("b", "c")}


# ---- D3 taxonomy ----
def test_D3_edge_types():
    L = S.StrictForensicLinker()
    u = ev("u", 0, role="user")
    assert L.evaluate_directed_edge(u, ev("v", 1, role="model")).edge_type == S.EdgeType.CAUSAL_REPLY
    assert L.evaluate_directed_edge(u, ev("v", 1, role="user")).edge_type == S.EdgeType.MESSAGE_SUCCESSION
    assert L.evaluate_directed_edge(u, ev("v", 1, role=None)) is None          # UNKNOWN: no edge
    assert L._determine_causal_order(u, ev("v", 1, role=None))[2] == S.EdgeType.UNKNOWN


# ---- D4 total order ----
def test_D4_total_order():
    P = list(S.PayloadIntegrity)
    for a in P:
        for b in P:
            assert [a < b, a == b, a > b].count(True) == 1                     # A6
            assert (a <= b) == (a < b or a == b) and (a >= b) == (a > b or a == b)
            assert (a < b) == (b > a)
    assert S.PayloadIntegrity.MALFORMED < S.PayloadIntegrity.COMPLETE
    assert S.PayloadIntegrity.COMPLETE > S.PayloadIntegrity.MALFORMED
    assert max(P) == S.PayloadIntegrity.COMPLETE


# ---- D5 artifact produced by the code ----
def test_D5_artifact_matches_code():
    with open(os.path.join(HERE, "strict_linker_example.json")) as f:
        assert f.read() == S.example_json()
    d = json.loads(S.example_json())[0]
    assert d["status"] == "CANDIDATE_COMPONENT"                               # tie, see below
    assert any(x.startswith("TIED_PARENT") for x in d["diagnostics"])


def test_tie_is_not_verified():
    L = S.StrictForensicLinker()
    c = L.reconstruct(S.example_events())[0]
    w = {(e.source_id, e.target_id): e.weight for e in c.selected_arborescence + c.discarded_edges}
    assert w[("evt_301", "evt_303")] == w[("evt_302", "evt_303")] == 0.964
    assert c.status == S.GraphComponentStatus.CANDIDATE


def test_confidence_not_supplied():
    L = S.StrictForensicLinker()
    c = L.reconstruct([ev("a", 0, event_confidence=None), ev("b", 1, role="model", event_confidence=None)])[0]
    assert c.component_confidence is None and "not supplied" in c.diagnostics[-1]


# ---- axioms on random inputs ----
def random_events(R, n):
    out = []
    for i in range(n):
        out.append(S.TurnEvent(f"e{i:02d}", T0 + timedelta(minutes=R.choice([0, 0, 1, 2, 5, 30, 60])),
                               source_sequence=R.choice([None, 1, 2, 3]),
                               role=R.choice([None, "user", "model"]),
                               session_id=R.choice([None, "s1", "s2"]),
                               is_explicit_root=R.random() < 0.1,
                               event_confidence=R.choice([None, 0.5, 1.0]),
                               payload_integrity=R.choice(list(S.PayloadIntegrity))))
    return out


@pytest.mark.parametrize("seed", range(150))
def test_axioms_random(seed):
    R = random.Random(seed)
    events = random_events(R, R.randrange(2, 9))
    L = S.StrictForensicLinker()
    out = L.reconstruct(events)
    # every event in exactly one component
    ids = sorted(e.event_id for c in out for e in c.events)
    assert ids == sorted(e.event_id for e in events)
    work = [e for e in events if e.payload_integrity != S.PayloadIntegrity.MALFORMED and e.timestamp]
    G = nx.DiGraph()
    passing = set()
    for u in work:
        for v in work:
            e = L.evaluate_directed_edge(u, v)
            if e:
                passing.add((u.event_id, v.event_id))
                # A1 basis
                assert e.ordering_basis in ("strict_timestamp_order", "protocol_sequence_continuity")
                if e.ordering_basis == "strict_timestamp_order":
                    assert u.role is not None and v.role is not None and u.timestamp < v.timestamp
                else:
                    assert u.timestamp == v.timestamp and u.source_sequence < v.source_sequence
                G.add_edge(u.event_id, v.event_id)
    assert nx.is_directed_acyclic_graph(G)                                    # A2
    ledger = [(e.source_id, e.target_id) for c in out
              for e in c.selected_arborescence + c.discarded_edges + c.rejected_edges]
    assert sorted(ledger) == sorted(passing)                                  # A3 exactly once
    for c in out:
        if c.selected_arborescence:                                           # A4
            T = nx.DiGraph([(e.source_id, e.target_id) for e in c.selected_arborescence])
            assert [n for n in T if T.in_degree(n) == 0] == [c.root_id]
            assert T.number_of_nodes() == len(c.events) and nx.is_arborescence(T)
        if c.component_confidence is not None and c.mean_event_confidence is not None:   # A5
            assert c.component_confidence <= min(c.bottleneck_score, c.mean_event_confidence) + 1e-12 \
                or c.status not in (S.GraphComponentStatus.VERIFIED, S.GraphComponentStatus.CANDIDATE)
    # A7 determinism
    R2 = random.Random(seed)
    again = S.StrictForensicLinker().reconstruct(random_events(R2, R2.randrange(2, 9)))
    assert json.dumps([S.to_record(c) for c in out], sort_keys=True) == \
        json.dumps([S.to_record(c) for c in again], sort_keys=True)


# ---- derivatives of the score ----
def test_affinity_derivative_nonpositive():
    H = 2700.0
    xs = [H * i / 1000 for i in range(1001)]
    a = [S.StrictForensicLinker.affinity(x, H) for x in xs]
    assert all(a[i + 1] <= a[i] for i in range(1000))                       # non-increasing
    for x in xs[1:-1]:                                                      # analytic slope
        h = 1e-3
        num = (S.StrictForensicLinker.affinity(x + h, H) - S.StrictForensicLinker.affinity(x - h, H)) / (2 * h)
        assert abs(num - (-2 * (1 - x / H) / H)) < 1e-7
    assert S.StrictForensicLinker.affinity(H, H) == 0.0


def test_weight_nonincreasing_in_gap():
    L = S.StrictForensicLinker()
    ws = [L.evaluate_directed_edge(ev("u", 0), ev("v", m / 4, role="model")).weight for m in range(1, 181)]
    assert all(ws[i + 1] <= ws[i] for i in range(len(ws) - 1))
