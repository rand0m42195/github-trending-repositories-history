#!/usr/bin/env python3
"""
Process subscription requests from GitHub Issues
This script reads GitHub Issues with 'subscription' label and adds them to subscriptions.json
"""

import os
import json
import re
from datetime import datetime
from subscription_manager import SubscriptionManager

def parse_issue_body(body):
    """Parse subscription details from GitHub Issue body"""
    email_match = re.search(r'\*\*Email:\*\*\s*(.+)', body)
    categories_match = re.search(r'\*\*Categories:\*\*\s*(.+)', body)
    repositories_match = re.search(r'\*\*Repositories:\*\*\s*(.+)', body)
    
    email = email_match.group(1).strip() if email_match else None
    categories = []
    repositories = []
    
    if categories_match and categories_match.group(1).strip() != 'None':
        categories = [cat.strip() for cat in categories_match.group(1).split(',')]
    
    if repositories_match and repositories_match.group(1).strip() != 'None':
        repositories = [repo.strip() for repo in repositories_match.group(1).split(',')]
    
    return {
        'email': email,
        'categories': categories,
        'repositories': repositories
    }

def process_subscription_issues():
    """Process subscription issues and update subscriptions.json"""
    print("Processing subscription issues...")
    
    # Load existing subscriptions
    subscription_manager = SubscriptionManager()
    
    # For now, we'll manually process issues
    # In a real implementation, you would use GitHub API to fetch issues
    print("""
To process subscription issues:

1. Go to your GitHub repository: https://github.com/rand0m42195/github-trending-repositories-history/issues
2. Look for issues with 'subscription' label
3. For each subscription issue:
   - Copy the issue body content
   - Run this script with the issue data
   - Close the issue after processing

Example usage:
python process_subscription_issues.py --issue-body "**Email:** user@example.com\n**Categories:** AI/ML, Web Development\n**Repositories:** openai/gpt-4"
    """)

def add_subscription_from_issue(issue_body):
    """Add subscription from issue body content"""
    try:
        subscription_data = parse_issue_body(issue_body)
        
        if not subscription_data['email']:
            print("❌ No email found in issue body")
            return False
        
        # Add subscription
        manager = SubscriptionManager()
        success = manager.add_email_subscription(
            email=subscription_data['email'],
            categories=subscription_data['categories'],
            repositories=subscription_data['repositories']
        )
        
        if success:
            print(f"✅ Successfully added subscription for {subscription_data['email']}")
            print(f"   Categories: {subscription_data['categories']}")
            print(f"   Repositories: {subscription_data['repositories']}")
            return True
        else:
            print(f"❌ Failed to add subscription for {subscription_data['email']}")
            return False
            
    except Exception as e:
        print(f"❌ Error processing subscription: {e}")
        return False

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--issue-body':
        if len(sys.argv) > 2:
            issue_body = sys.argv[2]
            add_subscription_from_issue(issue_body)
        else:
            print("❌ Please provide issue body content")
    else:
        process_subscription_issues() 