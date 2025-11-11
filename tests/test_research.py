"""
Tests for the research comparison system.
"""

import pytest
import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from research.entities import (
    Entity, EntityRelationship, EntityType, 
    RelationType, BenchmarkScore
)
from research.entity_store import EntityStore
from research.comparison_engine import ComparisonEngine
from research.research_pipeline import ResearchPipeline


class TestEntities:
    """Test entity classes."""
    
    def test_entity_creation(self):
        """Test creating an entity."""
        entity = Entity(
            id="test_method",
            name="Test Method",
            entity_type=EntityType.METHOD,
            features={"accuracy": 0.95},
            metadata={"year": 2024}
        )
        
        assert entity.id == "test_method"
        assert entity.name == "Test Method"
        assert entity.entity_type == EntityType.METHOD
        assert entity.get_feature("accuracy") == 0.95
    
    def test_entity_serialization(self):
        """Test entity to/from dict."""
        entity = Entity(
            id="test",
            name="Test",
            entity_type=EntityType.PAPER
        )
        
        data = entity.to_dict()
        restored = Entity.from_dict(data)
        
        assert restored.id == entity.id
        assert restored.name == entity.name
        assert restored.entity_type == entity.entity_type
    
    def test_relationship_creation(self):
        """Test creating a relationship."""
        rel = EntityRelationship(
            source_id="method1",
            target_id="benchmark1",
            relation_type=RelationType.EVALUATED_ON,
            confidence=0.95
        )
        
        assert rel.source_id == "method1"
        assert rel.target_id == "benchmark1"
        assert rel.relation_type == RelationType.EVALUATED_ON
        assert rel.confidence == 0.95
    
    def test_benchmark_score(self):
        """Test benchmark score."""
        score = BenchmarkScore(
            method_id="method1",
            benchmark_id="bench1",
            metric_name="accuracy",
            score=0.923
        )
        
        assert score.method_id == "method1"
        assert score.score == 0.923


class TestEntityStore:
    """Test entity store."""
    
    @pytest.fixture
    def temp_store(self, tmp_path):
        """Create a temporary entity store."""
        return EntityStore(str(tmp_path))
    
    def test_save_and_get_entity(self, temp_store):
        """Test saving and retrieving an entity."""
        entity = Entity(
            id="test1",
            name="Test Entity",
            entity_type=EntityType.METHOD
        )
        
        temp_store.save_entity(entity)
        retrieved = temp_store.get_entity("test1")
        
        assert retrieved is not None
        assert retrieved.id == entity.id
        assert retrieved.name == entity.name
    
    def test_list_entities(self, temp_store):
        """Test listing entities."""
        # Create multiple entities
        for i in range(3):
            entity = Entity(
                id=f"method{i}",
                name=f"Method {i}",
                entity_type=EntityType.METHOD
            )
            temp_store.save_entity(entity)
        
        # Create a paper entity
        paper = Entity(
            id="paper1",
            name="Paper 1",
            entity_type=EntityType.PAPER
        )
        temp_store.save_entity(paper)
        
        # List all entities
        all_entities = temp_store.list_entities()
        assert len(all_entities) == 4
        
        # List only methods
        methods = temp_store.list_entities(EntityType.METHOD)
        assert len(methods) == 3
    
    def test_search_entities(self, temp_store):
        """Test searching entities."""
        entity1 = Entity(
            id="rag_method",
            name="RAG System",
            entity_type=EntityType.METHOD
        )
        entity2 = Entity(
            id="colbert_method",
            name="ColBERT",
            entity_type=EntityType.METHOD
        )
        
        temp_store.save_entity(entity1)
        temp_store.save_entity(entity2)
        
        # Search for RAG
        results = temp_store.search_entities("RAG")
        assert len(results) == 1
        assert results[0].name == "RAG System"
    
    def test_save_and_get_relationships(self, temp_store):
        """Test saving and retrieving relationships."""
        rel = EntityRelationship(
            source_id="method1",
            target_id="benchmark1",
            relation_type=RelationType.EVALUATED_ON
        )
        
        temp_store.save_relationship(rel)
        
        # Get relationships by source
        rels = temp_store.get_relationships(source_id="method1")
        assert len(rels) == 1
        assert rels[0].source_id == "method1"
    
    def test_benchmark_scores(self, temp_store):
        """Test benchmark score operations."""
        score = BenchmarkScore(
            method_id="method1",
            benchmark_id="bench1",
            metric_name="accuracy",
            score=0.95
        )
        
        temp_store.save_benchmark_score(score)
        
        # Get scores by method
        scores = temp_store.get_benchmark_scores(method_id="method1")
        assert len(scores) == 1
        assert scores[0].score == 0.95
    
    def test_top_performers(self, temp_store):
        """Test getting top performers."""
        # Create methods
        for i in range(3):
            method = Entity(
                id=f"method{i}",
                name=f"Method {i}",
                entity_type=EntityType.METHOD
            )
            temp_store.save_entity(method)
            
            # Add scores
            score = BenchmarkScore(
                method_id=method.id,
                benchmark_id="bench1",
                metric_name="accuracy",
                score=0.8 + i * 0.05  # 0.80, 0.85, 0.90
            )
            temp_store.save_benchmark_score(score)
        
        # Get top performers
        top = temp_store.get_top_performers(
            benchmark_id="bench1",
            metric_name="accuracy",
            limit=2,
            higher_is_better=True
        )
        
        assert len(top) == 2
        assert top[0]["method"].id == "method2"  # Highest score
        assert top[0]["score"] == 0.90


