from typing import List

from audio_book_alert.storage.audio_book import AudioBook


def serialize_all_audio_books_human_readable(audio_books: List[AudioBook]) -> List[str]:
    serialized_audio_books: List[str] = [
        _serialize_audio_book_human_readable(audio_book) for audio_book in audio_books
    ]
    serialized_audio_books[0] = (
        "Es gibt neue Hörbücher die dich interessieren könnten: \n\n"
        + serialized_audio_books[0]
    )
    return serialized_audio_books


def _serialize_audio_book_human_readable(audio_book: AudioBook) -> str:
    output: str = audio_book.title
    if audio_book.subtitle:
        output += "\n" + audio_book.subtitle
    output += "\n" + audio_book.author
    output += "\n" + audio_book.reader
    if audio_book.play_time:
        output += "\n" + audio_book.play_time
    if audio_book.release_date:
        output += "\n" + audio_book.release_date
    if audio_book.language:
        output += "\n" + audio_book.language
    output += "\n" + audio_book.link
    return output
