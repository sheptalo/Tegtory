import logging

from aiogram import Dispatcher
from aiogram.client.default import DefaultBotProperties
from dishka.integrations.aiogram import setup_dishka

from infrastructure.di import dishka_container
from presentors.shared.middlewares.chat_action import ChatActionMiddleware
from presentors.shared.middlewares.register_user import AuthMiddleware

logger = logging.getLogger(__name__)


class BaseService:
    bot_singleton = None
    message_middlewares = [
        AuthMiddleware(),
        ChatActionMiddleware(),
    ]
    callback_middlewares = [AuthMiddleware()]

    def __init__(self, bot_token: str = None):
        self.bot = self._get_bot(bot_token)
        self._dp = None

    async def __call__(self, *args, **kwargs):
        if not self.bot:
            return
        self.prepare_handlers()
        setup_dishka(dishka_container, self.dp)
        await self.dp.start_polling(self.bot, skip_updates=True)

    def prepare_handlers(self):
        pass

    @property
    def dp(self):
        if hasattr(self, "_dp") and self._dp:
            return self._dp
        dp = Dispatcher()
        for middleware in self.message_middlewares:
            dp.message.middleware.register(middleware)
        for middleware in self.callback_middlewares:
            dp.callback_query.middleware.register(middleware)
        self._dp = dp
        return dp

    @classmethod
    def _get_bot(cls, token: str = None):
        if not token:
            logger.error("No bot token provided for %s", cls.__name__)
            return
        return cls.bot_singleton(
            token=token,
            default=DefaultBotProperties(parse_mode="Markdown"),
        )
