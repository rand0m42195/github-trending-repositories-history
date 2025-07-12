import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import re

# Get today's date string
DATE_STR = datetime.now().strftime('%Y-%m-%d')
YEAR = datetime.now().strftime('%Y')
MONTH = datetime.now().strftime('%m')
DAY = datetime.now().strftime('%d')

DATA_DIR = 'trending_data'
YEAR_DIR = os.path.join(DATA_DIR, YEAR)
MONTH_DIR = os.path.join(YEAR_DIR, MONTH)
DATA_PATH = os.path.join(MONTH_DIR, f'{DAY}.json')

# Ensure data directory exists
os.makedirs(MONTH_DIR, exist_ok=True)

# Fetch GitHub Trending page
url = 'https://github.com/trending'
headers = {'User-Agent': 'Mozilla/5.0'}
resp = requests.get(url, headers=headers)
resp.raise_for_status()
soup = BeautifulSoup(resp.text, 'html.parser')

def parse_stars(stars_text):
    """Parse star count from text like '1.2k stars' or '123 stars'"""
    if not stars_text:
        return 0
    
    # Remove 'stars' and whitespace
    stars_text = stars_text.strip().lower().replace('stars', '').strip()
    
    if not stars_text:
        return 0
    
    # Handle 'k' suffix (thousands)
    if 'k' in stars_text:
        try:
            return int(float(stars_text.replace('k', '')) * 1000)
        except ValueError:
            return 0
    
    # Handle regular numbers
    try:
        return int(stars_text)
    except ValueError:
        return 0

repos = []
for idx, repo_item in enumerate(soup.select('article.Box-row'), 1):
    # Repository name (e.g. 'owner/repo')
    repo_name = repo_item.h2.a.get('href').strip('/')
    # Repository link
    repo_link = f'https://github.com/{repo_name}'
    # Description
    desc_tag = repo_item.find('p')
    repo_desc = desc_tag.text.strip() if desc_tag else ''
    # Language
    lang_tag = repo_item.find('span', itemprop='programmingLanguage')
    repo_lang = lang_tag.text.strip() if lang_tag else ''
    # Stars
    stars_tag = repo_item.find('a', href=lambda x: x and 'stargazers' in x)
    stars_text = stars_tag.text.strip() if stars_tag else ''
    stars_count = parse_stars(stars_text)
    # Rank
    rank = idx
    repos.append({
        'name': repo_name,
        'link': repo_link,
        'description': repo_desc,
        'language': repo_lang,
        'stars': stars_count,
        'rank': rank
    })

# Save to JSON
with open(DATA_PATH, 'w', encoding='utf-8') as f:
    json.dump(repos, f, ensure_ascii=False, indent=2)

print(f'Saved trending data to {DATA_PATH}') 