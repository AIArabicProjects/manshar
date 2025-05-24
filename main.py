import lib.rss
import lib.summarizer
from clients.facebook.client import Client as FacebookClient
from clients.x.client import Client as XClient
from clients.linkedin.client import Client as LinkedinClient

from config import facebook as facebook_config
from config import x as x_config
from config import linkedin as linkedin_config

def read_history(filename="history.txt"):
    try:
        with open(filename, "r") as f:
            return set(line.strip() for line in f if line.strip())
    except FileNotFoundError:
        return set()

if __name__ == "__main__":  
    # TODO:
    # 1. Fetch the latest article
    # 2. check if it was published before in the history file
    # 3. term if it was published already
    # 4. otherwise, summarize the article
    # 5. publish on x
    # 6. publish on facebook
    # 7. publish on linkedin
    # 8. update the history file
     
    article = lib.rss.fetch_latest_article()    
    
    # Read the history.txt and check if the id in the file or not
    history = read_history()
    if article["id"] in history:
        print(f"Already posted: {article['id']}")
        exit(0)
        
    message = f"{article['title']}\n\\n{article['link']}"
    print(message)
    # fb_client = FacebookClient(facebook_config)
    # response = fb_client.send("Hello World! Hello AI in Arabic!", link="https://example.com")    

    # x_client = XClient(x_config)
    # response = x_client.send("Hello World! Hello AI in Arabic!")    

    # TODO: LinkedIn client still needs testing as the api key is not generated yet
    # linkedin_client = LinkedinClient(linkedin_config)
    # response = linkedin_client.send("Hello World! Hello AI in Arabic!", link="https://example.com")    

    # append the id to the history file
    with open("history.txt", "a") as f:
        f.write(article["id"] + "\n")
    
    
    

