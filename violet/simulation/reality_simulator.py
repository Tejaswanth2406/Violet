"""
Reality Simulation Engine
=========================
Before choosing an answer, simulate multiple futures.
Compare competing hypotheses across trajectories.
Prefer solutions robust across multiple states.

Inspired by:
- Monte Carlo simulation
- Many-worlds interpretation
- Scenario planning
- Evolutionary game theory
"""

from __future__ import annotations

import time
import math
import random
import uuid
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from violet.core.constants import (
    COLLAPSE_CERTAINTY, N_DIMENSIONS, COGNITIVE_PLANCK,
    CognitiveDimension
)
from violet.particles.cognitive_particles import (
    CognitiveParticle, Hypotheon, Reasonon, DimensionalVector, QuantumState
)


class TrajectoryOutcome(Enum):
    SUCCESS = auto()
    FAILURE = auto()
    UNCERTAIN = auto()
    CATASTROPHIC = auto()
    TRANSFORMATIVE = auto()


@dataclass
class FutureTrajectory:
    """A single simulated future state."""
    trajectory_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    hypothesis_id: str = ""
    description: str = ""

    # Outcome properties
    outcome: TrajectoryOutcome = TrajectoryOutcome.UNCERTAIN
    success_probability: float = 0.5
    risk_level: float = 0.3
    novelty_generated: float = 0.5
    utility_delivered: float = 0.5
    reversibility: float = 0.8  # Can this trajectory be undone?

    # Derived scores
    robustness: float = 0.0    # Robust to perturbations?
    optimality: float = 0.0    # How good is the outcome?

    # Simulation metadata
    simulated_at: float = field(default_factory=time.time)
    simulation_depth: int = 1
    branching_factor: int = 1

    def compute_scores(self) -> None:
        """Compute derived robustness and optimality scores."""
        self.robustness = (
            self.success_probability *
            (1.0 - self.risk_level) *
            self.reversibility
        )
        self.optimality = (
            self.utility_delivered *
            self.success_probability *
            (self.novelty_generated ** 0.3)
        )

    def to_dict(self) -> Dict:
        return {
            "id": self.trajectory_id,
            "outcome": self.outcome.name,
            "success_probability": round(self.success_probability, 3),
            "risk_level": round(self.risk_level, 3),
            "utility": round(self.utility_delivered, 3),
            "novelty": round(self.novelty_generated, 3),
            "robustness": round(self.robustness, 3),
            "optimality": round(self.optimality, 3),
            "reversibility": round(self.reversibility, 3),
        }


@dataclass
class SimulationResult:
    """Complete simulation result with all trajectories and recommendation."""
    query: str
    trajectories: List[FutureTrajectory]
    recommended: FutureTrajectory
    confidence: float
    uncertainty_reduced: float
    reasoning: str
    simulated_at: float = field(default_factory=time.time)

    def to_dict(self) -> Dict:
        return {
            "query": self.query,
            "n_trajectories": len(self.trajectories),
            "confidence": round(self.confidence, 3),
            "uncertainty_reduced": round(self.uncertainty_reduced, 3),
            "recommended": self.recommended.to_dict(),
            "all_trajectories": [t.to_dict() for t in self.trajectories],
            "reasoning": self.reasoning,
        }


