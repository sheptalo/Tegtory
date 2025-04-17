from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

back_city = InlineKeyboardButton(text="Обратно", callback_data="city")


__kb = [
    [
        InlineKeyboardButton(text="Продать", callback_data="sell"),
    ],
    [
        InlineKeyboardButton(text="Найм работников", callback_data="hire"),
    ],
    [
        InlineKeyboardButton(
            text="Вызвать бригаду для подготовки нового туннеля",
            callback_data="create_tunnel",
        ),
    ],
    [
        InlineKeyboardButton(text="Оборудование", callback_data="equipment"),
    ],
    [back_city],
]


shop_markup = InlineKeyboardMarkup(inline_keyboard=__kb)
back_shop = InlineKeyboardButton(text="Обратно", callback_data="shop")

__kb = [
    [
        InlineKeyboardButton(text="Продать всё", callback_data="sall_all"),
    ],
    [back_shop],
]

sell_markup = InlineKeyboardMarkup(inline_keyboard=__kb)

__kb = [
    [
        InlineKeyboardButton(text="Вызвать", callback_data="call_workers"),
    ],
    [
        back_shop,
    ],
]

create_tunnel_markup = InlineKeyboardMarkup(inline_keyboard=__kb)


def hire_tunnels_markup(ids):
    builder = InlineKeyboardBuilder()
    for i in ids:
        builder.button(text=f"номер {i}", callback_data="hire")
    builder.button(text="Назад", callback_data="shop")
    return builder.as_markup()


__kb = [
    [
        InlineKeyboardButton(
            text="Купить новое оборудование", callback_data="buy_equipment"
        ),
    ],
    [
        back_shop,
    ],
]

buy_equipment_markup = InlineKeyboardMarkup(inline_keyboard=__kb)
