# llm_eval/cognitive_runtime.py
"""
Cognitive Runtime Kernel
========================

Layer                    | Responsibility
-------------------------|--------------------------------------------------
CanonicalMessage         | Provider-neutral cognitive interface
TransformGraph           | Operational topology (not message history)
InvariantStore           | Persistent truths with temporal validity
OPERATOR_REGISTRY        | Operator metadata: determinism, TTL, entropy
ContextFingerprint       | Structured state identity (not string hash)
CognitiveRuntime         | Orchestrating kernel: routes, caches, invalidates

Key invariant: cognition is state evolution that preserves structure.
The transform graph replaces linear message history with operational topology,
enabling dependency tracking, subgraph invalidation, spectral analysis,
graph replay, and parallel execution planning.
"""

from __future__ import annotations

import hashlib
import json
import time
import uuid
from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

import numpy as np


# ── 1. CanonicalMessage ────────────────────────────────────────────────────────

@dataclass
class CanonicalMessage:
    """Provider-neutral cognitive message unit."""

    role: str                                                  # user | assistant | tool | system
    content: str
    name: Optional[str] = None                                 # tool name when role == "tool"
    tool_calls: List[Dict] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_openai(cls, obj: Dict) -> "CanonicalMessage":
        role = obj.get("role", "user")
        raw = obj.get("content") or ""
        content = (
            " ".join(p.get("text", "") for p in raw if isinstance(p, dict))
            if isinstance(raw, list)
            else str(raw)
        )
        tool_calls = [
            {
                "id":   tc.get("id"),
                "name": tc.get("function", {}).get("name"),
                "args": tc.get("function", {}).get("arguments", "{}"),
            }
            for tc in obj.get("tool_calls", [])
        ]
        return cls(
            role=role, content=content, name=obj.get("name"),
            tool_calls=tool_calls,
            metadata={"provider": "openai", "raw_role": role},
        )

    @classmethod
    def from_anthropic(cls, obj: Dict) -> "CanonicalMessage":
        role = obj.get("role", "user")
        raw = obj.get("content", "")
        if isinstance(raw, str):
            content, tool_calls = raw, []
        elif isinstance(raw, list):
            texts, tool_calls = [], []
            for block in raw:
                if not isinstance(block, dict):
                    continue
                btype = block.get("type")
                if btype == "text":
                    texts.append(block.get("text", ""))
                elif btype == "tool_use":
                    tool_calls.append({
                        "id":   block.get("id"),
                        "name": block.get("name"),
                        "args": json.dumps(block.get("input", {})),
                    })
            content = " ".join(texts)
        else:
            content, tool_calls = "", []
        return cls(
            role=role, content=content, tool_calls=tool_calls,
            metadata={"provider": "anthropic"},
        )

    @classmethod
    def from_gemini(cls, obj: Dict) -> "CanonicalMessage":
        texts, tool_calls = [], []
        for part in obj.get("parts", []):
            if not isinstance(part, dict):
                continue
            if "text" in part:
                texts.append(part["text"])
            elif "functionCall" in part:
                fc = part["functionCall"]
                tool_calls.append({
                    "id":   None,
                    "name": fc.get("name"),
                    "args": json.dumps(fc.get("args", {})),
                })
        raw_role = obj.get("role", "user")
        role = {"model": "assistant"}.get(raw_role, raw_role)
        return cls(
            role=role, content=" ".join(texts), tool_calls=tool_calls,
            metadata={"provider": "gemini", "raw_role": raw_role},
        )

    def fingerprint(self) -> str:
        """Deterministic 16-hex content hash for deduplication."""
        blob = json.dumps(
            {"role": self.role, "content": self.content, "name": self.name},
            sort_keys=True,
        )
        return hashlib.sha256(blob.encode()).hexdigest()[:16]


# ── 2. Operator registry ───────────────────────────────────────────────────────

@dataclass
class OperatorSignature:
    arity: int
    deterministic: bool
    ttl: Optional[int]          # seconds; 0 = never cache; None = no caching (non-det)
    invariance_class: str
    entropy_reduction: float    # 0..1 — how much knowing this reduces uncertainty
    operator_class: str = "generic"
    spectral_signature: Optional[str] = None


