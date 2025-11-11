"""
Complete demo of the Research Comparison System.

This demo shows how to:
1. Extract data from existing papers
2. Manually add benchmark data
3. Find state-of-the-art methods
4. Generate comparison reports
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from research.entities import Entity, EntityType, BenchmarkScore, EntityRelationship, RelationType
from research.entity_store import EntityStore
from research.comparison_engine import ComparisonEngine
from research.research_pipeline import ResearchPipeline


def setup_demo_data():
    """
    Set up demo data for RAG methods.
    
    This simulates what would be extracted from papers,
    but we're adding it manually for demonstration.
    """
    print("Setting up demo data for RAG comparison...")
    
    store = EntityStore()
    
    # Create benchmark entity
    beir_benchmark = Entity(
        id="benchmark_beir",
        name="BEIR Benchmark",
        entity_type=EntityType.BENCHMARK,
        features={
            "description": "Diverse information retrieval benchmark",
            "num_datasets": 18,
            "domain": "information retrieval"
        }
    )
    store.save_entity(beir_benchmark)
    
    # Create RAG methods
    methods_data = [
        {
            "id": "method_dense_passage_retrieval",
            "name": "Dense Passage Retrieval (DPR)",
            "features": {
                "architecture": "Dual encoder",
                "year": 2020,
                "open_source": True,
                "description": "Dense retrieval using BERT encoders"
            },
            "scores": {"NDCG@10": 0.530, "Recall@100": 0.782}
        },
        {
            "id": "method_colbert",
            "name": "ColBERT",
            "features": {
                "architecture": "Late interaction",
                "year": 2020,
                "open_source": True,
                "description": "Contextualized late interaction over BERT"
            },
            "scores": {"NDCG@10": 0.521, "Recall@100": 0.758}
        },
        {
            "id": "method_ance",
            "name": "ANCE",
            "features": {
                "architecture": "Dense retrieval with hard negatives",
                "year": 2020,
                "open_source": True,
                "description": "Approximate nearest neighbor negative contrastive learning"
            },
            "scores": {"NDCG@10": 0.547, "Recall@100": 0.801}
        },
        {
            "id": "method_splade",
            "name": "SPLADE",
            "features": {
                "architecture": "Sparse learned representations",
                "year": 2021,
                "open_source": True,
                "description": "Sparse lexical and expansion model"
            },
            "scores": {"NDCG@10": 0.498, "Recall@100": 0.721}
        },
        {
            "id": "method_retrieval_augmented_generation",
            "name": "RAG (Lewis et al.)",
            "features": {
                "architecture": "Retrieval + generation",
                "year": 2020,
                "open_source": True,
                "description": "Retrieval-augmented generation for knowledge-intensive NLP"
            },
            "scores": {"NDCG@10": 0.442, "Recall@100": 0.653}
        },
        {
            "id": "method_retro",
            "name": "RETRO",
            "features": {
                "architecture": "Chunked cross-attention retrieval",
                "year": 2021,
                "open_source": False,
                "description": "Retrieval-enhanced transformer"
            },
            "scores": {"NDCG@10": 0.573, "Recall@100": 0.832}
        }
    ]
    
    for method_data in methods_data:
        # Create method entity
        method = Entity(
            id=method_data["id"],
            name=method_data["name"],
            entity_type=EntityType.METHOD,
            features=method_data["features"]
        )
        store.save_entity(method)
        
        # Create relationship
        rel = EntityRelationship(
            source_id=method.id,
            target_id=beir_benchmark.id,
            relation_type=RelationType.EVALUATED_ON
        )
        store.save_relationship(rel)
        
        # Add benchmark scores
        for metric_name, score in method_data["scores"].items():
            benchmark_score = BenchmarkScore(
                method_id=method.id,
                benchmark_id=beir_benchmark.id,
                metric_name=metric_name,
                score=score,
                metadata={"source": "Demo data"}
            )
            store.save_benchmark_score(benchmark_score)
    
    print(f"✓ Created {len(methods_data)} RAG methods")
    print(f"✓ Created 1 benchmark (BEIR)")
    print(f"✓ Added {len(methods_data) * 2} benchmark scores\n")
    
    return store


def demo_1_list_entities(store):
    """Demo 1: List all stored entities."""
    print("=" * 60)
    print("DEMO 1: List All Entities")
    print("=" * 60 + "\n")
    
    methods = store.list_entities(EntityType.METHOD)
    print(f"Stored Methods ({len(methods)}):")
    for method in methods:
        print(f"  • {method.name}")
        print(f"    - Year: {method.get_feature('year', 'N/A')}")
        print(f"    - Architecture: {method.get_feature('architecture', 'N/A')}")
    
    print()


def demo_2_find_sota(store):
    """Demo 2: Find state-of-the-art RAG methods."""
    print("=" * 60)
    print("DEMO 2: Find State-of-the-Art RAG Methods")
    print("=" * 60 + "\n")
    
    engine = ComparisonEngine(store)
    
    # Find top performers on NDCG@10
    result = engine.compare_methods_on_benchmark(
        benchmark_id="benchmark_beir",
        metric_name="NDCG@10",
        limit=5,
        higher_is_better=True
    )
    
    print("Top 5 RAG Methods on BEIR (NDCG@10):\n")
    for ranking in result.rankings:
        print(f"{ranking['rank']}. {ranking['name']}")
        print(f"   Score: {ranking['score']:.4f}")
        print()


def demo_3_compare_specific_methods(store):
    """Demo 3: Compare specific methods."""
    print("=" * 60)
    print("DEMO 3: Compare Specific Methods")
    print("=" * 60 + "\n")
    
    engine = ComparisonEngine(store)
    
    # Compare DPR, ColBERT, and ANCE
    entity_ids = [
        "method_dense_passage_retrieval",
        "method_colbert",
        "method_ance"
    ]
    
    result = engine.compare_entities_by_features(entity_ids)
    
    print("Feature Comparison: DPR vs ColBERT vs ANCE\n")
    
    # Print feature matrix
    matrix = result.feature_matrix
    if "entity_name" in matrix:
        features = [k for k in matrix.keys() if k != "entity_name"]
        
        # Print header
        print(f"{'Feature':<30} | " + " | ".join([f"{name:<20}" for name in matrix["entity_name"]]))
        print("-" * 100)
        
        # Print each feature
        for feature in features:
            if feature in ['architecture', 'year', 'open_source']:
                values = matrix[feature]
                print(f"{feature:<30} | " + " | ".join([f"{str(v):<20}" for v in values]))
    
    print()


def demo_4_benchmark_comparison(store):
    """Demo 4: Compare all methods across multiple metrics."""
    print("=" * 60)
    print("DEMO 4: Multi-Metric Benchmark Comparison")
    print("=" * 60 + "\n")
    
    # Get all benchmark scores
    scores_ndcg = store.get_benchmark_scores(
        benchmark_id="benchmark_beir",
        metric_name="NDCG@10"
    )
    scores_recall = store.get_benchmark_scores(
        benchmark_id="benchmark_beir",
        metric_name="Recall@100"
    )
    
    # Organize by method
    method_scores = {}
    
    for score in scores_ndcg:
        method = store.get_entity(score.method_id)
        if method:
            method_scores[method.name] = {"NDCG@10": score.score}
    
    for score in scores_recall:
        method = store.get_entity(score.method_id)
        if method and method.name in method_scores:
            method_scores[method.name]["Recall@100"] = score.score
    
    # Print comparison table
    print(f"{'Method':<40} | {'NDCG@10':<10} | {'Recall@100':<10}")
    print("-" * 65)
    
    for method_name in sorted(method_scores.keys(), 
                             key=lambda x: method_scores[x].get("NDCG@10", 0),
                             reverse=True):
        scores = method_scores[method_name]
        ndcg = scores.get("NDCG@10", 0)
        recall = scores.get("Recall@100", 0)
        print(f"{method_name:<40} | {ndcg:<10.4f} | {recall:<10.4f}")
    
    print()


def demo_5_full_pipeline():
    """Demo 5: Full pipeline with report generation."""
    print("=" * 60)
    print("DEMO 5: Full Pipeline with Report Generation")
    print("=" * 60 + "\n")
    
    pipeline = ResearchPipeline()
    
    # Find SOTA for RAG
    result = pipeline.find_sota(
        domain="RAG",
        benchmark_id="benchmark_beir",
        metric_name="NDCG@10"
    )
    
    # Generate report
    report = pipeline.generate_report(result)
    print(report)
    
    # Save to file
    report_path = Path(__file__).parent.parent / "data" / "rag_sota_report.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✓ Report saved to: {report_path}")


def main():
    """Run all demos."""
    print("\n" + "=" * 60)
    print("RESEARCH COMPARISON SYSTEM - COMPLETE DEMO")
    print("=" * 60 + "\n")
    
    # Setup demo data
    store = setup_demo_data()
    
    # Run demos
    demo_1_list_entities(store)
    demo_2_find_sota(store)
    demo_3_compare_specific_methods(store)
    demo_4_benchmark_comparison(store)
    demo_5_full_pipeline()
    
    print("=" * 60)
    print("DEMO COMPLETED!")
    print("=" * 60 + "\n")
    print("Next steps:")
    print("1. Try CLI: python src/research/research_cli.py --help")
    print("2. Add your own papers: python src/research/research_cli.py research --papers <arxiv_id>")
    print("3. Find SOTA: python src/research/research_cli.py sota --domain 'your domain'")
    print()


if __name__ == "__main__":
    main()
