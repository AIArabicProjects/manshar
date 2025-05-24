import tweepy

class Client:
    def __init__(self, config):        
        self.client = tweepy.Client(
            consumer_key=config.api_key,
            consumer_secret=config.api_secret,
            access_token=config.access_token,
            access_token_secret=config.access_token_secret
        )  

    def send(self, message):
        response = self.client.create_tweet(text=message)
        return response
