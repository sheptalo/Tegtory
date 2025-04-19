from aiogram import Router, types
from aiogram.filters import Command

from common.settings import ASSETS_DIR
from domain.entity import User
from presentors.aiogram.filters.profile import ProfileFilter
from presentors.shared.utils.auth import get_user

router = Router()


@router.message(ProfileFilter())
@get_user
async def user_info(message: types.Message, user: User):
    await message.answer_photo(
        types.FSInputFile(ASSETS_DIR / "passport.png"),
        caption=str(user),
    )
