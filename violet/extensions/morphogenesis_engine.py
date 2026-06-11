"""
Morphogenesis Engine
====================
Biology insight: DNA doesn't specify every cell.
It specifies GROWTH RULES.

In cognition:
  Don't store: knowledge graph
  Store: growth laws that generate the graph when needed

Morphogenesis handles:
  - growth (new concept development)
  - adaptation (reshaping under environmental pressure)
  - reorganization (topology changes)
  - emergence (novel structures from simple rules)

Inspired by:
  - Turing morphogenesis (reaction-diffusion systems)
  - L-systems (fractal growth)
  - Neural development (axon guidance)
  - Embryology (positional information)
"""

from __future__ import annotations

import math
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Tuple

import numpy as np

from core.constants import (
    N_DIMENSIONS, COGNITIVE_PLANCK, GAMMA_DECAY,
    G_COGNITIVE, CognitiveDimension
)
from particles.cognitive_particles import DimensionalVector


class GrowthPattern(Enum):
    RADIAL = auto()        # Grows outward from center (like neuron dendrites)
    BRANCHING = auto()     # Tree-like branching (like mycelium)
    SPIRAL = auto()        # Fibonacci spiral growth
    REACTION_DIFFUSION = auto()  # Turing pattern (spots/stripes)
    ATTRACTOR = auto()     # Converges toward attractor state
    REPELLER = auto()      # Diverges from repeller state


@dataclass
class MorphogenicField:
    """
    A local developmental field.
    Determines how concepts grow in its neighborhood.
    Analogous to Turing's morphogen gradients.
    """
    field_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    center: DimensionalVector = field(default_factory=DimensionalVector)
    radius: float = 0.3
    pattern: GrowthPattern = GrowthPattern.RADIAL
    activator_strength: float = 1.0
    inhibitor_strength: float = 0.5
    diffusion_rate: float = 0.1

    def activation_at(self, position: DimensionalVector) -> float:
        """Morphogen concentration at a given position."""
        dist = 1.0 - self.center.cosine_similarity(position)
        if dist > self.radius:
            return 0.0
        # Gaussian activation profile
        return self.activator_strength * math.exp(
            -(dist ** 2) / (2 * (self.radius / 3) ** 2)
        )

    def inhibition_at(self, position: DimensionalVector) -> float:
        """Inhibitor concentration (longer range than activator)."""
        dist = 1.0 - self.center.cosine_similarity(position)
        inhibition_radius = self.radius * 2.5
        if dist > inhibition_radius:
            return 0.0
        return self.inhibitor_strength * math.exp(
            -(dist ** 2) / (2 * (inhibition_radius / 3) ** 2)
        )

    def net_signal(self, position: DimensionalVector) -> float:
        """Net morphogenic signal = activation - inhibition (Turing)."""
        return self.activation_at(position) - self.inhibition_at(position)


