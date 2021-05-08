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
from audio_book_alert.alert import subscription_manager


def start_bot() -> None:
    updater = create_updater()
    dispatcher = updater.dispatcher
    _register_commands(dispatcher)
    updater.start_polling()


def create_updater() -> Updater:
    return Updater(token=config.Settings().telegram_api_key, use_context=True)


def _register_commands(dispatcher: Dispatcher) -> None:
    start_command_handler = CommandHandler("start", _start_command_listener)
    dispatcher.add_handler(start_command_handler)

    unknown_handler = MessageHandler(Filters.command, _unknown_command)
    dispatcher.add_handler(unknown_handler)


def _start_command_listener(update: Update, context: CallbackContext):
    successfully_subscribed = subscription_manager.subscribe_user(
        update.effective_message.from_user, update.effective_chat.id
    )
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


def _unknown_command(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Tut mir leid, das habe ich nicht verstanden. Registriere dich für Hörbuch-Updates mit /start",
    )


def send_message(messages: List[str], chat_ids: List[int]) -> None:
    for chat_id in chat_ids:
        bot: Bot = Bot(token=config.Settings().telegram_api_key)
        for message in messages:
            send_telegram_message(bot, message, chat_id)


def send_telegram_message(bot, message, chat_id):
    try:
        bot.send_message(chat_id=chat_id, text=message)
    except RetryAfter as e:
        retry_in_seconds: float = e.retry_after
        time.sleep(retry_in_seconds)
        send_telegram_message(bot, message, chat_id)
