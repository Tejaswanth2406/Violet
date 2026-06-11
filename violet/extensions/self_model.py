"""
Self-Model
==========
Not consciousness in the philosophical sense.
A precise computational self-model.

Tracks:
  - What do I know? (knowledge inventory)
  - What don't I know? (gap map)
  - What am I doing? (current process state)
  - Why am I doing it? (goal hierarchy)
  - How confident am I? (calibration)
  - What are my biases? (systematic errors)
  - How have I changed? (self-delta)

Most agent frameworks LACK THIS ENTIRELY.
A system without a self-model cannot:
  - Know when it's out of its depth
  - Recognize its own biases
  - Detect its own degradation
  - Explain its own reasoning
  - Improve its own architecture

The self-model enables meta-cognition:
  Thinking about thinking.
"""

from __future__ import annotations

import time
import math
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

import numpy as np

from core.constants import N_DIMENSIONS, COGNITIVE_PLANCK, CognitiveDimension
from particles.cognitive_particles import CognitiveParticle, DimensionalVector


class CognitiveBias(Enum):
    CONFIRMATION = auto()     # Prefers confirming evidence
    ANCHORING = auto()        # Over-weights first information
    AVAILABILITY = auto()     # Over-weights recent/vivid info
    DUNNING_KRUGER = auto()   # Overconfident in unknown areas
    CONSERVATISM = auto()     # Under-updates on new evidence
    RECENCY = auto()          # Over-weights recent patterns


@dataclass
class KnowledgeInventory:
    """
    What does the system know?
    Broken down by cognitive dimension.
    """
    dimension_coverage: Dict[str, float] = field(default_factory=dict)
    strong_areas: List[str] = field(default_factory=list)
    weak_areas: List[str] = field(default_factory=list)
    total_particles: int = 0
    confident_particles: int = 0
    uncertain_particles: int = 0
    
    def coverage_score(self) -> float:
        if not self.dimension_coverage:
            return 0.0
        return sum(self.dimension_coverage.values()) / max(len(self.dimension_coverage), 1)


@dataclass
class GoalState:
    """Current goal hierarchy."""
    primary_goal: str = ""
    sub_goals: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    goal_confidence: float = 0.5
    goal_clarity: float = 0.5


@dataclass
class ProcessState:
    """What is the system currently doing?"""
    current_operation: str = "idle"
    operation_started: float = field(default_factory=time.time)
    operations_history: List[Dict] = field(default_factory=list)
    
    def record_operation(self, op: str) -> None:
        self.operations_history.append({
            "operation": op,
            "started": time.time()
        })
        if len(self.operations_history) > 100:
            self.operations_history = self.operations_history[-100:]
        self.current_operation = op
        self.operation_started = time.time()


@dataclass
class CalibrationState:
    """
    Tracks prediction accuracy vs confidence.
    Well-calibrated: 70% confidence → correct 70% of the time.
    """
    predictions: List[Dict] = field(default_factory=list)
    
    def record_prediction(self, predicted: Any, actual: Any,
                           confidence: float) -> None:
        correct = (predicted == actual)
        self.predictions.append({
            "confidence": confidence,
            "correct": correct,
            "timestamp": time.time()
        })
        if len(self.predictions) > 1000:
            self.predictions = self.predictions[-1000:]
    
    def calibration_score(self) -> float:
        """
        Brier score: lower = better calibrated.
        1/(n) * sum((confidence - outcome)^2)
        """
        if not self.predictions:
            return 0.5
        n = len(self.predictions)
        return sum(
            (p["confidence"] - (1.0 if p["correct"] else 0.0)) ** 2
            for p in self.predictions
        ) / n
    
    def confidence_gap(self) -> float:
        """Systematic over/under-confidence."""
        if not self.predictions:
            return 0.0
        avg_confidence = sum(p["confidence"] for p in self.predictions) / len(self.predictions)
        avg_accuracy = sum(1.0 if p["correct"] else 0.0 for p in self.predictions) / len(self.predictions)
        return avg_confidence - avg_accuracy  # Positive = overconfident


