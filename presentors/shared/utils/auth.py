import logging
from functools import wraps

from aiogram import types
from dishka import FromDishka

from domain.entity import Factory, User
from domain.use_cases import UCFactory, UCUser
from infrastructure.injectors import inject
from presentors.aiogram.kb import factory as kb_factory
from presentors.aiogram.messages import factory as factory_msg

logger = logging.getLogger(__name__)


def get_factory(func):
    @wraps(func)
    async def wrapper(
        event: types.Message | types.CallbackQuery,
        **kwargs,
    ):
        factory = kwargs.pop("factory", None)
        if not factory:
            factory = await _get_factory(event.from_user.id)
        if not factory:
            logger.info(
                "Пользователь %s не имеет фабрики" % event.from_user.id
            )
            return await get_event_message(event).answer(
                factory_msg.need_to_create,
                reply_markup=kb_factory.create_markup,
            )

        return await func(
            event,
            factory=factory,
            **kwargs,
        )

    return wrapper


def get_user(func):
    @wraps(func)
    async def wrapper(
        event: types.Message | types.CallbackQuery,
        **kwargs,
    ):
        user = kwargs.pop("user", None)
        if not user:
            user = await _get_user(event.from_user.id)
        if not user:
            user = await _create_user(event.from_user)
        return await func(
            event,
            user=user,
            **kwargs,
        )

    return wrapper


def get_event_message(event: types.Message | types.CallbackQuery):
    return event.message if type(event) is types.CallbackQuery else event


@inject(is_async=True)
async def _get_factory(
    user_id, uc_factory: FromDishka[UCFactory]
) -> Factory | None:
    return await uc_factory.get(user_id)


@inject(is_async=True)
async def _get_user(user_id, uc_user: FromDishka[UCUser]) -> User | None:
    return await uc_user.get(user_id)


@inject(is_async=True)
async def _create_user(user, uc_user: FromDishka[UCUser]) -> User | None:
    logger.info(f'Registering user {user.id} - {user.username}')
    return await uc_user.create(
        User(id=user.id, name=user.first_name, username=user.username)
    )
