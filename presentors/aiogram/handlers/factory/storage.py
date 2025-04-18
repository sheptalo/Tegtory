from aiogram import F, Router, types

from domain.context.holder import FactoryHolder, UserHolder
from domain.entity import Storage
from presentors.aiogram.kb import factory as kb
from presentors.aiogram.kb.callbacks import FactoryCB
from presentors.aiogram.messages import factory as msg
from presentors.shared.utils.auth import (
    get_factory_operation,
    get_user_operation,
)

router = Router()


@router.callback_query(F.data == FactoryCB.storage)
@get_factory_operation
async def open_storage(call: types.CallbackQuery, factory: FactoryHolder):
    result = get_storage_page_text(factory.entity.storage)
    await call.message.edit_caption(
        caption=result, reply_markup=kb.storage_markup
    )


@router.callback_query(F.data == FactoryCB.upgrade_storage)
@get_factory_operation
@get_user_operation
async def upgrade_storage(
    call: types.CallbackQuery, factory: FactoryHolder, user: UserHolder
):
    result = await factory.use_case.upgrade_storage(
        factory.entity.storage, user.entity
    )
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
