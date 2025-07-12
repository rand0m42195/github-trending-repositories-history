# GitHub Trending Repositories History

A comprehensive tool that automatically tracks and analyzes GitHub trending repositories over time, providing historical insights and trend analysis through an interactive web interface.

🌐 **Live Demo**: [View GitHub Trending History](https://rand0m42195.github.io/github-trending-repositories-history)

## Features

### 🔄 **Automated Data Collection**
- **Daily Scraping**: Automatically fetches GitHub trending repositories every day
- **Structured Storage**: Organizes data in year/month/day folder structure for efficient access
- **GitHub Actions Integration**: Fully automated workflow that runs daily at 2:00 UTC

### 📊 **Trend Analysis & Insights**
- **Continuous Days Tracking**: Shows how many consecutive days each repository has been trending
- **Historical Rankings**: Displays daily ranking positions for each repository
- **Technology Categorization**: Automatically categorizes repositories into 8 technology categories:
  - AI/ML (Machine Learning, AI, Neural Networks, etc.)
  - Web Development (Frontend, Backend, Frameworks, etc.)
  - Mobile (iOS, Android, React Native, etc.)
  - DevOps (Docker, Kubernetes, CI/CD, etc.)
  - Data Science (Analytics, Pandas, Jupyter, etc.)
  - System/OS (Operating Systems, Kernels, Low-level programming)
  - Security (Cryptography, Authentication, etc.)
  - Learning (Tutorials, Documentation, Educational content)

### 🌐 **Interactive Web Interface**
- **Today's Trending**: View current trending repositories with continuous days and categories
- **Historical Data**: Browse trending data for any specific date with date selector
- **Search & Filter**: Search repositories by name and filter by technology category
- **Trend Visualization**: Interactive charts showing trending patterns over time
- **Category Statistics**: Overview of trending repositories by technology category
- **Responsive Design**: Mobile-friendly interface that works on all devices

### 📈 **Data Visualization**
- **Trend Charts**: Visual representation of repository ranking trends
- **Category Distribution**: Charts showing the distribution of trending repositories across technology categories
- **Streak Analysis**: Highlight repositories with the longest continuous trending periods

### 📧 **Email Subscription System**
- **Category Subscriptions**: Subscribe to daily updates for specific technology categories
- **Repository Tracking**: Get notified when specific repositories appear on trending
- **HTML Email Templates**: Beautiful, responsive email notifications with repository details
- **Easy Unsubscribe**: Simple unsubscribe process via email reply

## How It Works

1. **Data Collection**: The `fetch_trending.py` script scrapes GitHub's trending page daily
2. **Data Processing**: The `analyze_and_generate.py` script analyzes historical data and calculates trends
3. **Web Generation**: Creates an interactive HTML webpage using Jinja2 templates
4. **Automation**: GitHub Actions workflow handles the entire process automatically
5. **Deployment**: Results are automatically deployed to GitHub Pages

## Technology Stack

- **Python**: Core data processing and web scraping
- **BeautifulSoup4**: HTML parsing for GitHub trending page
- **Jinja2**: Template engine for webpage generation
- **Chart.js**: Interactive data visualization
- **Flask**: REST API for subscription management
- **SMTP**: Email delivery system
- **GitHub Actions**: Automated workflow orchestration
- **GitHub Pages**: Static website hosting

## Project Structure

```
├── fetch_trending.py          # Daily trending data scraper
├── analyze_and_generate.py    # Data analysis and webpage generation
├── subscription_manager.py    # Email subscription management
├── subscription_api.py        # REST API for subscriptions
├── migrate_data.py           # Data migration utilities
├── requirements.txt          # Python dependencies
├── subscriptions.json        # Subscription data storage
├── trending_data/           # Historical data storage (year/month/day structure)
├── templates/               # Jinja2 HTML templates
├── docs/                   # Generated webpage (GitHub Pages)
└── .github/workflows/      # GitHub Actions automation
```

## Getting Started

### Prerequisites
- Python 3.11+
- Git

### Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd github-trending-assistant
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the scraper manually (optional):
   ```bash
   python fetch_trending.py
   python analyze_and_generate.py
   ```

### Automated Operation
The tool is designed to run automatically via GitHub Actions. Simply:
1. Enable GitHub Actions in your repository
2. The workflow will run daily at 2:00 UTC
3. Results are automatically deployed to GitHub Pages
4. Email subscriptions are sent automatically to subscribers

### Email Subscription Setup
To enable email subscriptions, set the following environment variables in your GitHub repository:
- `SMTP_SERVER`: Your SMTP server (e.g., smtp.gmail.com)
- `SMTP_PORT`: SMTP port (usually 587 for TLS)
- `SMTP_USERNAME`: Your email username
- `SMTP_PASSWORD`: Your email password or app password
- `SENDER_EMAIL`: The email address to send from

**Quick Setup:**
```bash
# Run the interactive setup script
python setup_subscription.py

# Test the subscription system
python test_subscription.py
```

**Manual Setup:**
1. Copy `subscriptions_example.json` to `subscriptions.json`
2. Add your email configuration to GitHub repository secrets
3. Follow the `GITHUB_SECRETS_GUIDE.md` for detailed instructions

## Data Storage

Historical data is stored in JSON format with the following structure:
```
trending_data/
├── 2024/
│   ├── 01/
│   │   ├── 01.json
│   │   ├── 02.json
│   │   └── ...
│   └── 02/
│       ├── 01.json
│       └── ...
└── 2025/
    └── ...
```

Each JSON file contains an array of trending repositories with:
- Repository name and link
- Description and programming language
- Daily ranking position
- Star count (when available)

## Contributing

This project is open to contributions! Areas for improvement include:
- Additional technology categories
- Enhanced visualization features
- Performance optimizations
- Mobile app development
- API development for external integrations

## License

This project is open source and available under the MIT License.

---

**Note**: This project was developed with the assistance of AI tools to automate the creation of a comprehensive GitHub trending analysis system. The AI helped with code generation, feature implementation, and documentation, but the core concept and functionality were designed to provide valuable insights into GitHub's trending ecosystem. 