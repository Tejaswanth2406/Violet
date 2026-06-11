"""
Physics Engines
===============
Core physics subsystems of the Cognitive Physics Engine.

resonance_engine.py  - Resonance dynamics
gravity_engine.py    - Cognitive gravity
wormhole_engine.py   - Wormhole formation/navigation
field_dynamics.py    - Field evolution equations
"""

from __future__ import annotations

import math
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from violet.core.constants import (
    ALPHA_PRIME, GAMMA_DECAY, G_COGNITIVE, WORMHOLE_THRESHOLD,
    N_DIMENSIONS, COGNITIVE_PLANCK, CognitiveDimension
)
from violet.particles.cognitive_particles import CognitiveParticle, DimensionalVector
from violet.strings.context_strings import ContextString, StringNetwork


# ══════════════════════════════════════════════════════════════
# RESONANCE ENGINE
# ══════════════════════════════════════════════════════════════

class ResonanceEngine:
    """
    Models cognitive resonance:
      A(t) = A₀ · cos(ωt) · e^(-γt)
    
    Two particles resonate when their vibration modes overlap.
    Resonance determines information flow strength.
    """

    def __init__(self, damping: float = GAMMA_DECAY):
        self.damping = damping
        self.resonance_events: List[Dict] = []

    def compute_resonance(self, a: CognitiveParticle,
                           b: CognitiveParticle) -> float:
        """
        Resonance = dimensional overlap × energy product × age weighting.
        """
        dim_overlap = a.dimensions.cosine_similarity(b.dimensions)
        energy_factor = math.sqrt(a.energy * b.energy) / 10.0
        age_factor = math.exp(-self.damping * abs(a.age - b.age) / 86400)
        return dim_overlap * energy_factor * age_factor

    def resonant_cascade(
        self,
        source: CognitiveParticle,
        field: List[CognitiveParticle],
        amplitude: float = 1.0,
        depth: int = 3
    ) -> List[Tuple[CognitiveParticle, float]]:
        """
        Standing wave formation — resonance propagates and reinforces.
        Particles that resonate at same frequency form stable patterns.
        """
        resonating: Dict[str, Tuple[CognitiveParticle, float]] = {}
        frontier = [(source, amplitude)]
        visited = {source.id}

        for d in range(depth):
            next_frontier = []
            decay = math.exp(-self.damping * d)
            for particle, current_amp in frontier:
                for other in field:
                    if other.id in visited:
                        continue
                    r = self.compute_resonance(particle, other)
                    if r > COGNITIVE_PLANCK:
                        new_amp = current_amp * r * decay
                        if new_amp > COGNITIVE_PLANCK:
                            resonating[other.id] = (other, new_amp)
                            visited.add(other.id)
                            next_frontier.append((other, new_amp))
            frontier = next_frontier

        results = sorted(resonating.values(), key=lambda x: x[1], reverse=True)
        self.resonance_events.append({
            "source": source.id,
            "resonating_particles": len(results),
            "timestamp": time.time()
        })
        return results

    def standing_wave_check(self, particles: List[CognitiveParticle]) -> List[List[str]]:
        """
        Find groups of particles that form standing wave patterns.
        These are stable, self-reinforcing concept clusters.
        """
        groups: List[List[str]] = []
        visited = set()

        for i, pa in enumerate(particles):
            if pa.id in visited:
                continue
            group = [pa.id]
            visited.add(pa.id)
            for pb in particles[i+1:]:
                if pb.id in visited:
                    continue
                r = self.compute_resonance(pa, pb)
                if r > 0.6:
                    group.append(pb.id)
                    visited.add(pb.id)
            if len(group) > 1:
                groups.append(group)

        return groups


# ══════════════════════════════════════════════════════════════
# GRAVITY ENGINE
# ══════════════════════════════════════════════════════════════

