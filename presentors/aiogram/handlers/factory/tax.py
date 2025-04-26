from typing import Any, Callable

from aiogram import F, Router, types

from domain.commands.factory import PayTaxCommand
from domain.context.factory import UserFactoryContext
from domain.entity import Factory
from domain.results import Success
from infrastructure.command import CommandExecutor
from presentors.aiogram.kb import factory as kb
from presentors.aiogram.kb.callbacks import FactoryCB
from presentors.aiogram.messages import factory as msg
from presentors.aiogram.utils import Images
from presentors.shared.utils.auth import get_factory, get_user
from presentors.shared.utils.cache import cache
from presentors.shared.utils.di_context import with_context

router = Router()


@router.callback_query(F.data == FactoryCB.tax)
@get_factory
@cache(Images.factory_tax, types.FSInputFile(Images.factory_tax))
async def tax_page(
    call: types.CallbackQuery,
    factory: Factory,
    cached: Any,
    cache_func: Callable,
) -> None:
    sent = await call.message.edit_media(
        media=types.InputMediaPhoto(
            caption=msg.tax_page.format(factory.tax),
            media=cached,
        ),
        reply_markup=kb.tax_markup,
    )
    if sent.photo:
        cache_func(sent.photo[-1].file_id)


@router.callback_query(F.data == FactoryCB.pay_tax)
@get_factory
@get_user
@with_context(UserFactoryContext)
async def pay_tax(
    call: types.CallbackQuery,
    ctx: UserFactoryContext,
) -> None:
    result = await CommandExecutor().execute(
        PayTaxCommand(
            user_id=ctx.user.id,
            user_money=ctx.user.money,
            factory_id=ctx.factory.id,
            factory_tax=ctx.factory.tax,
        )
    )
    if isinstance(result, Success):
        text = msg.tax_page.format(0)
    else:
        text = result.reason
    if str(call.message.caption).strip() == result.strip():
        return
    await call.message.edit_caption(caption=text, reply_markup=kb.tax_markup)
