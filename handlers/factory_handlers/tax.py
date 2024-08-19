from aiogram import types, F, Router

from db.Player import Player
from db.Factory import Factory

from replys import tax_markup
# region TAX

router = Router()
@router.callback_query(F.data == 'tax')
async def check_tax(call: types.CallbackQuery):
    factory = Factory(call.message.chat.id)
    if not factory.exists():
        return await call.message.answer('У вас нет фабрики а значит и налогов')
    tax = factory.tax
    await call.message.edit_caption(caption=f'💸*Налоги на фабрику:*\n\n'
                            f'💸*Налоги на электричество:* {round(tax * 0.05, 3)} очков \n'
                            f'💸*Налоги на прозводство:* {round(tax * 0.15, 3)} очков \n'
                            f'💸*Налог на землю:* {round(tax * 0.1)}\n'
                            f'💸*Налог на Оборудование:* {round(tax * 0.2)} \n'
                            f'💸*Налог на название фабрики:* {round(tax * 0.5)} \n\n'
                            f'💸💸*итоговая сумма налогов:* {tax}',
                            reply_markup=tax_markup,
                            parse_mode='Markdown')


@router.callback_query(F.data == 'pay_tax')
async def pay_tax(call: types.CallbackQuery):
    player = Player(call.from_user.id)
    if call.message.chat.type == "private":
        factory = Factory(call.from_user.id)
    else:
        factory = Factory(call.message.chat.id)
    if factory.tax == 0:
        return await call.message.answer('У вас нет налогов')
    elif player.money < factory.tax:
        return await call.message.answer('Недостаточно очков для оплаты налога')
    else:
        player.money -= factory.tax
        factory.tax = 0
        return await check_tax(call)


# endregion