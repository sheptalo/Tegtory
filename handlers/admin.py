from aiogram import Router, F, types
import random

from db import Player
from globalFunc import league
from bot import bot
from globalFunc.lottery import give_money_l
from aiogram.filters import Command

router = Router()


# region admin commands
def param(message, _int):
    try:
        param1 = message.text.split()[_int]
    except:
        param1 = 'null'

    return param1


@router.message(Command('Лотерея'))
async def lottery_start(message: types.Message):
    if int(message.from_user.id) != 1405684214:
        return
    await message.delete()
    win_tickets_bronze = ' '
    win_tickets_serebro = ' '
    win_tickets_gold = ' '
    win_tickets_stolar = ' '
    for i in range(100):
        win_tickets_bronze += f' {random.randint(1000, 1500)}'

    for i in range(1000):
        win_tickets_serebro += f' {random.randint(10000, 15000)}'

    for i in range(100000):
        win_tickets_gold += f' {random.randint(100000, 150000)}'

    for i in range(1000000):
        win_tickets_stolar += f' {random.randint(1000000, 1500000)}'

    counter = 0
    win_tickets_bronze_text = ''
    for i in win_tickets_bronze.split():
        if counter > 10:
            continue
        win_tickets_bronze_text += f' {i},'
        counter += 1
    counter = 0
    win_tickets_serebro_text = ''
    for i in win_tickets_serebro.split():
        if counter > 10:
            continue
        win_tickets_serebro_text += f' {i},'
        counter += 1
    counter = 0
    win_tickets_gold_text = ''
    for i in win_tickets_gold.split():
        if counter > 10:
            continue
        win_tickets_gold_text += f' {i},'
        counter += 1
    counter = 0
    win_tickets_stolar_text = ''
    for i in win_tickets_stolar.split():
        if counter > 10:
            continue
        win_tickets_stolar_text += f' {i},'
        counter += 1
    text = ('*Розыгрыш* билетов *произошел*, '
            'к сожалению все номера выигрышных билеты показать не получиться, но вот *некоторые* из них:\n\n'
            f'*Бронзовые билеты:* {win_tickets_bronze_text}...\n\n'
            f'*Серебряные билеты:* {win_tickets_serebro_text}...\n\n'
            f'*Золотые билеты:* {win_tickets_gold_text}...\n\n'
            f'*Столар билеты:* {win_tickets_stolar_text}...')
    _user = await give_money_l(win_tickets_bronze, win_tickets_serebro, win_tickets_gold, win_tickets_stolar)
    await bot.send_message('@tegtory', text)
    for user in _user:
        Player(str(user[1])).money += user[0]
        Player(user[1]).stolar_coin += user[3]
        await bot.send_message(user[1], f'Ваш билет {user[2]} выйграл')


@router.message(Command('обновить_лиги'))
async def update_leagues(message: types.Message):
    if int(message.from_user.id) == 1405684214:
        league.league()
        await message.answer("Лиги обновлены")


# endregion
