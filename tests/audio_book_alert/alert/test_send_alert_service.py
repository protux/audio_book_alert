from unittest.mock import MagicMock

from pytest import fixture

from audio_book_alert.alert import alert_serializer
from audio_book_alert.alert.send_alert_service import SendAlertService


def test_send_alert_does_nothing_on_empty_audio_book_list(
    send_alert_service: SendAlertService,
) -> None:
    send_alert_service.send_alert([])

    send_alert_service.telegram_bot.send_message.assert_not_called()


def test_send_alert_sends_alert(
    send_alert_service: SendAlertService,
    patched_serialize_all_audio_books_human_readable,
) -> None:
    subscriber_chat_ids = [123, 321]
    serialized_audio_books = ["book"]
    send_alert_service.telegram_subscription_repository = MagicMock()
    send_alert_service.telegram_subscription_repository.get_all_subscribers_chat_ids.return_value = (
        subscriber_chat_ids
    )

    send_alert_service.send_alert(["Hallo welt"])

    send_alert_service.telegram_bot.send_message.assert_called_with(
        serialized_audio_books, subscriber_chat_ids
    )


@fixture
def send_alert_service() -> SendAlertService:
    return SendAlertService(MagicMock(), MagicMock())


@fixture
def patched_serialize_all_audio_books_human_readable(monkeypatch) -> None:
    monkeypatch.setattr(
        alert_serializer, "serialize_all_audio_books_human_readable", lambda x: ["book"]
    )
