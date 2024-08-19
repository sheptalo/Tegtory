from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from MIddleWares.UserMiddleWare import UserMiddleWare
from db import Player

router = Router()
router.message.middleware(UserMiddleWare())


class ChangeNick(StatesGroup):
    new_nickname = State()


@router.message(Command('change_nickname'), StateFilter(None))
async def change_nick(message: types.Message, state: FSMContext):
    await message.answer('Введите ваше новое имя, не длинее 20 символов')
    await state.set_state(ChangeNick.new_nickname)


@router.message(StateFilter(ChangeNick.new_nickname))
async def confirm_changes(message: types.Message, state: FSMContext):
    if len(message.text) < 20:
        Player(message.from_user.id).username = message.text
        await state.clear()

