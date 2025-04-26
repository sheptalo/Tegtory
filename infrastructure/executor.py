import logging
from typing import Any, Awaitable, Callable, Self, Type

from common.exceptions import AppException
from domain.results import Failure, Success

logger = logging.getLogger(__name__)


class BaseExecutor:
    _instance: Self
    handler_base_class: Type

    def __new__(cls) -> Self:
        if not cls._instance:
            cls._instance: Self = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, "handlers"):
            self.handlers: dict[
                Type, Callable[[Any], Awaitable[Success | Failure]]
            ] = {}

    def register(self, command: Type, handler: Callable) -> None:
        self.handlers[command] = self._get_wrapper(handler)

    def _get_wrapper(self, handler: Callable) -> Callable:
        async def wrapper(*args: tuple, **kwargs: dict) -> Success | Failure:
            try:
                return Success(data=await handler(*args, **kwargs))
            except AppException as e:
                return Failure(reason=e.message)

        return wrapper


async def preparing_executors() -> None:
    from infrastructure.di import container

    for executor in BaseExecutor.__subclasses__():
        logger.info(f"Preparing {executor.__name__}")
        instance = executor()
        children = executor.handler_base_class.__subclasses__()
        for child in children:
            handler = await container.get(child)
            instance.register(handler.object_type, handler)
        logger.info(f"{executor.__name__} Prepared")
