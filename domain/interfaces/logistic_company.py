from domain.entity import LogisticCompany

from .base import ICrudRepository


class ILogisticRepository(ICrudRepository[LogisticCompany]):
    def find(self, shop: LogisticCompany) -> LogisticCompany | None:
        pass

    def sign_contract(self, contract: LogisticCompany) -> LogisticCompany:
        pass

    def update_contract(self, contract: LogisticCompany) -> LogisticCompany:
        pass
