"""
Query the extracted RAG-Gym data
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from research.entity_store import EntityStore
from research.comparison_engine import ComparisonEngine

def main():
    store = EntityStore()
    engine = ComparisonEngine(store)
    
    print("="*80)
    print("RAG-GYM DATA QUERY DEMO")
    print("="*80)
    
    # 1. Show all methods
    print("\n📋 ALL METHODS:")
    all_entities = store.list_entities(entity_type="method")
    for method in all_entities:
        print(f"  - {method.name} ({method.id})")
    
    # 2. Show Re²Search++ details
    print("\n🔍 Re²Search++ DETAILS:")
    re2search_plus = store.get_entity("method_re2search_plus")
    if re2search_plus:
        print(f"  Name: {re2search_plus.name}")
        print(f"  Type: {re2search_plus.entity_type.value}")
        print(f"\n  Features:")
        for key, value in re2search_plus.features.items():
            if isinstance(value, list):
                print(f"    - {key}:")
                for item in value:
                    print(f"        • {item}")
            else:
                print(f"    - {key}: {value}")
    
    # 3. Compare methods on HotpotQA
    print("\n🏆 COMPARISON ON HotpotQA (F1 Score):")
    comparison = engine.compare_methods_on_benchmark(
        benchmark_id="benchmark_hotpotqa",
        metric_name="F1",
        limit=5
    )
    
    for ranking in comparison.rankings:
        print(f"  {ranking['rank']}. {ranking['name']}: {ranking['score']:.2f}")
    
    # 4. Show relationships for Re²Search++
    print("\n🔗 Re²Search++ RELATIONSHIPS:")
    relationships = store.get_relationships(source_id="method_re2search_plus")
    for rel in relationships:
        target = store.get_entity(rel.target_id)
        if target:
            print(f"  - {rel.relation_type.value} → {target.name}")
            if "description" in rel.properties:
                print(f"    {rel.properties['description']}")
    
    # 5. Show all benchmark scores for Re²Search++
    print("\n📊 Re²Search++ BENCHMARK SCORES:")
    for bench_id in ["benchmark_hotpotqa", "benchmark_2wikimultihopqa", "benchmark_bamboogle", "benchmark_medqa"]:
        benchmark = store.get_entity(bench_id)
        if benchmark:
            print(f"\n  {benchmark.name}:")
            scores = store.get_benchmark_scores(benchmark_id=bench_id, method_id="method_re2search_plus")
            for score in scores:
                print(f"    - {score.metric_name}: {score.score:.2f}")
    
    # 6. Find best overall method
    print("\n🥇 BEST OVERALL METHOD (Average F1):")
    avg_scores = {}
    for method_id in ["method_re2search_plus", "method_re2search", "method_react", "method_search_o1"]:
        f1_scores = []
        for bench_id in ["benchmark_hotpotqa", "benchmark_2wikimultihopqa", "benchmark_bamboogle"]:
            scores = store.get_benchmark_scores(benchmark_id=bench_id, method_id=method_id, metric_name="F1")
            if scores:
                f1_scores.append(scores[0].score)
        if f1_scores:
            method = store.get_entity(method_id)
            avg_scores[method.name] = sum(f1_scores) / len(f1_scores)
    
    for rank, (name, avg) in enumerate(sorted(avg_scores.items(), key=lambda x: x[1], reverse=True), 1):
        print(f"  {rank}. {name}: {avg:.2f} average F1")
    
    print("\n" + "="*80)

if __name__ == "__main__":
    main()
