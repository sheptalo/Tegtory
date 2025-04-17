import logging

from domain.entity import User
from domain.interfaces import IUserRepository

logger = logging.getLogger(__name__)


class UserRepository(IUserRepository):
    def __init__(self):
        self.users = []

    def get(self, user_id: int) -> User:
        return self._filter_users(user_id)

    def create(self, uid: int, name: str, username: str) -> User:
        logger.info(f"Creating user {uid} with name {name}")
        user = User(id=uid, name=name, username=username)
        self.users.append(user)
        return user

    def update(self, user: User) -> User:
        pass

    def _filter_users(self, user_id: int) -> User | None:
        for i in filter(lambda u: u.id == user_id, self.users):
            return i
        return None
