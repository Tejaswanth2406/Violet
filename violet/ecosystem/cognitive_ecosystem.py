"""
Cognitive Ecosystem
===================
Knowledge objects evolve, compete, cooperate.
Natural selection of cognitive particles.
Emergence of species, niches, and food webs.

Nature-derived: Ecosystem model where:
- Particles are organisms
- Fields are environments  
- Strings are symbiotic relationships
- Branes are biomes
- Evolution shapes all
"""

from __future__ import annotations

import time
import random
import math
import copy
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Set, Tuple

import numpy as np

from core.constants import (
    MU_MUTATION, K_CARRYING, GAMMA_DECAY,
    COGNITIVE_PLANCK, N_DIMENSIONS, CognitiveDimension
)
from particles.cognitive_particles import (
    CognitiveParticle, ParticleLineage, DimensionalVector,
    Memoryon, Evidon, Hypotheon, Reasonon, Emergon, QuantumState
)


class EcologicalRole(Enum):
    PRODUCER = auto()     # Generates new knowledge
    CONSUMER = auto()     # Uses and transforms knowledge
    DECOMPOSER = auto()   # Breaks down outdated knowledge
    SYMBIONT = auto()     # Mutually beneficial relationships
    PARASITE = auto()     # Exploits without giving back
    APEX = auto()         # Dominant concept — high mass, high influence


@dataclass
class CognitiveFitness:
    """
    Multi-dimensional fitness assessment.
    F = utility * confidence * (1-risk) * novelty^0.3
    """
    utility: float = 0.5
    confidence: float = 0.5
    risk: float = 0.3
    novelty: float = 0.5
    age_penalty: float = 0.0

    def score(self) -> float:
        base = (self.utility * self.confidence *
                (1.0 - self.risk) *
                (self.novelty ** 0.3 + COGNITIVE_PLANCK))
        return base * (1.0 - self.age_penalty * 0.1)

    def is_viable(self) -> bool:
        return self.score() > COGNITIVE_PLANCK


@dataclass
class EcologicalNiche:
    """A cognitive niche — a region of dimensional space with stable occupancy."""
    center: DimensionalVector
    radius: float
    occupants: List[str] = field(default_factory=list)
    carrying_capacity: int = 100
    resource_level: float = 1.0
    niche_id: str = ""

    def __post_init__(self):
        if not self.niche_id:
            import uuid
            self.niche_id = str(uuid.uuid4())[:8]

    def can_support(self) -> bool:
        return len(self.occupants) < self.carrying_capacity

    def add_occupant(self, particle_id: str) -> bool:
        if self.can_support():
            self.occupants.append(particle_id)
            return True
        return False

    def competition_pressure(self) -> float:
        return len(self.occupants) / max(self.carrying_capacity, 1)


