# region donate
from aiogram import F, Router
from aiogram.types import CallbackQuery

router = Router()


@router.callback_query(F.data == 'донат')
async def donate(call: CallbackQuery):
    return await call.answer('В данный момент недоступно', show_alert=True)
    # await message.answer("сейчас можно купить только 100к очков за 85 руб")
    # await bot.send_invoice(message.from_user.id,
    #                        '100.000 очков',
    #                        'Закончились деньги? приобрети 100.000 очков прямо сейчас.',
    #                        'something',
    #                        provider_token=provider_t,
    #                        currency='rub',
    #                        prices=prices)


# endregion
