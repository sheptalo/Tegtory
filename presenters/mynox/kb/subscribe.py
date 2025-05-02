from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

subscribed_channel = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Готово", callback_data="subscribe")],
    ]
)
