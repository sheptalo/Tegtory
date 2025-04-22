from aiogram import F, Router, types
from aiogram.types import InputMediaPhoto
from dishka import FromDishka

from domain.commands.factory import HireWorkerCommand
from domain.context.factory import UserFactoryContext
from domain.entity import Factory
from domain.entity.factory import WorkersFactory
from domain.results import Success
from domain.use_cases import UCFactory
from infrastructure.command import CommandExecutor
from presentors.aiogram.kb import factory as kb
from presentors.aiogram.kb.callbacks import FactoryCB
from presentors.aiogram.messages import factory as msg
from presentors.aiogram.utils import Images
from presentors.shared.utils.auth import (
    get_factory,
    get_user,
)
from presentors.shared.utils.cache import cache
from presentors.shared.utils.di_context import with_context

router = Router()


@router.callback_query(F.data == FactoryCB.workers)
@get_factory
@cache(Images.factory_hire, types.FSInputFile(Images.factory_hire))
async def workers_page(
    call: types.CallbackQuery,
    factory: Factory,
    cached,
    cache_func,
):
    sent = await call.message.edit_media(
        media=InputMediaPhoto(
            caption=msg.workers_page.format(
                factory.workers, factory.hire_available, factory.hire_price
            ),
            media=cached,
        ),
        reply_markup=kb.hire_markup,
    )
    cache_func(sent.photo[-1].file_id)


@router.callback_query(F.data == FactoryCB.hire)
@get_factory
@get_user
@with_context(UserFactoryContext)
async def hire(
    call: types.CallbackQuery,
    ctx: UserFactoryContext,
):
    result = await CommandExecutor().execute(
        HireWorkerCommand(
            factory=WorkersFactory.model_validate(ctx.factory.model_dump()),
            user_money=ctx.user.money,
            user_id=ctx.user.id,
        )
    )
    markup = kb.failed_hire_markup
    if isinstance(result, Success):
        return await workers_page(call)

    await call.message.edit_caption(caption=result.reason, reply_markup=markup)
