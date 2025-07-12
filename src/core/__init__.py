"""
Core functionality for GitHub Trending Assistant.
"""

from .fetcher import fetch_trending_repos
from .analyzer import analyze_and_generate
from .categorizer import categorize_repo, TECH_CATEGORIES

__all__ = ['fetch_trending_repos', 'analyze_and_generate', 'categorize_repo', 'TECH_CATEGORIES'] 