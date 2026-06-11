<img width="1254" height="1254" alt="image" src="https://github.com/user-attachments/assets/f721ae17-3b5d-4b95-a6b2-4fc4eef9ccf6" />

# 🟣 Violet — Cognitive Physics Engine

> *Knowledge is not stored. It resonates.*

Violet is a **Cognitive Physics Engine (CPE)** — a radical rethinking of how AI systems should represent and process knowledge. Instead of static retrieval (RAG, vector stores, graph databases), Violet models cognition as **physics**: particles, fields, strings, branes, and dark energy.

---

## ✨ Core Concept

| Traditional AI | Violet |
|---|---|
| Store → Retrieve | Resonate → Emerge |
| Vector similarity | String vibration modes |
| Knowledge graph | Cognitive string network |
| Static embeddings | Evolving dimensional particles |
| Retrieval | Perturbation + resonance |

The cognitive universe Ω is composed of:

```
Ω = Universal Cognitive Field
  ├── Cognitive String Network   (fundamental relationships)
  ├── Cognitive Particles        (Memoryon, Evidon, Hypotheon, Reasonon, Emergon, Darkon)
  ├── Cognitive Fields           (Memory, Intent, Evidence, Reasoning, Tool, Curiosity)
  ├── Cognitive Branes           (Research, Memory, Simulation, Execution, Social)
  ├── Ecosystem Layer            (Evolution, Selection, Emergence)
  ├── Curiosity Engine           (Dark Energy, Contradictions, Gaps)
  └── Reality Simulator          (Multi-trajectory planning)
```

---

## 📁 Project Structure

```
Violet/
├── run.py                      # ← Start the API here
├── requirements.txt
├── .gitignore
│
├── api/                        # FastAPI REST interface
│   └── main.py
│
├── violet/                     # Core CPE library
│   ├── core/
│   │   ├── constants.py        # Physics constants (Planck, G, Lambda...)
│   │   └── engine.py           # CognitivePhysicsEngine orchestrator
│   │
│   ├── particles/
│   │   └── cognitive_particles.py   # Memoryon, Evidon, Hypotheon, Reasonon, Emergon, Darkon
│   │
│   ├── strings/
│   │   └── context_strings.py       # ContextString, StringNetwork, wormholes
│   │
│   ├── fields/
│   │   └── cognitive_fields.py      # UniversalCognitiveField + 6 sub-fields
│   │
│   ├── branes/
│   │   └── cognitive_branes.py      # BraneNetwork + 5 cognitive branes
│   │
│   ├── ecosystem/
│   │   └── cognitive_ecosystem.py   # Evolution, selection, biodiversity
│   │
│   ├── curiosity/
│   │   └── curiosity_engine.py      # Dark energy, contradictions, gap detection
│   │
│   ├── simulation/
│   │   └── reality_simulator.py     # Multi-trajectory Monte Carlo planning
│   │
│   └── extensions/                  # Advanced cognitive modules
│       ├── morphogenesis_engine.py  # Biological growth rules for concepts
│       ├── cognitive_genome.py      # DNA-style knowledge generation
│       ├── dream_engine.py          # Background sleep/consolidation cycles
│       ├── immune_system.py         # Threat detection & neutralization
│       ├── information_geometry.py  # Riemannian cognitive manifold
│       ├── physics_engine.py        # Resonance, gravity, wormhole engines
│       ├── self_model.py            # Meta-cognition & self-awareness
│       └── weather_engine.py        # Cognitive climate simulation
│
└── tests/                      # Test suite
```

---

## 🚀 Getting Started

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the API

```bash
python run.py
```

Or with options:

```bash
python run.py --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://127.0.0.1:8000`  
Interactive docs: `http://127.0.0.1:8000/docs`

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | System info |
| `GET` | `/status` | Full cognitive universe status |
| `POST` | `/ingest` | Ingest knowledge particle |
| `POST` | `/query` | Query via field resonance |
| `POST` | `/tools/execute` | Execute a registered tool |
| `GET` | `/particles/{id}` | Get specific particle |
| `GET` | `/strings/stats` | String network statistics |
| `GET` | `/curiosity` | Curiosity engine state |
| `POST` | `/curiosity/generate-impulse` | Generate curiosity impulse |
| `GET` | `/ecosystem/health` | Ecosystem health metrics |
| `POST` | `/ecosystem/evolve` | Trigger evolution cycle |
| `GET` | `/branes` | List all cognitive branes |
| `GET` | `/wormholes` | List detected wormholes |
| `POST` | `/simulate` | Run reality simulation |
| `DELETE` | `/strings/prune` | Prune dormant strings |

### Quick example

```bash
# Ingest knowledge
curl -X POST http://localhost:8000/ingest \
  -H "Content-Type: application/json" \
  -d '{"content": "Emergence arises from interaction", "particle_type": "memoryon"}'

# Query the cognitive universe
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "How does intelligence emerge?", "simulate": true}'
```

---

## 🧬 Cognitive Particle Types

| Particle | Description |
|----------|-------------|
| `Memoryon` | Persistent memory — long-lived, gains mass through activation |
| `Evidon` | External evidence — high truth dimension, variable confidence |
| `Hypotheon` | Speculative knowledge — exists in superposition |
| `Reasonon` | Causal chain — links antecedents to consequents |
| `Emergon` | Self-assembled — born from string resonance |
| `Darkon` | Inferred influence — detected through unexplained clustering |

---

## ⚙️ Physics Constants

| Constant | Symbol | Value | Meaning |
|----------|--------|-------|---------|
| Cognitive Planck | `ħ_c` | 1e-10 | Minimum meaningful quantum |
| Meaning Speed | `c_m` | 1.0 | Speed of meaning propagation |
| Cognitive Gravity | `G_c` | 6.674e-4 | Knowledge attraction constant |
| Dark Energy | `Λ_c` | 7.3e-3 | Curiosity pressure baseline |
| String Tension | `α'` | 0.5 | Resistance to deformation |
| Resonance Decay | `γ` | 0.02 | Energy decay rate |
| Hubble Cognitive | `H_c` | 0.07 | Knowledge universe expansion rate |

---

## 🧠 Extension Modules

The `violet/extensions/` directory contains advanced cognitive systems:

- **Morphogenesis Engine**: Concepts grow from DNA-like rules, not stored directly
- **Cognitive Genome**: Knowledge embryogenesis — generate concepts on demand
- **Dream Engine**: Autonomous background consolidation (REM/NREM sleep analog)
- **Immune System**: Detect and neutralize misinformation, hallucinations, adversarial inputs
- **Information Geometry**: Riemannian manifold — geodesic paths, curvature, Ricci flow
- **Physics Engine**: Resonance cascades, gravitational assists, wormhole navigation
- **Self-Model**: Meta-cognition — the system knows what it knows and doesn't know
- **Weather Engine**: Cognitive climate — uncertainty storms, knowledge fronts

---

## 📄 License

MIT License — feel free to explore, fork, and build upon.

---

*Built with ∞ curiosity. The cognitive universe is alive.*
