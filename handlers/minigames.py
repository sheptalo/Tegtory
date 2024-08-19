import random
import time

from aiogram import Router, F, types

from Filters import FarmFilter
from MIddleWares.UserMiddleWare import UserMiddleWare
from bot import bot
from config import coff
from db import Factory, Player

router = Router()
router.message.middleware(UserMiddleWare())


def cost_get(message):
    if message.text.lower().split()[1] == 'все':
        return Player(message.from_user.id).money
    cost = message.text.lower().split()[1].replace(',', '')
    cost = cost.replace('к', '000')
    cost = int(cost)
    return cost


# region Биржа
@router.message(F.text.lower().split()[0] == 'биржа')
async def birzha_main(message: types.Message):
    player = Player(message.from_user.id)

    try:
        message.text.split()[1]
    except:
        return await message.answer('Добро пожаловать на биржу.\n'
                                    'Вы можете Вложиться в товары '
                                    'и возможно их цена выростет, а вы получите профит\n'
                                    'чтобы отправить деньги на биржу укажи сумму которую тебе не жалко'
                                    '\nпример: биржа 10000000')

    try:
        cost = int(cost_get(message))
    except:
        return await message.answer('Неправильно указана сумма денег отправляемая на биржу')
    if cost < 0 or cost > player.money:
        return await message.answer('Недостаточно очков')
    player.money -= cost
    a = coff
    ran = random.randint(0, 5)
    random.shuffle(a)
    final = float(cost) * float(a[ran])
    player.money += round(final)
    await message.answer('Результаты ваших инвестиций:\n\n'
                         f'Коэффициент роста валюты {a[ran]}'
                         f'\nПолучено в итоге {round(final):,}')


# endregion
@router.message(FarmFilter())
async def farm_main(message: types.Message):
    current_time = int(time.time())
    player = Player(message.from_user.id)
    _time = 86400
    if current_time - player.farm >= _time:
        player.farm = current_time
        time.sleep(0.1)
        bonus = random.randint(20, 200)
        await message.answer(f'бонус получен в размере {bonus} очков')
        player.money += bonus
    else:
        await message.answer(
            f'вы получали бонус сегодня до следующего бонуса {round((player.farm + _time - current_time) / 60 / 60, 5)} часа. ')


# region fighting
# @router.callback_query(F.data.split(':')[0] == 'no_fight')
async def no_fight(call: types.CallbackQuery):
    data = call.data.split(':')
    if int(data[1]) == call.from_user.id:
        Player(call.from_user.id).money += round(int(data[2]))
        await call.message.delete()


# @router.callback_query(F.data.split(':')[0] == 'accept_fight')
async def accept_fight(call: types.CallbackQuery):
    data = call.data.split(":")
    player1 = Player(int(data[1]))
    player2 = Player(call.from_user.id)
    if int(data[1]) != call.from_user.id and player2.money >= int(data[2]):
        player2.money -= int(data[2])
        await call.message.delete()
        await call.message.answer('Битва началась')
        factory_user_1 = find_factory_fight(int(data[1]))
        factory_user_2 = find_factory_fight(call.from_user.id)
        phrases = ['Уровень: ', 'Рабочие: ']
        check = ['level', 'workers']
        _text = ''
        counter1 = 0
        counter2 = 0
        for i in range(6):
            if factory_user_1[i] > factory_user_2[i]:
                _text += f'{phrases[i]}{factory_user_1[i]}>{factory_user_2[i]}\n'
                counter1 += 1
            elif factory_user_1[i] < factory_user_2[i]:
                _text += f'{phrases[i]}{factory_user_1[i]}<{factory_user_2[i]}\n'
                counter1 += 1
            else:
                pass

        _text += f'Итог {counter1} и {counter2}'
        if counter1 > counter2:
            await call.message.answer('Битва между двумя игроками завершилась.\n'
                                      f'Результаты: первый игрок: {counter1} < второй игрок: {counter2}\n'
                                      f'победил тот кто предложил битву.')
            await bot.send_message(int(data[1]), 'Вы против анонимного игрока\n' + _text)
            await bot.send_message(call.from_user.id, 'Анонимный игрок против вас\n' + _text)
            player1.rating += 1
            player2.rating -= 1

            player1.money += int(data[2]) * 2
        elif counter2 > counter1:
            await call.message.answer('Битва между двумя игроками завершилась.\n'
                                      f'Результаты: первый игрок: {counter1} < второй игрок: {counter2}\n'
                                      f'победил тот кто принял битву.')
            await bot.send_message(call.from_user.id, 'Анонимный игрок против вас\n' + _text)
            await bot.send_message(int(data[1]), 'Вы против анонимного игрока\n' + _text)

            player1.rating -= 1
            player2.rating += 1

            player2.money += int(data[2]) * 2

        elif counter2 == counter1:
            await call.message.answer('Битва между двумя игроками завершилась.\n'
                                      f'Результаты: первый игрок: {counter1} < второй игрок: {counter2}\n'
                                      f'Ничья')
            await bot.send_message(call.from_user.id, 'Анонимный игрок против вас\n' + _text)
            await bot.send_message(int(data[1]), 'Вы против анонимного игрока\n' + _text)
            player2.money += int(data[2]) * 2
            player1.money += int(data[2]) * 2


# endregion
# region factory fight
@router.message(F.text.lower().split()[0] == 'битва')
async def fight_main(message: types.Message):
    if message.chat.id < 0 and int(message.text.split()[1]) != 'null' and Factory(message.from_user.id).level >= 100:
        try:
            cost = cost_get(message)
            player = Player(message.from_user.id)
        except:
            return await message.answer('Неправильная ставка')
        if cost > player.money:
            return await message.answer('Недостаточно очков')
        if cost < 50000:
            return await message.answer('Минимальная ставка в сражениях 50,000 очков')
        await message.delete()

        keyboard = [
            [
                types.InlineKeyboardButton(text='Принять', callback_data=f'accept_fight:{message.from_user.id}:{cost}'),
                types.InlineKeyboardButton(text='Отменить', callback_data=f'no_fight:{message.from_user.id}:{cost}')
            ]
        ]

        markup = types.InlineKeyboardMarkup(inline_keyboard=keyboard)

        player.money -= cost
        await message.answer('Некий пользователь предложил по соревноваться в прокачке фабриками'
                             ' и узнать чья лучше\n'
                             '*За победу:* Рейтинг +1\n'
                             '*При поражении:* Рейтинг -1\n'
                             f'*Ставка:* {cost:,}', reply_markup=markup)
    else:
        await message.answer('Добро пожаловать в *битвы* сразитесь за право получить рейтинг и деньги.\n\n'
                             '*Требования* для участников битвы:\n'
                             'Уровень фабрики > 100\n'
                             'Мин. ставка 50,000\n'
                             '*Участие только в супергруппах*\n\n'
                             'Условие победы:\n'
                             'По общему счету ваша фабрика лучше фабрики соперника\n\n'
                             '*Пример:* битва 600000')

# endregion
