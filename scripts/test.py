#!/usr/bin/env python3
"""
Test script for subscription functionality
Run this script to test the email subscription system
"""

import os
import json
from subscription_manager import SubscriptionManager, EmailSender
from datetime import datetime

def test_subscription_manager():
    """Test subscription manager functionality"""
    print("🧪 Testing Subscription Manager...")
    
    # Initialize manager
    manager = SubscriptionManager()
    
    # Test adding subscriptions
    test_email = "test@example.com"
    test_categories = ["AI/ML", "Web Development"]
    test_repositories = ["openai/gpt-4", "microsoft/vscode"]
    
    print(f"Adding subscription for {test_email}...")
    manager.add_email_subscription(test_email, test_categories, test_repositories)
    
    # Verify subscription was added
    all_subscribers = manager.get_all_subscribers()
    if test_email in all_subscribers:
        print("✅ Email subscription added successfully")
    else:
        print("❌ Email subscription failed")
        return False
    
    # Test category subscriptions
    ai_ml_subscribers = manager.get_subscribers_for_category("AI/ML")
    if test_email in ai_ml_subscribers:
        print("✅ Category subscription (AI/ML) added successfully")
    else:
        print("❌ Category subscription failed")
        return False
    
    # Test repository subscriptions
    repo_subscribers = manager.get_subscribers_for_repository("openai/gpt-4")
    if test_email in repo_subscribers:
        print("✅ Repository subscription added successfully")
    else:
        print("❌ Repository subscription failed")
        return False
    
    # Test removing subscription
    print(f"Removing subscription for {test_email}...")
    manager.remove_email_subscription(test_email)
    
    # Verify subscription was removed
    all_subscribers_after = manager.get_all_subscribers()
    if test_email not in all_subscribers_after:
        print("✅ Email subscription removed successfully")
    else:
        print("❌ Email subscription removal failed")
        return False
    
    print("✅ All subscription manager tests passed!")
    return True

def test_email_sender():
    """Test email sender functionality"""
    print("\n📧 Testing Email Sender...")
    
    sender = EmailSender()
    
    # Check if email configuration is available
    if not all([sender.username, sender.password, sender.sender_email]):
        print("⚠️  Email configuration not found. Skipping email tests.")
        print("   Set environment variables: SMTP_USERNAME, SMTP_PASSWORD, SENDER_EMAIL")
        return True
    
    print("✅ Email configuration found")
    print(f"   SMTP Server: {sender.smtp_server}:{sender.smtp_port}")
    print(f"   Username: {sender.username}")
    print(f"   Sender: {sender.sender_email}")
    
    return True

def test_email_templates():
    """Test email template generation"""
    print("\n📝 Testing Email Templates...")
    
    # Sample repository data
    test_repo = {
        'name': 'openai/gpt-4',
        'link': 'https://github.com/openai/gpt-4',
        'description': 'GPT-4 is a large multimodal model that can solve complex problems with greater accuracy than its predecessors.',
        'language': 'Python',
        'rank': 1,
        'streak': 5,
        'category': 'AI/ML'
    }
    
    test_repos = [test_repo]
    
    # Test category email template
    from subscription_manager import generate_category_email_content
    category_html = generate_category_email_content("AI/ML", test_repos, "2024-01-15")
    
    if "AI/ML" in category_html and "openai/gpt-4" in category_html:
        print("✅ Category email template generated successfully")
    else:
        print("❌ Category email template generation failed")
        return False
    
    # Test repository email template
    from subscription_manager import generate_repository_email_content
    repo_html = generate_repository_email_content(test_repo, "2024-01-15")
    
    if "openai/gpt-4" in repo_html and "GPT-4" in repo_html:
        print("✅ Repository email template generated successfully")
    else:
        print("❌ Repository email template generation failed")
        return False
    
    print("✅ All email template tests passed!")
    return True

def test_subscription_data_structure():
    """Test subscription data structure"""
    print("\n📊 Testing Subscription Data Structure...")
    
    # Create test data
    test_data = {
        'emails': ['user1@example.com', 'user2@example.com'],
        'categories': {
            'AI/ML': ['user1@example.com'],
            'Web Development': ['user2@example.com']
        },
        'repositories': {
            'openai/gpt-4': ['user1@example.com'],
            'microsoft/vscode': ['user2@example.com']
        }
    }
    
    # Test JSON serialization
    try:
        json_str = json.dumps(test_data, ensure_ascii=False, indent=2)
        parsed_data = json.loads(json_str)
        
        if parsed_data == test_data:
            print("✅ Subscription data JSON serialization works")
        else:
            print("❌ Subscription data JSON serialization failed")
            return False
    except Exception as e:
        print(f"❌ JSON serialization error: {e}")
        return False
    
    print("✅ All data structure tests passed!")
    return True

def main():
    """Run all tests"""
    print("🚀 Starting Subscription System Tests\n")
    
    tests = [
        test_subscription_manager,
        test_email_sender,
        test_email_templates,
        test_subscription_data_structure
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
    
    print(f"\n📈 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Subscription system is ready to use.")
    else:
        print("⚠️  Some tests failed. Please check the configuration.")
    
    # Clean up test data
    if os.path.exists('subscriptions.json'):
        try:
            os.remove('subscriptions.json')
            print("🧹 Cleaned up test data")
        except:
            pass

if __name__ == "__main__":
    main() 