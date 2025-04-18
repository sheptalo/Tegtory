from aiogram import F, Router, types

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


@router.callback_query(F.data == FactoryCB.tax)
@get_factory_operation
@cache(Images.factory_tax, types.FSInputFile(Images.factory_tax))
async def tax_page(
    call: types.CallbackQuery,
    factory: FactoryHolder,
    cached,
    cache_func,
):
    sent = await call.message.edit_media(
        media=types.InputMediaPhoto(
            caption=msg.tax_page.format(factory.entity.tax),
            media=cached,
        ),
        reply_markup=kb.tax_markup,
    )
    cache_func(sent.photo[-1].file_id)


@router.callback_query(F.data == FactoryCB.pay_tax)
@get_factory_operation
@get_user_operation
async def pay_tax(
    call: types.CallbackQuery,
    factory: FactoryHolder,
    user: UserHolder,
):
    ctx = UserFactoryContext(factory=factory.entity, user=user.entity)
    result = await factory.use_case.pay_tax(ctx)
    if isinstance(result, Factory):
        result = msg.tax_page.format(factory.entity.tax)
    if str(call.message.caption).strip() == result.strip():
        return
    await call.message.edit_caption(caption=result, reply_markup=kb.tax_markup)
