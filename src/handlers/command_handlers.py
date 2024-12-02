import asyncio
import logging
import random
from datetime import datetime, timezone
from typing import Dict

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from src.configs.base import TextMessages, Quiz, Status
from src.utils.utils import DataStorage


class TelegramBot:
    def __init__(self, token: str, storage: DataStorage, sheet_url: str):
        self.token = token
        self.storage = storage
        self.sheet_url = sheet_url
        self.app = Application.builder().token(token).build()
        self.logger = logging.getLogger(__name__)
        self.user_ids = set()
        self.quiz_answers: Dict[int, str] = {}
        self.active_quizzes = {}

    async def setup(self) -> None:
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_quiz_answer), group=0)
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message), group=1)
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(CommandHandler("sheet", self.sheet_command))

        job_queue = self.app.job_queue
        job_queue.run_repeating(self.send_quiz, interval=15, first=0)

    async def sheet_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [[InlineKeyboardButton("View Google Sheet", url=self.sheet_url)]]
        await update.message.reply_text("Click the button below to view the Google Sheet.", reply_markup=InlineKeyboardMarkup(keyboard))

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        self.user_ids.add(user_id)
        self.active_quizzes[user_id] = False
        await update.message.reply_text(TextMessages.WELCOME)

    @staticmethod
    async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(TextMessages.HELP)

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        self.user_ids.add(user_id)

        text = update.message.text
        if ' - ' in text:
            word, translation = map(str.strip, text.split('-', 1))
            data = {
                'id': str(update.message.message_id),
                'word': word,
                'translation': translation,
                'transcription': '',
                'created_at': datetime.now(timezone.utc),
                'updated_at': datetime.now(timezone.utc),
            }
            success = await self.storage.save_data(data)
            if success:
                await update.message.reply_text(Status.SUCCESS)
            else:
                await update.message.reply_text(Status.FAILED)
        else:
            await update.message.reply_text(TextMessages.DESCRIPTION)

    async def send_quiz(self, context: ContextTypes.DEFAULT_TYPE):
        self.logger.info("Sending quiz to users.")

        if not self.user_ids:
            self.logger.warning("No users to send the quiz to.")
            return

        entries = await self.storage.retrieve_data(query={'limit': 10})
        if len(entries) < 3:
            self.logger.warning("Not enough entries to generate a quiz.")
            return

        for user_id in self.user_ids:
            if self.active_quizzes.get(user_id, False):
                self.logger.info(f"User {user_id} already has an active quiz. Skipping.")
                continue

            entry = random.choice(entries)
            wrong_entries_list = [e for e in entries if e != entry]
            number_of_wrong_entries = min(2, len(wrong_entries_list))

            if number_of_wrong_entries < 2:
                self.logger.warning("Not enough wrong entries to generate quiz options for user %s.", user_id)
                continue

            wrong_entries = random.sample(wrong_entries_list, number_of_wrong_entries)
            options = [entry.translation] + [e.translation for e in wrong_entries]
            random.shuffle(options)

            question = Quiz.QUESTION.format(word=entry.word)
            for idx, option in enumerate(options, 1):
                question += f"{idx}. {option}\n"

            self.quiz_answers[user_id] = entry.translation.lower()
            self.active_quizzes[user_id] = True
            await self.app.bot.send_message(chat_id=user_id, text=question)

    async def handle_quiz_answer(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        if user_id not in self.quiz_answers:
            return

        user_answer = update.message.text.strip().lower()
        correct_answer = self.quiz_answers.get(user_id)

        if correct_answer is None:
            await update.message.reply_text(Status.NO_ACTIVE_CHAT)
            return

        if user_answer == correct_answer:
            await update.message.reply_text(Status.CORRECT)
        else:
            await update.message.reply_text(Quiz.INCORRECT.format(correct_answer=correct_answer))

        del self.quiz_answers[user_id]
        self.active_quizzes[user_id] = False

    async def run(self) -> None:
        await self.setup()
        await self.app.initialize()
        await self.app.start()
        await self.app.updater.start_polling()
        await asyncio.Event().wait()
        await self.app.updater.stop()
        await self.app.stop()
        await self.app.shutdown()
