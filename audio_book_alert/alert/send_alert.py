from typing import List

from audio_book_alert.storage.audio_book import AudioBook
from audio_book_alert.alert import (
    subscription_manager,
    telegram_bot,
)


def send_alert(audio_books: List[AudioBook]) -> None:
    if audio_books:
        subscriber_ids = subscription_manager.get_all_subscriber_ids()
        serialized_audio_books = serialize_all_audio_books_human_readable(audio_books)
        telegram_bot.send_message(serialized_audio_books, subscriber_ids)


def serialize_all_audio_books_human_readable(audio_books: List[AudioBook]) -> List[str]:
    serialized_audio_books: List[str] = [serialize_audio_book_human_readable(audio_book) for audio_book in audio_books]
    serialized_audio_books[0] = \
        'Es gibt neue Hörbücher die dich interessieren könnten: \n\n' + serialized_audio_books[0]
    return serialized_audio_books


def serialize_audio_book_human_readable(audio_book: AudioBook) -> str:
    output: str = audio_book.title
    if audio_book.subtitle:
        output += '\n' + audio_book.subtitle
    output += '\n' + audio_book.author
    output += '\n' + audio_book.reader
    output += '\n' + audio_book.play_time
    output += '\n' + audio_book.release_date
    output += '\n' + audio_book.language
    output += '\n' + audio_book.link
    return output
