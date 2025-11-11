"""
Command-line interface for the research comparison system.

Usage:
    python research_cli.py research --papers 2507.03254v1 2510.04607 --query "RAG methods"
    python research_cli.py sota --domain "RAG" --benchmark "BEIR" --metric "NDCG@10"
    python research_cli.py compare --methods "Method1" "Method2" "Method3"
    python research_cli.py list --type method
"""

import sys
import argparse
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from research.research_pipeline import ResearchPipeline
from research.entities import EntityType


def main():
    parser = argparse.ArgumentParser(
        description="Research Comparison System CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Research command
    research_parser = subparsers.add_parser('research', help='Research from papers')
    research_parser.add_argument(
        '--papers',
        nargs='+',
        required=True,
        help='ArXiv paper IDs to analyze'
    )
    research_parser.add_argument(
        '--query',
        help='Optional query to filter results'
    )
    research_parser.add_argument(
        '--output',
        help='Output file for report'
    )
    
    # SOTA command
    sota_parser = subparsers.add_parser('sota', help='Find state-of-the-art methods')
    sota_parser.add_argument(
        '--domain',
        required=True,
        help='Domain or task (e.g., "RAG", "object detection")'
    )
    sota_parser.add_argument(
        '--benchmark',
        help='Benchmark to rank by'
    )
    sota_parser.add_argument(
        '--metric',
        help='Metric to rank by'
    )
    sota_parser.add_argument(
        '--output',
        help='Output file for report'
    )
    
    # Compare command
    compare_parser = subparsers.add_parser('compare', help='Compare specific methods')
    compare_parser.add_argument(
        '--methods',
        nargs='+',
        required=True,
        help='Method names to compare'
    )
    compare_parser.add_argument(
        '--output',
        help='Output file for report'
    )
    
    # List command
    list_parser = subparsers.add_parser('list', help='List stored entities')
    list_parser.add_argument(
        '--type',
        choices=['method', 'paper', 'benchmark', 'all'],
        default='all',
        help='Type of entities to list'
    )
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize pipeline
    pipeline = ResearchPipeline()
    
    # Execute command
    if args.command == 'research':
        print(f"Researching papers: {', '.join(args.papers)}")
        result = pipeline.research_from_arxiv(args.papers)
        print(f"\n{result['summary']}")
        
        if args.query:
            print(f"\nFinding SOTA for: {args.query}")
            sota_result = pipeline.find_sota(args.query)
            report = pipeline.generate_report(sota_result, args.output)
            print("\n" + report)
        else:
            print("\nExtraction complete! Use 'sota' command to find best methods.")
    
    elif args.command == 'sota':
        print(f"Finding SOTA methods for: {args.domain}")
        result = pipeline.find_sota(
            args.domain,
            args.benchmark,
            args.metric
        )
        report = pipeline.generate_report(result, args.output)
        print("\n" + report)
    
    elif args.command == 'compare':
        print(f"Comparing methods: {', '.join(args.methods)}")
        result = pipeline.compare_methods(args.methods)
        
        if "error" in result:
            print(f"Error: {result['error']}")
            return
        
        report = pipeline.generate_report(result, args.output)
        print("\n" + report)
    
    elif args.command == 'list':
        entity_type_map = {
            'method': EntityType.METHOD,
            'paper': EntityType.PAPER,
            'benchmark': EntityType.BENCHMARK,
            'all': None
        }
        
        entity_type = entity_type_map[args.type]
        entities = pipeline.store.list_entities(entity_type)
        
        print(f"\nFound {len(entities)} entities:")
        for entity in entities:
            print(f"- [{entity.entity_type.value}] {entity.name} (ID: {entity.id})")


if __name__ == "__main__":
    main()
