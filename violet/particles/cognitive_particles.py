"""
Cognitive Particles
===================
The fundamental cognitive objects of the CPE universe.
All particles are probabilistic quantum objects until observed.
"""

from __future__ import annotations

import uuid
import time
import math
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from core.constants import (
    N_DIMENSIONS, GAMMA_DECAY, TAU_MEMORY,
    COGNITIVE_PLANCK, CognitiveDimension
)


class ParticleType(Enum):
    MEMORYON = auto()
    EVIDON = auto()
    HYPOTHEON = auto()
    REASONON = auto()
    EMERGON = auto()       # Emerged from string resonance
    DARKON = auto()        # Dark matter cognitive particle (inferred)


class QuantumState(Enum):
    SUPERPOSITION = auto()   # Multiple states coexist
    COLLAPSED = auto()       # Observed, definite state
    ENTANGLED = auto()       # Linked to another particle
    DORMANT = auto()         # Below energy threshold
    EXTINCT = auto()         # Energy = 0, historical record only


@dataclass
class DimensionalVector:
    """
    8-dimensional cognitive space vector.
    Dimensions: truth, time, novelty, utility, risk,
                confidence, influence, intent
    """
    values: np.ndarray = field(default_factory=lambda: np.zeros(N_DIMENSIONS))

    def __post_init__(self):
        if not isinstance(self.values, np.ndarray):
            self.values = np.array(self.values, dtype=float)
        self.values = np.clip(self.values, 0.0, 1.0)

    @property
    def truth(self) -> float:
        return float(self.values[CognitiveDimension.TRUTH])

    @property
    def novelty(self) -> float:
        return float(self.values[CognitiveDimension.NOVELTY])

    @property
    def utility(self) -> float:
        return float(self.values[CognitiveDimension.UTILITY])

    @property
    def confidence(self) -> float:
        return float(self.values[CognitiveDimension.CONFIDENCE])

    @property
    def risk(self) -> float:
        return float(self.values[CognitiveDimension.RISK])

    @property
    def influence(self) -> float:
        return float(self.values[CognitiveDimension.INFLUENCE])

    def cosine_similarity(self, other: DimensionalVector) -> float:
        a, b = self.values, other.values
        denom = np.linalg.norm(a) * np.linalg.norm(b)
        if denom < COGNITIVE_PLANCK:
            return 0.0
        return float(np.dot(a, b) / denom)

    def magnitude(self) -> float:
        return float(np.linalg.norm(self.values))

    def __add__(self, other: DimensionalVector) -> DimensionalVector:
        return DimensionalVector(values=(self.values + other.values) / 2)

    def to_dict(self) -> Dict:
        return {name: float(self.values[i])
                for i, name in enumerate(CognitiveDimension.NAMES)}


@dataclass
class ParticleLineage:
    """Evolutionary ancestry tracking."""
    parent_ids: List[str] = field(default_factory=list)
    generation: int = 0
    mutation_history: List[Dict] = field(default_factory=list)
    birth_timestamp: float = field(default_factory=time.time)
    split_from: Optional[str] = None
    merged_from: List[str] = field(default_factory=list)


