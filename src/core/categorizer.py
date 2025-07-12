"""
Repository categorization logic for Github Trending History.
"""

# Technology categories and keywords
TECH_CATEGORIES = {
    'AI/ML': ['machine learning', 'ai', 'neural', 'tensorflow', 'pytorch', 'llm', 'gpt', 'chatgpt', 'agent', 'model', 'deep learning', 'nlp', 'computer vision'],
    'Web Development': ['web', 'frontend', 'backend', 'react', 'vue', 'angular', 'node', 'javascript', 'typescript', 'css', 'html', 'api', 'framework'],
    'Mobile': ['mobile', 'ios', 'android', 'flutter', 'react native', 'swift', 'kotlin'],
    'DevOps': ['docker', 'kubernetes', 'ci/cd', 'infrastructure', 'deployment', 'cloud', 'aws', 'azure', 'gcp', 'terraform'],
    'Data Science': ['data', 'analytics', 'pandas', 'numpy', 'scipy', 'jupyter', 'notebook', 'visualization'],
    'System/OS': ['os', 'operating system', 'kernel', 'driver', 'system', 'low-level', 'embedded'],
    'Security': ['security', 'cryptography', 'encryption', 'authentication', 'authorization', 'vulnerability'],
    'Learning': ['tutorial', 'course', 'guide', 'documentation', 'book', 'learning', 'education', 'example']
}

def categorize_repo(repo):
    """
    Categorize repository based on description and language.
    
    Args:
        repo (dict): Repository information containing 'description' and 'language' fields
        
    Returns:
        str: Category name
    """
    description = repo.get('description', '').lower()
    language = repo.get('language', '').lower()
    
    # Check each category
    for category, keywords in TECH_CATEGORIES.items():
        for keyword in keywords:
            if keyword in description or keyword in language:
                return category
    
    # Default category based on language
    language_categories = {
        'python': 'AI/ML',
        'javascript': 'Web Development', 
        'typescript': 'Web Development',
        'go': 'System/OS',
        'rust': 'System/OS',
        'java': 'Web Development',
        'c++': 'System/OS',
        'c': 'System/OS'
    }
    
    return language_categories.get(language, 'Other') 