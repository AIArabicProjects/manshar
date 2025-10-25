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

## Renewing Facebook Access Token

Facebook access tokens expire periodically (typically after 60 days). When your token expires, you'll need to renew it to continue posting to Facebook.

The script will:
- Exchange your current token for a new long-lived token
- Check if the token is a User or Page token
- Display the new token and its expiration details
- Show which Facebook pages are accessible with this token


```bash
python scripts/renew_fb_token.py
```

After running the script, you'll see output like:
```
✅ New long-lived user token: EAAxxxxxxxxxxxxx...
✅ Page Access Token: EAAyyyyyyyyyyyyyy...
```

Copy the appropriate token and update your `config.yaml` file:
```yaml
facebook:
  access_token: YOUR_NEW_TOKEN_HERE
```

## Logging

The application logs all activities to the console with timestamps. You can monitor the application's activity and troubleshoot any issues through these logs.

## Contributing

Feel free to submit issues and enhancement requests! 