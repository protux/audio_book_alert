from sqlalchemy import (
    Column,
    Integer,
    String,
)

from audio_book_alert.database.orm import Base


class TelegramSubscription(Base):
    __tablename__ = "telegram_subscriptions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    chat_id = Column(Integer, nullable=False, unique=True)
    language = Column(String, nullable=False)
