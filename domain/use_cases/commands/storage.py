from ...commands import UpgradeStorageCommand
from ...interfaces import UserRepository
from ...interfaces.storage import StorageRepository
from .base import BaseCommandHandler
from .pay_required import pay_required


@pay_required
class UpgradeStorageCommandHandler(BaseCommandHandler[UpgradeStorageCommand]):
    object_type = UpgradeStorageCommand

    def __init__(
        self, storage_repo: StorageRepository, money_repo: UserRepository
    ) -> None:
        self.storage_repo = storage_repo
        self.money_repo = money_repo

    async def execute(self, cmd: UpgradeStorageCommand) -> None:
        await self.storage_repo.upgrade(cmd.factory_id)
