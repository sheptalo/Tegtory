from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton

from States import SellStolar
from bot import bot
from config import not_enough_points
from db import Player
from replys import rinok_markup

router = Router()


@router.callback_query(F.data == 'рынок')
async def shop_stolar(call: CallbackQuery):
    await call.message.edit_text('🌟 Добро пожаловать на рынок! 🌟 Я - торговец столар коинов.'
                                 '\n🪙 Я могу продать вам парочку за 1 млрд штука.\n'
                                 '🤩 Но если вам это не подходит, '
                                 'можете заглянуть на наш магазин @tegtoryshop для большего выбора. 🛍️🔥',
                                 reply_markup=rinok_markup)


@router.callback_query(F.data == 'sellonrinok')
async def sell_stolar_on_tegtory(call: CallbackQuery):
    await call.message.answer('чтобы продать на @tegtoryshop пиши: продать')


@router.message(F.text.lower().split()[0] == 'продать')
async def sell_on_channel(message: Message, state: FSMContext):
    await message.answer('Будет выставлен лот в канале @tegtoryshop.\n'
                         'Введите количество столар коинов на продажу, их сразу спишут')
    await state.set_state(SellStolar.stolar_on_sell)


@router.message(StateFilter(SellStolar.stolar_on_sell))
async def set_stolar_for_sale(message: Message, state: FSMContext):
    amount = message.text
    player = Player(message.from_user.id)

    if player.stolar < int(amount) or 0 > int(amount):
        return await message.answer('Недостаточно столар коинов')

    player.stolar -= int(amount)
    await message.answer('Введите цену за которую пользователи могут купить ваши столар коины\n'
                         'Рекомендуется продать за: '
                         f'{int(amount) * 1000000000:,} разрешено использовать \"к\" для обозначения тысячи')
    await state.update_data(stolar_on_sell=amount)
    await state.set_state(SellStolar.money_buy)


@router.message(StateFilter(SellStolar.money_buy))
async def set_buy_price(message: Message, state: FSMContext):
    cost = message.text
    cost = cost.replace("к", '000')
    cost = cost.replace(',', '')
    if int(cost) < 0:
        return await message.answer('Не правильная цена')
    await state.update_data(money_buy=cost)
    await state.set_state(SellStolar.confirm)
    user = await state.get_data()
    cost = user['money_buy']
    amount = user['stolar_on_sell']
    await message.answer('напишите \"Да\" если все верно\n'
                         f'Количество столар коинов: {amount}\n'
                         f'Цена: {int(cost):,}')


@router.message(StateFilter(SellStolar.confirm), F.text.lower() == 'да')
async def create_message_sell(message: Message, state: FSMContext):
    user = await state.get_data()
    cost = user['money_buy']
    amount = user['stolar_on_sell']
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Купить',
                              callback_data=
                              f'buy_stolar:{cost}:{amount}:{message.from_user.id}')]])
    await message.answer('Лот успешно создан можете проверять @tegtoryshop')
    await bot.send_message('@tegtoryshop', f'продается {amount} столар коинов за {int(cost):,} очков',
                           reply_markup=markup)
    await state.clear()


@router.callback_query(F.data.split(':')[0] == 'buy_stolar')
async def buy_on_channel(call: CallbackQuery):
    data = call.data.split(':')
    player = Player(call.from_user.id)
    if player.money < int(data[1]):
        return
    player.money -= int(data[1])
    player.stolar += int(data[2])
    Player(data[3]).money += int(data[1])
    await bot.delete_message("@tegtoryshop", call.message.message_id)
    await bot.send_message(data[3], f'У вас купили столар коины {data[2]} на сумму {int(data[1]):,}')


@router.callback_query(F.data == 'buy_stolar_coin_10x')
async def buy_stolar_coin_10(call: CallbackQuery):
    player = Player(call.from_user.id)
    if player.money >= 10000000000:
        player.money -= 10000000000
        player.stolar += 10
        await call.message.answer('куплено 10 столар коинов')
    else:
        await call.message.answer(not_enough_points)


@router.callback_query(F.data == 'buy_stolar_coin_100x')
async def buy_stolar_coin_100(call: CallbackQuery):
    player = Player(call.from_user.id)
    if player.money >= 100000000000:
        player.money -= 100000000000
        player.stolar += 100
        await call.message.answer('куплено 100 столар коинов')
    else:
        await call.message.answer(not_enough_points)


@router.callback_query(F.data == 'buy_stolar_coin')
async def buy_stolar_coin(call: CallbackQuery):
    player = Player(call.from_user.id)

    if player.money > 1000000000:
        player.money -= 1000000000
        player.stolar += 1
        await call.message.answer('куплен столар коин')
    else:
        await call.message.answer(not_enough_points)
