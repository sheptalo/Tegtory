from pydantic import BaseModel

from common.exceptions import NotEnoughPointsException
from domain.entity import Storage
from domain.entity.factory import WorkersFactory


class FactoryRequiredCommand(BaseModel):
    factory_id: int


class CreateFactoryCommand(BaseModel):
    name: str
    id: int


class PayRequiredCommand(BaseModel):
    user_id: int
    user_money: int

    def can_pay(self):
        if self.user_money < self.get_price():
            raise NotEnoughPointsException()

    def get_price(self):
        raise NotImplementedError


class PayTaxCommand(PayRequiredCommand, FactoryRequiredCommand):
    factory_tax: int

    def get_price(self):
        return self.factory_tax


class UpgradeStorageCommand(PayRequiredCommand, FactoryRequiredCommand):
    storage: Storage

    def get_price(self):
        return self.storage.upgrade_price


class UpgradeFactoryCommand(PayRequiredCommand, FactoryRequiredCommand):
    factory_upgrade_price: int

    def get_price(self):
        return self.factory_upgrade_price


class HireWorkerCommand(PayRequiredCommand):
    factory: WorkersFactory

    def get_price(self):
        return self.factory.hire_price
