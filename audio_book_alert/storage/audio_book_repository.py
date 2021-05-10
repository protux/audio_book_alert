from typing import List

from audio_book_alert.database.orm import SessionLocal
from audio_book_alert.storage.audio_book import AudioBook


class AudioBookRepository:
    def __init__(self, db_session: SessionLocal):
        self.db_session = db_session

    def get_all_audio_books(self) -> List[AudioBook]:
        return self.db_session.query(AudioBook).all()

    def get_all_audio_book_links(self) -> List[str]:
        return self.db_session.query(AudioBook.link).all()

    def save_audio_books(self, audio_books: List[AudioBook]) -> None:
        with self.db_session.begin():
            self.db_session.add_all(audio_books)
