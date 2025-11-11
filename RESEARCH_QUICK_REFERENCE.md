# Research Comparison System - Quick Reference

## 🚀 Quick Start

```bash
# 1. Run the demo
$env:PYTHONPATH="c:\Users\yan\repos\AI_Test\src"
python src/research/demo.py

# 2. Find SOTA methods (using demo data)
python src/research/research_cli.py sota --domain "RAG"
```

## 📋 Common Commands

### CLI Usage

```bash
# Research papers from arXiv
python src/research/research_cli.py research --papers 2507.03254v1 2510.04607

# Find state-of-the-art
python src/research/research_cli.py sota --domain "RAG" --benchmark "benchmark_beir" --metric "NDCG@10"

# Compare specific methods
python src/research/research_cli.py compare --methods "DPR" "ColBERT" "ANCE"

# List stored entities
python src/research/research_cli.py list --type method
python src/research/research_cli.py list --type paper
python src/research/research_cli.py list --type all
```

### Python API

```python
from research.research_pipeline import ResearchPipeline

# Initialize
pipeline = ResearchPipeline()

# Research papers
pipeline.research_from_arxiv(["2507.03254v1", "2510.04607"])

# Find SOTA
result = pipeline.find_sota(
    domain="RAG",
    benchmark_id="benchmark_beir",
    metric_name="NDCG@10"
)

# Generate report
report = pipeline.generate_report(result, output_file="report.md")
print(report)
```

### One-Line Quick Research

```python
from research.research_pipeline import quick_research

report = quick_research(query="RAG methods", paper_ids=["2312.10997"])
print(report)
```

## 🏗️ Manual Entity Creation

```python
from research.entities import Entity, EntityType, BenchmarkScore
from research.entity_store import EntityStore

store = EntityStore()

# Create method
method = Entity(
    id="method_my_rag",
    name="My RAG System",
    entity_type=EntityType.METHOD,
    features={"architecture": "Dense retrieval", "year": 2024}
)
store.save_entity(method)

# Add benchmark score
score = BenchmarkScore(
    method_id="method_my_rag",
    benchmark_id="benchmark_beir",
    metric_name="NDCG@10",
    score=0.650
)
store.save_benchmark_score(score)
```

## 📊 Query and Search

```python
from research.entity_store import EntityStore
from research.entities import EntityType

store = EntityStore()

# List all methods
methods = store.list_entities(EntityType.METHOD)

# Search by name
results = store.search_entities("RAG", EntityType.METHOD)

# Get top performers
top = store.get_top_performers(
    benchmark_id="benchmark_beir",
    metric_name="NDCG@10",
    limit=5
)
```

## 📁 File Structure

```
src/research/
├── entities.py              # Data models
├── entity_store.py          # Storage layer
├── extractors.py            # Paper/repo extraction
├── comparison_engine.py     # Ranking & comparison
├── research_pipeline.py     # End-to-end pipeline
├── research_cli.py          # CLI interface
├── demo.py                  # Interactive demo
├── examples.py              # Usage examples
└── README.md               # Full documentation

data/research/
├── entities/                # Stored entities
├── relationships/           # Stored relationships
└── benchmarks/              # Stored scores
```

## 🎯 Entity Types

- `METHOD` - Research methods/algorithms
- `PAPER` - Research papers
- `REPOSITORY` - Code repositories
- `BENCHMARK` - Evaluation benchmarks
- `DATASET` - Training datasets
- `FEATURE` - Specific features
- `METRIC` - Evaluation metrics

## 🔗 Relationship Types

- `IMPLEMENTS` - Paper/repo implements method
- `EVALUATED_ON` - Method evaluated on benchmark
- `USES` - Entity uses another
- `IMPROVES_UPON` - Method improves upon another
- `BASED_ON` - Entity based on another
- `PART_OF` - Entity is part of another
- `COMPARED_WITH` - Entities compared

## 📈 Comparison Strategies

```python
from research.comparison_engine import ComparisonEngine
from research.entity_store import EntityStore

store = EntityStore()
engine = ComparisonEngine(store)

# Compare on benchmark
result = engine.compare_methods_on_benchmark(
    benchmark_id="benchmark_beir",
    metric_name="NDCG@10"
)

# Compare by features
result = engine.compare_entities_by_features(
    entity_ids=["method1", "method2"]
)

# Find best solution
result = engine.find_best_solution(
    query="RAG",
    benchmark_id="benchmark_beir",
    metric_name="NDCG@10"
)
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/test_research.py -v

# Run specific test
pytest tests/test_research.py::TestEntityStore -v
```

## 📚 Documentation

- **Full Docs**: `src/research/README.md`
- **Quick Start**: `QUICKSTART_RESEARCH.md`
- **Summary**: `RESEARCH_IMPLEMENTATION_SUMMARY.md`
- **This Card**: `RESEARCH_QUICK_REFERENCE.md`

## 💡 Tips

1. **Run demo first** to understand capabilities
2. **Use CLI** for quick tasks
3. **Use Python API** for complex workflows
4. **Check `examples.py`** for code patterns
5. **Data persists** in `data/research/`
6. **JSON files** are human-readable and editable

## 🐛 Troubleshooting

**Import errors?**
```bash
$env:PYTHONPATH="c:\Users\yan\repos\AI_Test\src"
```

**No entities found?**
- Run `demo.py` to create sample data
- Or research papers with CLI
- Or manually create entities

**ArXiv download fails?**
- Some papers may not have HTML versions
- System will continue with other papers

## 🎓 Example Workflow

```python
# 1. Setup
from research.research_pipeline import ResearchPipeline
pipeline = ResearchPipeline()

# 2. Research papers
pipeline.research_from_arxiv(["paper1", "paper2", "paper3"])

# 3. Find SOTA
result = pipeline.find_sota("your domain")

# 4. Generate report
report = pipeline.generate_report(result, "report.md")

# 5. Done!
```

## 🔥 Demo Output Sample

```
Top 5 RAG Methods on BEIR (NDCG@10):

1. RETRO       Score: 0.5730
2. ANCE        Score: 0.5470
3. DPR         Score: 0.5300
4. ColBERT     Score: 0.5210
5. SPLADE      Score: 0.4980
```

---

**Ready to find the best research solutions!** 🚀
