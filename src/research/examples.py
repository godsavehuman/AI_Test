"""
Example usage of the research comparison system.

Demonstrates how to:
1. Research papers from arXiv
2. Extract entities and benchmarks
3. Find state-of-the-art methods
4. Compare methods
5. Generate reports
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from research.research_pipeline import ResearchPipeline, quick_research
from research.entities import EntityType


def example_1_basic_research():
    """Example 1: Basic research from arXiv papers."""
    print("=" * 60)
    print("Example 1: Basic Research from arXiv Papers")
    print("=" * 60 + "\n")
    
    pipeline = ResearchPipeline()
    
    # Research papers (example paper IDs - replace with real ones)
    paper_ids = ["2507.03254v1", "2510.04607"]
    
    print("Researching papers...")
    result = pipeline.research_from_arxiv(paper_ids)
    
    print(f"\nResults:")
    print(f"- Entities extracted: {len(result['entities'])}")
    print(f"- Relationships found: {len(result['relationships'])}")
    print(f"- Benchmarks recorded: {len(result['benchmarks'])}")


def example_2_find_sota():
    """Example 2: Find state-of-the-art RAG methods."""
    print("\n" + "=" * 60)
    print("Example 2: Find State-of-the-Art RAG Methods")
    print("=" * 60 + "\n")
    
    pipeline = ResearchPipeline()
    
    # Find SOTA for RAG
    result = pipeline.find_sota(
        domain="RAG",
        # Optionally specify benchmark and metric
        # benchmark_id="benchmark_beir",
        # metric_name="NDCG@10"
    )
    
    # Generate and print report
    report = pipeline.generate_report(result)
    print(report)


def example_3_compare_methods():
    """Example 3: Compare specific methods."""
    print("\n" + "=" * 60)
    print("Example 3: Compare Specific Methods")
    print("=" * 60 + "\n")
    
    pipeline = ResearchPipeline()
    
    # Compare methods by name
    methods = ["RAG", "ColBERT", "DPR"]
    result = pipeline.compare_methods(methods)
    
    if "error" not in result:
        report = pipeline.generate_report(result)
        print(report)
    else:
        print(f"Error: {result['error']}")


def example_4_query_entities():
    """Example 4: Query stored entities."""
    print("\n" + "=" * 60)
    print("Example 4: Query Stored Entities")
    print("=" * 60 + "\n")
    
    pipeline = ResearchPipeline()
    
    # List all methods
    methods = pipeline.store.list_entities(EntityType.METHOD)
    print(f"Stored Methods ({len(methods)}):")
    for method in methods[:5]:  # Show first 5
        print(f"  - {method.name}")
        if method.features:
            print(f"    Features: {list(method.features.keys())}")
    
    # Search for specific entities
    print("\nSearching for 'RAG' methods:")
    results = pipeline.store.search_entities("RAG", EntityType.METHOD)
    for result in results:
        print(f"  - {result.name}")


def example_5_quick_research():
    """Example 5: Quick research using convenience function."""
    print("\n" + "=" * 60)
    print("Example 5: Quick Research")
    print("=" * 60 + "\n")
    
    # Quick research and report generation in one call
    report = quick_research(
        query="RAG methods",
        paper_ids=["2507.03254v1"],  # Optional
        benchmark_id="benchmark_beir",  # Optional
        metric_name="NDCG@10"  # Optional
    )
    
    print(report)


def example_6_manual_entity_creation():
    """Example 6: Manually create and store entities."""
    print("\n" + "=" * 60)
    print("Example 6: Manual Entity Creation")
    print("=" * 60 + "\n")
    
    from research.entities import Entity, BenchmarkScore, EntityRelationship, RelationType
    from research.entity_store import EntityStore
    
    store = EntityStore()
    
    # Create a method entity manually
    method = Entity(
        id="method_custom_rag",
        name="Custom RAG System",
        entity_type=EntityType.METHOD,
        features={
            "architecture": "Dense retrieval + GPT-4",
            "year": 2024,
            "open_source": True
        },
        metadata={
            "authors": ["John Doe", "Jane Smith"],
            "institution": "Example University"
        }
    )
    
    store.save_entity(method)
    print(f"Created method: {method.name}")
    
    # Create a benchmark
    benchmark = Entity(
        id="benchmark_custom_qa",
        name="Custom QA Dataset",
        entity_type=EntityType.BENCHMARK,
        features={
            "domain": "question answering",
            "size": 10000
        }
    )
    
    store.save_entity(benchmark)
    print(f"Created benchmark: {benchmark.name}")
    
    # Create a benchmark score
    score = BenchmarkScore(
        method_id=method.id,
        benchmark_id=benchmark.id,
        metric_name="accuracy",
        score=0.923,
        metadata={"hardware": "NVIDIA A100"}
    )
    
    store.save_benchmark_score(score)
    print(f"Recorded score: {score.score} on {score.metric_name}")
    
    # Create a relationship
    relationship = EntityRelationship(
        source_id=method.id,
        target_id=benchmark.id,
        relation_type=RelationType.EVALUATED_ON,
        confidence=1.0
    )
    
    store.save_relationship(relationship)
    print(f"Created relationship: {method.name} -> {benchmark.name}")


if __name__ == "__main__":
    # Run examples
    print("\n" + "=" * 60)
    print("Research Comparison System - Usage Examples")
    print("=" * 60)
    
    # Uncomment the examples you want to run
    
    # example_1_basic_research()
    # example_2_find_sota()
    # example_3_compare_methods()
    # example_4_query_entities()
    # example_5_quick_research()
    example_6_manual_entity_creation()
    
    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60)
