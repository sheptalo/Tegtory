from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

__mine_main_kb = [
    [
        InlineKeyboardButton(text="Туннели", callback_data="tunnels"),
        InlineKeyboardButton(text="Оплата налогов", callback_data="tax"),
    ],
    [
        InlineKeyboardButton(
            text="Расширение территории", callback_data="lvl"
        ),
        InlineKeyboardButton(text="Меню", callback_data="menu"),
    ],
]

back_mine = InlineKeyboardButton(text="Обратно", callback_data="mine")

__tax_kb = [
    [
        InlineKeyboardButton(
            text="Оплатить Налоги", callback_data="mine-pay-tax"
        )
    ],
    [back_mine],
]

mine_tax_markup = InlineKeyboardMarkup(inline_keyboard=__tax_kb)
mine_main_markup = InlineKeyboardMarkup(inline_keyboard=__mine_main_kb)
back_mine_markup = InlineKeyboardMarkup(inline_keyboard=[[back_mine]])


def tunnels_markup(ids):
    builder = InlineKeyboardBuilder()
    for i in ids:
        builder.button(text=f"номер {i}", callback_data=f"mine-{i}")
    builder.button(text="Назад", callback_data="mine")
    return builder.as_markup()


__all__ = [
    "mine_tax_markup",
    "mine_main_markup",
    "tunnels_markup",
    "back_mine_markup",
]
