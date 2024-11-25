import asyncio

from aiogram import types, Router, F
from bot import api

import time
import random

router = Router()


@router.callback_query(F.data == "work")
async def work(call: types.CallbackQuery):
    current_time = int(time.time())
    factory = api.factory(call.message.chat.id)
    player = api.player(call.from_user.id)
    working, last_click = player.get("isWorking,workedAt")
    _time = (factory.lvl + 3) * 5
    if not working or current_time - last_click >= _time:
        if working:
            return await work_finish(call)
        await call.answer(
            "Вы приступили к работе. "
            "Чтобы прекратить досрочно пишите отлучиться\n\nсовет:\n"
            "Если вы начали работать на фабрике в чате, "
            "то завершайте работать в нем же.",
            show_alert=True,
        )
        player.isWorking = 1
        player.workedAt = current_time
        _ = asyncio.create_task(work_timer(call, _time))

    else:
        await call.answer(
            f"вы работаете осталось {round(last_click + _time - current_time, 1)} секунд",
            show_alert=True,
        )


@router.message(F.text.lower().split()[0] == "отлучиться")
async def drop_work(message: types.Message):
    player = api.player(message.from_user.id)
    player.set({"isWorking": 0, "workedAt": 0})


async def work_finish(call):
    factory = api.factory(call.message.chat.id)
    player = api.player(call.from_user.id)
    lvl = factory.lvl
    created = (lvl + 1) * (5 + random.randint(0, 5))
    factory.stock += created
    factory.tax += created // 2
    player.set({"isWorking": 0, "workedAt": 0})
    await call.message.answer(f"Работа окончена! Произведено товаров: {created}")


async def work_timer(call, tme):
    await asyncio.sleep(tme)
    if api.player(call.from_user.id).isWorking:
        await work_finish(call)
