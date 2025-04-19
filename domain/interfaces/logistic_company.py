from domain.entity import LogisticCompany

from .base import ICrudRepository


class ILogisticRepository(ICrudRepository[LogisticCompany]):
    async def find(self, shop: LogisticCompany) -> LogisticCompany | None:
        pass

    async def sign_contract(
        self, contract: LogisticCompany
    ) -> LogisticCompany:
        pass

    async def update_contract(
        self, contract: LogisticCompany
    ) -> LogisticCompany:
        pass
