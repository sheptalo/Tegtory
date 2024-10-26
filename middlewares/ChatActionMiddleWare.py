from asyncio import sleep

from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from bot import bot


class Typing(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        async with ChatActionSender.typing(bot=bot, chat_id=event.chat.id):
            await sleep(1)
            return await handler(event, data)
