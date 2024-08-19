import asyncio
import logging

from aiogram import types, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

from MIddleWares.UserMiddleWare import UserMiddleWare
from bot import bot, dp, con
from config import welcome
from db import console
from handlers import menu, shop_btns, leaderboard, minigames, admin, clanss, checkUser, change_nick, factory
from replys import menu_reply

logging.basicConfig(level=logging.INFO)

last_user = 0
last_button_click = 0


@dp.message(Command("cancel"))
async def cancel(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer('отменено')


@dp.message(Command("start"))
async def start_func(message: types.Message):
    await message.answer(welcome, reply_markup=menu_reply, parse_mode='HTML')


@dp.message(F.text == 'Я подписался')
async def check_text(message: types.Message):
    await message.answer(f'Вижу. удачной игры', reply_markup=menu_reply)

dp.message.middleware(UserMiddleWare())


async def ping_sql():
    while True:
        con.ping(True)
        await asyncio.sleep(30)


async def main():
    dp.include_router(checkUser.router)
    dp.include_router(change_nick.router)
    dp.include_router(menu.router)
    dp.include_router(shop_btns.router)
    dp.include_router(leaderboard.router)
    dp.include_router(minigames.router)
    dp.include_router(admin.router)
    dp.include_router(factory.router)
    dp.include_router(clanss.router)
    task = asyncio.create_task(ping_sql())
    cons = asyncio.create_task(console())
    polling = asyncio.create_task(dp.start_polling(bot))
    print("Started")
    await asyncio.gather(task, cons, polling)


if __name__ == "__main__":
    asyncio.run(main())