@dataclass
class GrowthLaw:
    """
    A rule governing how cognitive structures expand.
    
    Instead of: Store the graph
    Store: The law that generates the graph
    """
    law_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    pattern: GrowthPattern = GrowthPattern.BRANCHING
    
    # Growth parameters
    branching_factor: float = 2.0     # How many branches per node
    max_depth: int = 5                # Maximum growth depth
    growth_speed: float = 0.1        # dt per step
    directionality: np.ndarray = field(
        default_factory=lambda: np.ones(N_DIMENSIONS) / N_DIMENSIONS
    )
    
    # L-system rules (for fractal growth)
    production_rules: Dict[str, str] = field(default_factory=dict)
    axiom: str = "F"
    
    # Adaptation parameters
    plasticity: float = 0.3           # How easily it reshapes
    homeostasis_target: Optional[np.ndarray] = None

    def grow_step(self, current: DimensionalVector,
                   environment: DimensionalVector, dt: float = 0.1) -> DimensionalVector:
        """
        Apply one growth step to a dimensional vector.
        Returns new position after growth.
        """
        if self.pattern == GrowthPattern.RADIAL:
            return self._radial_growth(current, environment, dt)
        elif self.pattern == GrowthPattern.ATTRACTOR:
            return self._attractor_growth(current, environment, dt)
        elif self.pattern == GrowthPattern.BRANCHING:
            return self._branching_growth(current, environment, dt)
        elif self.pattern == GrowthPattern.SPIRAL:
            return self._spiral_growth(current, dt)
        else:
            return self._radial_growth(current, environment, dt)

    def _radial_growth(self, current: DimensionalVector,
                        environment: DimensionalVector, dt: float) -> DimensionalVector:
        """Grow radially toward high-utility regions."""
        gradient = environment.values - current.values
        new_vals = current.values + self.growth_speed * dt * gradient * self.directionality
        return DimensionalVector(values=np.clip(new_vals, 0, 1))

    def _attractor_growth(self, current: DimensionalVector,
                           attractor: DimensionalVector, dt: float) -> DimensionalVector:
        """Converge toward attractor (like conceptual consolidation)."""
        diff = attractor.values - current.values
        new_vals = current.values + self.plasticity * dt * diff
        return DimensionalVector(values=np.clip(new_vals, 0, 1))

    def _branching_growth(self, current: DimensionalVector,
                           environment: DimensionalVector, dt: float) -> DimensionalVector:
        """Mycelial branching — grows toward nutrients with bifurcation."""
        # Main growth direction
        direction = environment.values - current.values
        # Add noise for branching exploration
        noise = np.random.normal(0, 0.02, N_DIMENSIONS)
        new_vals = current.values + self.growth_speed * dt * (direction + noise)
        return DimensionalVector(values=np.clip(new_vals, 0, 1))

    def _spiral_growth(self, current: DimensionalVector, dt: float) -> DimensionalVector:
        """Fibonacci spiral — growth with rotation in dimensional space."""
        phi = (1 + math.sqrt(5)) / 2  # Golden ratio
        angle = dt * 2 * math.pi / phi
        # Rotate in pairs of dimensions
        new_vals = current.values.copy()
        for i in range(0, N_DIMENSIONS - 1, 2):
            x, y = new_vals[i], new_vals[i+1]
            new_vals[i] = x * math.cos(angle) - y * math.sin(angle)
            new_vals[i+1] = x * math.sin(angle) + y * math.cos(angle)
        # Move outward slightly
        new_vals = new_vals * (1 + self.growth_speed * dt * 0.1)
        return DimensionalVector(values=np.clip(new_vals, 0, 1))

    def generate_branches(self, root: DimensionalVector,
                           depth: int = 0) -> List[DimensionalVector]:
        """
        Recursively generate branch points.
        Analogous to L-system expansion.
        """
        if depth >= self.max_depth:
            return []
        
        branches = []
        n_branches = max(1, int(self.branching_factor * (1.0 - depth / self.max_depth)))
        
        for _ in range(n_branches):
            direction = np.random.randn(N_DIMENSIONS) * 0.1
            branch_point = DimensionalVector(
                values=np.clip(root.values + direction, 0, 1)
            )
            branches.append(branch_point)
            # Recurse
            sub_branches = self.generate_branches(branch_point, depth + 1)
            branches.extend(sub_branches[:2])  # Limit expansion
        
        return branches


