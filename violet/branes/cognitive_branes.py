"""
Cognitive Branes
================
Every MCP server is an information brane.
Branes are cognitive realms — higher-dimensional surfaces
through which context strings pass.

Branes:
  Research Brane   - Knowledge acquisition realm
  Memory Brane     - Persistent storage realm  
  Simulation Brane - Hypothesis testing realm
  Execution Brane  - Action & tool realm
  Social Brane     - Collaborative intelligence realm
"""

from __future__ import annotations

import time
import asyncio
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Set, Callable, Awaitable

import numpy as np

from core.constants import (
    MAX_BRANE_DEPTH, K_CARRYING, COGNITIVE_PLANCK,
    N_DIMENSIONS, CognitiveDimension
)
from particles.cognitive_particles import (
    CognitiveParticle, Memoryon, Evidon, Hypotheon, Reasonon, Emergon
)
from fields.cognitive_fields import UniversalCognitiveField, FieldType
from strings.context_strings import ContextString, StringNetwork, StringTopology


class BraneType(Enum):
    RESEARCH = auto()
    MEMORY = auto()
    SIMULATION = auto()
    EXECUTION = auto()
    SOCIAL = auto()


class BraneHealth(Enum):
    HEALTHY = auto()
    DEGRADED = auto()
    OVERLOADED = auto()
    OFFLINE = auto()


@dataclass
class BraneMetrics:
    particles_hosted: int = 0
    strings_passing_through: int = 0
    query_count: int = 0
    success_rate: float = 1.0
    avg_response_time: float = 0.0
    last_activity: float = field(default_factory=time.time)
    cross_brane_connections: int = 0


class CognitiveBrane(ABC):
    """
    A cognitive realm — higher-dimensional surface.
    Multiple strings pass through each brane.
    The same string can pass through multiple branes.
    """

    def __init__(self, brane_type: BraneType, name: str,
                 mcp_url: Optional[str] = None):
        self.id: str = f"brane:{brane_type.name.lower()}:{name}"
        self.brane_type: BraneType = brane_type
        self.name: str = name
        self.mcp_url: Optional[str] = mcp_url

        self.particles: Dict[str, CognitiveParticle] = {}
        self.hosted_strings: Set[str] = set()
        self.metrics: BraneMetrics = BraneMetrics()
        self.health: BraneHealth = BraneHealth.HEALTHY

        # Brane-specific properties
        self.temperature: float = 1.0      # Higher = more exploratory
        self.energy_capacity: float = float(K_CARRYING)
        self.current_energy: float = 0.0

        # Cross-brane connection strings
        self.inter_brane_strings: Dict[str, ContextString] = {}

        self.birth_time: float = time.time()

    def can_accept(self) -> bool:
        """Check if brane has capacity for more particles."""
        return (len(self.particles) < K_CARRYING and
                self.health != BraneHealth.OFFLINE)

    def ingest_particle(self, particle: CognitiveParticle) -> bool:
        if not self.can_accept():
            return False
        self.particles[particle.id] = particle
        self.metrics.particles_hosted = len(self.particles)
        return True

    def connect_to(self, other_brane: CognitiveBrane,
                   string_net: StringNetwork,
                   seed_particle_a: str, seed_particle_b: str) -> ContextString:
        """Create an inter-brane connection string."""
        s = ContextString(
            endpoint_a_id=seed_particle_a,
            endpoint_b_id=seed_particle_b,
            topology=StringTopology.OPEN
        )
        s.brane_a = self.id
        s.brane_b = other_brane.id
        s.crosses_branes = True
        string_net.add_string(s)
        self.inter_brane_strings[s.id] = s
        self.metrics.cross_brane_connections += 1
        return s

    @abstractmethod
    async def process_query(self, query: str,
                             context: Dict) -> Dict[str, Any]:
        """Process a query within this brane's domain."""
        pass

    @abstractmethod
    def native_particle_type(self) -> type:
        """The primary particle type this brane produces."""
        pass

    def health_check(self) -> BraneHealth:
        load = len(self.particles) / K_CARRYING
        if load > 0.9:
            self.health = BraneHealth.OVERLOADED
        elif load > 0.7:
            self.health = BraneHealth.DEGRADED
        else:
            self.health = BraneHealth.HEALTHY
        return self.health

    def get_active_particles(self, limit: int = 100) -> List[CognitiveParticle]:
        from particles.cognitive_particles import QuantumState
        active = [p for p in self.particles.values()
                  if p.quantum_state != QuantumState.EXTINCT]
        return sorted(active, key=lambda p: p.energy, reverse=True)[:limit]

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "type": self.brane_type.name,
            "name": self.name,
            "health": self.health.name,
            "particles": len(self.particles),
            "capacity": K_CARRYING,
            "load": len(self.particles) / K_CARRYING,
            "metrics": {
                "queries": self.metrics.query_count,
                "success_rate": self.metrics.success_rate,
                "cross_brane_connections": self.metrics.cross_brane_connections,
            }
        }


