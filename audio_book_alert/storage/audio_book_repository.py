import json
from os import path
from pathlib import Path
from typing import List

from audio_book_alert.storage.audio_book import AudioBook
from audio_book_alert.storage import file_utils

AUDIO_BOOK_FILE = path.join(Path.home(), '.audio_book_alert/audio_books.json')


def get_all_audio_books() -> List[AudioBook]:
    if _save_file_exists():
        return _read_audio_books_from_file()
    else:
        return []


def get_all_audio_book_links() -> List[str]:
    if _save_file_exists():
        with open(AUDIO_BOOK_FILE, 'r') as audio_book_file:
            audio_book_lines: List[str] = audio_book_file.readlines()
            audio_book_links: List[str] = [json.loads(audio_book_line)['link'] for audio_book_line in audio_book_lines]
            return audio_book_links
    else:
        return []


def _read_audio_books_from_file() -> List[AudioBook]:
    with open(AUDIO_BOOK_FILE, 'r') as audio_book_file:
        audio_book_lines: List[str] = audio_book_file.readlines()
        audio_books: List[AudioBook] = []
        for audio_book_dict in audio_book_lines:
            audio_book: AudioBook = AudioBook(**json.loads(audio_book_dict))
            audio_books.append(audio_book)

        return audio_books


def save_audio_books(audio_books: List[AudioBook]) -> None:
    was_file_created: bool = file_utils.make_sure_file_exists(AUDIO_BOOK_FILE)
    with open(AUDIO_BOOK_FILE, 'a') as audio_book_file:
        if not was_file_created:
            audio_book_file.write('\n')
        serialized_audio_books = _serialize_audio_books(audio_books)
        file_content = '\n'.join(serialized_audio_books)
        audio_book_file.writelines(file_content)


def _serialize_audio_books(audio_books: List[AudioBook]) -> List[str]:
    serialized_audio_books: List[str] = []
    for audio_book in audio_books:
        serialized_audio_books.append(json.dumps(audio_book.__dict__))
    return serialized_audio_books


def _save_file_exists() -> bool:
    return path.isfile(AUDIO_BOOK_FILE)
