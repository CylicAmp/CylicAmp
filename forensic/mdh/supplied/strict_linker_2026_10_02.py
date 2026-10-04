"""Supplied 2026-10-02, verbatim: StrictForensicLinker ("closed operational engine").
Audited in forensic/mdh/supplied/audit_strict_linker_2026_10_02.py. Not imported by the pipeline."""
import html
import re
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Optional
import networkx as nx

# --- Formal State Lattices ---

class PayloadIntegrity(str, Enum):
    COMPLETE = "COMPLETE"
    PARTIAL = "PARTIAL"
    TRUNCATED = "TRUNCATED"
    MALFORMED = "MALFORMED"

    def __lt__(self, other: "PayloadIntegrity") -> bool:
        order = [self.MALFORMED, self.TRUNCATED, self.PARTIAL, self.COMPLETE]
        return order.index(self) < order.index(other)

    def __le__(self, other: "PayloadIntegrity") -> bool:
        return self == other or self < other

class EvidenceCompleteness(str, Enum):
    SUFFICIENT = "SUFFICIENT"
    PARTIAL = "PARTIAL"
    FRAGMENTED = "FRAGMENTED"
    EMPTY = "EMPTY"

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
    SINGLETON = "SINGLETON"
    UNRESOLVED = "UNRESOLVED"
    QUARANTINED = "QUARANTINED"

# --- Models ---

@dataclass
class FieldEvidence:
    value: str
    source_field: str
    raw_value: Any
    transformations: list[str] = field(default_factory=list)

@dataclass
class TurnEvent:
    event_id: str
    timestamp: Optional[datetime]
    source_sequence: Optional[int] = None       # Explicit protocol/chunk sequence
    transport_index: int = 0                    # Raw serialization array index
    prompt: Optional[FieldEvidence] = None
    response: Optional[FieldEvidence] = None
    session_id: Optional[str] = None
    is_explicit_root: bool = False
    source: str = "unknown"

    payload_integrity: PayloadIntegrity = PayloadIntegrity.COMPLETE
    evidence_completeness: EvidenceCompleteness = EvidenceCompleteness.SUFFICIENT
    event_confidence: float = 0.0
    graph_status: GraphComponentStatus = GraphComponentStatus.UNRESOLVED

    provenance: dict[str, Any] = field(default_factory=dict)
    diagnostics: list[str] = field(default_factory=list)
    raw_ref: Any = field(default_factory=dict)

@dataclass
class EdgeEvidence:
    source_id: str
    target_id: str
    weight: float
    edge_type: EdgeType
    classification: EdgeClassification
    evidence_vector: dict[str, Optional[float]]
    ordering_basis: str

@dataclass
class ForensicComponent:
    component_id: str
    status: GraphComponentStatus
    root_id: Optional[str]
    events: list[TurnEvent]
    selected_arborescence: list[EdgeEvidence]
    discarded_edges: list[EdgeEvidence]
    bottleneck_score: float
    mean_event_confidence: float
    component_confidence: float
    diagnostics: list[str] = field(default_factory=list)

# --- Engine ---

