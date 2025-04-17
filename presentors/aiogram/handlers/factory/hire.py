from aiogram import F, Router, types
from aiogram.types import InputMediaPhoto

from domain.entity import Factory, User
from domain.use_cases import UCFactory
from presentors.aiogram.kb import factory as kb
from presentors.aiogram.kb.callbacks import FactoryCB
from presentors.aiogram.messages import factory as msg
from presentors.aiogram.utils import Images
from presentors.shared.utils.auth import auth_user, have_factory
from presentors.shared.utils.cache import cache

router = Router()


@router.callback_query(F.data == FactoryCB.workers)
@have_factory
@cache(Images.factory_hire, types.FSInputFile(Images.factory_hire))
async def workers_page(
    call: types.CallbackQuery, factory: Factory, cached, cache_func,
):
    sent = await call.message.edit_media(
        media=InputMediaPhoto(
            caption=msg.workers_page.format(
                factory.workers, factory.hire_available, factory.hire_price
            ),
            media=cached,
        ),
        reply_markup=kb.hire_markup,
    )
    cache_func(sent.photo[-1].file_id)


@router.callback_query(F.data == FactoryCB.hire)
@have_factory
@auth_user
async def hire(
    call: types.CallbackQuery,
    factory: Factory,
    user: User,
    uc_factory: UCFactory,
):
    result = await uc_factory.hire(factory, user)
    markup = kb.failed_hire_markup
    if isinstance(result, Factory):
        result = msg.workers_page.format(
            result.workers, result.hire_available, result.hire_price
        )
        markup = kb.hire_markup

    await call.message.edit_caption(caption=str(result), reply_markup=markup)
