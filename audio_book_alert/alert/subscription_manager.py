from os import path
from pathlib import Path
from typing import List
import json

from telegram import User

from audio_book_alert import config
from audio_book_alert.storage import file_utils

SUBSCRIBERS_SAVE_FILE = path.join(
    Path.home(), f'.telegram/subscriptions/{config.Settings().telegram_bot_name}/subscribers.json'
)


def subscribe_user(user_data: User) -> bool:
    file_was_created: bool = file_utils.make_sure_file_exists(SUBSCRIBERS_SAVE_FILE)
    subscribed_ids = _read_subriber_ids_from_file()
    if user_data.id not in subscribed_ids:
        _add_subscriber_to_storage(user_data, file_was_created)
        return True
    else:
        return False


def _add_subscriber_to_storage(user_data, first_entry: bool):
    with open(SUBSCRIBERS_SAVE_FILE, 'a') as subscribers_file:
        if not first_entry:
            subscribers_file.write('\n')
        serialized_user_data = {
            'id': user_data.id,
            'language': user_data.language_code,
        }
        subscribers_file.write(json.dumps(serialized_user_data))


def get_all_subscriber_ids() -> List[int]:
    if Path(SUBSCRIBERS_SAVE_FILE).is_file():
        return _read_subriber_ids_from_file()
    else:
        return []


def _read_subriber_ids_from_file() -> List[int]:
    with open(SUBSCRIBERS_SAVE_FILE, 'r') as subscribers_file:
        subscribers: List[str] = subscribers_file.readlines()
        subscriber_ids: List[int] = [
            _extract_subscriber_id_from_save_file(subscriber) for subscriber in subscribers
        ]
        return subscriber_ids


def _extract_subscriber_id_from_save_file(save_file_line: str) -> int:
    saved_dict: dict = json.loads(save_file_line)
    return saved_dict['id']
