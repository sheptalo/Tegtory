from asyncio import sleep
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram.utils.chat_action import ChatActionSender


class ChatActionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        async with ChatActionSender.typing(
            bot=data["bot"],
            chat_id=event.chat.id,  # ignore[attr-defined]
        ):
            await sleep(0.3)
            return await handler(event, data)
