# Research Comparison System - Quick Start Guide

## Overview

The Research Comparison System helps you find the best solutions for your research questions by:
- Extracting information from arXiv papers and GitHub repos
- Creating structured entities (methods, benchmarks, features)
- Comparing methods across benchmarks
- Finding state-of-the-art (SOTA) solutions

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Quick Start

### Option 1: Run the Demo

See the system in action with pre-populated RAG method data:

```bash
python src/research/demo.py
```

This will:
- Create sample RAG methods (DPR, ColBERT, ANCE, SPLADE, RAG, RETRO)
- Add benchmark scores on BEIR
- Show various comparison capabilities
- Generate a report

### Option 2: Use the CLI

#### Find State-of-the-Art Methods

```bash
# Find SOTA RAG methods
python src/research/research_cli.py sota --domain "RAG" --benchmark "benchmark_beir" --metric "NDCG@10"
```

#### Research Papers from arXiv

```bash
# Download and analyze papers
python src/research/research_cli.py research --papers 2507.03254v1 2510.04607
```

#### Compare Specific Methods

```bash
# Compare methods by name
python src/research/research_cli.py compare --methods "DPR" "ColBERT" "ANCE"
```

#### List Stored Entities

```bash
# List all methods
python src/research/research_cli.py list --type method

# List all entities
python src/research/research_cli.py list --type all
```

### Option 3: Python API

```python
from research import ResearchPipeline

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
report = pipeline.generate_report(result)
print(report)
```

## Common Use Cases

### Use Case 1: "What's the best RAG method?"

```bash
# First, research relevant papers
python src/research/research_cli.py research --papers 2312.10997

# Then find SOTA
python src/research/research_cli.py sota --domain "RAG" --benchmark "benchmark_beir" --metric "NDCG@10" --output rag_sota.md
```

### Use Case 2: Compare Methods from Different Papers

```python
from research import ResearchPipeline

pipeline = ResearchPipeline()

# Research multiple papers
pipeline.research_from_arxiv([
    "paper_id_1",
    "paper_id_2",
    "paper_id_3"
])

# Compare extracted methods
result = pipeline.find_sota("your domain")
report = pipeline.generate_report(result)
print(report)
```

### Use Case 3: Manually Add Your Own Methods

```python
from research.entities import Entity, EntityType, BenchmarkScore
from research.entity_store import EntityStore

store = EntityStore()

# Add a method
method = Entity(
    id="method_my_method",
    name="My Novel Method",
    entity_type=EntityType.METHOD,
    features={
        "architecture": "Transformer-based",
        "year": 2024,
        "description": "My innovative approach"
    }
)
store.save_entity(method)

# Add benchmark score
score = BenchmarkScore(
    method_id="method_my_method",
    benchmark_id="benchmark_beir",
    metric_name="NDCG@10",
    score=0.650
)
store.save_benchmark_score(score)
```

## Output Format

### Rankings Table

```markdown
| Rank | Method | Score | Metric |
|------|--------|-------|--------|
| 1    | RETRO  | 0.5730| NDCG@10|
| 2    | ANCE   | 0.5470| NDCG@10|
```

### Feature Comparison

```markdown
| Method | Architecture | Year | Open Source |
|--------|--------------|------|-------------|
| DPR    | Dual encoder | 2020 | True        |
| ColBERT| Late inter.  | 2020 | True        |
```

## Data Storage

All data is stored in `data/research/`:
- `entities/` - Methods, papers, benchmarks
- `relationships/` - Entity relationships
- `benchmarks/` - Benchmark scores

Files are JSON format and human-readable.

## Examples

See `src/research/examples.py` for comprehensive examples:

```bash
python src/research/examples.py
```

Examples include:
1. Basic research from papers
2. Finding SOTA methods
3. Comparing methods
4. Querying entities
5. Manual entity creation

## Troubleshooting

### No entities found

Make sure you've either:
1. Run the demo to create sample data
2. Researched papers using the CLI
3. Manually created entities

### Import errors

Make sure you're running from the project root:

```bash
cd AI_Test
python src/research/demo.py
```

### ArXiv download fails

Some papers may not have HTML versions. The system will show an error but continue processing other papers.

## Next Steps

1. **Try the demo**: `python src/research/demo.py`
2. **Research your domain**: Add papers relevant to your research question
3. **Find SOTA**: Use the comparison engine to find best methods
4. **Generate reports**: Create markdown reports for your findings

## Documentation

- Full documentation: `src/research/README.md`
- Examples: `src/research/examples.py`
- Tests: `tests/test_research.py`

## Support

For issues or questions, see the README.md in the research folder.
