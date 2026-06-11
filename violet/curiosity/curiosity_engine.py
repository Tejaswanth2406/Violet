"""
Curiosity Dynamics & Dark Matter Detection
==========================================
Curiosity = Cognitive Dark Energy (expansion force)
Dark Matter = Inferred structural influence

The system actively hunts for:
  - Contradictions (high curiosity trigger)
  - Uncertainty gradients (follow toward unknown)
  - Missing knowledge (detected via gap analysis)
  - Unexplored regions (dark matter indicators)
"""

from __future__ import annotations

import time
import math
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple

import numpy as np

from violet.core.constants import (
    LAMBDA_CURIOSITY, H_COGNITIVE, R_DARK_MATTER,
    COGNITIVE_PLANCK, N_DIMENSIONS, CognitiveDimension
)
from violet.particles.cognitive_particles import (
    CognitiveParticle, Hypotheon, Darkon, DimensionalVector, QuantumState
)


@dataclass
class ContradictionEvent:
    """Two particles with conflicting truth claims."""
    particle_a_id: str
    particle_b_id: str
    content_a: str
    content_b: str
    severity: float
    detected_at: float = field(default_factory=time.time)
    resolved: bool = False
    resolution_particle_id: Optional[str] = None


@dataclass
class KnowledgeGap:
    """
    A detected gap in the knowledge space.
    Region of dimensional space with few particles.
    """
    gap_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    center: DimensionalVector = field(default_factory=DimensionalVector)
    radius: float = 0.2
    estimated_importance: float = 0.5
    surrounding_particles: List[str] = field(default_factory=list)
    detected_at: float = field(default_factory=time.time)
    filled: bool = False


@dataclass
class CuriosityImpulse:
    """
    A directed curiosity impulse — the system's internal question.
    Generated automatically from uncertainty gradients.
    """
    impulse_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    question: str = ""
    target_region: DimensionalVector = field(default_factory=DimensionalVector)
    urgency: float = 0.5
    source: str = "uncertainty_gradient"  # or 'contradiction' | 'dark_matter' | 'gap'
    triggered_at: float = field(default_factory=time.time)
    resolved: bool = False


