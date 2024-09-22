import random

from aiogram import Router, types, F
from aiogram.filters import StateFilter

import time

from aiogram.types import FSInputFile, InputMediaPhoto, URLInputFile

from bot import bot
from config import factory_image

from db import Factory

from pyrogram_main import get_chat_members
from replys import factory_reply, tax_markup, create_factory_markup
from handlers.factory_handlers import router as rt

router = Router()
router.include_router(rt)


@router.callback_query(F.data == 'back_factory')
async def back_factory(call: types.CallbackQuery):
    try:
        # await call.message.edit_caption(caption=str(Factory(call.message.chat.id)), reply_markup=factory_reply)
        await call.message.edit_media(media=InputMediaPhoto(
                                        media=URLInputFile(factory_image(Factory(call.message.chat.id).type))),
                                      caption=str(Factory(call.message.chat.id)),
                                      reply_markup=factory_reply)
    except:
        pass


@router.message(F.text.lower().split()[0] == 'фабрика', StateFilter(None))
async def factory_main(message: types.Message):
    factory = Factory(message.chat.id)
    if not factory.exists():
        return await message.reply('у тебя еще нет фабрики', reply_markup=create_factory_markup)
    _type = factory_image(factory.type)
    await message.answer_photo(URLInputFile(url=_type),
                               str(factory),
                               reply_markup=factory_reply)


async def factory_working(call: types.CallbackQuery):
    if call.message.chat.type == "private":

        factory = Factory(call.message.chat.id)
        workers = factory.workers
        created = workers * 2 + random.randint(0, 20)
        factory.stock += created
        await bot.send_message(call.message.chat.id,
                               f'Рабочие на фабрике закончили работать, произведенно: {created}')

        factory.tax += workers * 5

    else:
        await call.message.answer("Склад фабрики каждого пользователя пополнится в течении пары минут.")
        chat_members = await get_chat_members(call.message.chat.id)

        factory = Factory(call.message.chat.id)
        workers = factory.workers
        created = workers * 5 + random.randint(0, 20) // len(chat_members)
        botik = await bot.get_me()
        for member in chat_members:
            try:
                if botik.id == member:
                    return
                Factory(member).stock += created
                await bot.send_message(member, f"рабочие в чате закончили работу и ваш склад пополнился на {created:,}")
            except:
                pass
        await call.message.answer(f'Рабочие на фабрике закончили работать, в общем произведено '
                                  f'{workers * 5 + random.randint(0, 20):,}')


@router.callback_query(F.data == 'start_factory')
async def start_factory(call: types.CallbackQuery):
    current_time = int(time.time())
    factory = Factory(call.message.chat.id)
    last_click = factory.start_work_at
    _time = 900

    if factory.workers == 0:
        return await call.message.answer('Фабрику нельзя запустить если рабочих нет')

    if not last_click or current_time - last_click >= _time:
        if factory.state == 1:
            factory.state = 0
            return await factory_working(call)

        if factory.tax > 20000:
            return await call.message.edit_text(f'У вас Неуплата налогов оплатите {factory.tax} чтобы запустить фабрику',
                                                reply_markup=tax_markup)

        await call.message.answer('Рабочие приступили к работе')

        factory.start_work_at = current_time
        factory.state = 1
        await back_factory(call)
    else:
        await call.message.answer(f'Фабрике осталось работать {last_click + _time - current_time} секунд')


