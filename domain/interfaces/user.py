from domain.entity import User
from domain.interfaces.base import ICrudRepository


class IUserRepository(ICrudRepository[User]):
    pass
