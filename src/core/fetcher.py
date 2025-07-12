"""
Data fetching functionality for Github Trending History.
"""

import requests
import json
import os
from datetime import datetime
from bs4 import BeautifulSoup

DATA_DIR = 'data/trending_data'

def fetch_trending_repos():
    """
    Fetch trending repositories from GitHub and save to data directory.
    
    Returns:
        list: List of trending repositories
    """
    url = 'https://github.com/trending'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        repos = []
        
        # Find all repository articles
        repo_articles = soup.find_all('article', class_='Box-row')
        
        for i, article in enumerate(repo_articles, 1):
            try:
                # Extract repository name and owner
                repo_link = article.find('h2', class_='h3 lh-condensed').find('a')
                repo_name = repo_link.get('href').strip('/')
                
                # Extract description
                description_elem = article.find('p', class_='col-9 color-fg-muted my-1 pr-4')
                description = description_elem.get_text(strip=True) if description_elem else ''
                
                # Extract language
                language_elem = article.find('span', {'itemprop': 'programmingLanguage'})
                language = language_elem.get_text(strip=True) if language_elem else ''
                
                # Extract stars
                stars_elem = article.find('a', href=lambda x: x and 'stargazers' in x)
                stars = stars_elem.get_text(strip=True) if stars_elem else '0'
                
                # Extract forks
                forks_elem = article.find('a', href=lambda x: x and 'forks' in x)
                forks = forks_elem.get_text(strip=True) if forks_elem else '0'
                
                repo_data = {
                    'rank': i,
                    'name': repo_name,
                    'description': description,
                    'language': language,
                    'stars': stars,
                    'forks': forks,
                    'link': f'https://github.com/{repo_name}'
                }
                
                repos.append(repo_data)
                
            except Exception as e:
                print(f"Error parsing repository {i}: {e}")
                continue
        
        # Save to file
        save_trending_data(repos)
        
        print(f"Successfully fetched {len(repos)} trending repositories")
        return repos
        
    except Exception as e:
        print(f"Error fetching trending repositories: {e}")
        return []

def save_trending_data(repos):
    """
    Save trending data to organized directory structure.
    
    Args:
        repos (list): List of repository data to save
    """
    today = datetime.now()
    year = str(today.year)
    month = f"{today.month:02d}"
    day = f"{today.day:02d}"
    
    # Create directory structure
    year_dir = os.path.join(DATA_DIR, year)
    month_dir = os.path.join(year_dir, month)
    
    os.makedirs(month_dir, exist_ok=True)
    
    # Save to file
    filename = f"{day}.json"
    filepath = os.path.join(month_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(repos, f, ensure_ascii=False, indent=2)
    
    print(f"Data saved to {filepath}")

if __name__ == "__main__":
    fetch_trending_repos() 