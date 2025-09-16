from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def make_keyboard(
    items: list[str],
    is_column: bool = False,
    has_cancel_button: bool = True
) -> ReplyKeyboardMarkup:
    if has_cancel_button:
        items.append("Отмена")

    if is_column:
        return ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text=item)] for item in items],
            resize_keyboard=True,
        )

    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=item) for item in items]],
        resize_keyboard=True
    )


def get_main_inline_keyboard(is_registered: bool = True):
    buttons = []

    if is_registered:
        buttons.extend(
            [
                KeyboardButton(text="Хочу предсказание!"),
                KeyboardButton(text="Профиль")
            ]
        )
    else:
        buttons.append(KeyboardButton(text="Регистрация"))

    return ReplyKeyboardMarkup(
        keyboard=[buttons],
        resize_keyboard=True,
    )
