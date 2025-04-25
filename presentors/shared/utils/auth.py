import logging
from functools import wraps
from typing import Any, Callable

from aiogram import types
from dishka import FromDishka

from domain.entity import Factory, User
from domain.queries.factory import GetFactoryQuery, GetStorageQuery
from domain.queries.user import UserQuery
from domain.results import Success
from domain.use_cases import UCUser
from infrastructure.injectors import inject
from infrastructure.query import QueryExecutor
from presentors.aiogram.kb import factory as kb_factory
from presentors.aiogram.messages import factory as factory_msg

logger = logging.getLogger(__name__)


def get_factory(func) -> Callable:
    @wraps(func)
    async def wrapper(
        event: types.Message | types.CallbackQuery, *args, **kwargs
    ) -> Any:
        factory = kwargs.pop("factory", await _get_factory(event.from_user.id))
        if not factory:
            await factory_required_handler(event)
            return
        return await func(event, *args, factory=factory, **kwargs)

    return wrapper


def get_storage_from_factory(func) -> Callable:
    @wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        factory = kwargs.pop("factory")
        result = await QueryExecutor().ask(
            GetStorageQuery(factory_id=factory.id)
        )
        if isinstance(result, Success):
            return await func(*args, storage=result.data, **kwargs)

    return wrapper


def get_user(func) -> Callable:
    @wraps(func)
    async def wrapper(
        event: types.Message | types.CallbackQuery, *args, **kwargs
    ) -> Any:
        user = kwargs.pop("user", await _get_user(event.from_user.id))
        if not user:
            user = await _create_user(event.from_user)
        return await func(event, *args, user=user, **kwargs)

    return wrapper


def get_event_message(
    event: types.Message | types.CallbackQuery,
) -> types.Message:
    return event.message if type(event) is types.CallbackQuery else event


async def _get_factory(user_id: int) -> Factory | None:
    result = await QueryExecutor().ask(
        GetFactoryQuery(
            factory_id=user_id,
        )
    )
    if isinstance(result, Success):
        return result.data
    return None


async def _get_user(user_id) -> User | None:
    res = await QueryExecutor().ask(UserQuery(user_id=user_id))
    if isinstance(res, Success):
        return res.data
    return None


@inject(is_async=True)
async def _create_user(user, uc_user: FromDishka[UCUser]) -> User | None:
    logger.info(f"Registering user {user.id} - {user.username}")
    return await uc_user.create(
        User(id=user.id, name=user.first_name, username=user.username)
    )


async def factory_required_handler(event) -> None:
    logger.info(f"Пользователь {event.from_user.id} не имеет фабрики")
    await get_event_message(event).answer(
        factory_msg.need_to_create,
        reply_markup=kb_factory.create_markup,
    )
