"""
metric_space_abstraction.py

MetricSpaceAbstractionLayer — per SEED_60 architectural decision.

Decision: DO_NOT_MERGE_ONTOLOGIES
  SEED_59  (severity_trigger_risk_scoring)   and
  SNAKE_SET_3X3_9X9 (grid_similarity_closure_system)
  share score-space [0,1] but NOT semantics, thresholds, or calibration.

Integration rules enforced here:
  rule_1: NO_SHARED_THRESHOLDS_ACROSS_DOMAINS
  rule_2: NO_SHARED_CALIBRATION_PARAMETERS
  rule_3: NO_CROSS_INTERPRETATION_OF_SCORE_SEMANTICS
  rule_4: ONLY_SHARE_INFRASTRUCTURE_LAYER_IF_ISOMORPHIC

The only shared layer is this file: a typed, domain-isolated interface.
"""

from __future__ import annotations

import abc
import dataclasses
import enum
from typing import Any, Dict, Final, FrozenSet, Optional


# ---------------------------------------------------------------------------
# Domain registry — closed enum prevents accidental cross-domain wiring
# ---------------------------------------------------------------------------

class Domain(str, enum.Enum):
    SEED_59    = "severity_trigger_risk_scoring"
    SNAKE_GRID = "grid_similarity_closure_system"


# ---------------------------------------------------------------------------
# Score token — carries domain tag so misuse raises at call-site
# ---------------------------------------------------------------------------

@dataclasses.dataclass(frozen=True)
class DomainScore:
    """
    Opaque score wrapper.  Consumers MUST check .domain before interpreting
    the value; cross-domain comparison raises DomainMismatchError (rule_3).
    """
    domain: Domain
    value: float           # always in [0, 1]
    metadata: Dict[str, Any] = dataclasses.field(default_factory=dict)

    def __post_init__(self) -> None:
        if not (0.0 <= self.value <= 1.0):
            raise ValueError(f"DomainScore.value must be in [0,1], got {self.value!r}")

    def __eq__(self, other: object) -> bool:
        if isinstance(other, DomainScore):
            if self.domain != other.domain:
                raise DomainMismatchError(
                    f"Cannot compare scores across domains: "
                    f"{self.domain.value!r} vs {other.domain.value!r}"
                )
            return self.value == other.value
        return NotImplemented

    def __lt__(self, other: "DomainScore") -> bool:
        if self.domain != other.domain:
            raise DomainMismatchError(
                f"Cannot order scores across domains: "
                f"{self.domain.value!r} vs {other.domain.value!r}"
            )
        return self.value < other.value


class DomainMismatchError(TypeError):
    """Raised when cross-domain score semantics are accidentally mixed (rule_3)."""


# ---------------------------------------------------------------------------
# Abstract metric space — rule_1 + rule_2 via isolated calibration blocks
# ---------------------------------------------------------------------------

class MetricSpaceProtocol(abc.ABC):
    """
    Each domain subclasses this.  Calibration state is instance-local;
    there is no class-level shared state (rule_2).
    """

    @property
    @abc.abstractmethod
    def domain(self) -> Domain:
        """Declare which domain this metric space belongs to."""

    @property
    @abc.abstractmethod
    def threshold(self) -> Optional[float]:
        """
        Domain-local threshold.  Must NOT be read by any other domain (rule_1).
        Exposed only for same-domain consumers via the typed accessor below.
        """

    @abc.abstractmethod
    def score(self, raw_state: Dict[str, Any]) -> DomainScore:
        """
        Map raw_domain_state → DomainScore.
        Must be deterministic and side-effect-free.
        """

    def score_above_threshold(self, raw_state: Dict[str, Any]) -> bool:
        """Threshold comparison — valid only within the owning domain (rule_1)."""
        t = self.threshold
        if t is None:
            raise ValueError(f"{self.__class__.__name__} has no configured threshold")
        return self.score(raw_state).value > t


# ---------------------------------------------------------------------------
# SEED_59 domain implementation
# ---------------------------------------------------------------------------

@dataclasses.dataclass
class Seed59Config:
    """Calibration parameters private to SEED_59 (rule_2)."""
    # Elevated-signal boundary per SEED_60 threshold_analysis_0_45
    elevated_signal_threshold: float = 0.45
    weight_severity: float = 0.6
    weight_frequency: float = 0.4


