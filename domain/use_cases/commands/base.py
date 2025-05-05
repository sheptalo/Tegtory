from typing import Any, Generic, TypeVar

from common.exceptions import AppException

from ...commands.base import BaseCommand
from ...results import Failure, Success
from ..base import DependencyRequired

Command = TypeVar("Command", bound=BaseCommand)


class BaseCommandHandler(DependencyRequired, Generic[Command]):
    object_type: Any

    async def __call__(self, command: Command) -> Success | Failure:
        try:
            return Success(data=await self.execute(command))
        except AppException as e:
            return Failure(reason=e.message)

    async def execute(self, command: Command) -> Any:
        raise NotImplementedError
