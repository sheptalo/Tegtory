import asyncio
import random
import time

from aiogram import Router, F, types

from Filters import FarmFilter
from MIddleWares.UserMiddleWare import UserMiddleWare
from db import Factory, Player

router = Router()
router.message.middleware(UserMiddleWare())
coff = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.4, 1.7]


def cost_get(message) -> int:
    if message.text.lower().split()[1] == 'все':
        return Player(message.from_user.id).money
    cost = message.text.lower().split()[1].replace(',', '')
    cost = cost.replace('к', '000')
    cost = int(cost)
    return abs(cost)


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
        cost = cost_get(message)
    except:
        return await message.answer('Неправильно указана сумма денег отправляемая на биржу')

    if cost > player.money:
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


@router.callback_query(F.data.split(':')[0] == 'no_fight')
async def no_fight(call: types.CallbackQuery):
    data = call.data.split(':')
    if int(data[1]) == call.from_user.id:
        Player(call.from_user.id).money += round(int(data[2]))
        await call.message.delete()


@router.callback_query(F.data.split(':')[0] == 'accept_fight')
async def accept_fight(call: types.CallbackQuery):
    data = call.data.split(":")
    player1 = Player(int(data[1]))
    player2 = Player(call.from_user.id)
    if int(data[1]) != call.from_user.id and player2.money >= int(data[2]):
        player2.money -= int(data[2])
        await call.message.delete()
        await call.message.answer('Инспектор начал инспекцию')
        factory_user_1 = Factory(int(data[1]))
        factory_user_2 = Factory(call.from_user.id)
        check = ['level', 'workers', 'eco', 'stock']
        counter = 0

        for i in range(len(check)):
            counter += 1 if factory_user_1[check[i-1]] > factory_user_1[check[i-1]] else 0

        counter2 = len(check) - counter
        await asyncio.sleep(3)
        if counter > counter2:
            await call.message.answer('Инспекция проведена.\n'
                                      f'По ее результатам инспектор прибавляет рейтинг к фабрике *{factory_user_1.name}*')
            player1.rating += 1
            player2.rating -= 1

            player1.money += int(data[2]) * 2
        elif counter2 > counter:
            await call.message.answer('Инспекция проведена.\n'
                                      f'По ее результатам инспектор прибавляет рейтинг к фабрике *{factory_user_2.name}*')

            player1.rating -= 1
            player2.rating += 1

            player2.money += int(data[2]) * 2

        elif counter2 == counter:
            await call.message.answer('Инспекция проведена.\n'
                                      'По ее результатам инспектор не прибавляет рейтинг ни одной фабрике')
            player2.money += int(data[2])
            player1.money += int(data[2])


@router.message(F.text.lower().split()[0] == 'инспекция')
async def fight_main(message: types.Message):
    if message.chat.type != 'private' and int(message.text.split()[1]) != 'null' and Factory(message.from_user.id).level >= 50:
        try:
            cost = cost_get(message)
            player = Player(message.from_user.id)
        except:
            return await message.answer('Неправильная сумма')

        if cost > player.money:
            return await message.answer('Недостаточно очков')

        if cost < 50000:
            return await message.answer('Минимальная стоимость инспекции 50.000')

        await message.delete()

        keyboard = [
            [
                types.InlineKeyboardButton(text='Принять', callback_data=f'accept_fight:{message.from_user.id}:{cost}'),
                types.InlineKeyboardButton(text='Отменить', callback_data=f'no_fight:{message.from_user.id}:{cost}')
            ]
        ]

        markup = types.InlineKeyboardMarkup(inline_keyboard=keyboard)

        player.money -= cost
        await message.answer(f'Владелец фабрики предложил провести инспекцию стоимостью в {cost:,},'
                             f' Тот кто не получит рейтинг от инспектора оплачивает ее', reply_markup=markup)
    else:
        await message.answer('Добро пожаловать в центр инспекции.\n\n'
                             '*Требования* для проведения инспекции:\n'
                             'Количество владельцев: 2\n'
                             'Уровень фабрики > 50\n'
                             'Мин. стоимость 50,000\n'
                             '*Участие только в супергруппах*\n\n'
                             'Условие победы:\n'
                             'Рейтинг получает та фабрика, которая по мнению инспектора лучше.'
                             '*Пример:* инспекция 600000')

