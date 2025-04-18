from pydantic import BaseModel, ConfigDict

from domain.entity import Factory, User
from domain.use_cases import UCFactory, UCUser


class FactoryHolder(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    entity: Factory | None = None
    use_case: UCFactory


class UserHolder(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    entity: User
    use_case: UCUser
