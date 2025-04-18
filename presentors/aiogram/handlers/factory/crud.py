from aiogram import F, Router, types
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from domain.context.factory import UserFactoryContext
from domain.context.holder import FactoryHolder, UserHolder
from domain.entity import Factory
from domain.use_cases import UCFactory
from presentors.aiogram.handlers.factory.main import open_factory
from presentors.aiogram.kb import factory as kb
from presentors.aiogram.kb.callbacks import FactoryCB
from presentors.aiogram.messages import factory as msg
from presentors.aiogram.states import factory as states
from presentors.aiogram.utils import Images
from presentors.shared.utils.auth import (
    get_factory_operation,
    get_user_operation,
)
from presentors.shared.utils.cache import cache

router = Router()


@router.callback_query(F.data == FactoryCB.create)
async def create_factory_callback(
    call: types.CallbackQuery, state: FSMContext
):
    await call.message.edit_text(msg.set_name, reply_markup=None)
    await state.set_state(states.Create.name)


@router.message(StateFilter(states.Create.name))
@inject
async def finish_create_factory_handler(
    message: types.Message,
    state: FSMContext,
    factory_use_case: FromDishka[UCFactory],
):
    await message.delete()
    factory = Factory(id=message.from_user.id, name=message.text)
    result = await factory_use_case.create(factory)
    if result:
        await state.clear()
        return await open_factory(message)
    await message.answer(msg.unique_name)


@router.message(Command("rename_factory"))
@get_factory_operation
async def rename_factory(message: types.Message, state: FSMContext):
    await message.answer(msg.set_name)
    await state.set_state(states.Rename.new_name)


@router.message(StateFilter(states.Rename.new_name))
@get_factory_operation
async def complete_rename_factory(
    message: types.Message, state: FSMContext, factory: FactoryHolder
):
    factory.entity.rename(message.text)
    result = await factory.use_case.rename(factory.entity)
    await state.clear()
    await message.answer(
        msg.successfully_rename if result else msg.unique_name
    )


@router.callback_query(F.data == FactoryCB.upgrade)
@get_factory_operation
@cache(Images.factory_upgrade, types.FSInputFile(Images.factory_upgrade))
async def upgrade_factory(
    call: types.CallbackQuery, factory: FactoryHolder, cached, cache_func
):
    try:
        sent = await call.message.edit_media(
            media=types.InputMediaPhoto(
                caption=msg.upgrade_page.format(
                    factory.entity.level, factory.entity.upgrade_price
                ),
                media=cached,
            ),
            reply_markup=kb.upgrade_markup,
        )
        cache_func(sent.photo[-1].file_id)
    except TelegramBadRequest:
        pass


@router.callback_query(F.data == FactoryCB.upgrade_conf)
@get_factory_operation
@get_user_operation
async def try_to_upgrade_factory(
    call: types.CallbackQuery, user: UserHolder, factory: FactoryHolder
):
    ctx = UserFactoryContext(factory=factory.entity, user=user.entity)
    result = await factory.use_case.upgrade(ctx)

    markup = kb.failed_upgrade_markup

    if isinstance(result, Factory):
        result = msg.upgrade_page.format(factory.level, factory.upgrade_price)
        markup = kb.upgrade_markup

    await call.message.edit_caption(caption=result, reply_markup=markup)
