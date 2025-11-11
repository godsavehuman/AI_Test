"""
Extractors for parsing research papers and repositories.

These extract entities, features, benchmarks, and relationships
from various sources (papers, repos, etc.).
"""

from typing import Dict, Any, List, Optional, Tuple
import re
import json
import sys
from pathlib import Path
from abc import ABC, abstractmethod

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from research.entities import (
    Entity, EntityRelationship, EntityType, 
    RelationType, BenchmarkScore
)


class BaseExtractor(ABC):
    """Base class for all extractors."""
    
    @abstractmethod
    def extract(self, source: Any) -> Dict[str, Any]:
        """
        Extract information from a source.
        
        Returns:
            Dictionary with:
                - entities: List[Entity]
                - relationships: List[EntityRelationship]
                - benchmarks: List[BenchmarkScore]
        """
        pass


class PaperExtractor(BaseExtractor):
    """
    Extract information from research papers.
    
    Supports markdown and HTML formats from arxiv downloads.
    """
    
    def __init__(self):
        # Common benchmark patterns
        self.benchmark_patterns = [
            r'(\w+)\s+dataset',
            r'evaluated on\s+(\w+)',
            r'benchmark[s]?:\s*(\w+)',
        ]
        
        # Score patterns (e.g., "accuracy: 95.3%", "F1: 0.923")
        self.score_patterns = [
            r'(\w+):\s*([\d.]+)%?',
            r'(\w+)\s+score:\s*([\d.]+)',
            r'achieve[s]?\s+(\w+)\s+of\s+([\d.]+)',
        ]
    
    def extract(self, paper_path: str) -> Dict[str, Any]:
        """
        Extract entities from a paper file.
        
        Args:
            paper_path: Path to paper markdown or HTML file
            
        Returns:
            Dictionary with entities, relationships, and benchmarks
        """
        paper_path = Path(paper_path)
        
        # Read content
        with open(paper_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract paper ID from filename
        paper_id = paper_path.stem
        
        # Create paper entity
        paper_entity = Entity(
            id=f"paper_{paper_id}",
            name=self._extract_title(content) or paper_id,
            entity_type=EntityType.PAPER,
            metadata={
                "file_path": str(paper_path),
                "arxiv_id": paper_id if paper_id.replace('.', '').replace('v', '').isdigit() else None
            }
        )
        
        # Extract methods mentioned
        methods = self._extract_methods(content)
        method_entities = []
        relationships = []
        
        for method_name in methods:
            method_id = f"method_{method_name.lower().replace(' ', '_')}"
            method_entity = Entity(
                id=method_id,
                name=method_name,
                entity_type=EntityType.METHOD,
                features=self._extract_method_features(content, method_name),
                metadata={"source_paper": paper_entity.id}
            )
            method_entities.append(method_entity)
            
            # Create relationship
            relationships.append(EntityRelationship(
                source_id=paper_entity.id,
                target_id=method_id,
                relation_type=RelationType.IMPLEMENTS
            ))
        
        # Extract benchmarks
        benchmarks = self._extract_benchmarks(content)
        benchmark_entities = []
        benchmark_scores = []
        
        for bench_name, scores_dict in benchmarks.items():
            bench_id = f"benchmark_{bench_name.lower().replace(' ', '_')}"
            bench_entity = Entity(
                id=bench_id,
                name=bench_name,
                entity_type=EntityType.BENCHMARK,
                metadata={"source_paper": paper_entity.id}
            )
            benchmark_entities.append(bench_entity)
            
            # Create benchmark scores for methods
            for method in method_entities:
                for metric_name, score in scores_dict.items():
                    benchmark_scores.append(BenchmarkScore(
                        method_id=method.id,
                        benchmark_id=bench_id,
                        metric_name=metric_name,
                        score=score,
                        metadata={"source_paper": paper_entity.id}
                    ))
                    
                    # Create relationship
                    relationships.append(EntityRelationship(
                        source_id=method.id,
                        target_id=bench_id,
                        relation_type=RelationType.EVALUATED_ON
                    ))
        
        return {
            "entities": [paper_entity] + method_entities + benchmark_entities,
            "relationships": relationships,
            "benchmarks": benchmark_scores
        }
    
    def _extract_title(self, content: str) -> Optional[str]:
        """Extract paper title from content."""
        # Try markdown heading
        match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if match:
            return match.group(1).strip()
        
        # Try HTML title
        match = re.search(r'<h1[^>]*>(.+?)</h1>', content, re.IGNORECASE)
        if match:
            return re.sub(r'<[^>]+>', '', match.group(1)).strip()
        
        return None
    
    def _extract_methods(self, content: str) -> List[str]:
        """Extract method names from content."""
        methods = set()
        
        # Look for common method indicators
        patterns = [
            r'our (?:method|approach|model|system)[\s:,]+(\w+)',
            r'we propose\s+(\w+)',
            r'(\w+)\s+(?:method|approach|model|algorithm)',
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                method_name = match.group(1)
                if len(method_name) > 2:  # Filter out short matches
                    methods.add(method_name)
        
        return list(methods)
    
    def _extract_method_features(self, content: str, method_name: str) -> Dict[str, Any]:
        """Extract features of a method from content."""
        features = {}
        
        # Look for descriptions near the method name
        context_pattern = rf'{re.escape(method_name)}[^.]*?([^.]+\.|.{{1,200}})'
        matches = re.findall(context_pattern, content, re.IGNORECASE)
        
        if matches:
            features["description"] = matches[0][:200]  # First description, truncated
        
        return features
    
    def _extract_benchmarks(self, content: str) -> Dict[str, Dict[str, float]]:
        """
        Extract benchmark names and scores.
        
        Returns:
            Dict mapping benchmark names to {metric: score} dicts
        """
        benchmarks = {}
        
        # Find benchmark mentions
        for pattern in self.benchmark_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                bench_name = match.group(1)
                
                # Look for scores near this benchmark
                # Search in a window around the match
                start = max(0, match.start() - 500)
                end = min(len(content), match.end() + 500)
                context = content[start:end]
                
                scores = {}
                for score_pattern in self.score_patterns:
                    score_matches = re.finditer(score_pattern, context, re.IGNORECASE)
                    for score_match in score_matches:
                        metric = score_match.group(1)
                        value = float(score_match.group(2))
                        scores[metric] = value
                
                if scores:
                    benchmarks[bench_name] = scores
        
        return benchmarks


class RepoExtractor(BaseExtractor):
    """
    Extract information from GitHub repositories.
    
    Parses README, requirements, and code structure.
    """
    
    def extract(self, repo_path: str) -> Dict[str, Any]:
        """
        Extract entities from a repository.
        
        Args:
            repo_path: Path to cloned repository
            
        Returns:
            Dictionary with entities, relationships, and benchmarks
        """
        repo_path = Path(repo_path)
        repo_name = repo_path.name
        
        # Create repo entity
        repo_entity = Entity(
            id=f"repo_{repo_name.lower().replace('-', '_')}",
            name=repo_name,
            entity_type=EntityType.REPOSITORY,
            metadata={"path": str(repo_path)}
        )
        
        # Parse README if exists
        readme_path = self._find_readme(repo_path)
        if readme_path:
            with open(readme_path, 'r', encoding='utf-8') as f:
                readme_content = f.read()
                repo_entity.add_feature("description", self._extract_description(readme_content))
        
        # Extract methods implemented
        methods = self._extract_methods_from_repo(repo_path)
        method_entities = []
        relationships = []
        
        for method_name, method_info in methods.items():
            method_id = f"method_{method_name.lower().replace(' ', '_')}"
            method_entity = Entity(
                id=method_id,
                name=method_name,
                entity_type=EntityType.METHOD,
                features=method_info,
                metadata={"source_repo": repo_entity.id}
            )
            method_entities.append(method_entity)
            
            relationships.append(EntityRelationship(
                source_id=repo_entity.id,
                target_id=method_id,
                relation_type=RelationType.IMPLEMENTS
            ))
        
        return {
            "entities": [repo_entity] + method_entities,
            "relationships": relationships,
            "benchmarks": []
        }
    
    def _find_readme(self, repo_path: Path) -> Optional[Path]:
        """Find README file in repository."""
        for pattern in ['README.md', 'README.rst', 'README.txt', 'README']:
            readme = repo_path / pattern
            if readme.exists():
                return readme
        return None
    
    def _extract_description(self, readme_content: str) -> str:
        """Extract description from README."""
        # Get first paragraph
        lines = readme_content.split('\n')
        desc_lines = []
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                desc_lines.append(line)
                if len(' '.join(desc_lines)) > 200:
                    break
        
        return ' '.join(desc_lines)[:500]
    
    def _extract_methods_from_repo(self, repo_path: Path) -> Dict[str, Dict[str, Any]]:
        """Extract methods from repository structure."""
        methods = {}
        
        # Look for model/method files
        for py_file in repo_path.rglob('*.py'):
            if 'model' in py_file.stem.lower() or 'method' in py_file.stem.lower():
                method_name = py_file.stem.replace('_', ' ').title()
                methods[method_name] = {
                    "file": str(py_file.relative_to(repo_path))
                }
        
        return methods
