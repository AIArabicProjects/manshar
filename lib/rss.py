import feedparser
from config import rss as rss_config
from urllib.parse import urlparse
from bs4 import BeautifulSoup

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
    
    # Extract cover image from HTML content
    cover_image = None
    if content:
        soup = BeautifulSoup(content, 'html.parser')
        # Try to find the first image in the content
        img = soup.find('img')
        if img:
            # Try to get the full-size image URL first
            if img.get('srcset'):
                # Get the largest image from srcset
                srcset = img['srcset'].split(',')
                largest_image = srcset[-1].strip().split(' ')[0]
                cover_image = largest_image
            # Fall back to src if no srcset
            elif img.get('src'):
                cover_image = img.get('src')
    
    # If no image found in content, try other methods
    if not cover_image:
        # Try to get image from media:content
        if hasattr(entry, 'media_content'):
            for media in entry.media_content:
                if media.get('type', '').startswith('image/'):
                    cover_image = media.get('url')
                    break
        
        # Try to get image from enclosure
        if not cover_image and hasattr(entry, 'enclosures'):
            for enclosure in entry.enclosures:
                if enclosure.get('type', '').startswith('image/'):
                    cover_image = enclosure.get('href')
                    break
        
        # Try to get image from image tag
        if not cover_image and hasattr(entry, 'image'):
            cover_image = entry.image.get('href')
    
    return {
        "id": get_slug_from_link(link),
        "title": title, 
        "content": content,
        "link": link,
        "cover_image": cover_image
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