class EvolutionEngine:
    """
    Governs the evolutionary dynamics of cognitive particles.
    
    Operations:
    - Mutation: random dimensional perturbation
    - Reproduction: high-fitness particles spawn offspring
    - Fusion: two particles merge (string fusion analog)
    - Fission: one particle splits into two
    - Extinction: low-energy particles die
    - Dormancy: particles enter low-energy state
    """

    def __init__(self, mutation_rate: float = MU_MUTATION):
        self.mutation_rate = mutation_rate
        self.generation: int = 0
        self.extinction_log: List[Dict] = []
        self.emergence_log: List[Dict] = []
        self.total_mutations: int = 0
        self.total_reproductions: int = 0
        self.total_extinctions: int = 0

    def mutate(self, particle: CognitiveParticle,
               strength: float = 1.0) -> CognitiveParticle:
        """
        Apply random mutation to a particle's dimensional vector.
        Inspired by genetic mutation.
        """
        new_values = particle.dimensions.values.copy()
        for i in range(N_DIMENSIONS):
            if random.random() < self.mutation_rate * strength:
                delta = np.random.normal(0, 0.05)
                new_values[i] = np.clip(new_values[i] + delta, 0.0, 1.0)

        particle.dimensions = DimensionalVector(values=new_values)
        particle.lineage.mutation_history.append({
            "generation": self.generation,
            "timestamp": time.time(),
            "strength": strength
        })
        self.total_mutations += 1
        return particle

    def reproduce(self, parent: CognitiveParticle,
                   environment_pressure: float = 0.5) -> Optional[CognitiveParticle]:
        """
        High-fitness particles reproduce.
        Offspring inherits parent properties with mutation.
        """
        fitness = CognitiveFitness(
            utility=parent.dimensions.utility,
            confidence=parent.dimensions.confidence,
            risk=parent.dimensions.values[CognitiveDimension.RISK],
            novelty=parent.dimensions.novelty,
        )
        if not fitness.is_viable():
            return None

        # Reproduction probability ∝ fitness
        if random.random() > fitness.score() * (1.0 - environment_pressure):
            return None

        # Create offspring
        offspring_content = f"{parent.content} [evolved]"
        offspring = self._clone_particle(parent, offspring_content)
        offspring.lineage.parent_ids = [parent.id]
        offspring.lineage.generation = parent.lineage.generation + 1
        offspring.energy = parent.energy * 0.5
        parent.energy *= 0.6  # Reproduction costs energy

        # Apply mutation
        self.mutate(offspring, strength=0.5)
        self.total_reproductions += 1

        self.emergence_log.append({
            "type": "reproduction",
            "parent": parent.id,
            "offspring": offspring.id,
            "generation": offspring.lineage.generation
        })
        return offspring

    def fuse(self, particle_a: CognitiveParticle,
              particle_b: CognitiveParticle) -> Optional[Emergon]:
        """
        String fusion analog: two concepts merge.
        Example: LLM + Operating System → Agent OS
        Requires dimensional overlap.
        """
        similarity = particle_a.dimensions.cosine_similarity(particle_b.dimensions)
        if similarity < 0.4:
            return None  # Too different to fuse

        fused_content = f"{particle_a.content} ⊕ {particle_b.content}"
        fused_dims = DimensionalVector(
            values=(particle_a.dimensions.values + particle_b.dimensions.values) / 2
        )

        emergon = Emergon(
            content=fused_content,
            origin_string_ids=[],
            emergence_strength=similarity
        )
        emergon.dimensions = fused_dims
        emergon.energy = (particle_a.energy + particle_b.energy) * 0.8
        emergon.lineage.merged_from = [particle_a.id, particle_b.id]
        emergon.lineage.generation = max(
            particle_a.lineage.generation, particle_b.lineage.generation
        ) + 1

        # Cost to fusing particles
        particle_a.energy *= 0.3
        particle_b.energy *= 0.3

        self.emergence_log.append({
            "type": "fusion",
            "particle_a": particle_a.id,
            "particle_b": particle_b.id,
            "emergon": emergon.id,
            "similarity": similarity
        })
        return emergon

    def fission(self, particle: CognitiveParticle,
                 split_dimension: int = CognitiveDimension.NOVELTY
                 ) -> Tuple[CognitiveParticle, CognitiveParticle]:
        """
        Concept fission: one concept splits into two specialized variants.
        Example: Artificial Intelligence → Machine Learning + Reasoning Systems
        """
        # Create two offspring with complementary dimension emphasis
        content_a = f"{particle.content} [aspect-A]"
        content_b = f"{particle.content} [aspect-B]"

        dims_a = particle.dimensions.values.copy()
        dims_b = particle.dimensions.values.copy()

        # Amplify different dimensions in each split
        for i in range(N_DIMENSIONS):
            if i == split_dimension:
                dims_a[i] = min(1.0, dims_a[i] * 1.3)
                dims_b[i] = max(0.0, dims_b[i] * 0.7)
            else:
                dims_a[i] = max(0.0, dims_a[i] * 0.9)
                dims_b[i] = min(1.0, dims_b[i] * 1.1)

        offspring_a = self._clone_particle(
            particle, content_a, DimensionalVector(values=dims_a)
        )
        offspring_b = self._clone_particle(
            particle, content_b, DimensionalVector(values=dims_b)
        )

        energy_each = particle.energy * 0.45
        offspring_a.energy = energy_each
        offspring_b.energy = energy_each
        offspring_a.lineage.split_from = particle.id
        offspring_b.lineage.split_from = particle.id

        particle.quantum_state = QuantumState.EXTINCT

        self.emergence_log.append({
            "type": "fission",
            "parent": particle.id,
            "offspring_a": offspring_a.id,
            "offspring_b": offspring_b.id
        })
        return offspring_a, offspring_b

    def selection_pressure(self,
                            particles: List[CognitiveParticle],
                            environment: DimensionalVector,
                            keep_ratio: float = 0.8
                            ) -> Tuple[List[CognitiveParticle], List[CognitiveParticle]]:
        """
        Natural selection: environment selects which particles survive.
        Returns (survivors, extinct)
        """
        if not particles:
            return [], []

        scored = []
        for p in particles:
            # Fitness relative to environment
            env_fit = environment.cosine_similarity(p.dimensions)
            abs_fit = p.fitness()
            combined = env_fit * abs_fit * p.energy
            scored.append((p, combined))

        scored.sort(key=lambda x: x[1], reverse=True)
        cutoff = max(1, int(len(scored) * keep_ratio))

        survivors = [p for p, _ in scored[:cutoff]]
        extinct = [p for p, _ in scored[cutoff:]]

        for p in extinct:
            if p.energy < 0.1:
                p.quantum_state = QuantumState.EXTINCT
                self.extinction_log.append({
                    "particle_id": p.id,
                    "content": p.content[:50],
                    "generation": p.lineage.generation,
                    "timestamp": time.time()
                })
                self.total_extinctions += 1

        return survivors, extinct

    def advance_generation(self,
                            particles: List[CognitiveParticle],
                            environment: DimensionalVector
                            ) -> List[CognitiveParticle]:
        """
        Full generational cycle:
        1. Selection pressure
        2. Reproduction of survivors
        3. Mutation
        4. Opportunistic fusion
        """
        self.generation += 1

        survivors, _ = self.selection_pressure(particles, environment)

        new_generation = list(survivors)

        # Reproduction
        for p in survivors:
            if p.energy > 0.5:
                offspring = self.reproduce(p, environment_pressure=0.3)
                if offspring:
                    new_generation.append(offspring)

        # Opportunistic fusion (random pairs)
        if len(survivors) > 3:
            random.shuffle(survivors)
            for i in range(0, min(len(survivors) - 1, 4), 2):
                emergon = self.fuse(survivors[i], survivors[i+1])
                if emergon:
                    new_generation.append(emergon)

        return new_generation

    def _clone_particle(self, source: CognitiveParticle,
                         content: str,
                         dimensions: Optional[DimensionalVector] = None
                         ) -> CognitiveParticle:
        """Create a particle clone with new content."""
        dims = dimensions or DimensionalVector(values=source.dimensions.values.copy())
        clone = Memoryon(content=content, dimensions=dims)
        clone.lineage = copy.deepcopy(source.lineage)
        clone.tags = list(source.tags)
        return clone

    def evolution_stats(self) -> Dict:
        return {
            "generation": self.generation,
            "total_mutations": self.total_mutations,
            "total_reproductions": self.total_reproductions,
            "total_extinctions": self.total_extinctions,
            "emergence_events": len(self.emergence_log),
        }


