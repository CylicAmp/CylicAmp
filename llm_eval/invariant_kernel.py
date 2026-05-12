from dataclasses import dataclass
from typing import Dict, Any, Callable

from .evidence_debt_manager import EvidenceDebtManager, CategoryStats
from .transition_state import TransitionState


@dataclass
class ContractDecision:
    accepted: bool
    violations: list[str]
    integrity_delta: float
    debt_map_after: Dict[str, float] = None
    metadata: Dict[str, Any] = None


class InvariantExecutionKernel:
    """
    Invariants are the execution substrate itself.
    Every transition is invariant-conditioned.
    Debt is updated as part of the transition, not after it.
    """

    def __init__(
        self,
        invariants: Dict[str, Callable],
        debt_manager: EvidenceDebtManager,
    ):
        if not invariants:
            raise ValueError("InvariantExecutionKernel requires at least one invariant.")
        self.invariants = invariants
        self.debt_manager = debt_manager

    def transition(
        self,
        state: TransitionState,
        output: str,
        context: Dict = None,
    ) -> ContractDecision:
        """Single atomic state transition. Debt is updated as part of the transition."""
        ctx = context or {}

        # 1. Evaluate invariants
        eval_results = self.evaluate(state, output, ctx)
        violations = self.violation_vector(eval_results)
        delta = self._compute_integrity_delta(violations)

        # 2. Update debt (gradient of fragility) atomically with the transition
        stats = self._build_stats(state, violations, delta)
        updated_debt_map = self.debt_manager.update_debt_map(state.debt_map, stats)

        return ContractDecision(
            accepted=len(violations) == 0,
            violations=list(violations.keys()),
            integrity_delta=delta,
            debt_map_after=updated_debt_map,
            metadata={"raw_results": eval_results},
        )
        # Note: observer.broadcast() is the caller's responsibility.

    def evaluate(
        self,
        state: TransitionState,
        output: str,
        context: Dict,
    ) -> Dict[str, bool]:
        """Run each invariant; return {name: passed}."""
        return {
            name: fn(state, output, context)
            for name, fn in self.invariants.items()
        }

    def violation_vector(self, eval_results: Dict[str, bool]) -> Dict[str, bool]:
        """Return only the failed invariants."""
        return {name: v for name, v in eval_results.items() if not v}

    def _compute_integrity_delta(self, violations: Dict[str, bool]) -> float:
        """Negative delta per violation, normalised by invariant count."""
        return -len(violations) / len(self.invariants)

    def _build_stats(
        self,
        state: TransitionState,
        violations: Dict[str, bool],
        delta: float,
    ) -> CategoryStats:
        """
        Build CategoryStats for debt calculation from the current transition.
        Lyapunov and manifold fields are proxies pending LLE / manifold_distance
        integration.
        """
        violation_entropy = len(violations) / len(self.invariants)
        return CategoryStats(
            compliance_mean=1.0 if not violations else 0.0,
            variance=state.variance,
            sample_size=state.sample_size,
            invariant_violation_entropy=violation_entropy,
            local_lyapunov_estimate=abs(delta) * 1.5,   # proxy for divergence rate
            manifold_distance_mean=abs(delta) * 1.2,
        )
