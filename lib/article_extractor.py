import requests
from bs4 import BeautifulSoup
import re


class ErrInvalidURL(Exception):
    pass


class ErrFailedToExtract(Exception):
    pass


def extract_article_content(url):
    """
    Extract article content from URL
    
    :param url: URL of the article to extract content from
    :return: Dictionary with title and content
    :raises ErrInvalidURL: If URL is invalid or inaccessible
    :raises ErrFailedToExtract: If content extraction fails
    """
    if not url or not url.startswith(('http://', 'https://')):
        raise ErrInvalidURL("Invalid URL provided")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "header", "footer", "aside"]):
            script.decompose()
        
        # Try to find the main content
        content = ""
        title = ""
        
        # Get title
        title_tag = soup.find('title')
        if title_tag:
            title = title_tag.get_text().strip()
        
        # Try different selectors for article content
        article_selectors = [
            'article',
            '[role="main"]',
            '.article-content',
            '.post-content',
            '.entry-content',
            '.content',
            '.main-content',
            '.article-body',
            '.post-body',
            '.story-body',
            'main'
        ]
        
        for selector in article_selectors:
            article = soup.select_one(selector)
            if article:
                content = article.get_text()
                break
        
        # If no specific article content found, try to get content from paragraphs
        if not content:
            paragraphs = soup.find_all('p')
            if paragraphs:
                content = ' '.join([p.get_text() for p in paragraphs])
        
        # If still no content, get all text from body
        if not content:
            body = soup.find('body')
            if body:
                content = body.get_text()
        
        if not content:
            raise ErrFailedToExtract("No content found in the article")
        
        # Clean up the text
        content = re.sub(r'\s+', ' ', content).strip()
        
        # Limit content to avoid token limits (8000 characters should be enough)
        if len(content) > 8000:
            content = content[:8000]
        
        return {
            'title': title,
            'content': content,
            'url': url
        }
        
    except requests.exceptions.RequestException as e:
        raise ErrInvalidURL(f"Failed to fetch URL: {str(e)}")
    except Exception as e:
        raise ErrFailedToExtract(f"Failed to extract article content: {str(e)}")


def extract_article_metadata(url):
    """
    Extract article metadata including title, description, and image
    
    :param url: URL of the article
    :return: Dictionary with metadata
    """
    if not url or not url.startswith(('http://', 'https://')):
        raise ErrInvalidURL("Invalid URL provided")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        metadata = {
            'title': '',
            'description': '',
            'image': '',
            'author': '',
            'publish_date': '',
            'url': url
        }
        
        # Extract title
        title_tag = soup.find('title')
        if title_tag:
            metadata['title'] = title_tag.get_text().strip()
        
        # Try to get Open Graph title
        og_title = soup.find('meta', property='og:title')
        if og_title and og_title.get('content'):
            metadata['title'] = og_title['content']
        
        # Extract description
        description_tag = soup.find('meta', attrs={'name': 'description'})
        if description_tag and description_tag.get('content'):
            metadata['description'] = description_tag['content']
        
        # Try to get Open Graph description
        og_description = soup.find('meta', property='og:description')
        if og_description and og_description.get('content'):
            metadata['description'] = og_description['content']
        
        # Extract image
        og_image = soup.find('meta', property='og:image')
        if og_image and og_image.get('content'):
            metadata['image'] = og_image['content']
        
        # Try to find article image if no og:image
        if not metadata['image']:
            img_tag = soup.find('img')
            if img_tag and img_tag.get('src'):
                metadata['image'] = img_tag['src']
        
        # Extract author
        author_tag = soup.find('meta', attrs={'name': 'author'})
        if author_tag and author_tag.get('content'):
            metadata['author'] = author_tag['content']
        
        # Try to find author in article
        if not metadata['author']:
            author_selectors = ['.author', '.byline', '[rel="author"]']
            for selector in author_selectors:
                author_elem = soup.select_one(selector)
                if author_elem:
                    metadata['author'] = author_elem.get_text().strip()
                    break
        
        # Extract publish date
        date_tag = soup.find('meta', property='article:published_time')
        if date_tag and date_tag.get('content'):
            metadata['publish_date'] = date_tag['content']
        
        # Try to find date in time tags
        if not metadata['publish_date']:
            time_tag = soup.find('time')
            if time_tag:
                if time_tag.get('datetime'):
                    metadata['publish_date'] = time_tag['datetime']
                else:
                    metadata['publish_date'] = time_tag.get_text().strip()
        
        return metadata
        
    except requests.exceptions.RequestException as e:
        raise ErrInvalidURL(f"Failed to fetch URL: {str(e)}")
    except Exception as e:
        raise ErrFailedToExtract(f"Failed to extract article metadata: {str(e)}")


def is_valid_article_url(url):
    """
    Check if a URL is likely to be a valid article URL
    
    :param url: URL to validate
    :return: Boolean indicating if URL is valid
    """
    if not url or not url.startswith(('http://', 'https://')):
        return False
    
    # Basic URL validation
    try:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        return bool(parsed.netloc and parsed.scheme)
    except:
        return False


# Example usage:
if __name__ == "__main__":
    test_url = "https://example.com/article"
    
    try:
        content = extract_article_content(test_url)
        print("Title:", content["title"])
        print("Content length:", len(content["content"]))
        print("Content preview:", content["content"][:200] + "...")
        
        metadata = extract_article_metadata(test_url)
        print("\nMetadata:")
        for key, value in metadata.items():
            print(f"{key}: {value}")
            
    except (ErrInvalidURL, ErrFailedToExtract) as e:
        print(f"Error: {str(e)}") 