from aiogram import types, Router, F
from api import api

import time
import random

router = Router()


@router.callback_query(F.data == 'work')
async def work(call: types.CallbackQuery):
    current_time = int(time.time())
    factory = api.factory(call.message.chat.id)
    player = api.player(call.from_user.id)
    last_click = player.workedAt
    _time = (factory.lvl + 3) * 5
    if not last_click or current_time - last_click >= _time:
        if player.isWorking:
            player.isWorking = 0
            return await work_finish(call)
        await call.message.answer('Вы приступили к работе. '
                                  'Чтобы прекратить досрочно пишите отлучиться\n\nсовет:\n'
                                  'Если вы начали работать на фабрике в чате, '
                                  'то завершайте работать в нем же.')
        player.isWorking = 1
        player.workedAt = current_time

    else:
        await call.message.answer(f'вы работаете осталось {round(last_click + _time - current_time, 1)} секунд')


@router.message(F.text.lower().split()[0] == 'отлучиться')
async def drop_work(message: types.Message):
    player = api.player(message.from_user.id)
    player.isWorking = 0
    player.workedAt = 0


async def work_finish(call):
    factory = api.factory(call.message.chat.id)
    lvl = factory.lvl
    created = (lvl + 1) * (5 + random.randint(0, 5))
    factory.stock += created
    await call.message.answer(f'Работа окончена! Произведено товаров: {created}')
    factory.tax += created // 2
