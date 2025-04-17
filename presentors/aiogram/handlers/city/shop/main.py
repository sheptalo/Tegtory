from aiogram import F, Router, types
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from domain.use_cases.shop import UCShop
from presentors.aiogram.kb import shop as kb
from presentors.aiogram.kb.callbacks import CityCB
from presentors.aiogram.messages import shop as msg
from presentors.shared.utils.auth import auth_user

router = Router()


@router.callback_query(F.data == CityCB.shop)
@auth_user
@inject
async def shop_list(
    call: types.CallbackQuery, uc_shop: FromDishka[UCShop]
):
    shops = await uc_shop.all()
    markup = kb.get_shop_list_markup(shops)
    await call.message.edit_caption(caption=msg.shop_list, reply_markup=markup)


@router.callback_query(F.data.startswith(f"{CityCB.shop}:"))
@auth_user
@inject
async def specific_shop_demand_list(
    call: types.CallbackQuery, uc_shop: FromDishka[UCShop]
):
    shop = await uc_shop.by_name(call.data.split(":")[1])
    demand_list = await uc_shop.get_product_list(shop, True)
    markup = kb.get_shop_demand_markup(demand_list)
    await call.message.edit_caption(
        caption=msg.specific_shop.format(
            shop.title,
            shop.description,
            "✅" if shop.delivery_required else "❌",
        ),
        reply_markup=markup,
    )
