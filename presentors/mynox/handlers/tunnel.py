from aiogram import F, Router, types

from ..kb.tunnel import tunnel_markup

router = Router()


# @router.callback_query(
#     F.data.split("-").len() == 2 and F.data.split("-")[1].isdigit()
# )
# async def tunnel_main(call: types.CallbackQuery):
#     ids = call.data.split("-")[1]
#     await call.message.edit_media(
#         media=types.InputMediaPhoto(media="", caption=str()),
#         reply_markup=tunnel_markup(ids),
#     )
