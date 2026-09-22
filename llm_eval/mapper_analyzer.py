# llm_eval/mapper_analyzer.py
"""
Mapper-style topological analysis of behavioral point clouds.

Implements a lightweight 1-D Mapper (no external TDA library required):
  1. Project points onto a scalar lens (first principal component or debt axis).
  2. Cover the lens range with overlapping intervals.
  3. Cluster each partial preimage (k-means, k=1..3).
  4. Build the nerve: nodes = clusters, edges = non-empty intersections.

The output is a graph suitable for force-directed visualisation.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import numpy as np


# ── K-means (pure numpy) ──────────────────────────────────────────────────────

def _kmeans(X: np.ndarray, k: int, n_iter: int = 30) -> np.ndarray:
    """Assign rows of X to k clusters; returns integer label array."""
    if len(X) <= k:
        return np.arange(len(X))
    rng = np.random.default_rng(0)
    centres = X[rng.choice(len(X), k, replace=False)]
    labels = np.zeros(len(X), dtype=int)
    for _ in range(n_iter):
        dists = np.stack([((X - c) ** 2).sum(axis=1) for c in centres])
        labels = dists.argmin(axis=0)
        new_centres = np.array([
            X[labels == j].mean(axis=0) if (labels == j).any() else centres[j]
            for j in range(k)
        ])
        if np.allclose(centres, new_centres):
            break
        centres = new_centres
    return labels


# ── Mapper graph ──────────────────────────────────────────────────────────────

@dataclass
class MapperNode:
    id: int
    indices: List[int]          # row indices of points in this node
    centroid: np.ndarray
    regime_label: str = "unknown"
    mean_debt: float = 0.0


@dataclass
class MapperGraph:
    nodes: List[MapperNode] = field(default_factory=list)
    edges: List[Tuple[int, int]] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "nodes": [
                {
                    "id": n.id,
                    "size": len(n.indices),
                    "regime": n.regime_label,
                    "mean_debt": round(n.mean_debt, 4),
                    "centroid": n.centroid.tolist(),
                }
                for n in self.nodes
            ],
            "edges": [{"source": u, "target": v} for u, v in self.edges],
        }


# ── Mapper algorithm ──────────────────────────────────────────────────────────

def run_mapper(
    features: np.ndarray,
    lens_values: Optional[np.ndarray] = None,
    n_intervals: int = 10,
    overlap: float = 0.4,
    max_k: int = 2,
    regime_labels: Optional[List[str]] = None,
    debt_values: Optional[np.ndarray] = None,
) -> MapperGraph:
    """
    1-D Mapper on a feature matrix.

    Parameters
    ----------
    features      : (n, d) float array
    lens_values   : (n,) scalar lens; defaults to first PCA component
    n_intervals   : number of cover intervals
    overlap       : fractional overlap between adjacent intervals (0..1)
    max_k         : maximum clusters per preimage bin (auto-selects 1..max_k)
    regime_labels : per-point regime strings for node annotation
    debt_values   : per-point debt values for node annotation

    Returns
    -------
    MapperGraph
    """
    n = len(features)
    if n == 0:
        return MapperGraph()

    # Lens: project onto first PC if not provided
    if lens_values is None:
        centered = features - features.mean(axis=0)
        cov = centered.T @ centered / max(n - 1, 1)
        _, vecs = np.linalg.eigh(cov)
        lens_values = centered @ vecs[:, -1]

    lo, hi = lens_values.min(), lens_values.max()
    span = hi - lo if hi > lo else 1.0
    step = span / n_intervals
    half_overlap = step * overlap / 2

    # Build bins
    node_id = 0
    nodes: List[MapperNode] = []
    bin_to_nodes: Dict[int, List[int]] = {}   # bin_index → list of node ids

    for b in range(n_intervals):
        left  = lo + b * step - half_overlap
        right = lo + (b + 1) * step + half_overlap
        mask  = (lens_values >= left) & (lens_values <= right)
        idx   = np.where(mask)[0]
        if len(idx) == 0:
            continue

        pts = features[idx]
        k = min(max_k, len(idx))
        labels = _kmeans(pts, k) if k > 1 else np.zeros(len(idx), dtype=int)

        bin_nodes = []
        for c in range(k):
            c_idx = idx[labels == c]
            if len(c_idx) == 0:
                continue
            centroid = features[c_idx].mean(axis=0)

            regime = "unknown"
            if regime_labels is not None:
                from collections import Counter
                regime = Counter(regime_labels[i] for i in c_idx).most_common(1)[0][0]

            mean_d = 0.0
            if debt_values is not None:
                mean_d = float(debt_values[c_idx].mean())

            nodes.append(MapperNode(
                id=node_id,
                indices=c_idx.tolist(),
                centroid=centroid,
                regime_label=regime,
                mean_debt=mean_d,
            ))
            bin_nodes.append(node_id)
            node_id += 1
        bin_to_nodes[b] = bin_nodes

    # Edges: adjacent bins that share points (Mapper nerve)
    edges: List[Tuple[int, int]] = []
    seen = set()
    for b, b_nodes in bin_to_nodes.items():
        next_b = b + 1
        if next_b not in bin_to_nodes:
            continue
        for u in b_nodes:
            for v in bin_to_nodes[next_b]:
                u_set = set(nodes[u].indices)
                v_set = set(nodes[v].indices)
                if u_set & v_set and (u, v) not in seen:
                    edges.append((u, v))
                    seen.add((u, v))

    return MapperGraph(nodes=nodes, edges=edges)
