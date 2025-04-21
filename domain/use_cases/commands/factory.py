from common import settings
from common.exceptions import AppException
from domain.entity import Factory

from ...commands.factory import (
    CreateFactoryCommand,
    PayTaxCommand,
    UpgradeStorageCommand,
)
from ...interfaces import (
    FactoryRepository,
    FactoryTaxRepository,
    UserMoneyRepository,
)
from .base import BaseCommandHandler, pay_required


class CreateFactoryHandler(BaseCommandHandler):
    command_type = CreateFactoryCommand

    def __init__(self, repo: FactoryRepository):
        self.repo = repo

    async def __call__(self, cmd: CreateFactoryCommand):
        if await self.repo.by_name(cmd.name):
            raise AppException("Фабрика с таким именем уже существует")

        factory = await self.repo.create(Factory(name=cmd.name, id=cmd.id))
        factory.storage = await self.repo.create_storage(factory)

        for product in settings.DEFAULT_AVAILABLE_PRODUCTS:
            await self.repo.add_available_product(factory, product)
        return factory


@pay_required
class PayFactoryTaxHandler(BaseCommandHandler):
    command_type = PayTaxCommand

    def __init__(
        self, tax_repo: FactoryTaxRepository, money_repo: UserMoneyRepository
    ):
        self.tax_repo = tax_repo
        self.money_repo = money_repo

    async def __call__(self, cmd: PayTaxCommand):
        self.tax_repo.remove_tax(cmd.factory_id)


@pay_required
class UpgradeStorageHandler(BaseCommandHandler):
    command_type = UpgradeStorageCommand

    def __init__(self, money_repo: UserMoneyRepository):
        self.storage_repo = 1
        self.money_repo = money_repo

    async def __call__(self, cmd: UpgradeStorageCommand):
        self.storage_repo
