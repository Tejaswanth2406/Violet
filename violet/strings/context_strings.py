"""
Context Strings
===============
The FUNDAMENTAL UNIT of the Cognitive Physics Engine.
Particles are not fundamental — relationships are fundamental.
A concept is a stable vibration pattern in the relationship field.

String Theory MCP: Every MCP server is an information brane.
Branes are connected through dynamic context strings.
"""

from __future__ import annotations

import uuid
import time
import math
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from core.constants import (
    ALPHA_PRIME, GAMMA_DECAY, WORMHOLE_THRESHOLD,
    E_THRESHOLD, E_FUSION, N_DIMENSIONS, COGNITIVE_PLANCK
)
from particles.cognitive_particles import CognitiveParticle, DimensionalVector


class StringTopology(Enum):
    OPEN = auto()       # Two distinct endpoints
    CLOSED = auto()     # Loop — concept reinforces itself
    BRAIDED = auto()    # Multiple strings wound together
    WORMHOLE = auto()   # Shortcut across cognitive space


class StringState(Enum):
    ACTIVE = auto()
    RESONATING = auto()
    DORMANT = auto()
    BROKEN = auto()
    FUSING = auto()


@dataclass
class VibrationSpectrum:
    """
    String vibration modes determine meaning.
    Different modes → different semantic interpretations.
    E = (alpha'/2) * sum(mode_amplitudes^2)
    """
    modes: List[float] = field(default_factory=lambda: [0.0] * N_DIMENSIONS)
    frequency: float = 1.0
    phase: float = 0.0
    damping: float = GAMMA_DECAY

    def energy(self) -> float:
        """String energy from mode amplitudes."""
        return (ALPHA_PRIME / 2) * sum(m ** 2 for m in self.modes)

    def resonance_with(self, other: VibrationSpectrum) -> float:
        """
        Resonance = overlap integral of two vibration patterns.
        High resonance → strong semantic relationship.
        """
        if not self.modes or not other.modes:
            return 0.0
        a = np.array(self.modes)
        b = np.array(other.modes)
        denom = np.linalg.norm(a) * np.linalg.norm(b)
        if denom < COGNITIVE_PLANCK:
            return 0.0
        return float(np.dot(a, b) / denom)

    def evolve(self, dt: float) -> None:
        """Time-evolution of vibration pattern."""
        for i in range(len(self.modes)):
            self.modes[i] *= math.exp(-self.damping * dt)
            self.modes[i] += math.sin(self.frequency * dt + self.phase + i) * 0.01

    def superpose(self, other: VibrationSpectrum) -> VibrationSpectrum:
        """Quantum superposition of two vibration patterns."""
        combined = [(a + b) / 2 for a, b in zip(self.modes, other.modes)]
        return VibrationSpectrum(
            modes=combined,
            frequency=(self.frequency + other.frequency) / 2,
            phase=(self.phase + other.phase) / 2
        )