class TestComparisonEngine:
    """Test comparison engine."""
    
    @pytest.fixture
    def engine_with_data(self, tmp_path):
        """Create engine with sample data."""
        store = EntityStore(str(tmp_path))
        
        # Create methods
        for i in range(3):
            method = Entity(
                id=f"method{i}",
                name=f"RAG Method {i}",
                entity_type=EntityType.METHOD,
                features={
                    "architecture": f"Type {i}",
                    "year": 2023 + i
                }
            )
            store.save_entity(method)
            
            # Add benchmark scores
            score = BenchmarkScore(
                method_id=method.id,
                benchmark_id="beir",
                metric_name="NDCG@10",
                score=0.70 + i * 0.05
            )
            store.save_benchmark_score(score)
        
        return ComparisonEngine(store)
    
    def test_compare_on_benchmark(self, engine_with_data):
        """Test comparing methods on a benchmark."""
        result = engine_with_data.compare_methods_on_benchmark(
            benchmark_id="beir",
            metric_name="NDCG@10",
            limit=3
        )
        
        assert len(result.entities) == 3
        assert len(result.rankings) == 3
        assert result.rankings[0]["rank"] == 1
        assert "summary" in result.summary
    
    def test_compare_by_features(self, engine_with_data):
        """Test comparing entities by features."""
        result = engine_with_data.compare_entities_by_features(
            entity_ids=["method0", "method1"]
        )
        
        assert len(result.entities) == 2
        assert "feature_matrix" in result.feature_matrix
    
    def test_find_best_solution(self, engine_with_data):
        """Test finding best solution."""
        result = engine_with_data.find_best_solution(
            query="RAG",
            benchmark_id="beir",
            metric_name="NDCG@10"
        )
        
        assert len(result.entities) > 0
        assert len(result.rankings) > 0


class TestResearchPipeline:
    """Test research pipeline."""
    
    @pytest.fixture
    def pipeline(self, tmp_path):
        """Create pipeline with temporary storage."""
        return ResearchPipeline(str(tmp_path))
    
    def test_pipeline_initialization(self, pipeline):
        """Test pipeline initializes correctly."""
        assert pipeline.store is not None
        assert pipeline.engine is not None
        assert pipeline.paper_extractor is not None
    
    def test_find_sota(self, pipeline):
        """Test SOTA finding with no data."""
        result = pipeline.find_sota("nonexistent domain")
        
        assert "domain" in result
        assert "rankings" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
