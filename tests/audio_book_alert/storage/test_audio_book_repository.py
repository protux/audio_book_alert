from typing import List

from pytest import fixture

from audio_book_alert.storage.audio_book import AudioBook
from audio_book_alert.storage.audio_book_repository import AudioBookRepository
from tests import test_orm


@fixture
def audio_books():
    audio_books: List[AudioBook] = [
        AudioBook(
            title="Title 01",
            subtitle="Subtitle 01",
            author="Author 01",
            reader="Reader 01",
            link="Link 01",
        ),
        AudioBook(
            title="Title 02",
            subtitle="Subtitle 02",
            author="Author 02",
            reader="Reader 02",
            link="Link 02",
        ),
    ]
    return audio_books


@fixture
def audio_book_repository():
    db_session = next(test_orm.get_db_for_testing())

    db_session.query(AudioBook).delete()
    db_session.commit()

    audio_book_repository: AudioBookRepository = AudioBookRepository(db_session)

    yield audio_book_repository


def test_get_all_audio_books_returns_all_audio_books(
    audio_book_repository: AudioBookRepository,
    audio_books: List[AudioBook],
):
    audio_book_repository.save_audio_books(audio_books)

    actual_audio_books = audio_book_repository.get_all_audio_books()

    assert len(actual_audio_books) == 2
    for idx, actual_audio_book in enumerate(actual_audio_books):
        assert actual_audio_book.title == audio_books[idx].title


def test_get_all_audio_book_links_returns_all_links(
    audio_book_repository: AudioBookRepository,
    audio_books: List[AudioBook],
):
    audio_book_repository.save_audio_books(audio_books)

    actual_audio_book_links = audio_book_repository.get_all_audio_book_links()

    assert len(actual_audio_book_links) == 2
    for idx, actual_audio_book_link in enumerate(actual_audio_book_links):
        assert actual_audio_book_link == audio_books[idx].link


def test_save_audio_books_persists_audio_books(
    audio_book_repository: AudioBookRepository, audio_books: List[AudioBook]
):
    initial_audio_books = audio_book_repository.get_all_audio_books()

    audio_book_repository.save_audio_books(audio_books)

    actual_audio_books = audio_book_repository.get_all_audio_books()
    assert len(actual_audio_books) > len(initial_audio_books)
