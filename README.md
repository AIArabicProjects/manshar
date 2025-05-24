# Social Media Queue

A Python application that automatically publishes new blog posts from an RSS feed to various social media platforms (Twitter, Facebook, Telegram, and LinkedIn).

## Features

- Monitors RSS feed for new posts
- Automatically publishes to Twitter, Facebook, Telegram, and LinkedIn
- Error handling and logging
- Prevents duplicate posts

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
git clone <repository-url>
cd social-queue
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

Run the application:
```bash
python main.py
```

The application will:
1. Check for new posts in the RSS feed every 15 minutes
2. Publish new posts to configured social media platforms
3. Log all activities and any errors that occur

## Logging

The application logs all activities to the console with timestamps. You can monitor the application's activity and troubleshoot any issues through these logs.

## Contributing

Feel free to submit issues and enhancement requests! 