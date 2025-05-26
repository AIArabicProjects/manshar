from telegram import Bot
from telegram.error import TelegramError
import asyncio

class Client:
    def __init__(self, config):
        """
        Initialize the Telegram client.
        :param config: Configuration object containing bot_token and chat_id
        """
        self.bot = Bot(token=config.bot_token)
        self.chat_id = config.chat_id

    async def _send_message(self, message, link=None):
        """
        Internal async method to send a message
        """
        full_message = message
        if link:
            full_message = f"{message}\n\n{link}"
        
        return await self.bot.send_message(
            chat_id=self.chat_id,
            text=full_message,
            parse_mode='HTML'
        )

    def send(self, message, link=None, dry_run=False):
        """
        Send a message to the configured Telegram chat.
        :param message: The text message to send
        :param link: (Optional) A URL to include in the message
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
            
            response = loop.run_until_complete(self._send_message(message, link))
            return response
        except TelegramError as e:
            raise Exception(f"Failed to send Telegram message: {str(e)}") 