class ResearchBrane(CognitiveBrane):
    """
    Knowledge acquisition realm.
    Interfaces with external knowledge sources.
    Produces Evidons from research activities.
    """

    def __init__(self, sources: Optional[List[str]] = None):
        super().__init__(BraneType.RESEARCH, "research")
        self.knowledge_sources: List[str] = sources or []
        self.active_searches: Dict[str, Dict] = {}
        self.discovered_topics: Set[str] = set()

    def native_particle_type(self) -> type:
        return Evidon

    async def process_query(self, query: str, context: Dict) -> Dict[str, Any]:
        self.metrics.query_count += 1
        start = time.time()

        # Generate Evidon from research
        evidon = Evidon(
            content=f"Research result for: {query}",
            source="research_brane",
            evidence_type="synthesized",
            reliability=0.7
        )
        self.ingest_particle(evidon)
        self.discovered_topics.add(query)

        elapsed = time.time() - start
        self.metrics.avg_response_time = (
            0.9 * self.metrics.avg_response_time + 0.1 * elapsed
        )

        return {
            "brane": self.id,
            "particle_id": evidon.id,
            "content": evidon.content,
            "elapsed": elapsed
        }

    def get_frontier_topics(self) -> List[str]:
        """Topics at the frontier of knowledge — high curiosity value."""
        return list(self.discovered_topics)[-20:]


class MemoryBrane(CognitiveBrane):
    """
    Persistent memory realm.
    Long-term storage with consolidation dynamics.
    Produces Memoryons.
    """

    def __init__(self):
        super().__init__(BraneType.MEMORY, "memory")
        self.consolidation_threshold: float = 5.0
        self.memory_index: Dict[str, List[str]] = {}  # tag → particle_ids

    def native_particle_type(self) -> type:
        return Memoryon

    def store(self, content: str, confidence: float = 0.8,
              tags: Optional[List[str]] = None) -> Memoryon:
        m = Memoryon(content=content, confidence=confidence)
        if tags:
            m.tags = tags
            for tag in tags:
                if tag not in self.memory_index:
                    self.memory_index[tag] = []
                self.memory_index[tag].append(m.id)
        self.ingest_particle(m)
        return m

    def recall_by_tag(self, tag: str) -> List[Memoryon]:
        ids = self.memory_index.get(tag, [])
        return [self.particles[pid] for pid in ids
                if pid in self.particles]

    async def process_query(self, query: str, context: Dict) -> Dict[str, Any]:
        self.metrics.query_count += 1
        # Search for relevant memories
        results = []
        for pid, p in self.particles.items():
            if query.lower() in p.content.lower():
                p.activate()
                results.append(p.to_dict())
        return {
            "brane": self.id,
            "results": results[:10],
            "total_memories": len(self.particles)
        }


