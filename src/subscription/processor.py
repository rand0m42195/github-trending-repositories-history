#!/usr/bin/env python3
"""
Process subscription requests from GitHub Issues
This script reads GitHub Issues with 'subscription' label and adds them to subscriptions.json
"""

import os
import json
import re
import sys
from datetime import datetime
from github import Github

# Add the src directory to the path so we can import from sibling modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from subscription.manager import SubscriptionManager

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
    
    # Get GitHub token from environment
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        print("❌ GITHUB_TOKEN environment variable not set")
        return
    
    # Initialize GitHub API
    g = Github(github_token)
    
    # Get repository
    repo_name = "rand0m42195/github-trending-repositories-history"
    try:
        repo = g.get_repo(repo_name)
    except Exception as e:
        print(f"❌ Failed to access repository {repo_name}: {e}")
        return
    
    # Get subscription issues
    try:
        issues = repo.get_issues(state='open', labels=['subscription'])
        print(f"Found {issues.totalCount} open subscription issues")
    except Exception as e:
        print(f"❌ Failed to fetch issues: {e}")
        return
    
    # Load subscription manager
    subscription_manager = SubscriptionManager()
    processed_count = 0
    
    for issue in issues:
        try:
            print(f"Processing issue #{issue.number}: {issue.title}")
            
            # Parse issue body
            subscription_data = parse_issue_body(issue.body or '')
            
            if not subscription_data['email']:
                print(f"  ❌ No email found in issue #{issue.number}")
                continue
            
            # Add subscription
            success = subscription_manager.add_email_subscription(
                email=subscription_data['email'],
                categories=subscription_data['categories'],
                repositories=subscription_data['repositories']
            )
            
            if success:
                print(f"  ✅ Successfully added subscription for {subscription_data['email']}")
                print(f"     Categories: {subscription_data['categories']}")
                print(f"     Repositories: {subscription_data['repositories']}")
                
                # Close the issue
                issue.create_comment("✅ Subscription processed successfully! You will receive a confirmation email shortly.")
                issue.edit(state='closed')
                print(f"  ✅ Issue #{issue.number} closed")
                processed_count += 1
            else:
                print(f"  ❌ Failed to add subscription for {subscription_data['email']}")
                issue.create_comment("❌ Failed to process subscription. Please check the email format and try again.")
                
        except Exception as e:
            print(f"  ❌ Error processing issue #{issue.number}: {e}")
            try:
                issue.create_comment(f"❌ Error processing subscription: {str(e)}")
            except:
                pass
    
    print(f"\n✅ Processing complete. Processed {processed_count} subscription(s)")

def process_unsubscribe_issues():
    """Process unsubscribe issues"""
    print("Processing unsubscribe issues...")
    
    # Get GitHub token from environment
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        print("❌ GITHUB_TOKEN environment variable not set")
        return
    
    # Initialize GitHub API
    g = Github(github_token)
    
    # Get repository
    repo_name = "rand0m42195/github-trending-repositories-history"
    try:
        repo = g.get_repo(repo_name)
    except Exception as e:
        print(f"❌ Failed to access repository {repo_name}: {e}")
        return
    
    # Get unsubscribe issues
    try:
        issues = repo.get_issues(state='open', labels=['unsubscribe'])
        print(f"Found {issues.totalCount} open unsubscribe issues")
    except Exception as e:
        print(f"❌ Failed to fetch issues: {e}")
        return
    
    # Load subscription manager
    subscription_manager = SubscriptionManager()
    processed_count = 0
    
    for issue in issues:
        try:
            print(f"Processing unsubscribe issue #{issue.number}: {issue.title}")
            
            # Extract email from issue title or body
            email_match = re.search(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', issue.title or issue.body or '')
            
            if not email_match:
                print(f"  ❌ No valid email found in issue #{issue.number}")
                continue
            
            email = email_match.group(1)
            
            # Remove subscription
            success = subscription_manager.remove_email_subscription(email)
            
            if success:
                print(f"  ✅ Successfully removed subscription for {email}")
                
                # Close the issue
                issue.create_comment("✅ Unsubscription processed successfully!")
                issue.edit(state='closed')
                print(f"  ✅ Issue #{issue.number} closed")
                processed_count += 1
            else:
                print(f"  ❌ Failed to remove subscription for {email}")
                issue.create_comment("❌ Failed to process unsubscription. Email may not be in our subscription list.")
                
        except Exception as e:
            print(f"  ❌ Error processing unsubscribe issue #{issue.number}: {e}")
            try:
                issue.create_comment(f"❌ Error processing unsubscription: {str(e)}")
            except:
                pass
    
    print(f"\n✅ Unsubscribe processing complete. Processed {processed_count} unsubscription(s)")

if __name__ == "__main__":
    # Process both subscription and unsubscribe issues
    process_subscription_issues()
    process_unsubscribe_issues() 