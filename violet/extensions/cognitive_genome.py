"""
Cognitive Genome
================
The breakthrough assumption we're breaking:

  OLD:  Store Knowledge → Retrieve it
  NEW:  Store DNA → Generate knowledge when needed

Nature doesn't store 'Tiger'.
Nature stores DNA and generates the tiger.

The CognitiveGenome stores:
  - traits (dimensional tendencies)
  - growth_rules (how concepts develop)
  - mutations (how they change)
  - ancestry (lineage)
  - expression_triggers (when to generate)

A concept like 'Agent Architecture' is not stored.
Instead: [Planning, Memory, Execution, Feedback] growth rules
are stored, and the concept is GROWN when needed.

This is Concept Embryogenesis.
"""

from __future__ import annotations

import time
import uuid
import math
import random
import copy
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Tuple

import numpy as np

from core.constants import (
    MU_MUTATION, N_DIMENSIONS, COGNITIVE_PLANCK,
    CognitiveDimension, ALPHA_PRIME
)
from particles.cognitive_particles import DimensionalVector


class GeneType(Enum):
    STRUCTURAL = auto()    # Defines shape of concept
    REGULATORY = auto()    # Controls when/how other genes express
    MARKER = auto()        # Identity tag
    GROWTH = auto()        # How concept expands
    INHIBITOR = auto()     # What this concept suppresses
    ENHANCER = auto()      # What this concept amplifies


class ExpressionState(Enum):
    DORMANT = auto()
    EXPRESSING = auto()
    SUPPRESSED = auto()
    HYPERACTIVE = auto()


@dataclass
class CognitiveGene:
    """
    A single gene in the cognitive genome.
    Not a fact — a growth instruction.
    """
    gene_id: str = field(default_factory=lambda: str(uuid.uuid4())[:12])
    gene_type: GeneType = GeneType.STRUCTURAL
    name: str = ""
    
    # What this gene encodes (not the concept, the rule)
    dimensional_bias: np.ndarray = field(
        default_factory=lambda: np.random.rand(N_DIMENSIONS) * 0.5
    )
    growth_rate: float = 0.1          # How fast expressed concepts grow
    expression_threshold: float = 0.3  # Minimum stimulus to activate
    decay_resistance: float = 0.7     # How resistant to forgetting
    
    # Regulatory connections
    activates: List[str] = field(default_factory=list)   # gene_ids it turns on
    suppresses: List[str] = field(default_factory=list)  # gene_ids it turns off
    
    # State
    expression_level: float = 0.0
    expression_state: ExpressionState = ExpressionState.DORMANT
    activation_count: int = 0
    
    # Lineage
    parent_gene_id: Optional[str] = None
    generation: int = 0
    mutations_survived: int = 0

    def express(self, stimulus: float) -> float:
        """
        Gene expression: stimulus triggers growth rule.
        Returns expression level (0-1).
        """
        if stimulus < self.expression_threshold:
            self.expression_state = ExpressionState.DORMANT
            return 0.0
        
        # Sigmoid expression response
        x = (stimulus - self.expression_threshold) * 10
        self.expression_level = 1.0 / (1.0 + math.exp(-x))
        self.expression_state = ExpressionState.EXPRESSING
        self.activation_count += 1
        return self.expression_level

    def mutate(self, rate: float = MU_MUTATION) -> CognitiveGene:
        """Create a mutated copy of this gene."""
        mutant = copy.deepcopy(self)
        mutant.gene_id = str(uuid.uuid4())[:12]
        mutant.parent_gene_id = self.gene_id
        mutant.generation = self.generation + 1
        
        for i in range(N_DIMENSIONS):
            if random.random() < rate:
                mutant.dimensional_bias[i] = np.clip(
                    mutant.dimensional_bias[i] + np.random.normal(0, 0.1), 0, 1
                )
        
        if random.random() < rate:
            mutant.growth_rate = np.clip(
                mutant.growth_rate + np.random.normal(0, 0.02), 0.01, 1.0
            )
        if random.random() < rate:
            mutant.expression_threshold = np.clip(
                mutant.expression_threshold + np.random.normal(0, 0.05), 0.01, 0.99
            )
        
        mutant.mutations_survived = 0
        return mutant

    def to_dict(self) -> Dict:
        return {
            "gene_id": self.gene_id,
            "type": self.gene_type.name,
            "name": self.name,
            "expression_level": round(self.expression_level, 3),
            "state": self.expression_state.name,
            "activation_count": self.activation_count,
            "growth_rate": round(self.growth_rate, 3),
            "generation": self.generation,
        }


