from domain.commands.base import BaseCommand
from domain.results import Failure, Success
from domain.use_cases.commands.base import BaseCommandHandler
from infrastructure.executor import BaseExecutor


class CommandExecutor(BaseExecutor):
    handler_base_class: type[BaseCommandHandler] = BaseCommandHandler

    async def execute(self, command: BaseCommand) -> Success | Failure:
        return await self.handlers[type(command)](command)
