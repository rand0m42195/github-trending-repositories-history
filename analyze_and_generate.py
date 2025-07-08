import os
import json
from collections import defaultdict, OrderedDict
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

DATA_DIR = 'trending_data'
OUTPUT_DIR = 'docs'
TEMPLATE_DIR = 'templates'
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'index.html')

# 1. 读取所有trending数据，按日期排序
date_files = sorted([f for f in os.listdir(DATA_DIR) if f.endswith('.json')])
dates = [f[:-5] for f in date_files]  # 'YYYY-MM-DD'

# 2. 构建repo历史数据结构: {repo_name: { 'info': {...}, 'history': [(date, rank), ...] }}
repo_history = defaultdict(lambda: {'info': None, 'history': []})
for date_file, date in zip(date_files, dates):
    with open(os.path.join(DATA_DIR, date_file), encoding='utf-8') as f:
        day_repos = json.load(f)
    for repo in day_repos:
        name = repo['name']
        if not repo_history[name]['info']:
            repo_history[name]['info'] = repo
        repo_history[name]['history'].append((date, repo['rank']))

# 3. 统计连续在榜天数和最近一次连续在榜的天数
def calc_streak(history_dates):
    # 输入: ['2025-07-06', '2025-07-07', '2025-07-08']
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

repo_stats = []
for name, data in repo_history.items():
    history = sorted(data['history'], key=lambda x: x[0])
    dates_only = [d for d, _ in history]
    streak = calc_streak(dates_only)
    repo_stats.append({
        'name': name,
        'link': data['info']['link'],
        'description': data['info']['description'],
        'language': data['info'].get('language', ''),
        'streak': streak,
        'history': history
    })

# 按 streak 和最近排名排序
def latest_rank(repo):
    return repo['history'][-1][1] if repo['history'] else 999
repo_stats.sort(key=lambda r: (-r['streak'], latest_rank(r)))

# 4. 渲染网页
os.makedirs(OUTPUT_DIR, exist_ok=True)
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
tmpl = env.get_template('index.html.j2')
html = tmpl.render(repos=repo_stats, dates=dates)
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    f.write(html)
print(f'Generated {OUTPUT_FILE}') 