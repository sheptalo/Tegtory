import logging

from domain.entity import User
from domain.interfaces import UserMoneyRepository, UserRepository

logger = logging.getLogger(__name__)
_users: list[User] = []


def _filter_users(user_id: int) -> User | None:
    for i in filter(lambda u: u.id == user_id, _users):
        return i
    return None


class UserRepositoryImpl(UserRepository):
    async def get(self, user_id: int) -> User:
        return _filter_users(user_id)

    async def create(self, user: User) -> User:
        logger.info(f"Creating user {user.id} with name {user.name}")
        _users.append(user)
        return user

    async def update(self, user: User) -> User:
        return user


class UserMoneyRepositoryImpl(UserMoneyRepository):
    async def send(self, from_user_id: int, to_user_id: int, amount: int) -> None:
        pass

    async def subtract(self, user_id: int, amount: int) -> None:
        user = _filter_users(user_id)
        if user:
            logger.error(f"Subtracting user {user_id} with amount {amount}")
            user.money -= amount
            logger.error(user)

    async def add(self, user_id: int, amount: int) -> None:
        user = _filter_users(user_id)
        if user:
            user.money += amount
