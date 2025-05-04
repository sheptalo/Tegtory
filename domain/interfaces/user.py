from domain.entities import User
from domain.interfaces.base import CrudRepository


class UserRepository(CrudRepository[User]):
    async def subtract(self, user_id: int, amount: int) -> None:
        pass

    async def add(self, user_id: int, amount: int) -> None:
        pass

    async def send(
        self, from_user_id: int, to_user_id: int, amount: int
    ) -> None:
        pass
