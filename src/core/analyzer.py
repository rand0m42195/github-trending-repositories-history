"""
Data analysis and webpage generation for Github Trending History.
"""

import os
import json
import shutil
from collections import defaultdict, OrderedDict
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

from .categorizer import categorize_repo, TECH_CATEGORIES

DATA_DIR = 'data/trending_data'
OUTPUT_DIR = 'docs'
TEMPLATE_DIR = 'src/web/templates'
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'index.html')

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

def get_repos_by_date(target_date):
    """Get trending data for specific date"""
    data_files = get_all_data_files()
    for date_str, file_path in data_files:
        if date_str == target_date:
            with open(file_path, encoding='utf-8') as f:
                day_repos = json.load(f)
            
            # Add consecutive days and category for each repo
            for repo in day_repos:
                name = repo['name']
                # Add category
                repo['category'] = categorize_repo(repo)
            
            return day_repos
    return []

def analyze_and_generate():
    """
    Main function to analyze trending data and generate the webpage.
    """
    # 1. Read all trending data, sorted by date
    data_files = get_all_data_files()
    dates = [date for date, _ in data_files]

    # 2. Build repo history data structure
    repo_history = defaultdict(lambda: {'info': None, 'history': []})

    for date_str, file_path in data_files:
        with open(file_path, encoding='utf-8') as f:
            day_repos = json.load(f)
        for repo in day_repos:
            name = repo['name']
            if not repo_history[name]['info']:
                repo_history[name]['info'] = repo
            repo_history[name]['history'].append((date_str, repo['rank']))

    # 3. Get today's data
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

    # 4. Generate statistics for all repos (for historical view)
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

    # 5. Generate category statistics
    category_stats = defaultdict(lambda: {'count': 0, 'repos': []})
    for repo in repo_stats:
        category = repo['category']
        category_stats[category]['count'] += 1
        category_stats[category]['repos'].append(repo)

    # 6. Render webpage
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Copy static files to output directory
    static_dir = 'src/web/static'
    if os.path.exists(static_dir):
        static_output_dir = os.path.join(OUTPUT_DIR, 'static')
        if os.path.exists(static_output_dir):
            shutil.rmtree(static_output_dir)
        shutil.copytree(static_dir, static_output_dir)
        print(f'Copied static files to {static_output_dir}')

    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

    # Generate main page
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

    # Generate unsubscribe page
    unsubscribe_tmpl = env.get_template('unsubscribe.html.j2')
    unsubscribe_html = unsubscribe_tmpl.render(email='')
    unsubscribe_file = os.path.join(OUTPUT_DIR, 'unsubscribe.html')
    with open(unsubscribe_file, 'w', encoding='utf-8') as f:
        f.write(unsubscribe_html)
    print(f'Generated {unsubscribe_file}')

    # 7. Send subscription emails
    if today_repos:
        try:
            from ..subscription.manager import send_daily_subscriptions
            send_daily_subscriptions(today_repos, dict(category_stats))
            print('Subscription emails sent')
        except ImportError:
            print('Subscription module not available, skipping email sending')
        except Exception as e:
            print(f'Error sending subscription emails: {e}')

if __name__ == "__main__":
    analyze_and_generate() 