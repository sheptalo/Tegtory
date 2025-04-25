from typing import Any, Callable

from aiogram import F, Router, types
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from domain.commands.factory import CreateFactoryCommand, UpgradeFactoryCommand
from domain.context.factory import UserFactoryContext
from domain.entity import Factory, User
from domain.results import Success
from infrastructure.command import CommandExecutor
from presentors.aiogram.handlers.factory.main import open_factory
from presentors.aiogram.kb import factory as kb
from presentors.aiogram.kb.callbacks import FactoryCB
from presentors.aiogram.messages import factory as msg
from presentors.aiogram.states import factory as states
from presentors.aiogram.utils import Images
from presentors.shared.utils.auth import (
    get_factory,
    get_user,
)
from presentors.shared.utils.cache import cache
from presentors.shared.utils.di_context import with_context

router = Router()


@router.callback_query(F.data == FactoryCB.create)
@get_user
async def create_factory_callback(
    call: types.CallbackQuery, state: FSMContext, user: User
) -> None:
    await call.message.edit_text(msg.set_name, reply_markup=None)
    await state.set_state(states.Create.name)


@router.message(StateFilter(states.Create.name))
async def finish_create_factory_handler(
    message: types.Message, state: FSMContext
) -> None:
    await message.delete()
    result = await CommandExecutor().execute(
        CreateFactoryCommand(id=message.from_user.id, name=str(message.text)),
    )
    if isinstance(result, Success):
        await state.clear()
        await open_factory(message)
        return
    await message.answer(msg.unique_name)


@router.callback_query(F.data == FactoryCB.upgrade)
@get_factory
@cache(Images.factory_upgrade, types.FSInputFile(Images.factory_upgrade))
async def upgrade_factory(
    call: types.CallbackQuery,
    factory: Factory,
    cached: Any,
    cache_func: Callable,
) -> None:
    try:
        sent = await call.message.edit_media(
            media=types.InputMediaPhoto(
                caption=msg.upgrade_page.format(
                    factory.level, factory.upgrade_price
                ),
                media=cached,
            ),
            reply_markup=kb.upgrade_markup,
        )
        cache_func(sent.photo[-1].file_id)
    except TelegramBadRequest:
        pass


@router.callback_query(F.data == FactoryCB.upgrade_conf)
@get_factory
@get_user
@with_context(UserFactoryContext)
async def try_to_upgrade_factory(
    call: types.CallbackQuery, ctx: UserFactoryContext
) -> None:
    result = await CommandExecutor().execute(
        UpgradeFactoryCommand(
            factory_id=ctx.factory.id,
            factory_upgrade_price=ctx.factory.upgrade_price,
            user_id=ctx.user.id,
            user_money=ctx.user.money,
        )
    )

    if isinstance(result, Success):
        await upgrade_factory(call)
        return
    await call.message.edit_caption(
        caption=result.reason, reply_markup=kb.failed_upgrade_markup
    )
