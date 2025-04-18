from aiogram import F, Router, types
from aiogram.types import InputMediaPhoto

from domain.context.factory import UserFactoryContext
from domain.context.holder import FactoryHolder, UserHolder
from domain.entity import Factory
from presentors.aiogram.kb import factory as kb
from presentors.aiogram.kb.callbacks import FactoryCB
from presentors.aiogram.messages import factory as msg
from presentors.aiogram.utils import Images
from presentors.shared.utils.auth import (
    get_factory_operation,
    get_user_operation,
)
from presentors.shared.utils.cache import cache

router = Router()


@router.callback_query(F.data == FactoryCB.workers)
@get_factory_operation
@cache(Images.factory_hire, types.FSInputFile(Images.factory_hire))
async def workers_page(
    call: types.CallbackQuery,
    factory: FactoryHolder,
    cached,
    cache_func,
):
    entity = factory.entity
    sent = await call.message.edit_media(
        media=InputMediaPhoto(
            caption=msg.workers_page.format(
                entity.workers, entity.hire_available, entity.hire_price
            ),
            media=cached,
        ),
        reply_markup=kb.hire_markup,
    )
    cache_func(sent.photo[-1].file_id)


@router.callback_query(F.data == FactoryCB.hire)
@get_factory_operation
@get_user_operation
async def hire(
    call: types.CallbackQuery, factory: FactoryHolder, user: UserHolder
):
    ctx = UserFactoryContext(factory=factory.entity, user=user.entity)
    result = await factory.use_case.hire(ctx)
    markup = kb.failed_hire_markup
    if isinstance(result, Factory):
        result = msg.workers_page.format(
            result.workers, result.hire_available, result.hire_price
        )
        markup = kb.hire_markup

    await call.message.edit_caption(caption=str(result), reply_markup=markup)
