from aiogram import F, Router, types

from domain.entity import Factory, User
from domain.use_cases import UCFactory
from presentors.aiogram.kb import factory as kb
from presentors.aiogram.kb.callbacks import FactoryCB
from presentors.aiogram.messages import factory as msg
from presentors.aiogram.utils import Images
from presentors.shared.utils.auth import auth_user, have_factory
from presentors.shared.utils.cache import cache

router = Router()


@router.callback_query(F.data == FactoryCB.tax)
@have_factory
@cache(Images.factory_tax, types.FSInputFile(Images.factory_tax))
async def tax_page(
    call: types.CallbackQuery, factory: Factory, cached, cache_func
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
@have_factory
@auth_user
async def pay_tax(
    call: types.CallbackQuery,
    factory: Factory,
    uc_factory: UCFactory,
    user: User
):
    result = await uc_factory.pay_tax(factory, user)
    if isinstance(result, Factory):
        result = msg.tax_page.format(factory.tax)
    if str(call.message.caption).strip() == result.strip():
        return call.answer(msg.empty_tax)
    await call.message.edit_caption(caption=result, reply_markup=kb.tax_markup)
