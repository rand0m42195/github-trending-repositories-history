# Email Configuration for GitHub Actions

This document explains how to configure email settings in GitHub Secrets to enable automatic sending of subscription emails.

## Overview

The GitHub Actions workflow automatically sends daily subscription emails to users who have subscribed to GitHub Trending updates. To enable this feature, you need to configure email settings in your GitHub repository secrets.

## Required GitHub Secrets

You need to add the following secrets to your GitHub repository:

### 1. SMTP_SERVER
- **Description**: Your SMTP server address
- **Example**: `smtp.gmail.com` (for Gmail)
- **Other options**: 
  - `smtp.office365.com` (for Outlook/Office 365)
  - `smtp.mail.yahoo.com` (for Yahoo Mail)
  - Your custom SMTP server

### 2. SMTP_PORT
- **Description**: SMTP server port number
- **Example**: `587` (for TLS)
- **Other options**: `465` (for SSL), `25` (for non-encrypted)

### 3. SMTP_USERNAME
- **Description**: Your email username/address
- **Example**: `your-email@gmail.com`

### 4. SMTP_PASSWORD
- **Description**: Your email password or app password
- **Note**: For Gmail, you need to use an App Password, not your regular password

### 5. SENDER_EMAIL
- **Description**: The email address that will appear as the sender
- **Example**: `your-email@gmail.com` (usually same as SMTP_USERNAME)

## How to Add GitHub Secrets

1. Go to your GitHub repository
2. Click on **Settings** tab
3. In the left sidebar, click on **Secrets and variables** → **Actions**
4. Click **New repository secret**
5. Add each secret with the exact names listed above

## Email Provider Setup Examples

### Gmail Setup

1. **Enable 2-Factor Authentication** on your Google account
2. **Generate an App Password**:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate a new app password for "Mail"
3. **Configure GitHub Secrets**:
   ```
   SMTP_SERVER: smtp.gmail.com
   SMTP_PORT: 587
   SMTP_USERNAME: your-email@gmail.com
   SMTP_PASSWORD: [your-16-character-app-password]
   SENDER_EMAIL: your-email@gmail.com
   ```

### Outlook/Office 365 Setup

1. **Enable SMTP Authentication** in your Office 365 account
2. **Configure GitHub Secrets**:
   ```
   SMTP_SERVER: smtp.office365.com
   SMTP_PORT: 587
   SMTP_USERNAME: your-email@outlook.com
   SMTP_PASSWORD: [your-email-password]
   SENDER_EMAIL: your-email@outlook.com
   ```

### Custom SMTP Server

If you have your own SMTP server or use a service like SendGrid, Mailgun, etc.:

```
SMTP_SERVER: [your-smtp-server.com]
SMTP_PORT: [your-smtp-port]
SMTP_USERNAME: [your-smtp-username]
SMTP_PASSWORD: [your-smtp-password]
SENDER_EMAIL: [your-sender-email]
```

## Testing Email Configuration

After setting up the secrets, the GitHub Actions workflow will automatically:

1. Fetch trending data daily
2. Generate the webpage
3. Send subscription emails to all subscribers
4. Commit and push changes

You can check if emails are being sent by:

1. **Viewing GitHub Actions logs**:
   - Go to Actions tab in your repository
   - Click on the latest workflow run
   - Check the "Send Subscription Emails" step logs

2. **Adding a test subscription**:
   - Visit your website's subscription page
   - Add a test email subscription
   - Wait for the next daily run to see if emails are sent

## Troubleshooting

### Common Issues

1. **"Email configuration incomplete" error**:
   - Check that all required secrets are set
   - Verify secret names are exactly as shown above

2. **"Authentication failed" error**:
   - For Gmail: Make sure you're using an App Password, not your regular password
   - For other providers: Check if SMTP authentication is enabled

3. **"Connection refused" error**:
   - Verify SMTP_SERVER and SMTP_PORT are correct
   - Check if your email provider allows SMTP access

4. **Emails not being sent**:
   - Check GitHub Actions logs for error messages
   - Verify that there are active subscriptions in `subscriptions.json`

### Security Notes

- **Never commit email credentials** to your repository
- **Use App Passwords** instead of regular passwords when possible
- **Regularly rotate** your email passwords/app passwords
- **Monitor** your email sending limits to avoid being blocked

## Email Templates

The system uses HTML email templates that include:

- Repository information (name, description, language, rank, streak)
- Category-based grouping
- Unsubscribe links
- Links to the main website

Templates are defined in `subscription_manager.py` and can be customized as needed.

## Monitoring and Logs

- **GitHub Actions logs** show email sending status
- **Email delivery** depends on your SMTP provider
- **Bounce handling** should be monitored through your email provider
- **Unsubscribe requests** are handled through the web interface

## Rate Limits

Be aware of email sending limits:

- **Gmail**: 500 emails/day for regular accounts, 2000/day for Google Workspace
- **Outlook**: 300 emails/day
- **Custom SMTP**: Varies by provider

The system will log when emails are sent and any errors that occur. 