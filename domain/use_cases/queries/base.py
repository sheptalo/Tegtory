from typing import Any, Generic, TypeVar

from common.exceptions import AppException
from domain.queries.base import BaseQuery
from domain.results import Failure, Success

from ..base import DependencyRequired

Query = TypeVar("Query", bound=BaseQuery)


class BaseQueryHandler(DependencyRequired, Generic[Query]):
    object_type: type[BaseQuery]

    async def __call__(self, query: Query) -> Success | Failure:
        try:
            return Success(data=await self.execute(query))
        except AppException as e:
            return Failure(reason=e.message)

    async def execute(self, query: Query) -> Any:
        raise NotImplementedError
