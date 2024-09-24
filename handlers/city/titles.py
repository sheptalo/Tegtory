# region titles
from aiogram import F, Router
from aiogram.types import CallbackQuery

from config import not_enough_points
from db import Leaderboard
from replys import titles_shop_markup, title_error_markup
from api import api

router = Router()
title_shop = """
Добро пожаловать в магазин *титулов!*
вы можете приобрести следующие титулы

*Богач* - 1млн очков.
*Магнат* - 100,000,000 очков и уровень фабрики выше 100.

*Один из лучших* - можно получить когда ты находишься в топ 3 по деньгам.

*Эколог* - Баллы вашей экологии больше 500.

*Хранитель* - У вас на фабрике Более 5000 товаров.

*Качественный* - скоро будет доступен.

Ассортимент будет пополняться
"""
have_title = 'У вас уже есть этот титул'


@router.callback_query(F.data == 'титулы')
async def buy_title_main(call: CallbackQuery):
    if not api.factory(call.from_user.id).exists():
        return await call.message.answer('Без фабрики вас не пустят в магазин титулов.')
    await call.message.edit_text(title_shop, reply_markup=titles_shop_markup)


@router.callback_query(F.data.split(':')[0] == 'buy_title')
async def buy_title_call(call: CallbackQuery):
    player = api.player(call.from_user.id)
    factory = api.factory(call.from_user.id)
    title = call.data.split(":")[1]

    if title == 'Богач':
        if player.money < 1000000:
            return await call.message.edit_text(not_enough_points, reply_markup=title_error_markup)

        if 'Богач' in player.titles.split():
            return await call.message.edit_text(have_title, reply_markup=title_error_markup)

        player.money -= 1000000

        player.titles += " Богач"

    elif title == 'Магнат':
        if player.money < 100000000:
            return await call.message.edit_text(not_enough_points, reply_markup=title_error_markup)

        if "Магнат" in player.titles.split():
            return await call.message.edit_text(have_title, reply_markup=title_error_markup)

        if factory.lvl < 100:
            return await call.message.edit_text('недостаточный уровень', reply_markup=title_error_markup)

        player.money -= 100000000
        player.titles += ' Магнат'

    elif title == 'Один_из_лучших' and Leaderboard().Money().me(api.player(call.from_user.id).iternal_id) <= 3:
        if 'Один_из_лучших' in player.titles.split():
            return call.message.edit_text('У вас уже есть этот титул', reply_markup=title_error_markup)

        player.titles += ' Один_из_лучших'

    elif title == 'Эколог' and api.factory(call.from_user.id).eco >= 500:
        if 'Эколог' in player.titles.split():
            return call.message.edit_text('У вас уже есть этот титул', reply_markup=title_error_markup)

        player.titles += ' Эколог'

    elif title == 'Хранитель' and api.factory(call.from_user.id).stock > 5000:
        if 'Хранитель' in player.titles.split():
            return call.message.edit_text('У вас уже есть этот титул', reply_markup=title_error_markup)

        player.titles += ' Хранитель'

    await call.message.edit_text(f'Куплен титул *{player.titles.split()[-1]}* ', reply_markup=title_error_markup)


# endregion
