from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

__kb = [
    [InlineKeyboardButton(text="Торговая точка", callback_data="shop")],
    [
        InlineKeyboardButton(text="К фабрике", url="t.me/TegtoryBot"),
        InlineKeyboardButton(text="Меню", callback_data="menu"),
    ],
]


city_markup = InlineKeyboardMarkup(inline_keyboard=__kb)
