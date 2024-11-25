from aiogram import Router, F, types

from bot import api

from config import not_enough_points
from replys import ecology_markup

router = Router()


@router.callback_query(F.data == "ecology_factory")
async def ecology_factory(call: types.CallbackQuery):
    await call.message.edit_caption(
        caption=f"""
Экология важный аспект любого завода.

Ваш завод экологичен на: {api.factory(call.from_user.id).ecology} единиц

Оборудование для повышения экологичности можно купить несколько раз.

Постепенно экологичность снова падает до 0
                                    """,
        reply_markup=ecology_markup,
    )


@router.callback_query(F.data.split(":")[0] == "ecology")
async def ecology_buy(call: types.CallbackQuery):
    amount = int(call.data.split(":")[1])
    player = api.player(call.from_user.id)
    if amount * 1000 + 50 > player.money:
        return await call.message.edit_text(
            not_enough_points, reply_markup=ecology_markup
        )
    player.money -= amount * 1000 + 50
    api.factory(call.message.chat.id).ecology += amount
    await ecology_factory(call)
