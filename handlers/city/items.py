from aiogram import types, F, Router

from replys import property_reply

router = Router()


@router.callback_query(F.data == 'имущество')
async def property_main(call: types.CallbackQuery):
    await call.message.edit_text('Если вы хотите сохранить ваши богатства,'
                                 ' приобретите имущество и не потеряете ни копейки.\n'
                                 'Ваше имущество: У вас нет имущества кроме фабрики',
                                 reply_markup=property_reply)

