from aiogram import F, Router, types

from ..kb.shop import (
    shop_markup,
)

router = Router()


@router.callback_query(F.data == "shop")
async def shop(call: types.CallbackQuery):
    await call.message.edit_caption(
        caption="Вы отправились в торговую точку, здесь вы можете купить услуги или же продать накопленное",
        reply_markup=shop_markup,
    )


@router.callback_query(F.data == "sell")
async def sell(call: types.CallbackQuery):
    pass


@router.callback_query(F.data == "create_tunnel")
async def create_tunnel(call: types.CallbackQuery):
    pass


@router.callback_query(F.data == "hire")
async def hire_to_tunnel(call: types.CallbackQuery):
    pass


@router.callback_query(F.data == "equipment")
async def buy_equipment(call: types.CallbackQuery):
    pass
