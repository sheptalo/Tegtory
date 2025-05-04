from collections.abc import Callable
from typing import Any

from aiogram import F, Router, types

from domain.entities import Factory
from presenters.aiogram.filters.factory import OpenFactoryFilter
from presenters.aiogram.images import Images
from presenters.aiogram.kb import FactoryCB
from presenters.aiogram.kb import factory as kb
from presenters.shared.utils import cache, get_factory

router = Router()


@router.message(OpenFactoryFilter())
@get_factory
@cache(Images.factory, types.FSInputFile(Images.factory))
async def open_factory(
    message: types.Message, factory: Factory, cached: Any, cache_func: Callable
):
    sent = await message.answer_photo(
        photo=cached, caption=str(factory), reply_markup=kb.main
    )
    if sent.photo:
        cache_func(sent.photo[-1].file_id)


@router.callback_query(F.data == FactoryCB.back)
@get_factory
@cache(Images.factory, types.FSInputFile(Images.factory))
async def callback_factory(
    call: types.CallbackQuery,
    factory: Factory,
    cached: Any,
    cache_func: Callable,
) -> None:
    sent = await call.message.edit_media(
        media=types.InputMediaPhoto(media=cached, caption=str(factory)),
        reply_markup=kb.main,
    )
    if sent.photo:
        cache_func(sent.photo[-1].file_id)
