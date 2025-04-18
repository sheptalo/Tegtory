from aiogram import F, Router, types
from aiogram.types import FSInputFile, InputMediaPhoto

from domain.context.holder import FactoryHolder
from presentors.aiogram.filters.factory import OpenFactoryFilter
from presentors.aiogram.kb import factory as kb
from presentors.aiogram.kb.callbacks import FactoryCB
from presentors.aiogram.utils import Images
from presentors.shared.utils.auth import get_factory_operation
from presentors.shared.utils.cache import cache

router = Router()


@router.message(OpenFactoryFilter())
@get_factory_operation
@cache(Images.factory, FSInputFile(Images.factory))
async def open_factory(
    message: types.Message, factory: FactoryHolder, cached, cache_func
):
    sent = await message.answer_photo(
        photo=cached, caption=str(factory.entity), reply_markup=kb.main
    )
    cache_func(sent.photo[-1].file_id)


@router.callback_query(F.data == FactoryCB.back)
@get_factory_operation
@cache(Images.factory, FSInputFile(Images.factory))
async def callback_factory(
    call: types.CallbackQuery, factory: FactoryHolder, cached, cache_func
):
    sent = await call.message.edit_media(
        media=InputMediaPhoto(media=cached, caption=str(factory.entity)),
        reply_markup=kb.main,
    )
    cache_func(sent.photo[-1].file_id)
