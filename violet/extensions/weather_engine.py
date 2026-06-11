"""
Weather Engine
==============
The cognitive climate system.

Cognitive weather models:
  - Uncertainty pressure (like barometric pressure)
  - Novelty pressure (like humidity — build-up before storm)
  - Contradiction storms (violent weather events)
  - Stability zones (high pressure — well-understood regions)
  - Cognitive fog (ambiguity fronts)
  - Knowledge fronts (advancing understanding)
  - Climate drift (long-term uncertainty bias)

Weather phenomena:
  Storm: rapid injection of contradictory evidence
  Fog:   high ambiguity, low resolution
  Clear: high certainty, consistent evidence
  Front: boundary between two knowledge domains
  Drought: no new information arriving
  Flood: information overload

This gives the CPE a temporal texture to cognition.
"""

from __future__ import annotations

import math
import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from violet.core.constants import (
    N_DIMENSIONS, COGNITIVE_PLANCK, LAMBDA_CURIOSITY,
    H_COGNITIVE, CognitiveDimension
)
from violet.particles.cognitive_particles import CognitiveParticle, DimensionalVector


class WeatherType(Enum):
    CLEAR = auto()         # High certainty, stable
    OVERCAST = auto()      # Moderate uncertainty
    FOG = auto()           # High ambiguity
    STORM = auto()         # Active contradiction cascade
    FRONT = auto()         # Domain boundary
    DROUGHT = auto()       # No new information
    FLOOD = auto()         # Information overload
    LIGHTNING = auto()     # Sudden insight event
    HURRICANE = auto()     # Catastrophic uncertainty collapse


@dataclass
class WeatherCell:
    """
    A local weather system in cognitive space.
    """
    cell_id: str
    center: DimensionalVector
    radius: float = 0.3
    weather_type: WeatherType = WeatherType.CLEAR
    
    # Atmospheric properties
    uncertainty_pressure: float = 0.5   # 0=certain, 1=maximally uncertain
    novelty_humidity: float = 0.3       # Novel information density
    contradiction_charge: float = 0.0  # Builds up before storms
    stability: float = 0.7             # Resistance to change
    
    # Dynamics
    movement_vector: np.ndarray = field(
        default_factory=lambda: np.zeros(N_DIMENSIONS)
    )
    age: float = 0.0
    intensity: float = 0.5

    def should_storm(self) -> bool:
        """Storm when contradiction charge exceeds stability."""
        return self.contradiction_charge > self.stability

    def visibility(self) -> float:
        """Cognitive visibility: how clear is understanding in this region?"""
        return 1.0 - self.uncertainty_pressure * 0.7 - (
            1.0 if self.weather_type == WeatherType.FOG else 0.0
        ) * 0.3


@dataclass
class WeatherFront:
    """
    A boundary between two cognitive weather systems.
    Knowledge fronts advance when one paradigm replaces another.
    """
    front_id: str
    leading_cell_id: str
    trailing_cell_id: str
    front_position: DimensionalVector
    advancement_speed: float = 0.02
    front_type: str = "knowledge"  # knowledge | paradigm | uncertainty


@dataclass
class CognitiveStorm:
    """A contradiction storm event."""
    storm_id: str
    epicenter: DimensionalVector
    intensity: float
    started_at: float = field(default_factory=time.time)
    ended_at: Optional[float] = None
    particles_affected: List[str] = field(default_factory=list)
    resolved: bool = False

    def duration(self) -> float:
        if self.ended_at:
            return self.ended_at - self.started_at
        return time.time() - self.started_at

    def is_active(self) -> bool:
        return not self.resolved and (time.time() - self.started_at) < 3600


