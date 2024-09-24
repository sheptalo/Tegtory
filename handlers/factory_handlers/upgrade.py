from aiogram import Router, types, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import InputMediaPhoto, URLInputFile

from api import api

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
    # await call.message.edit_caption(caption=text, reply_markup=upgrade_markup)
    try:
        await call.message.edit_media(media=InputMediaPhoto(media=URLInputFile(factory_image(factory.type)),
                                                            caption=text), reply_markup=upgrade_markup)
    except TelegramBadRequest:
        pass


@router.callback_query(F.data == 'upgrade_factory_conf')
async def upgrade_factory(call: types.CallbackQuery):
    player = api.player(call.from_user.id)

    if player.isWorking:
        return await call.message.answer(f'Во время работы нельзя прокачивать фабрику')

    factory = api.factory(call.message.chat.id)
    lvl = factory.lvl

    if lvl < 500:
        if player.money >= (lvl + 3) * 400:
            player.money -= (lvl + 3) * 400
        else:
            return await call.message.answer(not_enough_points)
    else:
        if player.stolar < lvl - 499:
            return await call.message.answer('Недостаточно столар коинов')
        else:
            player.stolar -= (lvl - 499)
    print(factory.lvl)
    factory.lvl += 1
    factory.started_work_at = 0
    print(factory.lvl)
    await upgrade_factory_price(call)
