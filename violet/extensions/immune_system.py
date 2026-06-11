"""
Cognitive Immune System
=======================
Current AI handles bad information poorly:
  hallucination → just... bad

Biology handles it differently:
  detect → contain → learn → adapt → remember pathogen

The immune system:
  - Maintains self/non-self distinction
  - Has innate (fast) and adaptive (slow, specific) responses
  - Creates antibodies (learned defenses)
  - Has memory cells (remember past attacks)
  - Can be overwhelmed (immunosuppression)

Cognitive immune targets:
  - Misinformation particles
  - Contradictory knowledge injection
  - Prompt injection attacks
  - Knowledge poisoning
  - False wormholes (misleading shortcuts)
  - Adversarial embeddings
"""

from __future__ import annotations

import time
import uuid
import math
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

import numpy as np

from violet.core.constants import (
    N_DIMENSIONS, COGNITIVE_PLANCK, CognitiveDimension
)
from violet.particles.cognitive_particles import (
    CognitiveParticle, DimensionalVector, QuantumState
)


class ThreatType(Enum):
    MISINFORMATION = auto()      # False content
    CONTRADICTION = auto()       # Conflicts with established knowledge
    PROMPT_INJECTION = auto()    # Adversarial instruction
    KNOWLEDGE_POISON = auto()    # Subtle corruption
    FALSE_WORMHOLE = auto()      # Misleading conceptual shortcut
    HALLUCINATION = auto()       # Internally generated falsehood
    ADVERSARIAL = auto()         # Crafted to fool the system
    STALENESS = auto()           # Outdated but presented as current


class ImmuneResponse(Enum):
    INNATE_FAST = auto()         # Immediate generic response
    ADAPTIVE_SPECIFIC = auto()   # Learned specific response
    TOLERANCE = auto()           # Recognized as safe (self)
    QUARANTINE = auto()          # Isolate but don't destroy
    ELIMINATION = auto()         # Remove from system
    ANTIBODY_PRODUCTION = auto() # Create specific defense pattern


@dataclass
class ThreatSignature:
    """
    A known threat pattern — the cognitive equivalent of an antigen.
    Once learned, future threats with similar signatures are detected faster.
    """
    signature_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    threat_type: ThreatType = ThreatType.MISINFORMATION
    
    # Pattern that identifies this threat
    dimensional_pattern: np.ndarray = field(
        default_factory=lambda: np.zeros(N_DIMENSIONS)
    )
    content_fingerprint: str = ""  # Hash/keywords
    confidence: float = 0.5
    
    # Response prescription
    recommended_response: ImmuneResponse = ImmuneResponse.QUARANTINE
    
    # Memory
    first_seen: float = field(default_factory=time.time)
    last_seen: float = field(default_factory=time.time)
    encounter_count: int = 0
    
    def matches(self, particle: CognitiveParticle, threshold: float = 0.7) -> bool:
        """Does a particle match this threat signature?"""
        dim_sim = float(np.dot(
            self.dimensional_pattern,
            particle.dimensions.values
        ) / max(
            np.linalg.norm(self.dimensional_pattern) *
            np.linalg.norm(particle.dimensions.values),
            COGNITIVE_PLANCK
        ))
        return dim_sim > threshold

    def strengthen(self) -> None:
        self.encounter_count += 1
        self.last_seen = time.time()
        self.confidence = min(0.99, self.confidence + 0.02)


@dataclass
class ImmuneCellType(Enum):
    MACROPHAGE = auto()       # Rapid, non-specific engulfment
    T_CELL = auto()           # Specific targeting of known threats
    B_CELL = auto()           # Produces antibodies
    MEMORY_CELL = auto()      # Remembers past infections
    REGULATORY = auto()       # Prevents autoimmune reactions
    NATURAL_KILLER = auto()   # Destroys highly anomalous particles


@dataclass
class Antibody:
    """
    A specific defense pattern learned from past threats.
    Faster and more precise than innate responses.
    """
    antibody_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    target_signature: ThreatSignature = field(default_factory=ThreatSignature)
    specificity: float = 0.8
    neutralization_power: float = 0.7
    created_at: float = field(default_factory=time.time)
    use_count: int = 0
    
    def neutralize(self, particle: CognitiveParticle) -> float:
        """
        Attempt to neutralize threat.
        Returns neutralization effectiveness (0-1).
        """
        self.use_count += 1
        if self.target_signature.matches(particle):
            return self.neutralization_power * self.specificity
        return 0.0


@dataclass
class ImmuneEvent:
    """Log of an immune system event."""
    event_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    threat_type: ThreatType = ThreatType.MISINFORMATION
    particle_id: str = ""
    response: ImmuneResponse = ImmuneResponse.QUARANTINE
    effectiveness: float = 0.0
    timestamp: float = field(default_factory=time.time)
    details: str = ""


