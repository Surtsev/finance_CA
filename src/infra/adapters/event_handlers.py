import logging

from telethon import events

from infra.adapters.bot_client import BotClient
from infra.adapters.callback_router import CallbackRouter
from infra.adapters.command_router import CommandRouter
from infra.adapters.keyboards import (
    make_cancel_keyboard,
    make_confirm_keyboard,
    make_main_menu_keyboard,
    make_mark_actions_keyboard,
    make_marks_list_keyboard,
)
from usecases import (
    add_card_to_mark,
    create_mark,
    delete_mark,
    update_card,
    update_mark,
    update_mark_current,
    delete_card_from_mark,
)

logger = logging.getLogger(__name__)


class BotEventHandlers:
    """Обработчики событий Telegram бота."""

    def __init__(
        self,
        bot: BotClient,
        command_router: CommandRouter,
        callback_router: CallbackRouter,
    ) -> None:
        self._bot = bot
        self._command_router = command_router
        self._callback_router = callback_router
        self._setup_handlers()

    def _setup_handlers(self) -> None:
        """Регистрирует все обработчики команд и callback."""
        self._setup_command_handlers()
        self._setup_callback_handlers()
        self._setup_message_handlers()

    def _setup_command_handlers(self) -> None:
        """Регистрирует обработчики команд."""

        @self._command_router.register("start")
        async def cmd_start(event: events.NewMessage.Event) -> None:
            await event.respond(
                "👋 Привет! Я бот для управления финансами.\n\n"
                "Используйте /menu для главного меню или /help для справки.",
                buttons=make_main_menu_keyboard(),
            )

        @self._command_router.register("help")
        async def cmd_help(event: events.NewMessage.Event) -> None:
            await event.respond(
                "📖 *Справка по боту*\n\n"
                "/start - Запустить бота\n"
                "/menu - Главное меню\n"
                "/marks - Список меток\n"
                "/help - Эта справка\n\n"
                "Вы можете создавать метки, добавлять карты и отслеживать финансовые цели.",
            )

        @self._command_router.register("menu")
        async def cmd_menu(event: events.NewMessage.Event) -> None:
            await self._command_router.send_main_menu(event)

        @self._command_router.register("marks")
        async def cmd_marks(event: events.NewMessage.Event) -> None:
            await self._handle_show_marks(event)

    def _setup_callback_handlers(self) -> None:
        """Регистрирует обработчики callback."""
        router = self._callback_router

        @router.callback(r"^menu_main$")
        async def cb_menu_main(event: events.CallbackQuery.Event) -> None:
            await event.edit("📱 Главное меню:", buttons=make_main_menu_keyboard())

        @router.callback(r"^menu_marks$")
        async def cb_menu_marks(event: events.CallbackQuery.Event) -> None:
            await self._handle_show_marks(event)

        @router.callback(r"^mark_select:(?P<mark_name>.+)$")
        async def cb_mark_select(event: events.CallbackQuery.Event, mark_name: str) -> None:
            await self._handle_mark_actions(event, mark_name)

        @router.callback(r"^mark_add_card:(?P<mark_name>.+)$")
        async def cb_mark_add_card(event: events.CallbackQuery.Event, mark_name: str) -> None:
            self._callback_router.set_user_state(event.sender_id, f"awaiting_card_name:{mark_name}")
            await event.edit(
                f"💳 Введите название карты для метки '{mark_name}':",
                buttons=make_cancel_keyboard(),
            )

        @router.callback(r"^mark_update_current:(?P<mark_name>.+)$")
        async def cb_mark_update_current(event: events.CallbackQuery.Event, mark_name: str) -> None:
            self._callback_router.set_user_state(event.sender_id, f"awaiting_current_amount:{mark_name}")
            await event.edit(
                f"✏️ Введите сумму для метки '{mark_name}':",
                buttons=make_cancel_keyboard(),
            )

        @router.callback(r"^mark_delete:(?P<mark_name>.+)$")
        async def cb_mark_delete(event: events.CallbackQuery.Event, mark_name: str) -> None:
            await event.edit(
                f"🗑 Вы уверены, что хотите удалить метку '{mark_name}'?",
                buttons=make_confirm_keyboard(),
            )
            self._callback_router.set_user_state(event.sender_id, f"confirm_delete_mark:{mark_name}")

        @router.callback(r"^confirm_yes$")
        async def cb_confirm_yes(event: events.CallbackQuery.Event) -> None:
            state = self._callback_router.get_user_state(event.sender_id)
            if state and state.startswith("confirm_delete_mark:"):
                mark_name = state.split(":", 1)[1]
                await self._handle_delete_mark(event, mark_name)
            self._callback_router.clear_user_state(event.sender_id)

        @router.callback(r"^confirm_no$")
        async def cb_confirm_no(event: events.CallbackQuery.Event) -> None:
            self._callback_router.clear_user_state(event.sender_id)
            await event.edit("❌ Действие отменено", buttons=make_main_menu_keyboard())

        @router.callback(r"^cancel$")
        async def cb_cancel(event: events.CallbackQuery.Event) -> None:
            self._callback_router.clear_user_state(event.sender_id)
            await event.edit("❌ Действие отменено", buttons=make_main_menu_keyboard())

    def _setup_message_handlers(self) -> None:
        """Регистрирует обработчики сообщений."""
        router = self._callback_router

        @router.expect_message(r"^awaiting_card_name:.+$")
        async def msg_card_name(event: events.NewMessage.Event) -> None:
            state = router.get_user_state(event.sender_id)
            mark_name = state.split(":", 1)[1]
            card_name = event.message.text.strip()

            # TODO: Implement add card usecase
            await event.respond(f"✅ Карта '{card_name}' добавлена к метке '{mark_name}'")
            router.clear_user_state(event.sender_id)
            await self._handle_mark_actions(event, mark_name)

        @router.expect_message(r"^awaiting_current_amount:.+$")
        async def msg_current_amount(event: events.NewMessage.Event) -> None:
            state = router.get_user_state(event.sender_id)
            mark_name = state.split(":", 1)[1]
            amount_text = event.message.text.strip()

            try:
                amount = int(amount_text.replace(" ", ""))
                # TODO: Implement update mark current usecase
                await event.respond(f"✅ Сумма метки '{mark_name}' обновлена на {amount}")
            except ValueError:
                await event.respond("❌ Неверный формат суммы. Введите число.")
                return

            router.clear_user_state(event.sender_id)
            await self._handle_mark_actions(event, mark_name)

        @router.expect_message(r"^confirm_delete_mark:.+$")
        async def msg_confirm_delete(event: events.NewMessage.Event) -> None:
            # This state is handled by confirm_yes/confirm_no callbacks
            pass

    async def _handle_show_marks(self, event) -> None:
        """Показывает список меток."""
        # TODO: Fetch marks from repository
        mark_names = []  # Replace with actual marks
        if mark_names:
            await event.respond("📋 Ваши метки:", buttons=make_marks_list_keyboard(mark_names))
        else:
            await event.respond(
                "📋 У вас пока нет меток.\n\n"
                "Используйте команду /create для создания новой метки.",
                buttons=make_main_menu_keyboard(),
            )

    async def _handle_mark_actions(self, event, mark_name: str) -> None:
        """Показывает действия для конкретной метки."""
        # TODO: Fetch mark details
        await event.respond(
            f"📝 Метка: {mark_name}\n\nВыберите действие:",
            buttons=make_mark_actions_keyboard(mark_name),
        )

    async def _handle_delete_mark(self, event, mark_name: str) -> None:
        """Удаляет метку."""
        # TODO: Implement delete mark usecase
        await event.respond(f"🗑 Метка '{mark_name}' удалена", buttons=make_main_menu_keyboard())
