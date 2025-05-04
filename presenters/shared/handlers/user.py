from aiogram import Router, types

from common.settings import ASSETS_DIR
from domain.entities import User

from ..filters.profile import ProfileFilter
from ..messages.user import format_user
from ..utils.auth import get_user

router = Router()


@router.message(ProfileFilter())
@get_user
async def user_info(message: types.Message, user: User) -> None:
    await message.answer_photo(
        types.FSInputFile(ASSETS_DIR / "passport.png"),
        caption=format_user(user),
    )
