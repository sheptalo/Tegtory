from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

menu_kb = [
    [KeyboardButton(text="Фабрика"), KeyboardButton(text="Город")],
    [KeyboardButton(text="Помощь")],
    [KeyboardButton(text="Биржа")],
]
menu_reply = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=menu_kb)

rinok_kb = [
    [
        InlineKeyboardButton(
            text="Продать на @tegtoryshop", callback_data="sellonrinok"
        ),
        InlineKeyboardButton(text="Купить", callback_data="buy_stolar_coin:1"),
    ],
    [
        InlineKeyboardButton(
            text="Купить 10x", callback_data="buy_stolar_coin:100"
        ),
        InlineKeyboardButton(
            text="Купить 100x", callback_data="buy_stolar_coin:100"
        ),
    ],
    [InlineKeyboardButton(text="Обратно", callback_data="city")],
]
rinok_markup = InlineKeyboardMarkup(inline_keyboard=rinok_kb)

old_seasons_kb = [
    [
        InlineKeyboardButton(
            text="Сезон pre-alpha", callback_data="pre_apha_season"
        )
    ],
    [InlineKeyboardButton(text="Сезон alpha", callback_data="alpha_season")],
    [InlineKeyboardButton(text="Обратно", callback_data="leaderboard")],
]
old_seasons_markup = InlineKeyboardMarkup(inline_keyboard=old_seasons_kb)


market_kb = [
    [InlineKeyboardButton(text="Продать", callback_data="sell_on_market")],
    [InlineKeyboardButton(text="Обратно", callback_data="city")],
]
market_markup = InlineKeyboardMarkup(inline_keyboard=market_kb)

back_shop_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Обратно", callback_data="back_shop")]
    ]
)

lottery_back_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Обратно", callback_data="Лотерея")]
    ]
)

back_city = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Обратно", callback_data="city")]
    ]
)

back_exchange = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data="рынок")]
    ]
)
