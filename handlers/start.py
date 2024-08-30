from aiogram import types, F, Router
from aiogram.filters.command import Command, CommandObject, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.utils.payload import decode_payload

from bot import bot
from db import Player
from replys import menu_reply


router = Router()
welcome = 'Добро пожаловать! Время стать владельцем фабрики и заработать крупные суммы.'


@router.message(Command("cancel"))
async def cancel(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer('отменено')


@router.message(CommandStart(deep_link=True))
async def start_func(message: types.Message, command: CommandObject):
    args = command.args
    payload = decode_payload(args)
    player = Player(message.from_user.id)
    if player.ref != '' or not Player(payload).exist:
        return await message.answer(welcome, reply_markup=menu_reply, parse_mode='HTML')

    player.money += 250
    player.ref = payload

    await message.answer(welcome + f'\n\nВас пригласил @{Player(payload).username}. Вы дополнительно получаете 250',
                         reply_markup=menu_reply, parse_mode='HTML')
    await bot.send_message(payload, 'По вашей ссылке перешёл новый игрок +250')
    Player(payload).money += 250


@router.message(CommandStart())
async def start(message: types.Message):
    return await message.answer(welcome, reply_markup=menu_reply, parse_mode='HTML')


@router.message(F.text == 'Я подписался')
async def check_text(message: types.Message):
    await message.answer(f'Вижу. удачной игры', reply_markup=menu_reply)
