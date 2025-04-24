from domain.use_cases.base import DependencyRequired


class BaseQueryHandler(DependencyRequired):
    object_type = None
