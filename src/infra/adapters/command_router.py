import logging
from collections.abc import Awaitable, Callable
from typing import Any

from telethon import events

from infra.adapters.bot_client import BotClient
from infra.adapters.keyboards import make_main_menu_keyboard

logger = logging.getLogger(__name__)

HandlerType = Callable[..., Awaitable[Any]]


class CommandRouter:
    """Роутер для обработки Telegram команд."""

    def __init__(self, bot: BotClient) -> None:
        self._bot = bot
        self._handlers: dict[str, HandlerType] = {}

    def register(self, command: str) -> Callable[[HandlerType], HandlerType]:
        """Декоратор для регистрации обработчика команды."""

        def decorator(func: HandlerType) -> HandlerType:
            self._handlers[command] = func
            return func

        return decorator

    async def setup(self) -> None:
        """Настраивает обработчики событий Telethon."""

        @self._bot.client.on(events.NewMessage(pattern=r"^/start$"))
        async def handle_start(event: events.NewMessage.Event) -> None:
            await self._dispatch("start", event)

        @self._bot.client.on(events.NewMessage(pattern=r"^/help$"))
        async def handle_help(event: events.NewMessage.Event) -> None:
            await self._dispatch("help", event)

        @self._bot.client.on(events.NewMessage(pattern=r"^/marks$"))
        async def handle_marks(event: events.NewMessage.Event) -> None:
            await self._dispatch("marks", event)

        @self._bot.client.on(events.NewMessage(pattern=r"^/menu$"))
        async def handle_menu(event: events.NewMessage.Event) -> None:
            await self._dispatch("menu", event)

        logger.info("Command handlers registered: %s", list(self._handlers.keys()))

    async def _dispatch(self, command: str, event: events.NewMessage.Event) -> None:
        """Вызывает зарегистрированный обработчик команды."""
        handler = self._handlers.get(command)
        if handler is None:
            logger.warning("No handler registered for command: %s", command)
            return
        try:
            await handler(event)
        except Exception as e:
            logger.error("Error handling command '%s': %s", command, e, exc_info=True)
            await event.respond("❌ Произошла ошибка при обработке команды")

    async def send_main_menu(self, event: events.NewMessage.Event) -> None:
        """Отправляет главное меню."""
        await event.respond("📱 Главное меню:", buttons=make_main_menu_keyboard())


command_router = CommandRouter
