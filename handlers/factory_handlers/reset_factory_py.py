from aiogram import Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from States import DeleteFactory
from bot import bot
from db import Factory, Player
from replys import menu_reply

router = Router()


@router.message(StateFilter(None), Command('reset_factory'))
async def reset_factory(message: Message, state: FSMContext):
    if message.chat.type != "private":
        member = await bot.get_chat_member(message.chat.id, message.from_user.id)
        if member == types.ChatMemberMember:
            return await message.answer('сбрасывать фабрику в группе могут только ее админы')
    await message.answer(f'Чтобы удалить фабрику введите: `{Player(message.from_user.id).iternal_id if message.chat.id > 0 else message.chat.id}` или /cancel')
    await state.set_state(DeleteFactory.user_id)


@router.message(DeleteFactory.user_id)
async def delete_factory(message: Message, state: FSMContext):
    if message.chat.type == "private":
        factory = Factory(message.from_user.id)
    else:
        factory = Factory(message.chat.id)
    
    if not factory.exists():
        return await message.answer("У вас и так нет фабрики")
    if str(factory.owner) == str(message.text):
        factory.delete()
        await message.answer('Фабрика удалена', reply_markup=menu_reply)
        await state.clear()
    else:
        await message.answer('Код подтверждения введен не верно. /cancel')
