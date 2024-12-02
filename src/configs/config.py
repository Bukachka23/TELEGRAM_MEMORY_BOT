"""
Configuration settings for the Telegram AI Translation Bot.

This module handles the loading and validation of environment variables required
for the bot's operation. It utilizes Pydantic's BaseSettings for configuration management.
"""

from pydantic_settings import BaseSettings
from pydantic import Field
import json
import os
from dotenv import load_dotenv
from typing import Optional, Dict

load_dotenv()


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    BOT_TOKEN: str = Field(...)
    SHEET_ID: str = Field(...)
    GOOGLE_CREDENTIALS: str = Field(...)
    SHEET_URL: str = Field(...)

    class Config:
        """
        Configuration for Pydantic settings.

        Specifies the environment file and its encoding.
        """
        env_file = '../../.env'
        env_file_encoding = 'utf-8'

    @classmethod
    def parse_gcloud_info(cls) -> Optional[Dict]:
        """
        Parse the Google Cloud Service Account Information from environment variables.

        Returns:
            Optional[Dict]: Parsed service account information if available and valid, else None.
        """
        gcloud_info = os.getenv('GCLOUD_SR_SERVICE_ACCOUNT_INFO')
        if gcloud_info:
            try:
                return json.loads(gcloud_info)
            except json.JSONDecodeError:
                print("Warning: Invalid JSON in GCLOUD_SR_SERVICE_ACCOUNT_INFO")
        return None


settings = Settings()