class CognitiveEcosystem:
    """
    The living cognitive ecosystem.
    All particles are organisms competing, cooperating, evolving.
    
    Inspired by:
    - Mycelium networks (nutrient flow)
    - River basins (information flow)
    - Neural tissue (signal propagation)
    - Evolutionary biology (natural selection)
    """

    def __init__(self):
        self.evolution_engine: EvolutionEngine = EvolutionEngine()
        self.niches: List[EcologicalNiche] = []
        self.all_particles: Dict[str, CognitiveParticle] = {}
        self.ecological_roles: Dict[str, EcologicalRole] = {}
        self.food_web: Dict[str, List[str]] = {}  # who influences whom
        self.ecosystem_age: float = 0.0
        self.climate: DimensionalVector = DimensionalVector(
            values=np.array([0.7, 0.5, 0.6, 0.7, 0.3, 0.6, 0.5, 0.5])
        )  # The "environment" that selection pressure acts on

        self._init_default_niches()

    def _init_default_niches(self) -> None:
        """Initialize ecological niches for different knowledge types."""
        niche_configs = [
            ([0.9, 0.5, 0.3, 0.8, 0.1, 0.9, 0.7, 0.5], "factual_knowledge"),
            ([0.5, 0.9, 0.9, 0.6, 0.4, 0.4, 0.5, 0.8], "speculative_frontier"),
            ([0.7, 0.3, 0.5, 0.9, 0.2, 0.8, 0.6, 0.6], "applied_utility"),
            ([0.6, 0.5, 0.7, 0.5, 0.5, 0.5, 0.9, 0.5], "influential_concepts"),
            ([0.8, 0.5, 0.4, 0.7, 0.3, 0.7, 0.5, 0.9], "intent_driven"),
        ]
        for values, label in niche_configs:
            niche = EcologicalNiche(
                center=DimensionalVector(values=np.array(values)),
                radius=0.3,
                niche_id=label
            )
            self.niches.append(niche)

    def assign_niche(self, particle: CognitiveParticle) -> Optional[EcologicalNiche]:
        """Find the most suitable niche for a particle."""
        best_niche = None
        best_sim = -1.0
        for niche in self.niches:
            sim = particle.dimensions.cosine_similarity(niche.center)
            if sim > best_sim and niche.can_support():
                best_sim = sim
                best_niche = niche
        if best_niche:
            best_niche.add_occupant(particle.id)
        return best_niche

    def assign_role(self, particle: CognitiveParticle) -> EcologicalRole:
        """Assign ecological role based on particle properties."""
        if isinstance(particle, Evidon):
            role = EcologicalRole.PRODUCER
        elif isinstance(particle, Reasonon):
            role = EcologicalRole.CONSUMER
        elif isinstance(particle, Hypotheon):
            role = EcologicalRole.SYMBIONT
        elif isinstance(particle, Emergon):
            role = EcologicalRole.APEX
        elif particle.age > 86400 * 30:
            role = EcologicalRole.DECOMPOSER
        else:
            role = EcologicalRole.CONSUMER

        self.ecological_roles[particle.id] = role
        return role

    def register_particle(self, particle: CognitiveParticle) -> None:
        self.all_particles[particle.id] = particle
        self.assign_niche(particle)
        self.assign_role(particle)

    def evolve_cycle(self, dt: float = 3600.0) -> Dict:
        """
        Run one evolutionary cycle.
        Returns summary of changes.
        """
        self.ecosystem_age += dt
        particles = list(self.all_particles.values())

        new_gen = self.evolution_engine.advance_generation(
            particles, self.climate
        )

        # Register new emergents
        new_count = 0
        for p in new_gen:
            if p.id not in self.all_particles:
                self.all_particles[p.id] = p
                self.assign_niche(p)
                self.assign_role(p)
                new_count += 1

        # Prune extinct
        extinct = [pid for pid, p in self.all_particles.items()
                   if p.quantum_state == QuantumState.EXTINCT]
        for pid in extinct:
            self.all_particles.pop(pid, None)

        return {
            "generation": self.evolution_engine.generation,
            "population": len(self.all_particles),
            "new_particles": new_count,
            "extinctions": len(extinct),
            "ecosystem_age": self.ecosystem_age,
        }

    def mycelial_flow(self, source_id: str, nutrient: str,
                       depth: int = 3) -> List[str]:
        """
        Mycelium-inspired nutrient (information) flow.
        Information flows through connected particles like nutrients
        through fungal networks.
        """
        if source_id not in self.all_particles:
            return []

        visited = {source_id}
        frontier = [source_id]
        reached = []

        for _ in range(depth):
            next_frontier = []
            for pid in frontier:
                # Flow to particles in same or adjacent niches
                particle = self.all_particles[pid]
                for target_id, target in self.all_particles.items():
                    if target_id in visited:
                        continue
                    sim = particle.dimensions.cosine_similarity(target.dimensions)
                    if sim > 0.6 and target.can_accept if hasattr(target, 'can_accept') else True:
                        reached.append(target_id)
                        visited.add(target_id)
                        next_frontier.append(target_id)
                        target.activate(strength=sim * 0.3)
            frontier = next_frontier
            if not frontier:
                break

        return reached

    def biodiversity_index(self) -> float:
        """
        Shannon diversity index of cognitive particle types.
        H = -sum(p_i * log(p_i))
        """
        type_counts: Dict[str, int] = {}
        total = len(self.all_particles)
        if total == 0:
            return 0.0

        for p in self.all_particles.values():
            t = p.particle_type.name
            type_counts[t] = type_counts.get(t, 0) + 1

        h = 0.0
        for count in type_counts.values():
            pi = count / total
            if pi > 0:
                h -= pi * math.log(pi)

        return h

    def ecosystem_health(self) -> Dict:
        total = len(self.all_particles)
        role_distribution = {}
        for pid, role in self.ecological_roles.items():
            r = role.name
            role_distribution[r] = role_distribution.get(r, 0) + 1

        return {
            "total_population": total,
            "biodiversity_index": self.biodiversity_index(),
            "role_distribution": role_distribution,
            "niche_utilization": [
                {
                    "id": n.niche_id,
                    "occupancy": len(n.occupants),
                    "capacity": n.carrying_capacity,
                    "pressure": n.competition_pressure()
                }
                for n in self.niches
            ],
            "ecosystem_age_hours": self.ecosystem_age / 3600.0,
            "evolution_stats": self.evolution_engine.evolution_stats(),
        }