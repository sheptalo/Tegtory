from aiogram import F, Router, types
from dishka import FromDishka

from domain.context.factory import UserFactoryContext
from domain.entity import Factory, Storage, User
from domain.use_cases import UCFactory
from presentors.aiogram.kb import factory as kb
from presentors.aiogram.kb.callbacks import FactoryCB
from presentors.aiogram.messages import factory as msg
from presentors.shared.utils.auth import (
    get_factory,
    get_user,
)
from presentors.shared.utils.di_context import with_context

router = Router()


@router.callback_query(F.data == FactoryCB.storage)
@get_factory
async def open_storage(call: types.CallbackQuery, factory: Factory):
    result = get_storage_page_text(factory.storage)
    await call.message.edit_caption(
        caption=result, reply_markup=kb.storage_markup
    )


@router.callback_query(F.data == FactoryCB.upgrade_storage)
@get_factory
@get_user
@with_context(UserFactoryContext)
async def upgrade_storage(
    call: types.CallbackQuery,
    ctx: UserFactoryContext,
    use_case: FromDishka[UCFactory],
):
    result = await use_case.upgrade_storage(ctx.user, ctx.factory.storage)
    if isinstance(result, Storage):
        return await open_storage(call)
    if isinstance(result, str):
        await call.answer(result, show_alert=True)


def get_storage_page_text(storage: Storage):
    result = msg.storage_title
    for product, amount in storage.products.items():
        result += msg.storage_products.format(product.name, amount)
    result += msg.storage_footer.format(storage.max_stock)
    return result
