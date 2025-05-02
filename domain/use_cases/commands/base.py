from functools import wraps
from typing import Any, Generic, TypeVar

from common.exceptions import AppException

from ...commands.base import BaseCommand
from ...commands.factory import PayRequiredCommand
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


def pay_required(cls: type) -> type:
    old_call = cls.__call__

    @wraps(old_call)
    async def wrapper(self: Any, cmd: PayRequiredCommand) -> Any:
        cmd.can_pay()
        result = await old_call(self, cmd)
        await self.money_repo.subtract(cmd.user_id, cmd.get_price())
        return result

    setattr(cls, "__call__", wrapper)
    return cls
