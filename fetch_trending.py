import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json

# Get today's date string
DATE_STR = datetime.now().strftime('%Y-%m-%d')
DATA_DIR = 'trending_data'
DATA_PATH = os.path.join(DATA_DIR, f'{DATE_STR}.json')

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# Fetch GitHub Trending page
url = 'https://github.com/trending'
headers = {'User-Agent': 'Mozilla/5.0'}
resp = requests.get(url, headers=headers)
resp.raise_for_status()
soup = BeautifulSoup(resp.text, 'html.parser')

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
    # Rank
    rank = idx
    repos.append({
        'name': repo_name,
        'link': repo_link,
        'description': repo_desc,
        'language': repo_lang,
        'rank': rank
    })

# Save to JSON
with open(DATA_PATH, 'w', encoding='utf-8') as f:
    json.dump(repos, f, ensure_ascii=False, indent=2)

print(f'Saved trending data to {DATA_PATH}') 