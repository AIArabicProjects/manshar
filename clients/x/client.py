import tweepy

class Client:
    def __init__(self, config):        
        self.client = tweepy.Client(
            consumer_key=config.api_key,
            consumer_secret=config.api_secret,
            access_token=config.access_token,
            access_token_secret=config.access_token_secret
        )  

    def send(self, message, dry_run=False):
        if dry_run:
            return {"id": "dry_run"}
        
        response = self.client.create_tweet(text=message)
        return response
