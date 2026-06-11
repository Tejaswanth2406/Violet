"""
Cognitive Physics Engine (CPE)
==============================
The Grand Unified Cognitive System.

Ω = Universal Cognitive Field
  ├── Cognitive String Network (fundamental)
  ├── Cognitive Particles (Memoryon, Evidon, Hypotheon, Reasonon, Emergon, Darkon)
  ├── Cognitive Fields (Memory, Intent, Evidence, Reasoning, Tool, Curiosity)
  ├── Cognitive Branes (Research, Memory, Simulation, Execution, Social)
  ├── Ecosystem Layer (Evolution, Selection, Emergence)
  ├── Curiosity Engine (Dark Energy, Contradictions, Gaps)
  └── Reality Simulator (Multi-trajectory planning)

This is not a RAG system.
This is not a graph database.
This is not a vector store.
This is a cognitive universe.
"""

from __future__ import annotations

import time
import asyncio
import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from core.constants import (
    N_DIMENSIONS, CognitiveDimension, COLLAPSE_CERTAINTY,
    WORMHOLE_THRESHOLD
)
from particles.cognitive_particles import (
    CognitiveParticle, Memoryon, Evidon, Hypotheon, Reasonon, Emergon,
    DimensionalVector, ParticleType, QuantumState
)
from strings.context_strings import ContextString, StringNetwork, StringTopology
from fields.cognitive_fields import (
    UniversalCognitiveField, FieldType, MemoryField
)
from branes.cognitive_branes import (
    BraneNetwork, BraneType, CognitiveBrane,
    ResearchBrane, MemoryBrane, SimulationBrane, ExecutionBrane, SocialBrane
)
from ecosystem.cognitive_ecosystem import CognitiveEcosystem
from curiosity.curiosity_engine import CuriosityEngine, CuriosityImpulse
from simulation.reality_simulator import RealitySimulator, SimulationResult

logger = logging.getLogger(__name__)


@dataclass
class CPEQueryResult:
    """The result of a CPE query — emergent, not retrieved."""
    query: str
    primary_particles: List[CognitiveParticle]
    resonance_scores: Dict[str, float]
    simulation_result: Optional[SimulationResult]
    curiosity_impulse: Optional[CuriosityImpulse]
    wormholes_discovered: List[str]
    reasoning_chain: List[str]
    confidence: float
    uncertainty: float
    dark_matter_hints: List[str]
    response_text: str
    elapsed_ms: float

    def to_dict(self) -> Dict:
        return {
            "query": self.query,
            "primary_particles": [p.to_dict() for p in self.primary_particles[:5]],
            "top_resonances": dict(list(sorted(
                self.resonance_scores.items(), key=lambda x: x[1], reverse=True
            ))[:5]),
            "confidence": round(self.confidence, 3),
            "uncertainty": round(self.uncertainty, 3),
            "wormholes_discovered": self.wormholes_discovered,
            "reasoning_chain": self.reasoning_chain,
            "dark_matter_hints": self.dark_matter_hints,
            "simulation": self.simulation_result.to_dict() if self.simulation_result else None,
            "curiosity_impulse": {
                "question": self.curiosity_impulse.question,
                "urgency": self.curiosity_impulse.urgency,
                "source": self.curiosity_impulse.source
            } if self.curiosity_impulse else None,
            "response": self.response_text,
            "elapsed_ms": round(self.elapsed_ms, 2),
        }


