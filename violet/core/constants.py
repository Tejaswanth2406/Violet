"""
Cognitive Physics Engine - Universal Constants
===============================================
Mathematical constants governing the cognitive universe Ω.
"""

import math
from dataclasses import dataclass
from typing import Final

# ─────────────────────────────────────────────
# Fundamental Cognitive Constants
# ─────────────────────────────────────────────

# Planck-equivalent: minimum meaningful cognitive quantum
COGNITIVE_PLANCK: Final[float] = 1e-10

# Speed of meaning propagation (normalized)
C_MEANING: Final[float] = 1.0

# Gravitational constant for cognitive mass attraction
G_COGNITIVE: Final[float] = 6.674e-4

# Dark energy density (curiosity pressure baseline)
LAMBDA_CURIOSITY: Final[float] = 7.3e-3

# String tension (resistance to deformation)
ALPHA_PRIME: Final[float] = 0.5

# Resonance decay constant
GAMMA_DECAY: Final[float] = 0.02

# Minimum string energy threshold (below = dormant)
E_THRESHOLD: Final[float] = 1e-6

# Wormhole formation threshold (shared dimension cosine sim)
WORMHOLE_THRESHOLD: Final[float] = 0.85

# Cognitive Hubble constant (expansion rate of knowledge universe)
H_COGNITIVE: Final[float] = 0.07

# Dark matter influence radius
R_DARK_MATTER: Final[float] = 5.0

# Maximum brane interaction depth
MAX_BRANE_DEPTH: Final[int] = 7

# Fusion energy threshold
E_FUSION: Final[float] = 0.75

# Fission energy threshold
E_FISSION: Final[float] = 2.5

# Superposition collapse threshold
COLLAPSE_CERTAINTY: Final[float] = 0.92

# Evolutionary mutation rate
MU_MUTATION: Final[float] = 0.03

# Ecosystem carrying capacity per brane
K_CARRYING: Final[int] = 10_000

# Memory half-life (seconds) for age decay
TAU_MEMORY: Final[float] = 86_400.0  # 1 day

# Number of cognitive dimensions
N_DIMENSIONS: Final[int] = 8

# Dimension indices
class CognitiveDimension:
    TRUTH: Final[int] = 0
    TIME: Final[int] = 1
    NOVELTY: Final[int] = 2
    UTILITY: Final[int] = 3
    RISK: Final[int] = 4
    CONFIDENCE: Final[int] = 5
    INFLUENCE: Final[int] = 6
    INTENT: Final[int] = 7

    NAMES: Final[list] = [
        "truth", "time", "novelty", "utility",
        "risk", "confidence", "influence", "intent"
    ]


@dataclass(frozen=True)
class PhysicsLaws:
    """Encapsulates governing equations of the CPE."""

    # Resonance amplitude: A = A0 * cos(ω*t) * e^(-γt)
    resonance_decay: str = "A(t) = A0 * cos(omega*t) * exp(-gamma*t)"

    # Cognitive gravity: F = G * m1 * m2 / r^2
    gravity: str = "F = G_COGNITIVE * m1 * m2 / r^2"

    # String energy: E = (1/2) * alpha_prime * integral(|dX/dsigma|^2 + |dX/dtau|^2)
    string_energy: str = "E = (alpha_prime/2) * sum(mode_amplitudes^2)"

    # Dark energy expansion: dU/dt = H_COGNITIVE * U + LAMBDA_CURIOSITY * novelty_gradient
    knowledge_expansion: str = "dU/dt = H * U + Lambda * nabla(novelty)"

    # Wormhole formation: W = sigmoid((cos_sim - threshold) / temperature)
    wormhole_probability: str = "P(wormhole) = sigma((sim - W_thresh) / T)"

    # Evolution fitness: F = utility * confidence * (1 - risk) * novelty^0.3
    fitness: str = "fitness = utility * confidence * (1-risk) * novelty^0.3"

    # Memory energy decay: E(t) = E0 * exp(-t / tau)
    memory_decay: str = "E(t) = E0 * exp(-t / tau)"


PHYSICS = PhysicsLaws()