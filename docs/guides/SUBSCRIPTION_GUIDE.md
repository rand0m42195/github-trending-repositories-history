# Email Subscription Guide

This guide explains how to set up and use the email subscription feature for GitHub Trending updates.

## Features

### 📧 **What You Can Subscribe To**

1. **Technology Categories**: Get daily updates for specific technology areas
   - AI/ML (Machine Learning, AI, Neural Networks)
   - Web Development (Frontend, Backend, Frameworks)
   - Mobile (iOS, Android, React Native)
   - DevOps (Docker, Kubernetes, CI/CD)
   - Data Science (Analytics, Pandas, Jupyter)
   - System/OS (Operating Systems, Kernels)
   - Security (Cryptography, Authentication)
   - Learning (Tutorials, Documentation)

2. **Specific Repositories**: Track individual repositories
   - Get notified when a specific repository appears on trending
   - Perfect for monitoring your favorite projects

## Automated Processing

GitHub Actions automatically processes subscription requests every 5 minutes:
- Checks for new subscription issues
- Processes subscription requests
- Updates subscription data
- Sends confirmation emails

## Setup Instructions

### 1. **Configure Email Settings**

Set up the following environment variables in your GitHub repository:

1. Go to your repository → Settings → Secrets and variables → Actions
2. Add the following repository secrets:

```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SENDER_EMAIL=your-email@gmail.com
```

### 2. **Gmail App Password Setup** (Recommended)

For Gmail, use an App Password instead of your regular password:

1. Enable 2-Factor Authentication on your Google account
2. Go to Google Account settings → Security → App passwords
3. Generate a new app password for "Mail"
4. Use this app password as `SMTP_PASSWORD`

### 3. **Alternative Email Providers**

#### Outlook/Hotmail
```
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587
```

#### Yahoo Mail
```
SMTP_SERVER=smtp.mail.yahoo.com
SMTP_PORT=587
```

#### Custom SMTP Server
```
SMTP_SERVER=your-smtp-server.com
SMTP_PORT=587
```

## Usage

### **For Users**

#### Subscribe via API
```bash
curl -X POST https://your-domain.com/subscribe \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "categories": ["AI/ML", "Web Development"],
    "repositories": ["openai/gpt-4", "microsoft/vscode"]
  }'
```

#### Unsubscribe
```bash
curl -X POST https://your-domain.com/unsubscribe \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com"}'
```

#### Web Interface
Visit `/subscribe` on your domain to use the web form.

### **For Developers**

#### Check Subscription Status
```bash
curl "https://your-domain.com/subscriptions?admin_key=your-admin-key"
```

#### Health Check
```bash
curl https://your-domain.com/health
```

## Email Format

### **Category Subscription Email**
- **Subject**: `GitHub Trending - AI/ML (2024-01-15)`
- **Content**: List of all trending repositories in the AI/ML category
- **Includes**: Repository name, description, language, rank, streak days

### **Repository Subscription Email**
- **Subject**: `Repository Trending - openai/gpt-4 (2024-01-15)`
- **Content**: Details about the specific repository
- **Includes**: Repository info, current rank, streak days

## Email Template Features

- **Responsive Design**: Works on desktop and mobile
- **Repository Links**: Direct links to GitHub repositories
- **Category Badges**: Color-coded category indicators
- **Streak Information**: Shows consecutive days on trending
- **Unsubscribe Instructions**: Easy unsubscribe process

## Management

### **View All Subscriptions**
```bash
curl "https://your-domain.com/subscriptions?admin_key=your-admin-key"
```

### **Manual Subscription Management**
Edit `subscriptions.json` directly:

```json
{
  "emails": ["user1@example.com", "user2@example.com"],
  "categories": {
    "AI/ML": ["user1@example.com"],
    "Web Development": ["user2@example.com"]
  },
  "repositories": {
    "openai/gpt-4": ["user1@example.com"]
  }
}
```

## Troubleshooting

### **Common Issues**

1. **Emails not sending**
   - Check SMTP credentials
   - Verify firewall settings
   - Check GitHub Actions logs

2. **Authentication errors**
   - Use App Password for Gmail
   - Enable "Less secure app access" (not recommended)
   - Check 2FA settings

3. **Subscription not working**
   - Verify email format
   - Check subscription file permissions
   - Review API logs

### **Testing**

Test the email system locally:

```bash
# Set environment variables
export SMTP_SERVER=smtp.gmail.com
export SMTP_PORT=587
export SMTP_USERNAME=your-email@gmail.com
export SMTP_PASSWORD=your-app-password
export SENDER_EMAIL=your-email@gmail.com

# Run subscription manager
python subscription_manager.py

# Test API (if running locally)
python subscription_api.py
```

## Security Considerations

1. **Environment Variables**: Never commit email credentials to code
2. **App Passwords**: Use app passwords instead of regular passwords
3. **Rate Limiting**: Consider implementing rate limiting for API endpoints
4. **Email Validation**: Validate email addresses before storing
5. **Unsubscribe**: Always provide easy unsubscribe options

## Privacy

- Email addresses are stored locally in `subscriptions.json`
- No third-party services are used for email storage
- Users can unsubscribe at any time
- No personal data is collected beyond email addresses

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review GitHub Actions logs
3. Verify email configuration
4. Test with a simple email first 