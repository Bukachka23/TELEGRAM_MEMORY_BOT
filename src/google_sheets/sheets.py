import logging
from datetime import datetime
from typing import Dict, Any, Optional, List

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from src.configs.base import SheetEntry
from src.utils.utils import DataStorage


class GoogleSheets(DataStorage):
    def __init__(self, credentials: Credentials, sheet_id: str):
        self.credentials = credentials
        self.sheet_id = sheet_id
        self.service = None
        self.logger = logging.getLogger(__name__)

    async def connect(self) -> bool:
        self.service = build('sheets', 'v4', credentials=self.credentials)
        self.logger.info("Connected to Google Sheets API.")
        return True

    async def save_data(self, data: Dict[str, Any]) -> bool:
        created_at = self._parse_datetime(data.get('created_at'))
        updated_at = self._parse_datetime(data.get('updated_at'))

        values = [
            [
                data.get('id', ''),
                data.get('word', ''),
                data.get('translation', ''),
                data.get('transcription', ''),
                created_at.isoformat() if created_at else '',
                updated_at.isoformat() if updated_at else '',
            ]
        ]
        body = {'values': values}
        self.service.spreadsheets().values().append(
            spreadsheetId=self.sheet_id,
            range='Sheet1!A1',
            valueInputOption='RAW',
            body=body
        ).execute()
        self.logger.info("Data saved to Google Sheets.")
        return True

    async def retrieve_data(self, query: Optional[Dict[str, Any]] = None) -> List[SheetEntry]:
        result = self.service.spreadsheets().values().get(spreadsheetId=self.sheet_id, range='Sheet1!A:F').execute()
        values = result.get('values', [])
        if not values:
            self.logger.info("No data found in Google Sheets.")
            return []

        entries = [
            SheetEntry(
                id=row[0],
                word=row[1],
                translation=row[2],
                created_at=datetime.fromisoformat(row[4]),
                updated_at=datetime.fromisoformat(row[5])
            )
            for row in values[1:]
            if len(row) >= 6
        ]
        self.logger.info("Data retrieved from Google Sheets.")
        return entries

    @staticmethod
    def _parse_datetime(value: Any) -> Optional[datetime]:
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value)
            except ValueError:
                return None
        return value
