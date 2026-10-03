#!/usr/bin/env python3
"""
JOY Investigative Analyzer — MSW Framework
===========================================
Applies the MSW mathematical constants to investigative data analysis:
  - Zeta-zero alignments for anomaly detection
  - Modular residues (mod 17) for hidden connection mapping
  - Shannon entropy for disorder measurement
  - JOY = φ³ · cos(2π t) resonance synthesis

Core formula:
  JOY = φ³ · L · W · C · cos(2π t) · V

Constants:
  φ  = (1 + √5) / 2   (golden ratio)
  φ³ = 4.236...
  TORSION_ANGLE = 108° (pentagon internal angle, φ-geometry)
  BASE_HARMONIC = 432  (memory saturation anchor, DR = 9)

© 2026 Michael Warren Song. All Rights Reserved.
"""

import numpy as np
import math
from typing import List, Dict

# ── Core constants ─────────────────────────────────────────────────────────

PHI            = (1 + math.sqrt(5)) / 2   # golden ratio ≈ 1.618
PHI_CUBED      = PHI ** 3                  # ≈ 4.236
TORSION_ANGLE  = 108.0                     # pentagon internal angle
BASE_HARMONIC  = 432.0                     # memory saturation (DR = 9)

# Riemann zeta zeros (imaginary parts of first non-trivial zeros)
ZETA_ZEROS = [14.135, 21.022, 25.011, 30.424, 43.327]

# Modular residue base from framework
MOD_BASE = 17


# ── Digital root (standalone) ──────────────────────────────────────────────

def digital_root(n):
    n = abs(int(n))
    if n == 0:
        return 0
    while n >= 10:
        n = sum(int(d) for d in str(n))
    return n


# ── JOY Investigative Analyzer ─────────────────────────────────────────────

