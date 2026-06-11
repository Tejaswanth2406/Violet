"""
Dream Engine
============
Brains don't only learn while awake.
They REORGANIZE during sleep.

The Dream Engine runs as a background process:
  - Discovers hidden wormholes (distant concept connections)
  - Compresses redundant memories (memory consolidation)
  - Repairs degraded field structures
  - Generates speculative hypotheses
  - Replays and strengthens important pathways
  - Prunes wasteful connections

REM sleep analog: active hypothesis generation
Deep sleep analog: memory consolidation + compression
Hypnagogia analog: novel connection discovery at threshold states

No user input required.
The system dreams autonomously.
"""

from __future__ import annotations

import asyncio
import math
import time
import uuid
import random
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from core.constants import (
    N_DIMENSIONS, COGNITIVE_PLANCK, GAMMA_DECAY,
    WORMHOLE_THRESHOLD, CognitiveDimension
)
from particles.cognitive_particles import (
    CognitiveParticle, Hypotheon, Emergon, DimensionalVector, QuantumState
)
from strings.context_strings import ContextString, StringTopology


class DreamStage(Enum):
    NREM_1 = auto()     # Light: pruning, cleanup
    NREM_2 = auto()     # Medium: memory consolidation
    NREM_3 = auto()     # Deep: structural repair
    REM = auto()        # Active: hypothesis generation, wormholes
    HYPNAGOGIA = auto() # Threshold: most creative, most chaotic


@dataclass
class DreamReport:
    """Record of a single dream cycle."""
    dream_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    stage: DreamStage = DreamStage.REM
    started_at: float = field(default_factory=time.time)
    ended_at: Optional[float] = None
    
    # What happened
    wormholes_discovered: List[Tuple[str, str]] = field(default_factory=list)
    memories_compressed: int = 0
    hypotheses_generated: List[str] = field(default_factory=list)
    strings_pruned: int = 0
    fields_repaired: int = 0
    emergent_concepts: List[str] = field(default_factory=list)
    
    # Quality metrics
    insight_score: float = 0.0
    consolidation_score: float = 0.0

    def duration(self) -> float:
        if self.ended_at:
            return self.ended_at - self.started_at
        return time.time() - self.started_at


