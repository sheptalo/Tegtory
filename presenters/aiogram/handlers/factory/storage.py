from typing import Any

from aiogram import F, Router, types

from domain import entities, results
from domain.commands import UpgradeStorageCommand
from domain.context import UserFactoryContext
from infrastructure import CommandExecutor
from presenters.aiogram.kb import factory as kb
from presenters.aiogram.kb.callbacks import FactoryCB
from presenters.aiogram.messages import factory as msg
from presenters.shared.utils import (
    get_factory,
    get_storage_from_factory,
    get_user,
    with_context,
)

router = Router()


@router.callback_query(F.data == FactoryCB.storage)
@get_factory
@get_storage_from_factory
async def open_storage(
    call: types.CallbackQuery, storage: entities.Storage
) -> None:
    result = get_storage_page_text(storage)
    await call.message.edit_caption(
        caption=result, reply_markup=kb.storage_markup
    )


@router.callback_query(F.data == FactoryCB.upgrade_storage)
@get_factory
@get_user
@with_context(UserFactoryContext)
async def upgrade_storage(
    call: types.CallbackQuery, ctx: UserFactoryContext
) -> Any:
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
    await open_storage(call)


def get_storage_page_text(storage: entities.Storage) -> str:
    result = msg.storage_title
    for product, amount in storage.products.items():
        result += msg.storage_products.format(product.name, amount)
    result += msg.storage_footer.format(storage.max_stock)
    return result
