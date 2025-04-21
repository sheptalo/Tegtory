import logging

from common.exceptions import AppException
from domain.results import Failure, Success
from domain.use_cases.commands.base import BaseCommandHandler
from infrastructure.di import container

logger = logging.getLogger(__name__)


class CommandExecutor:
    _instance = None
    handlers = {}

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def execute(self, command) -> Success | Failure:
        logger.error(self.handlers)
        return await self.handlers[type(command)](command)

    def register(self, command, handler):
        self.handlers[command] = self._get_wrapper(handler)

    def _get_wrapper(self, handler):
        async def wrapper(*args, **kwargs) -> Success | Failure:
            try:
                return Success(data=await handler(*args, **kwargs))
            except AppException as e:
                return Failure(reason=e.message)

        return wrapper


async def prepare_commands():
    logger.info("Preparing commands")
    executor = CommandExecutor()
    children = BaseCommandHandler.__subclasses__()
    for child in children:
        handler = await container.get(child)
        executor.register(handler.command_type, handler)
    logger.info("All commands registered")
