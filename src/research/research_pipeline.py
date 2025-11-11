"""
Research pipeline for end-to-end research and comparison.

Orchestrates retrieval, extraction, storage, and comparison.
"""

from typing import List, Dict, Any, Optional
from pathlib import Path
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from research.entity_store import EntityStore
from research.comparison_engine import ComparisonEngine
from research.extractors import PaperExtractor, RepoExtractor

# Import tools
try:
    from tools.download_arxiv import download_arxiv_html
except ImportError:
    print("Warning: download_arxiv not available")
    download_arxiv_html = None

# Fallback html_to_markdown function
def html_to_markdown(html_path, md_path):
    """Fallback - just use HTML directly."""
    pass


class ResearchPipeline:
    """
    End-to-end pipeline for research and comparison.
    
    Workflow:
    1. Retrieve papers/repos based on query
    2. Extract entities and relationships
    3. Store in entity store
    4. Compare and rank
    5. Present results
    """
    
    def __init__(self, data_dir: str = None):
        """
        Initialize research pipeline.
        
        Args:
            data_dir: Directory for storing data
        """
        self.store = EntityStore(data_dir)
        self.engine = ComparisonEngine(self.store)
        self.paper_extractor = PaperExtractor()
        self.repo_extractor = RepoExtractor()
    
    def research_from_arxiv(
        self,
        paper_ids: List[str],
        output_dir: str = "./papers"
    ) -> Dict[str, Any]:
        """
        Research from arXiv papers.
        
        Args:
            paper_ids: List of arXiv paper IDs
            output_dir: Directory to download papers to
            
        Returns:
            Dictionary with extraction results
        """
        all_entities = []
        all_relationships = []
        all_benchmarks = []
        
        for paper_id in paper_ids:
            print(f"Processing paper {paper_id}...")
            
            # Download paper
            try:
                download_arxiv_html(paper_id, output_dir)
                html_path = Path(output_dir) / f"{paper_id}.html"
                
                # Convert to markdown if converter available
                md_path = Path(output_dir) / f"{paper_id}.md"
                try:
                    if not md_path.exists() and html_to_markdown:
                        html_to_markdown(str(html_path), str(md_path))
                    if md_path.exists():
                        paper_path = md_path
                    else:
                        paper_path = html_path
                except Exception as e:
                    print(f"Warning: Could not convert to markdown: {e}")
                    paper_path = html_path
                
                # Extract entities
                result = self.paper_extractor.extract(str(paper_path))
                
                # Store entities
                for entity in result["entities"]:
                    self.store.save_entity(entity)
                    all_entities.append(entity)
                
                # Store relationships
                for rel in result["relationships"]:
                    self.store.save_relationship(rel)
                    all_relationships.append(rel)
                
                # Store benchmarks
                for benchmark in result["benchmarks"]:
                    self.store.save_benchmark_score(benchmark)
                    all_benchmarks.append(benchmark)
                
                print(f"✓ Extracted {len(result['entities'])} entities from {paper_id}")
                
            except Exception as e:
                print(f"✗ Error processing {paper_id}: {e}")
                continue
        
        return {
            "entities": all_entities,
            "relationships": all_relationships,
            "benchmarks": all_benchmarks,
            "summary": f"Processed {len(paper_ids)} papers, extracted {len(all_entities)} entities"
        }
    
    def research_from_repo(
        self,
        repo_path: str
    ) -> Dict[str, Any]:
        """
        Research from a GitHub repository.
        
        Args:
            repo_path: Path to cloned repository
            
        Returns:
            Dictionary with extraction results
        """
        print(f"Processing repository {repo_path}...")
        
        result = self.repo_extractor.extract(repo_path)
        
        # Store entities
        for entity in result["entities"]:
            self.store.save_entity(entity)
        
        # Store relationships
        for rel in result["relationships"]:
            self.store.save_relationship(rel)
        
        print(f"✓ Extracted {len(result['entities'])} entities from repository")
        
        return result
    
    def find_sota(
        self,
        domain: str,
        benchmark_id: Optional[str] = None,
        metric_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Find state-of-the-art methods in a domain.
        
        This is the main method for answering "What's the SOTA for X?"
        
        Args:
            domain: Domain or task (e.g., "RAG", "object detection")
            benchmark_id: Optional benchmark to rank by
            metric_name: Optional metric to rank by
            
        Returns:
            Dictionary with comparison results and formatted output
        """
        print(f"Finding SOTA methods for: {domain}")
        
        # Use comparison engine to find best solutions
        result = self.engine.find_best_solution(
            query=domain,
            benchmark_id=benchmark_id,
            metric_name=metric_name
        )
        
        # Format output
        output = {
            "domain": domain,
            "num_methods": len(result.entities),
            "rankings": result.rankings,
            "feature_matrix": result.feature_matrix,
            "summary": result.summary
        }
        
        return output
    
    def compare_methods(
        self,
        method_names: List[str]
    ) -> Dict[str, Any]:
        """
        Compare specific methods by name.
        
        Args:
            method_names: List of method names to compare
            
        Returns:
            Dictionary with comparison results
        """
        # Search for methods
        entities = []
        for name in method_names:
            results = self.store.search_entities(name, entity_type=None)
            if results:
                entities.append(results[0])
        
        if not entities:
            return {
                "error": "No methods found",
                "searched": method_names
            }
        
        entity_ids = [e.id for e in entities]
        result = self.engine.compare_entities_by_features(entity_ids)
        
        return {
            "methods": [e.name for e in entities],
            "comparison": result.feature_matrix,
            "summary": result.summary
        }
    
    def generate_report(
        self,
        result: Dict[str, Any],
        output_file: Optional[str] = None
    ) -> str:
        """
        Generate a formatted report from results.
        
        Args:
            result: Result dictionary from find_sota or compare_methods
            output_file: Optional file to write report to
            
        Returns:
            Formatted report string
        """
        report_lines = []
        
        # Title
        if "domain" in result:
            report_lines.append(f"# State-of-the-Art Report: {result['domain']}\n")
        else:
            report_lines.append("# Method Comparison Report\n")
        
        # Summary
        if "summary" in result:
            report_lines.append("## Summary\n")
            report_lines.append(result["summary"])
            report_lines.append("\n")
        
        # Rankings
        if "rankings" in result and result["rankings"]:
            report_lines.append("## Rankings\n")
            report_lines.append("| Rank | Method | Score | Metric |")
            report_lines.append("|------|--------|-------|--------|")
            
            for r in result["rankings"]:
                score = r.get("score", "N/A")
                metric = r.get("metric", "N/A")
                report_lines.append(
                    f"| {r['rank']} | {r['name']} | {score} | {metric} |"
                )
            
            report_lines.append("\n")
        
        # Feature Matrix
        if "feature_matrix" in result and result["feature_matrix"]:
            report_lines.append("## Feature Comparison\n")
            
            matrix = result["feature_matrix"]
            if "entity_name" in matrix:
                # Build markdown table
                features = [k for k in matrix.keys() if k != "entity_name"]
                if features:
                    # Header
                    header = "| Method | " + " | ".join(features) + " |"
                    separator = "|" + "|".join(["---"] * (len(features) + 1)) + "|"
                    report_lines.append(header)
                    report_lines.append(separator)
                    
                    # Rows
                    for idx, name in enumerate(matrix["entity_name"]):
                        row = f"| {name} |"
                        for feature in features:
                            value = matrix[feature][idx]
                            row += f" {value} |"
                        report_lines.append(row)
                    
                    report_lines.append("\n")
        
        report = "\n".join(report_lines)
        
        # Write to file if specified
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"Report written to {output_file}")
        
        return report


# Convenience function for quick research
def quick_research(
    query: str,
    paper_ids: Optional[List[str]] = None,
    benchmark_id: Optional[str] = None,
    metric_name: Optional[str] = None
) -> str:
    """
    Quick research function for immediate results.
    
    Args:
        query: Research query (e.g., "RAG methods")
        paper_ids: Optional list of arXiv paper IDs to analyze
        benchmark_id: Optional benchmark to rank by
        metric_name: Optional metric to rank by
        
    Returns:
        Formatted report string
    """
    pipeline = ResearchPipeline()
    
    # If paper IDs provided, process them first
    if paper_ids:
        pipeline.research_from_arxiv(paper_ids)
    
    # Find SOTA
    result = pipeline.find_sota(query, benchmark_id, metric_name)
    
    # Generate and return report
    return pipeline.generate_report(result)
