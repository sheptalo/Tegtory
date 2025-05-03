from asyncio import sleep
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram.utils.chat_action import ChatActionSender


class ChatActionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        if not hasattr(event, "chat"):
            return await handler(event, data)
        async with ChatActionSender.typing(
            bot=data["bot"], chat_id=event.chat.id
        ):
            await sleep(0.3)
            return await handler(event, data)
