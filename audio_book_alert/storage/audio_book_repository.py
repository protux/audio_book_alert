from typing import List, Tuple

from audio_book_alert.database.orm import SessionLocal
from audio_book_alert.storage.audio_book import AudioBook


class AudioBookRepository:
    def __init__(self, db_session: SessionLocal):
        self.db_session = next(db_session)

    def get_all_audio_books(self) -> List[AudioBook]:
        return self.db_session.query(AudioBook).all()

    def get_all_audio_book_links(self) -> List[str]:
        links: Tuple[str] = self.db_session.query(AudioBook.link).all()
        return [link[0] for link in links]

    def save_audio_books(self, audio_books: List[AudioBook]) -> None:
        self.db_session.add_all(audio_books)
        self.db_session.commit()
