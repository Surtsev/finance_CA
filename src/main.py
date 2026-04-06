import asyncio
import logging

from config.settings import settings
from infra.adapters.bot_client import BotClient
from infra.adapters.command_router import CommandRouter
from infra.adapters.callback_router import CallbackRouter
from infra.adapters.event_handlers import BotEventHandlers

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def run_bot() -> None:
    """Запускает Telegram бота."""
    bot = BotClient()

    async with bot:
        command_router = CommandRouter(bot)
        callback_router = CallbackRouter(bot)

        await command_router.setup()
        await callback_router.setup()

        event_handlers = BotEventHandlers(bot, command_router, callback_router)

        logger.info("Bot is starting...")
        await bot.client.run_until_disconnected()


def main() -> None:
    """Точка входа приложения."""
    if not settings.TELEGRAM_API_ID or not settings.TELEGRAM_API_HASH:
        logger.error(
            "TELEGRAM_API_ID and TELEGRAM_API_HASH must be set in environment variables"
        )
        return

    try:
        asyncio.run(run_bot())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error("Bot crashed: %s", e, exc_info=True)


if __name__ == "__main__":
    main()
