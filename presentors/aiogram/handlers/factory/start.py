from aiogram import Router, types

from domain.context.factory import StartWorkContext
from domain.context.holder import FactoryHolder, UserHolder
from domain.entity import Factory
from domain.events import EventType
from infrastructure.injectors import on_event
from presentors.aiogram.filters.factory import (
    ChooseProductFilter,
    ChooseTimeToWorkFilter,
    StartFactoryFilter,
    StartYourselfFactoryFilter,
)
from presentors.aiogram.kb import factory as kb
from presentors.aiogram.messages import factory as msg
from presentors.shared.bot import TegtorySingleton
from presentors.shared.utils.auth import (
    get_factory_operation,
    get_user_operation,
)

router = Router()


@router.callback_query(ChooseProductFilter())
@get_factory_operation
@get_user_operation
async def choose_product(
    call: types.CallbackQuery,
    factory: FactoryHolder,
    user: UserHolder,
):
    result = await check_can_start_factory(factory, user)
    if result:
        return await call.answer(result, show_alert=True)
    products = await factory.use_case.get_available_products(factory.entity)
    markup = kb.get_choose_product_markup(call.data, products)
    await call.message.edit_caption(
        caption=msg.choose_product, reply_markup=markup
    )


async def check_can_start_factory(
    factory: FactoryHolder,
    user: UserHolder,
) -> str | None:
    factory = factory.entity
    result = None
    if factory.state:
        result = msg.start_factory_work.format(factory.minutes_to_work)
    elif user.entity.state:
        result = msg.start_yourself_work.format(user.entity.minutes_to_work)
    return result


@router.callback_query(ChooseTimeToWorkFilter())
@get_factory_operation
async def choose_time(
    call: types.CallbackQuery,
    factory: FactoryHolder,
):
    mode = call.data.split(":")[1]
    product = await factory.use_case.get_available_product_by_name(
        factory.entity, call.data.split(":")[2]
    )
    markup = kb.get_time_choose_markup(mode, product)
    await call.message.edit_caption(
        caption=msg.choose_product, reply_markup=markup
    )


@router.callback_query(StartYourselfFactoryFilter())
@get_factory_operation
@get_user_operation
async def work_yourself(
    call: types.CallbackQuery,
    factory: FactoryHolder,
    user: UserHolder,
):
    ctx = await get_start_work_context(call, factory, user)
    await user.use_case.start_work(ctx)
    await choose_product(call, factory=factory, user=user)


@router.callback_query(StartFactoryFilter())
@get_factory_operation
async def start_factory(call: types.CallbackQuery, factory: FactoryHolder):
    ctx = await get_start_work_context(call, factory)
    result = await factory.use_case.start_factory(ctx)
    if result:
        await call.answer(str(result), show_alert=True)
    await choose_product(call, factory=factory)


@on_event(EventType.EndFactoryWork)
async def end_factory_work(factory: Factory, stock: int):
    bot = TegtorySingleton()
    await bot.send_message(factory.id, msg.success_work_end.format(stock))


async def get_start_work_context(
    call,
    factory_ctx: FactoryHolder,
    user_ctx: UserHolder = None,
):
    product, time = await get_product_time(call, factory_ctx)
    user = None
    if user_ctx:
        user = user_ctx.entity
    return StartWorkContext(
        factory=factory_ctx.entity, product=product, time=time, user=user
    )


async def get_product_time(
    call: types.CallbackQuery, factory_ctx: FactoryHolder
):
    product = await factory_ctx.use_case.get_available_product_by_name(
        factory_ctx.entity,
        call.data.split(":")[1],
    )
    return product, float(call.data.split(":")[2])
