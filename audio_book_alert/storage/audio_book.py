from dataclasses import dataclass
from typing import Optional


@dataclass
class AudioBook:
    title: str
    subtitle: Optional[str]
    author: str
    reader: str
    play_time: str
    release_date: str
    language: str
    link: str

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
