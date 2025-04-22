import logging

from common.exceptions import AppException
from domain.results import Success, Failure

logger = logging.getLogger(__name__)


class BaseExecutor:
    _instance = None
    handler_base_class = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "handlers"):
            self.handlers = {}

    def register(self, command, handler):
        self.handlers[command] = self._get_wrapper(handler)

    def _get_wrapper(self, handler):
        async def wrapper(*args, **kwargs) -> Success | Failure:
            try:
                return Success(data=await handler(*args, **kwargs))
            except AppException as e:
                return Failure(reason=e.message)

        return wrapper


async def preparing_executors():
    from infrastructure.di import container
    for executor in BaseExecutor.__subclasses__():
        logger.info(f"Preparing {executor.__name__}")
        instance = executor()
        children = executor.handler_base_class.__subclasses__()
        for child in children:
            handler = await container.get(child)
            instance.register(handler.object_type, handler)
        logger.info(f"{executor.__name__} Prepared")
