from typing import List
import re

from bs4 import BeautifulSoup

from audio_book_alert.storage.audio_book import AudioBook
from audio_book_alert.storage import audio_book_file_repository

CSS_SELECTOR_LIST_ITEMS = (
    ".adbl-impression-container > "
    + ".bc-list-item > "
    + ".bc-row-responsive > "
    + ".bc-col-responsive > "
    + ".bc-row-responsive > "
    + ".bc-col-responsive > "
    + ".bc-row-responsive > "
    + ".bc-col-responsive > "
    + "span > "
    + "ul"
)
CSS_TITLE_SELECTOR = "li:first-child > h3 > a"
CSS_SUBTITLE_SELECTOR = ".subtitle"
CSS_SELECTOR_AUTHOR = ".authorLabel a"
CSS_SELECTOR_NARRATOR = ".narratorLabel a"
CSS_SELECTOR_PLAY_TIME = ".runtimeLabel"
CSS_SELECTOR_RELEASE_DATE = ".releaseDateLabel"
CSS_SELECTOR_LANGUAGE = ".languageLabel"
CSS_SELECTOR_PAGE_NUMBERS = ".pageNumberElement"


def parse_page_count(html_body: str) -> int:
    soup: BeautifulSoup = BeautifulSoup(html_body, "lxml")
    page_number_elements = soup.select(CSS_SELECTOR_PAGE_NUMBERS)
    page_numbers: List[int] = []
    for page_number_element in page_number_elements:
        string_number = str(next(page_number_element.stripped_strings))
        if string_number != "...":
            page_numbers.append(int(string_number))

    if page_numbers:
        return max(page_numbers)
    else:
        return 1


def parse_audio_books(html_body: str) -> List[AudioBook]:
    stored_audible_links = audio_book_file_repository.get_all_audio_book_links()
    soup: BeautifulSoup = BeautifulSoup(html_body, "lxml")
    audio_books: List[AudioBook] = []
    audio_book_item_information_elements = soup.select(CSS_SELECTOR_LIST_ITEMS)
    for audio_book_item_information_element in audio_book_item_information_elements:
        audio_book = _parse_audio_book(audio_book_item_information_element)
        if audio_book.link not in stored_audible_links:
            stored_audible_links.append(audio_book.link)
            audio_books.append(audio_book)
    return audio_books


def _parse_audio_book(audio_book_item_information_element) -> AudioBook:
    return AudioBook(
        title=_parse_title(audio_book_item_information_element),
        subtitle=_parse_subtitle(audio_book_item_information_element),
        author=_parse_author(audio_book_item_information_element),
        reader=_parse_narrator(audio_book_item_information_element),
        play_time=_parse_play_time(audio_book_item_information_element),
        release_date=_parse_release_date(audio_book_item_information_element),
        language=_parse_language(audio_book_item_information_element),
        link=_parse_link(audio_book_item_information_element),
    )


def _parse_title(bs_element) -> str:
    return parse_by_css_element(bs_element, CSS_TITLE_SELECTOR)


def _parse_subtitle(bs_element) -> str:
    return parse_by_css_element(bs_element, CSS_SUBTITLE_SELECTOR)


def _parse_author(bs_element) -> str:
    authors: str = parse_by_css_element(bs_element, CSS_SELECTOR_AUTHOR)
    return f"Geschrieben von: {authors}"


def _parse_narrator(bs_element) -> str:
    narrators: str = parse_by_css_element(bs_element, CSS_SELECTOR_NARRATOR)
    return f"Gesprochen von: {narrators}"


def _parse_play_time(bs_element) -> str:
    return parse_by_css_element(bs_element, CSS_SELECTOR_PLAY_TIME)


def _parse_release_date(bs_element) -> str:
    return parse_by_css_element(bs_element, CSS_SELECTOR_RELEASE_DATE)


def _parse_language(bs_element) -> str:
    return parse_by_css_element(bs_element, CSS_SELECTOR_LANGUAGE)


def _parse_link(bs_element) -> str:
    element = bs_element.select(CSS_TITLE_SELECTOR)[0]
    path: str = element["href"]
    return f"https://audible.de{path}"


def parse_by_css_element(bs_element, css_selector: str) -> str:
    elements = bs_element.select(css_selector)

    if elements:
        strings: List[str] = []
        for element in elements:
            strings.append(next(element.stripped_strings))
        content: str = ", ".join(strings)
        # content: str = str(next(elements[0].stripped_strings))
        stripped_content: str = re.sub(r"\s+", " ", content)
        return stripped_content
    else:
        return ""
