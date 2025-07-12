#!/usr/bin/env python3
"""
Main entry point for Github Trending History.

This script provides a command-line interface to run different operations:
- fetch: Fetch today's trending repositories
- analyze: Analyze data and generate webpage
- full: Run both fetch and analyze operations
"""

import sys
import argparse
from src.core.fetcher import fetch_trending_repos
from src.core.analyzer import analyze_and_generate

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Github Trending History - Track and analyze trending repositories',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py fetch          # Fetch today's trending data
  python main.py analyze        # Generate webpage from existing data
  python main.py full           # Fetch data and generate webpage
        """
    )
    
    parser.add_argument(
        'operation',
        choices=['fetch', 'analyze', 'full'],
        help='Operation to perform'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    try:
        if args.operation == 'fetch':
            print("Fetching trending repositories...")
            repos = fetch_trending_repos()
            if repos:
                print(f"Successfully fetched {len(repos)} repositories")
            else:
                print("No repositories fetched")
                
        elif args.operation == 'analyze':
            print("Analyzing data and generating webpage...")
            analyze_and_generate()
            print("Analysis complete")
            
        elif args.operation == 'full':
            print("Running full pipeline...")
            print("1. Fetching trending repositories...")
            repos = fetch_trending_repos()
            if repos:
                print(f"Successfully fetched {len(repos)} repositories")
                print("2. Analyzing data and generating webpage...")
                analyze_and_generate()
                print("Full pipeline complete")
            else:
                print("Failed to fetch repositories, skipping analysis")
                
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main() 