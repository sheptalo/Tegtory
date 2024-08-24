import asyncio
import logging

from MIddleWares.UserMiddleWare import UserMiddleWare
from bot import bot, dp, con
from db import console
from handlers import menu, shop, minigames, clanss, factory, user, start, ref

logging.basicConfig(level=logging.INFO)

last_user = 0
last_button_click = 0

dp.message.middleware(UserMiddleWare())


async def ping_sql():
    while True:
        con.ping(True)
        await asyncio.sleep(30)


async def main():
    dp.include_router(user.router)
    dp.include_router(start.router)
    dp.include_router(ref.router)
    dp.include_router(menu.router)
    dp.include_router(shop.router)
    dp.include_router(minigames.router)
    dp.include_router(factory.router)
    dp.include_router(clanss.router)
    task = asyncio.create_task(ping_sql())
    cons = asyncio.create_task(console())
    polling = asyncio.create_task(dp.start_polling(bot))
    print("Started")
    await asyncio.gather(task, cons, polling)


if __name__ == "__main__":
    asyncio.run(main())
