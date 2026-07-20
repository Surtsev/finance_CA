from telethon.tl.custom import Button


def make_main_menu_keyboard() -> list[list[Button]]:
    """Главное меню бота."""
    return [
        [Button.inline("📋 Мои метки", b"menu_marks"), Button.inline("💳 Карты", b"menu_cards")],
        [Button.inline("🎯 Цели", b"menu_goals")],
        [Button.inline("❓ Помощь", b"menu_help")],
    ]


def make_mark_actions_keyboard(mark_name: str) -> list[list[Button]]:
    """Кнопки действий для конкретной метки."""
    return [
        [Button.inline("➕ Добавить карту", callback_data=f"mark_add_card:{mark_name}")],
        [Button.inline("✏️ Изменить текущую сумму", callback_data=f"mark_update_current:{mark_name}")],
        [Button.inline("🗑 Удалить метку", callback_data=f"mark_delete:{mark_name}")],
        [Button.inline("🔙 Назад", callback_data=b"menu_marks")],
    ]


def make_marks_list_keyboard(mark_names: list[str]) -> list[list[Button]]:
    """Клавиатура со списком меток."""
    buttons = []
    row = []
    for name in mark_names:
        row.append(Button.inline(name, callback_data=f"mark_select:{name}"))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    buttons.append([Button.inline("🔙 Назад", callback_data=b"menu_main")])
    return buttons


def make_confirm_keyboard() -> list[list[Button]]:
    """Клавиатура подтверждения."""
    return [
        [Button.inline("✅ Да", callback_data=b"confirm_yes"), Button.inline("❌ Нет", callback_data=b"confirm_no")],
    ]


def make_cancel_keyboard() -> list[list[Button]]:
    """Клавиатура отмены."""
    return [
        [Button.inline("❌ Отмена", callback_data=b"cancel")],
    ]
