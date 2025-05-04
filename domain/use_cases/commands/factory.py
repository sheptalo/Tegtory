from common.exceptions import AppException
from domain.entities import Factory, Product

from ...commands.factory import (
    CreateFactoryCommand,
    HireWorkerCommand,
    PayTaxCommand,
    UpgradeFactoryCommand,
    UpgradeStorageCommand,
)
from ...interfaces import FactoryRepository, UserRepository
from ...interfaces.storage import StorageRepository
from .base import BaseCommandHandler, pay_required

DEFAULT_AVAILABLE_PRODUCTS: list[Product] = [
    Product(
        name="Стулья",
        price_multiply=0.8,
        time_to_create=100,
        amount_multiply=0.8,
    ),
    Product(
        name="Кирпичи",
        price_multiply=0.9,
        time_to_create=160,
        amount_multiply=0.6,
    ),
    Product(
        name="Древесный Уголь",
        price_multiply=0.6,
        time_to_create=30,
        amount_multiply=1.2,
    ),
]


class CreateFactoryHandler(BaseCommandHandler[CreateFactoryCommand]):
    object_type = CreateFactoryCommand

    def __init__(
        self, repo: FactoryRepository, storage: StorageRepository
    ) -> None:
        self.repo = repo
        self.storage = storage

    async def execute(self, cmd: CreateFactoryCommand) -> Factory:
        if await self.repo.by_name(cmd.name):
            raise AppException("Фабрика с таким именем уже существует")

        factory = await self.repo.create(Factory(name=cmd.name, id=cmd.id))
        factory.storage = await self.storage.create(factory.id)

        for product in DEFAULT_AVAILABLE_PRODUCTS:
            await self.repo.add_available_product(factory, product)
        return factory


@pay_required
class PayFactoryTaxHandler(BaseCommandHandler[PayTaxCommand]):
    object_type = PayTaxCommand

    def __init__(
        self, repo: FactoryRepository, money_repo: UserRepository
    ) -> None:
        self.repo = repo
        self.money_repo = money_repo

    async def execute(self, cmd: PayTaxCommand) -> None:
        await self.repo.set_tax(cmd.factory_id, 0)


@pay_required
class UpgradeStorageHandler(BaseCommandHandler[UpgradeStorageCommand]):
    object_type = UpgradeStorageCommand

    def __init__(
        self, storage_repo: StorageRepository, money_repo: UserRepository
    ) -> None:
        self.storage_repo = storage_repo
        self.money_repo = money_repo

    async def execute(self, cmd: UpgradeStorageCommand) -> None:
        await self.storage_repo.upgrade(cmd.factory_id)


@pay_required
class UpgradeFactoryHandler(BaseCommandHandler[UpgradeFactoryCommand]):
    object_type = UpgradeFactoryCommand

    def __init__(
        self, factory_repo: FactoryRepository, money_repo: UserRepository
    ) -> None:
        self.factory = factory_repo
        self.money_repo = money_repo

    async def execute(self, cmd: UpgradeFactoryCommand) -> None:
        await self.factory.upgrade(cmd.factory_id)


@pay_required
class HireWorkerCommandHandler(BaseCommandHandler[HireWorkerCommand]):
    object_type = HireWorkerCommand

    def __init__(
        self, repo: FactoryRepository, money_repo: UserRepository
    ) -> None:
        self.repo = repo
        self.money_repo = money_repo

    async def execute(self, cmd: HireWorkerCommand) -> None:
        cmd.factory.hire()
        await self.repo.hire(cmd.factory.id)
