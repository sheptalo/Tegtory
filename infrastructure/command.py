from domain.results import Failure, Success
from domain.use_cases.commands.base import BaseCommandHandler
from infrastructure.executor import BaseExecutor


class CommandExecutor(BaseExecutor):
    handler_base_class = BaseCommandHandler

    async def execute(self, command) -> Success | Failure:
        return await self.handlers[type(command)](command)
