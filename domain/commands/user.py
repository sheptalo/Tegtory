from .base import BaseModel


class RegisterUserCommand(BaseModel):
    username: str
    name: str
    user_id: int
