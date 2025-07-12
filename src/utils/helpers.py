"""
Common utility functions for Github Trending History.
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Any

def ensure_directory(path: str) -> None:
    """
    Ensure a directory exists, create if it doesn't.
    
    Args:
        path: Directory path to ensure exists
    """
    os.makedirs(path, exist_ok=True)

def load_json_file(filepath: str) -> Dict[str, Any]:
    """
    Load JSON data from file.
    
    Args:
        filepath: Path to JSON file
        
    Returns:
        Dictionary containing JSON data
        
    Raises:
        FileNotFoundError: If file doesn't exist
        json.JSONDecodeError: If file contains invalid JSON
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json_file(filepath: str, data: Dict[str, Any]) -> None:
    """
    Save data to JSON file.
    
    Args:
        filepath: Path to save JSON file
        data: Data to save
    """
    ensure_directory(os.path.dirname(filepath))
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_date_string(date_obj: datetime = None) -> str:
    """
    Get formatted date string.
    
    Args:
        date_obj: Date object, defaults to current date
        
    Returns:
        Formatted date string (YYYY-MM-DD)
    """
    if date_obj is None:
        date_obj = datetime.now()
    return date_obj.strftime('%Y-%m-%d')

def parse_date_string(date_str: str) -> datetime:
    """
    Parse date string to datetime object.
    
    Args:
        date_str: Date string in YYYY-MM-DD format
        
    Returns:
        Datetime object
    """
    return datetime.strptime(date_str, '%Y-%m-%d')

def get_file_size_mb(filepath: str) -> float:
    """
    Get file size in megabytes.
    
    Args:
        filepath: Path to file
        
    Returns:
        File size in MB
    """
    if not os.path.exists(filepath):
        return 0.0
    return os.path.getsize(filepath) / (1024 * 1024)

def format_number(num: int) -> str:
    """
    Format large numbers with K, M suffixes.
    
    Args:
        num: Number to format
        
    Returns:
        Formatted string
    """
    if num >= 1000000:
        return f"{num/1000000:.1f}M"
    elif num >= 1000:
        return f"{num/1000:.1f}K"
    else:
        return str(num) 