"""
Extract information from RAG-Gym paper and save to entity store
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from research.entities import Entity, EntityType, EntityRelationship, RelationType, BenchmarkScore
from research.entity_store import EntityStore

def main():
    # Initialize entity store
    store = EntityStore()
    
    # Create RAG-Gym Framework entity
    rag_gym = Entity(
        id="method_rag_gym",
        name="RAG-Gym",
        entity_type=EntityType.METHOD,
        features={
            "description": "Systematic optimization framework for language agents in retrieval-augmented generation with three key optimization dimensions",
            "optimization_dimensions": [
                "Prompt Engineering - 6 functional components including reasoning reflection",
                "Actor Tuning - Direct Preference Optimization (DPO) with process-level supervision",
                "Critic Training - Process reward model for evaluating intermediate steps"
            ],
            "formulation": "Markov Decision Process (MDP) for knowledge-intensive QA",
            "supervision_type": "Fine-grained process-level supervision",
            "key_innovation": "Modular design enabling systematic optimization across three components",
            "source": "https://arxiv.org/html/2502.13957v2",
            "paper_id": "2502.13957v2"
        }
    )
    store.save_entity(rag_gym)
    print(f"✅ Saved entity: {rag_gym.name}")
    
    # Create Re²Search agent entity
    re2search = Entity(
        id="method_re2search",
        name="Re²Search",
        entity_type=EntityType.METHOD,
        features={
            "description": "Novel agentic RAG agent design with reasoning reflection capability",
            "agent_type": "Agentic RAG",
            "key_feature": "Reasoning Reflection - enables the agent to reflect on its reasoning process",
            "functional_components": [
                "Thought generation",
                "Search query generation",
                "Document retrieval",
                "Evidence extraction",
                "Reasoning",
                "Reflection (novel)"
            ],
            "optimization_method": "Prompt engineering within RAG-Gym framework",
            "comparison_baselines": ["Direct", "CoT", "RAG", "ReAct", "Search-o1"],
            "source": "https://arxiv.org/html/2502.13957v2",
            "paper_id": "2502.13957v2"
        }
    )
    store.save_entity(re2search)
    print(f"✅ Saved entity: {re2search.name}")
    
    # Create Re²Search++ entity (optimized version)
    re2search_plus = Entity(
        id="method_re2search_plus",
        name="Re²Search++",
        entity_type=EntityType.METHOD,
        features={
            "description": "Optimized version of Re²Search using all three RAG-Gym optimization dimensions (prompt engineering, actor tuning, critic training)",
            "agent_type": "Agentic RAG (Fully Optimized)",
            "optimization_components": [
                "Prompt Engineering (Re²Search design)",
                "Actor Tuning (DPO with process rewards)",
                "Critic Training (Process reward model)"
            ],
            "performance_improvement": "3.2%-11.6% average F1 improvement over baselines",
            "unseen_data_improvement": "8.5%-19.4% F1 improvement on unseen datasets",
            "comparison_target": "Search-R1 and other recent methods",
            "source": "https://arxiv.org/html/2502.13957v2",
            "paper_id": "2502.13957v2"
        }
    )
    store.save_entity(re2search_plus)
    print(f"✅ Saved entity: {re2search_plus.name}")
    
    # Create benchmark entities
    benchmarks = [
        ("benchmark_hotpotqa", "HotpotQA", "Multi-hop QA dataset from Wikipedia"),
        ("benchmark_2wikimultihopqa", "2WikiMultihopQA", "Multi-hop QA dataset from Wikipedia"),
        ("benchmark_bamboogle", "Bamboogle", "Multi-hop QA dataset from Wikipedia"),
        ("benchmark_medqa", "MedQA", "Medical exam questions requiring domain knowledge")
    ]
    
    for bench_id, bench_name, bench_desc in benchmarks:
        benchmark = Entity(
            id=bench_id,
            name=bench_name,
            entity_type=EntityType.BENCHMARK,
            features={
                "description": bench_desc,
                "domain": "Medical" if "Med" in bench_name else "General",
                "task_type": "Multiple Choice QA" if "Med" in bench_name else "Multi-hop QA",
                "metrics": ["Accuracy"] if "Med" in bench_name else ["Exact Match (EM)", "F1 Score"]
            }
        )
        store.save_entity(benchmark)
        print(f"✅ Saved benchmark: {benchmark.name}")
    
    # Save benchmark scores for Re²Search (zero-shot learning)
    re2search_scores = [
        ("benchmark_hotpotqa", 34.00, 44.91, "EM", "F1"),
        ("benchmark_2wikimultihopqa", 41.50, 49.06, "EM", "F1"),
        ("benchmark_bamboogle", 44.80, 55.33, "EM", "F1"),
        ("benchmark_medqa", 70.31, 70.31, "Acc", "Acc"),
    ]
    
    for bench_id, em_score, f1_score, metric1, metric2 in re2search_scores:
        score_em = BenchmarkScore(
            method_id="method_re2search",
            benchmark_id=bench_id,
            metric_name=metric1,
            score=em_score
        )
        store.save_benchmark_score(score_em)
        
        score_f1 = BenchmarkScore(
            method_id="method_re2search",
            benchmark_id=bench_id,
            metric_name=metric2,
            score=f1_score
        )
        store.save_benchmark_score(score_f1)
    
    print(f"✅ Saved Re²Search benchmark scores")
    
    # Save benchmark scores for Re²Search++ (with SFT)
    re2search_plus_scores = [
        ("benchmark_hotpotqa", 37.60, 49.16, "EM", "F1"),
        ("benchmark_2wikimultihopqa", 44.00, 50.54, "EM", "F1"),
        ("benchmark_bamboogle", 44.80, 56.78, "EM", "F1"),
        ("benchmark_medqa", 69.52, 69.52, "Acc", "Acc"),
    ]
    
    for bench_id, em_score, f1_score, metric1, metric2 in re2search_plus_scores:
        score_em = BenchmarkScore(
            method_id="method_re2search_plus",
            benchmark_id=bench_id,
            metric_name=metric1,
            score=em_score
        )
        store.save_benchmark_score(score_em)
        
        score_f1 = BenchmarkScore(
            method_id="method_re2search_plus",
            benchmark_id=bench_id,
            metric_name=metric2,
            score=f1_score
        )
        store.save_benchmark_score(score_f1)
    
    print(f"✅ Saved Re²Search++ benchmark scores")
    
    # Create comparison baseline scores (for reference)
    baselines = {
        "ReAct": [
            ("benchmark_hotpotqa", 30.70, 41.09),
            ("benchmark_2wikimultihopqa", 28.90, 35.03),
            ("benchmark_bamboogle", 32.00, 41.35),
            ("benchmark_medqa", 62.37, 62.37),
        ],
        "Search-o1": [
            ("benchmark_hotpotqa", 35.30, 47.33),
            ("benchmark_2wikimultihopqa", 34.00, 41.29),
            ("benchmark_bamboogle", 44.80, 52.50),
            ("benchmark_medqa", 66.14, 66.14),
        ]
    }
    
    for baseline_name, scores in baselines.items():
        baseline_id = f"method_{baseline_name.lower().replace('-', '_')}"
        baseline = Entity(
            id=baseline_id,
            name=baseline_name,
            entity_type=EntityType.METHOD,
            features={
                "description": f"{baseline_name} baseline method for agentic RAG",
                "agent_type": "Agentic RAG baseline"
            }
        )
        store.save_entity(baseline)
        
        for bench_id, em_score, f1_score in scores:
            metric1 = "Acc" if "medqa" in bench_id else "EM"
            metric2 = "Acc" if "medqa" in bench_id else "F1"
            
            score_em = BenchmarkScore(
                method_id=baseline_id,
                benchmark_id=bench_id,
                metric_name=metric1,
                score=em_score
            )
            store.save_benchmark_score(score_em)
            
            score_f1 = BenchmarkScore(
                method_id=baseline_id,
                benchmark_id=bench_id,
                metric_name=metric2,
                score=f1_score
            )
            store.save_benchmark_score(score_f1)
        
        print(f"✅ Saved baseline: {baseline_name}")
    
    # Create relationships
    relationships = [
        ("method_re2search", "method_rag_gym", RelationType.USES, "Re²Search uses RAG-Gym framework for optimization"),
        ("method_re2search_plus", "method_re2search", RelationType.IMPROVES_UPON, "Re²Search++ is the fully optimized version of Re²Search"),
        ("method_re2search_plus", "method_rag_gym", RelationType.USES, "Re²Search++ applies all three RAG-Gym optimization dimensions"),
        ("method_re2search", "method_react", RelationType.IMPROVES_UPON, "Re²Search improves upon ReAct baseline"),
        ("method_re2search", "method_search_o1", RelationType.IMPROVES_UPON, "Re²Search improves upon Search-o1 baseline"),
        ("method_re2search_plus", "method_react", RelationType.IMPROVES_UPON, "Re²Search++ significantly improves upon ReAct"),
        ("method_re2search_plus", "method_search_o1", RelationType.IMPROVES_UPON, "Re²Search++ significantly improves upon Search-o1"),
    ]
    
    for source, target, rel_type, desc in relationships:
        rel = EntityRelationship(
            source_id=source,
            target_id=target,
            relation_type=rel_type,
            properties={"description": desc}
        )
        store.save_relationship(rel)
    
    print(f"✅ Saved {len(relationships)} relationships")
    
    # Create evaluation relationships
    for entity_id in ["method_re2search", "method_re2search_plus", "method_react", "method_search_o1"]:
        for bench_id in ["benchmark_hotpotqa", "benchmark_2wikimultihopqa", "benchmark_bamboogle", "benchmark_medqa"]:
            rel = EntityRelationship(
                source_id=entity_id,
                target_id=bench_id,
                relation_type=RelationType.EVALUATED_ON
            )
            store.save_relationship(rel)
    
    print("✅ Saved evaluation relationships")
    
    print("\n" + "="*80)
    print("EXTRACTION SUMMARY")
    print("="*80)
    print(f"✅ Extracted from paper: RAG-Gym (2502.13957v2)")
    print(f"✅ Methods: RAG-Gym, Re²Search, Re²Search++, ReAct, Search-o1")
    print(f"✅ Benchmarks: HotpotQA, 2WikiMultihopQA, Bamboogle, MedQA")
    print(f"✅ Scores: Multiple EM, F1, and Accuracy metrics")
    print(f"✅ Relationships: USES, IMPROVES_UPON, EVALUATED_ON")
    print(f"\n📁 Data saved to: data/research/")
    print("="*80)
    
    # Show top performers
    print("\n🏆 TOP PERFORMERS:")
    top_f1 = store.get_top_performers("benchmark_hotpotqa", "F1", limit=3)
    for result in top_f1:
        print(f"  - {result['method'].name}: {result['score']:.2f} F1")
    
    print("\n🔍 To query this data:")
    print("  - Use ComparisonEngine to compare methods")
    print("  - Use ResearchPipeline to generate reports")
    print("  - Run: python src/research/research_cli.py compare --benchmark benchmark_hotpotqa --metric F1")

if __name__ == "__main__":
    main()
