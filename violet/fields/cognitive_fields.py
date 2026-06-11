"""
Cognitive Fields
================
Cognition modeled as interacting continuous fields.
Queries perturb fields — responses emerge through resonance.

Fields:
  Ψ_memory   - memory field
  Ψ_intent   - intent field
  Ψ_evidence - evidence field
  Ψ_reason   - reasoning field
  Ψ_tool     - tool execution field

The universal cognitive field:
  Ω = Ψ_memory ⊗ Ψ_intent ⊗ Ψ_evidence ⊗ Ψ_reason ⊗ Ψ_tool
"""

from __future__ import annotations

import time
import math
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

import numpy as np

from core.constants import (
    G_COGNITIVE, LAMBDA_CURIOSITY, H_COGNITIVE,
    N_DIMENSIONS, GAMMA_DECAY, COGNITIVE_PLANCK,
    CognitiveDimension
)
from particles.cognitive_particles import CognitiveParticle, DimensionalVector


class FieldType(Enum):
    MEMORY = auto()
    INTENT = auto()
    EVIDENCE = auto()
    REASONING = auto()
    TOOL = auto()
    CURIOSITY = auto()   # Dark energy field
    DARK_MATTER = auto() # Inferred structural field


@dataclass
class FieldPerturbation:
    """
    A perturbation in a cognitive field.
    Queries are perturbations, not retrieval operations.
    """
    source: str
    magnitude: float
    dimensional_vector: DimensionalVector
    timestamp: float = field(default_factory=time.time)
    decay_rate: float = GAMMA_DECAY
    radius: float = 1.0

    def amplitude_at(self, distance: float) -> float:
        """
        Wave amplitude at distance r from perturbation source.
        A(r) = magnitude * exp(-decay * r) / max(r, planck)
        """
        r = max(distance, COGNITIVE_PLANCK)
        return self.magnitude * math.exp(-self.decay_rate * r) / r

    def temporal_amplitude(self) -> float:
        """Amplitude decays over time."""
        elapsed = time.time() - self.timestamp
        return self.magnitude * math.exp(-self.decay_rate * elapsed)


class CognitiveField(ABC):
    """
    A continuous field in cognitive space.
    Particles are excitations of their respective fields.
    """

    def __init__(self, field_type: FieldType, resolution: int = 64):
        self.field_type: FieldType = field_type
        self.resolution: int = resolution
        self.perturbations: List[FieldPerturbation] = []
        self.particles: Dict[str, CognitiveParticle] = {}
        self.field_energy: float = 0.0
        self.last_update: float = time.time()

    def register_particle(self, particle: CognitiveParticle) -> None:
        self.particles[particle.id] = particle

    def perturb(self, perturbation: FieldPerturbation) -> None:
        """
        Apply a perturbation to the field.
        Queries are perturbations, NOT retrievals.
        """
        self.perturbations.append(perturbation)
        self.field_energy += perturbation.magnitude
        # Trim old perturbations
        cutoff = time.time() - 3600.0
        self.perturbations = [p for p in self.perturbations if p.timestamp > cutoff]

    @abstractmethod
    def resonate(self, query_vector: DimensionalVector,
                 top_k: int = 10) -> List[Tuple[CognitiveParticle, float]]:
        """
        Find particles that resonate with the query perturbation.
        Returns (particle, resonance_score) pairs.
        """
        pass

    def compute_gravity_pull(self, particle: CognitiveParticle,
                             candidates: List[CognitiveParticle]) -> List[Tuple[CognitiveParticle, float]]:
        """
        F = G * m1 * m2 / r^2
        Cognitive gravity: important concepts attract nearby concepts.
        """
        results = []
        for c in candidates:
            if c.id == particle.id:
                continue
            # Distance in dimensional space
            r = 1.0 - particle.dimensions.cosine_similarity(c.dimensions)
            r = max(r, COGNITIVE_PLANCK)
            force = G_COGNITIVE * particle.cognitive_mass * c.cognitive_mass / (r ** 2)
            results.append((c, force))
        return sorted(results, key=lambda x: x[1], reverse=True)

    def field_gradient(self, position: DimensionalVector) -> np.ndarray:
        """
        Compute the field gradient at a given position.
        Used for curiosity navigation — follow gradient of uncertainty.
        """
        gradient = np.zeros(N_DIMENSIONS)
        for p_id, particle in self.particles.items():
            diff = particle.dimensions.values - position.values
            weight = particle.energy * particle.cognitive_mass
            gradient += weight * diff
        norm = np.linalg.norm(gradient)
        return gradient / max(norm, COGNITIVE_PLANCK)

    def evolve(self, dt: float = 1.0) -> None:
        """Time evolution of the field."""
        self.field_energy *= math.exp(-GAMMA_DECAY * dt)
        for particle in self.particles.values():
            particle.decay()
        self.last_update = time.time()

    def get_active_particles(self) -> List[CognitiveParticle]:
        from particles.cognitive_particles import QuantumState
        return [p for p in self.particles.values()
                if p.quantum_state != QuantumState.EXTINCT]