class Seed59MetricSpace(MetricSpaceProtocol):
    """
    Domain: severity_trigger_risk_scoring
    Score semantics: probabilistic risk intensity in [0, 1].
    Threshold 0.45 is valid ONLY within this domain.
    """

    def __init__(self, config: Optional[Seed59Config] = None) -> None:
        self._config = config or Seed59Config()

    @property
    def domain(self) -> Domain:
        return Domain.SEED_59

    @property
    def threshold(self) -> float:
        return self._config.elevated_signal_threshold

    def score(self, raw_state: Dict[str, Any]) -> DomainScore:
        """
        Expected keys: severity (float [0,1]), frequency (float [0,1]).
        Returns weighted linear combination as probabilistic risk intensity.
        """
        severity  = float(raw_state["severity"])
        frequency = float(raw_state["frequency"])

        if not (0.0 <= severity <= 1.0 and 0.0 <= frequency <= 1.0):
            raise ValueError("SEED_59 inputs must be in [0,1]")

        value = (self._config.weight_severity * severity
                 + self._config.weight_frequency * frequency)

        return DomainScore(
            domain=self.domain,
            value=round(min(max(value, 0.0), 1.0), 10),
            metadata={
                "severity": severity,
                "frequency": frequency,
                "threshold": self.threshold,
                "above_threshold": value > self.threshold,
            },
        )


# ---------------------------------------------------------------------------
# SNAKE_SET_3X3_9X9 domain implementation
# ---------------------------------------------------------------------------

@dataclasses.dataclass
class SnakeGridConfig:
    """Calibration parameters private to SNAKE_SET (rule_2)."""
    grid_sizes: FrozenSet[int] = dataclasses.field(
        default_factory=lambda: frozenset({3, 9})
    )
    closure_weight: float = 0.7
    path_weight: float = 0.3
    # No 0.45 threshold — that belongs to SEED_59 (rule_1)
    closure_threshold: float = 0.72


class SnakeGridMetricSpace(MetricSpaceProtocol):
    """
    Domain: grid_similarity_closure_system (3×3, 9×9 snake grids).
    Score semantics: structural/graph closure metric in [0, 1].
    Threshold 0.45 does NOT apply here (rule_1).
    """

    def __init__(self, config: Optional[SnakeGridConfig] = None) -> None:
        self._config = config or SnakeGridConfig()

    @property
    def domain(self) -> Domain:
        return Domain.SNAKE_GRID

    @property
    def threshold(self) -> float:
        return self._config.closure_threshold

    def score(self, raw_state: Dict[str, Any]) -> DomainScore:
        """
        Expected keys: closure_ratio (float [0,1]), path_similarity (float [0,1]),
                       grid_size (int, must be in config.grid_sizes).
        Returns weighted structural closure metric.
        """
        grid_size       = int(raw_state["grid_size"])
        closure_ratio   = float(raw_state["closure_ratio"])
        path_similarity = float(raw_state["path_similarity"])

        if grid_size not in self._config.grid_sizes:
            raise ValueError(
                f"grid_size {grid_size} not in configured sizes "
                f"{self._config.grid_sizes}"
            )
        if not (0.0 <= closure_ratio <= 1.0 and 0.0 <= path_similarity <= 1.0):
            raise ValueError("SnakeGrid inputs must be in [0,1]")

        value = (self._config.closure_weight * closure_ratio
                 + self._config.path_weight * path_similarity)

        return DomainScore(
            domain=self.domain,
            value=round(min(max(value, 0.0), 1.0), 10),
            metadata={
                "grid_size": grid_size,
                "closure_ratio": closure_ratio,
                "path_similarity": path_similarity,
                "threshold": self.threshold,
                "above_threshold": value > self.threshold,
            },
        )


# ---------------------------------------------------------------------------
# Registry — the only shared infrastructure (rule_4: isomorphic interface)
# ---------------------------------------------------------------------------

class MetricSpaceAbstractionLayer:
    """
    Central registry.  Enforces domain isolation at registration time.
    Consumers call .score(domain, raw_state); they cannot reach across domains.
    """

    def __init__(self) -> None:
        self._spaces: Dict[Domain, MetricSpaceProtocol] = {}

    def register(self, space: MetricSpaceProtocol) -> None:
        if space.domain in self._spaces:
            raise ValueError(
                f"Domain {space.domain!r} already registered. "
                "Replace explicitly with .replace()."
            )
        self._spaces[space.domain] = space

    def replace(self, space: MetricSpaceProtocol) -> None:
        """Explicitly replace a registered metric space (e.g. for recalibration)."""
        self._spaces[space.domain] = space

    def score(self, domain: Domain, raw_state: Dict[str, Any]) -> DomainScore:
        space = self._spaces.get(domain)
        if space is None:
            raise KeyError(f"Domain {domain!r} not registered")
        return space.score(raw_state)

    def above_threshold(self, domain: Domain, raw_state: Dict[str, Any]) -> bool:
        """Threshold query — always domain-local (rule_1)."""
        space = self._spaces.get(domain)
        if space is None:
            raise KeyError(f"Domain {domain!r} not registered")
        return space.score_above_threshold(raw_state)

    def registered_domains(self) -> FrozenSet[Domain]:
        return frozenset(self._spaces)
