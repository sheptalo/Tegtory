from typing import Self

from aiogram import Bot


class BotSingleton(Bot):
    _instance: Bot | None = None

    def __new__(cls, *args, **kwargs) -> Self:
        if not cls._instance:
            cls._instance = object.__new__(cls)
        return cls._instance


class TegtorySingleton(BotSingleton):
    pass


class MynoxSingleton(BotSingleton):
    pass
