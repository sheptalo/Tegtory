from aiogram import F, Router, types
from dishka import FromDishka

from domain.context.factory import UserFactoryContext
from domain.entity import Factory
from domain.use_cases import UCFactory
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
    cached,
    cache_func,
):
    sent = await call.message.edit_media(
        media=types.InputMediaPhoto(
            caption=msg.tax_page.format(factory.tax),
            media=cached,
        ),
        reply_markup=kb.tax_markup,
    )
    cache_func(sent.photo[-1].file_id)


@router.callback_query(F.data == FactoryCB.pay_tax)
@get_factory
@get_user
@with_context(UserFactoryContext)
async def pay_tax(
    call: types.CallbackQuery,
    ctx: UserFactoryContext,
    use_case: FromDishka[UCFactory],
):
    result = await use_case.pay_tax(ctx.user, ctx.factory)
    if isinstance(result, Factory):
        result = msg.tax_page.format(result.tax)
    if str(call.message.caption).strip() == result.strip():
        return
    await call.message.edit_caption(caption=result, reply_markup=kb.tax_markup)
