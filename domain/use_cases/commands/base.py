from functools import wraps
from typing import Type

from pydantic import BaseModel

from domain.commands.factory import PayRequiredCommand


class BaseCommandHandler:
    command_type: BaseModel


def pay_required(cls: Type):
    old_call = cls.__call__

    @wraps(old_call)
    async def wrapper(self, cmd: PayRequiredCommand):
        cmd.can_pay()
        await old_call(self, cmd)
        self.money_repo.subtract(cmd.user_id, cmd.get_price())

    cls.__call__ = wrapper
    return cls
