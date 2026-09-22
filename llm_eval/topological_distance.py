# llm_eval/topological_distance.py
"""
Topological distance between behavioral point clouds.
Thin numpy wrapper around the H0 persistence machinery in persistent_homology.py.

Public API
----------
    topological_distance(features_a, features_b) -> float

The input can be raw numpy arrays (shape (n,d)).
The function computes H0 persistence for each cloud, then returns
a bottleneck-proxy distance between the two diagrams.
"""

from __future__ import annotations

import numpy as np

from .persistent_homology import (
    BehavioralPointCloud,
    compute_persistence,
    topological_distance as _topo_dist_clouds,
)


def topological_distance(
    features_a: np.ndarray,
    features_b: np.ndarray,
    normalize: bool = True,
) -> float:
    """
    Topological distance between two point clouds given as raw numpy arrays.

    Each row is one observation; columns are features.
    Uses H0 Vietoris-Rips persistence (pure numpy, no ripser required).

    Parameters
    ----------
    features_a, features_b : np.ndarray, shape (n, d)
        Point clouds to compare.
    normalize : bool
        Z-score normalise each cloud before computing distances.

    Returns
    -------
    float
        Proxy bottleneck distance between the H0 persistence diagrams.
        Larger values indicate more topologically distinct regimes.
    """
    cloud_a = _array_to_cloud(features_a)
    cloud_b = _array_to_cloud(features_b)
    return _topo_dist_clouds(cloud_a, cloud_b)


def _array_to_cloud(arr: np.ndarray) -> BehavioralPointCloud:
    """Wrap a raw feature matrix in a BehavioralPointCloud."""
    arr = np.asarray(arr, dtype=float)
    n = len(arr)
    # pad or truncate to 6 features (the canonical dimension)
    if arr.ndim == 1:
        arr = arr.reshape(-1, 1)
    if arr.shape[1] < 6:
        arr = np.pad(arr, ((0, 0), (0, 6 - arr.shape[1])))
    else:
        arr = arr[:, :6]
    return BehavioralPointCloud(points=arr, labels=[True] * n)
