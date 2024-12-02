import asyncio
import json

from google.oauth2 import service_account

from src.configs.config import settings
from src.google_sheets.sheets import GoogleSheets
from src.handlers.command_handlers import TelegramBot


class BotApplication:
    def __init__(self, token: str):
        self.token = token
        self.sheets_handler = None
        self.bot_handler = None

    async def initialize(self) -> None:
        if isinstance(settings.GOOGLE_CREDENTIALS, str):
            credentials_dict = json.loads(settings.GOOGLE_CREDENTIALS)
        else:
            credentials_dict = settings.GOOGLE_CREDENTIALS

        google_credentials = service_account.Credentials.from_service_account_info(credentials_dict)

        self.sheets_handler = GoogleSheets(sheet_id=settings.SHEET_ID, credentials=google_credentials)
        await self.sheets_handler.connect()
        self.bot_handler = TelegramBot(token=self.token, storage=self.sheets_handler, sheet_url=settings.SHEET_URL)
        await self.bot_handler.setup()

    async def run(self) -> None:
        await self.initialize()
        await self.bot_handler.run()


if __name__ == "__main__":
    app = BotApplication(settings.BOT_TOKEN)
    asyncio.run(app.run())
