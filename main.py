import os

from infrastructure.injectors import subscribe_all
from infrastructure.logger import configure_logger
from infrastructure.registry import prepare_commands
from presentors import MynoxService, TegtoryService


async def main():
    aiogram = asyncio.create_task(
        TegtoryService(os.environ.get("BOT_TOKEN"))()
    )
    mynox = asyncio.create_task(MynoxService(os.environ.get("MYNOX_TOKEN"))())
    await asyncio.gather(subscribe_all(), prepare_commands(), aiogram, mynox)


if __name__ == "__main__":
    import asyncio

    from dotenv import load_dotenv

    configure_logger()
    load_dotenv()
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
