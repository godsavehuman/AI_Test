"""
Research Comparison System

A system for comparing research methods, tools, and approaches across
papers and repositories. Extracts entities, features, and benchmarks
to enable comprehensive comparisons.
"""

# Entities are imported directly without circular dependencies
from research.entities import Entity, EntityRelationship, EntityType

# Other modules can be imported when needed
__all__ = [
    "Entity",
    "EntityRelationship", 
    "EntityType",
]
