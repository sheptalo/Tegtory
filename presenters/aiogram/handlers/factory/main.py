from typing import Any, Callable

from aiogram import F, Router, types
from aiogram.types import FSInputFile, InputMediaPhoto

from domain.entities import Factory
from presenters.aiogram.filters.factory import OpenFactoryFilter
from presenters.aiogram.kb import factory as kb
from presenters.aiogram.kb.callbacks import FactoryCB
from presenters.aiogram.utils import Images
from presenters.shared.utils.auth import get_factory
from presenters.shared.utils.cache import cache

router = Router()


@router.message(OpenFactoryFilter())
@get_factory
@cache(Images.factory, FSInputFile(Images.factory))
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
@cache(Images.factory, FSInputFile(Images.factory))
async def callback_factory(
    call: types.CallbackQuery,
    factory: Factory,
    cached: Any,
    cache_func: Callable,
) -> None:
    sent = await call.message.edit_media(
        media=InputMediaPhoto(media=cached, caption=str(factory)),
        reply_markup=kb.main,
    )
    if sent.photo:
        cache_func(sent.photo[-1].file_id)
