from aiogram.types import (
    InlineKeyboardMarkup,
    LabeledPrice,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from domain.entity import Shop, ShopProduct
from presentors.aiogram.kb.callbacks import CityCB


def get_shop_list_markup(shops: list[Shop]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for shop in shops:
        builder.button(
            text=shop.title, callback_data=f"{CityCB.shop}:{shop.title}"
        )
    builder.button(text="назад", callback_data=CityCB.back)
    builder.adjust(1, repeat=True)
    return builder.as_markup()


def shop_demand_markup(
    products: list[ShopProduct],
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for product in products:
        builder.button(
            text=f"{product.product.name} - {product.amount}",
            callback_data=f"{CityCB.choose_amount}:{product.id}",
        )
    builder.adjust(2, repeat=True)
    builder.button(text="назад", callback_data=CityCB.shop)

    return builder.as_markup()


def choose_amount_demand_markup(
    product: ShopProduct, step: int = 0
) -> InlineKeyboardMarkup:
    if not step:
        step = int(product.amount * 0.05) + 1
    builder = InlineKeyboardBuilder()
    available_amounts = [
        i for i in range(product.amount // 10, product.amount // 2, step)
    ]
    for available_amount in available_amounts:
        builder.button(
            text=str(available_amount),
            callback_data=f"{CityCB.preview_contract}:{product.shop.title}:{product.product.id}:{available_amount}",
        )
    builder.adjust(4, repeat=True)
    builder.button(
        text="назад", callback_data=f"{CityCB.shop}:{product.shop.title}"
    )
    return builder.as_markup()


prices = [LabeledPrice(label="1000 очков XTR", amount=10)]

# lottery_kb = [
#     [
#         InlineKeyboardButton(
#             text="Купить бронзовый билет", callback_data="bronze_ticket"
#         )
#     ],
#     [
#         InlineKeyboardButton(
#             text="Купить Серебряный билет", callback_data="serebro_ticket"
#         )
#     ],
#     [
#         InlineKeyboardButton(
#             text="Купить золотой билет", callback_data="gold_ticket"
#         )
#     ],
#     [
#         InlineKeyboardButton(
#             text="Купить Столар билет", callback_data="stolar_ticket"
#         )
#     ],
#     [InlineKeyboardButton(text="Обратно", callback_data="back_shop")],
# ]
# lottery_markup = InlineKeyboardMarkup(inline_keyboard=lottery_kb)
