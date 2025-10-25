# Manshar - Social Media Publishing Tool
<img src="./docs/logo.png" alt="Manshar Logo" width="200" height="auto">

A Python application that automatically publishes new blog posts from an RSS feed to various social media platforms (Twitter, Facebook, Telegram, and LinkedIn).

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

Run the application for regular article posting:
```bash
python main.py
```

## Logging

The application logs all activities to the console with timestamps. You can monitor the application's activity and troubleshoot any issues through these logs.

## Contributing

Feel free to submit issues and enhancement requests! 