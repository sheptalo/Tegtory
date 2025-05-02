from pydantic import BaseModel

from domain.entities.user import User


class Association(BaseModel):
    title: str
    description: str
    owner: User


class AssociationParticipant(BaseModel):
    association: Association
    participant: User
    role: str
    contributed: int = 0
