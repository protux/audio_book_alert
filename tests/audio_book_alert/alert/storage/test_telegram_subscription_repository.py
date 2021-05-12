import copy
from typing import List

from pytest import (
    fixture,
)

from audio_book_alert.alert.storage.telegram_subscription import TelegramSubscription
from audio_book_alert.alert.storage.telegram_subscription_repository import (
    TelegramSubscriptionRepository,
)
from tests import test_orm


def test_subscribe_user_persist_subscription(
    telegram_subscription_repository: TelegramSubscriptionRepository,
    telegram_subscription: TelegramSubscription,
) -> None:
    subscribed_successfully = telegram_subscription_repository.subscribe_user(
        telegram_subscription
    )

    assert subscribed_successfully
    db_session: test_orm.TestingSessionLocal = next(test_orm.get_db_for_testing())
    subscribed_users: List[TelegramSubscription] = db_session.query(
        TelegramSubscription
    ).all()
    assert len(subscribed_users) == 1
    subscribed_user: TelegramSubscription = subscribed_users[0]
    assert telegram_subscription.user_id == subscribed_user.user_id
    assert telegram_subscription.chat_id == subscribed_user.chat_id
    assert telegram_subscription.language == subscribed_user.language


def test_subscribe_user_returns_false_on_duplicate_chat_id(
    telegram_subscription_repository: TelegramSubscriptionRepository,
    telegram_subscription: TelegramSubscription,
) -> None:
    telegram_subscription_copy: TelegramSubscription = copy.deepcopy(
        telegram_subscription
    )

    telegram_subscription_repository.subscribe_user(telegram_subscription)
    successfully_subscribed = telegram_subscription_repository.subscribe_user(
        telegram_subscription_copy
    )
    assert not successfully_subscribed


def test_get_all_subscribers_chat_ids_returns_chat_ids(
    telegram_subscription_repository: TelegramSubscriptionRepository,
    telegram_subscription: TelegramSubscription,
    other_telegram_subscription: TelegramSubscription,
) -> None:
    telegram_subscription_repository.subscribe_user(telegram_subscription)
    telegram_subscription_repository.subscribe_user(other_telegram_subscription)

    chat_ids: List[
        int
    ] = telegram_subscription_repository.get_all_subscribers_chat_ids()

    assert telegram_subscription.chat_id == chat_ids[0]
    assert other_telegram_subscription.chat_id == chat_ids[1]


@fixture
def telegram_subscription_repository() -> TelegramSubscriptionRepository:
    db_session = next(test_orm.get_db_for_testing())

    db_session.query(TelegramSubscription).delete()
    db_session.commit()

    audio_book_repository: TelegramSubscriptionRepository = (
        TelegramSubscriptionRepository(db_session)
    )

    yield audio_book_repository


@fixture
def telegram_subscription() -> TelegramSubscription:
    return TelegramSubscription(user_id=4711, chat_id=2342, language="de")


@fixture
def other_telegram_subscription() -> TelegramSubscription:
    return TelegramSubscription(user_id=2323, chat_id=4242, language="en")
