from functools import wraps
from typing import Any

from ...commands.factory import PayRequiredCommand
from ..base import DependencyRequired


class BaseCommandHandler(DependencyRequired):  # TODO добавить wrapper на call
    object_type: Any


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
