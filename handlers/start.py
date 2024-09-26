from aiogram import types, F, Router
from aiogram.filters.command import Command, CommandObject, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.utils.payload import decode_payload

from api import api
from bot import bot
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
    player = api.player(message.from_user.id)
    money = player.money
    if player.ref != '' or not api.player(payload).exist:
        return await message.answer(welcome, reply_markup=menu_reply, parse_mode='HTML')

    player.global_change({
        'telegram_id': message.from_user.id,
        'money': money + 250,
        'ref': payload,
    })
    await message.answer(welcome + f'\n\nВас пригласил @{api.player(payload).username}. Вы дополнительно получаете 250',
                         reply_markup=menu_reply, parse_mode='HTML')
    await bot.send_message(payload, 'По вашей ссылке перешёл новый игрок +250')
    api.player(payload).money += 250


@router.message(CommandStart())
async def start(message: types.Message):
    return await message.answer(welcome, reply_markup=menu_reply, parse_mode='HTML')


@router.message(F.text == 'Я подписался')
async def check_text(message: types.Message):
    await message.answer(f'Вижу. удачной игры', reply_markup=menu_reply)
