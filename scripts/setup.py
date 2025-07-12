#!/usr/bin/env python3
"""
Setup script for email subscription system
This script helps configure the email settings for GitHub Trending subscriptions
"""

import os
import json
import getpass
from pathlib import Path

def print_banner():
    """Print setup banner"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                GitHub Trending Subscription Setup             ║
║                                                              ║
║  This script will help you configure email notifications    ║
║  for GitHub trending repositories.                          ║
╚══════════════════════════════════════════════════════════════╝
    """)

def get_email_provider():
    """Get email provider choice from user"""
    print("\n📧 Select your email provider:")
    print("1. Gmail (Recommended)")
    print("2. Outlook/Hotmail")
    print("3. Yahoo Mail")
    print("4. Custom SMTP Server")
    
    while True:
        choice = input("\nEnter your choice (1-4): ").strip()
        if choice in ['1', '2', '3', '4']:
            return int(choice)
        print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")

def get_smtp_config(provider_choice):
    """Get SMTP configuration based on provider choice"""
    config = {}
    
    if provider_choice == 1:  # Gmail
        config['server'] = 'smtp.gmail.com'
        config['port'] = 587
        print("\n📧 Gmail Configuration")
        print("Note: You'll need to use an App Password, not your regular password.")
        print("To create an App Password:")
        print("1. Enable 2-Factor Authentication on your Google account")
        print("2. Go to Google Account settings → Security → App passwords")
        print("3. Generate a new app password for 'Mail'")
        
    elif provider_choice == 2:  # Outlook
        config['server'] = 'smtp-mail.outlook.com'
        config['port'] = 587
        print("\n📧 Outlook/Hotmail Configuration")
        
    elif provider_choice == 3:  # Yahoo
        config['server'] = 'smtp.mail.yahoo.com'
        config['port'] = 587
        print("\n📧 Yahoo Mail Configuration")
        
    else:  # Custom
        config['server'] = input("Enter SMTP server (e.g., smtp.yourprovider.com): ").strip()
        config['port'] = int(input("Enter SMTP port (usually 587): ").strip() or "587")
        print("\n📧 Custom SMTP Configuration")
    
    # Get email credentials
    config['username'] = input("Enter your email address: ").strip()
    config['password'] = getpass.getpass("Enter your password/app password: ")
    config['sender_email'] = config['username']  # Usually same as username
    
    return config

def create_env_file(config):
    """Create .env file with email configuration"""
    env_content = f"""# Email Configuration for GitHub Trending Subscriptions
SMTP_SERVER={config['server']}
SMTP_PORT={config['port']}
SMTP_USERNAME={config['username']}
SMTP_PASSWORD={config['password']}
SENDER_EMAIL={config['sender_email']}

# Optional: Admin key for subscription management
ADMIN_KEY=admin123
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Created .env file with email configuration")

def create_github_secrets_guide():
    """Create guide for setting up GitHub secrets"""
    guide_content = """# GitHub Secrets Setup Guide

To enable email subscriptions in GitHub Actions, you need to add these secrets to your repository:

## Steps:
1. Go to your GitHub repository
2. Click on "Settings" tab
3. Click on "Secrets and variables" → "Actions"
4. Click "New repository secret" for each of the following:

## Required Secrets:

### SMTP_SERVER
- Value: Your SMTP server (e.g., smtp.gmail.com)
- Description: SMTP server for sending emails

### SMTP_PORT
- Value: SMTP port (usually 587)
- Description: SMTP port for sending emails

### SMTP_USERNAME
- Value: Your email address
- Description: Email username for SMTP authentication

### SMTP_PASSWORD
- Value: Your email password or app password
- Description: Email password for SMTP authentication

### SENDER_EMAIL
- Value: Your email address
- Description: Email address to send from

## Example for Gmail:
- SMTP_SERVER: smtp.gmail.com
- SMTP_PORT: 587
- SMTP_USERNAME: your-email@gmail.com
- SMTP_PASSWORD: your-app-password
- SENDER_EMAIL: your-email@gmail.com

## Security Notes:
- Never commit these secrets to your code
- Use App Passwords for Gmail (not your regular password)
- Keep your .env file local and don't commit it
"""
    
    with open('GITHUB_SECRETS_GUIDE.md', 'w') as f:
        f.write(guide_content)
    
    print("✅ Created GITHUB_SECRETS_GUIDE.md")

def test_email_config(config):
    """Test email configuration"""
    print("\n🧪 Testing email configuration...")
    
    try:
        import smtplib
        from email.mime.text import MIMEText
        
        # Create test message
        msg = MIMEText("This is a test email from GitHub Trending Subscription setup.")
        msg['Subject'] = 'GitHub Trending - Test Email'
        msg['From'] = config['sender_email']
        msg['To'] = config['username']
        
        # Test connection
        with smtplib.SMTP(config['server'], config['port']) as server:
            server.starttls()
            server.login(config['username'], config['password'])
            server.send_message(msg)
        
        print("✅ Email configuration test successful!")
        print(f"   Test email sent to {config['username']}")
        return True
        
    except Exception as e:
        print(f"❌ Email configuration test failed: {e}")
        print("\nCommon issues:")
        print("- Check your email and password")
        print("- For Gmail, make sure you're using an App Password")
        print("- Check if your email provider allows SMTP access")
        return False

def main():
    """Main setup function"""
    print_banner()
    
    # Check if .env already exists
    if os.path.exists('.env'):
        overwrite = input("⚠️  .env file already exists. Overwrite? (y/N): ").strip().lower()
        if overwrite != 'y':
            print("Setup cancelled.")
            return
    
    # Get email provider and configuration
    provider_choice = get_email_provider()
    config = get_smtp_config(provider_choice)
    
    # Create .env file
    create_env_file(config)
    
    # Create GitHub secrets guide
    create_github_secrets_guide()
    
    # Test configuration
    test_config = input("\n🧪 Test email configuration now? (y/N): ").strip().lower()
    if test_config == 'y':
        test_email_config(config)
    
    # Final instructions
    print("\n" + "="*60)
    print("🎉 Setup Complete!")
    print("="*60)
    print("\nNext steps:")
    print("1. ✅ Email configuration saved to .env file")
    print("2. 📋 Review GITHUB_SECRETS_GUIDE.md for GitHub setup")
    print("3. 🔧 Add secrets to your GitHub repository")
    print("4. 🚀 Run 'python test_subscription.py' to verify everything works")
    print("5. 📧 Test the subscription system with a real email")
    
    print("\n📚 Additional resources:")
    print("- SUBSCRIPTION_GUIDE.md - Detailed usage guide")
    print("- README.md - Project overview and features")
    
    print("\n🔒 Security reminder:")
    print("- Keep your .env file secure and don't commit it to Git")
    print("- Use App Passwords for Gmail accounts")
    print("- Regularly rotate your email passwords")

if __name__ == "__main__":
    main() 