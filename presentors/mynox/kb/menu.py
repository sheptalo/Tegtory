from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

menu_kb = [
    [
        InlineKeyboardButton(text="Шахта", callback_data="mine"),
        InlineKeyboardButton(text="Город", callback_data="city"),
    ]
]

menu_markup = InlineKeyboardMarkup(inline_keyboard=menu_kb)

__all__ = ["menu_markup"]
