from typing import List

from sqlalchemy.exc import IntegrityError

from audio_book_alert.alert.storage.telegram_subscription import TelegramSubscription
from audio_book_alert.database.orm import SessionLocal


class TelegramSubscriptionRepository:
    def __init__(self, db_session: SessionLocal):
        self.db_session = db_session

    def subscribe_user(self, telegram_subscription: TelegramSubscription) -> bool:
        try:
            self.db_session.add(telegram_subscription)
            self.db_session.commit()
            return True
        except IntegrityError:
            return False

    def get_all_subscribers_chat_ids(self) -> List[int]:
        chat_id_tuple = self.db_session.query(TelegramSubscription.chat_id).all()
        return [chat_id[0] for chat_id in chat_id_tuple]
