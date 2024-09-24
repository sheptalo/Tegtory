from aiogram import Router, types, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from Filters import SubscribeFilter, SpamFilter, SpamFilterCallBack, ProfileFilter, SubscribeFilterCallBack
from States import ChangeNick
from api import api
from replys import subscribed_channel, menu_reply

router = Router()
exactly = 'Telegram server says - Bad Request: message is not modified: specified new message content and reply markup are exactly the same as a current content and reply markup of the message'


@router.message(SubscribeFilter())
async def subscribe(message: types.Message):
    await message.answer('Подпишитесь на канал @tegtory',
                         reply_markup=subscribed_channel)


@router.callback_query(SubscribeFilterCallBack())
async def subscribe_call(call: types.CallbackQuery):
    try:
        await call.message.edit_text('Подпишитесь на канал @tegtory',
                                     reply_markup=subscribed_channel)
    except TelegramBadRequest:
        try:
            await call.message.delete()
            await call.message.answer(text='Подпишитесь на канал @tegtory',
                                      reply_markup=subscribed_channel)
        except TelegramBadRequest as e:
            print(e if e != exactly else None)


@router.message(SpamFilter(), F.text)
async def stop_spam(message: types.Message):

    await message.answer('Не спамьте!')
    await message.delete()


@router.callback_query(F.data == 'profile')
async def profile(call: types.CallbackQuery):
    player = api.player(call.from_user.id)
    await call.message.answer(str(player))


@router.message(ProfileFilter())
async def balance(message: types.Message):
    player = api.player(message.from_user.id)
    await message.answer(str(player))


@router.message(Command('change_nickname'), StateFilter(None))
async def change_nick(message: types.Message, state: FSMContext):
    await message.answer('Введите ваше новое имя, не длинее 20 символов')
    await state.set_state(ChangeNick.new_nickname)


@router.message(StateFilter(ChangeNick.new_nickname))
async def confirm_changes(message: types.Message, state: FSMContext):
    if len(message.text) < 20:
        api.player(message.from_user.id).name = message.text
        await state.clear()


@router.message(SpamFilterCallBack(), F.data)
async def spam(_: types.CallbackQuery):
    return 0


@router.callback_query(F.data == 'subscribe')
async def subscribe_check(call: types.CallbackQuery):
    try:
        await call.message.delete()
        await call.message.answer('Меню', reply_markup=menu_reply)
    except BaseException as e:
        print(e)