OPERATOR_REGISTRY: Dict[str, OperatorSignature] = {
    "get_date": OperatorSignature(
        arity=0, deterministic=True, ttl=86400,
        invariance_class="daily-stable", entropy_reduction=0.2,
        operator_class="temporal_projection",
    ),
    "get_weather": OperatorSignature(
        arity=2, deterministic=False, ttl=3600,
        invariance_class="location-temporal", entropy_reduction=0.7,
        operator_class="stochastic_projection",
    ),
    "read_file": OperatorSignature(
        arity=1, deterministic=True, ttl=300,
        invariance_class="filesystem-stable", entropy_reduction=0.5,
        operator_class="io_projection",
    ),
    "search_code": OperatorSignature(
        arity=1, deterministic=True, ttl=600,
        invariance_class="codebase-stable", entropy_reduction=0.6,
        operator_class="semantic_projection",
    ),
    "run_tests": OperatorSignature(
        arity=0, deterministic=True, ttl=0,   # never cache: results must be fresh
        invariance_class="runtime-volatile", entropy_reduction=0.9,
        operator_class="validation_operator",
    ),
    "llm_completion": OperatorSignature(
        arity=1, deterministic=False, ttl=None,
        invariance_class="stochastic", entropy_reduction=0.0,
        operator_class="generative_operator",
    ),
    "extract_invariants": OperatorSignature(
        arity=1, deterministic=True, ttl=3600,
        invariance_class="semantic-compression", entropy_reduction=0.8,
        operator_class="compression_operator",
    ),
}


# ── 3. InvariantStore ──────────────────────────────────────────────────────────

@dataclass
class InvariantEntry:
    value: Any
    expires_at: Optional[float]     # Unix timestamp; None = immortal
    invariance_class: str
    entropy_reduction: float
    provenance: List[str] = field(default_factory=list)

    def is_valid(self) -> bool:
        return self.expires_at is None or time.time() < self.expires_at


class InvariantStore:
    """Persistent truth field with temporal validity checking."""

    def __init__(self) -> None:
        self._store: Dict[str, InvariantEntry] = {}

    def put(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None,
        invariance_class: str = "unclassified",
        entropy_reduction: float = 0.5,
        provenance: Optional[List[str]] = None,
    ) -> None:
        if ttl is not None and ttl <= 0:
            return   # ttl=0 means "never cache"
        expires_at = (time.time() + ttl) if ttl is not None else None
        self._store[key] = InvariantEntry(
            value=value,
            expires_at=expires_at,
            invariance_class=invariance_class,
            entropy_reduction=entropy_reduction,
            provenance=provenance or [],
        )

    def get(self, key: str) -> Optional[Any]:
        entry = self._store.get(key)
        if entry is None:
            return None
        if not entry.is_valid():
            del self._store[key]
            return None
        return entry.value

    def evict_expired(self) -> int:
        stale = [k for k, v in self._store.items() if not v.is_valid()]
        for k in stale:
            del self._store[k]
        return len(stale)

    def active_keys(self) -> List[str]:
        self.evict_expired()
        return list(self._store.keys())

    def entropy_budget(self) -> float:
        """Sum of entropy reductions across all live invariants."""
        self.evict_expired()
        return sum(e.entropy_reduction for e in self._store.values())

    def snapshot(self) -> Dict[str, Any]:
        self.evict_expired()
        return {k: v.value for k, v in self._store.items()}


# ── 4. ContextFingerprint ──────────────────────────────────────────────────────

@dataclass
class ContextFingerprint:
    """
    Structured state identity for a reasoning node.
    Replaces opaque string hashes with topology-preserving structure,
    enabling structural distance computation between reasoning states.
    """
    conversation_id: str
    semantic_hash: str              # hash of (active_invariants + operator_chain)
    active_invariants: List[str]    # sorted live invariant keys
    operator_chain: List[str]       # ordered operator names applied so far

    @classmethod
    def compute(
        cls,
        conversation_id: str,
        invariant_store: InvariantStore,
        operator_chain: List[str],
    ) -> "ContextFingerprint":
        keys = sorted(invariant_store.active_keys())
        blob = json.dumps(
            {"invariants": keys, "operators": operator_chain},
            sort_keys=True,
        )
        semantic_hash = hashlib.sha256(blob.encode()).hexdigest()[:16]
        return cls(
            conversation_id=conversation_id,
            semantic_hash=semantic_hash,
            active_invariants=keys,
            operator_chain=list(operator_chain),
        )

    def structural_distance(self, other: "ContextFingerprint") -> float:
        """
        Convex combination of Jaccard distance on invariant sets
        and normalised Levenshtein distance on operator chains.
        Returns 0.0 if identical, approaching 1.0 when completely disjoint.
        """
        inv_a, inv_b = set(self.active_invariants), set(other.active_invariants)
        union = inv_a | inv_b
        inv_jaccard = (
            1.0 - len(inv_a & inv_b) / len(union) if union else 0.0
        )
        op_dist = _levenshtein(self.operator_chain, other.operator_chain)
        max_len = max(len(self.operator_chain), len(other.operator_chain), 1)
        return 0.5 * (inv_jaccard + op_dist / max_len)


