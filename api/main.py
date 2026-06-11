"""
CPE REST API
============
Production-grade FastAPI interface for the Cognitive Physics Engine.
"""

import asyncio
import logging
import time
from contextlib import asynccontextmanager
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Add violet package to path for imports
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "violet"))

from violet.core.engine import CognitivePhysicsEngine, CPEQueryResult
from violet.fields.cognitive_fields import FieldType

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────
# Global engine instance
# ─────────────────────────────────────────────────────────────
engine: Optional[CognitivePhysicsEngine] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize engine on startup."""
    global engine
    logger.info("[API] Starting CPE...")
    engine = CognitivePhysicsEngine(config={
        "name": "CPE-Omega-Production",
        "n_trajectories": 7,
        "simulation_depth": 3,
    })
    # Pre-seed with bootstrap knowledge
    _seed_bootstrap_knowledge(engine)
    logger.info("[API] CPE online and ready.")
    yield
    logger.info("[API] CPE shutting down.")


app = FastAPI(
    title="Cognitive Physics Engine API",
    description="A cognitive universe where knowledge resonates, not retrieves.",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _seed_bootstrap_knowledge(eng: CognitivePhysicsEngine) -> None:
    """Seed initial bootstrap particles."""
    seeds = [
        ("Knowledge is dynamic, not static", "memoryon", ["epistemology", "meta"]),
        ("Relationships are more fundamental than nodes", "memoryon", ["string_theory", "meta"]),
        ("Emergence arises from interaction, not design", "memoryon", ["emergence", "systems"]),
        ("Curiosity drives cognitive expansion", "memoryon", ["curiosity", "dark_energy"]),
        ("Contradiction is valuable information", "memoryon", ["dialectics", "meta"]),
        ("Context shapes meaning fundamentally", "memoryon", ["semantics", "context"]),
        ("Evolution applies to knowledge structures", "memoryon", ["evolution", "epistemology"]),
        ("Uncertainty is a first-class property", "memoryon", ["quantum", "epistemology"]),
    ]
    for content, ptype, tags in seeds:
        eng.ingest(content, ptype, tags=tags, confidence=0.95)


# ─────────────────────────────────────────────────────────────
# Request / Response Models
# ─────────────────────────────────────────────────────────────

class IngestRequest(BaseModel):
    content: str = Field(..., description="Knowledge content to ingest")
    particle_type: str = Field("memoryon", description="memoryon|evidon|hypotheon|reasonon")
    source: Optional[str] = Field(None, description="Source identifier")
    tags: Optional[List[str]] = Field(None, description="Classification tags")
    confidence: float = Field(0.8, ge=0.0, le=1.0)
    dimensions: Optional[Dict[str, float]] = Field(None,
        description="Override dimensional values (truth, novelty, utility, etc.)")


class QueryRequest(BaseModel):
    query: str = Field(..., description="The query to process")
    intent: Optional[str] = Field(None, description="Intent context")
    simulate: bool = Field(True, description="Run reality simulation")
    top_k: int = Field(10, ge=1, le=50)


class ToolExecutionRequest(BaseModel):
    tool_name: str
    args: Dict[str, Any] = Field(default_factory=dict)
    particle_id: Optional[str] = None


# ─────────────────────────────────────────────────────────────
# Endpoints
# ─────────────────────────────────────────────────────────────

@app.get("/", tags=["System"])
async def root():
    return {
        "system": "Cognitive Physics Engine",
        "version": "1.0.0",
        "status": "online",
        "manifesto": "Knowledge is not stored. It resonates.",
        "timestamp": time.time()
    }


@app.get("/status", tags=["System"])
async def get_status():
    """Full cognitive universe status."""
    if not engine:
        raise HTTPException(503, "Engine not initialized")
    return engine.status()


@app.post("/ingest", tags=["Knowledge"])
async def ingest_knowledge(request: IngestRequest):
    """
    Ingest new knowledge into the cognitive universe.
    Creates a particle and connects it via string network.
    """
    if not engine:
        raise HTTPException(503, "Engine not initialized")
    try:
        particle = engine.ingest(
            content=request.content,
            particle_type=request.particle_type,
            source=request.source,
            tags=request.tags,
            dimensions=request.dimensions,
            confidence=request.confidence
        )
        return {
            "status": "ingested",
            "particle": particle.to_dict(),
            "universe_size": len(engine.all_particles)
        }
    except Exception as e:
        raise HTTPException(500, str(e))


@app.post("/query", tags=["Query"])
async def query_universe(request: QueryRequest):
    """
    Query the cognitive universe.
    NOT a retrieval operation — a field perturbation.
    Response emerges through resonance.
    """
    if not engine:
        raise HTTPException(503, "Engine not initialized")
    try:
        result = await engine.query(
            query_text=request.query,
            intent=request.intent,
            simulate=request.simulate,
            top_k=request.top_k
        )
        return result.to_dict()
    except Exception as e:
        logger.error(f"Query error: {e}", exc_info=True)
        raise HTTPException(500, str(e))


@app.post("/tools/execute", tags=["Tools"])
async def execute_tool(request: ToolExecutionRequest):
    """
    Execute a registered tool (observation event).
    Collapses quantum superposition of related particles.
    """
    if not engine:
        raise HTTPException(503, "Engine not initialized")
    try:
        result = await engine.execute_tool(
            request.tool_name, request.args, request.particle_id
        )
        return result
    except Exception as e:
        raise HTTPException(500, str(e))


@app.get("/particles/{particle_id}", tags=["Knowledge"])
async def get_particle(particle_id: str):
    """Retrieve a specific cognitive particle."""
    if not engine:
        raise HTTPException(503, "Engine not initialized")
    particle = engine.all_particles.get(particle_id)
    if not particle:
        raise HTTPException(404, f"Particle {particle_id} not found")
    return particle.to_dict()


@app.get("/strings/stats", tags=["Strings"])
async def get_string_stats():
    """String network statistics."""
    if not engine:
        raise HTTPException(503, "Engine not initialized")
    return engine.string_network.get_stats()


@app.get("/curiosity", tags=["Curiosity"])
async def get_curiosity_status():
    """Current curiosity engine state."""
    if not engine:
        raise HTTPException(503, "Engine not initialized")
    return engine.curiosity_engine.curiosity_status()


@app.post("/curiosity/generate-impulse", tags=["Curiosity"])
async def generate_curiosity_impulse():
    """Generate a curiosity impulse from current state."""
    if not engine:
        raise HTTPException(503, "Engine not initialized")
    impulse = engine.curiosity_engine.generate_curiosity_impulse(
        list(engine.all_particles.values())
    )
    if impulse:
        return {
            "question": impulse.question,
            "urgency": impulse.urgency,
            "source": impulse.source,
            "triggered_at": impulse.triggered_at
        }
    return {"message": "No curiosity impulse generated — system is satisfied"}


@app.get("/ecosystem/health", tags=["Ecosystem"])
async def get_ecosystem_health():
    """Cognitive ecosystem health metrics."""
    if not engine:
        raise HTTPException(503, "Engine not initialized")
    return engine.ecosystem.ecosystem_health()


@app.post("/ecosystem/evolve", tags=["Ecosystem"])
async def trigger_evolution():
    """Manually trigger an evolutionary cycle."""
    if not engine:
        raise HTTPException(503, "Engine not initialized")
    result = engine.ecosystem.evolve_cycle()
    return {"status": "evolved", "result": result}


@app.get("/branes", tags=["Branes"])
async def list_branes():
    """List all cognitive branes and their health."""
    if not engine:
        raise HTTPException(503, "Engine not initialized")
    return engine.brane_network.health_report()


@app.get("/wormholes", tags=["Strings"])
async def list_wormholes():
    """List all detected cognitive wormholes."""
    if not engine:
        raise HTTPException(503, "Engine not initialized")
    wormholes = engine.string_network.wormholes
    return {
        "count": len(wormholes),
        "wormholes": [
            {"id": wh_id, "string_a": s_a, "string_b": s_b}
            for wh_id, (s_a, s_b) in list(wormholes.items())[:20]
        ]
    }


@app.post("/simulate", tags=["Simulation"])
async def simulate_trajectories(query: str, n: int = 5):
    """Run reality simulation for a query."""
    if not engine:
        raise HTTPException(503, "Engine not initialized")
    try:
        result = engine.reality_simulator.simulate(
            query, list(engine.all_particles.values())[:10], n_override=n
        )
        return result.to_dict()
    except Exception as e:
        raise HTTPException(500, str(e))


@app.delete("/strings/prune", tags=["Strings"])
async def prune_dormant_strings(max_age_hours: float = 1.0):
    """Prune dormant strings from the network."""
    if not engine:
        raise HTTPException(503, "Engine not initialized")
    pruned = engine.string_network.prune_dormant(max_age_hours * 3600)
    return {"pruned": pruned, "remaining": len(engine.string_network.strings)}