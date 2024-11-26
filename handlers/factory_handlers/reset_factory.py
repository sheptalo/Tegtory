from aiogram import Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from states import DeleteFactory
from bot import bot, api
from replys import menu_reply, create_factory_markup

router = Router()


@router.message(StateFilter(None), Command("reset_factory"))
async def reset_factory(message: Message, state: FSMContext):
    if not api.factory(message.from_user.id).exist:
        return await message.answer(
            "У вас нет фабрики", reply_markup=create_factory_markup
        )
    if message.chat.type != "private":
        member = await bot.get_chat_member(
            message.chat.id, message.from_user.id
        )
        if member == types.ChatMemberMember:
            return await message.answer(
                "сбрасывать фабрику в группе могут только ее админы"
            )
    await message.answer(
        f"Чтобы удалить фабрику введите:  `{message.chat.id}` или /cancel"
    )
    await state.set_state(DeleteFactory.user_id)


@router.message(DeleteFactory.user_id)
async def delete_factory(message: Message, state: FSMContext):
    if message.chat.type == "private":
        factory = api.factory(message.from_user.id)
    else:
        factory = api.factory(message.chat.id)
    player = api.player(message.from_user.id)
    if not factory.exist:
        return await message.answer("У вас и так нет фабрики")
    if (
        str(factory.owner_id) == str(message.text)
        or factory.owner_id == player.id
    ):
        factory.delete()
        await message.answer("Фабрика удалена", reply_markup=menu_reply)
        await state.clear()
    else:
        await message.answer("Код подтверждения введен не верно. /cancel")
