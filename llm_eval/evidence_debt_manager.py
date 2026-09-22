from dataclasses import dataclass, field
from typing import Dict


@dataclass
class CategoryStats:
    compliance_mean: float
    variance: float
    sample_size: int
    invariant_violation_entropy: float
    local_lyapunov_estimate: float
    manifold_distance_mean: float


class EvidenceDebtManager:
    """
    Tracks fragility gradient across invariant categories.
    Debt is the accumulated evidence of structural deviation.
    """

    def __init__(self, decay: float = 0.9):
        self.decay = decay

    def update_debt_map(
        self,
        current_debt: Dict[str, float],
        stats: CategoryStats,
    ) -> Dict[str, float]:
        """
        Produces a new debt map from the current one plus the transition stats.
        Does not mutate current_debt.
        """
        updated = dict(current_debt)
        updated["compliance"]  = self.decay * updated.get("compliance", 0.0)  \
                                 + (1 - stats.compliance_mean)
        updated["entropy"]     = self.decay * updated.get("entropy", 0.0)     \
                                 + stats.invariant_violation_entropy
        updated["lyapunov"]    = self.decay * updated.get("lyapunov", 0.0)    \
                                 + stats.local_lyapunov_estimate
        updated["manifold"]    = self.decay * updated.get("manifold", 0.0)    \
                                 + stats.manifold_distance_mean
        return updated
