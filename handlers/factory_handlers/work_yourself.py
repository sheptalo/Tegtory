from aiogram import types, Router, F

from db import Player, Factory

import time
import random

router = Router()


@router.callback_query(F.data == 'work')
async def work_by_yourself(call: types.CallbackQuery):
    current_time = int(time.time())
    factory = Factory(call.message.chat.id)
    player = Player(call.from_user.id)
    last_click = player.work_at
    _time = (factory.level + 3) * 5
    if not last_click or current_time - last_click >= _time:
        if player.is_working:
            player.is_working = 0
            return await workbyyourself_finish(call)
        await call.message.answer('Вы приступили к работе. '
                                  'Чтобы прекратить досрочно пишите отлучиться\n\nсовет:\n'
                                  'Если вы начали работать на фабрике в чате, '
                                  'то завершайте работать в нем же.')
        player.is_working = 1
        player.work_at = current_time

    else:
        await call.message.answer(f'вы работаете осталось {round(last_click + _time - current_time, 1)} секунд')


@router.message(F.text.lower().split()[0] == 'отлучиться')
async def drop_work(message: types.Message):
    player = Player(message.from_user.id)
    player.is_working = 0
    player.work_at = 0


async def workbyyourself_finish(call):
    factory = Factory(call.message.chat.id)
    lvl = factory.level
    created = (lvl + 1) * (5 + random.randint(0, 5))
    factory.stock += created
    await call.message.answer(f'Работа окончена! Произведено товаров: {created}')
    factory.tax += created // 2
