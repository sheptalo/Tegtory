from aiogram import Router, types

from common.settings import ASSETS_DIR
from domain.entities import User
from presenters.aiogram.filters.profile import ProfileFilter
from presenters.shared.utils.auth import get_user

router = Router()


@router.message(ProfileFilter())
@get_user
async def user_info(message: types.Message, user: User) -> None:
    await message.answer_photo(
        types.FSInputFile(ASSETS_DIR / "passport.png"),
        caption=str(user),
    )
