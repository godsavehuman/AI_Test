"""
Comparison engine for analyzing and comparing entities.

Provides ranking, feature comparison, and analysis capabilities.
"""

from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from research.entities import Entity, EntityType, BenchmarkScore
from research.entity_store import EntityStore


class RankingStrategy(Enum):
    """Strategies for ranking entities."""
    SCORE_BASED = "score_based"  # Rank by benchmark scores
    FEATURE_BASED = "feature_based"  # Rank by feature values
    HYBRID = "hybrid"  # Combination of scores and features


@dataclass
class ComparisonResult:
    """Result of comparing entities."""
    entities: List[Entity]
    rankings: List[Dict[str, Any]]  # Ranked list with scores
    feature_matrix: Dict[str, List[Any]]  # Feature comparison matrix
    summary: str  # Human-readable summary


class ComparisonEngine:
    """
    Engine for comparing and ranking entities.
    
    Supports multiple comparison strategies and customizable ranking.
    """
    
    def __init__(self, entity_store: EntityStore):
        """
        Initialize comparison engine.
        
        Args:
            entity_store: EntityStore instance for data access
        """
        self.store = entity_store
    
    def compare_methods_on_benchmark(
        self,
        benchmark_id: str,
        metric_name: str,
        limit: int = 10,
        higher_is_better: bool = True
    ) -> ComparisonResult:
        """
        Compare methods on a specific benchmark.
        
        Args:
            benchmark_id: Benchmark to compare on
            metric_name: Metric to use for comparison
            limit: Maximum number of methods to return
            higher_is_better: Whether higher scores are better
            
        Returns:
            ComparisonResult with ranked methods
        """
        # Get top performers
        top_performers = self.store.get_top_performers(
            benchmark_id=benchmark_id,
            metric_name=metric_name,
            limit=limit,
            higher_is_better=higher_is_better
        )
        
        if not top_performers:
            return ComparisonResult(
                entities=[],
                rankings=[],
                feature_matrix={},
                summary=f"No results found for {benchmark_id} on metric {metric_name}"
            )
        
        # Extract entities and build rankings
        entities = [p["method"] for p in top_performers]
        rankings = [
            {
                "rank": idx + 1,
                "entity_id": p["method"].id,
                "name": p["method"].name,
                "score": p["score"],
                "metric": metric_name,
                "metadata": p["metadata"]
            }
            for idx, p in enumerate(top_performers)
        ]
        
        # Build feature matrix
        feature_matrix = self._build_feature_matrix(entities)
        
        # Generate summary
        summary = self._generate_benchmark_summary(
            benchmark_id, metric_name, rankings, higher_is_better
        )
        
        return ComparisonResult(
            entities=entities,
            rankings=rankings,
            feature_matrix=feature_matrix,
            summary=summary
        )
    
    def compare_entities_by_features(
        self,
        entity_ids: List[str],
        features: Optional[List[str]] = None
    ) -> ComparisonResult:
        """
        Compare entities by their features.
        
        Args:
            entity_ids: List of entity IDs to compare
            features: Optional list of specific features to compare
            
        Returns:
            ComparisonResult with feature comparison
        """
        # Retrieve entities
        entities = []
        for entity_id in entity_ids:
            entity = self.store.get_entity(entity_id)
            if entity:
                entities.append(entity)
        
        if not entities:
            return ComparisonResult(
                entities=[],
                rankings=[],
                feature_matrix={},
                summary="No entities found for comparison"
            )
        
        # Build feature matrix
        feature_matrix = self._build_feature_matrix(entities, features)
        
        # Simple ranking by number of features
        rankings = [
            {
                "rank": idx + 1,
                "entity_id": entity.id,
                "name": entity.name,
                "feature_count": len(entity.features),
                "type": entity.entity_type.value
            }
            for idx, entity in enumerate(
                sorted(entities, key=lambda e: len(e.features), reverse=True)
            )
        ]
        
        # Generate summary
        summary = self._generate_feature_summary(entities, feature_matrix)
        
        return ComparisonResult(
            entities=entities,
            rankings=rankings,
            feature_matrix=feature_matrix,
            summary=summary
        )
    
    def find_best_solution(
        self,
        query: str,
        benchmark_id: Optional[str] = None,
        metric_name: Optional[str] = None,
        constraints: Optional[Dict[str, Any]] = None
    ) -> ComparisonResult:
        """
        Find the best solution for a given query.
        
        This is the main method for answering questions like
        "What's the best RAG method?"
        
        Args:
            query: Natural language query
            benchmark_id: Optional benchmark to filter by
            metric_name: Optional metric to rank by
            constraints: Optional constraints (e.g., {"year": ">=2023"})
            
        Returns:
            ComparisonResult with best solutions
        """
        # Search for relevant entities
        entities = self.store.search_entities(query, EntityType.METHOD)
        
        if not entities:
            return ComparisonResult(
                entities=[],
                rankings=[],
                feature_matrix={},
                summary=f"No methods found matching query: {query}"
            )
        
        # If benchmark and metric specified, rank by scores
        if benchmark_id and metric_name:
            # Filter entities that have scores on this benchmark
            entity_ids = [e.id for e in entities]
            scores = self.store.get_benchmark_scores(
                benchmark_id=benchmark_id,
                metric_name=metric_name
            )
            
            scored_entities = []
            for score in scores:
                if score.method_id in entity_ids:
                    entity = self.store.get_entity(score.method_id)
                    if entity:
                        scored_entities.append((entity, score.score))
            
            # Sort by score
            scored_entities.sort(key=lambda x: x[1], reverse=True)
            entities = [e for e, _ in scored_entities[:10]]
            
            rankings = [
                {
                    "rank": idx + 1,
                    "entity_id": entity.id,
                    "name": entity.name,
                    "score": score,
                    "metric": metric_name
                }
                for idx, (entity, score) in enumerate(scored_entities[:10])
            ]
        else:
            # Rank by relevance or feature count
            entities = entities[:10]
            rankings = [
                {
                    "rank": idx + 1,
                    "entity_id": entity.id,
                    "name": entity.name,
                    "feature_count": len(entity.features)
                }
                for idx, entity in enumerate(entities)
            ]
        
        # Build feature matrix
        feature_matrix = self._build_feature_matrix(entities)
        
        # Generate summary
        summary = self._generate_solution_summary(query, rankings)
        
        return ComparisonResult(
            entities=entities,
            rankings=rankings,
            feature_matrix=feature_matrix,
            summary=summary
        )
    
    def _build_feature_matrix(
        self,
        entities: List[Entity],
        features: Optional[List[str]] = None
    ) -> Dict[str, List[Any]]:
        """
        Build a feature comparison matrix.
        
        Args:
            entities: List of entities to compare
            features: Optional list of specific features
            
        Returns:
            Dictionary mapping feature names to lists of values
        """
        # Collect all feature keys if not specified
        if features is None:
            feature_keys = set()
            for entity in entities:
                feature_keys.update(entity.features.keys())
            features = sorted(list(feature_keys))
        
        # Build matrix
        matrix = {"entity_name": [e.name for e in entities]}
        
        for feature_key in features:
            matrix[feature_key] = [
                entity.get_feature(feature_key, "N/A")
                for entity in entities
            ]
        
        return matrix
    
    def _generate_benchmark_summary(
        self,
        benchmark_id: str,
        metric_name: str,
        rankings: List[Dict[str, Any]],
        higher_is_better: bool
    ) -> str:
        """Generate human-readable summary for benchmark comparison."""
        if not rankings:
            return f"No results found for {benchmark_id}"
        
        best = rankings[0]
        summary = f"Best performing method on {benchmark_id} ({metric_name}): "
        summary += f"{best['name']} with score {best['score']:.4f}\n\n"
        summary += "Top performers:\n"
        
        for r in rankings[:5]:
            summary += f"{r['rank']}. {r['name']}: {r['score']:.4f}\n"
        
        return summary
    
    def _generate_feature_summary(
        self,
        entities: List[Entity],
        feature_matrix: Dict[str, List[Any]]
    ) -> str:
        """Generate human-readable summary for feature comparison."""
        summary = f"Comparing {len(entities)} entities across {len(feature_matrix)-1} features\n\n"
        
        for entity in entities[:3]:
            summary += f"- {entity.name}: {len(entity.features)} features\n"
        
        return summary
    
    def _generate_solution_summary(
        self,
        query: str,
        rankings: List[Dict[str, Any]]
    ) -> str:
        """Generate human-readable summary for solution search."""
        if not rankings:
            return f"No solutions found for: {query}"
        
        summary = f"Best solutions for '{query}':\n\n"
        
        for r in rankings[:5]:
            summary += f"{r['rank']}. {r['name']}"
            if "score" in r:
                summary += f" (score: {r['score']:.4f})"
            summary += "\n"
        
        return summary
