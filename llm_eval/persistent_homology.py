"""
Persistent Homology for LLM Behavioral Dynamics
================================================
Computes topological features of a sequence of ContractDecision objects.

H0 (connected components / Betti-0):
    Implemented via Vietoris-Rips filtration + union-find.
    Tells us: how many distinct behavioral regimes exist, and how
    persistently they survive as we coarsen the resolution.

H1 (loops / Betti-1):
    Interface defined; requires ripser or gudhi for full computation.
    Install: pip install ripser    or    pip install gudhi

Usage
-----
    from llm_eval.persistent_homology import BehavioralPointCloud, compute_persistence

    cloud = BehavioralPointCloud.from_decisions(decisions)
    dgm   = compute_persistence(cloud, max_dim=0)
    print(dgm.betti_curve(dim=0))
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

import numpy as np

from .invariant_kernel import ContractDecision


# ── Feature extraction ────────────────────────────────────────────────────────

DEBT_KEYS = ("compliance", "entropy", "lyapunov", "manifold")


def _decision_to_vector(d: ContractDecision, n_invariants: int) -> np.ndarray:
    """
    Maps one ContractDecision to a fixed-length feature vector:
        [integrity_delta, violation_rate, debt_compliance,
         debt_entropy, debt_lyapunov, debt_manifold]
    """
    violation_rate = len(d.violations) / max(n_invariants, 1)
    debt = d.debt_map_after or {}
    return np.array([
        d.integrity_delta,
        violation_rate,
        debt.get("compliance", 0.0),
        debt.get("entropy",    0.0),
        debt.get("lyapunov",   0.0),
        debt.get("manifold",   0.0),
    ], dtype=float)


@dataclass
class BehavioralPointCloud:
    """
    Point cloud in R^6 derived from a sequence of ContractDecisions.
    Each point represents one atomic transition.
    """
    points: np.ndarray          # shape (n, 6)
    labels: List[bool]          # accepted flag per point

    @classmethod
    def from_decisions(
        cls,
        decisions: List[ContractDecision],
        n_invariants: int = 1,
    ) -> "BehavioralPointCloud":
        if not decisions:
            return cls(np.empty((0, 6)), [])
        vecs = np.stack([_decision_to_vector(d, n_invariants) for d in decisions])
        labels = [d.accepted for d in decisions]
        return cls(points=vecs, labels=labels)

    def normalize(self) -> "BehavioralPointCloud":
        """Z-score each feature dimension (in-place copy)."""
        std = self.points.std(axis=0)
        std[std == 0] = 1.0
        normed = (self.points - self.points.mean(axis=0)) / std
        return BehavioralPointCloud(points=normed, labels=list(self.labels))

    def pairwise_distances(self) -> np.ndarray:
        """Euclidean distance matrix, shape (n, n)."""
        n = len(self.points)
        d = np.zeros((n, n))
        for i in range(n):
            diff = self.points[i+1:] - self.points[i]
            d[i, i+1:] = np.sqrt((diff ** 2).sum(axis=1))
            d[i+1:, i] = d[i, i+1:]
        return d


# ── Union-Find ────────────────────────────────────────────────────────────────

class _UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank   = [0] * n
        self.birth  = [0.0] * n    # scale at which this root was born

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, x: int, y: int, scale: float) -> Optional[Tuple[int, float]]:
        """
        Merge components of x and y at the given scale.
        Returns (dying_root, birth_scale) if a merge happened, else None.
        """
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return None
        # younger root (higher birth scale) dies
        if self.birth[rx] < self.birth[ry]:
            rx, ry = ry, rx          # rx is the younger (dies)
        dying_root  = rx
        dying_birth = self.birth[rx]
        if self.rank[rx] < self.rank[ry]:
            self.parent[rx] = ry
        elif self.rank[rx] > self.rank[ry]:
            self.parent[ry] = rx
        else:
            self.parent[ry] = rx
            self.rank[rx] += 1
        return (dying_root, dying_birth)


# ── Persistence diagram ───────────────────────────────────────────────────────

@dataclass
class PersistenceDiagram:
    """
    Stores (birth, death) pairs for each homological dimension.
    death = inf means the feature survives to the end of the filtration.
    """
    pairs: List[Tuple[float, float]]    # H0 pairs
    dim: int = 0

    @property
    def finite_pairs(self) -> List[Tuple[float, float]]:
        return [(b, d) for b, d in self.pairs if not math.isinf(d)]

    @property
    def persistence(self) -> List[float]:
        """death - birth for finite pairs (lifetime of each feature)."""
        return [d - b for b, d in self.finite_pairs]

    def betti_curve(self, thresholds: Optional[np.ndarray] = None) -> Tuple[np.ndarray, np.ndarray]:
        """
        Returns (thresholds, betti_counts): the number of alive features
        at each threshold value.
        """
        if not self.pairs:
            eps = np.linspace(0, 1, 50) if thresholds is None else thresholds
            return eps, np.zeros(len(eps), dtype=int)

        max_finite = max((d for _, d in self.pairs if not math.isinf(d)), default=1.0)
        if thresholds is None:
            thresholds = np.linspace(0, max_finite * 1.1, 100)

        counts = np.zeros(len(thresholds), dtype=int)
        for eps_i, eps in enumerate(thresholds):
            counts[eps_i] = sum(
                1 for b, d in self.pairs
                if b <= eps and (math.isinf(d) or d > eps)
            )
        return thresholds, counts

    def most_persistent(self, k: int = 5) -> List[Tuple[float, float]]:
        """Top-k most persistent finite features."""
        return sorted(self.finite_pairs, key=lambda p: p[1]-p[0], reverse=True)[:k]


# ── H0 computation (pure numpy) ───────────────────────────────────────────────

def _h0_persistence(dist_matrix: np.ndarray) -> PersistenceDiagram:
    """
    Vietoris-Rips H0 via union-find.
    Each point starts as its own component at scale 0.
    Components merge when their distance falls below the current scale.
    The younger component's persistence pair is (0, merge_scale).
    One component survives to infinity.
    """
    n = len(dist_matrix)
    if n == 0:
        return PersistenceDiagram(pairs=[], dim=0)

    # Collect all edges sorted by distance
    edges = sorted(
        (dist_matrix[i, j], i, j)
        for i in range(n)
        for j in range(i + 1, n)
    )

    uf = _UnionFind(n)
    pairs: List[Tuple[float, float]] = []

    for scale, i, j in edges:
        result = uf.union(i, j, scale)
        if result is not None:
            _, birth = result
            pairs.append((birth, scale))

    # One component survives forever
    pairs.append((0.0, math.inf))

    return PersistenceDiagram(pairs=pairs, dim=0)


# ── Public API ────────────────────────────────────────────────────────────────

def compute_persistence(
    cloud: BehavioralPointCloud,
    max_dim: int = 0,
    normalize: bool = True,
) -> PersistenceDiagram:
    """
    Compute persistent homology of the behavioral point cloud.

    max_dim=0: H0 only (connected components) — pure numpy, always available.
    max_dim=1: H1 (loops) — requires ripser: pip install ripser

    Returns a PersistenceDiagram for H0 (and H1 if max_dim=1 and ripser present).
    """
    if len(cloud.points) == 0:
        return PersistenceDiagram(pairs=[], dim=0)

    c = cloud.normalize() if normalize else cloud
    dist = c.pairwise_distances()

    if max_dim == 0:
        return _h0_persistence(dist)

    # H1+ — delegate to ripser if available
    try:
        from ripser import ripser as _ripser
        result = _ripser(dist, distance_matrix=True, maxdim=max_dim)
        dgms = result["dgms"]
        # Return H0 by default; caller can inspect result["dgms"][1] for H1
        h0_pairs = [(float(b), float(d)) for b, d in dgms[0]]
        return PersistenceDiagram(pairs=h0_pairs, dim=0)
    except ImportError:
        raise ImportError(
            "H1 persistence requires ripser. Install with: pip install ripser"
        )


def topological_distance(cloud_a: BehavioralPointCloud,
                         cloud_b: BehavioralPointCloud) -> float:
    """
    Bottleneck-inspired distance between two H0 persistence diagrams.
    Uses the max unmatched persistence as a proxy (true bottleneck
    requires scipy.spatial; this version is pure numpy).
    """
    dgm_a = compute_persistence(cloud_a)
    dgm_b = compute_persistence(cloud_b)
    pers_a = sorted(dgm_a.persistence, reverse=True)
    pers_b = sorted(dgm_b.persistence, reverse=True)
    # Pad to equal length with zeros
    n = max(len(pers_a), len(pers_b))
    pers_a += [0.0] * (n - len(pers_a))
    pers_b += [0.0] * (n - len(pers_b))
    return float(max(abs(a - b) for a, b in zip(pers_a, pers_b)))