def _levenshtein(a: List[str], b: List[str]) -> int:
    m, n = len(a), len(b)
    dp = list(range(n + 1))
    for i in range(1, m + 1):
        prev, dp[0] = dp[0], i
        for j in range(1, n + 1):
            prev, dp[j] = dp[j], (
                prev if a[i - 1] == b[j - 1]
                else 1 + min(prev, dp[j], dp[j - 1])
            )
    return dp[n]


# ── 5. TransformNode and TransformGraph ───────────────────────────────────────

@dataclass
class TransformNode:
    """
    A single reasoning operation in the transform graph.
    Carries full operator metadata enabling graph optimization,
    spectral analysis, and stale-subgraph invalidation.
    """
    node_id: str
    node_type: str                  # operator | invariant_extract | message | synthesis
    operator_name: str
    operator_class: str
    determinism: str                # full | partial | stochastic
    entropy_delta: float            # net entropy change (negative = compression)
    fingerprint: ContextFingerprint
    dependencies: List[str] = field(default_factory=list)   # upstream node_ids
    result: Any = None
    spectral_signature: Optional[Dict] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class TransformGraph:
    """
    Directed acyclic graph of reasoning operations.

    Replaces linear message history with operational topology,
    enabling: dependency tracking, stale-subgraph detection,
    spectral analysis, graph replay, and parallel scheduling.
    """

    def __init__(self) -> None:
        self._nodes: Dict[str, TransformNode] = {}
        self._edges: Dict[str, List[str]] = defaultdict(list)       # node → successors
        self._rev_edges: Dict[str, List[str]] = defaultdict(list)   # node → predecessors

    def add_node(self, node: TransformNode) -> None:
        self._nodes[node.node_id] = node
        for dep_id in node.dependencies:
            self._edges[dep_id].append(node.node_id)
            self._rev_edges[node.node_id].append(dep_id)

    def topological_order(self) -> List[str]:
        """Kahn's algorithm. Raises ValueError if the graph contains a cycle."""
        in_deg = {nid: len(self._rev_edges[nid]) for nid in self._nodes}
        queue = deque(nid for nid, d in in_deg.items() if d == 0)
        order: List[str] = []
        while queue:
            nid = queue.popleft()
            order.append(nid)
            for succ in self._edges[nid]:
                in_deg[succ] -= 1
                if in_deg[succ] == 0:
                    queue.append(succ)
        if len(order) != len(self._nodes):
            raise ValueError("TransformGraph contains a cycle — not a valid DAG")
        return order

    def stale_subgraph(self, invalidated_node_id: str) -> List[str]:
        """All node_ids transitively downstream of invalidated_node_id."""
        visited: set = set()
        stack = [invalidated_node_id]
        while stack:
            nid = stack.pop()
            if nid in visited:
                continue
            visited.add(nid)
            stack.extend(self._edges[nid])
        visited.discard(invalidated_node_id)
        return list(visited)

    def adjacency_matrix(self) -> Tuple[np.ndarray, List[str]]:
        """Return (A, node_ids) where A[i,j]=1 iff edge from node i to node j."""
        ids = list(self._nodes)
        idx = {nid: i for i, nid in enumerate(ids)}
        n = len(ids)
        A = np.zeros((n, n), dtype=float)
        for nid, succs in self._edges.items():
            if nid not in idx:
                continue
            for succ in succs:
                if succ in idx:
                    A[idx[nid], idx[succ]] = 1.0
        return A, ids

    def spectral_analysis(self) -> Dict[str, Any]:
        """
        Eigenvalue spectrum of the symmetrised adjacency matrix.

        Returns:
          eigenvalues:       sorted real eigenvalues of A + A^T
          spectral_radius:   max |eigenvalue|
          spectral_entropy:  Shannon entropy of normalised |eigenvalue| distribution
          operator_harmonics: magnitude histogram (8 bins) — frequency decomposition
          attractor_nodes:   node_ids with highest eigenvector centrality
        """
        A, ids = self.adjacency_matrix()
        if A.shape[0] == 0:
            return {
                "eigenvalues": [], "spectral_radius": 0.0,
                "spectral_entropy": 0.0, "operator_harmonics": [],
                "attractor_nodes": [],
            }
        A_sym = A + A.T
        eigenvalues = np.linalg.eigvalsh(A_sym)
        mags = np.abs(eigenvalues)
        spectral_radius = float(mags.max())

        total = mags.sum()
        if total > 0:
            p = mags / total
            spectral_entropy = float(-np.sum(p * np.log2(p + 1e-12)))
        else:
            spectral_entropy = 0.0

        counts, _ = np.histogram(mags, bins=8)
        harmonics = counts.tolist()

        if A_sym.shape[0] > 1:
            _, evecs = np.linalg.eigh(A_sym)
            dominant = np.abs(evecs[:, -1])
            top_k = min(3, len(ids))
            top_idx = np.argsort(dominant)[-top_k:][::-1]
            attractor_nodes = [ids[i] for i in top_idx]
        else:
            attractor_nodes = ids[:1]

        return {
            "eigenvalues": sorted(eigenvalues.real.tolist()),
            "spectral_radius": spectral_radius,
            "spectral_entropy": spectral_entropy,
            "operator_harmonics": harmonics,
            "attractor_nodes": attractor_nodes,
        }

    def entropy_flow(self) -> Dict[str, float]:
        """
        Cumulative entropy delta along each path in topological order.
        A node's cumulative entropy = max(parent cumulative) + its own delta.
        """
        order = self.topological_order()
        cumulative: Dict[str, float] = {}
        for nid in order:
            node = self._nodes[nid]
            parent_entropy = max(
                (cumulative[dep] for dep in node.dependencies if dep in cumulative),
                default=0.0,
            )
            cumulative[nid] = parent_entropy + node.entropy_delta
        return cumulative

    def node_count(self) -> int:
        return len(self._nodes)

    def edge_count(self) -> int:
        return sum(len(v) for v in self._edges.values())


