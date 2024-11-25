from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from states import SellStock
from bot import api
from replys import market_markup, back_city, create_factory_markup


router = Router()


@router.callback_query(F.data == "маркет")
async def market(call: CallbackQuery):
    if not api.factory(call.from_user.id).exist:
        return await call.message.edit_text(
            "На маркете продают товары только магнаты.",
            reply_markup=create_factory_markup,
        )
    await call.message.edit_text(
        "Продайте свой товар на маркете, осторожно цена может упасть в любой момент\n"
        f"Текущая цена: {api.player(1).get_stock()} за штуку",
        reply_markup=market_markup,
    )


@router.callback_query(F.data == "sell_on_market")
async def sell_on_market(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        f"Введите сколько хотите продать товара. У вас есть {api.factory(call.from_user.id).stock}",
        reply_markup=back_city,
    )
    await state.set_state(SellStock().stock)


@router.message(SellStock().stock)
async def amount_to_sell(message: Message, state: FSMContext):
    try:
        amount = abs(int(message.text))
    except:
        return await message.answer("Неправильное количество /cancel")

    price = api.player(1).get_stock()
    factory = api.factory(message.from_user.id)
    if amount > factory.stock:
        return await message.answer("Нехватает товара")

    factory.stock -= amount
    api.player(message.from_user.id).money += amount * price
    await message.answer("Успешно продано")
    await state.clear()
