import logging

from domain.queries.base import BaseQuery
from domain.results import Failure, Success
from domain.use_cases.queries.base import BaseQueryHandler
from infrastructure.executor import BaseExecutor

logger = logging.getLogger(__name__)


class QueryExecutor(BaseExecutor):
    handler_base_class = BaseQueryHandler

    async def ask(self, query: BaseQuery) -> Success | Failure:
        logger.info(f"Executing command: {query.__class__.__name__}({query})")
        return await self.handlers[type(query)](query)
