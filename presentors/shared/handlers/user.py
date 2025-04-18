from aiogram import Router, types
from aiogram.filters import Command

from common.settings import ASSETS_DIR
from domain.context.holder import UserHolder
from presentors.aiogram.filters.profile import ProfileFilter
from presentors.shared.utils.auth import get_user_operation

router = Router()


@router.message(ProfileFilter())
@get_user_operation
async def user_info(message: types.Message, user: UserHolder):
    await message.answer_photo(
        types.FSInputFile(ASSETS_DIR / "passport.png"),
        caption=str(user.entity),
    )


@router.message(Command("rename"))
@get_user_operation
async def rename_user(message: types.Message, user: UserHolder):
    user.entity.set_name(message.text[8:].strip())
    await user.use_case.update(user.entity)
    await user_info(message)
