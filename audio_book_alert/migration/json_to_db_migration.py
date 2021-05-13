from typing import List

from audio_book_alert.database.orm import (
    get_db,
    SessionLocal,
)
from audio_book_alert.alert.storage.telegram_subscription_repository import TelegramSubscriptionRepository
from audio_book_alert.alert.storage.telegram_subscription import TelegramSubscription
from audio_book_alert.migration import subscription_reader
from audio_book_alert.storage.audio_book_repository import AudioBookRepository
from audio_book_alert.storage.audio_book import AudioBook
from audio_book_alert.storage import audio_book_file_repository


def migrate_json_to_database():
    db_session: SessionLocal = get_db()
    _migrate_subscribers(db_session)
    _migrate_audio_books(db_session)


def _migrate_subscribers(db_session: SessionLocal):
    subscribers = subscription_reader.read_subscribers_from_file()
    telegram_subscription_repository: TelegramSubscriptionRepository = TelegramSubscriptionRepository(
        db_session
    )

    for subscriber in subscribers:
        telegram_subscription: TelegramSubscription = TelegramSubscription(
            user_id=subscriber['user_id'],
            chat_id=subscriber['chat_id'],
            language=subscriber['language']
        )
        telegram_subscription_repository.subscribe_user(telegram_subscription)


def _migrate_audio_books(db_session: SessionLocal):
    audio_book_repository: AudioBookRepository = AudioBookRepository(db_session)
    audio_books: List[AudioBook] = audio_book_file_repository.get_all_audio_books()
    audio_book_repository.save_audio_books(audio_books)
