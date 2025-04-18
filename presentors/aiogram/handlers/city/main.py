from aiogram import F, Router, types

from presentors.aiogram.filters.city import CityFilter
from presentors.aiogram.kb import city as kb
from presentors.aiogram.kb.callbacks import CityCB
from presentors.aiogram.messages import city as msg
from presentors.aiogram.utils import Images
from presentors.shared.utils.auth import get_factory_operation
from presentors.shared.utils.cache import cache

router = Router()


@router.message(CityFilter())
@cache(Images.city, types.FSInputFile(Images.city))
async def city_page(
    message: types.Message,
    cached: types.FSInputFile | str,
    cache_func: callable,
):
    sent = await message.answer_photo(
        photo=cached,
        caption=msg.main,
        reply_markup=kb.city_markup,
    )
    cache_func(sent.photo[-1].file_id)


@router.callback_query(F.data == CityCB.back)
async def city_callback(call: types.CallbackQuery):
    await call.message.edit_caption(
        caption=msg.main, reply_markup=kb.city_markup
    )


@router.callback_query(F.data == CityCB.trading_companies)
@get_factory_operation
async def trading_companies_page(call: types.CallbackQuery):
    await call.message.edit_text(text=msg.main)
