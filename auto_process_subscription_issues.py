import os
import re
from github import Github
from subscription_manager import SubscriptionManager

REPO = "rand0m42195/github-trending-repositories-history"
SUBSCRIPTION_LABEL = "subscription"
UNSUBSCRIBE_LABEL = "unsubscribe"
TOKEN = os.environ.get("GITHUB_TOKEN")

def parse_issue_body(body):
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

def parse_unsubscribe_body(body):
    """Parse unsubscribe details from GitHub Issue body"""
    email_match = re.search(r'\*\*Email:\*\*\s*(.+)', body)
    email = email_match.group(1).strip() if email_match else None
    return {'email': email}

def main():
    if not TOKEN:
        print("❌ GITHUB_TOKEN not set!")
        return
    
    g = Github(TOKEN)
    repo = g.get_repo(REPO)
    subscription_manager = SubscriptionManager()
    
    # Process subscription issues
    subscription_issues = repo.get_issues(state='open', labels=[SUBSCRIPTION_LABEL])
    for issue in subscription_issues:
        data = parse_issue_body(issue.body)
        if data['email']:
            print(f"Processing subscription for {data['email']}")
            subscription_manager.add_email_subscription(
                email=data['email'],
                categories=data['categories'],
                repositories=data['repositories']
            )
            # Close issue and add comment
            issue.create_comment("✅ Subscription processed and added. Thank you!")
            issue.edit(state="closed")
    
    # Process unsubscribe issues
    unsubscribe_issues = repo.get_issues(state='open', labels=[UNSUBSCRIBE_LABEL])
    for issue in unsubscribe_issues:
        data = parse_unsubscribe_body(issue.body)
        if data['email']:
            print(f"Processing unsubscribe for {data['email']}")
            success = subscription_manager.remove_email_subscription(data['email'])
            if success:
                # Close issue and add comment
                issue.create_comment("✅ Successfully unsubscribed. You will no longer receive updates.")
                issue.edit(state="closed")
            else:
                # Close issue and add comment
                issue.create_comment("❌ Email not found in subscription list.")
                issue.edit(state="closed")

if __name__ == "__main__":
    main() 