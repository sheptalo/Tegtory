from aiogram import F, Router, types

from ..kb.city import city_markup

router = Router()


@router.callback_query(F.data == "city")
async def city(call: types.CallbackQuery):
    await call.message.edit_media(
        media=types.InputMediaPhoto(
            media="",
            caption="Вы отправились в город. Куда направимся?",
        ),
        reply_markup=city_markup,
    )
