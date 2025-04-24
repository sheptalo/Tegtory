from aiogram import F, Router, types

from domain import entity, results
from domain.commands.factory import UpgradeStorageCommand
from domain.context import UserFactoryContext
from infrastructure.command import CommandExecutor
from presentors.aiogram.kb import factory as kb
from presentors.aiogram.kb.callbacks import FactoryCB
from presentors.aiogram.messages import factory as msg
from presentors.shared.utils.auth import (
    get_factory,
    get_storage_from_factory,
    get_user,
)
from presentors.shared.utils.di_context import with_context

router = Router()


@router.callback_query(F.data == FactoryCB.storage)
@get_factory
@get_storage_from_factory
async def open_storage(call: types.CallbackQuery, storage: entity.Storage):
    result = get_storage_page_text(storage)
    await call.message.edit_caption(
        caption=result, reply_markup=kb.storage_markup
    )


@router.callback_query(F.data == FactoryCB.upgrade_storage)
@get_factory
@get_user
@with_context(UserFactoryContext)
async def upgrade_storage(call: types.CallbackQuery, ctx: UserFactoryContext):
    result = await CommandExecutor().execute(
        UpgradeStorageCommand(
            factory_id=ctx.factory.id,
            storage=ctx.factory.storage,
            user_money=ctx.user.money,
            user_id=ctx.user.id,
        )
    )
    if isinstance(result, results.Failure):
        return await call.answer(result.reason, show_alert=True)
    return await open_storage(call)


def get_storage_page_text(storage: entity.Storage):
    result = msg.storage_title
    for product, amount in storage.products.items():
        result += msg.storage_products.format(product.name, amount)
    result += msg.storage_footer.format(storage.max_stock)
    return result
