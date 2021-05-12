from pytest import fixture

from audio_book_alert.storage.audio_book import AudioBook
from audio_book_alert.alert import alert_serializer


def test_serialize_all_audio_books_human_readable_serializes_correctly(
    complete_audio_book: AudioBook, audio_book_with_mandatory_fields_only: AudioBook
) -> None:
    serialized_audio_books = alert_serializer.serialize_all_audio_books_human_readable(
        [complete_audio_book, audio_book_with_mandatory_fields_only]
    )

    expected_response = [
        (
            "Es gibt neue Hörbücher die dich interessieren könnten: \n\n"
            "Title\nSubtitle\nAuthor\nReader\nPlay Time\nRelease Date\nLanguage\nLink"
        ),
        "Title mandatory\nAuthor mandatory\nReader mandatory\nLink mandatory",
    ]

    assert expected_response == serialized_audio_books


def test_serialize_audio_book_human_readable_serializes_audio_book_correctly(
    complete_audio_book: AudioBook,
) -> None:
    serialized_audio_book = alert_serializer._serialize_audio_book_human_readable(
        complete_audio_book
    )

    expected_string = (
        "Title\nSubtitle\nAuthor\nReader\nPlay Time\nRelease Date\nLanguage\nLink"
    )
    assert expected_string == serialized_audio_book


def test_serialize_audio_book_human_readable_serializes_only_mandatory_fields(
    audio_book_with_mandatory_fields_only: AudioBook,
) -> None:
    serialized_audio_book = alert_serializer._serialize_audio_book_human_readable(
        audio_book_with_mandatory_fields_only
    )

    expected_string = (
        "Title mandatory\nAuthor mandatory\nReader mandatory\nLink mandatory"
    )
    assert expected_string == serialized_audio_book


@fixture
def complete_audio_book() -> AudioBook:
    return AudioBook(
        title="Title",
        subtitle="Subtitle",
        author="Author",
        reader="Reader",
        play_time="Play Time",
        release_date="Release Date",
        language="Language",
        link="Link",
    )


@fixture
def audio_book_with_mandatory_fields_only() -> AudioBook:
    return AudioBook(
        title="Title mandatory",
        author="Author mandatory",
        reader="Reader mandatory",
        link="Link mandatory",
    )
