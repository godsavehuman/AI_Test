# Research Comparison System

A comprehensive system for comparing research methods, tools, and approaches across papers and repositories. The system extracts entities, features, and benchmarks to enable structured comparisons and find state-of-the-art solutions.

## Features

- **Entity Management**: Create and manage entities (methods, papers, repos, benchmarks)
- **Relationship Tracking**: Track relationships between entities (implements, uses, evaluated_on, etc.)
- **Feature Extraction**: Automatically extract features and benchmarks from papers
- **Comparison Engine**: Compare and rank entities based on scores and features
- **SOTA Discovery**: Find state-of-the-art methods for specific domains
- **Reporting**: Generate formatted comparison reports

## Architecture

```
research/
├── __init__.py              # Package initialization
├── entities.py              # Entity, Relationship, and BenchmarkScore classes
├── entity_store.py          # Storage layer using LocalFileDB
├── extractors.py            # PaperExtractor and RepoExtractor
├── comparison_engine.py     # ComparisonEngine for ranking and analysis
├── research_pipeline.py     # End-to-end pipeline orchestration
├── research_cli.py          # Command-line interface
├── examples.py              # Usage examples
└── README.md               # This file
```

## Entity Types

- **METHOD**: Research methods, algorithms, models
- **PAPER**: Research papers
- **REPOSITORY**: Code repositories
- **BENCHMARK**: Evaluation benchmarks/datasets
- **DATASET**: Training datasets
- **FEATURE**: Specific features or capabilities
- **METRIC**: Evaluation metrics

## Relationship Types

- **IMPLEMENTS**: Paper/repo implements a method
- **USES**: Entity uses another entity
- **IMPROVES_UPON**: Method improves upon another
- **EVALUATED_ON**: Method evaluated on benchmark
- **PART_OF**: Entity is part of another
- **COMPARED_WITH**: Entities compared
- **BASED_ON**: Entity based on another

## Installation

No additional dependencies required beyond the base project requirements.

## Usage

### Command-Line Interface

```bash
# Research papers from arXiv
python src/research/research_cli.py research --papers 2507.03254v1 2510.04607 --query "RAG methods"

# Find state-of-the-art methods
python src/research/research_cli.py sota --domain "RAG" --benchmark "BEIR" --metric "NDCG@10"

# Compare specific methods
python src/research/research_cli.py compare --methods "Method1" "Method2" "Method3"

# List stored entities
python src/research/research_cli.py list --type method
```

### Python API

```python
from research import ResearchPipeline

# Initialize pipeline
pipeline = ResearchPipeline()

# Research from arXiv papers
result = pipeline.research_from_arxiv(["2507.03254v1", "2510.04607"])

# Find state-of-the-art RAG methods
sota_result = pipeline.find_sota(
    domain="RAG",
    benchmark_id="benchmark_beir",
    metric_name="NDCG@10"
)

# Generate report
report = pipeline.generate_report(sota_result, output_file="rag_sota.md")
print(report)
```

### Quick Research

```python
from research.research_pipeline import quick_research

# One-line research and report
report = quick_research(
    query="RAG methods",
    paper_ids=["2507.03254v1"],
    benchmark_id="benchmark_beir",
    metric_name="NDCG@10"
)
print(report)
```

## Examples

See `examples.py` for comprehensive usage examples:

1. **Basic Research**: Extract entities from arXiv papers
2. **Find SOTA**: Find state-of-the-art methods for a domain
3. **Compare Methods**: Compare specific methods by features
4. **Query Entities**: Search and list stored entities
5. **Quick Research**: One-line research and reporting
6. **Manual Creation**: Programmatically create entities

Run examples:
```bash
python src/research/examples.py
```

## Use Case: Finding SOTA RAG Methods

```python
from research import ResearchPipeline

pipeline = ResearchPipeline()

# 1. Research relevant papers
pipeline.research_from_arxiv([
    "2312.10997",  # Example: RAG paper
    "2401.00000",  # Example: Another RAG paper
])

# 2. Find state-of-the-art
result = pipeline.find_sota(
    domain="RAG",
    benchmark_id="benchmark_beir",
    metric_name="NDCG@10"
)

# 3. Generate report
report = pipeline.generate_report(result)
```

This will output:
- Ranked list of methods with scores
- Feature comparison matrix
- Summary of top performers

## Data Storage

All data is stored in `data/research/`:
- `entities/`: Entity JSON files
- `relationships/`: Relationship JSON files
- `benchmarks/`: Benchmark score JSON files

Data is persisted using the `LocalFileDB` for easy inspection and portability.

## Extending the System

### Custom Extractors

Create custom extractors for different sources:

```python
from research.extractors import BaseExtractor

class CustomExtractor(BaseExtractor):
    def extract(self, source):
        # Your extraction logic
        return {
            "entities": [...],
            "relationships": [...],
            "benchmarks": [...]
        }
```

### Custom Comparison Strategies

Extend the comparison engine:

```python
from research.comparison_engine import ComparisonEngine

class CustomEngine(ComparisonEngine):
    def custom_ranking(self, entities, criteria):
        # Your ranking logic
        pass
```

## Integration with Existing Tools

The system integrates with existing tools in the project:

- **download_arxiv.py**: Download papers from arXiv
- **html_to_markdown.py**: Convert HTML to markdown
- **local_db.py**: Persistent storage
- **workflow.py**: Can be integrated into workflows

## Future Enhancements

- [ ] LLM-powered entity extraction
- [ ] Automatic benchmark detection
- [ ] Graph visualization of relationships
- [ ] Real-time paper monitoring
- [ ] GitHub integration for code analysis
- [ ] Interactive comparison UI
- [ ] Export to different formats (CSV, JSON, etc.)

## License

Part of the AI_Test project.




next step
extract name description, key features and comparision information from text 