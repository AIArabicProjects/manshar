import re
from bs4 import BeautifulSoup
import html

def clean_html(html_content):
    """Clean HTML content by removing tags and decoding HTML entities."""
    # Remove HTML tags
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text()
    # Decode HTML entities
    text = html.unescape(text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def summarize(content, max_length=140):
    """
    Summarize RSS feed content into a specified number of characters.
    
    Args:
        content (str): The RSS feed content
        max_length (int): Maximum length of the summary (default: 140)
    
    Returns:
        str: Summarized content
    """
    # Clean the content
    clean_text = clean_html(content)
    
    # If text is already shorter than max_length, return it
    if len(clean_text) <= max_length:
        return clean_text
    
    # Find the last complete word within max_length
    summary = clean_text[:max_length]
    last_space = summary.rfind(' ')
    
    if last_space > 0:
        summary = summary[:last_space]
    
    return summary + '...'