from typing import Any

import pytest

from common.exceptions import AppException
from domain.results import Failure
from domain.use_cases.queries.base import BaseQueryHandler


def raise_app_exception(cmd: Any) -> None:
    raise AppException


@pytest.mark.asyncio
async def test_base_query_handler_failure() -> None:
    handler: BaseQueryHandler[Any] = BaseQueryHandler()
    setattr(handler, "handle", raise_app_exception)

    result = await handler(0)

    assert isinstance(result, Failure)
