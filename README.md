# Manshar - Social Media Publishing Tool
<img src="./docs/logo.png" alt="Manshar Logo" width="200" height="auto">

A Python application that automatically publishes new blog posts from an RSS feed to various social media platforms (Twitter, Facebook, Telegram, and LinkedIn). Now includes **daily manual posting** of engaging bite-sized content!

## Features

### 📰 Regular Article Posting
- Monitors RSS feed for new posts
- Automatically publishes to Twitter, Facebook, Telegram, and LinkedIn
- AI-powered content generation with OpenAI integration
- Error handling and logging
- Prevents duplicate posts

### 🎯 Daily Engaging Content (NEW!)
- **Manual daily posting** of bite-sized, engaging content
- **Random article selection** from aiinarabic.com  
- **Multiple content types**: "Did you know?", definitions, tips, quotes, amazing facts
- **Smart content generation** using AI to extract engaging snippets
- **Platform optimization** with engagement scoring
- **Duplicate prevention** across all content types
- **Dry-run mode** for testing before posting

👉 **[See Daily Posting Feature Details](DAILY_POSTING.md)**

## Prerequisites

- Python 3.7 or higher
- RSS feed URL of your blog
- Social media API credentials:
  - Twitter Developer Account
  - Facebook Developer Account
  - LinkedIn Developer Account

## Installation

1. Clone this repository:
```bash
git clone https://github.com/AIArabicProjects/manshar.git
cd manshar
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Copy the `config.yaml.example` file to `config.yaml` and fill in your credentials:
```bash
cp config.yaml.example config.yaml
```

4. Edit the `config.yaml` file with your API credentials and RSS feed URL.

## Usage

### Regular Article Posting
Run the application for regular article posting:
```bash
python main.py
```

### Daily Content Posting (NEW!)

#### Quick Start
```bash
# Test daily posting (dry run)
python3 daily_poster.py --dry-run

# Test the feature
python3 test_daily_posting.py

# Post daily content once
python3 daily_poster.py
```

The application will:
1. **Regular mode**: Check for new posts in the RSS feed every 15 minutes
2. **Daily mode**: Generate and post engaging content manually when you run the script
3. Log all activities and any errors that occur

## Logging

The application logs all activities to the console with timestamps. You can monitor the application's activity and troubleshoot any issues through these logs.

## Contributing

Feel free to submit issues and enhancement requests! 