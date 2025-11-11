"""
Entity storage and retrieval system.

Uses the LocalFileDB to persist entities and relationships.
"""

from typing import List, Optional, Dict, Any
import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from research.entities import Entity, EntityRelationship, EntityType, RelationType, BenchmarkScore
from local_db import LocalFileDB


class EntityStore:
    """
    Storage layer for entities and relationships.
    
    Provides CRUD operations and querying capabilities.
    """
    
    def __init__(self, root_dir: str = None):
        """
        Initialize entity store.
        
        Args:
            root_dir: Root directory for storage. Defaults to ../data/research
        """
        if root_dir is None:
            root_dir = Path(__file__).parent.parent.parent / "data" / "research"
        
        self.entities_db = LocalFileDB(str(Path(root_dir) / "entities"))
        self.relationships_db = LocalFileDB(str(Path(root_dir) / "relationships"))
        self.benchmarks_db = LocalFileDB(str(Path(root_dir) / "benchmarks"))
    
    # Entity operations
    def save_entity(self, entity: Entity) -> None:
        """Save or update an entity."""
        self.entities_db.save(entity.id, entity.to_dict())
    
    def get_entity(self, entity_id: str) -> Optional[Entity]:
        """Retrieve an entity by ID."""
        try:
            data = self.entities_db.get(entity_id)
            return Entity.from_dict(data)
        except KeyError:
            return None
    
    def delete_entity(self, entity_id: str) -> None:
        """Delete an entity."""
        self.entities_db.delete(entity_id)
    
    def list_entities(self, entity_type: Optional[EntityType] = None) -> List[Entity]:
        """
        List all entities, optionally filtered by type.
        
        Args:
            entity_type: Optional filter by entity type
            
        Returns:
            List of entities
        """
        entities = []
        for key in self.entities_db.list_keys():
            entity = self.get_entity(key)
            if entity and (entity_type is None or entity.entity_type == entity_type):
                entities.append(entity)
        return entities
    
    def search_entities(self, query: str, entity_type: Optional[EntityType] = None) -> List[Entity]:
        """
        Search entities by name or features.
        
        Args:
            query: Search query string
            entity_type: Optional filter by entity type
            
        Returns:
            List of matching entities
        """
        query_lower = query.lower()
        results = []
        
        for entity in self.list_entities(entity_type):
            # Search in name
            if query_lower in entity.name.lower():
                results.append(entity)
                continue
            
            # Search in features (values only)
            for value in entity.features.values():
                if isinstance(value, str) and query_lower in value.lower():
                    results.append(entity)
                    break
        
        return results
    
    # Relationship operations
    def save_relationship(self, relationship: EntityRelationship) -> None:
        """Save a relationship."""
        rel_id = f"{relationship.source_id}_{relationship.relation_type.value}_{relationship.target_id}"
        self.relationships_db.save(rel_id, relationship.to_dict())
    
    def get_relationships(
        self, 
        source_id: Optional[str] = None,
        target_id: Optional[str] = None,
        relation_type: Optional[RelationType] = None
    ) -> List[EntityRelationship]:
        """
        Get relationships with optional filters.
        
        Args:
            source_id: Filter by source entity
            target_id: Filter by target entity
            relation_type: Filter by relationship type
            
        Returns:
            List of matching relationships
        """
        relationships = []
        for key in self.relationships_db.list_keys():
            try:
                data = self.relationships_db.get(key)
                rel = EntityRelationship.from_dict(data)
                
                # Apply filters
                if source_id and rel.source_id != source_id:
                    continue
                if target_id and rel.target_id != target_id:
                    continue
                if relation_type and rel.relation_type != relation_type:
                    continue
                
                relationships.append(rel)
            except Exception:
                continue
        
        return relationships
    
    # Benchmark operations
    def save_benchmark_score(self, score: BenchmarkScore) -> None:
        """Save a benchmark score."""
        score_id = f"{score.method_id}_{score.benchmark_id}_{score.metric_name}"
        self.benchmarks_db.save(score_id, score.to_dict())
    
    def get_benchmark_scores(
        self,
        method_id: Optional[str] = None,
        benchmark_id: Optional[str] = None,
        metric_name: Optional[str] = None
    ) -> List[BenchmarkScore]:
        """
        Get benchmark scores with optional filters.
        
        Args:
            method_id: Filter by method
            benchmark_id: Filter by benchmark
            metric_name: Filter by metric
            
        Returns:
            List of matching benchmark scores
        """
        scores = []
        for key in self.benchmarks_db.list_keys():
            try:
                data = self.benchmarks_db.get(key)
                score = BenchmarkScore(**data)
                
                # Apply filters
                if method_id and score.method_id != method_id:
                    continue
                if benchmark_id and score.benchmark_id != benchmark_id:
                    continue
                if metric_name and score.metric_name != metric_name:
                    continue
                
                scores.append(score)
            except Exception:
                continue
        
        return scores
    
    def get_top_performers(
        self,
        benchmark_id: str,
        metric_name: str,
        limit: int = 10,
        higher_is_better: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Get top performing methods on a specific benchmark.
        
        Args:
            benchmark_id: The benchmark to query
            metric_name: The metric to rank by
            limit: Maximum number of results
            higher_is_better: Whether higher scores are better
            
        Returns:
            List of dicts with method info and scores
        """
        scores = self.get_benchmark_scores(
            benchmark_id=benchmark_id,
            metric_name=metric_name
        )
        
        # Sort scores
        sorted_scores = sorted(
            scores,
            key=lambda x: x.score,
            reverse=higher_is_better
        )[:limit]
        
        # Enrich with method details
        results = []
        for score in sorted_scores:
            method = self.get_entity(score.method_id)
            if method:
                results.append({
                    "method": method,
                    "score": score.score,
                    "metric": metric_name,
                    "benchmark": benchmark_id,
                    "metadata": score.metadata
                })
        
        return results
