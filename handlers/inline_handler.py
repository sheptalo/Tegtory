import os

import requests
from aiogram import types, Router
from bot import bot, api

router = Router()


@router.inline_query()
async def query(inline_query: types.InlineQuery):
    q = inline_query.query.replace("@", "")
    user = api.player(q)
    user_data = user.get("name,money,stolar,rating,league,clan_name,id,titles")
    a = types.InlineQueryResultCachedPhoto(
        id="0",
        photo_file_id="AgACAgIAAxkBAAIBtWcw8WiUYngUQvRWaEJfoajy8xkVAAJt7DEbumOISY63-g73HOakAQADAgADeQADNgQ",
    )
    if user_data:
        _text = f"""
{user_data[0]}

Баланс: {user_data[1]:,}
SC: {user_data[2]:,}

Рейтинг: {user_data[3]:,}
Лига: {user_data[4]}

Oбъединение: {user_data[5].replace('_', ' ')}
        """
        title = user_data[7]
        if title:
            _text += "\n\nТитулы:\n"
            for name in title.split():
                _text += f"{name.replace('_', ' ')}\n"

        req = requests.post(
            os.environ.get("API_URL") + "api/v2/image/" + q,
            json={"text": _text},
            verify=False,
        )
        txt = req.json()
        if txt:
            msg = await bot.send_photo("-4599348567", types.URLInputFile(txt))
            print(txt)
            a = types.InlineQueryResultCachedPhoto(
                id="0",
                photo_file_id=msg.photo[-1].file_id,
            )
    await inline_query.answer([a], is_personal=True)