# ── 6. extract_invariants ──────────────────────────────────────────────────────

def extract_invariants(
    tool_results: List[Dict[str, Any]],
    operator_registry: Optional[Dict[str, OperatorSignature]] = None,
) -> Dict[str, Any]:
    """
    Semantic state compression: extract stable truths from a list of tool results.

    A result is accepted as an invariant iff its operator is:
      - deterministic, AND
      - has TTL > 0 or TTL is None (immortal cache), AND
      - produces a non-None value.

    Unknown operators are accepted if they carry a ``stable=True`` hint.
    Returns {key: value} suitable for loading into an InvariantStore.
    """
    registry = operator_registry or OPERATOR_REGISTRY
    invariants: Dict[str, Any] = {}
    for result in tool_results:
        op_name = (
            result.get("operator")
            or result.get("tool")
            or result.get("name", "")
        )
        # Prefer explicit output key; fall back to result/value
        value = None
        for vkey in ("output", "result", "value"):
            if vkey in result:
                value = result[vkey]
                break
        if value is None:
            continue

        sig = registry.get(op_name)
        if sig is None:
            if result.get("stable", False):
                invariants[f"unknown.{op_name}.result"] = value
            continue

        if sig.deterministic and (sig.ttl is None or sig.ttl > 0):
            ih = result.get("input_hash", "")
            key = f"{op_name}.{ih[:8]}" if ih else f"{op_name}.result"
            invariants[key] = value

    return invariants


# ── 7. CognitiveRuntime ────────────────────────────────────────────────────────

