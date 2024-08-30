from aiogram import types, F, Router

from db import Factory, Player

from replys import tax_markup, back_factory


router = Router()


@router.callback_query(F.data == 'tax')
async def check_tax(call: types.CallbackQuery):
    factory = Factory(call.message.chat.id)
    if not factory.exists():
        return await call.message.answer('У вас нет фабрики а значит и налогов')
    tax = factory.tax
    if factory.tax == 0:
        return await call.message.edit_caption(caption='У вас нет налогов', reply_markup=back_factory)
    await call.message.edit_caption(caption=f'💸*Налоги на фабрику:* {tax}', reply_markup=tax_markup)


@router.callback_query(F.data == 'pay_tax')
async def pay_tax(call: types.CallbackQuery):
    player = Player(call.from_user.id)
    if call.message.chat.type == "private":
        factory = Factory(call.from_user.id)
    else:
        factory = Factory(call.message.chat.id)
    if player.money < factory.tax:
        return await call.message.answer('Недостаточно очков для оплаты налога')
    else:
        player.money -= factory.tax
        factory.tax = 0
        return await check_tax(call)
