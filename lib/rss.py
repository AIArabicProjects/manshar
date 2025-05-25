import feedparser
from config import rss as rss_config
from urllib.parse import urlparse

class ErrInvalidFeedURL(Exception):
    pass


class ErrEmptyFeed(Exception):
    pass


def fetch_latest_article():   
    if not rss_config.feed_url:
        raise ErrInvalidFeedURL("Feed URL is not set")
    
    feed = feedparser.parse(rss_config.feed_url)
    if not feed.entries:
        raise ErrEmptyFeed("Feed is empty")
    
    entry = feed.entries[0]
    title = entry.get("title", "")
    link = entry.get("link", "")
    content = entry.get("content", [{}])[0].get("value", "") or entry.get("summary", "")
    return {
        "id": get_slug_from_link(link),
        "title": title, 
        "content": content,
        "link": link
    }

def get_slug_from_link(link):
    path = urlparse(link).path
    # Split and filter out empty segments
    segments = [segment for segment in path.split("/") if segment]
    return segments[-1] if segments else None

# Example usage:
if __name__ == "__main__":
    article = fetch_latest_article()
    if article:
        print("Title:", article["title"])        
    else:
        print("No articles found.")
