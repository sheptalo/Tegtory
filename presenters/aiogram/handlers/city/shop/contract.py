from aiogram import Router, types
from dishka import FromDishka

from domain.context import UserFactoryContext
from domain.use_cases.shop import UCShop
from presenters.aiogram.kb import shop as kb
from presenters.aiogram.messages import shop as msg
from presenters.shared.utils import get_factory, get_user, with_context

router = Router()


@get_user
@get_factory
@with_context(UserFactoryContext)
async def choose_amount(
    call: types.CallbackQuery,
    _: UserFactoryContext,
    uc_shop: FromDishka[UCShop],
) -> None:
    product = await uc_shop.shop_product_by_id(int(call.data.split(":")[1]))
    if not product:
        raise ValueError
    markup = kb.choose_amount_demand_markup(product)
    await call.message.edit_caption(
        caption=msg.choose_amount, reply_markup=markup
    )


@get_user
@get_factory
@with_context(UserFactoryContext)
async def preview_contract(
    call: types.CallbackQuery,
    ctx: UserFactoryContext,
    uc_shop: FromDishka[UCShop],
) -> None:
    await uc_shop.shop_product_by_id(int(call.data.split(":")[2]))
    int(call.data.split(":")[3])


@get_user
@get_factory
@with_context(UserFactoryContext)
async def sign_contract(
    call: types.CallbackQuery,
    ctx: UserFactoryContext,
    uc_shop: FromDishka[UCShop],
) -> None:
    pass
