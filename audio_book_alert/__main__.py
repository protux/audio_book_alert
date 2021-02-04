import sys
from typing import List

from audio_book_alert.alert import telegram_bot
from audio_book_alert.scraper import (
    scraper,
    filter,
)
from audio_book_alert.storage import audio_book_repository
from audio_book_alert.storage.audio_book import AudioBook


def parse_audio_books() -> None:
    audio_books: List[AudioBook] = []

    with open('author_names', 'r') as author_names:
        authors = author_names.readlines()
        for author in authors:
            audio_books += scraper.find_titles_by_author(author.strip())
    with open('narrator_names', 'r') as narrator_names_file:
        narrators = narrator_names_file.readlines()
        for narrator in narrators:
            audio_books += scraper.find_titles_by_narrator(narrator.strip())

    past_audio_books = audio_book_repository.get_all_audio_books()
    filtered_audio_books = filter.filter_audio_books(audio_books, past_audio_books)
    audio_book_repository.save_audio_books(filtered_audio_books)
    print(f'{len(filtered_audio_books)} Hörbücher gefunden')
    print()
    for audio_book in filtered_audio_books:
        print(audio_book.link)
    print()
    audio_book_links: List[str] = [audio_book.link for audio_book in filtered_audio_books]
    for audio_book_link in audio_book_links:
        if audio_book_links.count(audio_book_link) > 1:
            print(audio_book_link)
    # send_alert.send_alert(filtered_audio_books)


def start_telegram_bot() -> None:
    telegram_bot.start_bot()


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--bot-mode':
        start_telegram_bot()
    else:
        parse_audio_books()
