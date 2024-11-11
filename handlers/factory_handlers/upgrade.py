from aiogram import Router, types, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import InputMediaPhoto

from bot import api

from replys import upgrade_markup
from config import not_enough_points, factory_image

router = Router()


@router.callback_query(F.data == 'upgrade_factory')
async def upgrade_factory_price(call: types.CallbackQuery):
    factory = api.factory(call.message.chat.id)
    lvl = factory.lvl
    text = (f'Текущий уровень {lvl}\n'
            f'Стоимость улучшения '
            f'{f'{(lvl + 3) * 400} очков' if lvl < 500 else f'{lvl - 499} столар'}\n'
            f'улучшить?')
    try:
        await call.message.edit_media(media=InputMediaPhoto(media=factory_image(factory.type),
                                                            caption=text), reply_markup=upgrade_markup)
    except TelegramBadRequest:
        pass


@router.callback_query(F.data == 'upgrade_factory_conf')
async def upgrade_factory(call: types.CallbackQuery):
    player = api.player(call.from_user.id)

    if player.isWorking:
        return await call.answer(f'Во время работы нельзя прокачивать фабрику', show_alert=True)

    factory = api.factory(call.message.chat.id)
    lvl = factory.lvl
    money, stolar = player.get('money,stolar')
    if lvl < 500:
        if money >= (lvl + 3) * 400:
            player.money -= (lvl + 3) * 400
        else:
            return await call.answer(not_enough_points, show_alert=True)
    else:
        if stolar < lvl - 499:
            return await call.answer('Недостаточно столар коинов', show_alert=True)
        else:
            player.stolar -= (lvl - 499)

    factory.set({
        'started_work_at': 0,
        'lvl': lvl + 1,
    })
    await upgrade_factory_price(call)
