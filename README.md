# Telegram Quiz&Word Memory Bot 


# Introduction
The Telegram Quiz Bot is a Python-based Telegram bot that helps users learn new words and their translations. Users can send words along with their translations to the bot, which are then saved to a Google Sheet. The bot periodically quizzes users on the words they've submitted, ensuring an interactive learning experience.

# Features
- **Word Submission**: Users can submit words and their translations in the format `word - translation`.
- **Data Storage**: Submissions are saved to a Google Sheet for persistence.
- **Periodic Quizzes**: The bot sends periodic quizzes to users based on the submitted words.
- **Active Quiz Tracking**: Users won't receive a new quiz until they've answered the current one.
- **Inline Keyboard Support**: Users can access the Google Sheet directly via an inline keyboard button.
- **Command Handling**: Supports `/start`, `/help`, and `/sheet` commands.

# Architecture
The bot is built using the `python-telegram-bot` library and follows an asynchronous programming model with `asyncio`. It integrates with the Google Sheets API to store and retrieve data.

# Setup Instructions

## Prerequisites
- Python 3.11 or higher
- Telegram Bot API Token (from BotFather)
- Google Cloud Service Account with access to Google Sheets API
- Google Sheet ID where the data will be stored

## .env Variables
```bash
BOT_TOKEN=your_telegram_bot_token
GOOGLE_CREDENTIALS='your_google_service_account_credentials_json'
SHEET_ID=your_google_sheet_id
SHEET_URL=https://docs.google.com/spreadsheets/d/your_google_sheet_id/edit#gid=0
```

## Installation

### Clone the Repository
```bash
git clone https://github.com/yourusername/telegram-quiz-bot.git
cd telegram-quiz-bot
