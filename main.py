import lib.rss
import lib.summarizer
import lib.logger
from clients.facebook.client import Client as FacebookClient
from clients.x.client import Client as XClient
from clients.linkedin.client import Client as LinkedinClient
from clients.telegram.client import Client as TelegramClient

from config import facebook as facebook_config
from config import x as x_config
from config import linkedin as linkedin_config
from config import telegram as telegram_config

logger = lib.logger.get_logger(__name__)

def read_history(filename="history.txt"):
    try:
        with open(filename, "r") as f:
            return set(line.strip() for line in f if line.strip())
    except FileNotFoundError:
        return set()

def post_to_social_media(article, dry_run=False):
    """
    Post article to all configured social media platforms
    """
    message = f"{article['title']}\n\n{article['link']}"
    
    # Post to Facebook
    try:
        fb_client = FacebookClient(facebook_config)
        response = fb_client.send(message, link=article["link"], image_url=article["cover_image"], dry_run=dry_run)
        logger.info(f"Facebook post successful: {response}")
    except Exception as e:
        logger.error(f"Failed to post to Facebook: {str(e)}")

    # Post to X (Twitter)
    try:
        x_client = XClient(x_config)
        response = x_client.send(message, image_url=article["cover_image"], dry_run=dry_run)
        logger.info(f"X post successful: {response}")
    except Exception as e:
        logger.error(f"Failed to post to X: {str(e)}")   

    # Post to Telegram
    try:
        telegram_client = TelegramClient(telegram_config)
        response = telegram_client.send(message, link=article["link"], image_url=article["cover_image"], dry_run=dry_run)
        logger.info(f"Telegram post successful: {response}")
    except Exception as e:
        logger.error(f"Failed to post to Telegram: {str(e)}")

def update_history(article_id, filename="history.txt"):
    """
    Update the history file with the posted article ID
    """
    try:
        with open(filename, "a") as f:
            f.write(article_id + "\n")
        logger.info(f"Updated history with article ID: {article_id}")
    except Exception as e:
        logger.error(f"Failed to update history: {str(e)}")

if __name__ == "__main__":
    try:
        # Fetch the latest article
        article = lib.rss.fetch_latest_article()
        logger.info(f"Fetched article: {article['title']}")
        
        # Check if article was already posted
        history = read_history()
        if article["id"] in history:
            logger.info(f"Article already posted: {article['id']}")
            exit(0)
        
        # Post to social media
        post_to_social_media(article)
        
        # Update history
        update_history(article["id"])
        
        logger.info(f"Successfully published article {article['id']}")
        
    except Exception as e:
        logger.error(f"Error in main process: {str(e)}")
        raise