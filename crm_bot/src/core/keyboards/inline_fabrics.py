from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def inline_keyboard_fabric(
    buttons: list[dict[str, str]],
    sizes: int = 2,
) -> InlineKeyboardBuilder:

    builder = InlineKeyboardBuilder()

    for button in buttons:
        text = button.get("text")
        call = button.get("call")

        if text is None or call is None:
            raise ValueError("Button must contain 'text' and 'call'")

        builder.button(text=text, callback_data=call)

    builder.adjust(sizes)

    return builder


def inline_keyboard_builder(
    buttons: list[dict[str, str]],
    sizes: int = 2,
    back_text: str = "Back",
    back_cb: str | None = None,
) -> InlineKeyboardMarkup:

    kb = inline_keyboard_fabric(
        buttons=buttons,
        sizes=sizes,
    )
    if back_cb is not None:
        kb.row(inline_back_button(back_cb=back_cb))
    return kb.as_markup()


def inline_keyboard_builder_with_pagination(
    buttons: list[dict[str, str]],
    pg_coll_prefix: str,
    page: int,
    sizes: int = 2,
    back_text: str = "Back",
    back_cb: str | None = None,
    hes_next: bool = True,
) -> InlineKeyboardMarkup:
    kb = inline_keyboard_fabric(
        buttons=buttons,
        sizes=sizes,
    )

    kb.row(
        InlineKeyboardButton(
            text="⬅️", callback_data=f"{pg_coll_prefix}:{max(1, page - 1)}"
        ),
        InlineKeyboardButton(
            text="➡️",
            callback_data=f"{pg_coll_prefix}:{page + 1 if hes_next else page}",
        ),
    )

    if back_cb is not None:
        kb.row(inline_back_button(back_cb=back_cb))
    return kb.as_markup()


def inline_menu_button() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Повернутися до меню", callback_data="start")]
        ]
    )


def inline_back_button(
    back_text: str = "Back",
    back_cb: str = "back",
):
    return InlineKeyboardButton(text=back_text, callback_data=back_cb)
