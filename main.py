import os

from infrastructure.executor import preparing_executors
from infrastructure.events import register_events
from infrastructure.injectors import subscribe_all
from infrastructure.logger import configure_logger
from presentors import MynoxService, TegtoryService


async def main():
    aiogram = asyncio.create_task(TegtoryService(os.environ.get("BOT_TOKEN"))())
    mynox = asyncio.create_task(MynoxService(os.environ.get("MYNOX_TOKEN"))())
    await asyncio.gather(subscribe_all(), register_events(), preparing_executors(), aiogram, mynox)


if __name__ == "__main__":
    import asyncio

    from dotenv import load_dotenv

    configure_logger()
    load_dotenv()
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
