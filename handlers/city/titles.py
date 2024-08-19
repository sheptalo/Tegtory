# region titles
from aiogram import F, Router
from aiogram.types import CallbackQuery

from config import title_shop, not_enough_points, have_title
from db import Player, Factory, Leaderboard
from replys import titles_shop_markup, title_error_markup

router = Router()


@router.callback_query(F.data == 'титулы')
async def buy_title_main(call: CallbackQuery):
    await call.message.edit_text(title_shop, reply_markup=titles_shop_markup)


@router.callback_query(F.data.split(':')[0] == 'buy_title')
async def buy_title_call(call: CallbackQuery):
    player = Player(call.from_user.id)
    factory = Factory(call.from_user.id)
    bought = ''
    title = call.data.split(":")[1]

    if title == 'Богач':
        if player.money < 1000000:
            return await call.message.edit_text(not_enough_points, reply_markup=title_error_markup)

        if 'Богач' in player.titles.split():
            return await call.message.edit_text(have_title, reply_markup=title_error_markup)

        player.money -= 1000000

        player.titles += " Богач"

        bought = 'Богач'

    elif title == 'Магнат':
        if player.money < 100000000:
            return await call.message.edit_text(not_enough_points, reply_markup=title_error_markup)

        if "Магнат" in player.titles.split():
            return await call.message.edit_text(have_title, reply_markup=title_error_markup)

        if factory.level < 100:
            return await call.message.edit_text('недостаточный уровень', reply_markup=title_error_markup)

        player.money -= 100000000
        player.titles += ' Магнат'
        bought = 'Магнат'

    elif title == 'Один_из_лучших' and Leaderboard().Money().me(Player(call.from_user.id).iternal_id) <= 3:
        if 'Один_из_лучших' in player.titles.split():
            return call.message.edit_text('У вас уже есть этот титул', reply_markup=title_error_markup)

        player.titles += ' Один_из_лучших'

        bought = 'Один из лучших'
    await call.message.edit_text(f'Куплен титул *{bought}* ', reply_markup=title_error_markup)


# endregion