@dataclass
class GrowthRule:
    """
    A developmental rule.
    Instead of storing 'Agent', store:
      [Planning + Memory + Execution + Feedback] → Agent emerges
    
    This is the fundamental shift from retrieval to generation.
    """
    rule_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    
    # Component genes that, when co-expressed, produce the concept
    required_genes: List[str] = field(default_factory=list)
    sufficient_genes: List[str] = field(default_factory=list)
    
    # Growth trajectory
    growth_stages: List[Dict] = field(default_factory=list)
    current_stage: int = 0
    
    # Output specification
    output_dimensions: np.ndarray = field(
        default_factory=lambda: np.zeros(N_DIMENSIONS)
    )
    output_label: str = ""
    
    # Conditions
    environmental_requirements: Dict[str, float] = field(default_factory=dict)
    min_energy: float = 0.3

    def can_express(self, active_genes: Dict[str, float],
                     environment: Dict[str, float]) -> bool:
        """Check if this rule can fire given current gene expression."""
        # Check required genes
        for gene_id in self.required_genes:
            if active_genes.get(gene_id, 0.0) < 0.5:
                return False
        # Check environment
        for key, required_val in self.environmental_requirements.items():
            if environment.get(key, 0.0) < required_val:
                return False
        # Check sufficient genes (at least one)
        if self.sufficient_genes:
            return any(active_genes.get(g, 0.0) > 0.3
                       for g in self.sufficient_genes)
        return True

    def grow_concept(self, gene_expressions: Dict[str, float],
                      dt: float = 1.0) -> DimensionalVector:
        """
        Grow the concept from gene expressions.
        Each stage adds developmental detail.
        """
        base = self.output_dimensions.copy()
        
        # Weight by active gene expressions
        for gene_id, level in gene_expressions.items():
            if gene_id in self.required_genes or gene_id in self.sufficient_genes:
                base = np.clip(base + level * 0.1 * np.random.rand(N_DIMENSIONS), 0, 1)
        
        # Progress through stages
        if self.current_stage < len(self.growth_stages):
            stage = self.growth_stages[self.current_stage]
            stage_influence = np.array(
                stage.get("dimensional_shift", [0.0] * N_DIMENSIONS)
            )
            base = np.clip(base + stage_influence * dt, 0, 1)
            self.current_stage = min(
                self.current_stage + 1, len(self.growth_stages) - 1
            )
        
        return DimensionalVector(values=base)