class GravityEngine:
    """
    Cognitive gravity:
      F = G · m₁ · m₂ / r²
    
    Mass comes from resonance frequency.
    High-mass concepts attract new knowledge.
    Forms conceptual orbits around foundational ideas.
    """

    def __init__(self, G: float = G_COGNITIVE):
        self.G = G
        self.orbital_registry: Dict[str, List[str]] = {}

    def gravitational_force(self, a: CognitiveParticle,
                             b: CognitiveParticle) -> float:
        """F = G·m₁·m₂/r²"""
        r = max(1.0 - a.dimensions.cosine_similarity(b.dimensions), COGNITIVE_PLANCK)
        return self.G * a.cognitive_mass * b.cognitive_mass / (r ** 2)

    def find_gravitational_center(
        self, particles: List[CognitiveParticle]
    ) -> DimensionalVector:
        """
        Center of cognitive mass.
        Weighted centroid = Σ(mass_i · position_i) / Σ(mass_i)
        """
        if not particles:
            return DimensionalVector()
        total_mass = sum(p.cognitive_mass for p in particles)
        if total_mass < COGNITIVE_PLANCK:
            return DimensionalVector()
        weighted = sum(
            p.cognitive_mass * p.dimensions.values
            for p in particles
        )
        return DimensionalVector(values=weighted / total_mass)

    def compute_orbits(
        self, particles: List[CognitiveParticle], anchor: CognitiveParticle
    ) -> List[Tuple[CognitiveParticle, float]]:
        """
        Find particles that orbit around a high-mass anchor.
        An orbit = gravitationally bound but not merged.
        """
        orbiting = []
        for p in particles:
            if p.id == anchor.id:
                continue
            force = self.gravitational_force(anchor, p)
            distance = 1.0 - anchor.dimensions.cosine_similarity(p.dimensions)
            # Orbital condition: strong enough gravity but not too close
            if 0.01 < force < 0.5 and 0.1 < distance < 0.7:
                orbiting.append((p, force))
        
        self.orbital_registry[anchor.id] = [p.id for p, _ in orbiting]
        return sorted(orbiting, key=lambda x: x[1], reverse=True)

    def gravitational_assist(
        self,
        particle: CognitiveParticle,
        through: CognitiveParticle,
        target: DimensionalVector,
        dt: float = 0.1
    ) -> DimensionalVector:
        """
        Gravitational slingshot: use a massive concept to redirect movement.
        Analogous to spacecraft gravity assist maneuvers.
        """
        pull_toward_through = (through.dimensions.values - particle.dimensions.values)
        pull_toward_target = (target.values - particle.dimensions.values)
        
        combined = (
            pull_toward_through * self.G * through.cognitive_mass +
            pull_toward_target * 0.1
        )
        new_pos = np.clip(particle.dimensions.values + combined * dt, 0, 1)
        return DimensionalVector(values=new_pos)

    def detect_black_holes(
        self, particles: List[CognitiveParticle]
    ) -> List[Tuple[CognitiveParticle, float]]:
        """
        Find cognitive black holes: extremely massive concepts that
        capture all nearby particles and don't let them escape.
        These can cause conceptual blindness (everything routes through one concept).
        """
        black_holes = []
        for particle in particles:
            captives = self.compute_orbits(particles, particle)
            capture_ratio = len(captives) / max(len(particles) - 1, 1)
            if capture_ratio > 0.5 and particle.cognitive_mass > 50:
                black_holes.append((particle, capture_ratio))
        return sorted(black_holes, key=lambda x: x[1], reverse=True)


# ══════════════════════════════════════════════════════════════
# WORMHOLE ENGINE
# ══════════════════════════════════════════════════════════════

class WormholeEngine:
    """
    Manages cognitive wormholes — shortcuts through concept space.
    
    Graphs require explicit links.
    String theory allows wormholes to form spontaneously
    when two distant concepts share deep dimensional structure.
    
    Swarm Intelligence ↔ Market Economics
    (both share: Emergence + Competition + Adaptation)
    """

    def __init__(self, threshold: float = WORMHOLE_THRESHOLD):
        self.threshold = threshold
        self.wormholes: Dict[str, Dict] = {}
        self.traversal_log: List[Dict] = []
        self.spontaneous_formations: int = 0

    def scan_for_wormholes(
        self, particles: List[CognitiveParticle]
    ) -> List[Dict]:
        """
        Scan particle population for wormhole candidates.
        Wormholes form between topically distant but structurally similar particles.
        """
        candidates = []
        for i, pa in enumerate(particles):
            for pb in particles[i+1:]:
                surface_distance = 1.0 - pa.dimensions.cosine_similarity(pb.dimensions)
                
                # Surface similarity (too close = no wormhole needed)
                if surface_distance < 0.2:
                    continue
                
                # Deep structure similarity (vibration mode overlap)
                mode_a = np.array(pa.vibration_modes())
                mode_b = np.array(pb.vibration_modes())
                norm = np.linalg.norm(mode_a) * np.linalg.norm(mode_b)
                deep_sim = float(np.dot(mode_a, mode_b) / max(norm, COGNITIVE_PLANCK))
                
                if deep_sim > self.threshold:
                    candidates.append({
                        "particle_a": pa.id,
                        "particle_b": pb.id,
                        "surface_distance": round(surface_distance, 3),
                        "deep_similarity": round(deep_sim, 3),
                        "wormhole_strength": round(deep_sim * surface_distance, 3),
                    })
        
        return sorted(candidates, key=lambda x: x["wormhole_strength"], reverse=True)

    def form_wormhole(self, pa: CognitiveParticle, pb: CognitiveParticle,
                       strength: float) -> str:
        """
        Form a wormhole between two particles.
        Returns wormhole ID.
        """
        import uuid
        wh_id = str(uuid.uuid4())[:8]
        self.wormholes[wh_id] = {
            "id": wh_id,
            "endpoint_a": pa.id,
            "endpoint_b": pb.id,
            "strength": strength,
            "formed_at": time.time(),
            "traversals": 0,
            "content_a": pa.content[:50],
            "content_b": pb.content[:50],
        }
        self.spontaneous_formations += 1
        return wh_id

    def traverse(self, from_id: str, wormhole_id: str) -> Optional[str]:
        """
        Traverse a wormhole from one side.
        Returns the other endpoint.
        """
        wh = self.wormholes.get(wormhole_id)
        if not wh:
            return None
        
        wh["traversals"] += 1
        destination = (wh["endpoint_b"] if from_id == wh["endpoint_a"]
                       else wh["endpoint_a"])
        
        self.traversal_log.append({
            "from": from_id,
            "to": destination,
            "via": wormhole_id,
            "timestamp": time.time()
        })
        return destination

    def wormhole_report(self) -> Dict:
        return {
            "total_wormholes": len(self.wormholes),
            "spontaneous_formations": self.spontaneous_formations,
            "total_traversals": sum(w["traversals"] for w in self.wormholes.values()),
            "most_traversed": max(
                self.wormholes.values(),
                key=lambda w: w["traversals"],
                default={"traversals": 0}
            ).get("traversals", 0),
        }