class CognitiveImmuneSystem:
    """
    The cognitive immune system.
    
    Innate arm: Fast, non-specific detection using heuristics.
    Adaptive arm: Learned specific responses from past exposure.
    Tolerance: Self-recognition (don't attack own validated knowledge).
    Memory: Faster response to previously seen threats.
    
    This is what makes VIOLET robust against:
    - Hallucination cascade
    - Adversarial injection
    - Knowledge base poisoning
    - False authority claims
    """

    def __init__(self):
        self.antibodies: Dict[str, Antibody] = {}
        self.threat_signatures: Dict[str, ThreatSignature] = {}
        self.quarantine_zone: Dict[str, CognitiveParticle] = {}
        self.memory_cells: List[ThreatSignature] = []
        self.immune_log: List[ImmuneEvent] = []
        
        # Self/non-self register (validated knowledge IDs)
        self.self_registry: Set[str] = set()
        self.immune_tolerance: float = 0.7
        
        # System health
        self.immune_strength: float = 1.0
        self.autoimmune_risk: float = 0.0
        self.infection_count: int = 0
        self.neutralized_count: int = 0
        
        # Initialize innate heuristics
        self._init_innate_patterns()
        
        # Contradiction memory (particles that conflicted before)
        self.known_contradictions: Dict[str, Tuple[str, str]] = {}

    def _init_innate_patterns(self) -> None:
        """Initialize fast innate detection patterns."""
        innate_threats = [
            (ThreatType.HALLUCINATION,
             np.array([0.1, 0.5, 0.9, 0.3, 0.8, 0.1, 0.3, 0.5])),
            (ThreatType.PROMPT_INJECTION,
             np.array([0.2, 0.3, 0.5, 0.8, 0.9, 0.1, 0.7, 0.9])),
            (ThreatType.MISINFORMATION,
             np.array([0.1, 0.6, 0.4, 0.5, 0.6, 0.1, 0.4, 0.3])),
            (ThreatType.ADVERSARIAL,
             np.array([0.3, 0.4, 0.7, 0.9, 0.8, 0.2, 0.8, 0.8])),
        ]
        for ttype, pattern in innate_threats:
            sig = ThreatSignature(
                threat_type=ttype,
                dimensional_pattern=pattern,
                confidence=0.6,
                recommended_response=ImmuneResponse.QUARANTINE
            )
            self.threat_signatures[sig.signature_id] = sig

    def register_self(self, particle_id: str) -> None:
        """Register a particle as verified self — won't be attacked."""
        self.self_registry.add(particle_id)

    def screen(self, particle: CognitiveParticle) -> Tuple[bool, Optional[ImmuneEvent]]:
        """
        Screen a particle for threats.
        Returns (is_safe, immune_event_if_threat).
        
        Process:
        1. Self check → skip if known safe
        2. Innate screening → fast heuristics
        3. Adaptive screening → antibody matching
        4. Anomaly detection → statistical outlier
        """
        # 1. Self-check
        if particle.id in self.self_registry:
            return True, None
        
        # 2. Innate response
        innate_threat = self._innate_screen(particle)
        if innate_threat:
            event = self._mount_response(particle, innate_threat, ImmuneResponse.INNATE_FAST)
            return False, event
        
        # 3. Adaptive response (antibody matching)
        antibody_match = self._adaptive_screen(particle)
        if antibody_match:
            neutralization = antibody_match.neutralize(particle)
            if neutralization > 0.5:
                event = ImmuneEvent(
                    threat_type=antibody_match.target_signature.threat_type,
                    particle_id=particle.id,
                    response=ImmuneResponse.ADAPTIVE_SPECIFIC,
                    effectiveness=neutralization,
                    details=f"Antibody {antibody_match.antibody_id} neutralized"
                )
                self.immune_log.append(event)
                self.neutralized_count += 1
                return False, event
        
        # 4. Statistical anomaly detection
        anomaly_score = self._compute_anomaly(particle)
        if anomaly_score > 0.85:
            sig = ThreatSignature(
                threat_type=ThreatType.ADVERSARIAL,
                dimensional_pattern=particle.dimensions.values.copy(),
                confidence=anomaly_score
            )
            event = self._mount_response(particle, sig, ImmuneResponse.QUARANTINE)
            return False, event
        
        return True, None

    def _innate_screen(self, particle: CognitiveParticle) -> Optional[ThreatSignature]:
        """Fast non-specific threat detection."""
        for sig in self.threat_signatures.values():
            if sig.matches(particle, threshold=0.75):
                return sig
        return None

    def _adaptive_screen(self, particle: CognitiveParticle) -> Optional[Antibody]:
        """Specific antibody-mediated detection."""
        for ab in self.antibodies.values():
            if ab.target_signature.matches(particle, threshold=0.8):
                return ab
        return None

    def _compute_anomaly(self, particle: CognitiveParticle) -> float:
        """
        Statistical anomaly score.
        Particles far from the population distribution are suspicious.
        """
        # Check for dimensional extremes (adversarial inputs often saturate dimensions)
        values = particle.dimensions.values
        extreme_dims = sum(1 for v in values if v > 0.95 or v < 0.05)
        extreme_ratio = extreme_dims / N_DIMENSIONS
        
        # Check uncertainty vs confidence mismatch
        stated_confidence = values[CognitiveDimension.CONFIDENCE]
        if particle.uncertainty > 0.7 and stated_confidence > 0.9:
            return 0.9  # Claims certainty while being uncertain — suspicious
        
        return extreme_ratio

    def _mount_response(self, particle: CognitiveParticle,
                         threat: ThreatSignature,
                         response_type: ImmuneResponse) -> ImmuneEvent:
        """Execute immune response against a threat."""
        self.infection_count += 1
        threat.strengthen()
        
        if response_type in [ImmuneResponse.QUARANTINE, ImmuneResponse.INNATE_FAST]:
            self.quarantine_zone[particle.id] = particle
            particle.quantum_state = QuantumState.DORMANT
            particle.energy *= 0.1
        
        elif response_type == ImmuneResponse.ELIMINATION:
            particle.quantum_state = QuantumState.EXTINCT
            particle.energy = 0.0
        
        event = ImmuneEvent(
            threat_type=threat.threat_type,
            particle_id=particle.id,
            response=response_type,
            effectiveness=threat.confidence,
            details=f"Threat type: {threat.threat_type.name}"
        )
        self.immune_log.append(event)
        
        # Learn from this encounter (create antibody)
        self._generate_antibody(threat)
        
        return event

    def _generate_antibody(self, threat: ThreatSignature) -> Antibody:
        """
        Generate a specific antibody from a threat encounter.
        Makes future detection faster and more precise.
        """
        antibody = Antibody(
            target_signature=threat,
            specificity=min(0.99, 0.5 + threat.encounter_count * 0.05),
            neutralization_power=min(0.99, 0.6 + threat.confidence * 0.3)
        )
        self.antibodies[antibody.antibody_id] = antibody
        
        # Add to memory cells
        self.memory_cells.append(threat)
        return antibody

    def review_quarantine(self) -> Tuple[List[str], List[str]]:
        """
        Periodically review quarantined particles.
        Some may have been false positives (autoimmune risk).
        Returns (released_ids, eliminated_ids)
        """
        released = []
        eliminated = []
        
        for pid, particle in list(self.quarantine_zone.items()):
            # Re-evaluate with higher threshold (benefit of doubt)
            innate = self._innate_screen(particle)
            anomaly = self._compute_anomaly(particle)
            
            if not innate and anomaly < 0.6:
                # False positive — release
                del self.quarantine_zone[pid]
                particle.quantum_state = QuantumState.SUPERPOSITION
                particle.energy = 0.5
                released.append(pid)
                self.autoimmune_risk += 0.01  # Track false positives
            elif len(self.quarantine_zone) > 100:
                # Quarantine overflow — eliminate oldest
                particle.quantum_state = QuantumState.EXTINCT
                eliminated.append(pid)
                del self.quarantine_zone[pid]
        
        return released, eliminated

    def detect_contradiction(self, particle_a: CognitiveParticle,
                              particle_b: CognitiveParticle) -> Optional[ImmuneEvent]:
        """Detect and respond to contradictory knowledge."""
        truth_a = particle_a.dimensions.values[CognitiveDimension.TRUTH]
        truth_b = particle_b.dimensions.values[CognitiveDimension.TRUTH]
        
        domain_sim = particle_a.dimensions.cosine_similarity(particle_b.dimensions)
        truth_conflict = abs(truth_a - truth_b)
        
        if domain_sim > 0.7 and truth_conflict > 0.4:
            lower_confidence = particle_a if (
                particle_a.dimensions.confidence < particle_b.dimensions.confidence
            ) else particle_b
            
            sig = ThreatSignature(
                threat_type=ThreatType.CONTRADICTION,
                dimensional_pattern=lower_confidence.dimensions.values.copy(),
                confidence=truth_conflict
            )
            event = self._mount_response(
                lower_confidence, sig, ImmuneResponse.QUARANTINE
            )
            self.known_contradictions[event.event_id] = (particle_a.id, particle_b.id)
            return event
        return None

    def immune_status(self) -> Dict:
        return {
            "immune_strength": round(self.immune_strength, 3),
            "antibodies": len(self.antibodies),
            "memory_cells": len(self.memory_cells),
            "quarantine_size": len(self.quarantine_zone),
            "self_registry_size": len(self.self_registry),
            "infections_detected": self.infection_count,
            "neutralizations": self.neutralized_count,
            "autoimmune_risk": round(self.autoimmune_risk, 3),
            "known_threats": len(self.threat_signatures),
            "total_events": len(self.immune_log),
        }