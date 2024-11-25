from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.deep_linking import create_start_link

from bot import bot

router = Router()


@router.message(Command("ref"))
async def ref(message: Message):
    link = await create_start_link(bot, f"{message.from_user.id}", encode=True)
    await message.answer(
        "ваша реферальная ссылка: \n"
        + link
        + "\n\nПри переходе вы и новый игрок получите 250 очков."
    )