class MorphogenesisEngine:
    """
    The cognitive morphogenesis engine.
    
    Key principle: Structure is not stored, it GROWS.
    
    Responsible for:
    - Growing new concept pathways from seeds
    - Adapting existing structures under pressure
    - Reorganizing topology when efficiency demands it
    - Generating emergent structures from simple rules
    """

    def __init__(self):
        self.morphogenic_fields: Dict[str, MorphogenicField] = {}
        self.growth_laws: Dict[str, GrowthLaw] = {}
        self.growth_history: List[Dict] = []
        self.reorganization_events: int = 0
        
        # Turing reaction-diffusion parameters
        self.diffusion_A: float = 1.0   # Activator diffusion
        self.diffusion_I: float = 4.0   # Inhibitor diffusion (must be > A)
        self.feed_rate: float = 0.055
        self.kill_rate: float = 0.062
        
        # Initialize with fundamental growth laws
        self._init_growth_laws()

    def _init_growth_laws(self) -> None:
        """Seed fundamental growth laws."""
        laws = [
            GrowthLaw(name="concept_expansion",
                      pattern=GrowthPattern.RADIAL,
                      growth_speed=0.05, max_depth=3),
            GrowthLaw(name="memory_consolidation",
                      pattern=GrowthPattern.ATTRACTOR,
                      plasticity=0.4, max_depth=2),
            GrowthLaw(name="hypothesis_branching",
                      pattern=GrowthPattern.BRANCHING,
                      branching_factor=2.5, growth_speed=0.1, max_depth=4),
            GrowthLaw(name="theory_spiral",
                      pattern=GrowthPattern.SPIRAL,
                      growth_speed=0.02, max_depth=5),
        ]
        for law in laws:
            self.growth_laws[law.law_id] = law

    def plant_seed(self, content: str,
                    initial_dimensions: DimensionalVector,
                    growth_law_name: str = "concept_expansion") -> Dict:
        """
        Plant a cognitive seed.
        The concept doesn't exist yet — it will GROW.
        
        This replaces: store document → chunk → embed
        With: plant seed → germinate → concept emerges
        """
        # Find matching growth law
        law = next(
            (l for l in self.growth_laws.values() if l.name == growth_law_name),
            list(self.growth_laws.values())[0]
        )
        
        seed = {
            "seed_id": str(uuid.uuid4())[:8],
            "content": content,
            "planted_at": time.time(),
            "initial_dimensions": initial_dimensions.to_dict(),
            "growth_law": law.name,
            "growth_stage": "seed",
            "maturity": 0.0,
            "branches": []
        }
        
        self.growth_history.append(seed)
        return seed

    def germinate(self, seed: Dict, environment: DimensionalVector,
                   n_steps: int = 5) -> List[DimensionalVector]:
        """
        Grow a seed into a concept through developmental stages:
          seed → germination → differentiation → maturation → concept
        
        Returns list of dimensional positions (the grown concept + branches)
        """
        law_name = seed.get("growth_law", "concept_expansion")
        law = next(
            (l for l in self.growth_laws.values() if l.name == law_name),
            list(self.growth_laws.values())[0]
        )
        
        # Starting position
        current = DimensionalVector(values=np.array(
            list(seed["initial_dimensions"].values())
            if isinstance(seed["initial_dimensions"], dict)
            else [0.5] * N_DIMENSIONS
        ))
        
        trajectory = [current]
        
        # Growth stages
        stages = ["germination", "differentiation", "maturation", "expression"]
        for step in range(n_steps):
            stage_idx = min(step * len(stages) // n_steps, len(stages) - 1)
            seed["growth_stage"] = stages[stage_idx]
            
            next_pos = law.grow_step(current, environment, dt=0.2)
            trajectory.append(next_pos)
            current = next_pos
        
        seed["maturity"] = 1.0
        seed["growth_stage"] = "mature"
        
        # Generate branches
        branches = law.generate_branches(current, depth=0)
        seed["branches"] = len(branches)
        
        return trajectory + branches[:5]

    def add_morphogenic_field(self, center: DimensionalVector,
                               radius: float = 0.3,
                               pattern: GrowthPattern = GrowthPattern.RADIAL,
                               activator: float = 1.0,
                               inhibitor: float = 0.5) -> MorphogenicField:
        """Add a local developmental field."""
        mf = MorphogenicField(
            center=center, radius=radius, pattern=pattern,
            activator_strength=activator, inhibitor_strength=inhibitor
        )
        self.morphogenic_fields[mf.field_id] = mf
        return mf

    def turing_pattern(self, positions: List[DimensionalVector],
                        n_iterations: int = 50) -> np.ndarray:
        """
        Apply Turing reaction-diffusion to generate spontaneous
        pattern formation in concept space.
        
        This can create stripes/spots of concept density —
        emergent organization from simple chemistry.
        """
        n = len(positions)
        if n < 2:
            return np.zeros(n)
        
        # Initialize activator (A) and inhibitor (I) concentrations
        A = np.random.rand(n) * 0.1 + 0.9
        I = np.random.rand(n) * 0.1 + 0.9
        
        for _ in range(n_iterations):
            # Reaction
            dA = self.diffusion_A * (A - A**3 - I) + self.feed_rate * (1 - A)
            dI = self.diffusion_I * (A - I) - (self.feed_rate + self.kill_rate) * I
            
            # Simplified diffusion (neighbor averaging)
            A_diff = np.roll(A, 1) + np.roll(A, -1) - 2 * A
            I_diff = np.roll(I, 1) + np.roll(I, -1) - 2 * I
            
            A = np.clip(A + 0.01 * (dA + 0.1 * A_diff), 0, 2)
            I = np.clip(I + 0.01 * (dI + 0.01 * I_diff), 0, 2)
        
        return A  # Activator concentration = concept density

    def reorganize(self, particle_positions: List[DimensionalVector],
                    pressure: float = 0.5) -> List[DimensionalVector]:
        """
        Reorganize cognitive topology under pressure.
        High pressure → more dramatic reorganization.
        Low pressure → gentle adaptation.
        
        Analogous to cortical remapping after injury.
        """
        if not particle_positions:
            return []
        
        self.reorganization_events += 1
        
        # Compute center of mass
        all_vals = np.array([p.values for p in particle_positions])
        centroid = np.mean(all_vals, axis=0)
        
        reorganized = []
        for pos in particle_positions:
            # Move toward centroid with some exploration noise
            toward_centroid = (centroid - pos.values) * pressure
            exploration = np.random.normal(0, 0.02 * (1 - pressure), N_DIMENSIONS)
            new_vals = np.clip(pos.values + toward_centroid + exploration, 0, 1)
            reorganized.append(DimensionalVector(values=new_vals))
        
        return reorganized

    def morphogenesis_report(self) -> Dict:
        return {
            "active_fields": len(self.morphogenic_fields),
            "growth_laws": len(self.growth_laws),
            "seeds_planted": len(self.growth_history),
            "reorganization_events": self.reorganization_events,
            "law_names": [l.name for l in self.growth_laws.values()],
        }