from aiogram import F, Router, types
from aiogram.types import FSInputFile, InputMediaPhoto

from domain.entity import Factory
from presentors.aiogram.filters.factory import OpenFactoryFilter
from presentors.aiogram.kb import factory as kb
from presentors.aiogram.kb.callbacks import FactoryCB
from presentors.aiogram.utils import Images
from presentors.shared.utils.auth import have_factory
from presentors.shared.utils.cache import cache

router = Router()


@router.message(OpenFactoryFilter())
@have_factory
@cache(Images.factory, FSInputFile(Images.factory))
async def open_factory(
    message: types.Message, factory: Factory, cached, cache_func
):
    sent = await message.answer_photo(
        photo=cached,
        caption=str(factory),
        reply_markup=kb.main,
    )
    cache_func(sent.photo[-1].file_id)


@router.callback_query(F.data == FactoryCB.back)
@have_factory
@cache(Images.factory, FSInputFile(Images.factory))
async def callback_factory(
    call: types.CallbackQuery,
    factory: Factory,
    cached,
    cache_func,
):
    sent = await call.message.edit_media(
        media=InputMediaPhoto(
            media=cached,
            caption=str(factory),
        ),
        reply_markup=kb.main,
    )
    cache_func(sent.photo[-1].file_id)
