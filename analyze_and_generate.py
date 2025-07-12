import os
import json
from collections import defaultdict, OrderedDict
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from subscription_manager import send_daily_subscriptions

DATA_DIR = 'trending_data'
OUTPUT_DIR = 'docs'
TEMPLATE_DIR = 'templates'
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'index.html')

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
    """Categorize repository based on description and language"""
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

# 1. Read all trending data, sorted by date
def get_all_data_files():
    """Get all data file paths"""
    data_files = []
    for year in os.listdir(DATA_DIR):
        year_path = os.path.join(DATA_DIR, year)
        if os.path.isdir(year_path):
            for month in os.listdir(year_path):
                month_path = os.path.join(year_path, month)
                if os.path.isdir(month_path):
                    for day_file in os.listdir(month_path):
                        if day_file.endswith('.json'):
                            day = day_file[:-5]  # Remove .json
                            date_str = f"{year}-{month}-{day}"
                            file_path = os.path.join(month_path, day_file)
                            data_files.append((date_str, file_path))
    return sorted(data_files, key=lambda x: x[0])

# 2. Build repo history data structure
repo_history = defaultdict(lambda: {'info': None, 'history': []})
data_files = get_all_data_files()
dates = [date for date, _ in data_files]

for date_str, file_path in data_files:
    with open(file_path, encoding='utf-8') as f:
        day_repos = json.load(f)
    for repo in day_repos:
        name = repo['name']
        if not repo_history[name]['info']:
            repo_history[name]['info'] = repo
        repo_history[name]['history'].append((date_str, repo['rank']))

# 3. Calculate consecutive days on trending
def calc_streak(history_dates):
    """Calculate consecutive days on trending"""
    if not history_dates:
        return 0
    streak = 1
    for i in range(len(history_dates)-2, -1, -1):
        d1 = datetime.strptime(history_dates[i+1], '%Y-%m-%d')
        d0 = datetime.strptime(history_dates[i], '%Y-%m-%d')
        if (d1 - d0).days == 1:
            streak += 1
        else:
            break
    return streak

# 4. Get today's data
today = datetime.now().strftime('%Y-%m-%d')
today_repos = []
if dates and dates[-1] == today:
    # If we have today's data
    today_file_path = data_files[-1][1]
    with open(today_file_path, encoding='utf-8') as f:
        today_repos = json.load(f)
    
    # Add consecutive days and category for each repo today
    for repo in today_repos:
        name = repo['name']
        if name in repo_history:
            history = sorted(repo_history[name]['history'], key=lambda x: x[0])
            dates_only = [d for d, _ in history]
            streak = calc_streak(dates_only)
            repo['streak'] = streak
        else:
            repo['streak'] = 1  # First time on trending
        
        # Add category
        repo['category'] = categorize_repo(repo)

# 5. Generate statistics for all repos (for historical view)
repo_stats = []
for name, data in repo_history.items():
    history = sorted(data['history'], key=lambda x: x[0])
    dates_only = [d for d, _ in history]
    streak = calc_streak(dates_only)
    repo_info = data['info'].copy()
    repo_info['category'] = categorize_repo(repo_info)
    repo_stats.append({
        'name': name,
        'link': repo_info['link'],
        'description': repo_info['description'],
        'language': repo_info.get('language', ''),
        'category': repo_info['category'],
        'streak': streak,
        'history': history,
        'total_days': len(history)
    })

# Sort by streak and latest rank
def latest_rank(repo):
    return repo['history'][-1][1] if repo['history'] else 999
repo_stats.sort(key=lambda r: (-r['streak'], latest_rank(r)))

# 6. Generate category statistics
category_stats = defaultdict(lambda: {'count': 0, 'repos': []})
for repo in repo_stats:
    category = repo['category']
    category_stats[category]['count'] += 1
    category_stats[category]['repos'].append(repo)

# 7. Generate data for specific date
def get_repos_by_date(target_date):
    """Get trending data for specific date"""
    for date_str, file_path in data_files:
        if date_str == target_date:
            with open(file_path, encoding='utf-8') as f:
                day_repos = json.load(f)
            
            # Add consecutive days and category for each repo
            for repo in day_repos:
                name = repo['name']
                if name in repo_history:
                    history = sorted(repo_history[name]['history'], key=lambda x: x[0])
                    # Only calculate consecutive days up to target date
                    target_date_obj = datetime.strptime(target_date, '%Y-%m-%d')
                    filtered_history = [(d, r) for d, r in history if datetime.strptime(d, '%Y-%m-%d') <= target_date_obj]
                    dates_only = [d for d, _ in filtered_history]
                    streak = calc_streak(dates_only)
                    repo['streak'] = streak
                else:
                    repo['streak'] = 1  # First time on trending
                
                # Add category
                repo['category'] = categorize_repo(repo)
            
            return day_repos
    return []

# 8. Render webpage
os.makedirs(OUTPUT_DIR, exist_ok=True)
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
tmpl = env.get_template('index.html.j2')
html = tmpl.render(
    today_repos=today_repos,
    all_repos=repo_stats,
    category_stats=dict(category_stats),
    categories=list(TECH_CATEGORIES.keys()) + ['Other'],
    dates=dates,
    today=today,
    get_repos_by_date=get_repos_by_date
)
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    f.write(html)
print(f'Generated {OUTPUT_FILE}')

# 9. Send subscription emails
if today_repos:
    send_daily_subscriptions(today_repos, dict(category_stats))
    print('Subscription emails sent') 