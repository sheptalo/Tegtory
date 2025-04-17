from aiogram import Router, types

from domain.entity import Factory, User
from domain.events import EventType
from domain.use_cases import UCFactory, UCUser
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
from presentors.shared.utils.auth import auth_user, have_factory

router = Router()


@router.callback_query(ChooseProductFilter())
@have_factory
@auth_user
async def choose_product(
    call: types.CallbackQuery,
    factory: Factory,
    uc_factory: UCFactory,
    user: User,
):
    if factory.state:
        return await call.answer(
            msg.start_factory_work.format(factory.minutes_to_work),
            show_alert=True,
        )
    if user.state:
        return await call.answer(
            msg.start_yourself_work.format(user.minutes_to_work),
            show_alert=True,
        )
    products = await uc_factory.get_available_products(factory)
    markup = kb.get_choose_product_markup(call.data, products)
    await call.message.edit_caption(
        caption=msg.choose_product, reply_markup=markup
    )


@router.callback_query(ChooseTimeToWorkFilter())
@have_factory
async def choose_time(
    call: types.CallbackQuery, uc_factory: UCFactory, factory: Factory
):
    mode = call.data.split(":")[1]
    product = await uc_factory.get_available_product_by_name(
        factory, call.data.split(":")[2]
    )
    markup = kb.get_time_choose_markup(mode, product)
    await call.message.edit_caption(
        caption=msg.choose_product, reply_markup=markup
    )


@router.callback_query(StartYourselfFactoryFilter())
@have_factory
@auth_user
async def work_yourself(
    call: types.CallbackQuery,
    user: User,
    factory: Factory,
    uc_user: UCUser,
    uc_factory: UCFactory,
):
    product, time = await get_product_time(call, factory, uc_factory)
    user = await uc_user.start_work(user, factory, product, time)
    await choose_product(
        call, user=user, uc_factory=uc_factory, factory=factory
    )


@router.callback_query(StartFactoryFilter())
@have_factory
async def start_factory(
    call: types.CallbackQuery, factory: Factory, uc_factory: UCFactory
):
    product, time = await get_product_time(call, factory, uc_factory)
    result = await uc_factory.start_factory(factory, product, time)
    if isinstance(result, Factory):
        await choose_product(
            call, uc_factory=uc_factory, factory=factory
        )
    await call.answer(str(result), show_alert=True)


@on_event(EventType.EndFactoryWork)
async def end_factory_work(factory: Factory, stock: int):
    bot = TegtorySingleton()
    await bot.send_message(factory.id, msg.success_work_end.format(stock))


async def get_product_time(
    call: types.CallbackQuery, factory: Factory, uc_factory: UCFactory
):
    product = await uc_factory.get_available_product_by_name(
        factory,
        call.data.split(":")[1],
    )
    return product, float(call.data.split(":")[2])