class WeatherEngine:
    """
    Simulates cognitive weather across the knowledge universe.
    
    Provides temporal texture and climate to cognition:
      - Where is cognition currently stormy vs clear?
      - What regions are experiencing knowledge droughts?
      - Where are advancing fronts of new understanding?
      - What is the long-term cognitive climate trend?
    """

    def __init__(self):
        self.weather_cells: Dict[str, WeatherCell] = {}
        self.active_storms: List[CognitiveStorm] = []
        self.weather_fronts: List[WeatherFront] = []
        self.climate_history: List[Dict] = []
        
        # Global climate
        self.global_temperature: float = 0.5  # 0=frozen/certain, 1=hot/chaotic
        self.global_pressure: float = 0.5     # Uncertainty pressure
        self.climate_trend: float = 0.0       # Rate of temperature change
        
        self.lightning_events: int = 0         # Sudden insight events
        self.total_storms: int = 0

    def create_weather_cell(
        self,
        center: DimensionalVector,
        initial_type: WeatherType = WeatherType.CLEAR
    ) -> WeatherCell:
        """Create a new weather cell in cognitive space."""
        import uuid
        cell = WeatherCell(
            cell_id=str(uuid.uuid4())[:8],
            center=center,
            weather_type=initial_type,
            uncertainty_pressure=0.3 if initial_type == WeatherType.CLEAR else 0.7
        )
        self.weather_cells[cell.cell_id] = cell
        return cell

    def get_weather_at(self, position: DimensionalVector) -> Dict:
        """
        Get current cognitive weather at a position.
        Composite of nearby weather cells.
        """
        if not self.weather_cells:
            return {
                "type": WeatherType.CLEAR.name,
                "uncertainty": 0.3,
                "visibility": 0.9,
                "storm_nearby": False
            }
        
        # Find nearby cells
        nearby_cells = []
        for cell in self.weather_cells.values():
            sim = position.cosine_similarity(cell.center)
            if sim > 0.5:
                nearby_cells.append((cell, sim))
        
        if not nearby_cells:
            return {
                "type": WeatherType.CLEAR.name,
                "uncertainty": self.global_pressure,
                "visibility": 1.0 - self.global_pressure,
                "storm_nearby": False
            }
        
        # Weight by proximity
        total_weight = sum(w for _, w in nearby_cells)
        uncertainty = sum(c.uncertainty_pressure * w for c, w in nearby_cells) / total_weight
        visibility = sum(c.visibility() * w for c, w in nearby_cells) / total_weight
        
        # Dominant weather type
        dominant = max(nearby_cells, key=lambda x: x[1])[0]
        
        # Check active storms
        storm_nearby = any(
            1.0 - position.cosine_similarity(s.epicenter) < 0.3
            for s in self.active_storms if s.is_active()
        )
        
        return {
            "type": dominant.weather_type.name,
            "uncertainty": round(float(uncertainty), 3),
            "visibility": round(float(visibility), 3),
            "storm_nearby": storm_nearby,
            "novelty_humidity": round(float(dominant.novelty_humidity), 3),
        }

    def update_from_particles(
        self, particles: List[CognitiveParticle]
    ) -> None:
        """
        Update weather based on particle state.
        Contradiction → storm charge.
        High uncertainty → pressure increase.
        New particles → humidity increase.
        """
        if not particles:
            return
        
        # Global statistics
        avg_uncertainty = np.mean([p.uncertainty for p in particles])
        avg_contradiction = np.mean([p.contradiction_score for p in particles])
        
        self.global_pressure = 0.7 * self.global_pressure + 0.3 * avg_uncertainty
        self.global_temperature = 0.7 * self.global_temperature + 0.3 * (
            avg_uncertainty * 0.6 + avg_contradiction * 0.4
        )
        
        # Update individual cells
        for cell in self.weather_cells.values():
            nearby = [
                p for p in particles
                if cell.center.cosine_similarity(p.dimensions) > 0.6
            ]
            if nearby:
                cell.uncertainty_pressure = np.mean([p.uncertainty for p in nearby])
                cell.contradiction_charge += np.mean([p.contradiction_score for p in nearby]) * 0.1
                cell.novelty_humidity = np.mean([p.dimensions.novelty for p in nearby])
                
                # Update weather type
                self._classify_cell(cell)
            
            cell.age += 1

    def _classify_cell(self, cell: WeatherCell) -> None:
        """Classify weather type based on atmospheric properties."""
        if cell.should_storm():
            cell.weather_type = WeatherType.STORM
            if cell.intensity > 0.8:
                cell.weather_type = WeatherType.HURRICANE
        elif cell.uncertainty_pressure > 0.8:
            cell.weather_type = WeatherType.FOG
        elif cell.uncertainty_pressure > 0.6:
            cell.weather_type = WeatherType.OVERCAST
        elif cell.novelty_humidity < 0.1:
            cell.weather_type = WeatherType.DROUGHT
        elif cell.novelty_humidity > 0.9:
            cell.weather_type = WeatherType.FLOOD
        else:
            cell.weather_type = WeatherType.CLEAR

    def trigger_storm(self, epicenter: DimensionalVector,
                       intensity: float, affected_particles: List[str]) -> CognitiveStorm:
        """
        Trigger a contradiction storm.
        Storms temporarily increase uncertainty but can produce lightning insights.
        """
        import uuid
        storm = CognitiveStorm(
            storm_id=str(uuid.uuid4())[:8],
            epicenter=epicenter,
            intensity=intensity,
            particles_affected=affected_particles
        )
        self.active_storms.append(storm)
        self.total_storms += 1
        
        # Create storm cell
        storm_cell = WeatherCell(
            cell_id=f"storm_{storm.storm_id}",
            center=epicenter,
            weather_type=WeatherType.STORM,
            uncertainty_pressure=intensity,
            contradiction_charge=intensity * 1.5,
            stability=0.1
        )
        self.weather_cells[storm_cell.cell_id] = storm_cell
        return storm

    def lightning_insight(self, position: DimensionalVector) -> Dict:
        """
        A lightning strike in cognitive space.
        Sudden insight that resolves uncertainty in a region.
        Storms sometimes produce lightning.
        """
        self.lightning_events += 1
        
        # Find storm cells nearby
        nearby_storms = [
            c for c in self.weather_cells.values()
            if c.weather_type in [WeatherType.STORM, WeatherType.HURRICANE]
            and position.cosine_similarity(c.center) > 0.6
        ]
        
        if nearby_storms:
            # Lightning resolves the storm
            for storm_cell in nearby_storms[:2]:
                storm_cell.contradiction_charge *= 0.3
                storm_cell.uncertainty_pressure *= 0.5
                self._classify_cell(storm_cell)
        
        return {
            "event": "lightning_insight",
            "position": position.to_dict(),
            "storms_resolved": len(nearby_storms),
            "total_lightning": self.lightning_events
        }

    def resolve_storm(self, storm: CognitiveStorm) -> None:
        """Resolve a cognitive storm."""
        storm.resolved = True
        storm.ended_at = time.time()
        
        # Check for lightning insight potential
        if storm.intensity > 0.7 and storm.duration() > 60:
            self.lightning_insight(storm.epicenter)

    def update_fronts(self) -> None:
        """Advance weather fronts through cognitive space."""
        for front in self.weather_fronts:
            # Advance front position
            leading_cell = self.weather_cells.get(front.leading_cell_id)
            if leading_cell:
                front.front_position = DimensionalVector(
                    values=np.clip(
                        front.front_position.values +
                        leading_cell.movement_vector * front.advancement_speed,
                        0, 1
                    )
                )

    def climate_forecast(self) -> Dict:
        """Forecast cognitive climate conditions."""
        active_storm_count = sum(1 for s in self.active_storms if s.is_active())
        avg_cell_pressure = np.mean([
            c.uncertainty_pressure for c in self.weather_cells.values()
        ]) if self.weather_cells else self.global_pressure
        
        # Forecast
        if active_storm_count > 3:
            outlook = "turbulent — high uncertainty, rapid change expected"
        elif avg_cell_pressure > 0.7:
            outlook = "foggy — difficult to navigate, clarification needed"
        elif avg_cell_pressure < 0.3:
            outlook = "clear — good conditions for precise reasoning"
        else:
            outlook = "partly cloudy — mixed certainty regions"
        
        return {
            "global_temperature": round(self.global_temperature, 3),
            "global_pressure": round(self.global_pressure, 3),
            "active_storms": active_storm_count,
            "total_storms_historical": self.total_storms,
            "lightning_events": self.lightning_events,
            "weather_cells": len(self.weather_cells),
            "active_fronts": len(self.weather_fronts),
            "outlook": outlook,
        }