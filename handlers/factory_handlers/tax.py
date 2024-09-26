from aiogram import types, F, Router

from api import api

from replys import tax_markup, back_factory


router = Router()


@router.callback_query(F.data == 'tax')
async def check_tax(call: types.CallbackQuery):
    factory = api.factory(call.message.chat.id)
    if not factory.exists():
        return await call.answer('У вас нет фабрики а значит и налогов', show_alert=True)
    tax = factory.tax
    if tax == 0:
        return await call.message.edit_caption(caption='У вас нет налогов', reply_markup=back_factory)
    await call.message.edit_caption(caption=f'💸*Налоги на фабрику:* {tax}', reply_markup=tax_markup)


@router.callback_query(F.data == 'pay_tax')
async def pay_tax(call: types.CallbackQuery):
    player = api.player(call.from_user.id)
    factory = api.factory(call.message.chat.id)
    if player.money < factory.tax:
        return await call.answer('Недостаточно очков для оплаты налога', show_alert=True)
    else:
        player.money -= factory.tax
        factory.tax = 0
        return await check_tax(call)
