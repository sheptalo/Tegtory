from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

from Filters import ProfileFilter, MenuFilter
from MIddleWares.ChatActionMiddleWare import Typing
from MIddleWares.UserMiddleWare import UserMiddleWare
from States import FindFactory
from bot import bot
from config import mini_games_text, not_enough_points, type_func
from db import Factory, Player
from replys import menu_reply, mini_game_markup, city_markup

router = Router()
router.message.middleware(Typing())
router.message.middleware(UserMiddleWare())


@router.message(MenuFilter())
async def menu_cmd(message: types.Message):
    await message.answer(f'Привет {message.from_user.first_name}\n', reply_markup=menu_reply)


@router.callback_query(F.data == 'city')
async def back_city(call: types.CallbackQuery):
    await call.message.edit_text('Вы в центре города', reply_markup=city_markup)


@router.message(F.text.lower() == 'город')
async def city(message: types.Message):
    await message.answer('Вы в центре города.', reply_markup=city_markup)


@router.message(F.text.lower() == 'мини игры')
async def mini_games_menu(message: types.Message):
    await message.answer(mini_games_text, reply_markup=mini_game_markup, parse_mode='Markdown')


@router.message(F.text.lower() == 'найти')
async def find_factory(message: types.Message, state: FSMContext):
    await state.set_state(FindFactory.name)
    await message.answer('Впишите название фабрики которую хотите найти')


@router.message(StateFilter(FindFactory.name))
async def answer_finded_factory(message: types.Message, state: FSMContext):
    factory = Factory.find(message.text)
    if not factory.exists():
        return await message.answer('Фабрика не найдена')
    _type = type_func(factory.type)
    await message.answer_photo(FSInputFile(_type),
                               f'* Фабрика пользователя:* \n\n'
                               f'🏭 *Название фабрики:* {factory.name} \n'
                               f'🔧 *Текущий уровень:* {factory.level} \n'
                               f'⚙️ *Тип фабрики:* {factory.type}\n'
                               f'🚧 *Статус фабрики:* {factory.state} \n'
                               f'👷‍ *Количество работников на фабрике:* {factory.workers}', parse_mode='Markdown')
    await state.clear()


@router.message(F.text.lower().split()[0] == 'передать')
async def give_money(message: types.Message):
    try:
        _id = str(message.text.split()[1])
        _money = int(message.text.split()[2])
        player = Player(message.from_user.id)
    except:
        return await message.answer('Принцип передачи денег: передать ID 1203')
    if 0 > _money or _money > player.money:
        return await message.answer(not_enough_points + '\nили сумма меньше 0')

    try:
        player2 = Player(_id)
        player2.money += _money
        player.money -= _money
    except:
        return await message.answer('видимо вы неверно указали айди')
    await bot.send_message(player2.user_id, f'вам перевели {int(_money):,}')
    await message.answer(f'перевод выполнен')
    await bot.send_message(1405684214, f'кому {_id} {_money} от {message.from_user.id}')