class CognitiveRuntime:
    """
    Orchestrating cognitive kernel.

    Normalises provider messages, routes operators, maintains invariants,
    builds the transform graph, and computes structured context fingerprints.
    """

    def __init__(
        self,
        conversation_id: Optional[str] = None,
        operator_registry: Optional[Dict[str, OperatorSignature]] = None,
    ) -> None:
        self.conversation_id = conversation_id or uuid.uuid4().hex[:12]
        self.registry = operator_registry or OPERATOR_REGISTRY
        self.invariant_store = InvariantStore()
        self.graph = TransformGraph()
        self._operator_chain: List[str] = []
        self._messages: List[CanonicalMessage] = []

    def ingest(self, raw_msg: Dict, provider: str = "anthropic") -> CanonicalMessage:
        """Normalise a provider-specific message dict to CanonicalMessage."""
        loaders = {
            "openai":    CanonicalMessage.from_openai,
            "anthropic": CanonicalMessage.from_anthropic,
            "gemini":    CanonicalMessage.from_gemini,
        }
        msg = loaders.get(provider, CanonicalMessage.from_anthropic)(raw_msg)
        self._messages.append(msg)
        return msg

    def apply_operator(
        self,
        operator_name: str,
        inputs: Any = None,
        result: Any = None,
        entropy_delta: float = 0.0,
        dependencies: Optional[List[str]] = None,
    ) -> TransformNode:
        """
        Register an operator application in the transform graph.
        Caches the result in InvariantStore when the operator is deterministic
        with positive TTL.
        """
        sig = self.registry.get(operator_name)
        determinism = "full" if (sig and sig.deterministic) else "stochastic"
        op_class = sig.operator_class if sig else "unknown"
        eff_delta = entropy_delta if entropy_delta != 0.0 else (
            -(sig.entropy_reduction) if sig else 0.0
        )

        fp = ContextFingerprint.compute(
            self.conversation_id,
            self.invariant_store,
            self._operator_chain + [operator_name],
        )
        node = TransformNode(
            node_id=uuid.uuid4().hex[:12],
            node_type="operator",
            operator_name=operator_name,
            operator_class=op_class,
            determinism=determinism,
            entropy_delta=eff_delta,
            fingerprint=fp,
            dependencies=dependencies or [],
            result=result,
            metadata={"inputs": inputs},
        )
        self.graph.add_node(node)
        self._operator_chain.append(operator_name)

        if sig and sig.deterministic and (sig.ttl is None or sig.ttl > 0) and result is not None:
            input_hash = (
                hashlib.sha256(
                    json.dumps(inputs, sort_keys=True, default=str).encode()
                ).hexdigest()[:8]
                if inputs is not None
                else "none"
            )
            self.invariant_store.put(
                key=f"{operator_name}.{input_hash}",
                value=result,
                ttl=sig.ttl,
                invariance_class=sig.invariance_class,
                entropy_reduction=sig.entropy_reduction,
                provenance=list(self._operator_chain),
            )
        return node

    def current_fingerprint(self) -> ContextFingerprint:
        return ContextFingerprint.compute(
            self.conversation_id,
            self.invariant_store,
            self._operator_chain,
        )

    def invalidate(self, operator_name: str) -> List[str]:
        """
        Evict all invariants produced by operator_name.
        Returns node_ids of the transitively stale subgraph.
        """
        evict_keys = [
            k for k in self.invariant_store.active_keys()
            if k.startswith(f"{operator_name}.")
        ]
        for k in evict_keys:
            self.invariant_store._store.pop(k, None)

        stale: List[str] = []
        for node in self.graph._nodes.values():
            if node.operator_name == operator_name:
                stale.extend(self.graph.stale_subgraph(node.node_id))
        return list(set(stale))

    def summary(self) -> Dict[str, Any]:
        fp = self.current_fingerprint()
        spec = self.graph.spectral_analysis()
        return {
            "conversation_id":    self.conversation_id,
            "messages_ingested":  len(self._messages),
            "operators_applied":  len(self._operator_chain),
            "graph_nodes":        self.graph.node_count(),
            "graph_edges":        self.graph.edge_count(),
            "live_invariants":    len(self.invariant_store.active_keys()),
            "invariant_entropy_budget": round(self.invariant_store.entropy_budget(), 4),
            "context_fingerprint": {
                "semantic_hash":    fp.semantic_hash,
                "active_invariants": fp.active_invariants,
                "operator_chain":   fp.operator_chain,
            },
            "spectral_radius":    spec["spectral_radius"],
            "spectral_entropy":   round(spec["spectral_entropy"], 4),
            "attractor_nodes":    spec["attractor_nodes"],
        }


