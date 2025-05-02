from aiogram import F, Router, types
from aiogram.types import InputMediaPhoto

from domain.commands.factory import HireWorkerCommand
from domain.context.factory import UserFactoryContext
from domain.entities import Factory
from domain.results import Success
from infrastructure.command import CommandExecutor
from presenters.aiogram.kb import factory as kb
from presenters.aiogram.kb.callbacks import FactoryCB
from presenters.aiogram.messages import factory as msg
from presenters.aiogram.utils import Images
from presenters.shared.utils.auth import (
    get_factory,
    get_user,
)
from presenters.shared.utils.cache import cache
from presenters.shared.utils.di_context import with_context

router = Router()


@router.callback_query(F.data == FactoryCB.workers)
@get_factory
@cache(Images.factory_hire, types.FSInputFile(Images.factory_hire))
async def workers_page(
    call: types.CallbackQuery,
    factory: Factory,
    cached,
    cache_func,
) -> None:
    sent = await call.message.edit_media(
        media=InputMediaPhoto(
            caption=msg.workers_page.format(
                factory.workers, factory.hire_available, factory.hire_price
            ),
            media=cached,
        ),
        reply_markup=kb.hire_markup,
    )
    if sent.photo:
        cache_func(sent.photo[-1].file_id)


@router.callback_query(F.data == FactoryCB.hire)
@get_factory
@get_user
@with_context(UserFactoryContext)
async def hire(
    call: types.CallbackQuery,
    ctx: UserFactoryContext,
) -> None:
    result = await CommandExecutor().execute(
        HireWorkerCommand(
            factory=ctx.factory,
            user_money=ctx.user.money,
            user_id=ctx.user.id,
        )
    )
    markup = kb.failed_hire_markup
    if isinstance(result, Success):
        await workers_page(call)
        return None

    await call.message.edit_caption(caption=result.reason, reply_markup=markup)