class StrictForensicLinker:
    def __init__(
        self,
        horizon_minutes: int = 45,
        accept_threshold: float = 0.70,
        ambiguous_threshold: float = 0.35,
        weight_epsilon: float = 1.0
    ):
        self.horizon = timedelta(minutes=horizon_minutes)
        self.accept_thresh = accept_threshold
        self.ambig_thresh = ambiguous_threshold
        self.epsilon = weight_epsilon

    def _determine_causal_order(self, u: TurnEvent, v: TurnEvent) -> tuple[bool, str, EdgeType]:
        """Enforces distinction: timestamp order != transport order != causal order."""
        if not u.timestamp or not v.timestamp:
            return False, "missing_timestamps", EdgeType.UNKNOWN

        # Case 1: Strict temporal order
        if u.timestamp < v.timestamp:
            # Check delta within horizon
            if (v.timestamp - u.timestamp) > self.horizon:
                return False, "temporal_horizon_exceeded", EdgeType.UNKNOWN
            return True, "strict_timestamp_order", EdgeType.CAUSAL_REPLY

        # Case 2: Equal timestamps (Tie-breaking analysis)
        if u.timestamp == v.timestamp:
            # Only valid if an explicit protocol/chunk sequence was supplied by source
            if u.source_sequence is not None and v.source_sequence is not None:
                if u.source_sequence < v.source_sequence:
                    return True, "protocol_sequence_continuity", EdgeType.FRAGMENT_CONTINUATION
                return False, "inverted_or_duplicate_protocol_sequence", EdgeType.UNKNOWN

            # Array serialization index alone does NOT establish causality
            return False, "equal_timestamp_unprovenanced_transport_index", EdgeType.UNKNOWN

        return False, "chronologically_inverted", EdgeType.UNKNOWN

    def evaluate_directed_edge(self, u: TurnEvent, v: TurnEvent) -> Optional[EdgeEvidence]:
        if u.event_id == v.event_id:
            return None

        has_causality, basis, edge_type = self._determine_causal_order(u, v)
        if not has_causality:
            return None

        # Rule: Conflicting metadata immediately invalidates candidate
        if u.session_id and v.session_id and u.session_id != v.session_id:
            return EdgeEvidence(
                source_id=u.event_id,
                target_id=v.event_id,
                weight=0.0,
                edge_type=edge_type,
                classification=EdgeClassification.REJECTED,
                evidence_vector={"session_match": -1.0},
                ordering_basis=basis
            )

        vector: dict[str, Optional[float]] = {
            "session_match": None,
            "temporal_affinity": None,
            "source_cohesion": None
        }

        # Epistemic Rule: Missing metadata is neutral (0.0 contribution)
        if u.session_id and v.session_id and u.session_id == v.session_id:
            vector["session_match"] = 1.0

        delta = v.timestamp - u.timestamp
        ratio = delta.total_seconds() / self.horizon.total_seconds()
        affinity = float((1.0 - ratio) ** 2.0) if ratio <= 1.0 else 0.0
        vector["temporal_affinity"] = round(affinity, 3)

        if u.source == v.source and u.source != "unknown":
            vector["source_cohesion"] = 0.05

        # Edge score formulation
        if vector["session_match"] == 1.0:
            score = min(1.0, 0.75 + (0.20 * affinity) + (vector["source_cohesion"] or 0.0))
        else:
            score = (affinity * 0.50) + (vector["source_cohesion"] or 0.0)

        score = round(score, 3)

        if score >= self.accept_thresh:
            classification = EdgeClassification.ACCEPTED
        elif score >= self.ambig_thresh:
            classification = EdgeClassification.AMBIGUOUS
        else:
            classification = EdgeClassification.REJECTED

        return EdgeEvidence(
            source_id=u.event_id,
            target_id=v.event_id,
            weight=score,
            edge_type=edge_type,
            classification=classification,
            evidence_vector=vector,
            ordering_basis=basis
        )

    def reconstruct(self, events: list[TurnEvent]) -> list[ForensicComponent]:
        components: list[ForensicComponent] = []
        event_map = {e.event_id: e for e in events}

        # 1. Quarantine corrupted payloads and isolate singletons lacking timestamps
        workable_events: list[TurnEvent] = []
        for e in events:
            if e.payload_integrity == PayloadIntegrity.MALFORMED:
                e.graph_status = GraphComponentStatus.QUARANTINED
                components.append(ForensicComponent(
                    component_id=f"quarantine_{e.event_id}",
                    status=GraphComponentStatus.QUARANTINED,
                    root_id=e.event_id,
                    events=[e],
                    selected_arborescence=[],
                    discarded_edges=[],
                    bottleneck_score=0.0,
                    mean_event_confidence=0.0,
                    component_confidence=0.0,
                    diagnostics=["Payload malformed: Quarantined at deframer/parser boundary."]
                ))
            elif not e.timestamp:
                e.graph_status = GraphComponentStatus.SINGLETON
                components.append(ForensicComponent(
                    component_id=f"singleton_{e.event_id}",
                    status=GraphComponentStatus.SINGLETON,
                    root_id=None,
                    events=[e],
                    selected_arborescence=[],
                    discarded_edges=[],
                    bottleneck_score=0.0,
                    mean_event_confidence=e.event_confidence,
                    component_confidence=0.0,
                    diagnostics=["Missing timestamp: Causally unanchored."]
                ))
            else:
                workable_events.append(e)

        # 2. Build candidate causal DAG
        candidate_dag = nx.DiGraph()
        candidate_edges: dict[tuple[str, str], EdgeEvidence] = {}

        for e in workable_events:
            candidate_dag.add_node(e.event_id)

        for i in range(len(workable_events)):
            for j in range(len(workable_events)):
                if i == j:
                    continue
                edge = self.evaluate_directed_edge(workable_events[i], workable_events[j])
                if edge and edge.classification in (EdgeClassification.ACCEPTED, EdgeClassification.AMBIGUOUS):
                    candidate_dag.add_edge(edge.source_id, edge.target_id, weight=edge.weight)
                    candidate_edges[(edge.source_id, edge.target_id)] = edge

        # 3. Partition across weakly connected components
        for component_node_ids in list(nx.weakly_connected_components(candidate_dag)):
            node_list = [event_map[nid] for nid in component_node_ids]

            if len(node_list) == 1:
                node = node_list[0]
                node.graph_status = GraphComponentStatus.SINGLETON
                components.append(ForensicComponent(
                    component_id=f"singleton_{node.event_id}",
                    status=GraphComponentStatus.SINGLETON,
                    root_id=node.event_id,
                    events=[node],
                    selected_arborescence=[],
                    discarded_edges=[],
                    bottleneck_score=0.0,
                    mean_event_confidence=node.event_confidence,
                    component_confidence=0.0,
                    diagnostics=["No causal edges survived feasibility pass."]
                ))
                continue

            sub_dag: nx.DiGraph = candidate_dag.subgraph(component_node_ids).copy()

            # Root feasibility pass
            explicit_roots = [n for n in node_list if n.is_explicit_root]
            in_degree_zero = [n.event_id for n in node_list if sub_dag.in_degree(n.event_id) == 0]

            selected_root: Optional[str] = None
            if len(explicit_roots) == 1:
                selected_root = explicit_roots[0].event_id
            elif len(in_degree_zero) == 1:
                selected_root = in_degree_zero[0]
            else:
                for n in node_list:
                    n.graph_status = GraphComponentStatus.UNRESOLVED
                components.append(ForensicComponent(
                    component_id=f"unresolved_{node_list[0].event_id}",
                    status=GraphComponentStatus.UNRESOLVED,
                    root_id=None,
                    events=node_list,
                    selected_arborescence=[],
                    discarded_edges=[candidate_edges[e] for e in sub_dag.edges()],
                    bottleneck_score=0.0,
                    mean_event_confidence=sum(n.event_confidence for n in node_list) / len(node_list),
                    component_confidence=0.0,
                    diagnostics=[f"Root feasibility failed. Candidate zero-in-degree nodes: {in_degree_zero}"]
                ))
                continue

            # 4. Mathematically Exact Edmonds Weight Inversion
            # Let M = max(w) + epsilon. Then w'(e) = M - w(e) >= epsilon > 0
            max_w = max(d["weight"] for _, _, d in sub_dag.edges(data=True))
            M = max_w + self.epsilon

            inverted_dag = nx.DiGraph()
            for u, v, d in sub_dag.edges(data=True):
                inverted_dag.add_edge(u, v, weight=M - d["weight"])

            try:
                arborescence = nx.minimum_spanning_arborescence(inverted_dag, attr="weight")
            except nx.NetworkXException as err:
                for n in node_list:
                    n.graph_status = GraphComponentStatus.UNRESOLVED
                components.append(ForensicComponent(
                    component_id=f"unresolved_{node_list[0].event_id}",
                    status=GraphComponentStatus.UNRESOLVED,
                    root_id=selected_root,
                    events=node_list,
                    selected_arborescence=[],
                    discarded_edges=[candidate_edges[e] for e in sub_dag.edges()],
                    bottleneck_score=0.0,
                    mean_event_confidence=sum(n.event_confidence for n in node_list) / len(node_list),
                    component_confidence=0.0,
                    diagnostics=[f"Arborescence optimization failed: {str(err)}"]
                ))
                continue

            if len(arborescence.edges) != len(node_list) - 1:
                for n in node_list:
                    n.graph_status = GraphComponentStatus.UNRESOLVED
                components.append(ForensicComponent(
                    component_id=f"unresolved_{node_list[0].event_id}",
                    status=GraphComponentStatus.UNRESOLVED,
                    root_id=selected_root,
                    events=node_list,
                    selected_arborescence=[],
                    discarded_edges=[candidate_edges[e] for e in sub_dag.edges()],
                    bottleneck_score=0.0,
                    mean_event_confidence=sum(n.event_confidence for n in node_list) / len(node_list),
                    component_confidence=0.0,
                    diagnostics=["Topological shortfall: Extracted edges do not form a spanning tree."]
                ))
                continue

            # Separate Selected Arborescence from Discarded Candidate Edges
            selected_set = set(arborescence.edges())
            selected_edges = [candidate_edges[e] for e in selected_set]
            discarded_edges = [candidate_edges[e] for e in sub_dag.edges() if e not in selected_set]

            bottleneck = min(e.weight for e in selected_edges) if selected_edges else 0.0
            all_accepted = all(e.classification == EdgeClassification.ACCEPTED for e in selected_edges)

            final_status = GraphComponentStatus.VERIFIED if all_accepted else GraphComponentStatus.CANDIDATE
            for n in node_list:
                n.graph_status = final_status

            mean_conf = sum(n.event_confidence for n in node_list) / len(node_list)
            # Epistemic Invariant: C_component <= min(bottleneck, mean_event_confidence)
            comp_conf = round(min(bottleneck, mean_conf), 3)

            components.append(ForensicComponent(
                component_id=f"comp_{selected_root}",
                status=final_status,
                root_id=selected_root,
                events=node_list,
                selected_arborescence=selected_edges,
                discarded_edges=discarded_edges,
                bottleneck_score=bottleneck,
                mean_event_confidence=round(mean_conf, 3),
                component_confidence=comp_conf,
                diagnostics=[] if all_accepted else ["Selected edges contain unverified candidates."]
            ))

        return components


