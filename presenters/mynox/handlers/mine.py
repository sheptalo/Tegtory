from aiogram import F, Router, types
from aiogram.types import InputMediaPhoto

from ..kb.mine import (
    mine_main_markup,
)

router = Router()


@router.callback_query(F.data == "mine")
async def mine_menu(call: types.CallbackQuery):
    await call.message.edit_caption(
        caption=str(), reply_markup=mine_main_markup
    )


@router.callback_query(F.data == "tunnels")
async def tunnels_menu(call: types.CallbackQuery):
    pass
    # await call.message.edit_media(
    #     media=InputMediaPhoto(
    #         media="",
    #         caption=f"Вы пришли в свои туннели, в какой отправитесь {' '.join(str(i) for i in [])}",
    #     ),
    # )


@router.callback_query(F.data == "tax")
async def tax_menu(call: types.CallbackQuery):
    pass


@router.callback_query(F.data == "mine-pay-tax")
async def pay_tax(call: types.CallbackQuery):
    await mine_menu(call)