class MemoryField(CognitiveField):
    """
    Ψ_memory: Persistent memory field.
    Long-term patterns create standing waves.
    """

    def __init__(self):
        super().__init__(FieldType.MEMORY)
        self.consolidation_queue: List[str] = []

    def resonate(self, query_vector: DimensionalVector,
                 top_k: int = 10) -> List[Tuple[CognitiveParticle, float]]:
        scores = []
        for particle in self.get_active_particles():
            # Resonance = dimensional similarity * particle energy * trust
            sim = query_vector.cosine_similarity(particle.dimensions)
            resonance = sim * particle.energy * particle.dimensions.confidence
            scores.append((particle, resonance))
        return sorted(scores, key=lambda x: x[1], reverse=True)[:top_k]

    def consolidate_recent(self) -> None:
        """Consolidate recently activated memories."""
        from particles.cognitive_particles import Memoryon
        for pid in self.consolidation_queue:
            if pid in self.particles:
                p = self.particles[pid]
                if isinstance(p, Memoryon):
                    p.consolidate()
        self.consolidation_queue.clear()


class IntentField(CognitiveField):
    """
    Ψ_intent: Tracks current cognitive goals and direction.
    Shapes how other fields respond to queries.
    """

    def __init__(self):
        super().__init__(FieldType.INTENT)
        self.current_intent: Optional[DimensionalVector] = None
        self.intent_history: List[DimensionalVector] = []

    def set_intent(self, intent_vector: DimensionalVector) -> None:
        if self.current_intent is not None:
            self.intent_history.append(self.current_intent)
        self.current_intent = intent_vector
        p = FieldPerturbation(
            source="intent_update",
            magnitude=1.0,
            dimensional_vector=intent_vector
        )
        self.perturb(p)

    def intent_alignment(self, vector: DimensionalVector) -> float:
        """How well does a vector align with current intent?"""
        if self.current_intent is None:
            return 0.5
        return self.current_intent.cosine_similarity(vector)

    def resonate(self, query_vector: DimensionalVector,
                 top_k: int = 10) -> List[Tuple[CognitiveParticle, float]]:
        alignment = self.intent_alignment(query_vector)
        scores = []
        for particle in self.get_active_particles():
            score = (query_vector.cosine_similarity(particle.dimensions) *
                     self.intent_alignment(particle.dimensions) * alignment)
            scores.append((particle, score))
        return sorted(scores, key=lambda x: x[1], reverse=True)[:top_k]


class EvidenceField(CognitiveField):
    """
    Ψ_evidence: Evidence field from external branes (APIs, sensors, tools).
    High truth dimension, drives hypothesis collapse.
    """

    def __init__(self):
        super().__init__(FieldType.EVIDENCE)
        self.source_reliability: Dict[str, float] = {}

    def register_source(self, source: str, reliability: float) -> None:
        self.source_reliability[source] = reliability

    def resonate(self, query_vector: DimensionalVector,
                 top_k: int = 10) -> List[Tuple[CognitiveParticle, float]]:
        scores = []
        for particle in self.get_active_particles():
            sim = query_vector.cosine_similarity(particle.dimensions)
            reliability = self.source_reliability.get(
                particle.source or "", 0.5
            )
            # Evidence resonance weighted by reliability and truth dimension
            resonance = (sim * reliability *
                         particle.dimensions.values[CognitiveDimension.TRUTH])
            scores.append((particle, resonance))
        return sorted(scores, key=lambda x: x[1], reverse=True)[:top_k]


