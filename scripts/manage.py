#!/usr/bin/env python3
"""
Subscription Management Script
A command-line tool to view and manage email subscriptions
"""

import json
import sys
import os

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from subscription.manager import SubscriptionManager

def print_banner():
    """Print management tool banner"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                Subscription Management Tool                  ║
║                                                              ║
║  View and manage email subscriptions for GitHub Trending    ║
╚══════════════════════════════════════════════════════════════╝
    """)

def view_all_subscriptions():
    """Display all current subscriptions"""
    try:
        with open('subscriptions.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("\n📊 Current Subscription Summary")
        print("=" * 50)
        
        # Total subscribers
        total_emails = len(data.get('emails', []))
        print(f"📧 Total Subscribers: {total_emails}")
        
        if total_emails > 0:
            print("\n📋 All Email Addresses:")
            for email in data['emails']:
                print(f"   • {email}")
        
        # Category subscriptions
        categories = data.get('categories', {})
        if categories:
            print(f"\n🏷️  Category Subscriptions ({len(categories)} categories):")
            for category, emails in categories.items():
                print(f"   • {category}: {len(emails)} subscribers")
                for email in emails:
                    print(f"     - {email}")
        
        # Repository subscriptions
        repositories = data.get('repositories', {})
        if repositories:
            print(f"\n📦 Repository Subscriptions ({len(repositories)} repositories):")
            for repo, emails in repositories.items():
                print(f"   • {repo}: {len(emails)} subscribers")
                for email in emails:
                    print(f"     - {email}")
        
        if not categories and not repositories:
            print("\n⚠️  No active subscriptions found.")
            
    except FileNotFoundError:
        print("\n⚠️  No subscription data found. Run the subscription system first.")
    except Exception as e:
        print(f"\n❌ Error reading subscription data: {e}")

def view_subscriber_details(email):
    """Show detailed information for a specific subscriber"""
    try:
        with open('subscriptions.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if email not in data.get('emails', []):
            print(f"\n❌ Email {email} not found in subscriptions.")
            return
        
        print(f"\n👤 Subscriber Details: {email}")
        print("=" * 50)
        
        # Find category subscriptions
        category_subscriptions = []
        for category, emails in data.get('categories', {}).items():
            if email in emails:
                category_subscriptions.append(category)
        
        # Find repository subscriptions
        repo_subscriptions = []
        for repo, emails in data.get('repositories', {}).items():
            if email in emails:
                repo_subscriptions.append(repo)
        
        print(f"📧 Email: {email}")
        print(f"🏷️  Category Subscriptions: {len(category_subscriptions)}")
        for category in category_subscriptions:
            print(f"   • {category}")
        
        print(f"📦 Repository Subscriptions: {len(repo_subscriptions)}")
        for repo in repo_subscriptions:
            print(f"   • {repo}")
        
        if not category_subscriptions and not repo_subscriptions:
            print("   ⚠️  No active subscriptions")
            
    except FileNotFoundError:
        print("\n⚠️  No subscription data found.")
    except Exception as e:
        print(f"\n❌ Error: {e}")

def export_subscriptions():
    """Export subscription data in different formats"""
    try:
        with open('subscriptions.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("\n📤 Export Options:")
        print("1. Export as JSON")
        print("2. Export as CSV")
        print("3. Export summary report")
        
        choice = input("\nSelect export format (1-3): ").strip()
        
        if choice == '1':
            # Export as formatted JSON
            with open('subscriptions_export.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print("✅ Exported to subscriptions_export.json")
            
        elif choice == '2':
            # Export as CSV
            import csv
            with open('subscriptions_export.csv', 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Email', 'Categories', 'Repositories'])
                
                for email in data.get('emails', []):
                    categories = []
                    for category, emails in data.get('categories', {}).items():
                        if email in emails:
                            categories.append(category)
                    
                    repositories = []
                    for repo, emails in data.get('repositories', {}).items():
                        if email in emails:
                            repositories.append(repo)
                    
                    writer.writerow([
                        email,
                        '; '.join(categories),
                        '; '.join(repositories)
                    ])
            print("✅ Exported to subscriptions_export.csv")
            
        elif choice == '3':
            # Export summary report
            with open('subscriptions_report.txt', 'w', encoding='utf-8') as f:
                f.write("GitHub Trending Subscription Report\n")
                f.write("=" * 40 + "\n\n")
                
                f.write(f"Total Subscribers: {len(data.get('emails', []))}\n\n")
                
                f.write("Category Subscriptions:\n")
                for category, emails in data.get('categories', {}).items():
                    f.write(f"  {category}: {len(emails)} subscribers\n")
                
                f.write("\nRepository Subscriptions:\n")
                for repo, emails in data.get('repositories', {}).items():
                    f.write(f"  {repo}: {len(emails)} subscribers\n")
            print("✅ Exported to subscriptions_report.txt")
            
        else:
            print("❌ Invalid choice.")
            
    except FileNotFoundError:
        print("\n⚠️  No subscription data found.")
    except Exception as e:
        print(f"\n❌ Error exporting data: {e}")

def show_menu():
    """Display the main menu"""
    print("\n🔧 Management Options:")
    print("1. View all subscriptions")
    print("2. View subscriber details")
    print("3. Export subscription data")
    print("4. Exit")
    
    choice = input("\nSelect option (1-4): ").strip()
    
    if choice == '1':
        view_all_subscriptions()
    elif choice == '2':
        email = input("Enter email address: ").strip()
        if email:
            view_subscriber_details(email)
        else:
            print("❌ Email address required.")
    elif choice == '3':
        export_subscriptions()
    elif choice == '4':
        print("\n👋 Goodbye!")
        sys.exit(0)
    else:
        print("❌ Invalid choice. Please select 1-4.")

def main():
    """Main function"""
    print_banner()
    
    while True:
        try:
            show_menu()
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    main() 