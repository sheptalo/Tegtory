import os

from infrastructure.events.events import subscribe_events
from infrastructure.executor import preparing_executors
from infrastructure.logger import configure_logger
from presenters import MynoxService, TegtoryService


async def main():
    aiogram = asyncio.create_task(
        TegtoryService(os.environ.get("BOT_TOKEN"))()
    )
    mynox = asyncio.create_task(MynoxService(os.environ.get("MYNOX_TOKEN"))())
    await asyncio.gather(
        preparing_executors(),
        subscribe_events(),
        aiogram,
        mynox,
    )


if __name__ == "__main__":
    import asyncio

    from dotenv import load_dotenv

    configure_logger()
    load_dotenv()
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
