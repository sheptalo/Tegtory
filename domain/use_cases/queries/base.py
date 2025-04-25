from domain.queries.base import BaseQuery
from domain.use_cases.base import DependencyRequired


class BaseQueryHandler(DependencyRequired):
    object_type: BaseQuery