# ══════════════════════════════════════════════════════════════
# FIELD DYNAMICS
# ══════════════════════════════════════════════════════════════

class FieldDynamics:
    """
    Governs how cognitive fields evolve over time.
    
    Field equations:
      ∂Ψ/∂t = -iĤΨ + dissipation + sources
    
    Where:
      Ψ = cognitive field state
      Ĥ = cognitive Hamiltonian (total energy operator)
      dissipation = GAMMA_DECAY · Ψ
      sources = new information, activations
    """

    def __init__(self):
        self.hamiltonian: np.ndarray = np.eye(N_DIMENSIONS)
        self.dissipation_rate: float = GAMMA_DECAY
        self.coupling_constants: Dict[str, float] = {
            "memory_evidence": 0.3,
            "evidence_reasoning": 0.4,
            "reasoning_intent": 0.5,
            "intent_memory": 0.2,
        }
        self.evolution_steps: int = 0

    def evolve_field_state(
        self, state: np.ndarray, dt: float = 0.1
    ) -> np.ndarray:
        """
        Time-evolve a field state vector.
        dΨ/dt = -Ĥ·Ψ - γ·Ψ
        """
        # Hamiltonian evolution
        dPsi_Hamiltonian = -self.hamiltonian @ state
        # Dissipation
        dPsi_dissipation = -self.dissipation_rate * state
        # Combined
        new_state = state + dt * (dPsi_Hamiltonian + dPsi_dissipation)
        # Normalize
        norm = np.linalg.norm(new_state)
        if norm > COGNITIVE_PLANCK:
            new_state /= norm
        self.evolution_steps += 1
        return new_state

    def field_coupling(
        self, field_a: np.ndarray, field_b: np.ndarray, coupling: float
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Two fields couple — each influences the other.
        Models how memory and evidence fields interact.
        """
        a_influence_on_b = coupling * field_a
        b_influence_on_a = coupling * field_b
        return (field_a + b_influence_on_a * 0.1,
                field_b + a_influence_on_b * 0.1)

    def interference_pattern(
        self, field_a: np.ndarray, field_b: np.ndarray
    ) -> np.ndarray:
        """
        Compute interference between two cognitive fields.
        Constructive: reinforced understanding.
        Destructive: cognitive dissonance.
        """
        constructive = (field_a + field_b) ** 2
        destructive = (field_a - field_b) ** 2
        return constructive - destructive

    def decoherence(
        self, quantum_state: np.ndarray, environment: np.ndarray,
        coupling_strength: float = 0.1
    ) -> np.ndarray:
        """
        Environment-induced decoherence.
        Collapses quantum superpositions through environmental interaction.
        Models how context collapses ambiguous meanings.
        """
        # Interaction with environment suppresses off-diagonal elements
        decohere_factor = 1.0 - coupling_strength * np.linalg.norm(environment - quantum_state)
        return quantum_state * max(0.0, decohere_factor)