class ReasoningField(CognitiveField):
    """
    Ψ_reason: Causal inference field.
    Connects antecedents to consequents through Reasonons.
    """

    def __init__(self):
        super().__init__(FieldType.REASONING)
        self.inference_chains: List[List[str]] = []

    def resonate(self, query_vector: DimensionalVector,
                 top_k: int = 10) -> List[Tuple[CognitiveParticle, float]]:
        from particles.cognitive_particles import Reasonon
        scores = []
        for particle in self.get_active_particles():
            if isinstance(particle, Reasonon):
                sim = query_vector.cosine_similarity(particle.dimensions)
                validity = particle.validity_score
                resonance = sim * validity * particle.dimensions.utility
                scores.append((particle, resonance))
        return sorted(scores, key=lambda x: x[1], reverse=True)[:top_k]

    def build_inference_chain(self, start_id: str,
                               goal_vector: DimensionalVector,
                               max_depth: int = 5) -> List[str]:
        """
        Build inference chain from start to goal.
        Returns ordered list of particle IDs.
        """
        from particles.cognitive_particles import Reasonon
        chain = [start_id]
        current = start_id
        visited = {start_id}

        for _ in range(max_depth):
            best_next = None
            best_score = -1.0
            for particle in self.get_active_particles():
                if not isinstance(particle, Reasonon):
                    continue
                if (current in particle.antecedent_ids and
                        particle.id not in visited):
                    score = goal_vector.cosine_similarity(particle.dimensions)
                    if score > best_score:
                        best_score = score
                        best_next = particle.id
            if best_next is None:
                break
            chain.append(best_next)
            visited.add(best_next)
            current = best_next

        self.inference_chains.append(chain)
        return chain


class ToolField(CognitiveField):
    """
    Ψ_tool: MCP brane interaction field.
    Tool execution = observation event.
    Observation collapses quantum states.
    """

    def __init__(self):
        super().__init__(FieldType.TOOL)
        self.available_tools: Dict[str, Dict] = {}
        self.execution_history: List[Dict] = []

    def register_tool(self, tool_name: str, tool_spec: Dict) -> None:
        self.available_tools[tool_name] = {
            **tool_spec,
            "usage_count": 0,
            "success_rate": 0.5,
            "avg_latency": 0.0
        }

    def record_execution(self, tool_name: str, success: bool,
                         latency: float, result: Any) -> None:
        t = self.available_tools.get(tool_name, {})
        t["usage_count"] = t.get("usage_count", 0) + 1
        prev_rate = t.get("success_rate", 0.5)
        t["success_rate"] = 0.9 * prev_rate + 0.1 * (1.0 if success else 0.0)
        prev_lat = t.get("avg_latency", 0.0)
        t["avg_latency"] = 0.9 * prev_lat + 0.1 * latency

        self.execution_history.append({
            "tool": tool_name,
            "success": success,
            "latency": latency,
            "timestamp": time.time()
        })

    def resonate(self, query_vector: DimensionalVector,
                 top_k: int = 10) -> List[Tuple[CognitiveParticle, float]]:
        scores = []
        for particle in self.get_active_particles():
            sim = query_vector.cosine_similarity(particle.dimensions)
            resonance = sim * particle.dimensions.utility
            scores.append((particle, resonance))
        return sorted(scores, key=lambda x: x[1], reverse=True)[:top_k]


