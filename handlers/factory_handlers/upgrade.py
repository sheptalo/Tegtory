from aiogram import Router, types, F
from aiogram.types import InputMediaPhoto, URLInputFile

from db import Factory, Player

from replys import upgrade_markup
from config import not_enough_points, factory_image
from .work_yourself import work_by_yourself

router = Router()


@router.callback_query(F.data == 'upgrade_factory')
async def upgrade_factory_price(call: types.CallbackQuery):
    player = Player(call.from_user.id)
    if player.is_working:
        return await work_by_yourself(call)
    factory = Factory(call.message.chat.id)
    lvl = factory.level
    text = (f'Текущий уровень {lvl}\n'
            f'Стоимость улучшения '
            f'{f'{(lvl + 3) * 400} очков' if lvl < 500 else f'{lvl - 499} столар'}\n'
            f'улучшить?')
    # await call.message.edit_caption(caption=text, reply_markup=upgrade_markup)
    await call.message.edit_media(media=InputMediaPhoto(media=URLInputFile(factory_image(factory.type)),
                                                        caption=text),
                                  reply_markup=upgrade_markup)


@router.callback_query(F.data == 'upgrade_factory_conf')
async def upgrade_factory(call: types.CallbackQuery):
    player = Player(call.from_user.id)

    if player.is_working:
        return await call.message.answer(f'Во время работы нельзя прокачивать фабрику')

    factory = Factory(call.message.chat.id)
    lvl = factory.level

    if lvl < 500:
        if player.money >= (lvl + 3) * 400:
            player.money -= (lvl + 3) * 400
        else:
            return await call.message.answer(not_enough_points)
    else:
        if player.stolar < lvl - 499:
            return await call.message.answer('Недостаточно столар коинов')
        else:
            player.stolar -= lvl - 499
    lvl += 1
    factory.level = lvl
    factory.start_work_at = 0
    await upgrade_factory_price(call)
