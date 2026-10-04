from dataclasses import dataclass, field
from typing import Dict


@dataclass
class TransitionState:
    """
    Input to a single invariant-conditioned transition.
    Carries the current debt map and any variance/sample metadata
    needed to compute CategoryStats.
    """
    debt_map: Dict[str, float] = field(default_factory=dict)
    variance: float = 0.0
    sample_size: int = 1
