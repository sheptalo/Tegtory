import random

from aiogram import F, Router, types
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from MIddleWares.UserMiddleWare import UserMiddleWare
from States import SellStolar, SellStock

from bot import bot
from config import title_shop, not_enough_points, shop_text, have_title
from db import Factory, Player, GetStockPrice, Leaderboard
from replys import rinok_markup, titles_shop_markup, lottery_markup, shop_reply, title_error_markup, market_markup, \
    back_shop_markup, lottery_back_markup

router = Router()
router.message.middleware(UserMiddleWare())


@router.callback_query(F.data == 'back_shop')
async def back_shop(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text(shop_text,
                                 reply_markup=shop_reply)


@router.callback_query(F.data == 'shop')
async def shop_main(call: types.CallbackQuery):
    text = '\n'
    if call.message.chat.type != 'private':
        text += ("🟥При покупке товаров связанных с фабрикой они будут *покупаться для фабрики группы*, "
                 "для покупки товаров для *своей фабрики* покупайте в личных сообщениях с ботом!!🟥")
    await call.message.edit_text(shop_text + text, reply_markup=shop_reply, parse_mode='Markdown')


# region donate
@router.callback_query(F.data == 'донат')
async def test(call: CallbackQuery):
    return await call.message.answer('В данный момент недоступно')
    # await message.answer("сейчас можно купить только 100к очков за 85 руб")
    # await bot.send_invoice(message.from_user.id,
    #                        '100.000 очков',
    #                        'Закончились деньги? приобрети 100.000 очков прямо сейчас.',
    #                        'something',
    #                        provider_token=provider_t,
    #                        currency='rub',
    #                        prices=prices)


# endregion
# region sell stolar
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

    if player.stolar_coin < int(amount) or 0 > int(amount):
        return await message.answer('Недостаточно столар коинов')

    player.stolar_coin -= int(amount)
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


# endregion
# region titles
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
# region buy_stolar_coin
@router.callback_query(F.data.split(':')[0] == 'buy_stolar')
async def buy_on_channel(call: CallbackQuery):
    data = call.data.split(':')
    player = Player(call.from_user.id)
    if player.money < int(data[1]):
        return
    player.money -= int(data[1])
    player.stolar_coin += int(data[2])
    Player(data[3]).money += int(data[1])
    await bot.delete_message("@tegtoryshop", call.message.message_id)
    await bot.send_message(data[3], f'У вас купили столар коины {data[2]} на сумму {int(data[1]):,}')


@router.callback_query(F.data == 'buy_stolar_coin_10x')
async def buy_stolar_coin_10(call: CallbackQuery):
    player = Player(call.from_user.id)
    if player.money >= 10000000000:
        player.money -= 10000000000
        player.stolar_coin += 10
        await call.message.answer('куплено 10 столар коинов')
    else:
        await call.message.answer(not_enough_points)


@router.callback_query(F.data == 'buy_stolar_coin_100x')
async def buy_stolar_coin_100(call: CallbackQuery):
    player = Player(call.from_user.id)
    if player.money >= 100000000000:
        player.money -= 100000000000
        player.stolar_coin += 100
        await call.message.answer('куплено 100 столар коинов')
    else:
        await call.message.answer(not_enough_points)


@router.callback_query(F.data == 'buy_stolar_coin')
async def buy_stolar_coin(call: CallbackQuery):
    player = Player(call.from_user.id)

    if player.money > 1000000000:
        player.money -= 1000000000
        player.stolar_coin += 1
        await call.message.answer('куплен столар коин')
    else:
        await call.message.answer(not_enough_points)


# endregion
# region lottery
@router.callback_query(F.data.lower() == 'лотерея')
async def lottery_main(call: CallbackQuery):
    await call.message.edit_text('🎟*Лотерея*🎟\n\n'
                                 'Здесь вы можете купить билеты для участия в лотереи.\n\n'
                                 '*Инфо:*\n'
                                 '*Бронзовый билет:\n*Цена - 5,000 очков, выйгрыш - 50,000 очков\n\n'
                                 '*Серебряный билет:\n*Цена - 100,000 очков, выйгрыш - 1,000,000 очков\n\n'
                                 '*Золотой билет:\n*Цена - 10,000,000 очков, выйгрыш - 1,000,000,000 очков\n\n'
                                 '*Столар билет:\n*Цена - 10 столар коинов, выйгрыш - 100 столар коинов\n\n'
                                 f'🎟Номера купленных билетов:{Player(call.from_user.id).tickets}\n\n',
                                 reply_markup=lottery_markup)


@router.callback_query(F.data == 'bronze_ticket')
async def buy_bronze_ticket(call: CallbackQuery):
    player = Player(call.from_user.id)
    new_ticket = random.randint(1000, 1500)
    while new_ticket in player.tickets.split():
        new_ticket = random.randint(1000, 1500)
    if player.money >= 5000:
        player.money -= 5000
        player.tickets += f' {new_ticket}'
        await call.message.edit_text(f'Куплен бронзовый билет с номером {new_ticket}', reply_markup=lottery_back_markup)
    else:
        await call.message.edit_text("Не хватает очков", reply_markup=lottery_back_markup)


@router.callback_query(F.data == 'serebro_ticket')
async def buy_serebro_ticket(call: CallbackQuery):
    player = Player(call.from_user.id)

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
    player = Player(call.from_user.id)
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
    player = Player(call.from_user.id)
    new_ticket = random.randint(1000000, 1500000)
    while new_ticket in player.tickets.split():
        new_ticket = random.randint(1000000, 1500000)
    if player.stolar_coin >= 10:
        player.stolar_coin -= 10
        player.tickets += f' {new_ticket}'
        await call.message.edit_text(f'Куплен столар билет с номером {new_ticket}', reply_markup=lottery_back_markup)
    else:
        await call.message.edit_text("Не хватает столар коинов", reply_markup=lottery_back_markup)


# endregion
# region market
@router.callback_query(F.data == 'маркет')
async def market(call: CallbackQuery):
    await call.message.edit_text('Продайте свой товар на маркете, осторожно цена может упасть в любой момент\n'
                                 f'Текущая цена: {GetStockPrice().get} за штуку',
                                 reply_markup=market_markup)


@router.callback_query(F.data == 'sell_on_market')
async def sell_on_market(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        f'Введите сколько хотите продать товара. У вас есть {Factory(call.from_user.id).stock}',
        reply_markup=back_shop_markup)
    await state.set_state(SellStock().stock)


@router.message(SellStock().stock)
async def amount_to_sell(message: Message, state: FSMContext):
    try:
        amount = int(message.text)
    except:
        return await message.answer('Неправильное количество')
    price = GetStockPrice().get
    factory = Factory(message.from_user.id)
    if amount <= 0 or amount > factory.stock:
        return await message.answer('Нехватает товара')

    factory.stock -= amount
    Player(message.from_user.id).money += amount * price
    await message.answer('Успешно продано')
    await state.clear()
# endregion
