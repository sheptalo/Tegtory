from typing import Protocol

from domain.entity import LogisticCompany


class LogisticRepository(Protocol):
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