class SimulationBrane(CognitiveBrane):
    """
    Hypothesis testing realm.
    Runs future trajectory simulations.
    Reality simulation before choosing answers.
    """

    def __init__(self):
        super().__init__(BraneType.SIMULATION, "simulation")
        self.active_simulations: Dict[str, Dict] = {}
        self.trajectory_history: List[Dict] = []

    def native_particle_type(self) -> type:
        return Hypotheon

    def generate_trajectories(
        self, hypothesis: str, n_trajectories: int = 5
    ) -> List[Dict]:
        """
        Generate multiple future trajectories.
        Simulate competing hypotheses.
        Compare outcomes.
        """
        trajectories = []
        for i in range(n_trajectories):
            confidence = max(0.1, 1.0 - i * 0.15)
            hyp = Hypotheon(
                content=f"Trajectory {i+1}: {hypothesis}",
                confidence=confidence,
                speculation_depth=i + 1
            )
            self.ingest_particle(hyp)
            trajectories.append({
                "id": hyp.id,
                "trajectory": i + 1,
                "hypothesis": hyp.content,
                "confidence": confidence,
                "fitness": hyp.fitness(),
                "risk": float(hyp.dimensions.values[CognitiveDimension.RISK])
            })

        return sorted(trajectories, key=lambda t: t["fitness"], reverse=True)

    def select_robust_trajectory(self, trajectories: List[Dict]) -> Dict:
        """
        Prefer solutions robust across multiple future states.
        Robustness = high confidence AND low risk.
        """
        if not trajectories:
            return {}
        # Robustness score = confidence * (1 - risk)
        for t in trajectories:
            t["robustness"] = t["confidence"] * (1.0 - t["risk"])
        return max(trajectories, key=lambda t: t["robustness"])

    async def process_query(self, query: str, context: Dict) -> Dict[str, Any]:
        self.metrics.query_count += 1
        trajectories = self.generate_trajectories(query)
        best = self.select_robust_trajectory(trajectories)
        self.trajectory_history.append({"query": query, "best": best})
        return {
            "brane": self.id,
            "trajectories": trajectories,
            "recommended": best
        }


class ExecutionBrane(CognitiveBrane):
    """
    Action and tool realm.
    Tool execution = observation event.
    Observation collapses quantum superposition.
    """

    def __init__(self):
        super().__init__(BraneType.EXECUTION, "execution")
        self.registered_tools: Dict[str, Callable] = {}
        self.execution_log: List[Dict] = []
        self.mcp_connections: Dict[str, str] = {}  # name → url

    def native_particle_type(self) -> type:
        return Reasonon

    def register_tool(self, name: str, handler: Callable,
                      mcp_url: Optional[str] = None) -> None:
        self.registered_tools[name] = handler
        if mcp_url:
            self.mcp_connections[name] = mcp_url

    async def execute_tool(self, tool_name: str,
                            args: Dict, particle_id: Optional[str] = None) -> Dict:
        """
        Execute a tool — this is an observation event.
        Collapses quantum superposition of related particles.
        """
        start = time.time()
        success = False
        result = {}

        try:
            if tool_name in self.registered_tools:
                handler = self.registered_tools[tool_name]
                if asyncio.iscoroutinefunction(handler):
                    result = await handler(**args)
                else:
                    result = handler(**args)
                success = True
        except Exception as e:
            result = {"error": str(e)}

        latency = time.time() - start
        log_entry = {
            "tool": tool_name,
            "success": success,
            "latency": latency,
            "timestamp": time.time(),
            "particle_id": particle_id
        }
        self.execution_log.append(log_entry)

        # Collapse related quantum states
        if particle_id and particle_id in self.particles:
            self.particles[particle_id].collapse({
                "tool": tool_name,
                "result": result,
                "latency": latency
            })

        return {
            "brane": self.id,
            "tool": tool_name,
            "success": success,
            "result": result,
            "latency": latency
        }

    async def process_query(self, query: str, context: Dict) -> Dict[str, Any]:
        self.metrics.query_count += 1
        tool_name = context.get("tool", "default")
        args = context.get("args", {})
        return await self.execute_tool(tool_name, args)