class JOYInvestigator:
    """
    Investigative analyzer using MSW framework constants.

    Applies zeta-zero alignments, mod-17 residues, Shannon entropy,
    and φ³ resonance synthesis to detect patterns in arbitrary data.
    """

    def __init__(self):
        self.data = None
        self._raw  = None

    def load_data(self, data: List[float]):
        """Load a list of values for analysis."""
        self._raw  = data
        self.data  = np.array(data, dtype=float)
        return self

    # ── Anomaly detection ──────────────────────────────────────────────────

    def detect_anomalies(self, threshold: float = 0.001) -> Dict:
        """
        Detect values that deviate from zeta-zero alignment.

        Each data point is compared against the nearest zeta zero.
        Points within `threshold` are considered aligned; others are anomalous.
        """
        zeros = np.array(ZETA_ZEROS[:len(self.data)])
        if len(zeros) < len(self.data):
            # Cycle zeros if data is longer than the zero list
            zeros = np.tile(ZETA_ZEROS, math.ceil(len(self.data) / len(ZETA_ZEROS)))
            zeros = zeros[:len(self.data)]

        deviations  = np.abs(self.data - zeros)
        anomaly_idx = np.where(deviations > threshold)[0]
        aligned_idx = np.where(deviations <= threshold)[0]

        return {
            'anomaly_indices':  anomaly_idx.tolist(),
            'aligned_indices':  aligned_idx.tolist(),
            'deviations':       deviations.tolist(),
            'threshold':        threshold,
            'anomaly_count':    len(anomaly_idx),
            'alignment_ratio':  len(aligned_idx) / len(self.data),
        }

    # ── Connection mapping ─────────────────────────────────────────────────

    def find_connections(self, mod: int = MOD_BASE) -> Dict:
        """
        Group data by modular residue (default mod 17) to reveal hidden links.

        Points sharing a residue class are structurally connected
        in the mod-17 field.
        """
        int_data  = np.floor(np.abs(self.data)).astype(int)
        mod_res   = int_data % mod
        unique_res = np.unique(mod_res)

        connections = {}
        for res in unique_res:
            idxs = np.where(mod_res == res)[0].tolist()
            connections[int(res)] = {
                'indices': idxs,
                'values':  [self._raw[i] for i in idxs],
                'dr_of_residue': digital_root(int(res)),
            }

        return {
            'mod_base':    mod,
            'connections': connections,
            'unique_residues': unique_res.tolist(),
        }

    # ── Entropy measurement ────────────────────────────────────────────────

    def measure_entropy(self, bins: int = 10) -> Dict:
        """
        Shannon entropy of the data distribution.

        H = −Σ p_i · log₂(p_i)

        Entropy = 0: perfectly ordered (all same value)
        Entropy = log₂(bins): maximally disordered (uniform)
        """
        hist, edges = np.histogram(self.data, bins=bins)
        probs       = hist / hist.sum()
        entropy     = -np.sum(probs * np.log2(probs + 1e-10))
        max_entropy = math.log2(bins)

        return {
            'entropy':          round(float(entropy), 6),
            'max_entropy':      round(max_entropy, 6),
            'normalized':       round(float(entropy / max_entropy), 6),
            'disorder_level':   'high' if entropy > max_entropy * 0.7
                                else 'medium' if entropy > max_entropy * 0.3
                                else 'low',
            'bin_edges':        edges.tolist(),
            'bin_counts':       hist.tolist(),
        }

    # ── Resonance synthesis ────────────────────────────────────────────────

    def resonate_patterns(self, tolerance: float = 0.01) -> Dict:
        """
        Find data points that resonate with the JOY formula.

        JOY(t) = φ³ · cos(2π t)

        Points where |JOY(t) − data[t]| < tolerance are resonance matches.
        """
        t    = np.arange(len(self.data))
        joy  = PHI_CUBED * np.cos(2 * np.pi * t)
        diff = np.abs(joy - self.data)
        resonant_idx = np.where(diff < tolerance)[0]

        return {
            'joy_values':       joy.tolist(),
            'residuals':        diff.tolist(),
            'resonant_indices': resonant_idx.tolist(),
            'resonance_count':  len(resonant_idx),
            'phi_cubed':        round(PHI_CUBED, 6),
            'tolerance':        tolerance,
        }

    # ── Full report ────────────────────────────────────────────────────────

    def run(self, verbose: bool = True) -> Dict:
        """Run all analyses and return combined report."""
        if self.data is None:
            raise ValueError("No data loaded. Call load_data() first.")

        anomalies   = self.detect_anomalies()
        connections = self.find_connections()
        entropy     = self.measure_entropy()
        patterns    = self.resonate_patterns()

        if verbose:
            print("=" * 60)
            print("  JOY INVESTIGATIVE ANALYZER — MSW Framework")
            print("  © 2026 Michael Warren Song")
            print("=" * 60)
            print()
            print(f"  Data:         {self._raw}")
            print(f"  φ³ constant:  {PHI_CUBED:.6f}")
            print(f"  432 harmonic: {BASE_HARMONIC}  (DR={digital_root(int(BASE_HARMONIC))})")
            print()
            print(f"  ANOMALIES (threshold={anomalies['threshold']})")
            print(f"    Anomalous indices:  {anomalies['anomaly_indices']}")
            print(f"    Aligned indices:    {anomalies['aligned_indices']}")
            print(f"    Alignment ratio:    {anomalies['alignment_ratio']:.1%}")
            print()
            print(f"  CONNECTIONS (mod {connections['mod_base']})")
            for res, grp in connections['connections'].items():
                print(f"    residue {res:>2d} (DR={grp['dr_of_residue']}): "
                      f"indices {grp['indices']}  values {grp['values']}")
            print()
            print(f"  ENTROPY")
            print(f"    H = {entropy['entropy']}  (max={entropy['max_entropy']})")
            print(f"    Normalized: {entropy['normalized']:.1%}  — {entropy['disorder_level']} disorder")
            print()
            print(f"  RESONANCE (φ³ · cos(2π t))")
            print(f"    JOY values:       {[round(v,4) for v in patterns['joy_values']]}")
            print(f"    Resonant indices: {patterns['resonant_indices']}")
            print("=" * 60)

        return {
            'anomalies':   anomalies,
            'connections': connections,
            'entropy':     entropy,
            'patterns':    patterns,
        }


# ── Demo ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Default: zeta zeros as input (perfectly aligned to themselves)
    investigator = JOYInvestigator()
    investigator.load_data([14.135, 21.022, 25.011, 30.424, 43.327])
    investigator.run()

    print()
    print("  CUSTOM DATA EXAMPLE")
    print("  (replace with real investigative data)")
    investigator2 = JOYInvestigator()
    investigator2.load_data([419, 432, 851, 23, 37])
    investigator2.run()
