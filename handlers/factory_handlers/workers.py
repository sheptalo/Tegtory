from aiogram import F, types, Router

from db.Factory import Factory
from db.Player import Player

from config import not_enough_points
from replys import hire_markup

from .work_yourself import work_by_yourself

router = Router()
max_workers = 'Максимальное количество работников на фабрике для данного уровня достигнуто, больше нанять не получится'


@router.callback_query(F.data == 'workers')
async def buy_workers(call: types.CallbackQuery):
    player = Player(call.from_user.id)
    if player.is_working:
        return await work_by_yourself(call)
    factory = Factory(call.message.chat.id)
    workers_amount = factory.workers
    await call.message.edit_caption(caption=f'сейчас на Фабрике нанято {workers_amount} человек \n'
                                            f'Можно нанять {factory.level - workers_amount} \n'
                                            f'Стоимость найма {(1 + workers_amount) * 300}',
                                    reply_markup=hire_markup)


@router.callback_query(F.data == 'hire_worker')
async def hire_worker(call: types.CallbackQuery):
    player = Player(call.from_user.id)
    factory = Factory(call.message.chat.id)

    if factory.level == factory.workers:
        return await call.message.answer(max_workers)
    if player.money < (1 + factory.workers) * 500:
        return await call.message.answer(not_enough_points)
    player.money -= (1 + factory.workers) * 500
    factory.workers += 1
    await buy_workers(call)
