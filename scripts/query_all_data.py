"""
Query all extracted data: RAG-Gym paper + Graphiti README
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from research.entity_store import EntityStore
from research.comparison_engine import ComparisonEngine

def print_section(title):
    print("\n" + "="*80)
    print(title.center(80))
    print("="*80)

def main():
    store = EntityStore()
    engine = ComparisonEngine(store)
    
    print_section("RESEARCH SYSTEM DATABASE - COMPLETE OVERVIEW")
    
    # 1. Show all entities by type
    print("\n📋 ALL ENTITIES IN DATABASE:")
    
    print("\n  Methods & Products:")
    all_entities = store.list_entities()
    methods = [e for e in all_entities if e.entity_type.value == "method"]
    for method in methods:
        entity_type = method.features.get("product_type", "Method")
        print(f"    • {method.name} ({entity_type})")
    
    print("\n  Benchmarks:")
    benchmarks = [e for e in all_entities if e.entity_type.value == "benchmark"]
    for benchmark in benchmarks:
        print(f"    • {benchmark.name}")
    
    # 2. Show RAG-Gym methods
    print_section("RAG-GYM METHODS (arxiv:2502.13957v2)")
    
    rag_methods = ["method_re2search_plus", "method_re2search", "method_react", "method_search_o1"]
    for method_id in rag_methods:
        method = store.get_entity(method_id)
        if method:
            desc = method.features.get("description", "N/A")
            print(f"\n  {method.name}:")
            print(f"    {desc}")
    
    # 3. Show Graphiti products
    print_section("GRAPHITI KNOWLEDGE GRAPH PRODUCTS")
    
    graphiti = store.get_entity("product_graphiti")
    if graphiti:
        print(f"\n  {graphiti.name} (OSS Framework):")
        print(f"    {graphiti.features.get('description', 'N/A')}")
        print(f"\n    Core Capabilities:")
        for cap in graphiti.features.get("core_capabilities", [])[:3]:
            print(f"      • {cap}")
        print(f"    Supported Databases: {len(graphiti.features.get('supported_databases', []))}")
        print(f"    Supported LLM Providers: {len(graphiti.features.get('supported_llm_providers', []))}")
    
    zep = store.get_entity("product_zep")
    if zep:
        print(f"\n  {zep.name} (Managed Platform):")
        print(f"    {zep.features.get('description', 'N/A')}")
        print(f"    Performance: {zep.features.get('performance', {}).get('retrieval_latency', 'N/A')}")
    
    # 4. Compare RAG methods on HotpotQA
    print_section("RAG METHODS COMPARISON - HotpotQA F1 Score")
    
    comparison = engine.compare_methods_on_benchmark(
        benchmark_id="benchmark_hotpotqa",
        metric_name="F1",
        limit=5
    )
    
    for ranking in comparison.rankings:
        print(f"  {ranking['rank']}. {ranking['name']:20s} {ranking['score']:6.2f}")
    
    # 5. Compare Knowledge Graph frameworks
    print_section("KNOWLEDGE GRAPH FRAMEWORK COMPARISON")
    
    kg_comparison = engine.compare_methods_on_benchmark(
        benchmark_id="benchmark_knowledge_graph_features",
        metric_name="Adaptability",
        limit=4
    )
    
    print("\n  Adaptability (0-100 scale):")
    for ranking in kg_comparison.rankings:
        bar = "█" * int(ranking['score'] / 5)
        print(f"    {ranking['name']:20s} {ranking['score']:5.1f} {bar}")
    
    # Query Latency
    latency_comparison = engine.compare_methods_on_benchmark(
        benchmark_id="benchmark_knowledge_graph_features",
        metric_name="Query_Latency",
        limit=4
    )
    
    print("\n  Query Speed (0-100, higher = faster):")
    for ranking in latency_comparison.rankings:
        bar = "█" * int(ranking['score'] / 5)
        print(f"    {ranking['name']:20s} {ranking['score']:5.1f} {bar}")
    
    # Real-time updates
    realtime_comparison = engine.compare_methods_on_benchmark(
        benchmark_id="benchmark_knowledge_graph_features",
        metric_name="Real_Time_Updates",
        limit=4
    )
    
    print("\n  Real-Time Updates (0-100):")
    for ranking in realtime_comparison.rankings:
        bar = "█" * int(ranking['score'] / 5) if ranking['score'] > 0 else "▒" * 10
        print(f"    {ranking['name']:20s} {ranking['score']:5.1f} {bar}")
    
    # 6. Show average scores across all benchmarks
    print_section("OVERALL PERFORMANCE SUMMARY")
    
    print("\n  RAG Methods (Average F1 across HotpotQA, 2Wiki, Bamboogle):")
    for method_id in rag_methods:
        f1_scores = []
        for bench_id in ["benchmark_hotpotqa", "benchmark_2wikimultihopqa", "benchmark_bamboogle"]:
            scores = store.get_benchmark_scores(benchmark_id=bench_id, method_id=method_id, metric_name="F1")
            if scores:
                f1_scores.append(scores[0].score)
        if f1_scores:
            method = store.get_entity(method_id)
            avg = sum(f1_scores) / len(f1_scores)
            bar = "█" * int(avg / 2.5)
            print(f"    {method.name:20s} {avg:5.2f} {bar}")
    
    print("\n  Knowledge Graph Frameworks (Average across all metrics):")
    kg_methods = ["product_graphiti", "method_graphrag", "method_traditional_rag"]
    for method_id in kg_methods:
        all_scores = []
        for metric in ["Adaptability", "Query_Latency", "Scalability", "Real_Time_Updates", "Temporal_Tracking", "Custom_Entities"]:
            scores = store.get_benchmark_scores(
                benchmark_id="benchmark_knowledge_graph_features",
                method_id=method_id,
                metric_name=metric
            )
            if scores:
                all_scores.append(scores[0].score)
        if all_scores:
            method = store.get_entity(method_id)
            avg = sum(all_scores) / len(all_scores)
            bar = "█" * int(avg / 5)
            print(f"    {method.name:20s} {avg:5.1f} {bar}")
    
    # 7. Show interesting relationships
    print_section("KEY RELATIONSHIPS")
    
    print("\n  Re²Search++ relationships:")
    rels = store.get_relationships(source_id="method_re2search_plus")
    for rel in rels[:4]:  # Show first 4
        target = store.get_entity(rel.target_id)
        if target and "description" in rel.properties:
            print(f"    • {rel.relation_type.value} → {target.name}")
            print(f"      {rel.properties['description']}")
    
    print("\n  Graphiti relationships:")
    rels = store.get_relationships(source_id="product_graphiti")
    for rel in rels:
        target = store.get_entity(rel.target_id)
        if target and "description" in rel.properties:
            print(f"    • {rel.relation_type.value} → {target.name}")
            print(f"      {rel.properties['description']}")
    
    # 8. Database statistics
    print_section("DATABASE STATISTICS")
    
    entity_counts = {}
    for entity in all_entities:
        entity_type = entity.entity_type.value
        entity_counts[entity_type] = entity_counts.get(entity_type, 0) + 1
    
    print("\n  Entity counts:")
    for entity_type, count in sorted(entity_counts.items()):
        print(f"    • {entity_type}: {count}")
    
    # Count all relationships
    all_rels = []
    for entity in all_entities:
        rels = store.get_relationships(source_id=entity.id)
        all_rels.extend(rels)
    
    print(f"\n  Total relationships: {len(all_rels)}")
    
    # Count benchmark scores
    total_scores = 0
    for benchmark in benchmarks:
        for entity in methods:
            scores = store.get_benchmark_scores(
                benchmark_id=benchmark.id,
                method_id=entity.id
            )
            total_scores += len(scores)
    
    print(f"  Total benchmark scores: {total_scores}")
    
    # 9. Data sources
    print_section("DATA SOURCES")
    
    print("\n  Papers & Documentation:")
    print("    • RAG-Gym paper (arxiv:2502.13957v2)")
    print("      'RAG-Gym: Systematic Optimization of Language Agents for RAG'")
    print("    • Graphiti README (github.com/getzep/graphiti)")
    print("      'Build Real-Time Knowledge Graphs for AI Agents'")
    print("    • Zep paper (arxiv:2501.13956)")
    print("      'Zep: A Temporal Knowledge Graph Architecture for Agent Memory'")
    
    print_section("SYSTEM READY")
    print("\n  ✅ All data extracted and indexed")
    print("  ✅ Ready for research queries and comparisons")
    print("  ✅ Use ComparisonEngine for detailed analysis")
    print("\n  📁 Data location: data/research/")
    print("  🔧 Scripts: scripts/extract_*.py, scripts/query_*.py")
    print("")

if __name__ == "__main__":
    main()
