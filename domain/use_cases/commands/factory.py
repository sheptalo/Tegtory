from common import settings
from common.exceptions import AppException
from domain.entity import Factory

from ...commands.factory import (
    CreateFactoryCommand,
    PayTaxCommand,
    UpgradeStorageCommand, UpgradeFactoryCommand, HireWorkerCommand,
)
from ...interfaces import (
    FactoryRepository,
    FactoryTaxRepository,
    UserMoneyRepository,
)
from .base import BaseCommandHandler, pay_required
from ...interfaces.factory import FactoryWorkersRepository
from ...interfaces.storage import StorageRepository


class CreateFactoryHandler(BaseCommandHandler):
    object_type = CreateFactoryCommand

    def __init__(self, repo: FactoryRepository, storage: StorageRepository):
        self.repo = repo
        self.storage = storage

    async def __call__(self, cmd: CreateFactoryCommand):
        if await self.repo.by_name(cmd.name):
            raise AppException("Фабрика с таким именем уже существует")

        factory = await self.repo.create(Factory(name=cmd.name, id=cmd.id))
        factory.storage = await self.storage.create(factory.id)

        for product in settings.DEFAULT_AVAILABLE_PRODUCTS:
            await self.repo.add_available_product(factory, product)
        return factory


@pay_required
class PayFactoryTaxHandler(BaseCommandHandler):
    object_type = PayTaxCommand

    def __init__(
        self, tax_repo: FactoryTaxRepository, money_repo: UserMoneyRepository
    ):
        self.tax_repo = tax_repo
        self.money_repo = money_repo

    async def __call__(self, cmd: PayTaxCommand):
        await self.tax_repo.remove_tax(cmd.factory_id)


@pay_required
class UpgradeStorageHandler(BaseCommandHandler):
    object_type = UpgradeStorageCommand

    def __init__(self, storage_repo: StorageRepository, money_repo: UserMoneyRepository):
        self.storage_repo = storage_repo
        self.money_repo = money_repo

    async def __call__(self, cmd: UpgradeStorageCommand):
        await self.storage_repo.upgrade(cmd.factory_id)


@pay_required
class UpgradeFactoryHandler(BaseCommandHandler):
    object_type = UpgradeFactoryCommand

    def __init__(self, factory_repo: FactoryRepository, money_repo: UserMoneyRepository):
        self.factory = factory_repo
        self.money_repo = money_repo

    async def __call__(self, cmd: UpgradeFactoryCommand):
        await self.factory.upgrade(cmd.factory_id)


@pay_required
class HireWorkerCommandHandler(BaseCommandHandler):
    object_type = HireWorkerCommand

    def __init__(self, repo: FactoryWorkersRepository, money_repo: UserMoneyRepository):
        self.repo = repo
        self.money_repo = money_repo

    async def __call__(self, cmd: HireWorkerCommand):
        if cmd.factory.hire_available <= 0:
            raise AppException("Вы достигли лимита рабочих для данного уровня")
        await self.repo.hire(cmd.factory.id)
