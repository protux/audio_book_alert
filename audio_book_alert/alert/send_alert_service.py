from typing import List, Callable

from audio_book_alert.alert import alert_serializer
from audio_book_alert.alert import (
    telegram_bot,
)
from audio_book_alert.alert.storage.telegram_subscription_repository import (
    TelegramSubscriptionRepository,
)
from audio_book_alert.database.orm import SessionLocal
from audio_book_alert.storage.audio_book import AudioBook


class SendAlertService:
    def __init__(self, db_session: SessionLocal, telegram_bot: Callable = telegram_bot):
        self.telegram_subscription_repository: TelegramSubscriptionRepository = (
            TelegramSubscriptionRepository(db_session)
        )
        self.telegram_bot = telegram_bot

    def send_alert(self, audio_books: List[AudioBook]) -> None:
        if audio_books:
            subscriber_chat_ids = (
                self.telegram_subscription_repository.get_all_subscribers_chat_ids()
            )
            serialized_audio_books = (
                alert_serializer.serialize_all_audio_books_human_readable(audio_books)
            )
            self.telegram_bot.send_message(serialized_audio_books, subscriber_chat_ids)
