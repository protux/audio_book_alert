import json
from os import path
from pathlib import Path
from typing import List

from audio_book_alert.storage.audio_book import AudioBook
from audio_book_alert.storage import file_utils

AUDIO_BOOK_FILE = path.join(Path.home(), ".audio_book_alert/audio_books.json")


def get_all_audio_books() -> List[AudioBook]:
    if _save_file_exists():
        return _read_audio_books_from_file()
    else:
        return []


def _read_audio_books_from_file() -> List[AudioBook]:
    with open(AUDIO_BOOK_FILE, "r") as audio_book_file:
        audio_book_lines: List[str] = audio_book_file.readlines()
        audio_books: List[AudioBook] = []
        for audio_book_dict in audio_book_lines:
            audio_book: AudioBook = AudioBook(**json.loads(audio_book_dict))
            audio_books.append(audio_book)

        return audio_books


def _save_file_exists() -> bool:
    return path.isfile(AUDIO_BOOK_FILE)
