"""StrictForensicLinker v2 -- the supplied engine (supplied/strict_linker_2026_10_02.py)
with the five audited defects fixed (supplied/audit_strict_linker_2026_10_02.py).

FIXES
 D1 Explicit root enforced: every other event must be reachable from the
    selected root.  The candidate graph is acyclic, so that forces the root's
    in-degree to 0 and every spanning arborescence to hang from it.  If an
    event is not reachable (e.g. an earlier event points INTO the explicit
    root) the component is UNRESOLVED with diagnostic EXPLICIT_ROOT_CONFLICT,
    never a report naming a root the tree does not have.
 D2 Every evaluated pair is kept.  Each component carries rejected_edges
    (REJECTED classification, attached to the component of the edge's target)
    alongside selected_arborescence and discarded_edges.
 D3 Section I taxonomy implemented.  TurnEvent.role is new.  For strict
    timestamp order: roles known and different -> CAUSAL_REPLY; roles known
    and equal -> MESSAGE_SUCCESSION; a role missing -> UNKNOWN, and as section
    I specifies, no edge is formed.  Equal timestamps with source_sequence
    u < v -> FRAGMENT_CONTINUATION (unchanged).
 D4 PayloadIntegrity has a total order: <, <=, >, >= all use one rank.
 D5 The audit artifact is produced by the code (to_record), and
    forensic/mdh/strict_linker_example.json is regenerated from it and checked
    byte for byte by the tests.
 Also (v3, from the 2026-10-02 paper, Invariant 5): a node with two or more
    equal-weight best parents makes the optimum non-unique.  The choice is the
    canonical tuple (source_id, target_id, edge_type), the diagnostic is
    TIED_PARENT, and the status is AMBIGUOUS_COMPONENT (same rule as the repo
    engine's AT-15).  On a DAG this per-node test is exact: two trees of equal
    total weight exist iff some node has tied best parents.  The section IV
    scenario is this case: evt_301 -> evt_303 and evt_302 -> evt_303 both 0.964.
 Also (v3): EvidenceCompleteness has the paper's total order
    EMPTY < FRAGMENTED < PARTIAL < SUFFICIENT.
 Also: event_confidence defaults to None ("not supplied"), and a component
    whose events lack it reports component_confidence None with a diagnostic,
    instead of a VERIFIED component at confidence 0.0.  Output order is
    deterministic (components and edges sorted).

AXIOMS (each tested in test_strict_linker.py)
 A1 No edge without a provenance basis: an edge exists only on strict
    timestamp order with known roles, or equal timestamps with source
    sequence u < v.
 A2 Acyclic: every edge goes forward in (timestamp, source_sequence), so the
    candidate graph is a DAG.
 A3 Ledger completeness: every ordered pair that passes ordering appears in
    exactly one of selected / discarded / rejected.
 A4 The reported root is the in-degree-0 node of the selected tree.
 A5 component_confidence <= min(bottleneck, mean_event_confidence).
 A6 PayloadIntegrity is a total order: exactly one of a<b, a==b, a>b.
 A7 Determinism: the same input gives byte-identical JSON.

DERIVATIVES of the edge score (tested)
 affinity a(D) = (1 - D/H)^2 on 0 <= D <= H, so da/dD = -2(1 - D/H)/H <= 0:
 non-increasing in the gap D, zero slope at D = H.  Same session:
 w = min(1, 0.75 + 0.2 a + c), dw/da = 0.2 below the cap, so dw/dD = 0.2 da/dD
 <= 0.  The weight never rises as the gap grows.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Optional



class PayloadIntegrity(str, Enum):
    COMPLETE = "COMPLETE"
    PARTIAL = "PARTIAL"
    TRUNCATED = "TRUNCATED"
    MALFORMED = "MALFORMED"

    @property
    def rank(self) -> int:
        return ["MALFORMED", "TRUNCATED", "PARTIAL", "COMPLETE"].index(self.value)

    def _cmp(self, other):
        if not isinstance(other, PayloadIntegrity):
            return NotImplemented
        return self.rank - other.rank

    def __lt__(self, other):
        c = self._cmp(other); return c if c is NotImplemented else c < 0

    def __le__(self, other):
        c = self._cmp(other); return c if c is NotImplemented else c <= 0

    def __gt__(self, other):
        c = self._cmp(other); return c if c is NotImplemented else c > 0

    def __ge__(self, other):
        c = self._cmp(other); return c if c is NotImplemented else c >= 0

    __hash__ = str.__hash__


class EvidenceCompleteness(str, Enum):
    """Paper section 2.2: EMPTY < FRAGMENTED < PARTIAL < SUFFICIENT (total order)."""
    SUFFICIENT = "SUFFICIENT"
    PARTIAL = "PARTIAL"
    FRAGMENTED = "FRAGMENTED"
    EMPTY = "EMPTY"

    @property
    def rank(self) -> int:
        return ["EMPTY", "FRAGMENTED", "PARTIAL", "SUFFICIENT"].index(self.value)

    def _cmp(self, other):
        if not isinstance(other, EvidenceCompleteness):
            return NotImplemented
        return self.rank - other.rank

    def __lt__(self, other):
        c = self._cmp(other); return c if c is NotImplemented else c < 0

    def __le__(self, other):
        c = self._cmp(other); return c if c is NotImplemented else c <= 0

    def __gt__(self, other):
        c = self._cmp(other); return c if c is NotImplemented else c > 0

    def __ge__(self, other):
        c = self._cmp(other); return c if c is NotImplemented else c >= 0

    __hash__ = str.__hash__


class EdgeType(str, Enum):
    CAUSAL_REPLY = "CAUSAL_REPLY"
    FRAGMENT_CONTINUATION = "FRAGMENT_CONTINUATION"
    MESSAGE_SUCCESSION = "MESSAGE_SUCCESSION"
    UNKNOWN = "UNKNOWN"


class EdgeClassification(str, Enum):
    ACCEPTED = "ACCEPTED"
    AMBIGUOUS = "AMBIGUOUS"
    REJECTED = "REJECTED"


class GraphComponentStatus(str, Enum):
    VERIFIED = "VERIFIED_COMPONENT"
    CANDIDATE = "CANDIDATE_COMPONENT"
    AMBIGUOUS = "AMBIGUOUS_COMPONENT"
    SINGLETON = "SINGLETON"
    UNRESOLVED = "UNRESOLVED"
    QUARANTINED = "QUARANTINED"


@dataclass
class TurnEvent:
    event_id: str
    timestamp: Optional[datetime]
    source_sequence: Optional[int] = None
    transport_index: int = 0
    role: Optional[str] = None
    session_id: Optional[str] = None
    is_explicit_root: bool = False
    source: str = "unknown"
    payload_integrity: PayloadIntegrity = PayloadIntegrity.COMPLETE
    evidence_completeness: EvidenceCompleteness = EvidenceCompleteness.SUFFICIENT
    event_confidence: Optional[float] = None
    graph_status: GraphComponentStatus = GraphComponentStatus.UNRESOLVED


@dataclass
class EdgeEvidence:
    source_id: str
    target_id: str
    weight: float
    edge_type: EdgeType
    classification: EdgeClassification
    evidence_vector: dict
    ordering_basis: str


@dataclass
class ForensicComponent:
    component_id: str
    status: GraphComponentStatus
    root_id: Optional[str]
    events: list
    selected_arborescence: list
    discarded_edges: list
    rejected_edges: list
    bottleneck_score: float
    mean_event_confidence: Optional[float]
    component_confidence: Optional[float]
    diagnostics: list = field(default_factory=list)


def _key(e: EdgeEvidence):
    return (e.source_id, e.target_id)


# ---- plain-Python graph helpers (no networkx needed) ----
def _weak_components(nodes, edges):
    """weakly connected components, as sets, ordered by smallest id"""
    parent = {n: n for n in nodes}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for u, v in edges:
        parent[find(u)] = find(v)
    groups = {}
    for n in nodes:
        groups.setdefault(find(n), set()).add(n)
    return sorted(groups.values(), key=min)


def _descendants(edges, root):
    out = {}
    for u, v in edges:
        out.setdefault(u, []).append(v)
    seen, stack = set(), [root]
    while stack:
        for w in out.get(stack.pop(), []):
            if w not in seen:
                seen.add(w)
                stack.append(w)
    return seen


class StrictForensicLinker:
    def __init__(self, horizon_minutes=45, accept_threshold=0.70, ambiguous_threshold=0.35):
        self.horizon = timedelta(minutes=horizon_minutes)
        self.accept_thresh = accept_threshold
        self.ambig_thresh = ambiguous_threshold

    # ---- ordering (A1, A2, D3) ----
    def _determine_causal_order(self, u: TurnEvent, v: TurnEvent):
        if not u.timestamp or not v.timestamp:
            return False, "missing_timestamps", EdgeType.UNKNOWN
        if u.timestamp < v.timestamp:
            if v.timestamp - u.timestamp > self.horizon:
                return False, "temporal_horizon_exceeded", EdgeType.UNKNOWN
            if u.role is None or v.role is None:
                return False, "strict_timestamp_order_role_unknown", EdgeType.UNKNOWN
            if u.role != v.role:
                return True, "strict_timestamp_order", EdgeType.CAUSAL_REPLY
            return True, "strict_timestamp_order", EdgeType.MESSAGE_SUCCESSION
        if u.timestamp == v.timestamp:
            if u.source_sequence is not None and v.source_sequence is not None:
                if u.source_sequence < v.source_sequence:
                    return True, "protocol_sequence_continuity", EdgeType.FRAGMENT_CONTINUATION
                return False, "inverted_or_duplicate_protocol_sequence", EdgeType.UNKNOWN
            return False, "equal_timestamp_unprovenanced_transport_index", EdgeType.UNKNOWN
        return False, "chronologically_inverted", EdgeType.UNKNOWN

    @staticmethod
    def affinity(delta_s: float, horizon_s: float) -> float:
        r = delta_s / horizon_s
        return (1.0 - r) ** 2 if 0 <= r <= 1 else 0.0

    def evaluate_directed_edge(self, u: TurnEvent, v: TurnEvent) -> Optional[EdgeEvidence]:
        if u.event_id == v.event_id:
            return None
        ok, basis, etype = self._determine_causal_order(u, v)
        if not ok:
            return None
        if u.session_id and v.session_id and u.session_id != v.session_id:
            return EdgeEvidence(u.event_id, v.event_id, 0.0, etype, EdgeClassification.REJECTED,
                                {"session_match": -1.0}, basis)
        vec = {"session_match": None, "temporal_affinity": None, "source_cohesion": None}
        if u.session_id and v.session_id:
            vec["session_match"] = 1.0
        a = self.affinity((v.timestamp - u.timestamp).total_seconds(), self.horizon.total_seconds())
        vec["temporal_affinity"] = round(a, 3)
        if u.source == v.source and u.source != "unknown":
            vec["source_cohesion"] = 0.05
        c = vec["source_cohesion"] or 0.0
        score = min(1.0, 0.75 + 0.20 * a + c) if vec["session_match"] == 1.0 else a * 0.50 + c
        score = round(score, 3)
        cls = (EdgeClassification.ACCEPTED if score >= self.accept_thresh else
               EdgeClassification.AMBIGUOUS if score >= self.ambig_thresh else EdgeClassification.REJECTED)
        return EdgeEvidence(u.event_id, v.event_id, score, etype, cls, vec, basis)

    # ---- reconstruction ----
    def _component(self, cid, status, root, nodes, sel, disc, rej, bott, diags):
        confs = [n.event_confidence for n in nodes]
        if any(c is None for c in confs):
            mean = None
            comp = None
            diags = diags + ["Event confidence not supplied for every event."]
        else:
            mean = round(sum(confs) / len(confs), 3)
            comp = round(min(bott, mean), 3) if status in (GraphComponentStatus.VERIFIED,
                                                           GraphComponentStatus.CANDIDATE,
                                                           GraphComponentStatus.AMBIGUOUS) else 0.0
        for n in nodes:
            n.graph_status = status
        return ForensicComponent(cid, status, root, sorted(nodes, key=lambda e: e.event_id),
                                 sorted(sel, key=_key), sorted(disc, key=_key), sorted(rej, key=_key),
                                 bott, mean, comp, diags)

    def reconstruct(self, events: list) -> list:
        out = []
        emap = {e.event_id: e for e in events}
        work = []
        for e in events:
            if e.payload_integrity == PayloadIntegrity.MALFORMED:
                out.append(self._component(f"quarantine_{e.event_id}", GraphComponentStatus.QUARANTINED,
                                           e.event_id, [e], [], [], [], 0.0,
                                           ["Payload malformed: quarantined."]))
            elif not e.timestamp:
                out.append(self._component(f"singleton_{e.event_id}", GraphComponentStatus.SINGLETON,
                                           None, [e], [], [], [], 0.0, ["Missing timestamp: causally unanchored."]))
            else:
                work.append(e)

        cand, rejected = {}, []
        for u in work:
            for v in work:
                ed = self.evaluate_directed_edge(u, v)
                if ed is None:
                    continue
                if ed.classification == EdgeClassification.REJECTED:
                    rejected.append(ed)
                else:
                    cand[_key(ed)] = ed

        for ids in _weak_components([e.event_id for e in work], cand):
            nodes = [emap[i] for i in ids]
            rej = [r for r in rejected if r.target_id in ids]
            if len(nodes) == 1:
                n = nodes[0]
                out.append(self._component(f"singleton_{n.event_id}", GraphComponentStatus.SINGLETON,
                                           n.event_id, nodes, [], [], rej, 0.0,
                                           ["No causal edges survived feasibility pass."]))
                continue
            sub_edges = [k for k in cand if k[0] in ids]
            in_edges = {v: [k for k in sub_edges if k[1] == v] for v in ids}
            all_edges = [cand[k] for k in sub_edges]
            explicit = sorted(n.event_id for n in nodes if n.is_explicit_root)
            zero_in = sorted(i for i in ids if not in_edges[i])
            if len(explicit) == 1:
                root = explicit[0]
            elif len(explicit) == 0 and len(zero_in) == 1:
                root = zero_in[0]
            else:
                out.append(self._component(f"unresolved_{min(ids)}", GraphComponentStatus.UNRESOLVED, None,
                                           nodes, [], all_edges, rej, 0.0,
                                           [f"Root feasibility failed. explicit={explicit} zero_in={zero_in}"]))
                continue
            # D1: the tree must hang from `root`.  The graph is a DAG (A2), so if
            # every node is reachable from root, root has no incoming edge (an
            # in-neighbour would be a descendant: a cycle) and every spanning
            # arborescence is rooted there.  Reachability is the whole check.
            unreachable = sorted(set(ids) - {root} - _descendants(sub_edges, root))
            if unreachable:
                out.append(self._component(f"unresolved_{root}", GraphComponentStatus.UNRESOLVED, None,
                                           nodes, [], all_edges, rej, 0.0,
                                           [f"EXPLICIT_ROOT_CONFLICT: {unreachable} not reachable from {root}"]))
                continue
            # Selection.  The candidate graph is a DAG (A2) and every node is
            # reachable from root, so ANY choice of one in-edge per non-root node
            # is a spanning arborescence, and the weight is a sum of independent
            # per-node terms: the maximum tree takes each node's best parent
            # (Edmonds' contraction step never fires on a DAG).  Ties resolve by
            # the canonical tuple (source_id, target_id, edge_type), and a tie
            # means the optimum is not unique: status AMBIGUOUS (paper, Inv. 5).
            sel, diags, tied = [], [], False
            for v in sorted(set(ids) - {root}):
                ins = sorted((cand[k] for k in in_edges[v]),
                             key=lambda e: (-e.weight, e.source_id, e.target_id, e.edge_type.value))
                sel.append(ins[0])
                rivals = [e.source_id for e in ins[1:] if e.weight == ins[0].weight]
                if rivals:
                    tied = True
                    diags.append(f"TIED_PARENT: {v} has equal-weight parents "
                                 f"{sorted([ins[0].source_id] + rivals)}; canonical choice {ins[0].source_id}.")
            sel_keys = {_key(e) for e in sel}
            disc = [cand[k] for k in sub_edges if k not in sel_keys]
            bott = min(e.weight for e in sel)
            all_acc = all(e.classification == EdgeClassification.ACCEPTED for e in sel)
            if not all_acc:
                diags.insert(0, "Selected edges contain unverified candidates.")
            status = (GraphComponentStatus.AMBIGUOUS if tied else
                      GraphComponentStatus.VERIFIED if all_acc else GraphComponentStatus.CANDIDATE)
            out.append(self._component(f"comp_{root}", status, root, nodes, sel, disc, rej, bott, diags))
        return out


# ---- D5: the artifact is produced by the code ----
def _edge_json(e: EdgeEvidence):
    return {"source_id": e.source_id, "target_id": e.target_id, "weight": e.weight,
            "edge_type": e.edge_type.value, "classification": e.classification.value,
            "ordering_basis": e.ordering_basis, "evidence_vector": e.evidence_vector}


def to_record(c: ForensicComponent) -> dict:
    return {
        "component_id": c.component_id, "status": c.status.value, "root_id": c.root_id,
        "component_confidence": c.component_confidence, "bottleneck_score": c.bottleneck_score,
        "mean_event_confidence": c.mean_event_confidence, "diagnostics": c.diagnostics,
        "selected_arborescence": [_edge_json(e) for e in c.selected_arborescence],
        "discarded_edges": [_edge_json(e) for e in c.discarded_edges],
        "rejected_edges": [_edge_json(e) for e in c.rejected_edges],
        "events": [{"event_id": e.event_id,
                    "timestamp": e.timestamp.isoformat() if e.timestamp else None,
                    "source_sequence": e.source_sequence, "transport_index": e.transport_index,
                    "role": e.role, "session_id": e.session_id,
                    "payload_integrity": e.payload_integrity.value,
                    "evidence_completeness": e.evidence_completeness.value,
                    "event_confidence": e.event_confidence, "graph_status": e.graph_status.value}
                   for e in c.events],
    }


def example_events():
    """The section IV scenario, with roles supplied so edges can be typed."""
    from datetime import timezone
    T = datetime(2026, 3, 8, 18, 0, 0, tzinfo=timezone.utc)
    return [
        TurnEvent("evt_301", T, source_sequence=1, transport_index=0, role="user",
                  session_id="sess_900", source="x", event_confidence=1.0),
        TurnEvent("evt_302", T, source_sequence=2, transport_index=1, role="user",
                  session_id="sess_900", source="x", event_confidence=0.90),
        TurnEvent("evt_303", T + timedelta(minutes=4, seconds=15), transport_index=2, role="model",
                  session_id="sess_900", source="x", event_confidence=0.95),
    ]


def example_json() -> str:
    comps = StrictForensicLinker().reconstruct(example_events())
    return json.dumps([to_record(c) for c in comps], indent=2, sort_keys=True) + "\n"


if __name__ == "__main__":
    print(example_json(), end="")
