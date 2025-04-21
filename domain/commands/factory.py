from pydantic import BaseModel

from common.exceptions import NotEnoughPointsException
from domain.entity import Storage


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


class PayTaxCommand(PayRequiredCommand):
    factory_id: int
    factory_tax: int

    def get_price(self):
        return self.factory_tax


class UpgradeStorageCommand(PayRequiredCommand):
    storage: Storage

    def get_price(self):
        return self.storage.upgrade_price

