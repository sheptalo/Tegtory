from aiogram import Router, types
from dishka import FromDishka

from domain import entities
from domain.use_cases.shop import UCShop
from presenters.aiogram.kb import shop as kb
from presenters.aiogram.messages import shop as msg
from presenters.shared.utils import get_factory

router = Router()


@get_factory
async def choose_amount(
    call: types.CallbackQuery,
    factory: entities.Factory,
    uc_shop: FromDishka[UCShop],
) -> None:
    product = await uc_shop.shop_product_by_id(int(call.data.split(":")[1]))
    if not product:
        raise ValueError
    markup = kb.choose_amount_demand_markup(product)
    await call.message.edit_caption(
        caption=msg.choose_amount, reply_markup=markup
    )


@get_factory
async def preview_contract(
    call: types.CallbackQuery,
    factory: entities.Factory,
    uc_shop: FromDishka[UCShop],
) -> None:
    await uc_shop.shop_product_by_id(int(call.data.split(":")[2]))
    int(call.data.split(":")[3])


@get_factory
async def sign_contract(
    call: types.CallbackQuery,
    uc_shop: FromDishka[UCShop],
) -> None:
    pass
