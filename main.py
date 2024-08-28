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
    print("Started")
    while True:
        con.ping(True)
        await asyncio.sleep(30)


async def main():
    dp.include_routers(start.router, user.router, ref.router, menu.router, shop.router, minigames.router, clanss.router,
                       factory.router)
    task = asyncio.create_task(ping_sql())
    cons = asyncio.create_task(console())
    polling = asyncio.create_task(dp.start_polling(bot))
    await asyncio.gather(task, cons, polling)


if __name__ == "__main__":
    asyncio.run(main())
