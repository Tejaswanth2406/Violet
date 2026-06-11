"""
Information Geometry Engine
============================
Beyond String Theory — into Information Geometry.

Replace: graph (nodes + edges)
With:    manifold (curved cognitive space)

A manifold is a curved surface.
Knowledge lives on this surface.
Distance = geodesic distance (not Euclidean).
Curvature indicates conceptual complexity.
Singularities indicate foundational concepts.

Mathematical foundation:
  Fisher information metric: g_ij = E[∂log p / ∂θ_i · ∂log p / ∂θ_j]
  The metric determines how concepts relate.

Cognitive implications:
  - Similar concepts cluster in low-curvature regions
  - Paradigm shifts = topology changes in the manifold
  - Wormholes = geodesic shortcuts
  - Dark matter = missing curvature source
  - Singularities = high-gravity concept anchors
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from core.constants import (
    N_DIMENSIONS, COGNITIVE_PLANCK, G_COGNITIVE, CognitiveDimension
)
from particles.cognitive_particles import CognitiveParticle, DimensionalVector


class ManifoldTopology(Enum):
    FLAT = auto()           # Euclidean-like region
    POSITIVELY_CURVED = auto()  # Spherical — concepts converge
    NEGATIVELY_CURVED = auto()  # Hyperbolic — concepts diverge
    SADDLE = auto()         # Mixed curvature
    SINGULAR = auto()       # High-density anchor point


@dataclass
class CognitivePatch:
    """
    A local patch of the cognitive manifold.
    The manifold is covered by overlapping patches,
    each with its own local metric tensor.
    """
    patch_id: str
    center: DimensionalVector
    local_metric: np.ndarray    # N×N metric tensor g_ij
    curvature: float = 0.0
    topology: ManifoldTopology = ManifoldTopology.FLAT
    
    def geodesic_distance(self, a: DimensionalVector,
                           b: DimensionalVector) -> float:
        """
        Geodesic distance using local metric.
        ds² = g_ij dx^i dx^j
        """
        diff = a.values - b.values
        # ds² = diff^T @ g @ diff
        ds2 = float(diff @ self.local_metric @ diff)
        return math.sqrt(max(ds2, COGNITIVE_PLANCK))

    def parallel_transport(self, vector: np.ndarray,
                            path: List[DimensionalVector]) -> np.ndarray:
        """
        Parallel transport a vector along a path.
        In curved space, vectors rotate as you move.
        This captures how meaning shifts across conceptual space.
        """
        transported = vector.copy()
        for i in range(len(path) - 1):
            diff = path[i+1].values - path[i].values
            # Simplified Christoffel correction
            correction = np.dot(diff, transported) * diff * self.curvature
            transported = transported + correction
            norm = np.linalg.norm(transported)
            if norm > COGNITIVE_PLANCK:
                transported /= norm
        return transported


class InformationGeometryEngine:
    """
    Treats the cognitive universe as a Riemannian manifold.
    
    Operations:
    - Compute geodesic paths (not shortest Euclidean)
    - Detect curvature singularities (anchor concepts)
    - Map topology changes (paradigm shifts)
    - Fisher information for uncertainty quantification
    - Ricci flow for concept space smoothing
    """

    def __init__(self, n_dims: int = N_DIMENSIONS):
        self.n_dims = n_dims
        self.patches: Dict[str, CognitivePatch] = {}
        self.global_metric: np.ndarray = np.eye(n_dims)
        self.curvature_map: Dict[str, float] = {}
        self.singularities: List[DimensionalVector] = []
        self.topology_changes: int = 0

    def compute_metric_tensor(
        self, particles: List[CognitiveParticle]
    ) -> np.ndarray:
        """
        Compute the Fisher information metric tensor.
        g_ij = Cov[X_i, X_j] of particle distribution.
        """
        if len(particles) < 2:
            return np.eye(self.n_dims)
        
        data = np.array([p.dimensions.values for p in particles])
        # Fisher metric ≈ inverse covariance of sufficient statistics
        cov = np.cov(data.T)
        
        # Regularize
        cov += COGNITIVE_PLANCK * np.eye(self.n_dims)
        
        self.global_metric = cov
        return cov

    def geodesic_path(
        self,
        start: DimensionalVector,
        end: DimensionalVector,
        n_steps: int = 10
    ) -> List[DimensionalVector]:
        """
        Compute geodesic path between two points in cognitive manifold.
        Uses gradient descent on path energy.
        
        In flat space: straight line.
        In curved space: curves around high-density regions.
        """
        # Initialize with linear interpolation
        path = [
            DimensionalVector(values=start.values * (1 - t/n_steps) + end.values * (t/n_steps))
            for t in range(n_steps + 1)
        ]
        
        # Refine path using metric
        for iteration in range(5):
            for i in range(1, len(path) - 1):
                prev, curr, next_p = path[i-1], path[i], path[i+1]
                
                # Geodesic equation: move toward midpoint
                midpoint = (prev.values + next_p.values) / 2
                
                # Apply metric correction
                diff = midpoint - curr.values
                correction = self.global_metric @ diff * 0.1
                
                new_vals = np.clip(curr.values + correction, 0, 1)
                path[i] = DimensionalVector(values=new_vals)
        
        return path

    def compute_curvature(
        self, position: DimensionalVector,
        particles: List[CognitiveParticle],
        radius: float = 0.2
    ) -> float:
        """
        Compute Ricci scalar curvature at a position.
        High curvature = many concepts converging here.
        Negative curvature = concepts spreading/diverging.
        """
        # Count particles within radius
        nearby = [
            p for p in particles
            if 1.0 - position.cosine_similarity(p.dimensions) < radius
        ]
        
        if len(nearby) < 2:
            return 0.0
        
        n = len(nearby)
        
        # Local density (positive curvature)
        density = n / (math.pi * radius ** 2)
        
        # Check if particles converge (positive) or diverge (negative)
        centroid = np.mean([p.dimensions.values for p in nearby], axis=0)
        variance = np.mean([
            np.linalg.norm(p.dimensions.values - centroid) ** 2
            for p in nearby
        ])
        
        # High density + low variance = positive curvature (sphere-like)
        # Low density + high variance = negative curvature (saddle-like)
        curvature = density / max(variance, COGNITIVE_PLANCK) - 1.0
        return curvature

    def ricci_flow(
        self,
        particles: List[CognitiveParticle],
        dt: float = 0.01,
        n_steps: int = 10
    ) -> List[CognitiveParticle]:
        """
        Apply Ricci flow to smooth the cognitive manifold.
        dg/dt = -2 * Ric(g)
        
        Positive curvature shrinks (consolidates).
        Negative curvature expands (explores).
        
        Makes the knowledge landscape more uniform.
        """
        for _ in range(n_steps):
            for particle in particles:
                curvature = self.compute_curvature(particle.dimensions, particles)
                
                # Move against curvature gradient
                flow_direction = -2 * curvature * (
                    particle.dimensions.values -
                    np.mean([p.dimensions.values for p in particles], axis=0)
                )
                
                new_vals = np.clip(
                    particle.dimensions.values + dt * flow_direction, 0, 1
                )
                particle.dimensions = DimensionalVector(values=new_vals)
        
        return particles

    def detect_singularities(
        self, particles: List[CognitiveParticle]
    ) -> List[DimensionalVector]:
        """
        Detect high-gravity singularities — foundational anchor concepts.
        These are the 'black holes' of the cognitive universe.
        High cognitive mass + high activation + high curvature.
        """
        self.singularities = []
        
        for particle in particles:
            curvature = self.compute_curvature(particle.dimensions, particles)
            gravity = particle.cognitive_mass * curvature
            
            if gravity > 5.0:  # Singularity threshold
                self.singularities.append(particle.dimensions)
                particle.metadata["is_singularity"] = True
                particle.metadata["gravitational_strength"] = gravity
        
        return self.singularities

    def fisher_information(self, particle: CognitiveParticle,
                            nearby: List[CognitiveParticle]) -> np.ndarray:
        """
        Compute local Fisher information matrix.
        High Fisher information = high discrimination power.
        Determines how precisely we can locate this concept.
        """
        if not nearby:
            return np.eye(self.n_dims)
        
        # Expected value of score function squared
        scores = []
        for n in nearby:
            score = n.dimensions.values - particle.dimensions.values
            scores.append(np.outer(score, score))
        
        return np.mean(scores, axis=0)

    def paradigm_shift_detector(
        self,
        before_particles: List[CognitiveParticle],
        after_particles: List[CognitiveParticle]
    ) -> Dict:
        """
        Detect if the topology of cognitive space has fundamentally changed.
        A paradigm shift = topological change in the manifold.
        """
        if not before_particles or not after_particles:
            return {"shift_detected": False}
        
        before_metric = self.compute_metric_tensor(before_particles)
        after_metric = self.compute_metric_tensor(after_particles)
        
        # Metric change = topology change
        metric_diff = np.linalg.norm(after_metric - before_metric)
        
        before_center = np.mean([p.dimensions.values for p in before_particles], axis=0)
        after_center = np.mean([p.dimensions.values for p in after_particles], axis=0)
        center_shift = np.linalg.norm(after_center - before_center)
        
        shift_magnitude = metric_diff + center_shift * 2
        
        if shift_magnitude > 1.0:
            self.topology_changes += 1
            return {
                "shift_detected": True,
                "magnitude": round(float(shift_magnitude), 3),
                "type": "metric_deformation",
                "topology_changes_total": self.topology_changes
            }
        
        return {"shift_detected": False, "magnitude": round(float(shift_magnitude), 3)}

    def manifold_report(self) -> Dict:
        return {
            "metric_determinant": round(float(np.linalg.det(self.global_metric)), 4),
            "patches": len(self.patches),
            "singularities": len(self.singularities),
            "topology_changes": self.topology_changes,
            "space_dimensionality": self.n_dims,
        }