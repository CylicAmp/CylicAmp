#!/usr/bin/env python3
"""
mc_sensitivity_analyzer.py

Monte Carlo sensitivity validation engine as provided.
See mc_sensitivity_audit.py for the mathematical audit of this code.
"""

import re
import random
import math
import statistics
from typing import List, Dict, Any


class CascadeStructureAnalyzer:
    """
    Evaluates structural connections between empirical scales
    and a specific modular cyclic orbit sequence.
    """
    def __init__(self, modulus: int = 37):
        self.modulus = modulus
        # Standard base-2 multiplicative group orbit modulo 37
        self.orbit = [
            1, 2, 4, 8, 16, 32, 27, 17, 34, 31, 25, 13,
            26, 15, 30, 23, 9, 18, 36, 35, 33, 29, 21, 5,
            10, 20, 3, 6, 12, 24, 11, 22, 7, 14, 28, 19
        ]

    def analyze_scale_residency(self, deltas: List[float]) -> Dict[str, Any]:
        """Calculates scale remainder positions inside the modular field."""
        results = {}
        for dt in deltas:
            rounded_dt = int(round(dt))
            remainder = rounded_dt % self.modulus
            in_orbit = remainder in self.orbit
            results[str(dt)] = {
                "resolved_integer": rounded_dt,
                "remainder": remainder,
                "in_orbit": in_orbit,
                "orbit_position": self.orbit.index(remainder) if in_orbit else None
            }
        return results


class SensitivityValidationEngine:
    """
    Executes global sensitivity analysis and Monte Carlo simulations
    to quantify input uncertainty propagation and prevent selection bias.
    """
    @staticmethod
    def run_monte_carlo_audit(
        analyzer: CascadeStructureAnalyzer,
        base_deltas: List[float],
        sigma_noise: float = 0.5,
        iterations: int = 10000
    ) -> Dict[str, Any]:
        """
        Injects Gaussian white noise into input deltas over thousands of trials.
        Calculates the exact empirical probability of orbit residency.
        """
        total_elements_tested = len(base_deltas) * iterations
        orbit_hit_count = 0
        per_trial_densities = []

        if not base_deltas:
            return {"error": "Empty input delta vector"}

        for _ in range(iterations):
            trial_hits = 0
            perturbed_deltas = [d + random.gauss(0, sigma_noise) for d in base_deltas]
            trial_results = analyzer.analyze_scale_residency(perturbed_deltas)

            for res in trial_results.values():
                if res["in_orbit"]:
                    orbit_hit_count += 1
                    trial_hits += 1

            per_trial_densities.append(trial_hits / len(base_deltas))

        overall_empirical_probability = orbit_hit_count / total_elements_tested
        mean_density = statistics.mean(per_trial_densities)
        variance_density = statistics.variance(per_trial_densities) if len(per_trial_densities) > 1 else 0.0

        std_error = statistics.stdev(per_trial_densities) if len(per_trial_densities) > 1 else 0.0
        margin_of_error = 1.96 * (std_error / math.sqrt(iterations))

        return {
            "simulation_iterations": iterations,
            "injected_noise_sigma": sigma_noise,
            "empirical_hit_probability": round(overall_empirical_probability, 6),
            "mean_trial_density": round(mean_density, 6),
            "output_variance": round(variance_density, 6),
            "confidence_interval_95": {
                "lower_bound": round(mean_density - margin_of_error, 6),
                "upper_bound": round(mean_density + margin_of_error, 6)
            }
        }


class TextAuditorEngine:
    """Parses text strings for scientific claim bounds and sentiment metrics."""
    def __init__(self, text: str):
        self.text_lower = text.lower()

    def extract_metrics(self) -> Dict[str, Any]:
        metrics = {}
        base_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:-second|second|coherence)', self.text_lower)
        metrics["baseline_coherence_time"] = float(base_match.group(1)) if base_match else None

        max_match = re.search(r'(?:extended to|up to|about|reached)\s*(\d+(?:\.\d+?)?)', self.text_lower)
        metrics["max_coherence_time"] = float(max_match.group(1)) if max_match else None

        ion_match = re.search(r'(\d+)\s*(?:-ion|yb\+|qubit)', self.text_lower)
        metrics["qubit_count"] = int(ion_match.group(1)) if ion_match else None

        hype_words = ["unbreakable", "absolute immunity", "impenetrable", "revolutionary"]
        detected = [w for w in hype_words if w in self.text_lower]
        metrics["hyperbolic_count"] = len(detected)
        metrics["detected_hyperbole"] = detected

        pos = sum(1 for w in ["breakthrough", "robust", "stable"] if w in self.text_lower)
        neg = sum(1 for w in ["unstable", "failure", "fragile"] if w in self.text_lower)
        total = pos + neg
        metrics["sentiment_score"] = round((pos - neg) / total, 4) if total > 0 else 0.0

        return metrics


if __name__ == "__main__":
    core_analyzer = CascadeStructureAnalyzer(modulus=37)
    test_deltas = [12.0, 50.4, 120.1]

    print("=" * 70)
    print("        MWS MONTE CARLO RISK & SENSITIVITY VERIFICATION        ")
    print("=" * 70)

    simulation_report = SensitivityValidationEngine.run_monte_carlo_audit(
        analyzer=core_analyzer,
        base_deltas=test_deltas,
        sigma_noise=0.75,
        iterations=10000
    )

    print(f"Iterations Run       : {simulation_report['simulation_iterations']:,}")
    print(f"Noise Threshold (σ)  : {simulation_report['injected_noise_sigma']}")
    print(f"Empirical Probability: {simulation_report['empirical_hit_probability']:.4%}")
    print(f"Output Variance      : {simulation_report['output_variance']}")
    print(f"95% Bounds Interval  : [{simulation_report['confidence_interval_95']['lower_bound']} to {simulation_report['confidence_interval_95']['upper_bound']}]")
    print("=" * 70)
