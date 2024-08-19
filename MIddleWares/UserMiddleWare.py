from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

from db.Player import Player


class UserMiddleWare(BaseMiddleware):
    def __init__(self) -> None:
        self.counter = 0

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        player = Player(data['event_from_user'].id)
        if not player.exist:
            await player.create(data['event_from_user'].first_name, data['event_from_user'].username)
        return await handler(event, data)
