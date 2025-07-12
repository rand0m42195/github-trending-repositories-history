import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from collections import defaultdict

# Subscription data file
SUBSCRIPTION_FILE = 'data/subscriptions.json'

# Email configuration (to be set via environment variables)
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
SMTP_USERNAME = os.getenv('SMTP_USERNAME', '')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')
SENDER_EMAIL = os.getenv('SENDER_EMAIL', '')

class SubscriptionManager:
    def __init__(self):
        self.subscriptions = self.load_subscriptions()
    
    def load_subscriptions(self):
        """Load existing subscriptions from file"""
        if os.path.exists(SUBSCRIPTION_FILE):
            try:
                with open(SUBSCRIPTION_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return {'emails': [], 'categories': {}, 'repositories': {}}
        return {'emails': [], 'categories': {}, 'repositories': {}}
    
    def save_subscriptions(self):
        """Save subscriptions to file"""
        with open(SUBSCRIPTION_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.subscriptions, f, ensure_ascii=False, indent=2)
    
    def add_email_subscription(self, email, categories=None, repositories=None):
        """Add a new email subscription"""
        if email not in self.subscriptions['emails']:
            self.subscriptions['emails'].append(email)
        
        # Add category subscriptions
        if categories:
            for category in categories:
                if category not in self.subscriptions['categories']:
                    self.subscriptions['categories'][category] = []
                if email not in self.subscriptions['categories'][category]:
                    self.subscriptions['categories'][category].append(email)
        
        # Add repository subscriptions
        if repositories:
            for repo in repositories:
                if repo not in self.subscriptions['repositories']:
                    self.subscriptions['repositories'][repo] = []
                if email not in self.subscriptions['repositories'][repo]:
                    self.subscriptions['repositories'][repo].append(email)
        
        self.save_subscriptions()
        # Send welcome email
        EmailSender().send_welcome_email(email)
        return True
    
    def remove_email_subscription(self, email):
        """Remove an email subscription"""
        if email in self.subscriptions['emails']:
            self.subscriptions['emails'].remove(email)
        
        # Remove from category subscriptions
        for category in self.subscriptions['categories']:
            if email in self.subscriptions['categories'][category]:
                self.subscriptions['categories'][category].remove(email)
        
        # Remove from repository subscriptions
        for repo in self.subscriptions['repositories']:
            if email in self.subscriptions['repositories'][repo]:
                self.subscriptions['repositories'][repo].remove(email)
        
        self.save_subscriptions()
        return True
    
    def get_subscribers_for_category(self, category):
        """Get all subscribers for a specific category"""
        return self.subscriptions['categories'].get(category, [])
    
    def get_subscribers_for_repository(self, repository):
        """Get all subscribers for a specific repository"""
        return self.subscriptions['repositories'].get(repository, [])
    
    def get_all_subscribers(self):
        """Get all email subscribers"""
        return self.subscriptions['emails']

class EmailSender:
    def __init__(self):
        self.smtp_server = SMTP_SERVER
        self.smtp_port = SMTP_PORT
        self.username = SMTP_USERNAME
        self.password = SMTP_PASSWORD
        self.sender_email = SENDER_EMAIL
    
    def send_email(self, to_email, subject, html_content):
        """Send email to subscriber"""
        if not all([self.username, self.password, self.sender_email]):
            print(f"Email configuration incomplete. Skipping email to {to_email}")
            return False
        
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.sender_email
            msg['To'] = to_email
            
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
            
            print(f"Email sent successfully to {to_email}")
            return True
        except Exception as e:
            print(f"Failed to send email to {to_email}: {e}")
            return False

    def send_welcome_email(self, to_email):
        """Send welcome/confirmation email with unsubscribe button"""
        unsubscribe_url = f"https://rand0m42195.github.io/github-trending-repositories-history/unsubscribe?email={to_email}"
        html_content = f"""
        <html>
        <body style='font-family: Arial, sans-serif;'>
            <h2>Welcome to GitHub Trending Updates!</h2>
            <p>You have successfully subscribed to daily trending repository updates.</p>
            <p>You will receive emails based on your selected categories and repositories.</p>
            <p>If you wish to unsubscribe at any time, simply click the button below:</p>
            <a href='{unsubscribe_url}' style='display:inline-block;padding:10px 20px;background:#dc3545;color:white;text-decoration:none;border-radius:5px;font-weight:bold;'>Unsubscribe</a>
        </body>
        </html>
        """
        self.send_email(to_email, "Subscription Confirmed: GitHub Trending Updates", html_content)

def generate_category_email_content(category, repos, date):
    """Generate HTML email content for category subscription"""
    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .header {{ background-color: #f6f8fa; padding: 20px; border-radius: 8px; }}
            .repo-item {{ border: 1px solid #e1e4e8; margin: 10px 0; padding: 15px; border-radius: 6px; }}
            .repo-name {{ font-weight: bold; color: #0366d6; }}
            .repo-desc {{ color: #586069; margin: 5px 0; }}
            .repo-meta {{ color: #6a737d; font-size: 14px; }}
            .streak {{ background-color: #28a745; color: white; padding: 2px 8px; border-radius: 12px; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h2>GitHub Trending Update - {category}</h2>
            <p>Date: {date}</p>
            <p>Found {len(repos)} trending repositories in {category} category</p>
        </div>
    """
    
    for repo in repos:
        html += f"""
        <div class="repo-item">
            <div class="repo-name">
                <a href="{repo['link']}" style="color: #0366d6; text-decoration: none;">
                    {repo['name']}
                </a>
            </div>
            <div class="repo-desc">{repo['description']}</div>
            <div class="repo-meta">
                Language: {repo.get('language', 'N/A')} | 
                Rank: #{repo['rank']} | 
                <span class="streak">{repo['streak']} days</span>
            </div>
        </div>
        """
    
    html += f"""
        <div style=\"margin-top: 30px; padding: 15px; background-color: #f6f8fa; border-radius: 6px;\">
            <p>View all trending repositories: <a href=\"https://rand0m42195.github.io/github-trending-repositories-history\">GitHub Trending History</a></p>
            <a href=\"https://rand0m42195.github.io/github-trending-repositories-history/unsubscribe?email={repos[0].get('subscriber_email', '')}\" style=\"display:inline-block;padding:10px 20px;background:#dc3545;color:white;text-decoration:none;border-radius:5px;font-weight:bold;\">Unsubscribe</a>
        </div>
    </body>
    </html>
    """
    return html.replace("{{email}}", repos[0].get('subscriber_email', '')) if repos else html

def generate_repository_email_content(repo, date):
    """Generate HTML email content for repository subscription"""
    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .header {{ background-color: #f6f8fa; padding: 20px; border-radius: 8px; }}
            .repo-item {{ border: 1px solid #e1e4e8; margin: 10px 0; padding: 15px; border-radius: 6px; }}
            .repo-name {{ font-weight: bold; color: #0366d6; }}
            .repo-desc {{ color: #586069; margin: 5px 0; }}
            .repo-meta {{ color: #6a737d; font-size: 14px; }}
            .streak {{ background-color: #28a745; color: white; padding: 2px 8px; border-radius: 12px; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h2>Repository Trending Update</h2>
            <p>Date: {date}</p>
            <p>Repository: {repo['name']}</p>
        </div>
        
        <div class="repo-item">
            <div class="repo-name">
                <a href="{repo['link']}" style="color: #0366d6; text-decoration: none;">
                    {repo['name']}
                </a>
            </div>
            <div class="repo-desc">{repo['description']}</div>
            <div class="repo-meta">
                Language: {repo.get('language', 'N/A')} | 
                Rank: #{repo['rank']} | 
                <span class="streak">{repo['streak']} days</span>
            </div>
        </div>
        
        <div style="margin-top: 30px; padding: 15px; background-color: #f6f8fa; border-radius: 6px;">
            <p>View all trending repositories: <a href="https://rand0m42195.github.io/github-trending-repositories-history">GitHub Trending History</a></p>
            <a href="https://rand0m42195.github.io/github-trending-repositories-history/unsubscribe?email={repo.get('subscriber_email', '')}" style="display:inline-block;padding:10px 20px;background:#dc3545;color:white;text-decoration:none;border-radius:5px;font-weight:bold;">Unsubscribe</a>
        </div>
    </body>
    </html>
    """
    return html

def send_daily_subscriptions(today_repos, category_stats):
    """Send daily subscription emails"""
    subscription_manager = SubscriptionManager()
    email_sender = EmailSender()
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Send category-based subscriptions
    for category, subscribers in subscription_manager.subscriptions['categories'].items():
        if subscribers:
            # Filter repos for this category
            category_repos = [dict(repo, subscriber_email=email) for repo in today_repos if repo.get('category') == category for email in subscribers]
            if category_repos:
                html_content = generate_category_email_content(category, category_repos, today)
                subject = f"GitHub Trending - {category} ({today})"
                
                for email in subscribers:
                    email_sender.send_email(email, subject, html_content.replace("{{email}}", email))
    
    # Send repository-based subscriptions
    for repo_name, subscribers in subscription_manager.subscriptions['repositories'].items():
        if subscribers:
            # Find the repository in today's trending
            repo_data = next((repo for repo in today_repos if repo['name'] == repo_name), None)
            if repo_data:
                for email in subscribers:
                    repo_with_email = dict(repo_data, subscriber_email=email)
                    html_content = generate_repository_email_content(repo_with_email, today)
                    subject = f"Repository Trending - {repo_name} ({today})"
                    
                    email_sender.send_email(email, subject, html_content)

if __name__ == "__main__":
    # Example usage
    subscription_manager = SubscriptionManager()
    
    # Add a test subscription
    # subscription_manager.add_email_subscription(
    #     "test@example.com", 
    #     categories=["AI/ML"], 
    #     repositories=["openai/gpt-4"]
    # )
    
    print("Subscription manager initialized")
    print(f"Total subscribers: {len(subscription_manager.get_all_subscribers())}") 