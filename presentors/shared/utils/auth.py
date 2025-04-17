import logging
from functools import wraps

from aiogram import types
from dishka import FromDishka

from domain.entity import Factory, User
from domain.use_cases import UCFactory, UCUser
from infrastructure.injectors import inject
from presentors.aiogram.kb import factory as kb_factory
from presentors.aiogram.messages import factory as factory_msg
from presentors.shared.utils.injection import smart_call

logger = logging.getLogger(__name__)


def have_factory(func):
    @wraps(func)
    async def wrapper(
        event: types.Message | types.CallbackQuery,
        **kwargs,
    ):
        user_id = event.from_user.id
        factory = kwargs.pop('factory', None)
        use_case = kwargs.pop('uc_factory', None)
        if not factory or not use_case:
            factory, use_case = await get_factory(user_id)
        if not factory:
            logger.info("Пользователь %s не имеет фабрики" % user_id)
            return await get_event_message(event).answer(
                factory_msg.need_to_create,
                reply_markup=kb_factory.create_markup,
            )

        return await smart_call(
            func,
            event,
            factory=factory,
            uc_factory=use_case,
            **kwargs,
        )

    return wrapper


def auth_user(func):
    @wraps(func)
    async def wrapper(
        event: types.Message | types.CallbackQuery,
        **kwargs,
    ):
        user = kwargs.pop('user', None)
        use_case = kwargs.pop('uc_user', None)
        if not user or not use_case:
            user, use_case = await get_user(event.from_user.id)
        return await smart_call(
            func, event, user=user, uc_user=use_case, **kwargs
        )

    return wrapper


def get_event_message(event: types.Message | types.CallbackQuery):
    return event.message if type(event) is types.CallbackQuery else event


@inject(is_async=True)
async def get_factory(
    user_id, uc_factory: FromDishka[UCFactory]
) -> tuple[Factory | None, UCFactory]:
    return await uc_factory.get(user_id), uc_factory


@inject(is_async=True)
async def get_user(
    user_id, uc_user: FromDishka[UCUser]
) -> tuple[User | None, UCUser]:
    return await uc_user.get(user_id), uc_user
