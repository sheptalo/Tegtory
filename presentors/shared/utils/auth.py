import logging
from functools import wraps

from aiogram import types
from dishka import FromDishka

from domain.context.holder import FactoryHolder, UserHolder
from domain.use_cases import UCFactory, UCUser
from infrastructure.injectors import inject
from presentors.aiogram.kb import factory as kb_factory
from presentors.aiogram.messages import factory as factory_msg
from presentors.shared.utils.injection import smart_call

logger = logging.getLogger(__name__)


def get_factory_operation(func):
    @wraps(func)
    async def wrapper(
        event: types.Message | types.CallbackQuery,
        **kwargs,
    ):
        holder = kwargs.pop("factory", None)
        if not holder:
            holder = await get_factory(event.from_user.id)
        if not holder.entity:
            logger.info(
                "Пользователь %s не имеет фабрики" % event.from_user.id
            )
            return await get_event_message(event).answer(
                factory_msg.need_to_create,
                reply_markup=kb_factory.create_markup,
            )

        return await smart_call(
            func,
            event,
            factory=holder,
            **kwargs,
        )

    return wrapper


def get_user_operation(func):
    @wraps(func)
    async def wrapper(
        event: types.Message | types.CallbackQuery,
        **kwargs,
    ):
        holder = kwargs.pop("user", None)
        if not holder:
            holder = await get_user(event.from_user.id)
        return await smart_call(
            func,
            event,
            user=holder,
            **kwargs,
        )

    return wrapper


def get_event_message(event: types.Message | types.CallbackQuery):
    return event.message if type(event) is types.CallbackQuery else event


@inject(is_async=True)
async def get_factory(
    user_id, uc_factory: FromDishka[UCFactory]
) -> FactoryHolder:
    return FactoryHolder(
        entity=await uc_factory.get(user_id),
        use_case=uc_factory,
    )


@inject(is_async=True)
async def get_user(user_id, uc_user: FromDishka[UCUser]) -> UserHolder:
    return UserHolder(
        entity=await uc_user.get(user_id),
        use_case=uc_user,
    )
