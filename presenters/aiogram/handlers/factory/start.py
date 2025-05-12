from typing import Any

from aiogram import Router, types
from dishka import FromDishka

from domain import entities, results
from domain.commands.user import StartUserWorkCommand
from domain.entities import Factory, Product
from domain.events import EventType
from domain.use_cases import UCFactory
from infrastructure import CommandExecutor
from infrastructure.injectors import inject, on_event
from presenters.aiogram.filters.factory import (
    ChooseProductFilter,
    ChooseTimeToWorkFilter,
    StartFactoryFilter,
    StartYourselfFactoryFilter,
)
from presenters.aiogram.handlers.factory.main import callback_factory
from presenters.aiogram.kb import factory as kb
from presenters.aiogram.messages import factory as msg
from presenters.shared.bot import TegtorySingleton
from presenters.shared.utils import get_factory

router = Router()


@router.callback_query(ChooseProductFilter())
@get_factory
async def choose_product(
    call: types.CallbackQuery,
    user: entities.User,
    factory: entities.Factory,
    use_case: FromDishka[UCFactory],
) -> Any:
    can_start = await check_can_start_factory(user, factory)
    if can_start:
        return await call.answer(can_start, show_alert=True)
    result = await use_case.get_available_products(factory)
    markup = kb.get_choose_product_markup(str(call.data), result)
    await call.message.edit_caption(
        caption=msg.choose_product, reply_markup=markup
    )


async def check_can_start_factory(
    user: entities.User, factory: entities.Factory
) -> str | None:
    result = None
    if factory.state:
        result = msg.start_factory_work.format(factory.minutes_to_work)
    elif user.state:
        result = msg.start_yourself_work.format(user.minutes_to_work)
    return result


@router.callback_query(ChooseTimeToWorkFilter())
@get_factory
async def choose_time(
    call: types.CallbackQuery,
    factory: Factory,
    use_case: FromDishka[UCFactory],
) -> None:
    mode = call.data.split(":")[1]
    product = await use_case.find_product_by_name(
        factory, call.data.split(":")[2]
    )
    if not product:
        raise ValueError
    markup = kb.get_time_choose_markup(mode, product)
    await call.message.edit_caption(
        caption=msg.choose_product, reply_markup=markup
    )


@router.callback_query(StartYourselfFactoryFilter())
@get_factory
async def work_yourself(
    call: types.CallbackQuery,
    user: entities.User,
    factory: entities.Factory,
    cmd_executor: CommandExecutor,
) -> Any:
    product, time = await get_product_time(call, factory)
    result = await cmd_executor.execute(
        StartUserWorkCommand(
            user=user,
            product=product,
            time=time,
            factory=factory,
        )
    )
    if isinstance(result, results.Success):
        return await callback_factory(call)
    await call.answer(result.reason, show_alert=True)


@router.callback_query(StartFactoryFilter())
@get_factory
async def start_factory(
    call: types.CallbackQuery,
    factory: Factory,
    use_case: FromDishka[UCFactory],
) -> Any:
    product, time = await get_product_time(call, factory)
    result: Any = await use_case.start_factory(factory, time, product)
    if result:
        return await call.answer(str(result), show_alert=True)
    await callback_factory(call)


@on_event(EventType.EndFactoryWork)
async def end_factory_work(data: dict[str, Factory | int]) -> None:
    factory = data.get("factory")
    stock = data.get("stock")
    if not isinstance(factory, Factory) or not isinstance(stock, int):
        return
    bot = TegtorySingleton()
    await bot.send_message(factory.id, msg.success_work_end.format(stock))


@inject
async def get_product_time(
    call: types.CallbackQuery,
    factory: Factory,
    use_case: FromDishka[UCFactory],
) -> tuple[Product, float] | None:
    product = await use_case.find_product_by_name(
        factory, call.data.split(":")[1]
    )
    if not product:
        return None
    return product, float(call.data.split(":")[2])
