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
        project_url = "https://rand0m42195.github.io/github-trending-repositories-history"
        
        html_content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 0; background-color: #f6f8fa; }}
                .container {{ max-width: 600px; margin: 0 auto; background-color: white; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px 30px; text-align: center; }}
                .header h1 {{ margin: 0; font-size: 28px; font-weight: 600; }}
                .header p {{ margin: 10px 0 0 0; opacity: 0.9; font-size: 16px; }}
                .content {{ padding: 40px 30px; }}
                .welcome-text {{ font-size: 18px; line-height: 1.6; color: #24292e; margin-bottom: 30px; }}
                .features {{ background-color: #f8f9fa; padding: 25px; border-radius: 8px; margin: 30px 0; }}
                .features h3 {{ margin: 0 0 15px 0; color: #24292e; font-size: 20px; }}
                .features ul {{ margin: 0; padding-left: 20px; }}
                .features li {{ margin: 8px 0; color: #586069; }}
                .buttons {{ text-align: center; margin: 40px 0; }}
                .btn {{ display: inline-block; padding: 12px 24px; margin: 0 10px; text-decoration: none; border-radius: 6px; font-weight: 600; font-size: 14px; transition: all 0.2s; }}
                .btn-primary {{ background-color: #0366d6; color: white; }}
                .btn-primary:hover {{ background-color: #0256cc; }}
                .btn-danger {{ background-color: #dc3545; color: white; }}
                .btn-danger:hover {{ background-color: #c82333; }}
                .footer {{ background-color: #f6f8fa; padding: 30px; text-align: center; color: #586069; font-size: 14px; }}
                .footer a {{ color: #0366d6; text-decoration: none; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎉 Welcome to GitHub Trending!</h1>
                    <p>You're now part of our community of developers</p>
                </div>
                
                <div class="content">
                    <div class="welcome-text">
                        <p>Hi there! 👋</p>
                        <p>Thank you for subscribing to <strong>GitHub Trending Repositories History</strong>! You'll now receive daily updates about the most popular repositories on GitHub, tailored to your interests.</p>
                    </div>
                    
                    <div class="features">
                        <h3>✨ What you'll receive:</h3>
                        <ul>
                            <li>📊 Daily trending repository updates</li>
                            <li>🏷️ Curated content by technology categories</li>
                            <li>📈 Historical trend analysis</li>
                            <li>🔍 Detailed repository information and stats</li>
                        </ul>
                    </div>
                    
                    <div class="buttons">
                        <a href="{project_url}" class="btn btn-primary">🚀 View Trending Repositories</a>
                        <a href="{unsubscribe_url}" class="btn btn-danger">❌ Unsubscribe</a>
                    </div>
                    
                    <p style="font-size: 14px; color: #586069; text-align: center; margin-top: 30px;">
                        💡 <strong>Tip:</strong> You can manage your subscription preferences anytime by visiting our website.
                    </p>
                </div>
                
                <div class="footer">
                    <p>This email was sent to {to_email}</p>
                    <p>Powered by <a href="{project_url}">GitHub Trending History</a></p>
                </div>
            </div>
        </body>
        </html>
        """
        self.send_email(to_email, "🎉 Welcome to GitHub Trending Updates!", html_content)

def generate_category_email_content(category, repos, date):
    """Generate HTML email content for category subscription"""
    project_url = "https://rand0m42195.github.io/github-trending-repositories-history"
    unsubscribe_url = f"{project_url}/unsubscribe?email={repos[0].get('subscriber_email', '')}" if repos else ""
    
    # Get category emoji
    category_emoji = {
        'AI/ML': '🤖',
        'Web Development': '🌐',
        'Mobile': '📱',
        'DevOps': '⚙️',
        'Data Science': '📊',
        'System/OS': '💻',
        'Security': '🔒',
        'Learning': '📚',
        'Other': '📦'
    }.get(category, '📋')
    
    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 0; background-color: #f6f8fa; }}
            .container {{ max-width: 700px; margin: 0 auto; background-color: white; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; }}
            .header h1 {{ margin: 0; font-size: 24px; font-weight: 600; }}
            .header .meta {{ margin: 10px 0 0 0; opacity: 0.9; font-size: 14px; }}
            .content {{ padding: 30px; }}
            .summary {{ background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 25px; text-align: center; }}
            .summary h3 {{ margin: 0 0 10px 0; color: #24292e; font-size: 18px; }}
            .summary p {{ margin: 0; color: #586069; }}
            .repo-item {{ border: 1px solid #e1e4e8; margin: 15px 0; padding: 20px; border-radius: 8px; background-color: white; transition: box-shadow 0.2s; }}
            .repo-item:hover {{ box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
            .repo-name {{ font-weight: 600; font-size: 16px; margin-bottom: 8px; }}
            .repo-name a {{ color: #0366d6; text-decoration: none; }}
            .repo-name a:hover {{ text-decoration: underline; }}
            .repo-desc {{ color: #586069; margin: 8px 0; line-height: 1.5; }}
            .repo-meta {{ color: #6a737d; font-size: 13px; display: flex; align-items: center; gap: 15px; flex-wrap: wrap; }}
            .repo-meta span {{ display: inline-flex; align-items: center; }}
            .streak {{ background-color: #28a745; color: white; padding: 3px 8px; border-radius: 12px; font-size: 11px; font-weight: 600; }}
            .language {{ background-color: #f1f3f4; color: #586069; padding: 3px 8px; border-radius: 12px; font-size: 11px; }}
            .rank {{ color: #0366d6; font-weight: 600; }}
            .footer {{ background-color: #f6f8fa; padding: 25px; text-align: center; }}
            .buttons {{ margin: 20px 0; }}
            .btn {{ display: inline-block; padding: 12px 24px; margin: 0 8px; text-decoration: none; border-radius: 6px; font-weight: 600; font-size: 14px; transition: all 0.2s; }}
            .btn-primary {{ background-color: #0366d6; color: white; }}
            .btn-primary:hover {{ background-color: #0256cc; }}
            .btn-danger {{ background-color: #dc3545; color: white; }}
            .btn-danger:hover {{ background-color: #c82333; }}
            .footer-text {{ color: #586069; font-size: 13px; margin-top: 15px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>{category_emoji} GitHub Trending - {category}</h1>
                <div class="meta">
                    <p>📅 {date} • 📊 {len(repos)} trending repositories</p>
                </div>
            </div>
            
            <div class="content">
                <div class="summary">
                    <h3>🔥 Today's Top {category} Repositories</h3>
                    <p>Here are the most popular repositories in the {category} category today</p>
                </div>
    """
    
    for repo in repos:
        html += f"""
                <div class="repo-item">
                    <div class="repo-name">
                        <a href="{repo['link']}" target="_blank">
                            📦 {repo['name']}
                        </a>
                    </div>
                    <div class="repo-desc">{repo['description']}</div>
                    <div class="repo-meta">
                        <span class="language">💻 {repo.get('language', 'N/A')}</span>
                        <span class="rank">🏆 Rank #{repo['rank']}</span>
                        <span class="streak">🔥 {repo['streak']} days trending</span>
                    </div>
                </div>
        """
    
    html += f"""
            </div>
            
            <div class="footer">
                <div class="buttons">
                    <a href="{project_url}" class="btn btn-primary">🚀 View All Trending</a>
                    <a href="{unsubscribe_url}" class="btn btn-danger">❌ Unsubscribe</a>
                </div>
                <div class="footer-text">
                    <p>💡 Want to see more categories? Visit our website to explore all trending repositories!</p>
                    <p>This email was sent to {repos[0].get('subscriber_email', '') if repos else 'subscriber'}</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return html.replace("{{email}}", repos[0].get('subscriber_email', '')) if repos else html

def generate_repository_email_content(repo, date):
    """Generate HTML email content for repository subscription"""
    project_url = "https://rand0m42195.github.io/github-trending-repositories-history"
    unsubscribe_url = f"{project_url}/unsubscribe?email={repo.get('subscriber_email', '')}"
    
    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 0; background-color: #f6f8fa; }}
            .container {{ max-width: 600px; margin: 0 auto; background-color: white; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; }}
            .header h1 {{ margin: 0; font-size: 24px; font-weight: 600; }}
            .header .meta {{ margin: 10px 0 0 0; opacity: 0.9; font-size: 14px; }}
            .content {{ padding: 30px; }}
            .repo-card {{ border: 2px solid #e1e4e8; border-radius: 12px; padding: 25px; margin: 20px 0; background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%); }}
            .repo-name {{ font-weight: 700; font-size: 20px; margin-bottom: 12px; }}
            .repo-name a {{ color: #0366d6; text-decoration: none; }}
            .repo-name a:hover {{ text-decoration: underline; }}
            .repo-desc {{ color: #586069; margin: 12px 0; line-height: 1.6; font-size: 15px; }}
            .repo-stats {{ display: flex; gap: 20px; margin: 15px 0; flex-wrap: wrap; }}
            .stat {{ display: flex; align-items: center; gap: 5px; }}
            .stat-label {{ color: #6a737d; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; }}
            .stat-value {{ font-weight: 600; }}
            .language {{ background-color: #f1f3f4; color: #586069; padding: 4px 10px; border-radius: 12px; font-size: 12px; }}
            .rank {{ color: #0366d6; font-weight: 700; }}
            .streak {{ background-color: #28a745; color: white; padding: 4px 10px; border-radius: 12px; font-size: 12px; font-weight: 600; }}
            .footer {{ background-color: #f6f8fa; padding: 25px; text-align: center; }}
            .buttons {{ margin: 20px 0; }}
            .btn {{ display: inline-block; padding: 12px 24px; margin: 0 8px; text-decoration: none; border-radius: 6px; font-weight: 600; font-size: 14px; transition: all 0.2s; }}
            .btn-primary {{ background-color: #0366d6; color: white; }}
            .btn-primary:hover {{ background-color: #0256cc; }}
            .btn-secondary {{ background-color: #6c757d; color: white; }}
            .btn-secondary:hover {{ background-color: #5a6268; }}
            .btn-danger {{ background-color: #dc3545; color: white; }}
            .btn-danger:hover {{ background-color: #c82333; }}
            .footer-text {{ color: #586069; font-size: 13px; margin-top: 15px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📦 Repository Update</h1>
                <div class="meta">
                    <p>📅 {date} • 🔥 Trending on GitHub</p>
                </div>
            </div>
            
            <div class="content">
                <div class="repo-card">
                    <div class="repo-name">
                        <a href="{repo['link']}" target="_blank">
                            📦 {repo['name']}
                        </a>
                    </div>
                    <div class="repo-desc">{repo['description']}</div>
                    <div class="repo-stats">
                        <div class="stat">
                            <span class="stat-label">Language</span>
                            <span class="language">{repo.get('language', 'N/A')}</span>
                        </div>
                        <div class="stat">
                            <span class="stat-label">Rank</span>
                            <span class="rank">#{repo['rank']}</span>
                        </div>
                        <div class="stat">
                            <span class="stat-label">Streak</span>
                            <span class="streak">🔥 {repo['streak']} days</span>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="footer">
                <div class="buttons">
                    <a href="{repo['link']}" class="btn btn-primary" target="_blank">🔗 View Repository</a>
                    <a href="{project_url}" class="btn btn-secondary">🚀 View All Trending</a>
                    <a href="{unsubscribe_url}" class="btn btn-danger">❌ Unsubscribe</a>
                </div>
                <div class="footer-text">
                    <p>💡 This repository is currently trending on GitHub! Check it out and stay updated.</p>
                    <p>This email was sent to {repo.get('subscriber_email', 'subscriber')}</p>
                </div>
            </div>
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