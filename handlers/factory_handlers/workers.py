from aiogram import F, types, Router

from api import api

from config import not_enough_points
from replys import hire_markup

from .work_yourself import work

router = Router()
max_workers = 'Максимальное количество работников на фабрике для данного уровня достигнуто, больше нанять не получится'


@router.callback_query(F.data == 'workers')
async def buy_workers(call: types.CallbackQuery):
    player = api.player(call.from_user.id)
    if player.isWorking:
        return await work(call)
    factory = api.factory(call.message.chat.id)
    workers_amount = factory.workers
    await call.message.edit_caption(caption=f'сейчас на Фабрике нанято {workers_amount} человек \n'
                                            f'Можно нанять {factory.lvl - workers_amount} \n'
                                            f'Стоимость найма {(1 + workers_amount) * 300}',
                                    reply_markup=hire_markup)


@router.callback_query(F.data == 'hire_worker')
async def hire_worker(call: types.CallbackQuery):
    player = api.player(call.from_user.id)
    factory = api.factory(call.message.chat.id)

    if factory.lvl == factory.workers:
        return await call.message.answer(max_workers)
    if player.money < (1 + factory.workers) * 300:
        return await call.message.answer(not_enough_points)
    player.money -= (1 + factory.workers) * 300
    factory.workers += 1
    await buy_workers(call)
