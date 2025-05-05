from aiogram import F, Router, types
from dishka import FromDishka

from domain.use_cases.shop import UCShop
from presenters.aiogram.kb import CityCB
from presenters.aiogram.kb import shop as kb
from presenters.aiogram.messages import shop as msg

router = Router()


@router.callback_query(F.data == CityCB.shop)
async def shop_list(
    call: types.CallbackQuery, uc_shop: FromDishka[UCShop]
) -> None:
    shops = await uc_shop.all()
    markup = kb.get_shop_list_markup(shops)
    await call.message.edit_caption(caption=msg.shop_list, reply_markup=markup)