class ContextString:
    """
    The fundamental unit of the CPE.
    
    A string connects two cognitive entities.
    Properties: meaning, trust, uncertainty, novelty,
                time, utility, energy
    
    Concepts emerge as standing waves from string resonance.
    """

    def __init__(
        self,
        endpoint_a_id: str,
        endpoint_b_id: str,
        topology: StringTopology = StringTopology.OPEN,
        initial_energy: float = 1.0,
    ):
        self.id: str = str(uuid.uuid4())
        self.endpoint_a: str = endpoint_a_id
        self.endpoint_b: str = endpoint_b_id
        self.topology: StringTopology = topology
        self.state: StringState = StringState.ACTIVE

        # String properties
        self.trust: float = 0.5
        self.uncertainty: float = 0.5
        self.novelty: float = 0.5
        self.utility: float = 0.5
        self.energy: float = initial_energy
        self.tension: float = ALPHA_PRIME
        self.semantic_resonance: float = 0.0
        self.latency: float = 0.0           # MCP / tool response latency
        self.historical_success: float = 0.5

        # Vibration
        self.vibration: VibrationSpectrum = VibrationSpectrum()

        # Usage history
        self.activation_count: int = 0
        self.birth_time: float = time.time()
        self.last_activated: float = time.time()
        self.activation_history: List[float] = []

        # Brane metadata
        self.brane_a: Optional[str] = None
        self.brane_b: Optional[str] = None
        self.crosses_branes: bool = False

        # Wormhole data
        self.wormhole_target: Optional[str] = None
        self.shared_dimensions: List[int] = []

    @property
    def age(self) -> float:
        return time.time() - self.birth_time

    def activate(self, strength: float = 1.0) -> None:
        """Activate the string — increases trust and energy."""
        self.activation_count += 1
        self.last_activated = time.time()
        self.activation_history.append(time.time())

        # Trim history to last 1000
        if len(self.activation_history) > 1000:
            self.activation_history = self.activation_history[-1000:]

        self.energy = min(self.energy + 0.05 * strength, 10.0)
        self.trust = min(self.trust + 0.02 * strength, 1.0)
        self.semantic_resonance = min(self.semantic_resonance + 0.01, 1.0)

        if self.state == StringState.DORMANT:
            self.state = StringState.ACTIVE

    def decay(self, dt: float = 1.0) -> None:
        """Energy decay over time."""
        self.energy *= math.exp(-GAMMA_DECAY * dt)
        self.vibration.evolve(dt)
        if self.energy < E_THRESHOLD:
            self.state = StringState.DORMANT

    def compute_resonance(self, other: ContextString) -> float:
        """
        Resonance between two strings.
        High resonance can trigger wormhole formation.
        """
        return self.vibration.resonance_with(other.vibration)

    def can_form_wormhole(self, other: ContextString,
                          particle_registry: Dict) -> Tuple[bool, List[int]]:
        """
        Check if two strings can form a cognitive wormhole.
        Wormholes appear when strings share multiple cognitive dimensions.
        """
        # Compute shared dimension strength
        a_modes = np.array(self.vibration.modes)
        b_modes = np.array(other.vibration.modes)

        shared = []
        for i in range(N_DIMENSIONS):
            if (abs(a_modes[i]) > 0.1 and abs(b_modes[i]) > 0.1 and
                    abs(a_modes[i] - b_modes[i]) < 0.3):
                shared.append(i)

        similarity = self.compute_resonance(other)
        threshold_met = similarity > WORMHOLE_THRESHOLD and len(shared) >= 3

        return threshold_met, shared

    def fuse_with(self, other: ContextString) -> ContextString:
        """
        String fusion: two strings merge into a new string.
        Requires combined energy above E_FUSION threshold.
        """
        if self.energy + other.energy < E_FUSION:
            raise ValueError("Insufficient energy for string fusion")

        fused = ContextString(
            endpoint_a_id=self.endpoint_a,
            endpoint_b_id=other.endpoint_b,
            topology=StringTopology.BRAIDED,
            initial_energy=(self.energy + other.energy) * 0.9
        )
        fused.trust = (self.trust + other.trust) / 2
        fused.semantic_resonance = max(self.semantic_resonance, other.semantic_resonance)
        fused.vibration = self.vibration.superpose(other.vibration)
        return fused

    def update_from_tool_execution(
        self, success: bool, latency: float, result_confidence: float
    ) -> None:
        """
        Tool execution is an observation event.
        Observation reduces uncertainty on the string.
        """
        self.latency = latency
        self.historical_success = (
            0.9 * self.historical_success + 0.1 * (1.0 if success else 0.0)
        )
        self.uncertainty = max(0.0, self.uncertainty - result_confidence * 0.3)
        if success:
            self.activate(strength=result_confidence)
        else:
            self.energy *= 0.9

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "endpoint_a": self.endpoint_a,
            "endpoint_b": self.endpoint_b,
            "topology": self.topology.name,
            "state": self.state.name,
            "trust": self.trust,
            "uncertainty": self.uncertainty,
            "energy": self.energy,
            "semantic_resonance": self.semantic_resonance,
            "activation_count": self.activation_count,
            "vibration_energy": self.vibration.energy(),
            "age": self.age,
            "brane_a": self.brane_a,
            "brane_b": self.brane_b,
        }


