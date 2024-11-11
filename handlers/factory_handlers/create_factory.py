from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from States import CreateFactory
from bot import bot, api

router = Router()
create_factory_caution = 'максимальная длина названия 20 символов'


@router.callback_query(F.data == 'create_factory')
async def callback_create_factory(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Придумайте название фабрики /cancel")
    await state.set_state(CreateFactory.new_factory_name)


@router.message(CreateFactory.new_factory_name, F.text)
async def process_factory_name(message: Message, state: FSMContext):
    factory_name = message.text
    if message.chat.type == "private":
        factory = api.factory(message.from_user.id)
    else:
        member = await bot.get_chat_member(message.chat.id, message.from_user.id)
        if member == types.ChatMemberMember:
            await state.clear()
            return await message.answer('Создать фабрику в группе могут только ее админы')
        factory = api.factory(message.chat.id)
    if factory.exists():
        await state.clear()
        return await message.answer("У вас уже есть фабрика.")
    if len(factory_name) > 20:
        return await message.answer(create_factory_caution)
    if type(api.find_factory(factory_name)) == api.Factory:
        return await message.answer('Фабрика с таким названием существует')
    factory.create(factory_name)
    await message.answer(f'Успешно создана фабрика {factory_name}')
    await state.clear()
