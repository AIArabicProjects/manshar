import tweepy
import requests
from io import BytesIO
import mimetypes
import os

class Client:
    def __init__(self, config):        
        self.client = tweepy.Client(
            consumer_key=config.api_key,
            consumer_secret=config.api_secret,
            access_token=config.access_token,
            access_token_secret=config.access_token_secret
        )
        # Create API v1.1 instance for media upload
        auth = tweepy.OAuth1UserHandler(
            config.api_key, config.api_secret,
            config.access_token, config.access_token_secret
        )
        self.api = tweepy.API(auth)

    def send(self, message, image_url=None, dry_run=False):
        if dry_run:
            return {"id": "dry_run"}
        
        media_ids = []
        if image_url:
            try:
                # Download the image with proper headers
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                response = requests.get(image_url, headers=headers)
                response.raise_for_status()
                
                # Get the content type and extension
                content_type = response.headers.get('content-type', '')
                ext = mimetypes.guess_extension(content_type) or '.jpg'
                
                # Create a temporary file-like object
                image_data = BytesIO(response.content)
                
                # Upload the image with proper filename and content type
                media = self.api.media_upload(
                    filename=f"image{ext}",
                    file=image_data,
                    media_category='tweet_image'
                )
                media_ids.append(media.media_id)
            except Exception as e:
                print(f"Error uploading image to Twitter: {str(e)}")
                # Don't include media_ids if upload failed
                media_ids = []
        
        # Only include media_ids in the tweet if we have them
        if media_ids:
            response = self.client.create_tweet(text=message, media_ids=media_ids)
        else:
            response = self.client.create_tweet(text=message)
            
        return response
