from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from Filters import SubscribeFilter, SpamFilter, SpamFilterCallBack, ProfileFilter
from MIddleWares.UserMiddleWare import UserMiddleWare
from States import ChangeNick
from db import Player
from replys import subscribed_channel

router = Router()
router.message.middleware(UserMiddleWare())


@router.callback_query(F.data == 'profile')
async def profile(call: types.CallbackQuery):
    player = Player(call.from_user.id)
    await call.message.answer(str(player))


@router.message(ProfileFilter())
async def balance(message: types.Message):
    player = Player(message.from_user.id)
    await message.answer(str(player))


@router.message(Command('change_nickname'), StateFilter(None))
async def change_nick(message: types.Message, state: FSMContext):
    await message.answer('Введите ваше новое имя, не длинее 20 символов')
    await state.set_state(ChangeNick.new_nickname)


@router.message(StateFilter(ChangeNick.new_nickname))
async def confirm_changes(message: types.Message, state: FSMContext):
    if len(message.text) < 20:
        Player(message.from_user.id).nickname = message.text
        await state.clear()


@router.message(SubscribeFilter())
async def not_subscribed(message: types.Message):
    await message.answer('Подпишитесь на канал @tegtory чтобы пользоваться ботом',
                         reply_markup=subscribed_channel)


@router.message(SpamFilter(), F.text)
async def not_subscribed(message: types.Message):
    await message.answer('Не спамьте!')
    await message.delete()


@router.message(SpamFilterCallBack(), F.data)
async def not_subscribed(call: types.CallbackQuery):
    return 0
