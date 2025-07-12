# GitHub Trending Assistant

A comprehensive tool to track and analyze GitHub trending repositories over time, with historical data visualization and email subscription features.

## 🚀 Features

- **Daily Trending Data Collection**: Automatically fetches GitHub trending repositories
- **Historical Analysis**: Tracks repositories over time with streak calculations
- **Interactive Web Interface**: Beautiful, responsive web page with filtering and search
- **Email Subscriptions**: Daily email updates for specific categories or repositories
- **Trend Visualization**: Charts showing category distribution and trending patterns
- **Multi-level Date Navigation**: Browse historical data by year/month/day

## 📁 Project Structure

```
github-trending-assistant/
├── src/                          # Source code
│   ├── core/                     # Core functionality
│   │   ├── fetcher.py           # Data fetching from GitHub
│   │   ├── analyzer.py          # Data analysis and webpage generation
│   │   └── categorizer.py       # Repository categorization logic
│   ├── subscription/             # Subscription system
│   │   ├── manager.py           # Subscription management
│   │   ├── api.py               # REST API for subscriptions
│   │   └── processor.py         # GitHub Issues processing
│   ├── web/                     # Web assets
│   │   ├── templates/           # Jinja2 templates
│   │   └── static/              # Static files (CSS, JS, images)
│   └── utils/                   # Utility functions
│       └── helpers.py           # Common helper functions
├── data/                        # Data storage
│   ├── trending_data/           # Historical trending data
│   └── subscriptions.json       # Subscription data
├── scripts/                     # Management scripts
│   ├── setup.py                 # Setup and configuration
│   ├── test.py                  # Testing utilities
│   └── manage.py                # Subscription management CLI
├── docs/                        # Generated documentation
│   ├── guides/                  # User guides
│   └── features/                # Feature documentation
├── .github/                     # GitHub configuration
│   └── workflows/               # GitHub Actions
├── main.py                      # Main entry point
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/github-trending-assistant.git
   cd github-trending-assistant
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment** (optional, for email subscriptions):
   ```bash
   python scripts/setup.py
   ```

## 🚀 Usage

### Command Line Interface

The project provides a unified CLI through `main.py`:

```bash
# Fetch today's trending repositories
python main.py fetch

# Analyze existing data and generate webpage
python main.py analyze

# Run complete pipeline (fetch + analyze)
python main.py full

# Enable verbose output
python main.py fetch --verbose
```

### Individual Scripts

You can also run individual components:

```bash
# Fetch trending data
python src/core/fetcher.py

# Generate webpage
python src/core/analyzer.py

# Manage subscriptions
python scripts/manage.py

# Test subscription system
python scripts/test.py
```

### Web Interface

After running the analysis, open `docs/index.html` in your browser to view:
- Today's trending repositories
- Historical data with date navigation
- Category-based filtering and search
- Trend analysis charts
- Subscription management

## 📧 Email Subscriptions

### For Users

1. Visit the web interface and go to the "Subscribe" tab
2. Enter your email and select categories of interest
3. Optionally specify individual repositories to track
4. Submit the form to create a subscription request

### For Administrators

Manage subscriptions using the CLI:

```bash
# View all subscriptions
python scripts/manage.py list

# Export subscriptions to CSV
python scripts/manage.py export --format csv

# Send test emails
python scripts/test.py
```

## 🔧 Configuration

### Email Settings

For email functionality, set these environment variables:

```bash
export SMTP_SERVER=smtp.gmail.com
export SMTP_PORT=587
export SMTP_USERNAME=your-email@gmail.com
export SMTP_PASSWORD=your-app-password
export SENDER_EMAIL=your-email@gmail.com
```

### GitHub Actions

The project includes automated workflows:
- **Daily Updates**: Fetches trending data and generates webpage
- **Subscription Processing**: Processes subscription requests from GitHub Issues

## 📊 Data Storage

- **Trending Data**: Stored in `data/trending_data/` organized by year/month/day
- **Subscriptions**: Stored in `data/subscriptions.json`
- **Generated Webpage**: Output to `docs/index.html`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test thoroughly: `python scripts/test.py`
5. Commit your changes: `git commit -m 'Add feature'`
6. Push to the branch: `git push origin feature-name`
7. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- GitHub for providing the trending data
- BeautifulSoup for web scraping capabilities
- Jinja2 for template rendering
- Chart.js for data visualization

## 📞 Support

If you encounter any issues or have questions:
1. Check the documentation in `docs/`
2. Review existing issues on GitHub
3. Create a new issue with detailed information

---

**Happy trending! 🚀** 