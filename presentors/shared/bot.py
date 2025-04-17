from aiogram import Bot


class BotSingleton(Bot):
    _instance = None

    def __new__(cls, *args, **kwargs) -> Bot:
        if not cls._instance:
            cls._instance = Bot(*args, **kwargs)
        return cls._instance


class TegtorySingleton(BotSingleton):
    pass


class MynoxSingleton(BotSingleton):
    pass
