from ..shared.base_service import BaseService
from ..shared.bot import MynoxSingleton


class MynoxService(BaseService):
    bot_singleton = MynoxSingleton

    def prepare_handlers(self):
        pass
