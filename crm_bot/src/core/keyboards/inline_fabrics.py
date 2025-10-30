from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def inline_keyboard_builder(
    buttons: list[dict[str, str]],
    sizes: int = 2,
    back_text: str = "Back",
    back_cb: str = None,
) -> InlineKeyboardMarkup:
    if not buttons:
        raise ValueError("The list of buttons is empty")

    builder = InlineKeyboardBuilder()

    for button in buttons:
        builder.button(text=button.get("text"), callback_data=button.get("call"))

    builder.adjust(sizes)

    if back_cb:
        builder.row(InlineKeyboardButton(text=back_text, callback_data=back_cb))
    return builder.as_markup()


def inline_back_button(
    back_text: str = "Back",
    back_cb: str = "back",
):
    return InlineKeyboardButton(text=back_text, callback_data=back_cb)


def inline_menu_button() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Повернутися до меню", callback_data="start")]
        ]
    )
