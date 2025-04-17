from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message
from dishka import FromDishka

from domain.use_cases import UCUser
from infrastructure.injectors import inject


class AuthMiddleware(BaseMiddleware):
    users = []

    def __init__(self) -> None:
        self.counter = 0

    @inject(is_async=True)
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
        user_use_case: FromDishka[UCUser],
    ) -> Any:
        user = data["event_from_user"]
        if user.id not in AuthMiddleware.users:
            await user_use_case.create_if_not_exist(
                user.id, user.first_name, user.username
            )
            AuthMiddleware.users.append(user.id)
        return await handler(event, data)
