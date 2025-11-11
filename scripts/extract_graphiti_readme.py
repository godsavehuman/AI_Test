"""
Extract information from Graphiti README and save to entity store
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
    
    # Create Graphiti entity
    graphiti = Entity(
        id="product_graphiti",
        name="Graphiti",
        entity_type=EntityType.METHOD,
        features={
            "description": "Framework for building and querying temporally-aware knowledge graphs for AI agents in dynamic environments",
            "product_type": "Knowledge Graph Framework",
            "organization": "Zep (getzep)",
            "release_status": "Open Source",
            "github_url": "https://github.com/getzep/graphiti",
            "arxiv_paper": "2501.13956",
            "paper_title": "Zep: A Temporal Knowledge Graph Architecture for Agent Memory",
            
            # Core Capabilities
            "core_capabilities": [
                "Real-Time Incremental Updates - immediate integration without batch recomputation",
                "Bi-Temporal Data Model - tracks event occurrence and ingestion times",
                "Efficient Hybrid Retrieval - semantic embeddings + keyword (BM25) + graph traversal",
                "Custom Entity Definitions - flexible ontology via Pydantic models",
                "Scalability - parallel processing for enterprise datasets"
            ],
            
            # Key Features
            "key_features": [
                "Temporally-aware knowledge graphs",
                "Continuous integration of user interactions",
                "Incremental data updates",
                "Point-in-time historical queries",
                "State-based reasoning for agents",
                "Task automation capabilities",
                "Semantic search",
                "Keyword search (BM25)",
                "Graph-based search",
                "Dynamic relationship handling",
                "Historical context maintenance"
            ],
            
            # Technical Architecture
            "architecture": {
                "data_model": "Bi-temporal (event time + ingestion time)",
                "retrieval_method": "Hybrid (semantic + keyword + graph)",
                "update_model": "Real-time incremental",
                "query_latency": "Typically sub-second",
                "entity_customization": "Yes, via Pydantic models",
                "scalability": "High with parallel processing"
            },
            
            # Supported Databases
            "supported_databases": [
                "Neo4j 5.26+",
                "FalkorDB 1.1.2+",
                "Kuzu 0.11.2+",
                "Amazon Neptune Database",
                "Amazon Neptune Analytics + OpenSearch Serverless"
            ],
            
            # Supported LLM Providers
            "supported_llm_providers": [
                "OpenAI (default, with Structured Output)",
                "Azure OpenAI",
                "Google Gemini",
                "Anthropic",
                "Groq",
                "Ollama (local models)",
                "OpenAI-compatible APIs"
            ],
            
            # Use Cases
            "use_cases": [
                "AI agent memory systems",
                "Dynamic user interaction tracking",
                "Business data integration",
                "Context-aware AI applications",
                "Interactive knowledge management",
                "Temporal data analysis"
            ],
            
            # Performance Characteristics
            "performance": {
                "query_latency": "Sub-200ms at scale (Zep managed)",
                "update_mode": "Real-time without batch processing",
                "concurrency": "Configurable via SEMAPHORE_LIMIT (default: 10)",
                "scalability": "Enterprise-scale with parallel processing"
            },
            
            # API & Integration
            "apis": [
                "Python SDK",
                "REST API (FastAPI-based server)",
                "MCP Server (Model Context Protocol)",
                "TypeScript SDK (via Zep)",
                "Go SDK (via Zep)"
            ],
            
            # Deployment Options
            "deployment": "Self-hosted only (OSS version)",
            
            # License & Telemetry
            "telemetry": "Opt-out anonymous usage statistics",
            "status": "Under active development",
            
            # Repository Stats
            "github_stars": "Trending on GitHub (TrendShift badge)",
            "badges": ["Lint", "Unit Tests", "MyPy Check", "arXiv paper", "Discord community"]
        }
    )
    store.save_entity(graphiti)
    print(f"✅ Saved entity: {graphiti.name}")
    
    # Create Zep Platform entity (managed version)
    zep = Entity(
        id="product_zep",
        name="Zep",
        entity_type=EntityType.METHOD,
        features={
            "description": "Turn-key context engineering platform for AI Agents with agent memory, Graph RAG, and context retrieval",
            "product_type": "Managed Platform",
            "organization": "Zep (getzep)",
            "website": "https://www.getzep.com",
            "arxiv_paper": "2501.13956",
            "paper_title": "Zep: A Temporal Knowledge Graph Architecture for Agent Memory",
            
            # Core Capabilities
            "core_capabilities": [
                "Agent Memory - State of the Art performance",
                "Graph RAG for dynamic data",
                "Context retrieval and assembly",
                "Built-in user and conversation management",
                "Pre-configured production-ready retrieval"
            ],
            
            # Platform Features
            "platform_features": [
                "Built-in users, threads, and message storage",
                "Sub-200ms retrieval performance at scale",
                "Dashboard with graph visualization",
                "Debug logs and API logs",
                "SDKs for Python, TypeScript, and Go",
                "SLAs and enterprise support",
                "Security guarantees"
            ],
            
            # Performance
            "performance": {
                "retrieval_latency": "Sub-200ms at scale",
                "production_ready": "Yes",
                "scalability": "Enterprise-scale"
            },
            
            # Deployment
            "deployment": ["Fully managed", "Self-hosted in your cloud"],
            
            # Developer Tools
            "developer_tools": [
                "Graph visualization dashboard",
                "Debug logs",
                "API logs",
                "Python SDK",
                "TypeScript SDK", 
                "Go SDK"
            ],
            
            # Enterprise Features
            "enterprise_features": [
                "SLAs",
                "Support",
                "Security guarantees",
                "Fully managed option"
            ]
        }
    )
    store.save_entity(zep)
    print(f"✅ Saved entity: {zep.name}")
    
    # Create GraphRAG entity (comparison baseline)
    graphrag = Entity(
        id="method_graphrag",
        name="GraphRAG",
        entity_type=EntityType.METHOD,
        features={
            "description": "Static document summarization approach using entity clusters and community summaries",
            "product_type": "RAG Framework",
            "primary_use": "Static document summarization",
            "data_handling": "Batch-oriented processing",
            "knowledge_structure": "Entity clusters and community summaries",
            "retrieval_method": "Sequential LLM summarization",
            "adaptability": "Low",
            "temporal_handling": "Basic timestamp tracking",
            "contradiction_handling": "LLM-driven summarization judgments",
            "query_latency": "Seconds to tens of seconds",
            "custom_entity_types": "No",
            "scalability": "Moderate"
        }
    )
    store.save_entity(graphrag)
    print(f"✅ Saved entity: {graphrag.name}")
    
    # Create Traditional RAG entity (comparison baseline)
    traditional_rag = Entity(
        id="method_traditional_rag",
        name="Traditional RAG",
        entity_type=EntityType.METHOD,
        features={
            "description": "Traditional retrieval-augmented generation with batch processing and static summarization",
            "product_type": "RAG Approach",
            "data_handling": "Batch processing",
            "update_model": "Static data summarization",
            "limitations": [
                "Inefficient for frequently changing data",
                "Requires batch recomputation",
                "No temporal tracking",
                "Poor handling of dynamic data"
            ]
        }
    )
    store.save_entity(traditional_rag)
    print(f"✅ Saved entity: {traditional_rag.name}")
    
    # Create comparison scores (qualitative metrics)
    # Using a 0-100 scale for comparison features
    
    comparison_features = {
        "Adaptability": [
            ("product_graphiti", 95.0),  # High
            ("method_graphrag", 20.0),   # Low
            ("method_traditional_rag", 10.0)  # Very Low
        ],
        "Query_Latency": [  # Lower is better, inverted scale
            ("product_graphiti", 95.0),  # Sub-second
            ("method_graphrag", 20.0),   # Seconds to tens of seconds
            ("method_traditional_rag", 30.0)  # Seconds
        ],
        "Scalability": [
            ("product_graphiti", 95.0),  # High
            ("method_graphrag", 60.0),   # Moderate
            ("method_traditional_rag", 50.0)  # Moderate
        ],
        "Real_Time_Updates": [
            ("product_graphiti", 100.0),  # Yes, incremental
            ("method_graphrag", 0.0),     # No, batch only
            ("method_traditional_rag", 0.0)  # No, batch only
        ],
        "Temporal_Tracking": [
            ("product_graphiti", 100.0),  # Bi-temporal explicit tracking
            ("method_graphrag", 30.0),    # Basic timestamps
            ("method_traditional_rag", 0.0)  # None
        ],
        "Custom_Entities": [
            ("product_graphiti", 100.0),  # Yes
            ("method_graphrag", 0.0),     # No
            ("method_traditional_rag", 0.0)  # No
        ]
    }
    
    # Create benchmark entity for feature comparison
    feature_benchmark = Entity(
        id="benchmark_knowledge_graph_features",
        name="Knowledge Graph Feature Comparison",
        entity_type=EntityType.BENCHMARK,
        features={
            "description": "Qualitative comparison of knowledge graph and RAG framework capabilities",
            "metrics": list(comparison_features.keys()),
            "scale": "0-100 (higher is better)",
            "source": "Graphiti README comparison table"
        }
    )
    store.save_entity(feature_benchmark)
    print(f"✅ Saved benchmark: {feature_benchmark.name}")
    
    # Save comparison scores
    for metric_name, scores in comparison_features.items():
        for method_id, score_value in scores:
            score = BenchmarkScore(
                method_id=method_id,
                benchmark_id="benchmark_knowledge_graph_features",
                metric_name=metric_name,
                score=score_value,
                metadata={
                    "scale": "0-100",
                    "source": "Graphiti README",
                    "comparison_type": "qualitative"
                }
            )
            store.save_benchmark_score(score)
    
    print(f"✅ Saved comparison scores for {len(comparison_features)} metrics")
    
    # Create Zep vs Graphiti benchmark
    zep_graphiti_comparison = Entity(
        id="benchmark_zep_vs_graphiti",
        name="Zep vs Graphiti Comparison",
        entity_type=EntityType.BENCHMARK,
        features={
            "description": "Comparison between Zep managed platform and Graphiti OSS framework",
            "aspects": [
                "User & conversation management",
                "Retrieval & performance", 
                "Developer tools",
                "Enterprise features",
                "Deployment options"
            ],
            "source": "Graphiti README Zep vs Graphiti table"
        }
    )
    store.save_entity(zep_graphiti_comparison)
    print(f"✅ Saved benchmark: {zep_graphiti_comparison.name}")
    
    # Create relationships
    relationships = [
        # Graphiti relationships
        ("product_graphiti", "method_graphrag", RelationType.IMPROVES_UPON, 
         "Graphiti addresses GraphRAG limitations with real-time updates and sub-second queries"),
        ("product_graphiti", "method_traditional_rag", RelationType.IMPROVES_UPON,
         "Graphiti provides dynamic data handling vs static batch processing"),
        
        # Zep relationships
        ("product_zep", "product_graphiti", RelationType.USES,
         "Zep is built on Graphiti and powers its core functionality"),
        ("product_zep", "product_graphiti", RelationType.IMPROVES_UPON,
         "Zep adds managed platform features, enterprise support, and pre-configured retrieval"),
        
        # Evaluations
        ("product_graphiti", "benchmark_knowledge_graph_features", RelationType.EVALUATED_ON,
         "Graphiti compared on key knowledge graph capabilities"),
        ("method_graphrag", "benchmark_knowledge_graph_features", RelationType.EVALUATED_ON,
         "GraphRAG compared on key knowledge graph capabilities"),
        ("method_traditional_rag", "benchmark_knowledge_graph_features", RelationType.EVALUATED_ON,
         "Traditional RAG compared on key knowledge graph capabilities"),
        ("product_zep", "benchmark_zep_vs_graphiti", RelationType.EVALUATED_ON,
         "Zep compared with Graphiti OSS"),
        ("product_graphiti", "benchmark_zep_vs_graphiti", RelationType.EVALUATED_ON,
         "Graphiti compared with Zep platform"),
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
    
    print("\n" + "="*80)
    print("EXTRACTION SUMMARY")
    print("="*80)
    print(f"✅ Extracted from: Graphiti README")
    print(f"✅ Products: Graphiti (OSS), Zep (Managed Platform)")
    print(f"✅ Comparison Baselines: GraphRAG, Traditional RAG")
    print(f"✅ Features Extracted:")
    print(f"   - Core capabilities (5 for Graphiti)")
    print(f"   - Key features (11 for Graphiti)")
    print(f"   - Technical architecture details")
    print(f"   - Supported databases (5)")
    print(f"   - Supported LLM providers (7+)")
    print(f"   - Performance characteristics")
    print(f"   - APIs and integration options")
    print(f"✅ Comparisons:")
    print(f"   - Graphiti vs GraphRAG (6 metrics)")
    print(f"   - Graphiti vs Traditional RAG")
    print(f"   - Zep vs Graphiti (platform features)")
    print(f"\n📁 Data saved to: data/research/")
    print("="*80)
    
    # Show comparison results
    print("\n🏆 FEATURE COMPARISON SCORES (0-100 scale):")
    print("\nAdaptability:")
    adaptability = store.get_top_performers("benchmark_knowledge_graph_features", "Adaptability", limit=3)
    for result in adaptability:
        print(f"  - {result['method'].name}: {result['score']:.1f}")
    
    print("\nQuery Latency (higher = faster):")
    latency = store.get_top_performers("benchmark_knowledge_graph_features", "Query_Latency", limit=3)
    for result in latency:
        print(f"  - {result['method'].name}: {result['score']:.1f}")
    
    print("\nReal-Time Updates:")
    realtime = store.get_top_performers("benchmark_knowledge_graph_features", "Real_Time_Updates", limit=3)
    for result in realtime:
        print(f"  - {result['method'].name}: {result['score']:.1f}")
    
    print("\n🔍 To query this data:")
    print("  - Run: python scripts/query_rag_gym_data.py")
    print("  - Use ComparisonEngine to compare Graphiti with other methods")

if __name__ == "__main__":
    main()
