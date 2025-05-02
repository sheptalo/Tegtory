from .base import BaseCommand


class RegisterUserCommand(BaseCommand):
    username: str
    name: str
    user_id: int
