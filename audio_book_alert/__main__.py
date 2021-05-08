import sys
from typing import List

from audio_book_alert.alert import telegram_bot
from audio_book_alert.scraper import (
    scraper,
    filter,
)
from audio_book_alert.storage import audio_book_repository
from audio_book_alert.storage.audio_book import AudioBook
from audio_book_alert.alert import send_alert
from audio_book_alert.scraper import parser_config


def parse_audio_books() -> None:
    audio_books: List[AudioBook] = []

    for author in parser_config.authors:
        audio_books += scraper.find_titles_by_author(author.strip())
    for narrator in parser_config.narrators:
        audio_books += scraper.find_titles_by_narrator(narrator.strip())

    past_audio_books = audio_book_repository.get_all_audio_books()
    filtered_audio_books = filter.filter_audio_books(audio_books, past_audio_books)
    audio_book_repository.save_audio_books(filtered_audio_books)
    send_alert.send_alert(filtered_audio_books)


def start_telegram_bot() -> None:
    telegram_bot.start_bot()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--bot-mode":
        start_telegram_bot()
    else:
        parse_audio_books()
