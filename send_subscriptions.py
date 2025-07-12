#!/usr/bin/env python3
"""
Script to send daily subscription emails for GitHub Trending updates.
This script is designed to be run from GitHub Actions after fetching trending data.
"""

import os
import sys
import json
from datetime import datetime
from subscription_manager import send_daily_subscriptions

def load_today_trending_data():
    """Load today's trending data from the JSON file"""
    today = datetime.now().strftime('%Y/%m/%d')
    data_file = f'trending_data/{today}/trending.json'
    
    if not os.path.exists(data_file):
        print(f"Trending data file not found: {data_file}")
        return []
    
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"Error loading trending data: {e}")
        return []

def load_category_stats():
    """Load category statistics for email content"""
    today = datetime.now().strftime('%Y/%m/%d')
    stats_file = f'trending_data/{today}/category_stats.json'
    
    if not os.path.exists(stats_file):
        print(f"Category stats file not found: {stats_file}")
        return {}
    
    try:
        with open(stats_file, 'r', encoding='utf-8') as f:
            stats = json.load(f)
        return stats
    except Exception as e:
        print(f"Error loading category stats: {e}")
        return {}

def main():
    """Main function to send daily subscription emails"""
    print("Starting daily subscription email sending...")
    
    # Check if email configuration is available
    required_env_vars = ['SMTP_USERNAME', 'SMTP_PASSWORD', 'SENDER_EMAIL']
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"Missing required environment variables: {missing_vars}")
        print("Skipping email sending. Please configure email settings in GitHub Secrets.")
        return
    
    # Load today's trending data
    today_repos = load_today_trending_data()
    if not today_repos:
        print("No trending data found for today. Skipping email sending.")
        return
    
    # Load category statistics
    category_stats = load_category_stats()
    
    print(f"Found {len(today_repos)} trending repositories for today")
    print(f"Category stats: {len(category_stats)} categories")
    
    # Send subscription emails
    try:
        send_daily_subscriptions(today_repos, category_stats)
        print("Daily subscription emails sent successfully!")
    except Exception as e:
        print(f"Error sending subscription emails: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 