class DreamEngine:
    """
    The autonomous background cognitive reorganizer.
    
    Runs independently of user queries.
    Improves the cognitive universe during idle time.
    
    Dream cycle stages:
    NREM-1: Light pruning
    NREM-2: Memory consolidation (replay + strengthen)
    NREM-3: Deep structural repair
    REM:    Active hypothesis generation, wormhole discovery
    
    Key insight: The best connections are found when not actively searching.
    """

    def __init__(self):
        self.is_dreaming: bool = False
        self.current_stage: DreamStage = DreamStage.NREM_1
        self.dream_history: List[DreamReport] = []
        self.total_dream_cycles: int = 0
        self.total_insight_generated: float = 0.0
        
        # Dream parameters
        self.rem_ratio: float = 0.25          # Fraction of sleep in REM
        self.consolidation_threshold: float = 3.0  # Min activations to consolidate
        self.compression_ratio: float = 0.7   # Keep 70% after compression
        
        # Background task handle
        self._dream_task: Optional[asyncio.Task] = None
        self._running: bool = False

    async def start_dream_loop(
        self,
        particle_registry: Dict[str, CognitiveParticle],
        string_network,
        curiosity_engine,
        interval_seconds: float = 300.0
    ) -> None:
        """
        Start the autonomous dream loop.
        Runs continuously in background.
        """
        self._running = True
        while self._running:
            await asyncio.sleep(interval_seconds)
            if not self.is_dreaming:
                report = await self.dream_cycle(
                    particle_registry, string_network, curiosity_engine
                )
                self.dream_history.append(report)

    def stop(self) -> None:
        self._running = False

    async def dream_cycle(
        self,
        particles: Dict[str, CognitiveParticle],
        string_network,
        curiosity_engine
    ) -> DreamReport:
        """
        Execute a full dream cycle through all stages.
        """
        self.is_dreaming = True
        self.total_dream_cycles += 1
        report = DreamReport()
        particle_list = list(particles.values())

        # Stage 1: NREM-1 — Light pruning
        report.stage = DreamStage.NREM_1
        pruned = await self._nrem1_prune(particles, string_network)
        report.strings_pruned = pruned

        # Stage 2: NREM-2 — Memory consolidation
        report.stage = DreamStage.NREM_2
        consolidated = await self._nrem2_consolidate(particle_list)
        report.memories_compressed = consolidated

        # Stage 3: NREM-3 — Structural repair
        report.stage = DreamStage.NREM_3
        repaired = await self._nrem3_repair(particle_list, string_network)
        report.fields_repaired = repaired

        # Stage 4: REM — Active hypothesis generation
        report.stage = DreamStage.REM
        hyps, wormholes = await self._rem_generate(
            particle_list, string_network, curiosity_engine
        )
        report.hypotheses_generated = hyps
        report.wormholes_discovered = wormholes

        # Stage 5: Hypnagogia — Novel emergence
        report.stage = DreamStage.HYPNAGOGIA
        emergents = await self._hypnagogia_emerge(particle_list)
        report.emergent_concepts = emergents

        # Score the dream
        report.insight_score = (
            len(wormholes) * 0.3 +
            len(hyps) * 0.1 +
            len(emergents) * 0.2 +
            consolidated * 0.01
        )
        report.consolidation_score = consolidated / max(len(particle_list), 1)
        report.ended_at = time.time()

        self.total_insight_generated += report.insight_score
        self.is_dreaming = False
        return report

    async def _nrem1_prune(
        self, particles: Dict[str, CognitiveParticle], string_network
    ) -> int:
        """Light sleep: prune dormant strings and low-energy particles."""
        # Prune dormant strings
        pruned = string_network.prune_dormant(max_dormant_age=1800.0)
        
        # Fade low-energy particles
        faded = 0
        for pid, p in particles.items():
            p.decay()
            if p.energy < COGNITIVE_PLANCK * 10 and p.activation_frequency == 0:
                p.quantum_state = QuantumState.DORMANT
                faded += 1
        
        await asyncio.sleep(0)  # Yield control
        return pruned + faded

    async def _nrem2_consolidate(
        self, particles: List[CognitiveParticle]
    ) -> int:
        """
        Memory consolidation:
        - Replay high-activation particles
        - Strengthen important pathways
        - Compress similar memories
        """
        consolidated = 0
        
        # Sort by activation frequency
        high_activation = sorted(
            particles,
            key=lambda p: p.activation_frequency,
            reverse=True
        )[:50]
        
        for particle in high_activation:
            if particle.activation_frequency >= self.consolidation_threshold:
                particle.activate(strength=0.3)  # Replay strengthening
                if hasattr(particle, 'consolidate'):
                    particle.consolidate()
                consolidated += 1
        
        # Find and merge near-identical particles
        for i, pa in enumerate(particles[:30]):
            for pb in particles[i+1:i+10]:
                sim = pa.dimensions.cosine_similarity(pb.dimensions)
                if sim > 0.95 and pa.id != pb.id:
                    # Merge: keep the more activated one
                    if pb.activation_frequency > pa.activation_frequency:
                        pa, pb = pb, pa
                    pa.energy = min(pa.energy + pb.energy * 0.5, 10.0)
                    pb.quantum_state = QuantumState.DORMANT
                    consolidated += 1
        
        await asyncio.sleep(0)
        return consolidated

    async def _nrem3_repair(
        self, particles: List[CognitiveParticle], string_network
    ) -> int:
        """
        Deep sleep: repair degraded field structures.
        - Restore broken strings
        - Recalibrate dimensional vectors
        - Fix orphaned particles
        """
        repaired = 0
        
        # Find orphaned particles (no string connections)
        connected = set()
        for s in string_network.strings.values():
            connected.add(s.endpoint_a)
            connected.add(s.endpoint_b)
        
        for particle in particles:
            if particle.id not in connected and particle.energy > 0.5:
                # Try to reconnect orphan to nearest particle
                best_match = None
                best_sim = 0.3
                for other in particles[:20]:
                    if other.id != particle.id and other.id in connected:
                        sim = particle.dimensions.cosine_similarity(other.dimensions)
                        if sim > best_sim:
                            best_sim = sim
                            best_match = other
                
                if best_match:
                    new_string = ContextString(
                        endpoint_a_id=particle.id,
                        endpoint_b_id=best_match.id,
                        initial_energy=best_sim * 0.5
                    )
                    new_string.semantic_resonance = best_sim
                    string_network.add_string(new_string)
                    repaired += 1
        
        await asyncio.sleep(0)
        return repaired

    async def _rem_generate(
        self,
        particles: List[CognitiveParticle],
        string_network,
        curiosity_engine
    ) -> Tuple[List[str], List[Tuple[str, str]]]:
        """
        REM sleep: the most active dream state.
        Generate hypotheses, discover wormholes.
        """
        hypotheses_generated = []
        wormholes_found = []
        
        # Generate hypotheses from high-curiosity regions
        high_uncertainty = sorted(
            particles, key=lambda p: p.uncertainty, reverse=True
        )[:10]
        
        for particle in high_uncertainty:
            if random.random() < 0.3:  # Stochastic — like dream creativity
                hyp = Hypotheon(
                    content=f"[DREAM-HYP] What if {particle.content[:60]} implies X?",
                    confidence=0.2,
                    speculation_depth=2
                )
                hypotheses_generated.append(hyp.id)
                
                # Add to curiosity engine
                curiosity_engine.uncertainty_gradient += (
                    particle.uncertainty * particle.dimensions.values * 0.01
                )
        
        # Discover wormholes by random walk
        if len(particles) > 10:
            sample_size = min(20, len(particles))
            sampled = random.sample(particles, sample_size)
            
            for i, pa in enumerate(sampled):
                for pb in sampled[i+1:]:
                    sim = pa.dimensions.cosine_similarity(pb.dimensions)
                    # Dream wormholes: find non-obvious connections
                    if 0.7 < sim < 0.9:  # Not too obvious, not too distant
                        wormholes_found.append((pa.id, pb.id))
                        
                        # Create the wormhole string
                        wh_string = ContextString(
                            endpoint_a_id=pa.id,
                            endpoint_b_id=pb.id,
                            topology=StringTopology.WORMHOLE,
                            initial_energy=sim * 0.7
                        )
                        wh_string.semantic_resonance = sim
                        string_network.add_string(wh_string)
                        
                        if len(wormholes_found) >= 5:
                            break
                if len(wormholes_found) >= 5:
                    break
        
        await asyncio.sleep(0)
        return hypotheses_generated, wormholes_found

    async def _hypnagogia_emerge(
        self, particles: List[CognitiveParticle]
    ) -> List[str]:
        """
        Hypnagogic state: the threshold between sleep and wake.
        Most creative, most chaotic. Novel concepts emerge here.
        
        This is where the most surprising emergent concepts appear.
        """
        emergents = []
        
        if len(particles) < 3:
            await asyncio.sleep(0)
            return emergents
        
        # Random combinations at the threshold of sense/nonsense
        for _ in range(3):
            # Pick 2-3 random particles and attempt fusion
            sample = random.sample(particles, min(3, len(particles)))
            
            # Compute combined dimensional signature
            combined = np.zeros(N_DIMENSIONS)
            labels = []
            for p in sample:
                combined += p.dimensions.values * p.energy
                labels.append(p.content[:20])
            
            combined /= max(sum(p.energy for p in sample), COGNITIVE_PLANCK)
            combined = np.clip(combined, 0, 1)
            
            # Only emerge if the combination is novel (not too similar to existing)
            is_novel = True
            for existing in particles[:20]:
                if DimensionalVector(values=combined).cosine_similarity(
                    existing.dimensions
                ) > 0.9:
                    is_novel = False
                    break
            
            if is_novel:
                emergon = Emergon(
                    content=f"[DREAM-EMERGE] {' + '.join(labels[:2])}",
                    origin_string_ids=[p.id for p in sample],
                    emergence_strength=float(np.linalg.norm(combined)) / math.sqrt(N_DIMENSIONS)
                )
                emergon.dimensions = DimensionalVector(values=combined)
                emergents.append(emergon.id)
        
        await asyncio.sleep(0)
        return emergents

    def dream_summary(self) -> Dict:
        recent = self.dream_history[-5:]
        avg_insight = sum(r.insight_score for r in recent) / max(len(recent), 1)
        total_wh = sum(len(r.wormholes_discovered) for r in self.dream_history)
        total_hyp = sum(len(r.hypotheses_generated) for r in self.dream_history)
        
        return {
            "total_dream_cycles": self.total_dream_cycles,
            "is_dreaming": self.is_dreaming,
            "current_stage": self.current_stage.name,
            "total_wormholes_discovered": total_wh,
            "total_hypotheses_generated": total_hyp,
            "total_insight_generated": round(self.total_insight_generated, 3),
            "avg_recent_insight": round(avg_insight, 3),
            "recent_cycles": len(recent),
        }