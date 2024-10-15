import asyncio
import random

from aiogram import Router, types, F
from aiogram.filters import StateFilter

import time

from aiogram.types import InputMediaPhoto, URLInputFile

from bot import bot
from config import factory_image

from api import api

from pyrogram_main import get_chat_members
from replys import factory_reply, tax_markup, create_factory_markup
from handlers.factory_handlers import router as rt

router = Router()
router.include_router(rt)


@router.callback_query(F.data == 'back_factory')
async def back_factory(call: types.CallbackQuery):
    try:
        # await call.message.edit_caption(caption=str(api.factory(call.message.chat.id)), reply_markup=factory_reply)
        await call.message.edit_media(media=InputMediaPhoto(
                                        media=URLInputFile(factory_image(api.factory(call.message.chat.id).type)),
                                        caption=str(api.factory(call.message.chat.id))),
                                      caption=str(api.factory(call.message.chat.id)),
                                      reply_markup=factory_reply)
    except:
        pass


@router.message(F.text.lower().split()[0] == 'фабрика', StateFilter(None))
async def factory_main(message: types.Message):
    factory = api.factory(message.chat.id)
    if not factory.exists():
        return await message.reply('у тебя еще нет фабрики', reply_markup=create_factory_markup)
    _type = factory_image(factory.type)
    await message.answer_photo(URLInputFile(url=_type),
                               caption=str(factory),
                               reply_markup=factory_reply)


async def factory_working(call: types.CallbackQuery):
    factory = api.factory(call.message.chat.id)
    factory.state = 0
    workers = factory.workers
    if call.message.chat.type == "private":
        created = workers * 2 + random.randint(0, 20)
        factory.stock += created
        await bot.send_message(call.message.chat.id,
                               f'Рабочие на фабрике закончили работать, произведенно: {created} товаров')

        factory.tax += workers * 5
        await back_factory(call)

    else:
        await call.message.answer("Склад фабрики каждого пользователя пополнится в течении пары минут.")
        chat_members = await get_chat_members(call.message.chat.id)
        created_all = workers * 5 + random.randint(0, 20)
        created = created_all // len(chat_members)
        botik = await bot.get_me()
        for member in chat_members:
            try:
                if botik.id == member:
                    return
                api.factory(member).stock += created
                await bot.send_message(member, f"рабочие в чате закончили работу и ваш склад пополнился на {created:,}")
            except:
                pass
        await call.message.answer(f'Рабочие на фабрике закончили работать, в общем произведено '
                                  f'{created_all:,}')


@router.callback_query(F.data == 'start_factory')
async def start_factory(call: types.CallbackQuery):
    current_time = int(time.time())
    factory = api.factory(call.message.chat.id)
    state, tax, last_click, workers = factory.get('state,tax,started_work_at,workers')
    _time = 1800

    if workers == 0:
        return await call.answer('Фабрику нельзя запустить если рабочих нет', show_alert=True)

    if not last_click or current_time - last_click >= _time:
        if state == 1:
            return await factory_working(call)

        if tax > 20000:
            return await call.message.edit_text(f'У вас Неуплата налогов оплатите {tax} чтобы запустить фабрику',
                                                reply_markup=tax_markup)

        await call.answer('Рабочие приступили к работе', show_alert=True)

        factory.set({
            'owner_id': factory.player_id,
            'started_work_at': current_time,
            'state': 1
        })
        await back_factory(call)
        task = asyncio.create_task(work_timer(call))
    else:
        await call.answer(f'Фабрике осталось работать {last_click + _time - current_time} секунд', show_alert=True)


async def work_timer(call: types.CallbackQuery):
    await asyncio.sleep(1800)
    factory = api.factory(call.message.chat.id)
    if factory.state == 1:
        await factory_working(call)


