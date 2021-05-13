from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
)
from sqlalchemy.sql import func

from audio_book_alert.database.orm import Base


class AudioBook(Base):
    __tablename__ = "audio_books"

    id: Column = Column(Integer, primary_key=True, autoincrement=True)
    title: Column = Column(String, nullable=False)
    subtitle: Column = Column(String)
    author: Column = Column(String, nullable=False)
    reader: Column = Column(String, nullable=False)
    play_time: Column = Column(String)
    release_date: Column = Column(String)
    language: Column = Column(String)
    link: Column = Column(String, nullable=False, unique=True)
    time_added = Column(DateTime, nullable=False, server_default=func.now())

    def __hash__(self):
        return hash(self.title + self.author + self.play_time)

    def __eq__(self, other):
        if not isinstance(other, AudioBook):
            return False

        if other.title != self.title:
            return False

        if other.author != self.author:
            return False

        if other.play_time != self.play_time:
            return False

        return True