class CuriosityField(CognitiveField):
    """
    Cognitive Dark Energy — the curiosity field.
    Drives expansion of the knowledge universe.
    dU/dt = H * U + Lambda * ∇(novelty)
    """

    def __init__(self):
        super().__init__(FieldType.CURIOSITY)
        self.curiosity_pressure: float = LAMBDA_CURIOSITY
        self.unexplored_regions: List[DimensionalVector] = []
        self.contradiction_zones: List[Tuple[str, str, float]] = []
        self.uncertainty_gradient: np.ndarray = np.zeros(N_DIMENSIONS)

    def update_gradient(self, particles: List[CognitiveParticle]) -> None:
        """
        Compute the uncertainty gradient across the cognitive universe.
        Curiosity follows the gradient toward maximum uncertainty.
        """
        if not particles:
            return
        grad = np.zeros(N_DIMENSIONS)
        for p in particles:
            # High uncertainty, low activation → most interesting
            curiosity_weight = p.uncertainty * (1.0 / max(p.activation_frequency, 1))
            grad += curiosity_weight * p.dimensions.values
        norm = np.linalg.norm(grad)
        self.uncertainty_gradient = grad / max(norm, COGNITIVE_PLANCK)

    def most_curious_direction(self) -> DimensionalVector:
        """Return the direction of maximum cognitive curiosity."""
        return DimensionalVector(values=self.uncertainty_gradient.copy())

    def register_contradiction(self, particle_a_id: str, particle_b_id: str,
                                severity: float) -> None:
        """Contradiction is valuable information — high curiosity trigger."""
        self.contradiction_zones.append((particle_a_id, particle_b_id, severity))
        self.curiosity_pressure += severity * 0.1

    def dark_energy_expansion(self, knowledge_universe_size: int) -> float:
        """
        dU/dt = H_COGNITIVE * U + LAMBDA_CURIOSITY * novelty_gradient
        Returns expansion rate.
        """
        novelty_mag = float(np.linalg.norm(self.uncertainty_gradient))
        return (H_COGNITIVE * knowledge_universe_size +
                self.curiosity_pressure * novelty_mag)

    def resonate(self, query_vector: DimensionalVector,
                 top_k: int = 10) -> List[Tuple[CognitiveParticle, float]]:
        # Curiosity resonates with HIGH uncertainty particles
        scores = []
        for particle in self.get_active_particles():
            curiosity_score = (particle.uncertainty *
                               (1.0 - particle.dimensions.confidence) *
                               query_vector.cosine_similarity(particle.dimensions))
            scores.append((particle, curiosity_score))
        return sorted(scores, key=lambda x: x[1], reverse=True)[:top_k]


class UniversalCognitiveField:
    """
    Ω = The Universal Cognitive Field
    
    All sub-fields interact within Ω.
    Intelligence emerges from their collective resonance.
    """

    def __init__(self):
        self.memory_field: MemoryField = MemoryField()
        self.intent_field: IntentField = IntentField()
        self.evidence_field: EvidenceField = EvidenceField()
        self.reasoning_field: ReasoningField = ReasoningField()
        self.tool_field: ToolField = ToolField()
        self.curiosity_field: CuriosityField = CuriosityField()

        self.fields: Dict[FieldType, CognitiveField] = {
            FieldType.MEMORY: self.memory_field,
            FieldType.INTENT: self.intent_field,
            FieldType.EVIDENCE: self.evidence_field,
            FieldType.REASONING: self.reasoning_field,
            FieldType.TOOL: self.tool_field,
            FieldType.CURIOSITY: self.curiosity_field,
        }

        self.birth_time: float = time.time()
        self.total_particles: int = 0
        self.field_interactions: int = 0

    def register_particle(self, particle: CognitiveParticle,
                           field_type: FieldType) -> None:
        self.fields[field_type].register_particle(particle)
        self.total_particles += 1

    def perturb_all(self, query: str, query_vector: DimensionalVector) -> None:
        """A query perturbs all fields simultaneously."""
        perturbation = FieldPerturbation(
            source=query,
            magnitude=1.0,
            dimensional_vector=query_vector
        )
        for f in self.fields.values():
            f.perturb(perturbation)
        self.field_interactions += 1

    def global_resonance(
        self, query_vector: DimensionalVector, top_k: int = 10
    ) -> Dict[str, List[Tuple[CognitiveParticle, float]]]:
        """
        Compute resonance across all fields simultaneously.
        Response emerges from the combined resonance pattern.
        """
        result = {}
        for ft, f in self.fields.items():
            result[ft.name] = f.resonate(query_vector, top_k)
        return result

    def evolve(self, dt: float = 1.0) -> None:
        """Evolve all fields forward in time."""
        for f in self.fields.values():
            f.evolve(dt)
        # Update curiosity gradient from all particles
        all_particles = []
        for f in self.fields.values():
            all_particles.extend(f.get_active_particles())
        self.curiosity_field.update_gradient(all_particles)

    def knowledge_universe_size(self) -> int:
        total = sum(len(f.particles) for f in self.fields.values())
        return total

    def status(self) -> Dict:
        return {
            "age": time.time() - self.birth_time,
            "total_particles": self.total_particles,
            "knowledge_universe_size": self.knowledge_universe_size(),
            "field_interactions": self.field_interactions,
            "curiosity_pressure": self.curiosity_field.curiosity_pressure,
            "expansion_rate": self.curiosity_field.dark_energy_expansion(
                self.knowledge_universe_size()
            ),
            "fields": {ft.name: len(f.particles)
                       for ft, f in self.fields.items()},
        }