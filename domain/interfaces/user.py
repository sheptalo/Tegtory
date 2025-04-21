from typing import Protocol

from domain.entity import User
from domain.interfaces.base import CrudRepository


class UserRepository(CrudRepository[User]):
    pass


class UserMoneyRepository(Protocol):
    def subtract(self, user_id: int, amount: int):
        pass

    def add(self, user_id: int, amount: int):
        pass

    def send(self, from_user_id: int, to_user_id: int, amount: int):
        pass
