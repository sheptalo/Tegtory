from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

from bot import api


class UserMiddleWare(BaseMiddleware):
    users = []

    def __init__(self) -> None:
        self.counter = 0

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        eve = data["event_from_user"]
        if eve.id not in UserMiddleWare.users:
            player = api.player(eve.id)
            if not player.exist:
                await player.create(eve.username, eve.first_name)
            UserMiddleWare.users.append(eve.id)
        return await handler(event, data)