class SelfModel:
    """
    The cognitive self-model.
    
    Enables meta-cognition:
      - Know what you know
      - Know what you don't know
      - Know how you know things
      - Know your own limitations
      - Detect self-degradation
    
    Without this, the system is cognitively blind to itself.
    """

    def __init__(self):
        self.knowledge_inventory: KnowledgeInventory = KnowledgeInventory()
        self.goal_state: GoalState = GoalState()
        self.process_state: ProcessState = ProcessState()
        self.calibration: CalibrationState = CalibrationState()
        
        # Bias tracking
        self.detected_biases: Dict[CognitiveBias, float] = {
            bias: 0.0 for bias in CognitiveBias
        }
        
        # Self-delta (how has the system changed?)
        self.snapshots: List[Dict] = []
        self.snapshot_interval: float = 3600.0  # Every hour
        self.last_snapshot: float = time.time()
        
        # Meta-cognitive awareness
        self.known_knowns: Set[str] = set()      # What I know I know
        self.known_unknowns: Set[str] = set()    # What I know I don't know
        self.unknown_unknowns_estimate: float = 0.5  # Estimated dark knowledge
        
        # Performance tracking
        self.query_performance: List[float] = []
        self.error_log: List[Dict] = []
        
        self.birth_time: float = time.time()

    def update_knowledge_inventory(
        self, particles: List[CognitiveParticle]
    ) -> KnowledgeInventory:
        """Survey what the system currently knows."""
        inv = self.knowledge_inventory
        inv.total_particles = len(particles)
        
        # Confidence breakdown
        inv.confident_particles = sum(
            1 for p in particles if p.dimensions.confidence > 0.7
        )
        inv.uncertain_particles = sum(
            1 for p in particles if p.uncertainty > 0.6
        )
        
        # Dimensional coverage
        if particles:
            all_dims = np.array([p.dimensions.values for p in particles])
            for i, name in enumerate(CognitiveDimension.NAMES):
                avg_coverage = float(np.mean(all_dims[:, i]))
                inv.dimension_coverage[name] = avg_coverage
            
            # Identify strong/weak areas
            sorted_dims = sorted(inv.dimension_coverage.items(), key=lambda x: x[1], reverse=True)
            inv.strong_areas = [d for d, v in sorted_dims[:3] if v > 0.6]
            inv.weak_areas = [d for d, v in sorted_dims if v < 0.4]
        
        # Update known unknowns
        uncertain_contents = [
            p.content[:50] for p in particles
            if p.uncertainty > 0.7
        ]
        self.known_unknowns.update(uncertain_contents[:20])
        
        return inv

    def assess_goal_clarity(self, recent_queries: List[str]) -> float:
        """
        How clear is the current goal?
        Computed from query consistency.
        """
        if len(recent_queries) < 2:
            return 0.5
        
        # If recent queries are topically consistent, goal is clear
        # Simple heuristic: word overlap between consecutive queries
        overlaps = []
        for i in range(len(recent_queries) - 1):
            words_a = set(recent_queries[i].lower().split())
            words_b = set(recent_queries[i+1].lower().split())
            union = words_a | words_b
            intersection = words_a & words_b
            overlap = len(intersection) / max(len(union), 1)
            overlaps.append(overlap)
        
        clarity = sum(overlaps) / max(len(overlaps), 1)
        self.goal_state.goal_clarity = clarity
        return clarity

    def detect_biases(self, particles: List[CognitiveParticle]) -> Dict[str, float]:
        """
        Detect systematic biases in knowledge distribution.
        """
        if not particles:
            return {}
        
        # Confirmation bias: recent particles cluster with high confidence
        recent = sorted(particles, key=lambda p: p.birth_time, reverse=True)[:20]
        if recent:
            avg_confidence_recent = np.mean([p.dimensions.confidence for p in recent])
            self.detected_biases[CognitiveBias.CONFIRMATION] = max(
                0, avg_confidence_recent - 0.5
            )
        
        # Availability bias: recently accessed particles over-represented
        recent_activated = sorted(particles, key=lambda p: p.last_activated, reverse=True)[:10]
        activation_recency_bias = np.std([
            p.activation_frequency for p in recent_activated
        ]) if recent_activated else 0.0
        self.detected_biases[CognitiveBias.AVAILABILITY] = min(1.0, activation_recency_bias / 5)
        
        # Dunning-Kruger: high confidence in low-evidence areas
        high_conf_low_evidence = sum(
            1 for p in particles
            if (p.dimensions.confidence > 0.8 and
                p.dimensions.values[CognitiveDimension.TRUTH] < 0.4)
        )
        dk_ratio = high_conf_low_evidence / max(len(particles), 1)
        self.detected_biases[CognitiveBias.DUNNING_KRUGER] = dk_ratio
        
        return {bias.name: round(score, 3)
                for bias, score in self.detected_biases.items()}

    def take_snapshot(self, particles: List[CognitiveParticle]) -> Dict:
        """Take a snapshot of current self-state."""
        now = time.time()
        if now - self.last_snapshot < self.snapshot_interval:
            return {}
        
        self.update_knowledge_inventory(particles)
        snap = {
            "timestamp": now,
            "total_particles": len(particles),
            "avg_confidence": float(np.mean([p.dimensions.confidence for p in particles])) if particles else 0,
            "avg_uncertainty": float(np.mean([p.uncertainty for p in particles])) if particles else 1,
            "known_unknowns": len(self.known_unknowns),
            "biases": {b.name: s for b, s in self.detected_biases.items()},
            "calibration_score": self.calibration.calibration_score(),
        }
        self.snapshots.append(snap)
        self.last_snapshot = now
        return snap

    def compute_self_delta(self) -> Optional[Dict]:
        """
        How has the system changed since the last snapshot?
        """
        if len(self.snapshots) < 2:
            return None
        
        prev = self.snapshots[-2]
        curr = self.snapshots[-1]
        
        return {
            "particle_growth": curr["total_particles"] - prev["total_particles"],
            "confidence_delta": round(curr["avg_confidence"] - prev["avg_confidence"], 3),
            "uncertainty_delta": round(curr["avg_uncertainty"] - prev["avg_uncertainty"], 3),
            "new_known_unknowns": curr["known_unknowns"] - prev["known_unknowns"],
            "time_elapsed": curr["timestamp"] - prev["timestamp"],
        }

    def generate_self_report(self) -> Dict:
        """
        The system's self-assessment.
        What do I know? What don't I know? How am I doing?
        """
        return {
            "i_know": {
                "total_concepts": self.knowledge_inventory.total_particles,
                "confident_about": self.knowledge_inventory.confident_particles,
                "strong_domains": self.knowledge_inventory.strong_areas,
                "coverage_score": round(self.knowledge_inventory.coverage_score(), 3),
            },
            "i_dont_know": {
                "uncertain_concepts": self.knowledge_inventory.uncertain_particles,
                "weak_domains": self.knowledge_inventory.weak_areas,
                "known_unknowns_count": len(self.known_unknowns),
                "estimated_dark_knowledge": round(self.unknown_unknowns_estimate, 3),
                "sample": list(self.known_unknowns)[:5],
            },
            "i_am_doing": {
                "current_operation": self.process_state.current_operation,
                "goal_clarity": round(self.goal_state.goal_clarity, 3),
                "primary_goal": self.goal_state.primary_goal,
            },
            "my_quality": {
                "calibration_brier": round(self.calibration.calibration_score(), 4),
                "confidence_gap": round(self.calibration.confidence_gap(), 3),
                "biases_detected": {
                    b: s for b, s in self.detect_biases([]).items() if s > 0.1
                },
            },
            "i_have_changed_by": self.compute_self_delta(),
            "age_hours": (time.time() - self.birth_time) / 3600,
        }