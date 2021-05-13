from typing import (
    List,
    Set,
)

import requests
from requests import Response

from audio_book_alert.scraper import parser
from audio_book_alert.storage.audio_book import AudioBook
from audio_book_alert.storage.audio_book_repository import AudioBookRepository

AUDIBLE_AUTHOR_SEARCH_URL = (
    "https://www.audible.de/search?searchAuthor={author}&pageSize=50&page={page}"
)
AUDIBLE_NARRATOR_SEARCH_URL = (
    "https://www.audible.de/search?searchNarrator={narrator}&pageSize=50&page={page}"
)


def find_titles_by_author(
    author: str, audio_book_repository: AudioBookRepository
) -> Set[AudioBook]:
    author_url: str = AUDIBLE_AUTHOR_SEARCH_URL.format(author=author, page="{page}")
    return _find_titles(author_url, audio_book_repository)


def find_titles_by_narrator(
    narrator: str, audio_book_repository: AudioBookRepository
) -> Set[AudioBook]:
    narrator_url = AUDIBLE_NARRATOR_SEARCH_URL.format(narrator=narrator, page="{page}")
    return _find_titles(narrator_url, audio_book_repository)


def _find_titles(
    url: str, audio_book_repository: AudioBookRepository
) -> Set[AudioBook]:
    audio_books: Set[AudioBook] = set()
    html = _request_html(url=url, page=1)
    audio_books.update(parser.parse_audio_books(html, audio_book_repository))
    page_count = parser.parse_page_count(html)

    for i in range(2, page_count + 1):
        html = _request_html(url=url, page=i)
        parsed_audio_books = parser.parse_audio_books(html, audio_book_repository)
        audio_books.update(parsed_audio_books)

    return audio_books


def _request_html(url: str, **kwargs) -> str:
    response: Response = requests.get(url.format(**kwargs))
    if response.status_code != 200:
        raise Exception(
            f"got status code {response.status_code} and response {response.text}"
        )
    return response.text
