import random

from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot import api
from replys import lottery_markup, lottery_back_markup

router = Router()


@router.callback_query(F.data.lower() == 'лотерея')
async def lottery_main(call: CallbackQuery):
    await call.message.edit_text('🎟*Лотерея*🎟\n\n'
                                 'Здесь вы можете купить билеты для участия в лотереи.\n\n'
                                 '*Инфо:*\n'
                                 '*Бронзовый билет:\n*Цена - 5,000 очков, выйгрыш - 50,000 очков\n\n'
                                 '*Серебряный билет:\n*Цена - 100,000 очков, выйгрыш - 1,000,000 очков\n\n'
                                 '*Золотой билет:\n*Цена - 10,000,000 очков, выйгрыш - 1,000,000,000 очков\n\n'
                                 '*Столар билет:\n*Цена - 10 столар коинов, выйгрыш - 100 столар коинов\n\n'
                                 f'🎟Номера купленных билетов:{api.player(call.from_user.id).tickets}\n\n',
                                 reply_markup=lottery_markup)


@router.callback_query(F.data == 'bronze_ticket')
async def buy_bronze_ticket(call: CallbackQuery):
    player = api.player(call.from_user.id)
    new_ticket = random.randint(1000, 1500)
    while new_ticket in player.tickets.split():
        new_ticket = random.randint(1000, 1500)
    if player.money >= 5000:
        player.money -= 5000
        player.tickets = f'{player.tickets} {new_ticket}'
        print(player.tickets, new_ticket)
        await call.message.edit_text(f'Куплен бронзовый билет с номером {new_ticket}', reply_markup=lottery_back_markup)
    else:
        await call.message.edit_text("Не хватает очков", reply_markup=lottery_back_markup)


@router.callback_query(F.data == 'serebro_ticket')
async def buy_serebro_ticket(call: CallbackQuery):
    player = api.player(call.from_user.id)

    new_ticket = random.randint(10000, 15000)
    while new_ticket in player.tickets.split():
        new_ticket = random.randint(10000, 15000)
    if player.money >= 100000:
        player.money -= 100000
        player.tickets += f' {new_ticket}'
        await call.message.edit_text(f'Куплен серебряный билет с номером {new_ticket}',
                                     reply_markup=lottery_back_markup)
    else:
        await call.message.edit_text("Не хватает очков", reply_markup=lottery_back_markup)


@router.callback_query(F.data == 'gold_ticket')
async def buy_gold_ticket(call: CallbackQuery):
    player = api.player(call.from_user.id)
    new_ticket = random.randint(100000, 150000)
    while new_ticket in player.tickets.split():
        new_ticket = random.randint(100000, 150000)
    if player.money >= 10000000:
        player.money -= 10000000
        player.tickets += f' {new_ticket}'
        await call.message.edit_text(f'Куплен золотой билет с номером {new_ticket}', reply_markup=lottery_back_markup)
    else:
        await call.message.edit_text("Не хватает очков", reply_markup=lottery_back_markup)


@router.callback_query(F.data == 'stolar_ticket')
async def buy_stolar_ticket(call: CallbackQuery):
    player = api.player(call.from_user.id)
    new_ticket = random.randint(1000000, 1500000)
    while new_ticket in player.tickets.split():
        new_ticket = random.randint(1000000, 1500000)
    if player.stolar >= 10:
        player.stolar -= 10
        player.tickets += f' {new_ticket}'
        await call.message.edit_text(f'Куплен столар билет с номером {new_ticket}', reply_markup=lottery_back_markup)
    else:
        await call.message.edit_text("Не хватает столар коинов", reply_markup=lottery_back_markup)


# endregion
