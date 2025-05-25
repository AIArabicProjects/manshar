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

if __name__ == "__main__":               
    article = lib.rss.fetch_latest_article()    
    
    # Read the history.txt and check if the id in the file or not
    history = read_history()
    if article["id"] in history:
        logger.info(f"already posted: {article['id']}")
        exit(0)
        
    message = f"{article['title']}\n\n{article['link']}"    
    
    fb_client = FacebookClient(facebook_config)
    response = fb_client.send(message)    
    logger.info(f"facebook response: {response}")

    x_client = XClient(x_config)
    response = x_client.send(message)
    logger.info(f"X response: {response}")

    # TODO: LinkedIn client still needs testing as the api key is not generated yet
    # linkedin_client = LinkedinClient(linkedin_config)
    # response = linkedin_client.send("Hello World! Hello AI in Arabic!", link="https://example.com")    
    # logger.info(f"linkedin response: {response}")

    # Send to Telegram
    telegram_client = TelegramClient(telegram_config)
    response = telegram_client.send(message)
    logger.info(f"telegram response: {response}")

    # append the id to the history file
    with open("history.txt", "a") as f:
        f.write(article["id"] + "\n")
    
    logger.info(f"published article {article['id']} successfully")