class RealitySimulator:
    """
    Multi-trajectory reality simulator.
    
    Process:
    1. Generate N competing hypotheses
    2. Simulate each across time horizon
    3. Score on robustness + optimality
    4. Select most robust trajectory
    5. Reduce uncertainty of selected
    """

    def __init__(self, n_trajectories: int = 7, simulation_depth: int = 3):
        self.n_trajectories = n_trajectories
        self.simulation_depth = simulation_depth
        self.simulation_history: List[SimulationResult] = []
        self.total_simulations: int = 0

    def simulate(
        self,
        query: str,
        context_particles: List[CognitiveParticle],
        n_override: Optional[int] = None
    ) -> SimulationResult:
        """
        Run full reality simulation for a query.
        """
        n = n_override or self.n_trajectories
        self.total_simulations += 1

        # Generate trajectories from context
        trajectories = self._generate_trajectories(query, context_particles, n)

        # Score all trajectories
        for t in trajectories:
            t.compute_scores()

        # Collapse quantum superposition to best trajectory
        recommended = self._select_robust(trajectories)

        # Confidence = fraction of trajectories agreeing with recommendation
        confidence = self._compute_consensus(recommended, trajectories)

        # Uncertainty reduction from simulation
        uncertainty_reduced = confidence * 0.4

        reasoning = self._build_reasoning(recommended, trajectories, confidence)

        result = SimulationResult(
            query=query,
            trajectories=trajectories,
            recommended=recommended,
            confidence=confidence,
            uncertainty_reduced=uncertainty_reduced,
            reasoning=reasoning
        )
        self.simulation_history.append(result)
        return result

    def _generate_trajectories(
        self,
        query: str,
        context: List[CognitiveParticle],
        n: int
    ) -> List[FutureTrajectory]:
        """Generate n distinct trajectory hypotheses."""
        trajectories = []

        # Outcome types to explore
        outcome_spectrum = [
            (TrajectoryOutcome.SUCCESS, 0.7, 0.2),
            (TrajectoryOutcome.UNCERTAIN, 0.5, 0.5),
            (TrajectoryOutcome.TRANSFORMATIVE, 0.6, 0.4),
            (TrajectoryOutcome.FAILURE, 0.2, 0.7),
            (TrajectoryOutcome.SUCCESS, 0.8, 0.15),
            (TrajectoryOutcome.CATASTROPHIC, 0.1, 0.9),
            (TrajectoryOutcome.UNCERTAIN, 0.45, 0.55),
        ]

        # Extract context signal
        context_confidence = np.mean([p.dimensions.confidence for p in context]) if context else 0.5
        context_utility = np.mean([p.dimensions.utility for p in context]) if context else 0.5
        context_risk = np.mean(
            [p.dimensions.values[CognitiveDimension.RISK] for p in context]
        ) if context else 0.3

        for i in range(min(n, len(outcome_spectrum))):
            base_outcome, base_success, base_risk = outcome_spectrum[i]

            # Modulate by context
            adjusted_success = base_success * 0.6 + context_confidence * 0.4
            adjusted_risk = base_risk * 0.6 + context_risk * 0.4
            adjusted_utility = context_utility * 0.7 + random.random() * 0.3
            novelty = max(0.1, 1.0 - adjusted_success * 0.7)
            reversibility = max(0.1, 1.0 - adjusted_risk)

            t = FutureTrajectory(
                description=f"Trajectory {i+1}: {base_outcome.name} variant for '{query[:40]}'",
                outcome=base_outcome,
                success_probability=np.clip(adjusted_success + np.random.normal(0, 0.05), 0, 1),
                risk_level=np.clip(adjusted_risk + np.random.normal(0, 0.05), 0, 1),
                utility_delivered=np.clip(adjusted_utility, 0, 1),
                novelty_generated=np.clip(novelty, 0, 1),
                reversibility=np.clip(reversibility, 0, 1),
                simulation_depth=self.simulation_depth,
                branching_factor=n
            )
            trajectories.append(t)

        return trajectories

    def _select_robust(self, trajectories: List[FutureTrajectory]) -> FutureTrajectory:
        """
        Select the most robust trajectory.
        Robustness = success_prob * (1-risk) * reversibility
        """
        if not trajectories:
            raise ValueError("No trajectories to select from")
        return max(trajectories, key=lambda t: t.robustness)

    def _compute_consensus(
        self,
        recommended: FutureTrajectory,
        all_trajectories: List[FutureTrajectory]
    ) -> float:
        """
        Confidence = fraction of trajectories with similar outcome type.
        """
        same_outcome = sum(
            1 for t in all_trajectories
            if t.outcome == recommended.outcome
        )
        return same_outcome / max(len(all_trajectories), 1)

    def _build_reasoning(
        self,
        recommended: FutureTrajectory,
        trajectories: List[FutureTrajectory],
        confidence: float
    ) -> str:
        avg_success = np.mean([t.success_probability for t in trajectories])
        avg_risk = np.mean([t.risk_level for t in trajectories])
        n_catastrophic = sum(1 for t in trajectories
                             if t.outcome == TrajectoryOutcome.CATASTROPHIC)

        reasons = []
        if recommended.robustness > 0.6:
            reasons.append(f"High robustness ({recommended.robustness:.2f}) across perturbations")
        if confidence > 0.5:
            reasons.append(f"Strong consensus across {len(trajectories)} simulated trajectories")
        if n_catastrophic > 0:
            reasons.append(f"WARNING: {n_catastrophic} catastrophic trajectory(s) detected")
        if avg_risk > 0.5:
            reasons.append(f"Elevated average risk ({avg_risk:.2f}) — proceed with caution")
        if recommended.reversibility > 0.7:
            reasons.append(f"High reversibility ({recommended.reversibility:.2f}) — decision is recoverable")

        return "; ".join(reasons) if reasons else "Standard trajectory recommendation"

    def superposition_collapse(
        self,
        particle: CognitiveParticle,
        simulation_result: SimulationResult
    ) -> None:
        """
        Collapse a particle's quantum superposition based on simulation.
        Only collapse if confidence exceeds COLLAPSE_CERTAINTY threshold.
        """
        if simulation_result.confidence >= COLLAPSE_CERTAINTY:
            particle.collapse({
                "tool": "reality_simulator",
                "recommended_trajectory": simulation_result.recommended.trajectory_id,
                "confidence": simulation_result.confidence
            })
            particle.uncertainty = max(
                0.0,
                particle.uncertainty - simulation_result.uncertainty_reduced
            )

    def stats(self) -> Dict:
        return {
            "total_simulations": self.total_simulations,
            "avg_confidence": np.mean([r.confidence for r in self.simulation_history]) if self.simulation_history else 0.0,
            "history_size": len(self.simulation_history),
        }