class CognitivePhysicsEngine:
    """
    The central CPE orchestrator.
    
    All knowledge, memory, tools, and reasoning exists within this engine.
    Nothing is stored. Everything resonates.
    """

    def __init__(self, config: Optional[Dict] = None):
        cfg = config or {}
        self.name: str = cfg.get("name", "CPE-Omega")
        self.version: str = "1.0.0"

        logger.info(f"[CPE] Initializing {self.name}...")

        # ── Core infrastructure ──────────────────────────────────
        self.universal_field = UniversalCognitiveField()
        self.string_network = StringNetwork()
        self.brane_network = BraneNetwork()
        self.ecosystem = CognitiveEcosystem()
        self.curiosity_engine = CuriosityEngine()
        self.reality_simulator = RealitySimulator(
            n_trajectories=cfg.get("n_trajectories", 5),
            simulation_depth=cfg.get("simulation_depth", 3)
        )

        # ── Initialize branes ────────────────────────────────────
        self._init_branes()

        # ── Global particle registry ─────────────────────────────
        self.all_particles: Dict[str, CognitiveParticle] = {}

        # ── Operational stats ─────────────────────────────────────
        self.query_count: int = 0
        self.birth_time: float = time.time()
        self.last_evolution: float = time.time()

        logger.info(f"[CPE] {self.name} online. The cognitive universe is alive.")

    def _init_branes(self) -> None:
        """Initialize all cognitive branes."""
        branes = [
            ResearchBrane(),
            MemoryBrane(),
            SimulationBrane(),
            ExecutionBrane(),
            SocialBrane(),
        ]
        for brane in branes:
            self.brane_network.register_brane(brane)
        logger.info(f"[CPE] {len(branes)} cognitive branes initialized")

    # ─────────────────────────────────────────────────────────────
    # Particle Ingestion
    # ─────────────────────────────────────────────────────────────

    def ingest(
        self,
        content: str,
        particle_type: str = "memoryon",
        source: Optional[str] = None,
        tags: Optional[List[str]] = None,
        dimensions: Optional[Dict[str, float]] = None,
        confidence: float = 0.8
    ) -> CognitiveParticle:
        """
        Ingest new knowledge into the cognitive universe.
        Creates appropriate particle, registers with fields and branes.
        """
        # Build dimensional vector
        dim_values = np.zeros(N_DIMENSIONS)
        dim_values[CognitiveDimension.CONFIDENCE] = confidence
        dim_values[CognitiveDimension.TRUTH] = 0.7
        dim_values[CognitiveDimension.UTILITY] = 0.6
        dim_values[CognitiveDimension.NOVELTY] = 0.5

        if dimensions:
            for name, val in dimensions.items():
                idx = CognitiveDimension.NAMES.index(name) if name in CognitiveDimension.NAMES else -1
                if idx >= 0:
                    dim_values[idx] = float(val)

        dim_vec = DimensionalVector(values=dim_values)

        # Create particle
        ptype = particle_type.lower()
        if ptype == "memoryon":
            particle = Memoryon(content, confidence=confidence, dimensions=dim_vec)
        elif ptype == "evidon":
            particle = Evidon(content, source=source or "unknown", dimensions=dim_vec)
        elif ptype == "hypotheon":
            particle = Hypotheon(content, confidence=confidence, dimensions=dim_vec)
        elif ptype == "reasonon":
            particle = Reasonon(content, antecedent_ids=[], consequent_ids=[], dimensions=dim_vec)
        else:
            particle = Memoryon(content, confidence=confidence, dimensions=dim_vec)

        if tags:
            particle.tags = tags

        # Register everywhere
        self.all_particles[particle.id] = particle
        self.universal_field.register_particle(particle, FieldType.MEMORY)
        self.ecosystem.register_particle(particle)

        # Register in memory brane if appropriate
        mem_brane: MemoryBrane = self.brane_network.get_brane(BraneType.MEMORY)
        if mem_brane and ptype == "memoryon":
            mem_brane.store(content, confidence=confidence, tags=tags)

        # Create string connections to similar particles
        self._auto_connect(particle)

        logger.debug(f"[CPE] Ingested {particle.particle_type.name}: {content[:50]}")
        return particle

    def _auto_connect(self, new_particle: CognitiveParticle, top_k: int = 3) -> None:
        """Automatically create strings to the most similar existing particles."""
        candidates = self.universal_field.global_resonance(
            new_particle.dimensions, top_k=top_k
        )
        for field_name, results in candidates.items():
            for particle, score in results[:2]:
                if particle.id == new_particle.id or score < 0.3:
                    continue
                s = ContextString(
                    endpoint_a_id=new_particle.id,
                    endpoint_b_id=particle.id,
                    initial_energy=score
                )
                s.semantic_resonance = score
                s.trust = score
                self.string_network.add_string(s)

    # ─────────────────────────────────────────────────────────────
    # Core Query Processing
    # ─────────────────────────────────────────────────────────────

    async def query(
        self,
        query_text: str,
        intent: Optional[str] = None,
        simulate: bool = True,
        top_k: int = 10
    ) -> CPEQueryResult:
        """
        Process a query through the full cognitive universe.
        
        This is NOT retrieval.
        This is RESONANCE.
        """
        start = time.time()
        self.query_count += 1

        # 1. Build query dimensional vector
        query_vector = self._vectorize_query(query_text)

        # 2. Set intent
        if intent:
            intent_vector = self._vectorize_query(intent)
            self.universal_field.intent_field.set_intent(intent_vector)

        # 3. Perturb all fields (query = perturbation, not retrieval)
        self.universal_field.perturb_all(query_text, query_vector)

        # 4. Global resonance across all fields
        resonance_map = self.universal_field.global_resonance(query_vector, top_k)

        # 5. Collect resonating particles
        primary_particles = []
        resonance_scores = {}
        for field_name, results in resonance_map.items():
            for particle, score in results:
                if particle.id not in resonance_scores:
                    primary_particles.append(particle)
                    resonance_scores[particle.id] = score
                    particle.activate(strength=score)

        # Sort by resonance
        primary_particles.sort(key=lambda p: resonance_scores.get(p.id, 0), reverse=True)

        # 6. Spider-web propagation through string network
        activated_ids = []
        if primary_particles:
            activated_ids = self.string_network.propagate_activation(
                primary_particles[0].id, strength=0.7, depth=2
            )
            for pid in activated_ids[:5]:
                if pid in self.all_particles:
                    p = self.all_particles[pid]
                    if p.id not in resonance_scores:
                        primary_particles.append(p)
                        resonance_scores[p.id] = 0.3

        # 7. Detect wormholes
        wormhole_candidates = self.string_network.detect_wormhole_candidates()
        new_wormholes = []
        for s_a, s_b, shared_dims in wormhole_candidates[:3]:
            wh_id = self.string_network.form_wormhole(s_a, s_b, shared_dims)
            new_wormholes.append(wh_id)

        # 8. Reality simulation
        sim_result = None
        if simulate and primary_particles:
            sim_result = self.reality_simulator.simulate(
                query_text, primary_particles[:5]
            )
            # Collapse superpositions
            for p in primary_particles[:3]:
                self.reality_simulator.superposition_collapse(p, sim_result)

        # 9. Reasoning chain
        reasoning_chain = self.universal_field.reasoning_field.build_inference_chain(
            primary_particles[0].id if primary_particles else "",
            query_vector,
            max_depth=3
        ) if primary_particles else []

        # 10. Curiosity impulse
        all_particles_list = list(self.all_particles.values())
        self.curiosity_engine.update_uncertainty_map(all_particles_list)
        curiosity_impulse = self.curiosity_engine.generate_curiosity_impulse(
            all_particles_list, context=query_text
        )

        # 11. Contradiction scan (background)
        new_contradictions = self.curiosity_engine.scan_for_contradictions(
            primary_particles[:10]
        )

        # 12. Dark matter detection
        dark_matter = self.curiosity_engine.detect_dark_matter(
            list(self.string_network.strings.values()),
            all_particles_list
        )
        dark_matter_hints = [dm.inferred_domain for dm in dark_matter[:3]]

        # 13. Compute response confidence
        if resonance_scores:
            top_scores = sorted(resonance_scores.values(), reverse=True)[:5]
            confidence = float(np.mean(top_scores))
        else:
            confidence = 0.1

        avg_uncertainty = float(np.mean([p.uncertainty for p in primary_particles[:5]])) if primary_particles else 0.9

        # 14. Synthesize response
        response_text = self._synthesize_response(
            query_text, primary_particles[:5], sim_result, confidence
        )

        elapsed_ms = (time.time() - start) * 1000

        result = CPEQueryResult(
            query=query_text,
            primary_particles=primary_particles[:5],
            resonance_scores=resonance_scores,
            simulation_result=sim_result,
            curiosity_impulse=curiosity_impulse,
            wormholes_discovered=new_wormholes,
            reasoning_chain=reasoning_chain,
            confidence=confidence,
            uncertainty=avg_uncertainty,
            dark_matter_hints=dark_matter_hints,
            response_text=response_text,
            elapsed_ms=elapsed_ms
        )

        # 15. Periodic evolution
        if time.time() - self.last_evolution > 3600:
            self.ecosystem.evolve_cycle()
            self.last_evolution = time.time()

        return result

    def _vectorize_query(self, text: str) -> DimensionalVector:
        """
        Convert text to dimensional vector.
        In production: use embedding model.
        Here: deterministic hash-based approximation.
        """
        values = np.zeros(N_DIMENSIONS)
        text_lower = text.lower()

        # Heuristic dimension assignment
        truth_words = ["fact", "true", "false", "evidence", "prove", "verify"]
        novelty_words = ["new", "novel", "unknown", "discover", "explore"]
        utility_words = ["how", "why", "use", "apply", "build", "create"]
        risk_words = ["risk", "danger", "safe", "threat", "warn", "avoid"]
        intent_words = ["want", "need", "goal", "objective", "achieve"]

        values[CognitiveDimension.TRUTH] = sum(1 for w in truth_words if w in text_lower) / len(truth_words)
        values[CognitiveDimension.NOVELTY] = sum(1 for w in novelty_words if w in text_lower) / len(novelty_words)
        values[CognitiveDimension.UTILITY] = min(1.0, sum(1 for w in utility_words if w in text_lower) / 3)
        values[CognitiveDimension.RISK] = sum(1 for w in risk_words if w in text_lower) / len(risk_words)
        values[CognitiveDimension.INTENT] = sum(1 for w in intent_words if w in text_lower) / len(intent_words)
        values[CognitiveDimension.CONFIDENCE] = 0.5
        values[CognitiveDimension.INFLUENCE] = min(1.0, len(text) / 500)
        values[CognitiveDimension.TIME] = 0.5

        # Ensure at least minimum signal
        if np.linalg.norm(values) < 0.1:
            values = np.random.rand(N_DIMENSIONS) * 0.5 + 0.2

        return DimensionalVector(values=np.clip(values, 0, 1))

    def _synthesize_response(
        self,
        query: str,
        particles: List[CognitiveParticle],
        sim: Optional[SimulationResult],
        confidence: float
    ) -> str:
        """Synthesize a response from resonating particles."""
        parts = []

        if particles:
            parts.append(f"[Resonance: {len(particles)} particles activated]")
            top = particles[0]
            parts.append(f"Primary: {top.content[:120]}")
            if len(particles) > 1:
                parts.append(f"Supporting: {particles[1].content[:80]}")

        if sim:
            rec = sim.recommended
            parts.append(
                f"[Simulation: {sim.n_trajectories} trajectories → "
                f"{rec.outcome.name} (confidence: {sim.confidence:.2f})]"
            )
            if sim.reasoning:
                parts.append(f"Reasoning: {sim.reasoning}")

        if not parts:
            parts.append(f"[No resonating particles found for: {query}]")

        return " | ".join(parts)

    # ─────────────────────────────────────────────────────────────
    # Tool Registration
    # ─────────────────────────────────────────────────────────────

    def register_tool(self, name: str, handler, mcp_url: Optional[str] = None) -> None:
        """Register a tool in the execution brane."""
        exec_brane: ExecutionBrane = self.brane_network.get_brane(BraneType.EXECUTION)
        if exec_brane:
            exec_brane.register_tool(name, handler, mcp_url)
            self.universal_field.tool_field.register_tool(name, {"name": name, "url": mcp_url})

    async def execute_tool(self, tool_name: str, args: Dict,
                            particle_id: Optional[str] = None) -> Dict:
        """Execute a tool — observation event."""
        exec_brane: ExecutionBrane = self.brane_network.get_brane(BraneType.EXECUTION)
        if not exec_brane:
            return {"error": "Execution brane not available"}
        result = await exec_brane.execute_tool(tool_name, args, particle_id)
        self.universal_field.tool_field.record_execution(
            tool_name, result["success"], result["latency"], result
        )
        return result

    # ─────────────────────────────────────────────────────────────
    # Universe Status
    # ─────────────────────────────────────────────────────────────

    def status(self) -> Dict:
        """Full cognitive universe status report."""
        return {
            "engine": self.name,
            "version": self.version,
            "age_seconds": time.time() - self.birth_time,
            "query_count": self.query_count,
            "particles": len(self.all_particles),
            "strings": self.string_network.get_stats(),
            "fields": self.universal_field.status(),
            "branes": self.brane_network.health_report(),
            "ecosystem": self.ecosystem.ecosystem_health(),
            "curiosity": self.curiosity_engine.curiosity_status(),
            "simulator": self.reality_simulator.stats(),
            "wormholes": len(self.string_network.wormholes),
        }