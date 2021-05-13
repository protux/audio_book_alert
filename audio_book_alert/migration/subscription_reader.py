import json
from os import path
from pathlib import Path
from typing import List

from audio_book_alert import config

SUBSCRIBERS_SAVE_FILE = path.join(
    Path.home(),
    f".telegram/subscriptions/{config.Settings().telegram_bot_name}/subscribers.json",
)


def read_subscribers_from_file() -> List[dict]:
    with open(SUBSCRIBERS_SAVE_FILE, "r") as subscribers_file:
        subscribers_plain: List[str] = subscribers_file.readlines()
        subscribers = [
            json.loads(subscriber) for subscriber in subscribers_plain
        ]
        return subscribers