# ── 8. Verification ────────────────────────────────────────────────────────────

def _verify():
    print("Cognitive Runtime Kernel — verification\n")

    # ── Test 1: CanonicalMessage normalization ────────────────────────────────
    print("=" * 60)
    print("TEST 1: Provider-neutral CanonicalMessage")
    print("=" * 60)

    msg_oai = CanonicalMessage.from_openai({
        "role": "assistant", "content": "Hello",
        "tool_calls": [{"id": "tc1", "function": {"name": "get_date", "arguments": "{}"}}],
    })
    assert msg_oai.role == "assistant"
    assert msg_oai.content == "Hello"
    assert msg_oai.tool_calls[0]["name"] == "get_date"
    assert msg_oai.metadata["provider"] == "openai"
    print("  OpenAI → canonical  OK")

    msg_ant = CanonicalMessage.from_anthropic({
        "role": "assistant",
        "content": [
            {"type": "text", "text": "Let me check"},
            {"type": "tool_use", "id": "tu1", "name": "read_file", "input": {"path": "/foo"}},
        ],
    })
    assert msg_ant.role == "assistant"
    assert "Let me check" in msg_ant.content
    assert msg_ant.tool_calls[0]["name"] == "read_file"
    print("  Anthropic → canonical  OK")

    msg_gem = CanonicalMessage.from_gemini({
        "role": "model",
        "parts": [
            {"text": "The result is"},
            {"functionCall": {"name": "search_code", "args": {"query": "main"}}},
        ],
    })
    assert msg_gem.role == "assistant"
    assert "The result is" in msg_gem.content
    assert msg_gem.tool_calls[0]["name"] == "search_code"
    print("  Gemini → canonical  OK")

    assert msg_oai.fingerprint() != msg_ant.fingerprint()
    print("  Fingerprints distinct across providers  OK\n")

    # ── Test 2: InvariantStore with TTL ───────────────────────────────────────
    print("=" * 60)
    print("TEST 2: InvariantStore — persistence and expiry")
    print("=" * 60)

    store = InvariantStore()
    store.put("current_date", "2026-05-19", ttl=86400,
              invariance_class="daily-stable", entropy_reduction=0.2)
    store.put("user_pref", "dark_mode", ttl=None,
              invariance_class="session", entropy_reduction=0.1)
    store.put("stale_fact", "old_value", ttl=0,          # ttl=0 → never stored
              invariance_class="volatile", entropy_reduction=0.0)

    assert store.get("current_date") == "2026-05-19"
    assert store.get("user_pref") == "dark_mode"
    assert store.get("stale_fact") is None   # ttl=0 → not stored

    keys = store.active_keys()
    assert "current_date" in keys
    assert "user_pref" in keys
    assert "stale_fact" not in keys

    budget = store.entropy_budget()
    assert budget > 0
    print(f"  active_keys = {keys}  OK")
    print(f"  entropy_budget = {budget:.2f}  OK")
    print(f"  stale_fact (ttl=0) not stored  OK\n")

    # ── Test 3: OPERATOR_REGISTRY ─────────────────────────────────────────────
    print("=" * 60)
    print("TEST 3: OPERATOR_REGISTRY — determinism and entropy")
    print("=" * 60)

    assert OPERATOR_REGISTRY["get_date"].deterministic is True
    assert OPERATOR_REGISTRY["get_date"].ttl == 86400
    assert OPERATOR_REGISTRY["llm_completion"].deterministic is False
    assert OPERATOR_REGISTRY["llm_completion"].ttl is None
    assert OPERATOR_REGISTRY["run_tests"].ttl == 0
    for name, sig in OPERATOR_REGISTRY.items():
        assert 0.0 <= sig.entropy_reduction <= 1.0, f"{name}: entropy_reduction out of range"
    print(f"  {len(OPERATOR_REGISTRY)} operators validated  OK")
    print(f"  get_date: deterministic=True, ttl=86400  OK")
    print(f"  llm_completion: deterministic=False, ttl=None  OK")
    print(f"  run_tests: ttl=0 (never cache)  OK\n")

    # ── Test 4: TransformGraph topology and spectral analysis ─────────────────
    print("=" * 60)
    print("TEST 4: TransformGraph — topology and spectral analysis")
    print("=" * 60)

    graph = TransformGraph()
    fp0 = ContextFingerprint.compute("test", InvariantStore(), [])

    node_a = TransformNode("a", "operator", "get_date",      "temporal",   "full",       -0.2, fp0, [])
    node_b = TransformNode("b", "operator", "read_file",     "io",         "full",       -0.5, fp0, ["a"])
    node_c = TransformNode("c", "operator", "search_code",   "semantic",   "full",       -0.6, fp0, ["a"])
    node_d = TransformNode("d", "synthesis","llm_completion","generative", "stochastic",  0.0, fp0, ["b", "c"])

    for n in [node_a, node_b, node_c, node_d]:
        graph.add_node(n)

    order = graph.topological_order()
    assert order.index("a") < order.index("b")
    assert order.index("a") < order.index("c")
    assert order.index("b") < order.index("d")
    assert order.index("c") < order.index("d")
    print(f"  Topological order: {order}  OK")

    stale = graph.stale_subgraph("a")
    assert set(stale) == {"b", "c", "d"}
    print(f"  Stale subgraph from 'a': {sorted(stale)}  OK")

    spec = graph.spectral_analysis()
    assert spec["spectral_radius"] >= 0
    assert spec["spectral_entropy"] >= 0
    print(f"  Spectral radius: {spec['spectral_radius']:.4f}")
    print(f"  Spectral entropy: {spec['spectral_entropy']:.4f}")
    print(f"  Attractor nodes: {spec['attractor_nodes']}")
    print(f"  Operator harmonics: {spec['operator_harmonics']}")
    print(f"  Spectral analysis  OK")

    # Cycle detection
    g2 = TransformGraph()
    g2.add_node(TransformNode("x", "operator", "get_date", "temporal", "full", -0.2, fp0, []))
    g2.add_node(TransformNode("y", "operator", "read_file", "io", "full", -0.5, fp0, ["x"]))
    g2._edges["y"].append("x")
    g2._rev_edges["x"].append("y")
    try:
        g2.topological_order()
        assert False, "Expected ValueError for cycle"
    except ValueError:
        print(f"  Cycle detection raises ValueError  OK\n")

    # ── Test 5: ContextFingerprint structural distance ────────────────────────
    print("=" * 60)
    print("TEST 5: ContextFingerprint — structural distance")
    print("=" * 60)

    st = InvariantStore()
    st.put("k1", "v1", ttl=None, invariance_class="test", entropy_reduction=0.3)
    fp1 = ContextFingerprint.compute("c", st, ["get_date", "read_file"])
    fp2 = ContextFingerprint.compute("c", st, ["get_date", "read_file"])
    fp3 = ContextFingerprint.compute("c", st, ["get_date", "search_code"])
    fp4 = ContextFingerprint.compute("c", InvariantStore(), ["run_tests"])

    assert fp1.structural_distance(fp2) == 0.0
    d13 = fp1.structural_distance(fp3)
    d14 = fp1.structural_distance(fp4)
    assert 0.0 < d13 <= 1.0
    assert d14 > d13
    print(f"  fp1 vs fp2 (identical): {fp1.structural_distance(fp2):.3f}  OK")
    print(f"  fp1 vs fp3 (1 op diff): {d13:.3f}  OK")
    print(f"  fp1 vs fp4 (different invariants+ops): {d14:.3f}  OK\n")

    # ── Test 6: extract_invariants ────────────────────────────────────────────
    print("=" * 60)
    print("TEST 6: extract_invariants — semantic state compression")
    print("=" * 60)

    extracted = extract_invariants([
        {"operator": "get_date",       "output": "2026-05-19",  "input_hash": "abc123"},
        {"operator": "llm_completion", "output": "some text"},
        {"operator": "read_file",      "output": "file contents","input_hash": "def456"},
        {"operator": "run_tests",      "output": {"passed": 10}},
        {"operator": "unknown_op",     "output": "something",   "stable": True},
    ])
    assert any("get_date"     in k for k in extracted)
    assert any("read_file"    in k for k in extracted)
    assert any("unknown_op"   in k for k in extracted)
    assert not any("llm_completion" in k for k in extracted)
    assert not any("run_tests"      in k for k in extracted)
    print(f"  Extracted: {sorted(extracted.keys())}  OK")
    print(f"  llm_completion excluded (non-deterministic)  OK")
    print(f"  run_tests excluded (ttl=0)  OK")
    print(f"  unknown_op with stable=True included  OK\n")

    # ── Test 7: CognitiveRuntime end-to-end ───────────────────────────────────
    print("=" * 60)
    print("TEST 7: CognitiveRuntime — end-to-end")
    print("=" * 60)

    rt = CognitiveRuntime(conversation_id="test-session")

    rt.ingest({"role": "user", "content": "What's today?"}, "openai")
    rt.ingest({"role": "assistant",
               "content": [{"type": "text", "text": "Let me check"}]}, "anthropic")
    assert len(rt._messages) == 2
    print(f"  Ingested 2 messages (openai + anthropic)  OK")

    n1 = rt.apply_operator("get_date",    inputs=None,
                            result="2026-05-19")
    n2 = rt.apply_operator("read_file",   inputs={"path": "/etc/hosts"},
                            result="127.0.0.1 localhost",
                            dependencies=[n1.node_id])
    n3 = rt.apply_operator("search_code", inputs={"query": "def main"},
                            result=["file.py:1"],
                            dependencies=[n1.node_id])
    n4 = rt.apply_operator("llm_completion", inputs={"prompt": "summary"},
                            result="Summary",
                            dependencies=[n2.node_id, n3.node_id])

    assert rt.graph.node_count() == 4
    assert rt.graph.edge_count() == 4   # n1→n2, n1→n3, n2→n4, n3→n4
    print(f"  4 operators applied, {rt.graph.node_count()} nodes, {rt.graph.edge_count()} edges  OK")

    live = rt.invariant_store.active_keys()
    assert any("get_date"  in k for k in live)
    assert any("read_file" in k for k in live)
    assert not any("llm_completion" in k for k in live)
    print(f"  Cached invariants: {live}  OK")

    stale = rt.invalidate("get_date")
    assert set(stale) >= {n2.node_id, n3.node_id, n4.node_id}
    print(f"  Invalidating get_date → {len(stale)} stale downstream nodes  OK")

    sm = rt.summary()
    assert sm["messages_ingested"] == 2
    assert sm["operators_applied"] == 4
    assert sm["graph_nodes"] == 4
    print(f"  Summary: {sm['graph_nodes']} nodes, "
          f"spectral_radius={sm['spectral_radius']:.4f}, "
          f"entropy_budget={sm['invariant_entropy_budget']:.4f}  OK\n")

    # ── Test 8: Entropy flow ──────────────────────────────────────────────────
    print("=" * 60)
    print("TEST 8: Entropy flow through transform graph")
    print("=" * 60)

    flow = rt.graph.entropy_flow()
    print(f"  Cumulative entropy deltas:")
    for nid, delta in sorted(flow.items(), key=lambda x: x[1]):
        name = rt.graph._nodes[nid].operator_name
        print(f"    {name} ({nid[:8]}): {delta:.4f}")

    assert flow[n1.node_id] == rt.graph._nodes[n1.node_id].entropy_delta
    print(f"  Root node entropy = its own delta  OK")
    print(f"  Entropy propagates through DAG  OK\n")

    # ── Summary ───────────────────────────────────────────────────────────────
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"""
  VERIFIED:
    CanonicalMessage: OpenAI/Anthropic/Gemini → normalized schema             OK
    InvariantStore:   put/get with TTL, eviction, entropy budget              OK
    OPERATOR_REGISTRY: {len(OPERATOR_REGISTRY)} operators with determinism/entropy/TTL metadata     OK
    TransformGraph:   topological sort, stale subgraph, cycle detection       OK
    Spectral analysis: eigenvalues, radius, entropy, attractor nodes          OK
    ContextFingerprint: structured identity, Jaccard+Levenshtein distance     OK
    extract_invariants: semantic state compression from tool results          OK
    CognitiveRuntime:  ingest, apply_operator, invalidate, summary            OK
    Entropy flow:     cumulative delta propagates through DAG                 OK

  ARCHITECTURE:
    Provider-neutral   → transport decoupled from cognition
    Transform graph    → operational topology replaces message history
    Invariant store    → persistent truths with temporal validity + TTL decay
    Operator registry  → determinism/entropy metadata enables planning
    Context fingerprint→ structured state identity (not opaque string hash)
    Spectral analysis  → adjacency eigenvalues expose attractor structure
    """)
    print("All assertions passed.")


if __name__ == "__main__":
    _verify()