class CognitiveParticle(ABC):
    """
    Base class for all cognitive particles.
    Exists in probabilistic quantum states.
    """

    def __init__(
        self,
        content: str,
        particle_type: ParticleType,
        dimensions: Optional[DimensionalVector] = None,
        source: Optional[str] = None,
    ):
        self.id: str = str(uuid.uuid4())
        self.content: str = content
        self.particle_type: ParticleType = particle_type
        self.dimensions: DimensionalVector = dimensions or DimensionalVector()
        self.source: Optional[str] = source

        # Physical properties
        self.energy: float = 1.0
        self.mass: float = 0.1            # grows with resonance
        self.activation_frequency: int = 0
        self.last_activated: float = time.time()
        self.birth_time: float = time.time()

        # Quantum state
        self.quantum_state: QuantumState = QuantumState.SUPERPOSITION
        self.superposition_states: List[Dict] = []
        self.entangled_particle_ids: List[str] = []

        # Uncertainty
        self.uncertainty: float = 1.0    # 0 = certain, 1 = maximally uncertain
        self.contradiction_score: float = 0.0

        # Evolution
        self.lineage: ParticleLineage = ParticleLineage()
        self.tags: List[str] = []
        self.metadata: Dict[str, Any] = {}

    @property
    def age(self) -> float:
        """Particle age in seconds."""
        return time.time() - self.birth_time

    @property
    def cognitive_mass(self) -> float:
        """
        Mass = base_mass * activation_frequency^0.5 * energy
        Heavy particles attract new knowledge.
        """
        return self.mass * math.sqrt(max(self.activation_frequency, 1)) * self.energy

    def decay(self) -> None:
        """Apply temporal energy decay: E(t) = E0 * exp(-t/tau)."""
        elapsed = time.time() - self.last_activated
        decay_factor = math.exp(-elapsed / TAU_MEMORY)
        self.energy *= decay_factor
        self.energy = max(self.energy, COGNITIVE_PLANCK)

    def activate(self, strength: float = 1.0) -> None:
        """Activation strengthens the particle."""
        self.activation_frequency += 1
        self.energy = min(self.energy + strength * 0.1, 10.0)
        self.mass = min(self.mass + 0.001 * strength, 100.0)
        self.last_activated = time.time()
        if self.quantum_state == QuantumState.DORMANT:
            self.quantum_state = QuantumState.SUPERPOSITION

    def fitness(self) -> float:
        """
        Evolutionary fitness score.
        F = utility * confidence * (1 - risk) * novelty^0.3
        """
        d = self.dimensions
        return (d.utility * d.confidence *
                (1.0 - d.risk) *
                (d.novelty ** 0.3 + COGNITIVE_PLANCK))

    def collapse(self, observation: Dict) -> None:
        """
        Quantum collapse: observation reduces uncertainty.
        Tool execution is an observation event.
        """
        self.quantum_state = QuantumState.COLLAPSED
        self.uncertainty = max(0.0, self.uncertainty - 0.3)
        self.superposition_states = [observation]
        self.metadata["collapsed_by"] = observation.get("tool", "direct_observation")
        self.metadata["collapsed_at"] = time.time()

    def entangle(self, other_id: str) -> None:
        if other_id not in self.entangled_particle_ids:
            self.entangled_particle_ids.append(other_id)
            self.quantum_state = QuantumState.ENTANGLED

    @abstractmethod
    def vibration_modes(self) -> List[float]:
        """Return the string vibration mode spectrum for this particle."""
        pass

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "type": self.particle_type.name,
            "content": self.content,
            "energy": self.energy,
            "mass": self.mass,
            "cognitive_mass": self.cognitive_mass,
            "activation_frequency": self.activation_frequency,
            "uncertainty": self.uncertainty,
            "quantum_state": self.quantum_state.name,
            "dimensions": self.dimensions.to_dict(),
            "fitness": self.fitness(),
            "age": self.age,
            "tags": self.tags,
        }


class Memoryon(CognitiveParticle):
    """
    Persistent memory particle.
    Long-lived, gains mass through repeated activation.
    """

    def __init__(self, content: str, confidence: float = 0.8,
                 dimensions: Optional[DimensionalVector] = None, **kwargs):
        super().__init__(content, ParticleType.MEMORYON, dimensions, **kwargs)
        self.dimensions.values[CognitiveDimension.CONFIDENCE] = confidence
        self.recall_count: int = 0
        self.consolidation_level: float = 0.0  # 0=fresh, 1=fully consolidated

    def consolidate(self) -> None:
        """Memory consolidation increases stability."""
        self.consolidation_level = min(1.0, self.consolidation_level + 0.1)
        self.uncertainty = max(0.0, self.uncertainty - 0.05)

    def vibration_modes(self) -> List[float]:
        d = self.dimensions.values
        return [d[i] * math.cos(i * math.pi / N_DIMENSIONS) for i in range(N_DIMENSIONS)]


class Evidon(CognitiveParticle):
    """
    Evidence particle from external sources.
    High truth dimension, variable confidence.
    """

    def __init__(self, content: str, source: str,
                 evidence_type: str = "empirical",
                 reliability: float = 0.9, **kwargs):
        dims = DimensionalVector(values=np.array([
            reliability,   # truth
            time.time() % 1.0,  # time (normalized)
            0.5,           # novelty
            0.7,           # utility
            1.0 - reliability,  # risk
            reliability,   # confidence
            0.5,           # influence
            0.5            # intent
        ]))
        super().__init__(content, ParticleType.EVIDON, dims, source=source, **kwargs)
        self.evidence_type: str = evidence_type
        self.reliability: float = reliability
        self.verification_status: str = "unverified"
        self.citation_count: int = 0

    def verify(self, score: float) -> None:
        self.verification_status = "verified" if score > 0.7 else "disputed"
        self.dimensions.values[CognitiveDimension.TRUTH] = score
        self.collapse({"tool": "verifier", "score": score})

    def vibration_modes(self) -> List[float]:
        d = self.dimensions.values
        return [d[i] * math.sin((i + 1) * math.pi / N_DIMENSIONS) for i in range(N_DIMENSIONS)]


