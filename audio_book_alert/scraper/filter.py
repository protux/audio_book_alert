from typing import List

from audio_book_alert.storage.audio_book import AudioBook


def filter_audio_books(
    parsed_audio_books: List[AudioBook], past_audio_books: List[AudioBook]
) -> List[AudioBook]:
    filtered_audio_books: List[AudioBook] = [
        audio_book
        for audio_book in parsed_audio_books
        if _should_accept_audio_book(audio_book, past_audio_books)
    ]
    audio_books_without_duplicates = _remove_duplicates(filtered_audio_books)
    return audio_books_without_duplicates


def _remove_duplicates(filtered_audio_books):
    audio_books_without_duplicates: List[AudioBook] = []
    links: [str] = []
    for audio_book in filtered_audio_books:
        if audio_book.link not in links:
            audio_books_without_duplicates.append(audio_book)
            links.append(audio_book.link)
    return audio_books_without_duplicates


def _should_accept_audio_book(
    audio_book: AudioBook, past_audio_books: List[AudioBook]
) -> bool:
    return _audio_book_has_acceptable_language(
        audio_book
    ) and _audio_book_already_known(audio_book, past_audio_books)


def _audio_book_has_acceptable_language(audio_book):
    return "Deutsch" in audio_book.language or not audio_book.language


def _audio_book_already_known(audio_book, past_audio_books):
    return audio_book not in past_audio_books
