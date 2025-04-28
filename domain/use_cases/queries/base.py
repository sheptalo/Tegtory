from domain.queries.base import BaseQuery
from domain.use_cases.base import DependencyRequired, SafeCall


class BaseQueryHandler(DependencyRequired, SafeCall):
    object_type: type[BaseQuery]
