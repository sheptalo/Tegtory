import asyncio
import logging

from middlewares.UserMiddleWare import UserMiddleWare

from bot import bot, dp
from db import console
from handlers import menu, shop, minigames, clanss, factory, user, start, ref, \
    inline_handler

logging.basicConfig(level=logging.INFO)

last_user = 0
last_button_click = 0

dp.message.middleware(UserMiddleWare())


async def main():
    print("Started")
    dp.include_routers(start.router, user.router, ref.router, menu.router,
                       shop.router, minigames.router, clanss.router,
                       factory.router, inline_handler.router)
    cons = asyncio.create_task(console())
    polling = asyncio.create_task(dp.start_polling(bot))
    await asyncio.gather(cons, polling)


if __name__ == "__main__":
    asyncio.run(main())