class CognitiveGenome:
    """
    The DNA of the cognitive system.
    
    Stores growth rules, not concepts.
    Generates concepts when needed, like an organism.
    
    This breaks the fundamental retrieval assumption:
      Store: growth rules + gene regulatory networks
      Generate: concepts on demand from those rules
    """

    def __init__(self):
        self.genome_id: str = str(uuid.uuid4())
        self.genes: Dict[str, CognitiveGene] = {}
        self.growth_rules: Dict[str, GrowthRule] = {}
        self.regulatory_network: Dict[str, List[Tuple[str, float]]] = {}
        
        # Expression state
        self.active_expressions: Dict[str, float] = {}  # gene_id → level
        self.environmental_state: Dict[str, float] = {}
        
        # Evolution tracking
        self.generation: int = 0
        self.fitness_history: List[float] = []
        
        # Bootstrap with fundamental cognitive genes
        self._bootstrap_genes()
    
    def _bootstrap_genes(self) -> None:
        """Seed the genome with fundamental cognitive genes."""
        fundamental_genes = [
            ("planning", GeneType.STRUCTURAL,
             [0.5, 0.6, 0.4, 0.8, 0.3, 0.7, 0.6, 0.9]),
            ("memory", GeneType.STRUCTURAL,
             [0.8, 0.3, 0.3, 0.7, 0.2, 0.9, 0.5, 0.4]),
            ("execution", GeneType.STRUCTURAL,
             [0.7, 0.5, 0.5, 0.9, 0.3, 0.7, 0.6, 0.6]),
            ("feedback", GeneType.REGULATORY,
             [0.6, 0.4, 0.5, 0.8, 0.4, 0.6, 0.7, 0.5]),
            ("curiosity", GeneType.GROWTH,
             [0.4, 0.9, 0.9, 0.6, 0.4, 0.4, 0.5, 0.7]),
            ("synthesis", GeneType.STRUCTURAL,
             [0.7, 0.5, 0.7, 0.8, 0.3, 0.6, 0.8, 0.6]),
            ("abstraction", GeneType.REGULATORY,
             [0.5, 0.5, 0.8, 0.7, 0.2, 0.6, 0.9, 0.5]),
            ("grounding", GeneType.INHIBITOR,
             [0.9, 0.4, 0.2, 0.8, 0.3, 0.8, 0.5, 0.4]),
        ]
        
        for name, gtype, bias in fundamental_genes:
            gene = CognitiveGene(
                gene_type=gtype,
                name=name,
                dimensional_bias=np.array(bias)
            )
            self.genes[gene.gene_id] = gene
        
        # Seed growth rules for common concepts
        self._seed_growth_rules()
    
    def _seed_growth_rules(self) -> None:
        """Seed growth rules for fundamental concept categories."""
        gene_ids = list(self.genes.keys())
        
        if len(gene_ids) >= 4:
            # Rule: [planning + memory + execution + feedback] → agent
            agent_rule = GrowthRule(
                name="agent_architecture",
                required_genes=gene_ids[:2],
                sufficient_genes=gene_ids[2:4],
                output_dimensions=np.array(
                    [0.7, 0.5, 0.6, 0.9, 0.3, 0.7, 0.8, 0.8]
                ),
                output_label="agent",
                growth_stages=[
                    {"stage": "seed", "dimensional_shift": [0.0] * N_DIMENSIONS},
                    {"stage": "differentiation", "dimensional_shift": [0.1, 0, 0, 0.1, 0, 0, 0, 0]},
                    {"stage": "maturation", "dimensional_shift": [0.05, 0, 0.05, 0, 0, 0.05, 0, 0]},
                ]
            )
            self.growth_rules[agent_rule.rule_id] = agent_rule
            
            # Rule: [curiosity + abstraction + synthesis] → theory
            theory_rule = GrowthRule(
                name="theory_formation",
                required_genes=gene_ids[4:6] if len(gene_ids) > 5 else gene_ids[:2],
                sufficient_genes=gene_ids[6:7] if len(gene_ids) > 6 else [],
                output_dimensions=np.array(
                    [0.6, 0.5, 0.8, 0.7, 0.3, 0.5, 0.9, 0.5]
                ),
                output_label="theory",
                growth_stages=[
                    {"stage": "hypothesis", "dimensional_shift": [0, 0, 0.2, 0, 0, 0, 0, 0]},
                    {"stage": "testing", "dimensional_shift": [0.1, 0, 0, 0.1, 0, 0.1, 0, 0]},
                    {"stage": "consolidation", "dimensional_shift": [0.1, 0, -0.1, 0.1, -0.05, 0.1, 0, 0]},
                ]
            )
            self.growth_rules[theory_rule.rule_id] = theory_rule

    def stimulate(self, stimulus_vector: DimensionalVector,
                   strength: float = 1.0) -> Dict[str, float]:
        """
        Apply stimulus to the genome.
        Different genes respond to different dimensional stimuli.
        Returns map of gene_id → expression_level.
        """
        expressions = {}
        for gene_id, gene in self.genes.items():
            # Stimulus relevance = dot product with gene's dimensional bias
            relevance = float(np.dot(
                stimulus_vector.values,
                gene.dimensional_bias / max(np.linalg.norm(gene.dimensional_bias), COGNITIVE_PLANCK)
            ))
            expr = gene.express(relevance * strength)
            if expr > 0:
                expressions[gene_id] = expr
        
        self.active_expressions = expressions
        return expressions

    def generate_concept(self, stimulus: DimensionalVector,
                          context: Optional[str] = None) -> Optional[Dict]:
        """
        Generate a concept from stimulus via gene expression.
        This is embryogenesis — concept grows from genetic instructions.
        
        NOT retrieval. GENERATION.
        """
        # Step 1: Stimulate genome
        expressions = self.stimulate(stimulus)
        
        if not expressions:
            return None
        
        # Step 2: Find active growth rules
        active_rules = []
        for rule in self.growth_rules.values():
            if rule.can_express(expressions, self.environmental_state):
                active_rules.append(rule)
        
        if not active_rules:
            # No rule matched — generate novel concept via gene fusion
            return self._generate_novel_concept(expressions, context)
        
        # Step 3: Grow concept through most active rule
        best_rule = max(active_rules, key=lambda r: sum(
            expressions.get(g, 0) for g in r.required_genes
        ))
        
        grown_vector = best_rule.grow_concept(expressions)
        
        return {
            "label": best_rule.output_label,
            "rule": best_rule.name,
            "dimensions": grown_vector.to_dict(),
            "expression_profile": {
                self.genes[gid].name: round(lvl, 3)
                for gid, lvl in expressions.items()
                if gid in self.genes
            },
            "generation_method": "embryogenesis",
            "is_retrieved": False,     # ← The key property
            "is_generated": True,      # ← The key property
        }

    def _generate_novel_concept(self, expressions: Dict[str, float],
                                  context: Optional[str]) -> Dict:
        """
        Generate a completely novel concept when no rule matches.
        Analogous to evolutionary innovation.
        """
        if not expressions:
            return {"label": "void", "dimensions": {}, "generation_method": "null"}
        
        # Weighted blend of expressing genes
        blend = np.zeros(N_DIMENSIONS)
        total_weight = 0.0
        label_parts = []
        
        for gene_id, level in sorted(expressions.items(), key=lambda x: x[1], reverse=True)[:3]:
            gene = self.genes.get(gene_id)
            if gene:
                blend += level * gene.dimensional_bias
                total_weight += level
                label_parts.append(gene.name)
        
        if total_weight > 0:
            blend /= total_weight
        
        novel_label = "_".join(label_parts[:2]) if label_parts else "emergent"
        
        return {
            "label": novel_label,
            "rule": "novel_emergence",
            "dimensions": DimensionalVector(values=np.clip(blend, 0, 1)).to_dict(),
            "expression_profile": {
                self.genes[gid].name: round(lvl, 3)
                for gid, lvl in list(expressions.items())[:5]
                if gid in self.genes
            },
            "generation_method": "novel_emergence",
            "is_retrieved": False,
            "is_generated": True,
        }

    def evolve(self, fitness_signal: float) -> None:
        """
        Evolve the genome based on fitness feedback.
        High fitness → stabilize. Low fitness → mutate.
        """
        self.generation += 1
        self.fitness_history.append(fitness_signal)
        
        avg_fitness = sum(self.fitness_history[-10:]) / max(len(self.fitness_history[-10:]), 1)
        
        # Mutation rate inversely proportional to fitness
        mutation_rate = MU_MUTATION * (1.0 + (1.0 - avg_fitness))
        
        new_genes = {}
        for gene_id, gene in self.genes.items():
            if random.random() < mutation_rate:
                mutant = gene.mutate(rate=mutation_rate)
                new_genes[mutant.gene_id] = mutant
                gene.mutations_survived += 1
        
        self.genes.update(new_genes)
        
        # Prune poorly expressing genes
        if len(self.genes) > 200:
            to_prune = sorted(
                self.genes.items(),
                key=lambda x: x[1].activation_count
            )[:10]
            for gid, _ in to_prune:
                del self.genes[gid]

    def add_gene(self, name: str, gene_type: GeneType,
                  dimensional_bias: Optional[List[float]] = None) -> CognitiveGene:
        """Add a new gene to the genome."""
        bias = np.array(dimensional_bias) if dimensional_bias else np.random.rand(N_DIMENSIONS)
        gene = CognitiveGene(gene_type=gene_type, name=name, dimensional_bias=bias)
        self.genes[gene.gene_id] = gene
        return gene

    def genome_summary(self) -> Dict:
        return {
            "genome_id": self.genome_id,
            "total_genes": len(self.genes),
            "growth_rules": len(self.growth_rules),
            "generation": self.generation,
            "active_expressions": len(self.active_expressions),
            "avg_fitness": sum(self.fitness_history[-10:]) / max(len(self.fitness_history[-10:]), 1),
            "gene_types": {
                gtype.name: sum(1 for g in self.genes.values() if g.gene_type == gtype)
                for gtype in GeneType
            }
        }