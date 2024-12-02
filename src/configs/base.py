from dataclasses import dataclass
from datetime import datetime


@dataclass
class SheetEntry:
    id: str
    word: str
    translation: str
    created_at: datetime
    updated_at: datetime


@dataclass
class Status:
    SUCCESS: str = "Saved word '{word}' with translation '{translation}'."
    FAILED: str = "Failed to save data."
    CORRECT: str = "Correct!"
    NO_ACTIVE_CHAT: str = "You have no active quiz."


@dataclass
class TextMessages:
    WELCOME: str = "Welcome! Send me a word and its translation."
    HELP: str = "To use this bot, send a word and its translation in the format 'word - translation'."
    DESCRIPTION: str = "Please send the word and translation in the format 'word - translation'."


@dataclass
class Quiz:
    QUESTION: str = "What is the translation for '{word}'?\nOptions:\n"
    INCORRECT: str = "Incorrect. The correct answer was '{correct_answer}'."