# --- Supplied tests, verbatim ---

def test_equal_timestamp_without_sequence_fails():
    """Asserts that serialization order alone does not manufacture an edge."""
    linker = StrictForensicLinker()
    t0 = datetime(2026, 3, 8, 12, 0, 0)

    # Two records with identical timestamps and no protocol sequence
    e1 = TurnEvent("e1", timestamp=t0, transport_index=0, session_id="s1")
    e2 = TurnEvent("e2", timestamp=t0, transport_index=1, session_id="s1")

    # Neither directed orientation may yield a valid edge
    assert linker.evaluate_directed_edge(e1, e2) is None
    assert linker.evaluate_directed_edge(e2, e1) is None

    results = linker.reconstruct([e1, e2])
    # Must yield two singletons, not a connected conversation
    assert len(results) == 2
    assert results[0].status == GraphComponentStatus.SINGLETON
    assert results[1].status == GraphComponentStatus.SINGLETON

def test_equal_timestamp_with_sequence_succeeds():
    """Asserts that explicit protocol sequence enables causal reconstruction."""
    linker = StrictForensicLinker()
    t0 = datetime(2026, 3, 8, 12, 0, 0)

    e1 = TurnEvent("e1", timestamp=t0, source_sequence=1, session_id="s1", event_confidence=1.0)
    e2 = TurnEvent("e2", timestamp=t0, source_sequence=2, session_id="s1", event_confidence=1.0)

    edge = linker.evaluate_directed_edge(e1, e2)
    assert edge is not None
    assert edge.edge_type == EdgeType.FRAGMENT_CONTINUATION
    assert edge.ordering_basis == "protocol_sequence_continuity"

    results = linker.reconstruct([e1, e2])
    assert len(results) == 1
    assert results[0].status == GraphComponentStatus.VERIFIED
    assert results[0].root_id == "e1"

