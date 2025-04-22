from functools import wraps

from pydantic import BaseModel

from domain.commands.factory import PayRequiredCommand


class BaseCommandHandler:
    object_type: BaseModel


def pay_required(cls: type):
    old_call = cls.__call__

    @wraps(old_call)
    async def wrapper(self, cmd: PayRequiredCommand):
        cmd.can_pay()
        await old_call(self, cmd)
        await self.money_repo.subtract(cmd.user_id, cmd.get_price())

    cls.__call__ = wrapper
    return cls