class StringNetwork:
    """
    The global web of context strings.
    Topology inspired by spider web resonance.
    Meaning emerges from interaction patterns.
    """

    def __init__(self):
        self.strings: Dict[str, ContextString] = {}
        self.particle_adjacency: Dict[str, List[str]] = {}  # particle_id → string_ids
        self.wormholes: Dict[str, Tuple[str, str]] = {}     # wormhole_id → (str_a, str_b)
        self._stats = {"total_activations": 0, "wormholes_formed": 0, "fusions": 0}

    def add_string(self, string: ContextString) -> None:
        self.strings[string.id] = string
        for ep in [string.endpoint_a, string.endpoint_b]:
            if ep not in self.particle_adjacency:
                self.particle_adjacency[ep] = []
            self.particle_adjacency[ep].append(string.id)

    def get_strings_for_particle(self, particle_id: str) -> List[ContextString]:
        ids = self.particle_adjacency.get(particle_id, [])
        return [self.strings[sid] for sid in ids if sid in self.strings]

    def propagate_activation(
        self, source_id: str, strength: float = 1.0, depth: int = 3
    ) -> List[str]:
        """
        Spider-web resonance propagation.
        Activation spreads through connected strings with decay.
        """
        visited: set = {source_id}
        frontier = [(source_id, strength)]
        activated_particles = []

        for _ in range(depth):
            next_frontier = []
            for particle_id, current_strength in frontier:
                if current_strength < COGNITIVE_PLANCK:
                    continue
                for s in self.get_strings_for_particle(particle_id):
                    s.activate(current_strength)
                    self._stats["total_activations"] += 1
                    other_id = (s.endpoint_b if s.endpoint_a == particle_id
                                else s.endpoint_a)
                    if other_id not in visited:
                        visited.add(other_id)
                        activated_particles.append(other_id)
                        # Decay through string: energy * trust * resonance
                        next_strength = current_strength * s.trust * s.semantic_resonance
                        next_frontier.append((other_id, next_strength))
            frontier = next_frontier

        return activated_particles

    def detect_wormhole_candidates(self) -> List[Tuple[str, str, List[int]]]:
        """
        Scan string pairs for wormhole formation potential.
        Returns candidates: (string_a_id, string_b_id, shared_dimensions)
        """
        candidates = []
        string_list = list(self.strings.values())
        for i, s_a in enumerate(string_list):
            for s_b in string_list[i + 1:]:
                if s_a.endpoint_a == s_b.endpoint_a:
                    continue  # Same source
                can, shared = s_a.can_form_wormhole(s_b, {})
                if can:
                    candidates.append((s_a.id, s_b.id, shared))
        return candidates

    def form_wormhole(self, str_a_id: str, str_b_id: str,
                      shared_dims: List[int]) -> str:
        """Create a cognitive wormhole between two concept clusters."""
        wh_id = str(uuid.uuid4())
        s_a = self.strings[str_a_id]
        s_b = self.strings[str_b_id]

        s_a.topology = StringTopology.WORMHOLE
        s_a.wormhole_target = str_b_id
        s_a.shared_dimensions = shared_dims

        self.wormholes[wh_id] = (str_a_id, str_b_id)
        self._stats["wormholes_formed"] += 1
        return wh_id

    def prune_dormant(self, max_dormant_age: float = 3600.0) -> int:
        """Remove strings that have been dormant too long."""
        now = time.time()
        to_remove = [
            sid for sid, s in self.strings.items()
            if s.state == StringState.DORMANT and
            (now - s.last_activated) > max_dormant_age
        ]
        for sid in to_remove:
            s = self.strings.pop(sid)
            for ep in [s.endpoint_a, s.endpoint_b]:
                if ep in self.particle_adjacency:
                    self.particle_adjacency[ep] = [
                        x for x in self.particle_adjacency[ep] if x != sid
                    ]
        return len(to_remove)

    def get_stats(self) -> Dict:
        active = sum(1 for s in self.strings.values() if s.state == StringState.ACTIVE)
        return {
            **self._stats,
            "total_strings": len(self.strings),
            "active_strings": active,
            "wormholes": len(self.wormholes),
            "particles_connected": len(self.particle_adjacency),
        }