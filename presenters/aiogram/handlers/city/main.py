from typing import Callable

from aiogram import F, Router, types

from presenters.aiogram.filters.city import CityFilter
from presenters.aiogram.kb import city as kb
from presenters.aiogram.kb.callbacks import CityCB
from presenters.aiogram.messages import city as msg
from presenters.aiogram.utils import Images
from presenters.shared.utils.auth import get_factory
from presenters.shared.utils.cache import cache

router = Router()


@router.message(CityFilter())
@cache(Images.city, types.FSInputFile(Images.city))
async def city_page(
    message: types.Message,
    cached: types.FSInputFile | str,
    cache_func: Callable,
) -> None:
    sent = await message.answer_photo(
        photo=cached,
        caption=msg.main,
        reply_markup=kb.city_markup,
    )
    if sent.photo:
        cache_func(sent.photo[-1].file_id)


@router.callback_query(F.data == CityCB.back)
async def city_callback(call: types.CallbackQuery) -> None:
    await call.message.edit_caption(
        caption=msg.main, reply_markup=kb.city_markup
    )


@router.callback_query(F.data == CityCB.trading_companies)
@get_factory
async def trading_companies_page(call: types.CallbackQuery) -> None:
    await call.message.edit_text(text=msg.main)
