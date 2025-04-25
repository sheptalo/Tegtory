from aiogram import Router, types
from dishka import FromDishka

from domain.context.factory import UserFactoryContext
from domain.entity import Factory, Product
from domain.events import EventType
from domain.use_cases import UCFactory, UCUser
from infrastructure.injectors import inject, on_event
from presentors.aiogram.filters.factory import (
    ChooseProductFilter,
    ChooseTimeToWorkFilter,
    StartFactoryFilter,
    StartYourselfFactoryFilter,
)
from presentors.aiogram.handlers.factory.main import callback_factory
from presentors.aiogram.kb import factory as kb
from presentors.aiogram.messages import factory as msg
from presentors.shared.bot import TegtorySingleton
from presentors.shared.utils.auth import get_factory, get_user
from presentors.shared.utils.di_context import with_context

router = Router()


@router.callback_query(ChooseProductFilter())
@get_factory
@get_user
@with_context(UserFactoryContext)
async def choose_product(
    call: types.CallbackQuery,
    ctx: UserFactoryContext,
    use_case: FromDishka[UCFactory],
) -> None:
    result = await check_can_start_factory(ctx)
    if result:
        await call.answer(result, show_alert=True)
        return
    products = await use_case.get_available_products(ctx.factory)
    markup = kb.get_choose_product_markup(str(call.data), products)
    await call.message.edit_caption(
        caption=msg.choose_product, reply_markup=markup
    )


async def check_can_start_factory(ctx: UserFactoryContext) -> str | None:
    factory = ctx.factory
    result = None
    if factory.state:
        result = msg.start_factory_work.format(factory.minutes_to_work)
    elif ctx.user.state:
        result = msg.start_yourself_work.format(ctx.user.minutes_to_work)
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
    markup = kb.get_time_choose_markup(mode, product)
    await call.message.edit_caption(
        caption=msg.choose_product, reply_markup=markup
    )


@router.callback_query(StartYourselfFactoryFilter())
@get_factory
@get_user
@with_context(UserFactoryContext)
async def work_yourself(
    call: types.CallbackQuery,
    ctx: UserFactoryContext,
    use_case: FromDishka[UCUser],
) -> None:
    product, time = await get_product_time(call, ctx.factory)
    await use_case.start_work(ctx.factory, product, time, ctx.user)
    await callback_factory(call)


@router.callback_query(StartFactoryFilter())
@get_factory
async def start_factory(
    call: types.CallbackQuery,
    factory: Factory,
    use_case: FromDishka[UCFactory],
) -> None:
    product, time = await get_product_time(call, factory)
    result = await use_case.start_factory(factory, time, product)
    if result:
        await call.answer(str(result), show_alert=True)
    await callback_factory(call)


@on_event(EventType.EndFactoryWork)
async def end_factory_work(factory: Factory, stock: int) -> None:
    bot = TegtorySingleton()
    await bot.send_message(factory.id, msg.success_work_end.format(stock))


@inject(is_async=True)
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
