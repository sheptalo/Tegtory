from functools import wraps
from typing import Any

from common.exceptions import AppException

from ...commands.factory import PayRequiredCommand


def pay_required(cls: type) -> type:
    if not hasattr(cls, "execute"):
        raise AppException("Method execute must be overridden")

    old_call = cls.execute

    @wraps(old_call)
    async def wrapper(self: Any, cmd: PayRequiredCommand) -> Any:
        cmd.can_pay()
        result = await old_call(self, cmd)
        await self.money_repo.subtract(cmd.user_id, cmd.get_price())
        return result

    cls.execute = wrapper
    return cls
