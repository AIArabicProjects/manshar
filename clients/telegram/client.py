from telegram import Bot
from telegram.error import TelegramError
import asyncio
import requests
from io import BytesIO
import mimetypes

class Client:
    def __init__(self, config):
        """
        Initialize the Telegram client.
        :param config: Configuration object containing bot_token and chat_id
        """
        self.bot = Bot(token=config.bot_token)
        self.chat_id = config.chat_id

    async def _send_message(self, message, link=None, image_url=None):
        """
        Internal async method to send a message
        """
        full_message = message
        if link:
            full_message = f"{message}\n\n{link}"
        
        if image_url:
            try:
                # Download the image with proper headers
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                response = requests.get(image_url, headers=headers)
                response.raise_for_status()
                
                # Create a temporary file-like object
                image_data = BytesIO(response.content)
                
                # Send photo with caption
                return await self.bot.send_photo(
                    chat_id=self.chat_id,
                    photo=image_data,
                    caption=full_message,
                    parse_mode='HTML'
                )
            except Exception as e:
                print(f"Error uploading image to Telegram: {str(e)}")
                # Fall back to text-only message if image upload fails
                return await self.bot.send_message(
                    chat_id=self.chat_id,
                    text=full_message,
                    parse_mode='HTML'
                )
        else:
            # Send text only
            return await self.bot.send_message(
                chat_id=self.chat_id,
                text=full_message,
                parse_mode='HTML'
            )

    def send(self, message, link=None, image_url=None, dry_run=False):
        """
        Send a message to the configured Telegram chat.
        :param message: The text message to send
        :param link: (Optional) A URL to include in the message
        :param image_url: (Optional) URL of the image to attach
        :param dry_run: (Optional) If True, the message will not be sent.
        :return: The response from the Telegram API
        """
        if dry_run:
            return {"id": "dry_run"}
        
        try:
            # Run the async function in an event loop
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            response = loop.run_until_complete(self._send_message(message, link, image_url))
            return response
        except TelegramError as e:
            raise Exception(f"Failed to send Telegram message: {str(e)}") 