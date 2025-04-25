from aiogram import F, Router, types
from dishka import FromDishka

from domain.context.factory import UserFactoryContext
from domain.use_cases.shop import UCShop
from presentors.aiogram.kb import shop as kb
from presentors.aiogram.kb.callbacks import CityCB
from presentors.aiogram.messages import shop as msg
from presentors.shared.utils.auth import get_factory, get_user
from presentors.shared.utils.di_context import with_context

router = Router()


@router.callback_query(F.data.startswith(f"{CityCB.choose_amount}:"))
@get_user
@get_factory
@with_context(UserFactoryContext)
async def choose_amount(
    call: types.CallbackQuery,
    _: UserFactoryContext,
    uc_shop: FromDishka[UCShop],
) -> None:
    product = await uc_shop.shop_product_by_id(int(call.data.split(":")[1]))
    markup = kb.choose_amount_demand_markup(product)
    await call.message.edit_caption(
        caption=msg.choose_amount, reply_markup=markup
    )


# @router.callback_query(F.data.startswith(f"{CityCB.preview_contract}:"))
# @get_user
# @get_factory
# @with_context(UserFactoryContext)
# async def preview_contract(
#     call: types.CallbackQuery,
#     ctx: UserFactoryContext,
#     uc_shop: FromDishka[UCShop],
# ):
#     product = await uc_shop.shop_product_by_id(int(call.data.split(":")[2]))
#     amount = int(call.data.split(":")[3])
# shop_product = ShopProduct(
#     product=product,
#     amount=amount,
#     shop=shop
# )
#     contract = await uc_shop.preview_contract(ctx.factory)
#     await call.message.edit_caption(str(contract), reply_markup=None)


# @router.callback_query(F.data.startswith(f"{CityCB.success_contract}:"))
# @get_user
# @get_factory
# @with_context(UserFactoryContext)
# async def sign_contract(
#     call: types.CallbackQuery,
#     ctx: UserFactoryContext,
#     uc_shop: FromDishka[UCShop],
# ):
#     pass
