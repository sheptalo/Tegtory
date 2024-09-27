from aiogram import Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from States import FactoryName
from api import api
from bot import bot
from replys import create_factory_markup

router = Router()
create_factory_caution = 'максимальная длина названия 20 символов'


@router.message(StateFilter(None), Command('rename_factory'))
async def rename_factory_yes(message: Message, state: FSMContext):
    if not api.factory(message.from_user.id).exists():
        return await message.reply('у вас нету фабрики', reply_markup=create_factory_markup)
    await message.answer("Введите новое название фабрики")
    await state.set_state(FactoryName.new_factory_name)


@router.message(FactoryName.new_factory_name)
async def process_factory_name(message: Message, state: FSMContext):
    new_factory_name = message.text
    if message.chat.type == "private":
        factory = api.factory(message.from_user.id)
    else:
        member = await bot.get_chat_member(message.chat.id, message.from_user.id)
        if member == types.ChatMemberMember:
            await state.clear()
            return await message.answer('Переименовать фабрику в группе могут только ее админы')
        factory = api.factory(message.chat.id)
    if len(new_factory_name) > 20:
        return await message.answer(create_factory_caution)
    if type(api.find_factory(new_factory_name)) != "<class 'int'>":
        return await message.answer('Фабрика с таким названием существует')
    factory.name = new_factory_name
    await message.answer('Название фабрики изменено')
    await state.clear()