def test_exact_edmonds_weight_inversion():
    """Confirms that dynamic M = max(w) + epsilon selects the exact maximum-weight tree."""
    linker = StrictForensicLinker(weight_epsilon=0.5)
    t0 = datetime(2026, 3, 8, 12, 0, 0)

    e1 = TurnEvent("e1", timestamp=t0, is_explicit_root=True, session_id="s1")
    e2 = TurnEvent("e2", timestamp=t0 + timedelta(minutes=1), session_id="s1")
    e3 = TurnEvent("e3", timestamp=t0 + timedelta(minutes=2), session_id="s1")
    e4 = TurnEvent("e4", timestamp=t0 + timedelta(minutes=3), session_id="s1")

    linker.evaluate_directed_edge = lambda u, v: {
        ("e1", "e2"): EdgeEvidence("e1", "e2", 0.9, EdgeType.CAUSAL_REPLY, EdgeClassification.ACCEPTED, {}, "t"),
        ("e1", "e3"): EdgeEvidence("e1", "e3", 0.7, EdgeType.CAUSAL_REPLY, EdgeClassification.ACCEPTED, {}, "t"),
        ("e2", "e4"): EdgeEvidence("e2", "e4", 0.4, EdgeType.CAUSAL_REPLY, EdgeClassification.ACCEPTED, {}, "t"),
        ("e3", "e4"): EdgeEvidence("e3", "e4", 0.8, EdgeType.CAUSAL_REPLY, EdgeClassification.ACCEPTED, {}, "t"),
    }.get((u.event_id, v.event_id))

    results = linker.reconstruct([e1, e2, e3, e4])
    comp = results[0]
    selected_pairs = {(e.source_id, e.target_id) for e in comp.selected_arborescence}

    assert selected_pairs == {("e1", "e2"), ("e1", "e3"), ("e3", "e4")}
    assert ("e2", "e4") in {(e.source_id, e.target_id) for e in comp.discarded_edges}
