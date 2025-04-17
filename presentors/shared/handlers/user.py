from aiogram import Router, types
from aiogram.filters import Command

from common.settings import ASSETS_DIR
from domain.use_cases import UCUser
from presentors.aiogram.filters.profile import ProfileFilter
from presentors.shared.utils.auth import auth_user

router = Router()


@router.message(ProfileFilter())
@auth_user
async def user_info(message: types.Message, uc_user: UCUser, **_):
    user = await uc_user.get(message.from_user.id)
    await message.answer_photo(
        types.FSInputFile(ASSETS_DIR / "passport.png"), caption=str(user)
    )


@router.message(Command("rename"))
@auth_user
async def rename_user(message: types.Message, uc_user: UCUser, **_):
    user = await uc_user.get(message.from_user.id)
    user.set_name(message.text[8:].strip())
    await uc_user.update(user)
    await user_info(message)
