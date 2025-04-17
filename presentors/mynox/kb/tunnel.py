from aiogram.utils.keyboard import InlineKeyboardBuilder


def tunnel_markup(ids):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Заставить рабочих работать", callback_data=f"push-{ids}"
    )
    builder.button(text="К туннелям", callback_data="tunnels")
    return builder.as_markup()
