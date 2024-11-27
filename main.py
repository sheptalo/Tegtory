import asyncio
import logging

from middlewares.UserMiddleWare import UserMiddleWare

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from bot import bot, dp
from functions import lottery
from handlers import (
    menu,
    minigames,
    clanss,
    factory,
    user,
    start,
    ref,
    inline_handler,
    promo,
    city,
)

logging.basicConfig(level=logging.INFO)

dp.message.middleware(UserMiddleWare())


async def scheduler_start():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        lottery.lottery, CronTrigger(day_of_week="sat", hour=12, minute=0)
    )
    scheduler.start()


async def main():
    dp.include_routers(
        start.router,
        user.router,
        ref.router,
        menu.router,
        minigames.router,
        clanss.router,
        factory.router,
        inline_handler.router,
        promo.router,
        city.router,
    )
    cons = asyncio.create_task(scheduler_start())
    polling = asyncio.create_task(dp.start_polling(bot))
    await asyncio.gather(cons, polling)


if __name__ == "__main__":
    asyncio.run(main())
