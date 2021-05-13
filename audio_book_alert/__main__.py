import sys
from typing import List

from audio_book_alert.alert import telegram_bot
from audio_book_alert.alert.send_alert_service import SendAlertService
from audio_book_alert.database.orm import get_db
from audio_book_alert.migration import json_to_db_migration
from audio_book_alert.scraper import parser_config
from audio_book_alert.scraper import (
    scraper,
    filter,
)
from audio_book_alert.storage.audio_book import AudioBook
from audio_book_alert.storage.audio_book_repository import AudioBookRepository


def start_telegram_bot() -> None:
    telegram_bot.start_bot()


def parse_audio_books() -> None:
    db_session = get_db()
    audio_books: List[AudioBook] = []

    for author in parser_config.authors:
        audio_books += scraper.find_titles_by_author(author.strip())
    for narrator in parser_config.narrators:
        audio_books += scraper.find_titles_by_narrator(narrator.strip())

    audio_book_repository: AudioBookRepository = AudioBookRepository(db_session)
    past_audio_books: List[AudioBook] = audio_book_repository.get_all_audio_books()
    filtered_audio_books: List[AudioBook] = filter.filter_audio_books(
        audio_books, past_audio_books
    )
    audio_book_repository.save_audio_books(filtered_audio_books)
    SendAlertService(db_session).send_alert(filtered_audio_books)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--bot-mode":
            start_telegram_bot()
        elif sys.argv[1] == "--migrate":
            json_to_db_migration.migrate_json_to_database()
    else:
        parse_audio_books()
    print("Unknown parameters parsed.")
