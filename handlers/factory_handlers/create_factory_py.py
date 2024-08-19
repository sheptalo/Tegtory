from aiogram import Router, F, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from States import CreateFactory
from bot import bot
from config import create_factory_caution
from db.Factory import Factory

router = Router()


@router.message(StateFilter(None), Command('create_factory'))
async def rename_factory_yes(message: Message, state: FSMContext):
    await message.answer("Придумайте название фабрики /cancel")
    await state.set_state(CreateFactory.new_factory_name)


@router.message(CreateFactory.new_factory_name, F.text)
async def process_factory_name(message: Message, state: FSMContext):
    factory_name = message.text
    if message.chat.type == "private":
        factory = Factory(message.from_user.id)
    else:
        member = await bot.get_chat_member(message.chat.id, message.from_user.id)
        if member == types.ChatMemberMember:
            await state.clear()
            return await message.answer('Создать фабрику в группе могут только ее админы')
        factory = Factory(message.chat.id)
    if factory.exists():
        await state.clear()
        return await message.answer("У вас уже есть фабрика.")
    if len(factory_name) > 20:
        return await message.answer(create_factory_caution)
    factory.create(factory_name)
    await message.answer(f'Успешно создана фабрика {factory_name}')
    await state.clear()
