"""
Entity definitions for the research comparison system.

Entities represent methods, papers, repositories, benchmarks, etc.
that can be compared and analyzed.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from enum import Enum
from datetime import datetime


class EntityType(Enum):
    """Types of entities in the research system."""
    METHOD = "method"
    PAPER = "paper"
    REPOSITORY = "repository"
    BENCHMARK = "benchmark"
    DATASET = "dataset"
    FEATURE = "feature"
    METRIC = "metric"


class RelationType(Enum):
    """Types of relationships between entities."""
    IMPLEMENTS = "implements"
    USES = "uses"
    IMPROVES_UPON = "improves_upon"
    EVALUATED_ON = "evaluated_on"
    PART_OF = "part_of"
    COMPARED_WITH = "compared_with"
    BASED_ON = "based_on"


@dataclass
class Entity:
    """
    Core entity class representing any research artifact.
    
    Attributes:
        id: Unique identifier
        name: Human-readable name
        entity_type: Type of entity
        features: Dictionary of features and their values
        metadata: Additional metadata (urls, authors, dates, etc.)
        created_at: Timestamp of creation
    """
    id: str
    name: str
    entity_type: EntityType
    features: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    
    def add_feature(self, key: str, value: Any) -> None:
        """Add or update a feature."""
        self.features[key] = value
    
    def get_feature(self, key: str, default: Any = None) -> Any:
        """Get a feature value."""
        return self.features.get(key, default)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert entity to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "entity_type": self.entity_type.value,
            "features": self.features,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Entity":
        """Create entity from dictionary."""
        return cls(
            id=data["id"],
            name=data["name"],
            entity_type=EntityType(data["entity_type"]),
            features=data.get("features", {}),
            metadata=data.get("metadata", {}),
            created_at=datetime.fromisoformat(data["created_at"]) if "created_at" in data else datetime.now()
        )


@dataclass
class EntityRelationship:
    """
    Represents a relationship between two entities.
    
    Attributes:
        source_id: ID of the source entity
        target_id: ID of the target entity
        relation_type: Type of relationship
        properties: Additional properties of the relationship
        confidence: Confidence score (0-1) if extracted automatically
    """
    source_id: str
    target_id: str
    relation_type: RelationType
    properties: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 1.0
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert relationship to dictionary."""
        return {
            "source_id": self.source_id,
            "target_id": self.target_id,
            "relation_type": self.relation_type.value,
            "properties": self.properties,
            "confidence": self.confidence,
            "created_at": self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EntityRelationship":
        """Create relationship from dictionary."""
        return cls(
            source_id=data["source_id"],
            target_id=data["target_id"],
            relation_type=RelationType(data["relation_type"]),
            properties=data.get("properties", {}),
            confidence=data.get("confidence", 1.0),
            created_at=datetime.fromisoformat(data["created_at"]) if "created_at" in data else datetime.now()
        )


@dataclass
class BenchmarkScore:
    """
    Represents a benchmark score for a method.
    
    Attributes:
        method_id: ID of the method
        benchmark_id: ID of the benchmark/dataset
        metric_name: Name of the metric (e.g., 'accuracy', 'F1', 'BLEU')
        score: The actual score value
        metadata: Additional context (e.g., hardware, date, conditions)
    """
    method_id: str
    benchmark_id: str
    metric_name: str
    score: float
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert benchmark score to dictionary."""
        return {
            "method_id": self.method_id,
            "benchmark_id": self.benchmark_id,
            "metric_name": self.metric_name,
            "score": self.score,
            "metadata": self.metadata
        }
