from aiogram import F, Router, types
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from domain.entity import Factory, User
from domain.use_cases.shop import UCShop
from presentors.aiogram.kb import shop as kb
from presentors.aiogram.kb.callbacks import CityCB
from presentors.aiogram.messages import shop as msg
from presentors.shared.utils.auth import auth_user, have_factory

router = Router()


@router.callback_query(F.data.startswith(f"{CityCB.choose_amount}:"))
@auth_user
@have_factory
@inject
async def choose_amount(
    call: types.CallbackQuery,
    uc_shop: FromDishka[UCShop]
):
    product = await uc_shop.specific_shop_product_by_id(
        int(call.data.split(":")[1])
    )
    markup = kb.get_choose_amount_demand_markup(product)
    await call.message.edit_caption(
        caption=msg.choose_amount, reply_markup=markup
    )


# @router.callback_query()
@auth_user
@have_factory
async def sign_contract(
    call: types.CallbackQuery,
    user: User,
    factory: Factory,
    uc_shop: FromDishka[UCShop],
):
    pass
