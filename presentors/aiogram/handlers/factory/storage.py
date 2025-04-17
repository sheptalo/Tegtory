from aiogram import F, Router, types

from domain.entity.factory import Factory
from domain.entity.user import User
from domain.use_cases import UCFactory
from presentors.aiogram.kb import factory as kb
from presentors.aiogram.kb.callbacks import FactoryCB
from presentors.aiogram.messages import factory as msg
from presentors.shared.utils.auth import auth_user, have_factory

router = Router()


@router.callback_query(F.data == FactoryCB.storage)
@have_factory
async def open_storage(call: types.CallbackQuery, factory: Factory):
    stroka = msg.storage_title
    for product, amount in factory.storage.products.items():
        stroka += msg.storage_products.format(product.name, amount)
    stroka += msg.storage_footer.format(factory.storage.max_stock)
    await call.message.edit_caption(
        caption=stroka, reply_markup=kb.storage_markup
    )


@router.callback_query(F.data == FactoryCB.upgrade_storage)
@have_factory
@auth_user
async def upgrade_storage(
    call: types.CallbackQuery,
    factory: Factory,
    uc_factory: UCFactory,
    user: User,
):
    result = await uc_factory.upgrade_storage(factory.storage, user)
    if not result:
        return await open_storage(call)
    await call.answer(result, show_alert=True)
