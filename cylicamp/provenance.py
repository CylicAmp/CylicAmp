from enum import Enum, auto
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime


class Domain(Enum):
    MATHEMATICS = auto()
    PHYSICS = auto()
    LOGIC = auto()
    KNOWLEDGE_GRAPH = auto()
    SCIENTIFIC_LITERATURE = auto()
    NATURAL_LANGUAGE = auto()
    METAPHYSICAL = auto()


class Modality(Enum):
    ASSERTION = auto()
    HYPOTHESIS = auto()
    QUESTION = auto()
    NEGATION = auto()


class SourceType(Enum):
    PUBLISHED_PAPER = auto()
    INTERNAL_DERIVATION = auto()
    DATASET = auto()
    HARDCODED_CONSTANT = auto()
    USER_INPUT = auto()


@dataclass(frozen=True)
class Provenance:
    source_id: str
    source_type: SourceType
    retrieval_method: str
    timestamp: datetime
    hash: str
    citation: str


@dataclass
class Claim:
    proposition: str
    domain: Domain
    modality: Modality
    entities: List[str] = field(default_factory=list)
    predicates: List[str] = field(default_factory=list)
    provenance: Optional[Provenance] = None


@dataclass
class InferenceStep:
    rule: str
    premises: List[Claim]
    conclusion: Claim
    engine: str


@dataclass
class Evidence:
    source: Provenance
    relevance: float
    excerpt: Optional[str] = None


@dataclass
class Derivation:
    conclusion: Claim
    premises: List[Claim]
    inference_steps: List[InferenceStep]
    assumptions: List[Claim]
    evidence: List[Evidence]
    reproducible: bool
    soundness_checked: bool
    confidence: Optional[float] = None
    limitations: List[str] = field(default_factory=list)

    @property
    def is_verified(self) -> bool:
        return (
            self.soundness_checked and
            self.reproducible and
            len(self.assumptions) == 0 and
            all(p.provenance is not None for p in self.premises)
        )