class SocialBrane(CognitiveBrane):
    """
    Collaborative intelligence realm.
    Multi-agent cognitive coordination.
    Swarm intelligence patterns.
    """

    def __init__(self):
        super().__init__(BraneType.SOCIAL, "social")
        self.agents: Dict[str, Dict] = {}
        self.consensus_particles: Dict[str, float] = {}  # pid → consensus_score
        self.dissent_registry: List[Tuple] = []

    def native_particle_type(self) -> type:
        return Emergon

    def register_agent(self, agent_id: str, capabilities: List[str]) -> None:
        self.agents[agent_id] = {
            "capabilities": capabilities,
            "trust": 0.7,
            "contributions": 0
        }

    def build_consensus(self, particle_id: str, votes: Dict[str, float]) -> float:
        """
        Swarm intelligence: consensus through weighted voting.
        Returns consensus strength.
        """
        if not votes:
            return 0.0
        weighted_sum = sum(
            vote * self.agents.get(aid, {}).get("trust", 0.5)
            for aid, vote in votes.items()
        )
        total_weight = sum(
            self.agents.get(aid, {}).get("trust", 0.5)
            for aid in votes
        )
        score = weighted_sum / max(total_weight, COGNITIVE_PLANCK)
        self.consensus_particles[particle_id] = score
        return score

    async def process_query(self, query: str, context: Dict) -> Dict[str, Any]:
        self.metrics.query_count += 1
        agent_responses = []
        for agent_id, agent_data in list(self.agents.items())[:5]:
            agent_responses.append({
                "agent": agent_id,
                "response": f"Agent {agent_id} perspective on: {query}",
                "confidence": agent_data["trust"]
            })
        return {
            "brane": self.id,
            "agent_responses": agent_responses,
            "consensus_required": len(agent_responses) > 1
        }


class BraneNetwork:
    """
    The interconnected network of all cognitive branes.
    Manages inter-brane strings and cross-realm routing.
    """

    def __init__(self):
        self.branes: Dict[str, CognitiveBrane] = {}
        self.string_network: StringNetwork = StringNetwork()
        self.routing_table: Dict[str, List[str]] = {}

    def register_brane(self, brane: CognitiveBrane) -> None:
        self.branes[brane.id] = brane

    def get_brane(self, brane_type: BraneType) -> Optional[CognitiveBrane]:
        for b in self.branes.values():
            if b.brane_type == brane_type:
                return b
        return None

    async def route_query(self, query: str, context: Dict,
                           target_branes: Optional[List[BraneType]] = None) -> Dict:
        """
        Route a query through relevant branes.
        Results aggregate across the brane network.
        """
        targets = target_branes or list(BraneType)
        results = {}
        for bt in targets:
            brane = self.get_brane(bt)
            if brane and brane.health != BraneHealth.OFFLINE:
                try:
                    r = await brane.process_query(query, context)
                    results[bt.name] = r
                except Exception as e:
                    results[bt.name] = {"error": str(e)}
        return results

    def inter_brane_connection_strength(
        self, brane_a_type: BraneType, brane_b_type: BraneType
    ) -> float:
        """
        Strength of connection between two branes.
        Based on shared string activations.
        """
        ba = self.get_brane(brane_a_type)
        bb = self.get_brane(brane_b_type)
        if not ba or not bb:
            return 0.0
        shared = set(ba.inter_brane_strings.keys()) & set(bb.inter_brane_strings.keys())
        return min(1.0, len(shared) / 10.0)

    def health_report(self) -> Dict:
        return {
            brane_id: brane.to_dict()
            for brane_id, brane in self.branes.items()
        }