class CuriosityEngine:
    """
    The cognitive dark energy engine.
    Continuously generates curiosity impulses.
    Drives autonomous knowledge expansion.
    
    dU/dt = H_COGNITIVE * U + LAMBDA_CURIOSITY * ∇(novelty)
    """

    def __init__(self):
        self.curiosity_pressure: float = LAMBDA_CURIOSITY
        self.impulses: List[CuriosityImpulse] = []
        self.contradictions: List[ContradictionEvent] = []
        self.knowledge_gaps: List[KnowledgeGap] = []
        self.uncertainty_map: np.ndarray = np.ones(N_DIMENSIONS)
        self.exploration_history: List[Dict] = []

        # Dark matter tracker
        self.dark_matter_candidates: Dict[str, Darkon] = {}
        self.unexplained_link_clusters: Dict[str, List[str]] = {}

    def scan_for_contradictions(
        self, particles: List[CognitiveParticle]
    ) -> List[ContradictionEvent]:
        """
        Scan particle population for contradictions.
        Two particles contradict if:
        - High semantic similarity (same domain)
        - Low truth-dimension agreement
        """
        new_contradictions = []
        checked: Set[Tuple[str, str]] = set()

        for i, p_a in enumerate(particles):
            for p_b in particles[i+1:]:
                pair = tuple(sorted([p_a.id, p_b.id]))
                if pair in checked:
                    continue
                checked.add(pair)

                # Same domain (high dimensional sim) but conflicting truth
                dim_sim = p_a.dimensions.cosine_similarity(p_b.dimensions)
                truth_a = p_a.dimensions.values[CognitiveDimension.TRUTH]
                truth_b = p_b.dimensions.values[CognitiveDimension.TRUTH]
                truth_conflict = abs(truth_a - truth_b)

                if dim_sim > 0.7 and truth_conflict > 0.4:
                    severity = dim_sim * truth_conflict
                    event = ContradictionEvent(
                        particle_a_id=p_a.id,
                        particle_b_id=p_b.id,
                        content_a=p_a.content[:100],
                        content_b=p_b.content[:100],
                        severity=severity
                    )
                    p_a.contradiction_score = max(p_a.contradiction_score, severity)
                    p_b.contradiction_score = max(p_b.contradiction_score, severity)
                    new_contradictions.append(event)
                    self.contradictions.append(event)

                    # High-contradiction zones boost curiosity
                    self.curiosity_pressure += severity * 0.05

        return new_contradictions

    def detect_knowledge_gaps(
        self,
        particles: List[CognitiveParticle],
        n_probe_points: int = 20
    ) -> List[KnowledgeGap]:
        """
        Detect sparse regions in dimensional space — knowledge gaps.
        Uses a grid probe approach.
        """
        if not particles:
            return []

        new_gaps = []
        particle_vectors = np.array([p.dimensions.values for p in particles])

        # Generate random probe points
        probe_points = np.random.rand(n_probe_points, N_DIMENSIONS)

        for probe in probe_points:
            probe_dim = DimensionalVector(values=probe)

            # Find nearest particles to this probe
            distances = [
                1.0 - probe_dim.cosine_similarity(p.dimensions)
                for p in particles
            ]
            nearest_dist = min(distances) if distances else 1.0
            nearest_idx = np.argmin(distances)

            # Large nearest-distance = sparse region = gap
            if nearest_dist > 0.4:
                importance = nearest_dist * probe_dim.values[CognitiveDimension.UTILITY]
                nearby = [p.id for p, d in zip(particles, distances) if d < 0.6]

                gap = KnowledgeGap(
                    center=probe_dim,
                    radius=nearest_dist,
                    estimated_importance=float(importance),
                    surrounding_particles=nearby[:5]
                )
                new_gaps.append(gap)
                self.knowledge_gaps.append(gap)

        return sorted(new_gaps, key=lambda g: g.estimated_importance, reverse=True)

    def generate_curiosity_impulse(
        self,
        particles: List[CognitiveParticle],
        context: Optional[str] = None
    ) -> Optional[CuriosityImpulse]:
        """
        Generate a curiosity impulse based on current state.
        Sources: contradiction, gap, dark matter, uncertainty gradient
        """
        # Priority 1: Unresolved contradictions
        unresolved = [c for c in self.contradictions if not c.resolved]
        if unresolved:
            c = max(unresolved, key=lambda x: x.severity)
            return CuriosityImpulse(
                question=f"How do we resolve: '{c.content_a[:50]}' vs '{c.content_b[:50]}'?",
                urgency=c.severity,
                source="contradiction"
            )

        # Priority 2: Knowledge gaps
        unfilled_gaps = [g for g in self.knowledge_gaps if not g.filled]
        if unfilled_gaps:
            g = max(unfilled_gaps, key=lambda x: x.estimated_importance)
            return CuriosityImpulse(
                question=f"What exists in the knowledge region at dimensions: "
                         f"{[f'{v:.2f}' for v in g.center.values[:4]]}?",
                target_region=g.center,
                urgency=g.estimated_importance,
                source="gap"
            )

        # Priority 3: Dark matter zones
        if self.dark_matter_candidates:
            dm = max(self.dark_matter_candidates.values(),
                     key=lambda d: d.detection_confidence)
            if dm.detection_confidence > 0.3:
                return CuriosityImpulse(
                    question=f"What hidden theory explains the {dm.inferred_domain} cluster?",
                    urgency=dm.detection_confidence,
                    source="dark_matter"
                )

        # Priority 4: High uncertainty particles
        if particles:
            high_unc = max(particles, key=lambda p: p.uncertainty, default=None)
            if high_unc and high_unc.uncertainty > 0.7:
                return CuriosityImpulse(
                    question=f"What would increase certainty about: {high_unc.content[:80]}?",
                    target_region=high_unc.dimensions,
                    urgency=high_unc.uncertainty,
                    source="uncertainty_gradient"
                )

        return None

    def detect_dark_matter(
        self, strings: List[Any], particles: List[CognitiveParticle]
    ) -> List[Darkon]:
        """
        Dark matter detection:
        When many strings cluster around a region with no visible anchor,
        infer a hidden cognitive structure.
        
        You don't know the concept, but you detect its gravitational effects.
        """
        detected = []

        # Cluster string endpoints
        endpoint_regions: Dict[str, int] = {}
        for string in strings:
            for ep in [string.endpoint_a, string.endpoint_b]:
                region_key = ep[:8]  # Use ID prefix as rough region key
                endpoint_regions[region_key] = endpoint_regions.get(region_key, 0) + 1

        # Find clusters with no matching particle (unexplained links)
        particle_ids = {p.id for p in particles}
        for region, count in endpoint_regions.items():
            if count > 5:  # Significant cluster
                # Check if any known particle explains this
                explained = any(pid.startswith(region) for pid in particle_ids)
                if not explained:
                    key = f"dark_{region}"
                    if key not in self.dark_matter_candidates:
                        darkon = Darkon(
                            inferred_domain=f"region_{region}",
                            influence_radius=float(count) / 10.0
                        )
                        self.dark_matter_candidates[key] = darkon
                        detected.append(darkon)
                    else:
                        self.dark_matter_candidates[key].register_unexplained_link(region)

        return detected

    def compute_expansion_rate(self, universe_size: int) -> float:
        """
        Knowledge universe expansion rate.
        dU/dt = H * U + Lambda * ||∇novelty||
        """
        novelty_gradient_mag = float(np.linalg.norm(self.uncertainty_map))
        return (H_COGNITIVE * universe_size +
                self.curiosity_pressure * novelty_gradient_mag)

    def update_uncertainty_map(self, particles: List[CognitiveParticle]) -> None:
        """Update the N-dimensional uncertainty landscape."""
        if not particles:
            return
        unc_vals = np.zeros(N_DIMENSIONS)
        for p in particles:
            weight = p.uncertainty
            unc_vals += weight * p.dimensions.values
        norm = np.linalg.norm(unc_vals)
        self.uncertainty_map = unc_vals / max(norm, COGNITIVE_PLANCK)

    def resolve_contradiction(self, contradiction_event: ContradictionEvent,
                               resolution_particle_id: str) -> None:
        """Mark a contradiction as resolved."""
        contradiction_event.resolved = True
        contradiction_event.resolution_particle_id = resolution_particle_id
        self.curiosity_pressure = max(
            LAMBDA_CURIOSITY,
            self.curiosity_pressure - contradiction_event.severity * 0.03
        )

    def curiosity_status(self) -> Dict:
        return {
            "curiosity_pressure": self.curiosity_pressure,
            "active_contradictions": sum(1 for c in self.contradictions if not c.resolved),
            "knowledge_gaps": sum(1 for g in self.knowledge_gaps if not g.filled),
            "dark_matter_candidates": len(self.dark_matter_candidates),
            "pending_impulses": len([i for i in self.impulses if not i.resolved]),
            "uncertainty_magnitude": float(np.linalg.norm(self.uncertainty_map)),
        }