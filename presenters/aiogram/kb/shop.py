from aiogram.types import InlineKeyboardMarkup, LabeledPrice
from aiogram.utils.keyboard import InlineKeyboardBuilder

from domain.entities import Shop, ShopProduct
from presenters.aiogram.kb.callbacks import CityCB


def get_shop_list_markup(shops: list[Shop]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for shop in shops:
        builder.button(
            text=shop.title, callback_data=f"{CityCB.shop}:{shop.title}"
        )
    builder.button(text="назад", callback_data=CityCB.back)
    builder.adjust(1, repeat=True)
    return builder.as_markup()


def shop_demand_markup(products: list[ShopProduct]) -> InlineKeyboardMarkup:
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
            callback_data=f"{CityCB.preview_contract}:{product.shop.title}:{product.product.name}:{available_amount}",
        )
    builder.adjust(4, repeat=True)
    builder.button(
        text="назад", callback_data=f"{CityCB.shop}:{product.shop.title}"
    )
    return builder.as_markup()


prices = [LabeledPrice(label="1000 очков XTR", amount=10)]
