from typing import Protocol

from domain.entity import User


class IUserRepository(Protocol):
    def get(self, user_id: int) -> User:
        pass

    def create(self, uid: int, name: str, username: str) -> User:
        pass

    def update(self, user: User) -> User:
        pass