class Hypotheon(CognitiveParticle):
    """
    Speculative knowledge particle.
    Represents hypotheses, assumptions, predictions.
    Exists maximally in superposition.
    """

    def __init__(self, content: str, confidence: float = 0.3,
                 speculation_depth: int = 1, **kwargs):
        dims = DimensionalVector(values=np.array([
            confidence * 0.5,  # truth (uncertain)
            0.9,               # time (future-oriented)
            0.9,               # novelty (high)
            0.6,               # utility
            0.5,               # risk
            confidence,        # confidence
            0.4,               # influence
            0.7                # intent
        ]))
        super().__init__(content, ParticleType.HYPOTHEON, dims, **kwargs)
        self.speculation_depth: int = speculation_depth
        self.competing_hypotheses: List[str] = []
        self.evidence_for: List[str] = []
        self.evidence_against: List[str] = []
        self.prediction_accuracy: Optional[float] = None

    def add_competing(self, hyp_id: str) -> None:
        if hyp_id not in self.competing_hypotheses:
            self.competing_hypotheses.append(hyp_id)

    def update_from_evidence(self, supports: bool, strength: float) -> None:
        delta = strength * 0.1 if supports else -strength * 0.1
        self.dimensions.values[CognitiveDimension.CONFIDENCE] = np.clip(
            self.dimensions.values[CognitiveDimension.CONFIDENCE] + delta, 0, 1
        )
        self.uncertainty = max(0.0, self.uncertainty - abs(delta))

    def vibration_modes(self) -> List[float]:
        d = self.dimensions.values
        # Hypotheons vibrate at higher frequency — speculative
        return [d[i] * math.sin(i * 2 * math.pi / N_DIMENSIONS) for i in range(N_DIMENSIONS)]


class Reasonon(CognitiveParticle):
    """
    Reasoning particle. Represents causal chains and inferential pathways.
    Links antecedents to consequents.
    """

    def __init__(self, content: str, antecedent_ids: List[str],
                 consequent_ids: List[str], inference_type: str = "deductive", **kwargs):
        dims = DimensionalVector(values=np.array([
            0.7,    # truth
            0.5,    # time
            0.4,    # novelty
            0.8,    # utility
            0.3,    # risk
            0.7,    # confidence
            0.6,    # influence
            0.6     # intent
        ]))
        super().__init__(content, ParticleType.REASONON, dims, **kwargs)
        self.antecedent_ids: List[str] = antecedent_ids
        self.consequent_ids: List[str] = consequent_ids
        self.inference_type: str = inference_type  # deductive|inductive|abductive
        self.validity_score: float = 0.7
        self.applied_count: int = 0

    def apply(self) -> None:
        self.applied_count += 1
        self.activate(strength=0.5)

    def vibration_modes(self) -> List[float]:
        d = self.dimensions.values
        # Reasonons: phase-shifted — they transform other particles
        return [d[i] * math.cos((i + 0.5) * math.pi / N_DIMENSIONS)
                for i in range(N_DIMENSIONS)]


class Emergon(CognitiveParticle):
    """
    Emerged concept particle. Born from string resonance.
    These are NOT manually created — they self-assemble.
    """

    def __init__(self, content: str, origin_string_ids: List[str],
                 emergence_strength: float = 0.5, **kwargs):
        dims = DimensionalVector(values=np.array([
            0.6,                # truth
            0.5,                # time
            emergence_strength, # novelty (emergent = novel)
            0.7,                # utility
            0.2,                # risk
            0.5,                # confidence
            emergence_strength, # influence
            0.5                 # intent
        ]))
        super().__init__(content, ParticleType.EMERGON, dims, **kwargs)
        self.origin_string_ids: List[str] = origin_string_ids
        self.emergence_strength: float = emergence_strength
        self.stability: float = 0.3  # grows over time if reinforced

    def reinforce(self) -> None:
        self.stability = min(1.0, self.stability + 0.05)
        self.activate()

    def vibration_modes(self) -> List[float]:
        # Complex interference pattern
        d = self.dimensions.values
        return [(d[i] * math.cos(i * math.pi / 4) +
                 d[(i+1) % N_DIMENSIONS] * math.sin(i * math.pi / 4)) / 2
                for i in range(N_DIMENSIONS)]


class Darkon(CognitiveParticle):
    """
    Dark matter cognitive particle.
    Inferred structural influence — not directly observed.
    Detected through unexplained link clustering.
    """

    def __init__(self, inferred_domain: str, influence_radius: float = 1.0, **kwargs):
        dims = DimensionalVector(values=np.zeros(N_DIMENSIONS))
        super().__init__(f"[DARK: {inferred_domain}]",
                         ParticleType.DARKON, dims, **kwargs)
        self.inferred_domain: str = inferred_domain
        self.influence_radius: float = influence_radius
        self.unexplained_links: List[str] = []
        self.detection_confidence: float = 0.1

    def register_unexplained_link(self, string_id: str) -> None:
        self.unexplained_links.append(string_id)
        self.detection_confidence = min(
            0.95, self.detection_confidence + 0.05 * len(self.unexplained_links)
        )

    def vibration_modes(self) -> List[float]:
        # Dark matter: nearly undetectable — tiny amplitudes
        return [COGNITIVE_PLANCK * (i + 1) for i in range(N_DIMENSIONS)]