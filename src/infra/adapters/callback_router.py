import logging
import re
from collections.abc import Awaitable, Callable
from typing import Any

from telethon import events

from infra.adapters.bot_client import BotClient
from infra.adapters.keyboards import (
    make_confirm_keyboard,
    make_main_menu_keyboard,
    make_mark_actions_keyboard,
    make_marks_list_keyboard,
)

logger = logging.getLogger(__name__)

CallbackHandlerType = Callable[..., Awaitable[Any]]
MessageHandlerType = Callable[..., Awaitable[Any]]


class CallbackRouter:
    """Роутер для обработки callback-запросов от inline-кнопок."""

    def __init__(self, bot: BotClient) -> None:
        self._bot = bot
        self._callback_handlers: dict[str, CallbackHandlerType] = {}
        self._message_handlers: dict[str, MessageHandlerType] = {}
        self._waiting_for_message: dict[int, str] = {}

    def callback(self, pattern: str) -> Callable[[CallbackHandlerType], CallbackHandlerType]:
        """Декоратор для регистрации обработчика callback."""

        def decorator(func: CallbackHandlerType) -> CallbackHandlerType:
            self._callback_handlers[pattern] = func
            return func

        return decorator

    def expect_message(self, state: str) -> Callable[[MessageHandlerType], MessageHandlerType]:
        """Декоратор для регистрации обработчика ожидаемого сообщения."""

        def decorator(func: MessageHandlerType) -> MessageHandlerType:
            self._message_handlers[state] = func
            return func

        return decorator

    def set_user_state(self, user_id: int, state: str) -> None:
        """Устанавливает состояние ожидания для пользователя."""
        self._waiting_for_message[user_id] = state

    def clear_user_state(self, user_id: int) -> None:
        """Очищает состояние ожидания для пользователя."""
        self._waiting_for_message.pop(user_id, None)

    def get_user_state(self, user_id: int) -> str | None:
        """Получает текущее состояние ожидания пользователя."""
        return self._waiting_for_message.get(user_id)

    async def setup(self) -> None:
        """Настраивает обработчики событий Telethon."""

        @self._bot.client.on(events.CallbackQuery)
        async def handle_callback(event: events.CallbackQuery.Event) -> None:
            await self._dispatch_callback(event)

        @self._bot.client.on(events.NewMessage)
        async def handle_message(event: events.NewMessage.Event) -> None:
            await self._dispatch_message(event)

        logger.info("Callback and message handlers registered")

    async def _dispatch_callback(self, event: events.CallbackQuery.Event) -> None:
        """Вызывает обработчик callback-запроса."""
        data = event.data.decode() if event.data else ""
        logger.debug("Callback received: %s", data)

        for pattern, handler in self._callback_handlers.items():
            match = re.match(pattern, data)
            if match:
                try:
                    await handler(event, **match.groupdict())
                except Exception as e:
                    logger.error("Error handling callback '%s': %s", data, e, exc_info=True)
                    await event.answer("❌ Произошла ошибка")
                return

        logger.warning("No handler for callback: %s", data)
        await event.answer("Неизвестное действие")

    async def _dispatch_message(self, event: events.NewMessage.Event) -> None:
        """Вызывает обработчик сообщения для ожидающих состояний."""
        if event.sender_id is None:
            return

        state = self.get_user_state(event.sender_id)
        if state is None:
            return

        handler = self._message_handlers.get(state)
        if handler is None:
            logger.warning("No message handler for state: %s", state)
            return

        try:
            await handler(event)
        except Exception as e:
            logger.error("Error handling message in state '%s': %s", state, e, exc_info=True)
            await event.respond("❌ Произошла ошибка")


callback_router = CallbackRouter
