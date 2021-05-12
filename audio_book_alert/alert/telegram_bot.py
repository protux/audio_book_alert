import time
from typing import List

from telegram import (
    Update,
    Bot,
)
from telegram.error import RetryAfter
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
    Dispatcher,
)

from audio_book_alert import config
from audio_book_alert.alert.storage.telegram_subscription import TelegramSubscription
from audio_book_alert.alert.storage.telegram_subscription_repository import (
    TelegramSubscriptionRepository,
)
from audio_book_alert.database.orm import get_db


def start_bot() -> None:
    updater = _create_updater()
    dispatcher = updater.dispatcher
    _register_commands(dispatcher)
    updater.start_polling()


def _create_updater() -> Updater:
    return Updater(token=config.Settings().telegram_api_key, use_context=True)


def _register_commands(dispatcher: Dispatcher) -> None:
    start_command_handler = CommandHandler("start", _start_command_listener)
    dispatcher.add_handler(start_command_handler)

    unknown_handler = MessageHandler(Filters.command, _unknown_command)
    dispatcher.add_handler(unknown_handler)


def _start_command_listener(update: Update, context: CallbackContext) -> None:
    successfully_subscribed = _subscribe_user(update)

    if successfully_subscribed:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Du bist jetzt für Hörbuch-Updates angemeldet.",
        )
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Du bist bereits für Hörbuch-Updates angemeldet.",
        )


def _subscribe_user(update):
    telegram_subscription: TelegramSubscription = TelegramSubscription(
        user_id=update.effective_message.from_user.id,
        language=update.effective_message.from_user.language_code,
        chat_id=update.effective_chat.id,
    )
    telegram_subscription_repository: TelegramSubscriptionRepository = (
        TelegramSubscriptionRepository(get_db())
    )
    successfully_subscribed: bool = telegram_subscription_repository.subscribe_user(
        telegram_subscription
    )
    return successfully_subscribed


def _unknown_command(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Tut mir leid, das habe ich nicht verstanden. Registriere dich für Hörbuch-Updates mit /start",
    )


def send_message(messages: List[str], chat_ids: List[int]) -> None:
    for chat_id in chat_ids:
        bot: Bot = Bot(token=config.Settings().telegram_api_key)
        for message in messages:
            _send_telegram_message(bot, message, chat_id)


def _send_telegram_message(bot: Bot, message: str, chat_id: int) -> None:
    try:
        bot.send_message(chat_id=chat_id, text=message)
    except RetryAfter as e:
        retry_in_seconds: float = e.retry_after
        time.sleep(retry_in_seconds)
        _send_telegram_message(bot, message, chat_id)
