import logging
from functools import wraps
from typing import Any, Callable

from aiogram import types

from domain.commands.user import RegisterUserCommand
from domain.entities import Factory, User
from domain.queries.factory import GetFactoryQuery, GetStorageQuery
from domain.queries.user import UserQuery
from domain.results import Failure, Success
from infrastructure.command import CommandExecutor
from infrastructure.query import QueryExecutor
from presenters.aiogram.kb import factory as kb_factory
from presenters.aiogram.messages import factory as factory_msg

logger = logging.getLogger(__name__)


def get_factory(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(
        event: types.Message | types.CallbackQuery,
        *args: tuple,
        **kwargs: dict,
    ) -> Any:
        if not event.from_user:
            return
        factory = kwargs.pop("factory", await _get_factory(event.from_user.id))
        if not factory:
            await factory_required_handler(event)
            return
        return await func(event, *args, factory=factory, **kwargs)

    return wrapper


def get_storage_from_factory(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(*args: tuple, **kwargs: Any) -> Any:
        factory: Factory = kwargs.pop("factory")
        result = await QueryExecutor().ask(
            GetStorageQuery(factory_id=factory.id)
        )
        if isinstance(result, Success):
            return await func(*args, storage=result.data, **kwargs)

    return wrapper


def get_user(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(
        event: types.Message | types.CallbackQuery,
        *args: tuple,
        **kwargs: dict,
    ) -> Any:
        if not event.from_user:
            logger.error("Событие не от пользователя.игнорируем")
            return None
        user = kwargs.pop("user", await _get_user(event.from_user.id))
        if not user:
            user = await _create_user(event.from_user)
        return await func(event, *args, user=user, **kwargs)

    return wrapper


def get_event_message(
    event: types.Message | types.CallbackQuery | None,
) -> types.Message | types.InaccessibleMessage | None:
    return (
        event.message
        if isinstance(event, types.CallbackQuery) and event.message is not None
        else event
        if isinstance(event, types.Message)
        else None
    )


async def _get_factory(user_id: int) -> Factory | None:
    result: Success[Factory] | Failure = await QueryExecutor().ask(
        GetFactoryQuery(factory_id=user_id)
    )
    if isinstance(result, Success):
        return result.data
    return None


async def _get_user(user_id: int) -> User | None:
    res: Success[User] | Failure = await QueryExecutor().ask(
        UserQuery(user_id=user_id)
    )
    if isinstance(res, Success):
        return res.data
    return None


async def _create_user(user: types.User) -> User | None:
    logger.info(f"Registering user {user.id} - {user.username}")
    result: Success[User] | Failure = await CommandExecutor().execute(
        RegisterUserCommand(
            user_id=user.id,
            name=user.first_name,
            username=user.username or "none",
        )
    )
    if isinstance(result, Success):
        return result.data
    logger.error(result.reason)
    return None


async def factory_required_handler(
    event: types.CallbackQuery | types.Message,
) -> None:
    if not event.from_user:
        logger.error("У События нет пользователя")
        return None
    logger.info(f"Пользователь {event.from_user.id} не имеет фабрики")
    message = get_event_message(event)
    if message:
        await message.answer(
            factory_msg.need_to_create, reply_markup=kb_factory.create_markup
        )
