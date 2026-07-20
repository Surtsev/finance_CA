import logging
from typing import Optional

from telethon import TelegramClient
from telethon.errors import AuthKeyError, RPCError

from config.settings import settings

logger = logging.getLogger(__name__)


class BotClient:
    """Telegram client wrapper для работы с Bot API через Telethon."""

    def __init__(
        self,
        api_id: Optional[str] = None,
        api_hash: Optional[str] = None,
        session_name: Optional[str] = None,
    ) -> None:
        self._api_id = api_id or settings.TELEGRAM_API_ID
        self._api_hash = api_hash or settings.TELEGRAM_API_HASH
        self._session_name = session_name or settings.TELEGRAM_SESSION_NAME
        self._client: Optional[TelegramClient] = None

    @property
    def client(self) -> TelegramClient:
        if self._client is None:
            raise RuntimeError("BotClient not connected. Call connect() first.")
        return self._client

    async def connect(self) -> None:
        """Инициализирует и подключает TelegramClient с авторизацией бота."""
        if self._client is not None:
            logger.debug("BotClient already connected")
            return

        try:
            self._client = TelegramClient(
                self._session_name,
                int(self._api_id),
                self._api_hash,
            )
            await self._client.start(bot_token=settings.TELEGRAM_BOT_TOKEN)
            logger.info("BotClient connected and authorized as bot")
        except (AuthKeyError, RPCError, ValueError) as e:
            logger.error("Failed to connect BotClient: %s", e)
            self._client = None
            raise

    async def disconnect(self) -> None:
        """Отключает TelegramClient."""
        if self._client is not None:
            await self._client.disconnect()
            self._client = None
            logger.info("BotClient disconnected")

    async def send_message(self, chat_id: int, message: str, *, parse_mode: str = "html") -> None:
        """Отправляет сообщение в чат."""
        await self.client.send_message(chat_id, message, parse_mode=parse_mode)

    async def send_message_with_buttons(
        self, chat_id: int, message: str, buttons, *, parse_mode: str = "html"
    ) -> None:
        """Отправляет сообщение с inline-кнопками."""
        await self.client.send_message(chat_id, message, buttons=buttons, parse_mode=parse_mode)

    async def get_me(self):
        """Возвращает информацию о боте."""
        return await self.client.get_me()

    async def __aenter__(self) -> "BotClient":
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.disconnect()
